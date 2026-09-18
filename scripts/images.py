#!/usr/bin/env python3
"""Image archive pipeline, see "Images" in AGENTS.md.

Every image of the site has a full-resolution *master* in assets/images/ and,
if it is shown on a page, a downscaled *display copy* at the path the page
references. Both carry the 2 % text watermark, the DCT watermark, IPTC/XMP
metadata and the licensing link. _data/images.yml is the manifest.

  scripts/images.py            process every tracked image not yet in the manifest
  scripts/images.py --redisplay  rebuild all display copies from their masters
  scripts/images.py --remeta     re-read alt texts from the articles, rewrite manifest + file metadata
  scripts/images.py --check    re-detect the DCT watermark in all processed files

Needs: ImageMagick (magick), exiftool, python3 with numpy, scipy, Pillow, PyYAML.
An image that is already in the manifest is never processed again, so the
script can be re-run safely after adding new pictures.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import dct_watermark as dct  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "_data" / "images.yml"
ARCHIVE = "assets/images"
SITE = "https://maxclerkwell.tech"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
WM_TEXT = "https://maxclerkwell.tech\nStephan Bökelmann\n施泓杰\nMaxClerkwell"
WM_OPACITY = 0.02
DISPLAY_MAX = 960          # longest side of a display copy, px
NAME = "Stephan Bökelmann"
BASE_KW = [NAME, "施泓杰", "MaxClerkwell", "maxclerkwell.tech"]

# Not mine: never watermarked, never claimed, not listed on /images/.
THIRD_PARTY = {
    "assets/valid-atom.png",
    "assets/posts/25square-capacitive-rain-sensing-september-2026/okeanos-logo.png",
    "assets/posts/zero-to-one-python-libraries-environments-june-2026/python-logo.png",
    "assets/posts/from-aristotle-to-the-bit-july-2026/claude-shannon.jpg",
    "assets/posts/cunninghams-law-june-2026/cunninghams-law-quora.png",
}
# Display files whose master already exists under another name.
ALIAS = {
    "slides/Avatar.jpg": "assets/images/portraits/Stephan_Boekelmann_Avatar_2024.jpg",
    "assets/about/cern-banner.jpg": "assets/images/portraits/Stephan_Boekelmann_at_CERN_2018.jpg",
}


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def tracked_images():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines()
            if re.search(r"\.(jpe?g|png|gif)$", p, re.I) and not p.startswith(ARCHIVE + "/")]


def post_of(path):
    """(slug, source file of the page that owns the image) or (None, None)."""
    m = re.match(r"posts/([^/]+)/", path) or re.match(r"assets/posts/([^/]+)/", path)
    if not m:
        return None, None
    slug = m.group(1)
    cands = [ROOT / "_articles" / f"{slug}.md", *sorted((ROOT / "posts" / slug).glob("*.md"))]
    if slug.endswith("-series"):            # series landing pages: alinx.md, linkmicro.md, …
        cands.insert(0, ROOT / f"{slug[:-7]}.md")
    md = next((c for c in cands if c.exists()), None)
    if md is None:                          # slug of the asset folder differs from the article file name
        needle = f"/assets/posts/{slug}/"
        md = next((c for c in sorted((ROOT / "_articles").glob("*.md")) if needle in c.read_text(encoding="utf-8")), None)
    return slug, md


def front_matter(md):
    txt = md.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, txt)


def alt_for(body, basename):
    b = re.escape(basename)
    for pat in (r"!\[([^\]]*)\]\([^)]*%s" % b, r'<img[^>]*%s[^>]*alt="([^"]*)"' % b,
                r'<img[^>]*alt="([^"]*)"[^>]*%s' % b):
        m = re.search(pat, body)
        if m and m.group(1).strip():
            return re.sub(r"\s+", " ", m.group(1)).strip()
    return ""


def text_watermark(src, dst):
    w, h = (int(x) for x in subprocess.run(["magick", "identify", "-format", "%w %h", f"{src}[0]"],
                                           capture_output=True, text=True, check=True).stdout.split())
    with tempfile.NamedTemporaryFile(suffix=".png") as wm:
        run("magick", "-background", "none", "-font", FONT, "-fill", "white", "-stroke", "black",
            "-strokewidth", min(w, h) // 200 + 1, "-gravity", "center",
            "-size", f"{w * 94 // 100}x{h * 94 // 100}", f"caption:{WM_TEXT}",
            "-channel", "A", "-evaluate", "multiply", WM_OPACITY, "+channel", wm.name)
        run("magick", src, wm.name, "-gravity", "center", "-composite", dst)


def write_meta(path, e):
    rights = f"© {e['year']} {NAME} (施泓杰, MaxClerkwell)."
    if e["license"] == "CC BY-SA 4.0":
        rights += " CC BY-SA 4.0 — attribute MaxClerkwell and link back to the original."
        terms = (f"CC BY-SA 4.0. Attribute \"MaxClerkwell\" and link to {e['source']} — "
                 f"see {SITE}/licensing/#images")
        cc = ["-XMP-cc:License=https://creativecommons.org/licenses/by-sa/4.0/"]
    else:
        rights += " All rights reserved."
        terms = (f"All rights reserved. Unmodified editorial and speaker-announcement use permitted with "
                 f"credit '{NAME} / maxclerkwell.tech' (MaxClerkwell) and a link to {SITE}/ — "
                 f"see {SITE}/licensing/#images")
        cc = []
    kw = ", ".join(dict.fromkeys(BASE_KW + e.get("keywords", [])))
    d = e["description"]
    run("exiftool", "-q", "-m", "-overwrite_original", "-codedcharacterset=utf8",
        f"-XMP-dc:Title={e['title']}", f"-IPTC:ObjectName={e['title'][:64]}", f"-XMP-photoshop:Headline={e['title']}",
        f"-XMP-dc:Description={d}", f"-IPTC:Caption-Abstract={d}", f"-EXIF:ImageDescription={d}",
        f"-XMP-iptcCore:AltTextAccessibility={d}",
        f"-XMP-dc:Creator={NAME}", f"-IPTC:By-line={NAME}", f"-EXIF:Artist={NAME}",
        f"-XMP-dc:Rights={rights}", f"-IPTC:CopyrightNotice={rights}", f"-EXIF:Copyright={rights}",
        "-XMP-xmpRights:Marked=True", f"-XMP-xmpRights:Owner={NAME}", f"-XMP-xmpRights:UsageTerms={terms}",
        f"-XMP-xmpRights:WebStatement={SITE}/licensing/#images",
        f"-XMP-plus:LicensorURL={SITE}/licensing/#contact",
        f"-XMP-photoshop:Credit={NAME} / maxclerkwell.tech", f"-IPTC:Credit={NAME}",
        f"-XMP-photoshop:Source={e['source']}", f"-IPTC:Source={e['source'][:32]}",
        f"-XMP-iptcCore:CreatorWorkURL={SITE}", f"-XMP-photoshop:DateCreated={e['year']}",
        "-sep", ", ", f"-XMP-dc:Subject={kw}", f"-IPTC:Keywords={kw}", *cc, path)


def embed_readable(src, dst, alpha, quality, subsampling=0):
    """Flat or clipped images (screenshots, plots) swallow a weak mark: raise alpha until it reads back."""
    for a in (alpha, alpha * 2, alpha * 3, alpha * 4.5):
        dct.embed(src, dst, alpha=a, quality=quality, subsampling=subsampling)
        if dct.detect(dst)[0] == dct.DEFAULT_TEXT.encode():
            return


def make_master(src, master, e):
    master.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".gif":        # animated: pixels stay untouched, metadata only
        master.write_bytes(src.read_bytes())
        e["watermark"] = "metadata only (animated GIF)"
    else:
        with tempfile.NamedTemporaryFile(suffix=".png") as t:
            text_watermark(src, t.name)
            embed_readable(t.name, master, 3.0, 92)
    write_meta(master, e)


def make_display(master, display):
    if master.suffix.lower() == ".gif":
        display.write_bytes(master.read_bytes())
        return
    with tempfile.NamedTemporaryFile(suffix=".png") as t:
        run("magick", master, "-resize", f"{DISPLAY_MAX}x{DISPLAY_MAX}>", "-strip", t.name)
        # scaling destroys the DCT mark of the master, so it is embedded again
        embed_readable(t.name, display, 4.0, 80, subsampling=2)
    run("exiftool", "-q", "-m", "-overwrite_original", "-tagsfromfile", master, "-all:all", "-unsafe", display)


def score(path):
    if path.suffix.lower() == ".gif":
        return None
    text, z = dct.detect(path)
    return round(z, 1) if text == dct.DEFAULT_TEXT.encode() else f"UNREADABLE ({z:.1f})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--redisplay", action="store_true")
    ap.add_argument("--remeta", action="store_true")
    args = ap.parse_args()
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []
    manifest = manifest or []

    if args.check:
        for e in manifest:
            for k in ("file", "display"):
                if e.get(k) and e.get("rights") == "own":
                    print(f"{score(ROOT / e[k].lstrip('/'))!s:>18}  {e[k]}")
        return

    if args.remeta:                         # exiftool only: pixels and watermarks stay untouched
        for e in manifest:
            if e.get("rights") != "own":
                continue
            if e.get("display") and e.get("post"):
                _, md = post_of(e["display"].lstrip("/"))
                fm, body = front_matter(md) if md else ({}, "")
                alt = alt_for(body, Path(e["display"]).name)
                if alt:                     # entries without a Markdown alt keep their hand-written texts
                    e["title"] = alt if len(alt) <= 120 else alt[:117].rsplit(" ", 1)[0] + "…"
                    e["description"] = f"{alt} — from the article “{fm.get('title', '')}” by {NAME} (MaxClerkwell)."
                    if md and md.parent.name == "_articles":
                        e["source"] = f"{SITE}/posts/{md.stem}/"
            master = ROOT / e["file"].lstrip("/")
            write_meta(master, e)
            if e.get("display"):
                run("exiftool", "-q", "-m", "-overwrite_original", "-tagsfromfile", master, "-all:all", "-unsafe",
                    ROOT / e["display"].lstrip("/"))
        MANIFEST.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
        return

    if args.redisplay:
        for e in manifest:
            if e.get("display") and e.get("rights") == "own":
                make_display(ROOT / e["file"].lstrip("/"), ROOT / e["display"].lstrip("/"))
                e["dct_display"] = score(ROOT / e["display"].lstrip("/"))
        MANIFEST.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
        return

    known = {e["display"].lstrip("/") for e in manifest if e.get("display")}
    # "<name>-800.jpg" next to "<name>.jpg" is a thumbnail of the same picture: it shares the
    # master of the full file and is processed after it.
    todo = [r for r in tracked_images() if r not in known]
    def full_of(r):
        m = re.match(r"(.*)-\d{3,4}(\.\w+)$", r)
        return m.group(1) + m.group(2) if m and (ROOT / (m.group(1) + m.group(2))).exists() else None
    todo.sort(key=lambda r: (full_of(r) is not None, r))
    for rel in todo:
        src = ROOT / rel
        if full_of(rel):
            parent = next(x for x in manifest if x.get("display") == "/" + full_of(rel))
            make_display(ROOT / parent["file"].lstrip("/"), src)
            manifest.append({**parent, "display": "/" + rel, "variant": True, "dct_display": score(src)})
            print("variant", rel)
            continue
        slug, md = post_of(rel)
        if rel in THIRD_PARTY:
            manifest.append({"display": "/" + rel, "post": slug, "rights": "third-party"})
            continue
        if rel in ALIAS:
            master = ROOT / ALIAS[rel]
            e = next(x for x in manifest if x["file"] == "/" + ALIAS[rel])
            e["display"] = "/" + rel
            make_display(master, src)
            e["dct_display"] = score(src)
            print("alias  ", rel)
            continue
        fm, body = front_matter(md) if md else ({}, "")
        alt = alt_for(body, src.name)
        ptitle = fm.get("title", "maxclerkwell.tech")
        year = str(fm.get("date", ""))[:4] or "2026"
        sub = Path(rel).parent.name if Path(rel).parent.name not in ("assets", slug or "") else ""
        name = f"{sub}-{src.name}" if sub else src.name
        master = ROOT / ARCHIVE / (slug or "site") / name
        purl = f"{SITE}/posts/{slug}/" if slug and not slug.endswith("-series") else (f"{SITE}/{slug[:-7]}/" if slug else SITE + "/")
        e = {
            "file": "/" + str(master.relative_to(ROOT)),
            "display": "/" + rel,
            "post": slug,
            "title": alt[:120] if alt else f"{src.stem.replace('_', ' ').replace('-', ' ')} — {ptitle}",
            "description": (f"{alt} — from" if alt else "Image from") + f" the article “{ptitle}” by {NAME} (MaxClerkwell).",
            "year": year,
            "source": purl,
            "license": "CC BY-SA 4.0",
            "rights": "own",
            "keywords": [str(t) for t in (fm.get("tags") or [])],
        }
        make_master(src, master, e)
        make_display(master, src)
        e["dct_master"], e["dct_display"] = score(master), score(src)
        manifest.append(e)
        print("done   ", rel, e["dct_master"], e["dct_display"])
        MANIFEST.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    MANIFEST.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")


if __name__ == "__main__":
    main()
