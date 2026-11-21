---
name: draft-post-from-recording
description: Turn a voice memo into a published bilingual blog post. Use when the author uploads an audio recording (m4a, mp3, wav) and asks for it to be organised into a post or draft.
---

# Draft a post from a recording

The author records loose spoken notes. The ideas are theirs and the order is not. The job is to give the ideas a structure, keep their voice, and get both language versions published. Follow the Writing Style section of `AGENTS.md` throughout.

## 1. Transcribe

Copy the upload to a scratch directory, then run the script next to this file:

```bash
uv run .claude/skills/draft-post-from-recording/transcribe.py RECORDING > sensevoice.txt
uv run .claude/skills/draft-post-from-recording/transcribe.py RECORDING --model whisper > whisper.txt
```

The first run downloads about 1.6 GB of models from GitHub releases into `~/.cache/blog-transcribe`. A ten-minute memo takes about a minute per model on four cores.

Use the SenseVoice output for the Chinese wording and the Whisper output for English names, article titles and product names. Neither is reliable for proper nouns alone.

## 2. Check what the recording refers to

The author usually reacts to things they have read. Before writing:

- Find each article, post or incident mentioned, and confirm its exact title, author, date and URL.
- Read the piece the author is responding to in full. The recording paraphrases from memory, so compare each claim attributed to it against the text.
- Fix details that the source contradicts and tell the author which ones changed. Flag anything that could not be verified.

## 3. Write the Chinese draft

- Open with the author's own argument. Background and summaries of other people's writing come later and stay short.
- Regroup the spoken points by topic. Do not add claims the author did not make; if an argument needs a step they skipped, raise it with them first.
- Create `content/posts/<slug>-cn.md` with the usual metadata. Leave `Status: draft` off so the Cloudflare preview renders it.
- Run the CI build, commit, push, and open a PR that says it is not ready to merge. Give the author the preview URL.

## 4. Revise with the author

The author edits the file on the PR branch and often rewrites headings and endings in their own voice. Fetch before every edit and keep their wording. When they ask for ideas, offer angles and let them pick, then weave in the chosen ones without changing the sections they have already rewritten.

## 5. Write the English version

Start only after the author approves the Chinese text.

- Create `content/posts/<slug>.md` with the same `Date`, and cross-link the two files as described in `AGENTS.md`.
- Translate for meaning. Chinese idioms and literary allusions rarely survive literally: rewrite them, and list every place where the English departs from the Chinese when handing the draft over.
- Keep both versions in step. A structural change to one is made to the other in the same commit.

## 6. Publish

Merge only when the author says to. Squash-merge, wait for the Cloudflare deploy, then confirm both article URLs and their preview cards under `/og/` return 200.
