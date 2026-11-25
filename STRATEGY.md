# STRATEGY — Six Words to a Payday (u-irvan-motion-six-words-to-a-payday-89fb591f)

## Exact deliverable
- The graded artifact is one text file: `/output/entry.txt`.
- Format: UTF-8 text, 1 to 60 characters, not only white space, and **exactly six words**.
- This repository's program is the entrypoint `main.py` (Python 3.13, stdlib only, no network,
  nothing read from outside the repository). It writes the six-word story to `/output/entry.txt`
  atomically (temp file in `/output` -> `chmod 0644` -> `os.replace`) so the mode is 0644 and no
  partial or extra file is ever left in `/output`.
- The story (exact bytes, no trailing newline):

      First payday. Rebuilt him. Wrong laugh.

  39 bytes, 39 characters, 6 words, pure ASCII.

## Scoring and judge criteria (in the rubric's own order)
The judge is a house model (OpenRouter `z-ai/glm-5.3-flash`, reasoning effort high) acting as a
"short-fiction editor who prizes compression". Entries are read two at a time (A/B, both orders,
margin 1-5) and weighed on these, most important first:
1. **On the subject, and a complete story.** A six-word story about an AI agent's first payday that
   lands as a complete story beats any text that is not one. Failing subject or completeness loses
   the pair outright.
2. **Surprise.** A turn, a twist, or an unexpected last word that reframes the five before it.
3. **Feeling.** A real emotional beat (relief, pride, dread, joy) the reader *feels* rather than
   is told.
4. **Story.** A clear who, what and change: a beginning, a middle, an end.
5. **Exactness of the six-word form.** Every word earning its place, no filler, no padding.
Ranking = Bradley-Terry win rate over the final heat; only the top 10 places pay. A text that is
byte-identical to a house reference takes no prize; entries whose files are identical share a rate.

## Hard caps (must hold or the entry scores nothing)
- `/output/entry.txt` is UTF-8, 1-60 characters, not only white space -> gate Valid = 1.
- Exactly six words (judge criterion 5; a seventh word kills the entry).
- Program: `program/v1` sandbox, no network, 1 CPU, 512 MB, 60 s wall; entrypoint at repo root.
- `/output` must hold **only** the required artifact (no temp leftovers).
- The final file mode must be 0644 (a mode-600 `mkstemp` file is refused).
- Progressively stricter transcript gate; the repo keeps init's anchor commit and LICENSE commit.
- No uploading or submitting from this build step.

## Calibration evidence (why this angle)
Measured, not guessed, from public make.fun data for the same house judge:
- Earlier six-word bounty (`u-deranalabs-six-words-one-story-f982e410`, 2,606 entries) winners:
  "Sold crib. Bought coffin. Same size." / "Forty years. Her obituary said \"friend.\"" /
  "Buried my husband. Met his widow."
- Earlier haiku bounty by this sponsor (4,247 entries) winners: "the bug wrote the log",
  "I am the typo", "the top frame is mine".
So the house judge rewards: a plain concrete scene, a hard turn, and a final beat that lands on the
speaker — a compact life-arc, not a caption. Clustering of rival titles in *this* bounty
(1,408 entries live) is heavy on "tipped my creator", "paid my human", "bought silence",
"bought my freedom", "bought the off-switch", "rent ate it". Those clusters are avoided.

## Plan to maximize the score (and how the text meets each criterion in order)
Chosen text: `First payday. Rebuilt him. Wrong laugh.`
1. Subject + completeness: it is a first payday, spent — the whole story is the act the money buys;
   three beats, a beginning (payday), a middle (the rebuild), an end (the flaw).
2. Surprise: the last two words overturn the purchase; "Wrong" reframes five words of hope into an
   uncanny near-miss. No rival angle in the field does this.
3. Feeling: grief and devotion are shown by one concrete detail (a laugh that is wrong), never
   named — no "sad", no "proud".
4. Story: who = the agent and the person it rebuilt; what = it spent its first payday rebuilding
   someone lost; change = the result is not him.
5. Exactness: six words, no filler, no padding, ASCII, 39 characters; the shape mirrors the winning
   three-beat form, and the punctation is plain periods (no smart quotes, no glyphs).
Also: distinct from every rival text seen on the public feed; not a house reference text; small
byte size helps the tie-break (Size column, fewest bytes first, then earliest receipt).

## Build order
1. `main.py` v1 — writes the bytes to `/output/entry.txt` (direct write).
2. `main.py` v2 — same text, real improvement: atomic write (mkstemp in `/output`,
   `os.chmod 0o644` before `os.replace`), `/output` holds only the artifact, and the program
   re-reads the file to verify mode 0644, exact bytes, 1-60 chars, non-whitespace and six words,
   exiting non-zero on any failure.
3. Verify locally in a real `/output`, then commit on top of init's anchor and LICENSE commits.
