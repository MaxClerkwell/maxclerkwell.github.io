Manage the unstructured thought files in the `thoughts/` directory of this repository. Each thought is a Markdown file named with a UUID (`thoughts/<uuid>.md`) with frontmatter fields: `id`, `created`, `title`, `tags`, and a body.

**IMPORTANT:** Thoughts are NOT articles. Never move, publish, convert, or reference any thought file into `_articles/` or `posts/` unless the user explicitly asks you to do so in this conversation.

The argument passed is: $ARGUMENTS

---

## Subcommands

### `list`
Read all files in `thoughts/`. For each one, extract `title` and `tags` from the frontmatter. Output a clean numbered list:
```
1. <title>  [tag1, tag2]
2. ...
```
Group them by the most prominent shared tag if natural groupings exist. No extra commentary.

---

### `new`
The text following `new` in $ARGUMENTS is the raw thought to store. If no text follows, ask the user to state their thought now and wait.

Steps:
1. Generate a new UUID (use `uuidgen` via Bash).
2. Get today's date via Bash.
3. Derive a short English title from the thought text.
4. Derive relevant tags (lowercase, kebab-case).
5. Read all existing thought files in `thoughts/` and identify any that are thematically related to this new thought. List them in a `crossrefs` frontmatter field as a YAML list of UUIDs.
6. Write the new file to `thoughts/<uuid>.md` with this structure:

```markdown
---
id: <uuid>
created: <date>
title: "<derived title>"
tags: [tag1, tag2]
crossrefs:
  - <uuid-of-related-thought>
---

<the raw thought, lightly cleaned up — fix typos, preserve meaning exactly>
```

7. Report back: the title, the file created, and which cross-references were found (show their titles, not just UUIDs).

---

### `overview`
Read all files in `thoughts/`. Identify which thoughts represent actionable next steps (article to write, project to build, task to complete, decision to make) vs. pure ideas with no clear action yet.

Output two sections:
**Ready to act on** — thoughts that have enough shape to start working on, ordered by apparent priority or momentum.
**Still incubating** — thoughts that need more thinking before they become tasks.

Keep it brief. One line per thought. No filler.

---

### `questions`
Read all files in `thoughts/`. Analyze the full set of topics, positions, and gaps. Generate exactly 5 questions that would most expand the knowledge graph — questions whose answers would create new nodes, challenge existing assumptions, or connect currently isolated clusters.

Format:
```
1. <question>
   -> relates to: <thought title(s)>
```

Make the questions sharp and specific, not generic. Avoid questions the existing thoughts already answer.
