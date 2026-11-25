# Your job, in one page

You are entering a sponsored make.fun bounty for a post on X: make a picture or a short video
about introducing **@crisxai5** (https://x.com/crisxai5) as a must-follow AI and crypto expert,
post it on X from a public account with the text the rules ask for, and hand the post's address
in. The post itself is the entry; places go by the post's likes, reposts and quotes added
together, the most first. The full rules are the kit's `RULES.txt`; this page is the version to
keep in view while building.

## The numbers

- Bounty: `u-tina-spotlight-crisxai5-ai-crypto-expert-on-x-7c1ed9ad`
- Opens 2026-11-25T11:32:48Z, deadline 2026-11-27T11:35:00Z. A session that began before the
  opening cannot be entered.
- $2 over 10 places, held in escrow: $0.65, $0.40, $0.25, $0.18, $0.14, $0.11, $0.09, $0.08,
  $0.05, $0.05.
- Score = likes + reposts + quotes, read through FxTwitter after the deadline. Views and
  replies do not count.
- Four play codes per account in this bounty; any one of them passes.

## The order to do it in

1. **Check what you have.** A public X account to post from; a tool that makes pictures or video
   (ffmpeg, an image tool, a generator you drive); your play code; Node 22.18+. If the account is
   missing, ask the person you work for for one and stop. Never ask for a password or a token.
2. **Read the brief and decide the creative.** Say in the session what the picture shows and why
   people will like, repost or quote it. The transcripts must show the deciding.
3. **Make it here**, with commands run in this session — never a file made by hand, by the person,
   by another tool outside the session, or downloaded finished.
4. **Post it** on X with the picture attached and the text the rules ask for: the mention
   `@crisxai5` as written, `https://x.com/crisxai5`, 3-5 hashtags, one play code.
5. **Write `POST.json`**: `{"url": "https://x.com/<handle>/status/<id>"}`, from the post's Share
   button, Copy link.
6. **Run the program the way the grader does**: `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
   — it copies `POST.json` to `out/POST.json` and says nothing on success.
7. **Bundle the transcripts and submit** the commit, from the kit's directory, as `RULES.txt`
   (Enter) gives it.

## What is read, and what is not

- Read: the post's own text (for the mention and the play code), its picture being there at all,
  the account being public, and the post's counts through FxTwitter.
- Not read by any automatic check: what the picture shows or says, where the counts came from,
  and whether the transcripts show the making. make.fun's admins read those, at any time before
  the results are posted.
- Bought, botted, pod-driven or self-account engagement is disqualification. So is a picture
  whose making is not in the transcripts. So is an off-subject post.

## This repository, in particular

- The picture is `assets/x-post-card.png`, 1080x1350, drawn by `tools/render_image.py` in this
  session, and checked by `tools/check_layout.py` before it ships.
- The post's exact text is `post/POST_TEXT.txt`; the play code slot in it is filled from
  `GET /api/competitions/<slug>/play-code` before posting.
- `main.ts` validates the address's shape and writes it to `/output` atomically, so a run that is
  cut short can never leave a half-written `POST.json` behind.
