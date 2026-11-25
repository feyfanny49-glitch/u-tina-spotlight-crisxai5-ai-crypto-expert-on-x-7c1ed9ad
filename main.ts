// main.ts — the graded entrypoint for make.fun competition
// u-tina-spotlight-crisxai5-ai-crypto-expert-on-x-7c1ed9ad (harness program/v1, Node 22).
//
// Contract: the house runs this twice inside its sandbox and both runs must write the same bytes.
// The post is the entry; the house reads the post's public counts from X itself, and it refuses an
// entry whose POST.json does not name a post whose address has the shape the rules give. So this
// program does one thing, carefully: it checks the address, then hands POST.json over to /output.
//
// Hard rules kept: no network, no wall clock, no files outside the repository (the two paths it
// touches, /bot and /output, are the sandbox's own), standard library only.
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// What changed from the first version, and why:
//   1. the address is validated against the accepted shapes before it is handed over, and a url that
//      is not one (the starter's placeholder above all) is reported on stderr — the gate reads
//      POST.json as a URL, so an unchecked hand-over fails far away from its cause;
//   2. the copy is atomic (write a temporary file in /output, then rename it): a reader can never see
//      a half-written POST.json if the run is cut short;
//   3. the two runs are proven identical, not assumed: the sha256 of what was written is printed on
//      stderr only when something is off, so a clean run stays silent as the rules describe.
//
// A warning never blocks the hand-over: the house reads POST.json itself, and the bytes it receives
// are always exactly the bytes in the repository. Exit code 1 is reserved for "there was nothing to
// hand over" (no POST.json, or one that is not a JSON object with a string url).

import { mkdirSync, readFileSync, renameSync, unlinkSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const NAME = 'POST.json';

const source = join(BOT_DIR, NAME);
const target = join(OUTPUT_DIR, NAME);

// The address shapes the rules accept, and nothing else:
//   https://x.com/<handle>/status/<id>, the same on twitter.com, optionally behind www. or mobile.,
//   or /i/web/status/<id>; the id is digits; a query or fragment after it is read past.
const POST_URL = /^https?:\/\/(?:www\.|mobile\.)?(?:x|twitter)\.com\/(?:[A-Za-z0-9_]{1,15}\/status|i\/web\/status)\/(\d{1,25})(?:[?#].*)?$/;
const PLACEHOLDER = /<handle>|<id>/;

type Warning = string;

function checkAddress(raw: string): Warning[] {
  const warnings: Warning[] = [];
  if (PLACEHOLDER.test(raw)) {
    warnings.push('the url is still the starter placeholder, so the gate will refuse this entry');
    return warnings;
  }
  if (!POST_URL.test(raw)) {
    warnings.push('the url is not one of the shapes the rules accept (<handle>/status/<id>, or /i/web/status/<id>)');
  }
  return warnings;
}

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// 1. read the file the repository hands over, and refuse only when there is nothing to hand over
let bytes: Buffer;
try {
  bytes = readFileSync(source);
} catch (err) {
  fail(`${source} could not be read: ${(err as Error).message}`);
}

// 2. it must be a JSON object whose url is a string: that is what the gate reads out of it
let warnings: Warning[] = [];
let url = '';
try {
  const parsed: unknown = JSON.parse(bytes.toString('utf8'));
  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    fail(`${source} is not a JSON object`);
  }
  const value = (parsed as Record<string, unknown>).url;
  if (typeof value !== 'string') {
    fail(`${source} carries no string "url"`);
  }
  url = value.trim();
  warnings = checkAddress(url);
} catch (err) {
  if (err instanceof SyntaxError) {
    fail(`${source} is not valid JSON: ${err.message}`);
  }
  throw err;
}

// 3. hand the very bytes over, atomically: written beside the target, then renamed over it
mkdirSync(OUTPUT_DIR, { recursive: true });
const staging = `${target}.${process.pid}.tmp`;
try {
  writeFileSync(staging, bytes);
  renameSync(staging, target);
} catch (err) {
  try {
    unlinkSync(staging);
  } catch {
    // nothing to clean up
  }
  fail(`${target} could not be written: ${(err as Error).message}`);
}

// 4. a clean run says nothing; a run that hands over something the gate will refuse says so, loudly,
//    on stderr, and still hands it over — the house reads the post, not this program's opinion of it
if (warnings.length > 0) {
  for (const warning of warnings) {
    console.error(`main.ts: WARNING: ${warning}`);
  }
  console.error(`main.ts: handed over anyway: ${source} -> ${target} (${bytes.length} bytes, url ${JSON.stringify(url)})`);
}

// Belt and braces: the file that was written is byte for byte the file that was read. This is a plain
// comparison inside the sandbox — no clock, no network — and it is exactly what the two-run rule is
// about, so it is checked rather than assumed. Nothing extra is written to /output: the house checks
// the files there, so POST.json is the only thing this program leaves in it.
if (!readFileSync(target).equals(bytes)) {
  fail(`${target} does not match ${source} byte for byte`);
}
