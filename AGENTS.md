# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## What this is

A personal Jekyll blog and linktree for Stephan Bökelmann (alias MaxClerkwell), deployed to GitHub Pages via the `master` branch. No build step is run locally — GitHub Actions handles the Jekyll build on push.

## Local development

```bash
bundle install          # install Ruby gems (first time)
bundle exec jekyll serve --livereload   # serve at http://localhost:4000
```

Jekyll requires Ruby and Bundler. The site uses `github-pages` gem to mirror the GitHub Pages build environment.

## Architecture

- `_config.yml` — site-wide settings (title, plugins, excludes, collections, defaults)
- `_layouts/default.html` — shell with nav and footer; uses Inter + JetBrains Mono from Google Fonts and Font Awesome 6 for icons
- `_layouts/post.html` — wraps `default.html`, adds back-link and post header
- `assets/css/site.css` — all styles (single file, no preprocessor)
- `index.html` — home page: hero section, linktree grid, and auto-generated post list
- `posts/<slug>/...` — **legacy** blog posts (26 existing articles). Their `.md` source files and directories must never be moved or renamed (see "Adding a blog post").
- `_articles/<slug>.md` — **new** blog posts (Jekyll `articles` collection)
- `_includes/get-blog-posts.html` — single source of truth for the unified post list (legacy pages + new collection documents)

## Images (mandatory pipeline)

Every picture that is used on the site, **and** every picture Stephan merely
wants to have crawlable on the web without using it on a page, lives as a
full-resolution **master** in the archive folder `assets/images/`:

- `assets/images/<post-slug>/<file>` for article images,
- `assets/images/portraits/` for portraits and other stand-alone pictures,
- `assets/images/site/` for anything else.

A master ALWAYS carries all four of these, no exceptions:

1. the four-line text watermark (`https://maxclerkwell.tech` / `Stephan Bökelmann`
   / `施泓杰` / `MaxClerkwell`), centred, filling the frame, at **2 % opacity**,
2. the keyed **DCT (frequency-domain) watermark** with payload `maxclerkwell.tech`
   (`scripts/dct_watermark.py`; key from env `WM_KEY`),
3. complete **IPTC/XMP/EXIF metadata** (title, description = alt text, creator,
   copyright, credit, keywords, source URL, year),
4. the **licensing link**: XMP `WebStatement` → `https://maxclerkwell.tech/licensing/#images`
   and `LicensorURL` → `…/licensing/#contact`.

When a picture is shown anywhere on the site, the page never embeds the master.
It embeds a **display copy**: downscaled (longest side 960 px, JPEG q80) for
fast loading, and again with text watermark, a freshly embedded DCT watermark
(scaling destroys the master's) and the same metadata. Display copies live where
the page expects them (`assets/posts/<slug>/…`, legacy `posts/<slug>/assets/…`,
`slides/Avatar.jpg`, …) — legacy paths are never moved or renamed.

**Lightboxes always open the master** from `assets/images/`, not the display
copy. `_includes/lightbox.html` does this via the display→master map generated
from `_data/images.yml`; use that include instead of writing a new lightbox.

`/images/` (`images.html`, linked in the footer) is a plain text list of all
masters without previews; each entry opens the master in the lightbox. It is
generated from the manifest — never edit it by hand.

### Workflow for a new picture

1. Put the original at the display path (or, for a crawl-only picture, process
   it by hand into `assets/images/portraits/` and add a manifest entry with
   `display: null`).
2. Write a meaningful alt text in the Markdown — it becomes title, description
   and alt metadata.
3. Run `python3 scripts/images.py`. It creates the master, replaces the file at
   the display path with the display copy, verifies that both DCT watermarks
   read back, and appends the entry to `_data/images.yml`. Entries already in
   the manifest are never reprocessed. `--remeta` re-reads the alt texts after you edited them and rewrites manifest and file metadata (pixels untouched), `--check` re-verifies all watermarks,
   `--redisplay` rebuilds all display copies from the masters.
4. Commit master, display copy and manifest together.

Rules and edge cases:

- **Third-party pictures** (logos, historic photos, screenshots of other
  people's content) are never watermarked and never get Stephan's copyright
  metadata. List them in `THIRD_PARTY` in `scripts/images.py`; they appear in the
  manifest as `rights: third-party` and are not shown on `/images/`. When in
  doubt whether a picture is Stephan's own, ask.
- Portraits are `license: All rights reserved`; article figures and photos are
  `CC BY-SA 4.0` (see `/licensing/`).
- Animated GIFs keep their pixels (metadata only); SVGs are not processed.
- The original, unwatermarked file is not kept in the working tree. Never run
  the pipeline on a file that is already a display copy (the manifest prevents
  this; do not delete manifest entries to "redo" an image — restore the
  original from git history first).

## Adding a blog post

### Legacy posts (the 26 articles that already exist)

These live under `posts/<slug>/` (some use `index.md`, most use `<slug>.md`).  
**Do not move, rename, or delete any of these files or their directories.** External sites and tools link directly to the raw `.md` sources on GitHub; changing their paths would break those links.

They continue to work exactly as before. Their frontmatter still contains the explicit `layout` and `permalink` (harmless; the new defaults only apply to the `articles` collection).

### New posts (recommended for all future writing)

Create a file `_articles/<kebab-slug>.md` (flat file, not a directory) with **minimal** frontmatter:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
tags: [tag1, tag2]
description: "One-sentence summary shown in the post card."
---
```

- `layout: post` and `permalink: /posts/<slug>/` are supplied automatically by `_config.yml` (the `articles` collection + defaults).
- The file is named `<kebab-slug>.md` so the collection permalink `/posts/:name/` produces the clean public URL `/posts/<kebab-slug>/`.
- **Images and other media** for new posts live in `assets/posts/<kebab-slug>/` and are referenced with absolute paths, e.g.:
  ```markdown
  ![Description](/assets/posts/my-post/photo.jpg)
  ```
  (This is the new convention; the old relative `assets/...` trick only works for the legacy `posts/<slug>/` layout.)

After adding the file, the post appears automatically on the home page, in the feed, sitemap, search, tag cloud, and archive.

The unified discovery logic lives in `_includes/get-blog-posts.html` (legacy `site.pages` filter + `site.articles`). Never duplicate the old `where_exp: "item", "item.url contains '/posts/'"` pattern again.

### Content model transition note

The hybrid approach (legacy pages + new `articles` collection) was chosen so that the 26 existing article Markdown files could remain at their historical paths forever while still giving future content a clean, idiomatic Jekyll structure.

## Article series naming conventions

### Zero-to-One (ZTO) series

All Zero-to-One articles must be named with the prefix `zero-to-one-*`:

```
_articles/zero-to-one-<topic>-<optional-subtitle>-<month>-<year>.md
```

Example: `_articles/zero-to-one-python-libraries-environments-june-2026.md`

Never use `<topic>-zero-to-one-*` or any other ordering. The series prefix always comes first.

## Writing style

- **No em-dashes.** Do not use the em-dash character (—) anywhere in articles, commit messages, or documentation. Replace with a comma, semicolon, colon, or a period depending on the grammatical context.

## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds with `actions/jekyll-build-pages` and deploys to GitHub Pages. There is no staging environment.

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
about_id: https://.../#id               # optional, @id of a site-graph entity the post is about
video:                                  # optional, emits a VideoObject (see structured-data-video.html)
  id: YOUTUBE_ID
  name: "Video title"
  description: "One sentence."
  upload_date: YYYY-MM-DD
event:                                  # optional, emits an Event node for conference reports
  name: "KiCon Europe 2026"             # (see structured-data-event.html for all keys)
  start_date: YYYY-MM-DD
  end_date: YYYY-MM-DD
  location: "Venue"
  city: "Bochum"
  country: "DE"
  organizer_id: https://maxclerkwell.tech/#skunkforce
  role: organizer                       # organizer | performer | attendee
---
```

Notes on the actual field wiring (see `_includes/structured-data-post.html`):

- `description` is preferred; if missing, the include falls back to the
  generated `excerpt`. An explicit `description` is always better, because the
  same value is reused for the post card and for the llms.txt line.
- `image` MUST be an absolute path (`/posts/<slug>/assets/x.jpg` for legacy
  posts, `/assets/posts/<slug>/x.jpg` for new ones) or a full URL. A relative
  `assets/x.jpg` renders a 404 in JSON-LD, og:image and Twitter Card.
- `about_id`, `video` and `event` are all optional; `about` on the BlogPosting
  becomes a list when both `about_id` and `event` are set.
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
- `_includes/structured-data.html` holds the full site-wide schema.org
  `@graph` and is emitted only on `/`, `/about/`, `/hire/`, `/talks/` and the
  Edge-Compute article; every other page gets `structured-data-slim.html`,
  short stubs with the same canonical `@id`s (add a stub there whenever a new
  `about_id` or `organizer_id` target is introduced). The full graph (Person, nabla B, publisher Organization,
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
