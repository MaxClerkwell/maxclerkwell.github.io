# CLAUDE.md

> **Note for Claude Code**: This project uses `AGENTS.md` as the primary instruction file for all AI coding agents.
>
> This file exists only for backward compatibility with Claude Code. Please read [AGENTS.md](AGENTS.md) instead.

All project-specific guidance for AI agents lives in `AGENTS.md`.

## SEO, JSON-LD and llms.txt (mandatory for every new article)

The site is a Jekyll blog served from GitHub Pages under the custom domain
**https://maxclerkwell.tech** (see `CNAME`); author and site owner is
**Stephan Bökelmann** (alias MaxClerkwell).

Machine readability (structured data for search engines, llms.txt for LLM
crawlers) is a first-class requirement here, not an afterthought. It is driven
entirely by post front matter, so an incomplete front matter block silently
degrades the JSON-LD and the llms.txt entry.

### Checklist "new blog post"

When creating a new post in `_articles/<kebab-slug>.md`, ALWAYS fill the
front matter completely:

```yaml
---
title: "Post Title"                     # required, becomes headline/name in JSON-LD
date: YYYY-MM-DD                        # required, ISO date, becomes datePublished
author: "Stephan Bökelmann"             # optional; falls back to site.author.name
description: "One-sentence summary."    # required, feeds JSON-LD description, post card, llms.txt
tags: [tag1, tag2]                      # optional, becomes JSON-LD keywords
keywords: "comma, separated, phrases"   # optional, used only when tags are absent
image: /assets/posts/<slug>/cover.jpg   # optional, absolute path; falls back to /slides/Avatar.jpg
last_modified_at: YYYY-MM-DD            # optional, becomes dateModified (defaults to date)
---
```

Notes on the actual field wiring (see `_includes/structured-data-post.html`):

- `description` is preferred; if missing, the include falls back to the
  generated `excerpt`. An explicit `description` is always better, because the
  same value is reused for the post card and for the llms.txt line.
- `tags` win over `keywords`: if `tags` is non-empty it is joined into the
  JSON-LD `keywords` field and `keywords` is ignored.
- `layout: post` and the `/posts/<slug>/` permalink come from `_config.yml`
  (the `articles` collection plus `defaults`). Do not repeat them per post.

### What is generated automatically (never duplicate by hand)

- `_layouts/default.html` writes `<title>`, meta description, the
  `<link rel="canonical">` pointing at `site.url` (https://maxclerkwell.tech),
  and the Open Graph and Twitter Card tags by hand from the front matter.
  jekyll-seo-tag is deliberately NOT used: it emitted its own `@id`-less
  Person/WebSite JSON-LD on every page, duplicating the entities in
  `_includes/structured-data.html`. Do not reintroduce `{% seo %}`.
- Canonical entity `@id`s shared across maxclerkwell.tech,
  nabla-b.engineering and edge-compute.skainet.io (never invent local
  aliases for these): person `https://maxclerkwell.tech/#person`, nabla B
  `https://nabla-b.engineering/#organization`, Auto-Intern GmbH
  `https://www.auto-intern.de/#organization`, skAInet brand
  `https://www.skainet.io/#brand`, AI-Gruppe `https://gruppe.ai/#brand`,
  Edge-Compute `https://edge-compute.skainet.io/#product`. LinkedIn is
  always written as `https://www.linkedin.com/in/accelerator-stephan/`.
- Links to nabla-b.engineering and edge-compute.skainet.io open an
  interstitial (`_includes/leave-modal.html`) and get `?ref=maxclerkwell.tech`
  appended; add `data-no-leave` to an anchor to bypass it.
- `_includes/structured-data.html` is included on every page and holds the
  site-wide schema.org `@graph` (Person, nabla B, publisher Organization,
  WebSite) with stable `@id` values under `https://maxclerkwell.tech/#...`.
- `_includes/structured-data-post.html` is included only when `page.date`
  exists and emits the per-post `BlogPosting` JSON-LD, referencing the
  site-wide nodes by `@id` instead of repeating them.
- `llms.txt` (root, `permalink: /llms.txt`) is a Liquid template. Its
  "All writing" section is regenerated on every Jekyll build from
  `_includes/get-blog-posts.html`. Never add post entries manually.
- `sitemap.xml` (root, `layout: null`) is likewise a Liquid template and is
  rebuilt on every build. Never add URLs manually.
- `robots.txt` points crawlers at both `sitemap.xml` and `llms.txt`.

So: adding a properly filled `_articles/<slug>.md` is the ONLY manual step.
JSON-LD, canonical URL, feed, sitemap and llms.txt follow automatically.

### Relevant files

| File | Role |
| --- | --- |
| `_includes/structured-data-post.html` | per-post `BlogPosting` JSON-LD |
| `_includes/structured-data.html` | site-wide schema.org `@graph` |
| `_includes/get-blog-posts.html` | unified post list (legacy pages plus `articles`) |
| `llms.txt` | LLM-facing site summary plus auto-generated post list |
| `sitemap.xml` | auto-generated sitemap |
| `robots.txt` | crawler rules, sitemap and llms.txt pointers |
| `_config.yml` | `url`, `author`, collection and defaults, plugins |

### Repository rule

**Never commit binary files.** Images that genuinely belong to a post go to
`assets/posts/<kebab-slug>/` and must be discussed before being added; anything
else (archives, PDFs, binaries, build artefacts) stays out of the repository.
