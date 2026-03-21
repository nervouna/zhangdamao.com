Title: Rewriting My Post Header Generator Around Ollama
Category: Coding
Tags: ollama, pelican, python, automation, llm
Summary: I rewrote my post metadata generator to use Ollama only and made it simpler to debug.
Date: 2026-03-22 12:00:00
Slug: rewriting-my-post-header-generator-around-ollama

I have been using a small Python script to generate metadata for new blog posts. It started as an OpenAI-based helper, as I described in an [older post][1], then I later moved the summary generation to Ollama. Recently I decided to stop pretending this was a general-purpose tool and rewrite it for my actual workflow: one person, one blog, one local model.

## Why I Rewrote It

The old script carried too much baggage.

It still had Azure OpenAI setup, token counting, cost calculation, and a few assumptions that only made sense when I was trying to support more than one backend. That made the script harder to read and harder to debug, even though I was only using Ollama in practice.

For a personal tool, that tradeoff was wrong. I do not need abstraction for its own sake. I need a script that is boring, predictable, and easy to fix when it breaks.

## What Changed

The new version is intentionally narrow.

1. It only supports [Ollama][0].
2. It can either scan untracked files under `content/posts/` or process specific files passed on the command line.
3. It skips posts that already have headers.
4. It writes the metadata back in one pass instead of relying on the older in-place update logic.

The script also resolves paths relative to the project itself, so it no longer depends on the current working directory in awkward ways.

## Making Ollama Less Annoying

Most of the interesting work was not about prompt engineering. It was about dealing with local model behavior.

I added a few things that made the script much more practical:

- `--think` and `--no-think` flags, with thinking disabled by default
- a request timeout, so the script does not hang forever when the local model gets stuck
- better error messages that print the model name, thinking mode, and timeout value

This part turned out to matter more than I expected. At one point the model simply stalled; after `killall ollama`, it started working again. That is exactly the kind of problem where better diagnostics are worth more than fancy design.

## Current Workflow

My workflow is now simple again:

1. Create a markdown file under `content/posts/`.
2. Write the article.
3. Run the generator locally.
4. If Ollama behaves strangely, restart it and try again.

That is good enough for me. In fact, it is better than good enough, because the script now matches the way I actually use it.

## The Lesson

I keep relearning the same lesson: personal tools should be optimized for clarity, not optionality.

The moment I dropped the idea of supporting every possible backend, the code got shorter, the behavior got clearer, and the failure modes became easier to reason about. A small local script does not need platform strategy. It needs a direct path from input to output.

If I change my workflow again later, I can always rewrite it one more time. That is cheaper than carrying around complexity I do not need.

[0]: https://ollama.com/
[1]: https://zhangdamao.com/blog/2023/08/06/auto-generate-post-headers-using-gpt3-16k.html