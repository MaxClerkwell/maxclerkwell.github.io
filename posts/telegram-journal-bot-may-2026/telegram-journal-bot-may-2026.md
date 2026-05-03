---
layout: post
title: "Building a Personal Journal Bot with Telegram, Gemini, and Docker"
date: 2026-05-03
tags: [telegram, gemini, docker, journaling, llm, python, latex, obsidian]
description: "I spent a day building a Dockerized Telegram bot that turns voice messages and scattered thoughts into a structured journal, Obsidian topic notes, and a compiled LaTeX memoir — and what I learned about LLM APIs along the way."
permalink: /posts/telegram-journal-bot-may-2026/
---

I have been meaning to journal consistently for years. The friction has never been motivation — it has always been the blank page. Opening a text editor, deciding on a format, remembering what happened, structuring it. By the time I have done all of that, the thought I wanted to capture has either sharpened itself into something obvious or dissolved entirely.

So I built a bot that does the structuring for me.

## What it does

You send a message to a Telegram bot. The bot asks you one follow-up question. You answer. It might ask another. After two or three exchanges it writes a journal entry, extracts a topic note in Obsidian-compatible markdown, and commits both to a private git repository.

Voice messages get transcribed. Photos get analysed — Gemini looks at the image and asks what drew your attention there, or what you were trying to capture. The bot remembers what you have been thinking about over the past week and uses that as background context when deciding what to ask next.

At 23:30 each night it compiles the day's entries into a LaTeX chapter. Every Saturday afternoon it sends a written summary of the week and a compiled PDF of the memoir via Telegram.

Todos work too. "I need to call the doctor tomorrow" gets classified as a todo for tomorrow's date, not a journal entry. Uncompleted todos roll over to the next day at 22:00.

The whole thing runs as a Docker container on a cheap VPS. One-command setup.

## The conversation design

The follow-up question approach took a few iterations to feel right.

The first version generated all questions upfront — three at once, delivered as a list. It felt like filling in a form. The thought I had was already gone by the time I finished answering question three.

The second version asked one question at a time, but generated the next question without looking at what had already been answered. So it would ask about context, I would explain, and then it would ask about context again from a different angle. Repetitive.

The version that works generates each question fresh, with the full history of what has been said so far. The prompt instructs the model to decide whether there is still one genuinely worthwhile thing to ask — or to declare itself done. For technical or project-related thoughts it asks about decisions and next steps. For personal or emotional thoughts it tries to deepen understanding rather than extract facts. If it decides enough has been covered, it returns the string `DONE` and the bot moves straight to writing.

It caps out at three rounds regardless. Three turns of back-and-forth is usually enough to turn a half-formed thought into something writable.

## The context system

The quality of follow-up questions improves significantly with context. "I'm stuck on the auth refactor again" is a much more useful starting point if the bot knows that you spent the last three days working on that refactor than if it has no background at all.

After the daily memoir chapter is compiled, the bot saves a compact bullet-point summary of the day — not the full entries, just the key themes, decisions, and open questions. These summaries are loaded as background context when generating follow-up questions.

The context rolls up over time:

- Every Sunday: a weekly summary is built from that week's daily summaries
- The 1st of every month: a monthly summary is built from the weekly summaries
- January 1st: a yearly summary is built from the monthly summaries

None of this is visible to you unless you open the files. It just makes the questions better.

## On the Gemini API

I had not used the Google Gemini API before this project. A few things I learned:

The SDK changed. The old `google-generativeai` package is deprecated. The new one is `google-genai` — note the missing `ative` — with a completely different import and client structure: `from google import genai`, then `genai.Client(api_key=...)`. If you find yourself looking at FutureWarning messages about this, switch packages.

Model names are a moving target. In the course of a single day I had 404 errors from `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`, and `gemini-2.5-flash-preview-04-17`. The model that works is `gemini-2.5-flash`. Without the preview suffix, without a date suffix.

For anyone hitting quota limits on the free tier: `gemma-3-4b-it` is available through the same API key and has a significantly higher quota. The tradeoff is that it does not support multimodal input — no voice transcription, no image analysis. But for pure text journaling it works well.

The multimodal API for audio is straightforward once the model name is right. You send the raw audio bytes with a mime type of `audio/ogg` and ask for a transcription. Gemini handles Telegram's voice message format without any conversion.

## The LaTeX memoir

This part was more annoying than expected, in an instructive way.

`pdflatex` needs to be run from the directory containing `main.tex`, not from a temp directory. The reason is that `\input{chapters/2026-05-03}` is a relative path — it resolves correctly when the working directory is `memoir/`, and fails with "file not found" when it is anything else. The fix is `subprocess.run(..., cwd=str(memoir_dir))` rather than running from a temporary directory.

The `microtype` package causes a crash with some font setups unless you disable expansion explicitly: `\usepackage[protrusion=true,expansion=false]{microtype}`. This is not obvious from the error message.

The LaTeX chapter style prompt went through two iterations. The first generated chapters in a reflective, somewhat literary style — long paragraphs, metaphors, the kind of writing that sounds like someone trying to write well. I did not want that. The second prompt specifies: sober, direct, one idea per paragraph, no embellishment, report what happened. The results are considerably more useful for actually remembering what was going on.

## The SSH key handling

The bot runs in a Docker container and needs to push to a private git repository via SSH. Getting this to work cleanly took longer than the LLM integration.

The issue is that `/root/.ssh` in the container is mounted as read-only (so the host keys cannot be written back), but SSH wants to write `known_hosts`. The solution is to copy the keys to a writable temp location in the entrypoint script, add GitHub's known hosts there manually, and point SSH at that location via `GIT_SSH_COMMAND`.

Additionally, SSH will prefer `authorized_keys` over actual identity files if it finds them — so the entrypoint explicitly tries `id_rsa`, then `id_ed25519`, then `id_ecdsa` in order, rather than letting SSH pick arbitrarily.

Git in newer versions also refuses to operate on repositories owned by a different user. Running the container as root and cloning into `/repo` means you need `git config --global --add safe.directory /repo` before any git operations.

## The repository structure

After a few weeks of use, the journal repository looks like this:

```
journal/         — daily markdown files
topics/          — Obsidian-compatible topic notes, one per extracted concept
attachments/     — photos, organised by date
memoir/          — LaTeX source and chapter files
  main.tex
  chapters/
context/         — compact summaries for the bot's memory
  2026-05-03.md
  weeks/
  months/
  years/
todos/           — JSON files, one per day
```

The topics directory is the part I find most interesting over time. A topic file for, say, `deep-work` gets a new dated section every time you mention something related to it. After a few months you have a document that shows how your thinking on a subject evolved — which decisions you made, which ones you revisited, what changed. Obsidian can render these with the full backlink graph.

## What is missing

A few things I did not build today that would make this more complete:

**Editing**. There is no way to correct an entry after it has been written. You would have to open the git repository and edit the file directly.

**Search**. The bot can write and commit, but cannot answer "what did I write about X last month?" — that would require either an embedding index or a smarter read path.

**Multiple users**. The bot is single-user by design — it checks the chat ID against an environment variable and ignores everything else. Making it multi-user would require persistent state per user, which the current in-memory state dict does not support.

## Running it

The repository is at [github.com/MaxClerkwell/telegram_journal_bot](https://github.com/MaxClerkwell/telegram_journal_bot). The README has the full setup walkthrough — BotFather, Google AI Studio API key, deploy keys, the works. The short version:

```bash
git clone git@github.com:MaxClerkwell/telegram_journal_bot.git
cd telegram_journal_bot
bash setup.sh
vim .env
docker compose up -d
```

If you build something on top of this or find something broken, the issues tab is open.
