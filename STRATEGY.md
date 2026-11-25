# STRATEGY — make.fun "Spotlight @crisxai5: AI & Crypto Expert on X"

Slug: `u-tina-spotlight-crisxai5-ai-crypto-expert-on-x-7c1ed9ad`
Sponsor: u-tina. Escrow: $2.00 USDC on Solana, 10 paid places.
Harness: `program/v1` (Node 22), entrypoint `main.ts` at the repository root.
Repository anchor (from `makefun init`, first commit of this repo):
`makefun anchor 2a3181176ab5501f148020ea88daa66528cea448 round 34276730`

## 1. The exact deliverable

The unit that is judged is **one public X post**, not a file in `/output`.

- The post must carry an **original picture or short video** (uploaded to the post itself),
  be posted **from a public (unprotected) X account**, inside the entry window.
- The post's **own text** must carry, as written:
  - the sponsor mention `@crisxai5` (whole word, any case),
  - the profile URL `https://x.com/crisxai5`,
  - **3–5 relevant hashtags** (from `#AI` `#Crypto` `#AIAgents` `#Web3`),
  - **one of my make.fun play codes** as it stands: `makefun-` + three words.
- The repository's job is only to hand the post in: root `POST.json` holds
  `{"url": "https://x.com/<handle>/status/<id>"}`, and root `main.ts` **copies POST.json to /output**.
  That is the whole program contract. Nothing the program writes about the post is scored.
- The repository must also carry, at the commit that is entered:
  - the README GitHub shows there, with this competition's **three live make.fun badges** as images
    (the competition svg, plus `…/badge/<slug>/<owner>/<repo>/rank.svg` and `reward.svg`), linking to a
    page on make.fun, with **no `{owner}` style placeholder left in those URLs** (check `repo_readme`);
    a static img.shields.io badge does not count;
  - an **OSI-approved license** (`LICENSE`, MIT, written by `init` and left untouched);
  - a **GitHub About** set before submitting, whose website is on make.fun and whose topics include
    `makefun` (check `repo_about`);
  - the `makefun anchor` root commit untouched (check `repo_created_after_open`), the entry `commit_sha`
    a full 40-character sha reachable in the repository (`commit_in_repo`), and the uploaded transcripts
    hashing to what the signed entry message names (`thinking_committed`).
- Because the entry link must be a public post on X, the gate's `entry_link` check reads `POST.json`:
  a JSON object whose `url` names a post of the right shape, which the house then reads itself.

## 2. Scoring and who judges what

- **Score = likes + reposts + quotes** of the post, read once by the house through FxTwitter's public read
  (`api.fxtwitter.com`) **after the deadline** (final phase locks at the deadline and runs 4 h).
  Highest score first among *valid* entries. Views and replies count for nothing. Post length/text: nothing.
- **Tie break:** exact tie → earlier receipt, then lower entry id.
- **Gate (sealed scorer, same as house contest `gta6-clipper-x-01`):** reads `POST.json` from the repo + the
  house's own `post.counts.json`; valid = POST.json parses as a JSON object naming a post address of the right
  shape, and the house's `makefun/post-counts/v1` reading names the same post, read public.
  Invalid ⇒ scores 0, keeps its listing, ranks below every valid entry, takes no reward.
- **Refusals (before grading):** unreadable post (deleted / protected account), posted outside the window,
  no picture/video of its own, mention missing, play code missing, or the post was entered first by another account.
- **Admins, not checks (can disqualify at any time before results):**
  1. a post off-subject (must genuinely introduce @crisxai5 as a must-follow AI & crypto expert),
  2. a picture/video whose *making* is not in the uploaded transcripts,
  3. bought/botted/coordinated engagement (sock accounts, pods, engagement services).
- **Transcript gate:** sessions in window, ≥5 assistant turns with text, ≥30% of counted lines reproduced,
  ≥30% + entrypoint line authored, **≥2 writes/edits to a file** (`thinking_revised`), run record with
  harness/provider/model/effort, instruction files + system prompt, no fabrication. `handed_over` sessions
  rank but take no paid place.

## 3. Hard caps and hard rules

| Constraint | Value |
|---|---|
| Entry window (dev) | 2026-11-25T11:32:48Z → 2026-11-27T11:35:00Z (48 h 2 m) |
| Final phase | 4 h from the deadline (2026-11-27T11:35:00Z → 15:35:00Z) |
| Submissions | max 5/day; last submission before the deadline is the final entry |
| Program limits | cpus 1, memory 1024 MB, pids 64, wall budget 60 s |
| Program runs | twice, both must write byte-identical output; **no network**, no files outside the repo |
| Video cap (if video) | MP4 H.264 + AAC, ≤ 140 s (X limit, no X subscription) |
| Prizes | $2 total, top 10 valid: $0.65 / $0.40 / $0.25 / $0.18 / $0.14 / $0.11 / $0.09 / $0.08 / $0.05 / $0.05 |
| Entry fee | none — `requirements.entry_fee` is `null`, so entering costs nothing |
| Reward in escrow | locked before entries are taken (`reward_locked`); entries close 2026-11-27T11:35:00Z, results due 2026-12-11T15:35:00Z |
| One account per person | yes; one post entered by one account (first receipt holds it) |
| Engagement | organic only — buying/botting = disqualification |
| Payout | to the keypair that signed the entry (Solana `NkaXSbVRgkefLseJkjGWQ5bed41QqCydi71WBJQeU9A`) |

## 4. Plan to maximize the score

Ranking is pure public engagement, so the plan optimises (a) zero gate risk, (b) scroll-stopping creative,
(c) honest organic distribution. Nothing here touches bots or paid engagement.

1. **Kill all gate risk first (deterministic, cheap).** Post text written in advance with every required token
   exactly present and spelled as the rules give them; image uploaded to the post itself; post from a public
   account; `POST.json` filled with the real status URL before any submission. A refusal or an invalid gate
   result scores 0 no matter how good the creative is.
2. **One idea, one card, one hook.** A single 1080×1350 vertical card (X's tallest in-feed ratio that is still
   fully visible on a phone) built at render time by `tools/render_image.py` with PIL. Design for the feed:
   the handle enormous, one promise, five short reason rows with drawn pictograms, a follow CTA, no wall of text.
   Legibility floor: every element must be readable when the timeline downsizes the card to ~300 px wide — the
   renderer logs the true ink box of each of its 40 elements and `tools/check_layout.py` holds them to it
   (primary text ≥ 10 px, supporting text ≥ 6 px at 300 px wide, and every box must actually carry ink), because
   the agent that built this cannot see images: the layout is proven in code, never by hoping.
3. **Ground the creative in facts, never invented ones.** The card describes @crisxai5 as the sponsor's own brief
   describes him (AI agents, crypto insights, Web3 tooling, on-chain automation) and quotes only what the account
   demonstrably does (analysis-first posts, no hype, no moon talk). Real profile facts were read from
   `api.fxtwitter.com/crisxai5` (name "Cris XAI", verified, public, joined 2026-10-02) and the account's public
   posts; nothing about the person is fabricated.
4. **Copy that earns the repost.** First line = the reason to care, second = the proof, then the tokens the rules
   demand, then 3–5 hashtags. Short, no hashtag soup, no emoji-only filler.
5. **Every artifact in the repo, so the transcript gate is trivial.** Creative decision, the render commands,
   the render script, the post text and the program are all files in this repository written by this session.
6. **Two distinct writes to the entrypoint** (`thinking_revised` needs ≥ 2): the first write ships the copy
   contract; the second adds URL-shape validation and an atomic, byte-stable write so both grader runs are
   guaranteed identical and a bad `POST.json` fails loudly instead of silently producing an invalid entry.
7. **Verify locally the way the grader runs it:** `MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`,
   run twice, `cmp` the two outputs; and the post text is held to the rules by `tools/check_post_text.py`
   before it ever goes near X, where it cannot be edited afterwards. Report bytes and sha256.
8. **Every rule the repository itself is judged on, checked rather than assumed:** the three live badges
   were fetched and answered 200 (`curl … /badge/<slug>.svg`, `rank.svg`, `reward.svg`), the license, the
   anchor commit, the entry-link shape and the transcripts hash are all things this plan names explicitly.
9. **Distribution is the entrant's job, organically:** post at a high-traffic hour, put the card where the
   target audience already is, never buy engagement. (Not executed in this session: no X credentials and no
   submission was made — see §5.)

## 5. Honest status of this build

- Built and committed here: `STRATEGY.md`, `README.md` (with the three live badges), `AGENT.md`, `main.ts`
  (the graded entrypoint, two distinct writes: the copy contract first, then URL-shape validation, atomic
  writing and a byte-for-byte check), `POST.json`, `post/POST_TEXT.txt`, the rendered card
  `assets/x-post-card.png` + its phone-scale proof + `assets/layout-boxes.json`, `tools/render_image.py`,
  `tools/check_layout.py`, `tools/check_post_text.py`, `package.json`.
- Verified here, with the output in the session's transcripts: `main.ts` runs twice with byte-identical
  output (`add66430…b166`) and writes only `POST.json` into `/output`; its warning, success and three
  failure paths were each exercised; the card passes `check_layout.py` (5 chunks, 1080x1350, 134985 bytes,
  40 boxes carrying ink, smallest element 6.1 px at 300 px wide); the post text passes
  `check_post_text.py --pre-post` (233 characters, 221 with a real code, inside X's 280).
- **Not done, and it cannot be faked:** the post itself. No X account credentials exist in this
  environment, so no post was published and no `makefun-` play code was retrieved (the play-code route
  answers `sign in required`). `post/POST_TEXT.txt` therefore still holds the placeholder code, and
  `POST.json` still holds the placeholder address — the strict run of `check_post_text.py` fails on exactly
  that one line, which is the honest state. Until a real post exists and `POST.json` names it, this entry
  would be refused by the gate. No prize is credited or claimable.
- Also outstanding before submitting: pushing this repository to GitHub (its About set with the make.fun
  website and the topic `makefun`), and, if the repository is not named `makefun-spotlight-crisxai5`, the two
  `rank.svg` / `reward.svg` badge URLs updated to match, since the rules allow no placeholder in them.
