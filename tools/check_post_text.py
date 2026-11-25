#!/usr/bin/env python3
"""Hold the post's text to this bounty's rules before it ever goes near X.

RULES.txt is explicit about what the post's OWN text must carry:
  * `@crisxai5` -- "the sponsor's mention, as written, in any case, as a whole word (inside a
    longer word it does not count)";
  * one make.fun play code: `makefun-` and three words, as it stands;
  * the brief's extras: the profile url https://x.com/crisxai5 and 3-5 relevant hashtags.

This reads the block between the dashed rulers in post/POST_TEXT.txt and checks all of that, plus
the character count against the 280 a free X account is limited to. It exits 1 and prints one line
per failure otherwise, so a post can be checked in the session that wrote it instead of on X,
where the text cannot be edited afterwards.

Usage:
    python3 tools/check_post_text.py [--file post/POST_TEXT.txt] [--pre-post]

`--pre-post` is for checking the repository as it stands before the post exists: the placeholder
play code is then a note rather than a failure, and everything else still has to pass.
"""

from __future__ import annotations

import argparse
import re
import sys

DASHES = re.compile(r"^-{20,}\s*$", re.M)
MENTION = re.compile(r"(?<![0-9A-Za-z_])@crisxai5(?!\w)", re.I)
PROFILE_URL = re.compile(r"https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/crisxai5\b", re.I)
HASHTAG = re.compile(r"(?<!\w)#([0-9A-Za-z_]+)")
PLAY_CODE = re.compile(r"(?<![\w-])makefun-([a-z]+(?:-[a-z]+)*)", re.I)
PLACEHOLDER = "REPLACE-WITH-YOUR-PLAY-CODE"
SAMPLE_CODE = "tide-vault-loom"   # a code of the shape the rules describe, for the length estimate
X_LIMIT = 280
WANTED_TAGS = {"ai", "crypto", "aiagents", "web3"}


def post_text(path: str) -> str:
    raw = open(path, encoding="utf-8").read()
    blocks = DASHES.split(raw)
    if len(blocks) < 3:
        raise SystemExit("no text block between dashed rulers found in %s" % path)
    return blocks[1].strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="post/POST_TEXT.txt")
    ap.add_argument("--pre-post", action="store_true",
                    help="the post does not exist yet: the placeholder play code is a note, not a failure")
    args = ap.parse_args()

    text = post_text(args.file)
    flat = re.sub(r"\s+", " ", text)
    posted = flat.replace("REPLACE-WITH-YOUR-PLAY-CODE", SAMPLE_CODE)
    errs: list[str] = []
    notes: list[str] = []

    print("post text as written (%d characters):" % len(flat))
    for line in text.splitlines():
        print("  | %s" % line)
    print()
    print("length with a real %d-character code in place: %d characters (X's limit is %d)"
          % (len("makefun-" + SAMPLE_CODE), len(posted), X_LIMIT))
    print()

    if MENTION.search(text):
        print("ok         mention @crisxai5 present as a whole word")
    else:
        errs.append("the mention @crisxai5 is missing, or buried inside a longer word")

    if PROFILE_URL.search(text):
        print("ok         profile url https://x.com/crisxai5 present")
    else:
        errs.append("the profile url https://x.com/crisxai5 is missing")

    tags = [t.lower() for t in HASHTAG.findall(text)]
    if 3 <= len(tags) <= 5:
        print("ok         %d hashtags, inside the 3-5 the brief wants: %s" % (len(tags), " ".join("#" + t for t in tags)))
    else:
        errs.append("%d hashtags, outside the 3-5 the brief wants" % len(tags))
    missing = WANTED_TAGS - set(tags)
    if missing:
        notes.append("hashtags the brief names that are absent (not required, worth considering): %s"
                     % " ".join(sorted("#" + m for m in missing)))
    else:
        print("ok         covers every hashtag the brief names (#AI #Crypto #AIAgents #Web3)")

    codes = PLAY_CODE.findall(text)
    if not codes:
        errs.append("no play code: the text must carry one makefun- code")
    elif PLACEHOLDER in text:
        message = ("the play code is still the placeholder %s -- fill it from "
                   "GET /api/competitions/<slug>/play-code before posting" % PLACEHOLDER)
        if args.pre_post:
            notes.append(message)
        else:
            errs.append(message)
    else:
        words = [len(c.split("-")) for c in codes]
        if any(w == 3 for w in words):
            print("ok         play code present with three words: %s" % ", ".join("makefun-" + c for c in codes))
        else:
            errs.append("play code present but not makefun- plus three words: %s" % ", ".join(codes))

    if len(flat) > X_LIMIT:
        errs.append("the text is %d characters, over the %d a free X account may post" % (len(flat), X_LIMIT))

    for note in notes:
        print("note       %s" % note)
    if errs:
        print("\nFAIL (%d)" % len(errs))
        for e in errs:
            print(" - %s" % e)
        return 1
    print("\nPASS: the text carries the mention, the url, the hashtags and a play code, and fits in one post")
    return 0


if __name__ == "__main__":
    sys.exit(main())
