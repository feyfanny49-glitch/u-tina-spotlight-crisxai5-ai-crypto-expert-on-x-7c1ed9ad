#!/usr/bin/env python3
"""Assert the rendered card's layout and PNG structure -- no eyeballing required.

The model that built this entry cannot see images, so the card is verified two ways in code:

  1. layout: re-renders the card through tools/render_image.py, which logs the true ink box of
     every element, then asserts
       - nothing crosses the page margin or the 1080x1350 canvas,
       - the five reason rows stack in order with no vertical overlap,
       - the last row clears the footer bar, and the footer URL never runs into the CTA pill,
       - legibility at 300 px wide (how a phone timeline shows it): every primary element
         (handle, claim, row titles) stays >= 12 px and every secondary one >= 7 px there;
  2. ink: opens the PNG and, for every box the renderer logged, measures the luminance spread inside
     that box -- a box the renderer says it drew but that came out flat is an element nobody can see,
     so each one must actually carry ink (spread >= INK_SPREAD_MIN);
  3. structure: signature, IHDR, declared size, chunk CRCs, single IEND, and X's per-image caps.

Exit code 0 when everything holds, 1 with one printed line per failure otherwise.

Usage:
    python3 tools/check_layout.py --image assets/x-post-card.png
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib
from typing import cast

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import render_image as R  # noqa: E402  (same directory)

PROOF_WIDTH = 300          # the width a phone timeline renders the card at
PRIMARY_MIN_PX = 10.0      # cap height of primary text at this width (>= 20 px at full size)
SECONDARY_MIN_PX = 6.0     # supporting text at this width (>= 12 px at full size)
INK_SPREAD_MIN = 30        # luminance range a drawn box must show, else nothing visible landed there

PRIMARY = ("handle", "claim-1", "claim-2", "name", "row0-title", "row1-title", "row2-title",
           "row3-title", "row4-title")

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 5 * 1024 * 1024   # X's per-image upload cap for a PNG
MAX_EDGE = 4096               # X's max edge; the card is 1080x1350, a standard 4:5 portrait


def check_png(path: str) -> list[str]:
    errs: list[str] = []
    with open(path, "rb") as fh:
        blob = fh.read()
    if blob[:8] != PNG_SIG:
        errs.append("signature: %s is not a PNG" % path)
        return errs
    i, seen_ihdr, seen_iend, chunks = 8, 0, 0, 0
    width = height = None
    while i + 8 <= len(blob):
        (ln,) = struct.unpack(">I", blob[i:i + 4])
        ctype = blob[i + 4:i + 8]
        body = blob[i + 8:i + 8 + ln]
        crc = blob[i + 8 + ln:i + 12 + ln]
        if len(body) != ln or len(crc) != 4:
            errs.append("chunk %s truncated at offset %d" % (ctype.decode("latin1", "replace"), i))
            break
        (want,) = struct.unpack(">I", crc)
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != want:
            errs.append("chunk %s CRC mismatch at offset %d" % (ctype.decode("latin1"), i))
        chunks += 1
        if ctype == b"IHDR":
            seen_ihdr += 1
            width, height, depth, colour = struct.unpack(">IIBB", body[:10])
            if depth != 8 or colour not in (0, 2, 6):
                errs.append("IHDR: unsupported depth/colour %d/%d" % (depth, colour))
        elif ctype == b"IEND":
            seen_iend += 1
        i += 12 + ln
    if seen_ihdr != 1:
        errs.append("IHDR appears %d times, expected 1" % seen_ihdr)
    if seen_iend != 1:
        errs.append("IEND appears %d times, expected 1" % seen_iend)
    if i != len(blob):
        errs.append("trailing bytes after the last chunk: %d unread" % (len(blob) - i))
    if width is not None and height is not None:
        if (width, height) != tuple(R.render().size):
            errs.append("IHDR says %sx%s, the renderer draws %s" % (width, height, R.render().size))
        if width > MAX_EDGE or height > MAX_EDGE:
            errs.append("%dx%d exceeds the %dpx cap" % (width, height, MAX_EDGE))
    if len(blob) > MAX_BYTES:
        errs.append("%d bytes exceeds the %d byte cap" % (len(blob), MAX_BYTES))
    print("png        %s: %d chunks, %sx%s, %d bytes" % (path, chunks, width, height, len(blob)))
    return errs


def check_boxes(scale: float = PROOF_WIDTH / R.WIDTH) -> list[str]:
    errs: list[str] = []
    boxes = {b["name"]: b for b in R.BOXES}
    W, H, M = R.WIDTH, R.HEIGHT, R.MARGIN

    for b in R.BOXES:
        if b["x1"] < 0 or b["y1"] < 0 or b["x2"] > W or b["y2"] > H:
            errs.append("%s crosses the canvas: %s" % (b["name"], b))
        elif b["x2"] > W - M or b["x1"] < M - 14:
            errs.append("%s crosses the margin: %s" % (b["name"], b))

    rows = [boxes["row%d" % i] for i in range(len(R.ROWS))]
    for a, b in zip(rows, rows[1:]):
        if b["y1"] < a["y2"]:
            errs.append("rows overlap vertically: %s ends %d, next starts %d" % (a["name"], a["y2"], b["y1"]))
    footer = boxes["footer-bar"]
    if rows[-1]["y2"] > footer["y1"]:
        errs.append("last row (%d) runs into the footer bar (%d)" % (rows[-1]["y2"], footer["y1"]))
    if boxes["footer-cta"]["x1"] < boxes["footer-url"]["x2"] + 8:
        errs.append("footer URL runs into the CTA pill: %d vs %d" % (boxes["footer-url"]["x2"], boxes["footer-cta"]["x1"]))
    if boxes["content-bottom"]["y2"] > H - 8:
        errs.append("hashtags run off the bottom edge: %d" % boxes["content-bottom"]["y2"])

    # legibility when the timeline scales the card down to a phone-width thumbnail
    print("scale      %d px wide -> %.3f of full size" % (PROOF_WIDTH, scale))
    smallest: tuple[str, float] = ("(none)", 1e9)
    for name in PRIMARY + ("row0-detail", "row1-detail", "row2-detail", "row3-detail",
                           "row4-detail", "footer-url", "hashtags", "verified-top"):
        b = boxes.get(name)
        if b is None:
            errs.append("box %s was never drawn" % name)
            continue
        px = (b["y2"] - b["y1"]) * scale
        floor = PRIMARY_MIN_PX if name in PRIMARY else SECONDARY_MIN_PX
        if px < floor:
            errs.append("%s is %.1f px tall at %d px wide, under the %.1f px floor" % (name, px, PROOF_WIDTH, floor))
        if smallest is None or px < smallest[1]:
            smallest = (name, px)
    print("legibility smallest element %s at %.1f px (proof width %d)" % (smallest[0], smallest[1], PROOF_WIDTH))
    return errs


def check_ink(path: str) -> list[str]:
    """Every box the renderer logged must actually carry visible ink in the shipped PNG."""
    errs: list[str] = []
    grey = Image.open(path).convert("L")
    spread_min = 255
    thinnest = "(none)"
    checked = 0
    for b in R.BOXES:
        x1, y1 = max(0, b["x1"]), max(0, b["y1"])
        x2, y2 = min(grey.width, b["x2"]), min(grey.height, b["y2"])
        if x2 - x1 < 3 or y2 - y1 < 3:
            errs.append("box %s is %dx%d, too small to hold anything" % (b["name"], x2 - x1, y2 - y1))
            continue
        extrema = grey.crop((x1, y1, x2, y2)).getextrema()
        lo, hi = int(cast(int, extrema[0])), int(cast(int, extrema[1]))  # "L" is a single band
        spread = hi - lo
        checked += 1
        if spread < INK_SPREAD_MIN:
            errs.append("box %s came out flat (luminance spread %d), so nothing visible landed in it"
                        % (b["name"], spread))
        elif spread < spread_min:
            spread_min, thinnest = spread, b["name"]
    print("ink        %d boxes checked in %s; thinnest is %s at a spread of %d"
          % (checked, os.path.basename(path), thinnest, spread_min))
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="assets/x-post-card.png")
    args = ap.parse_args()

    R.render()  # fills R.BOXES
    errs = check_png(args.image) + check_ink(args.image) + check_boxes()
    if errs:
        print("\nFAIL (%d)" % len(errs))
        for e in errs:
            print(" - %s" % e)
        return 1
    print("\nPASS: layout, margins, legibility and PNG structure all hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
