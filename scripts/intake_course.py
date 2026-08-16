#!/usr/bin/env python3
"""Normalize a freshly generated course package into site/<slug>/.

Standard library only, by design (AGENTS.md section 7: PR CI is install-free and
reproducible offline). Nothing here fetches, and nothing here needs a build step.


WHY THIS EXISTS
---------------
Four course packages have arrived from the generator. Every one of them shipped
the same five defects, and every one of them was fixed by hand:

    1. a light palette with the neutrals but none of the accents, so every
       accent that is read AS TEXT stayed at its dark-theme value on a light
       ground;
    2. no `@media (prefers-color-scheme: light)` block at all, so the reader who
       never touches the toggle got no light theme;
    3. its own localStorage theme key -- four distinct keys so far -- so a
       reader's explicit choice silently reset at every course boundary;
    4. no cross-page navigation: no breadcrumb, no prev/next pager;
    5. placeholder meta descriptions ("Interactive standalone lesson: X.");
    6. component rules scoped to `[data-theme="light"] .foo`, which reach the
       reader who clicked the toggle and not the reader whose OS is light -- the
       precise mechanism by which the two light paths drift apart.

Fixing that by hand, four times, produced drift: at one point one course carried
three incompatible pager families. A deterministic script cannot drift. This is
that script.


THE LINE: WHAT IS REUSED AS-IS, AND WHAT THIS TOOL OWNS
-------------------------------------------------------
The generator is GOOD at content and BAD at standards, so the split follows
exactly that.

REUSED AS-IS -- copied through byte-for-byte, never re-rendered:

    * the lesson's body content and teaching prose;
    * its inline SVG charts and every number behind them (anchor arrays, PRNG,
      thresholds, scoring logic);
    * its interactive JavaScript;
    * its own component CSS.

  This is the valuable, hard-to-rebuild part. It is also tightly coupled to its
  own markup: the chart code addresses elements by id, the CSS is written
  against the exact class names the generator emitted, and the quiz logic reads
  its own data structures. Re-skinning or re-rendering any of it would break
  interactivity for no gain, because none of it is what drifts.

OWNED AND OVERWRITTEN -- rewritten from pinned constants on every run:

    * the <head> metadata block (title, description, canonical, og:*, twitter:*,
      theme-color, icon);
    * the light palette, both of its paths;
    * the pre-paint theme script, the theme storage key, and the toggle;
    * the breadcrumb;
    * the lesson pager;
    * the footer's identity lines;
    * the MECHANISM by which a component reaches a theme-dependent colour --
      not the colour itself. A `[data-theme="light"] .foo { background: X }`
      override is lifted into a custom property that both light paths declare,
      with X and the dark value carried across unchanged. Nothing renders
      differently; the component simply stops naming a theme. See
      plan_component_overrides() for the guards that keep that exact, and for
      the cases where it refuses and hands the decision back to a person.

  These are SHELL. They are mechanical, they are identical in shape across every
  page of the library, they are exactly what tests/test_site_invariants.py pins,
  and they are exactly what a per-course generator has no way to get right --
  it cannot know the course's URL, its neighbours in the path, or what the other
  three courses already do. So the generator's version is discarded and this
  tool's version is written, every time.

The rule of thumb for anything new: if the reader carries it ACROSS a course
boundary, this tool owns it. If it only makes sense inside one lesson, the
generator owns it and this tool must not touch it.

ONE SOURCE OF TRUTH. The pinned values are imported from
tests/test_site_invariants.py -- LIGHT_PALETTE, THEME_STORAGE_KEY,
THEME_TOGGLE_MARKUP, LESSON_NAV_MARKUP, CANONICAL_ORIGIN, and the scanners
themselves. They are never re-typed here. A tool that duplicated the palette
would be a fifth place for it to drift, which is the problem, not the fix.


IDEMPOTENT BY CONSTRUCTION
--------------------------
Every step is a CHECK first and a REPAIR second. The check is the invariant
itself (usually the test suite's own predicate), not "does this look like my
template" -- so a page that already satisfies the invariant is left untouched,
byte for byte, however it came to satisfy it. Running the tool against an
already-normalized course therefore reports nothing and writes nothing, and
running it twice produces the same tree. Files are byte-compared before writing,
so "no change" means no write at all, not a rewrite with identical content.


FAILS LOUDLY, CHANGES NOTHING
-----------------------------
Preflight runs over the whole package before a single byte is written. Any of
these aborts the run with a non-zero exit and no output written:

    * manifest / file-count mismatch (a lesson the manifest does not declare, or
      a declared lesson with no file);
    * a theme key shape this tool cannot safely rewrite -- the storage calls must
      be confined to one `function setupTheme(){...}`, which is shell this tool
      replaces wholesale; a key used anywhere else is content it will not touch;
    * a lesson that already references an external resource (scanned with
      scripts/smoke.py's own scanner, the same one CI and the test suite use);
    * structural surprises: no <head>, no <style>, more than one <header>,
      <footer> or theme toggle, an unrecognized element in the head metadata
      region, or a light @media block holding more than the palette;
    * retired pager markup, which is content this tool will not strip;
    * a component light override whose token extraction would not be exact;
    * --position disagreeing with the manifest's courseNumber, or with COURSES
      in tests/test_site_invariants.py, or lesson slugs that disagree with the
      order declared there.


WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
    * It does not write the COURSE HOME (site/<slug>/index.html). The generator
      does not produce one, and it is not shell: it carries the syllabus, the
      course's position in the path, and the course pager to its neighbours.
      Author it by hand -- see docs/INTAKE.md.
    * It does not touch site/index.html, site/paths/, or the tests, all of which
      must be updated by hand when a course is added.
    * It does not restructure the body. The generator's <main class="shell"> and
      its header stay exactly as shipped.
    * It does not write the participation reading or any other teaching copy.
      Content is content; this tool moves no prose except the footer notice it
      re-wraps verbatim.


USAGE
-----
    python3 scripts/intake_course.py --source DIR --slug SLUG \\
        --title "Course Title" --position N [--manifest PATH] [--out DIR]
        [--dry-run]

    --source    the generated package: NN-name.html lesson files plus
                lessons-manifest.json. An already-normalized tree
                (<slug>/index.html per lesson) is also accepted, which is how
                idempotence is checked against a published course.
    --slug      the course's URL slug; output goes to <out>/<slug>/.
    --title     the course title, as it appears in the breadcrumb and <title>.
    --position  the course's 1-based position in the path. Cross-checked against
                the manifest's courseNumber and against COURSES in
                tests/test_site_invariants.py when the course is declared there.
    --manifest  path to lessons-manifest.json when it is not in --source.
    --out       document root to write under (default: site/).
    --dry-run   report what WOULD change; write nothing.

Exit status:
    0  success (or, with --dry-run, a clean report)
    1  preflight failed; nothing was written
    2  usage error
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# The pinned conventions, imported from the tests. Never re-typed here.
# --------------------------------------------------------------------------

def _load_invariants():
    """Import tests/test_site_invariants.py as a module.

    The test module is the source of truth for every pinned value and for the
    scanners that decide whether a page already complies. Importing it (rather
    than copying constants across) is what keeps this tool and the suite that
    grades it from disagreeing.
    """
    path = REPO_ROOT / "tests" / "test_site_invariants.py"
    spec = importlib.util.spec_from_file_location("_site_invariants", path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise SystemExit("cannot load the pinned conventions from %s" % path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INV = _load_invariants()

LIGHT_PALETTE = INV.LIGHT_PALETTE
THEME_STORAGE_KEY = INV.THEME_STORAGE_KEY
THEME_TOGGLE_MARKUP = INV.THEME_TOGGLE_MARKUP
LESSON_NAV_MARKUP = INV.LESSON_NAV_MARKUP
RETIRED_PAGER_MARKUP = INV.RETIRED_PAGER_MARKUP
CANONICAL_ORIGIN = INV.CANONICAL_ORIGIN
CANONICAL_HOST = INV.CANONICAL_HOST
COURSES = INV.COURSES
scan_self_containment = INV.scan_self_containment


# --------------------------------------------------------------------------
# Pinned shell fragments. Everything below is markup this tool OWNS.
# --------------------------------------------------------------------------

# The library-wide copyright line. A literal, never datetime.now(): a tool whose
# output depends on the clock is not deterministic, and a course onboarded next
# January must not disagree with the 58 pages already published. Bump it here,
# deliberately, and re-run intake for every course if it ever changes.
FOOTER_IDENTITY = (
    "© 2026 dmedellin · Released under the MIT License · "
    "Educational use only — charts are synthetic examples, not trade signals."
)
FOOTER_IDENTITY_P = "<p>%s</p>" % FOOTER_IDENTITY
FOOTER_SITE_LINK_P = '<p><a href="%s">%s</a></p>' % (CANONICAL_ORIGIN, CANONICAL_HOST)

META_AUTHOR = "dmedellin"
THEME_COLOR_DARK = "#071019"
THEME_COLOR_LIGHT = LIGHT_PALETTE["--bg"]

# The lesson favicon the library settled on. Only used when the generated page
# ships none; a package that brings its own icon keeps it, because a course's
# mark is identity, not shell.
DEFAULT_ICON_HREF = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'"
    "%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop "
    "offset='0' stop-color='%238ff3ff'/%3E%3Cstop offset='1' stop-color='%2336d6e7'"
    "/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='15' "
    "fill='url(%23g)'/%3E%3Cpath d='M14 45L26 33L38 41L51 18' fill='none' "
    "stroke='%23041116' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'"
    "/%3E%3Cg fill='%23041116'%3E%3Ccircle cx='14' cy='45' r='4.5'/%3E%3Ccircle "
    "cx='26' cy='33' r='4.5'/%3E%3Ccircle cx='38' cy='41' r='4.5'/%3E%3Ccircle "
    "cx='51' cy='18' r='4.5'/%3E%3C/g%3E%3C/svg%3E"
)

OG_IMAGE_NOTE = (
    "<!-- No og:image / twitter:image: a share card needs an absolute hosted "
    "image URL, and this page is deliberately self-contained. -->"
)

# Applied before first paint. It lives LAST in <head> on purpose: the page script
# at the bottom of <body> runs after the first paint, which is how course 1
# shipped a theme that flashed the wrong palette and snapped. The allowlist
# matters too -- a corrupt stored value written straight onto data-theme matches
# no CSS while still counting as an explicit choice, pinning the page to dark.
PREPAINT_SCRIPT = """  <noscript>
    <style>
      /* The toggle is a JS-only control: without JS it renders, invites a click,
         and does nothing. Hide it rather than ship a dead affordance. */
      #themeToggle { display: none; }
    </style>
  </noscript>

  <script>
    /* Applied before first paint so an explicit theme choice never flashes the
       other theme. This is why it lives LAST in <head> and not with the rest of
       the page script at the bottom of <body>: that runs after the first paint.
       SAME localStorage key as every other page in the library ('%(key)s')
       so the choice persists across every course. The allowlist matters: a
       corrupt value would otherwise be written straight onto data-theme,
       matching no CSS while still counting as an explicit choice, which pins
       the page to the dark palette.
       No stored value => CSS prefers-color-scheme decides. */
    (function () {
      try {
        var t = localStorage.getItem('%(key)s');
        if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
      } catch (e) { /* Storage can be unavailable (private mode, file://). */ }
    })();
  </script>
""" % {"key": THEME_STORAGE_KEY}

# The runtime half of the toggle. Direction-neutral: the accessible name is
# static markup (THEME_TOGGLE_MARKUP), so nothing here rewrites aria-label --
# the courses that did rewrote it differently, some naming the current theme and
# some the next. onThemeChange() is called only if the lesson defines one, so a
# lesson whose charts resolve colours at draw time can redraw them.
SETUP_THEME_JS = """function setupTheme(){
 const btn=byId('themeToggle');
 const lightQuery=window.matchMedia?window.matchMedia('(prefers-color-scheme: light)'):null;
 const effectiveTheme=()=>document.documentElement.dataset.theme||(lightQuery&&lightQuery.matches?'light':'dark');
 const renderIcon=()=>{if(btn)btn.textContent=effectiveTheme()==='light'?'\\u2600':'\\u263e'};
 const repaint=()=>{if(typeof onThemeChange==='function')onThemeChange()};
 renderIcon();
 if(btn)btn.addEventListener('click',()=>{
  const next=effectiveTheme()==='light'?'dark':'light';
  document.documentElement.dataset.theme=next;
  try{localStorage.setItem('%(key)s',next)}catch(e){}
  renderIcon();repaint();
 });
 if(lightQuery){
  const onSystemThemeChange=()=>{if(document.documentElement.dataset.theme)return;renderIcon();repaint()};
  if(lightQuery.addEventListener)lightQuery.addEventListener('change',onSystemThemeChange);
  else if(lightQuery.addListener)lightQuery.addListener(onSystemThemeChange);
 }
}""" % {"key": THEME_STORAGE_KEY}

TOGGLE_ELEMENT = THEME_TOGGLE_MARKUP + "☾</button>"

# CSS for the chrome this tool injects. Appended only when the page has none of
# it: the class names are this tool's, so there is nothing of the generator's to
# collide with, and every value is a token so both light paths reach it.
CHROME_CSS = """
/* --- chrome owned by scripts/intake_course.py ---------------------------- */

/* Breadcrumb. A lesson sits two levels below the document root
   (library -> course -> lesson): "../" is this course's home and "../../" is
   the library index. flex-wrap lets the crumbs fall onto a second line on a
   phone instead of collapsing, which keeps the route back to the library
   reachable at every width. */
.crumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2px;
  margin: 10px 2px 0;
  font-size: 0.84rem;
  color: var(--muted);
}

.crumbs a {
  text-decoration: none;
  color: var(--muted);
  padding: 6px 9px;
  border-radius: 9px;
}

.crumbs a:hover { color: var(--text); background: var(--line); }
.crumb-sep { opacity: 0.5; }
.crumb-current { color: var(--text); padding: 6px 9px; }

/* Previous / next lesson pager. The sequence is the course order the manifest
   declares; the last lesson points back at the course home. Same shape and
   tokens as the pagers in every other course so the whole library pages
   identically. */
.lesson-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 32px;
}

.lesson-link {
  flex: 1 1 240px;
  padding: 13px 15px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: var(--panel-2);
  color: var(--text);
  text-decoration: none;
  transition: transform 150ms ease, border-color 150ms ease;
}

.lesson-link:hover { transform: translateY(-1px); border-color: var(--line-strong); }
.lesson-link span { display: block; color: var(--muted); font-size: 0.7rem; font-weight: 850; letter-spacing: 0.07em; text-transform: uppercase; }
.lesson-link strong { display: block; margin-top: 4px; font-size: 0.9rem; }
.lesson-link.next { margin-left: auto; text-align: right; }

/* One card per row on a phone; a two-up pager at 320px is two unreadable columns. */
@media (max-width: 720px) {
  .lesson-link { flex-basis: 100%; }
}
/* --- end chrome ---------------------------------------------------------- */
"""

CHROME_CSS_SELECTORS = (".crumbs", ".lesson-nav", ".lesson-link")


class IntakeError(Exception):
    """A preflight failure. Nothing is written when one of these is raised."""


# --------------------------------------------------------------------------
# Small text utilities
# --------------------------------------------------------------------------

def attr_escape(value):
    """Escape a string for use inside a double-quoted HTML attribute.

    Deliberately does NOT escape the apostrophe: the published pages carry raw
    apostrophes in prose, and &#x27; everywhere would be a gratuitous diff.
    """
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text_escape(value):
    """Escape a string for use as element text."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slug_from_href(href):
    """The published lesson slug for a manifest href: 06-macd.html -> macd."""
    name = Path(href).name
    name = re.sub(r"\.html?$", "", name, flags=re.I)
    return re.sub(r"^\d+[-_]", "", name)


def _skip_css_comment(text, i):
    if text.startswith("/*", i):
        end = text.find("*/", i + 2)
        return len(text) if end == -1 else end + 2
    return i


def matching_brace(text, open_index, css=True):
    """Index just past the `}` that closes the `{` at open_index.

    Comments are skipped so a brace inside one cannot unbalance the scan. For
    JavaScript, string literals are skipped too. Raises IntakeError rather than
    guessing when the braces do not balance.
    """
    depth = 0
    i = open_index
    n = len(text)
    while i < n:
        ch = text[i]
        if css:
            j = _skip_css_comment(text, i)
            if j != i:
                i = j
                continue
        else:
            if text.startswith("/*", i):
                end = text.find("*/", i + 2)
                i = n if end == -1 else end + 2
                continue
            if text.startswith("//", i):
                end = text.find("\n", i)
                i = n if end == -1 else end + 1
                continue
            if ch in "'\"`":
                quote = ch
                i += 1
                while i < n:
                    if text[i] == "\\":
                        i += 2
                        continue
                    if text[i] == quote:
                        i += 1
                        break
                    i += 1
                continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise IntakeError("unbalanced braces starting at offset %d" % open_index)


def find_rule_span(text, prelude):
    """(start, end) of the first top-level CSS rule whose prelude is `prelude`."""
    pattern = re.compile(re.escape(prelude) + r"\s*\{")
    match = pattern.search(text)
    if not match:
        return None
    return match.start(), matching_brace(text, match.end() - 1, css=True)


class CssRule:
    """One top-level CSS rule, located in the RAW document text."""

    __slots__ = ("selector", "start", "body_start", "body_end", "end")

    def __init__(self, selector, start, body_start, body_end, end):
        self.selector = selector
        self.start = start          # first char of the selector
        self.body_start = body_start  # first char after `{`
        self.body_end = body_end    # the `}`
        self.end = end              # one past the `}`

    def declarations(self, text):
        return text[self.body_start : self.body_end]


def top_level_css_rules(text):
    """Every depth-0 rule inside every <style> block, with raw-text offsets.

    Only depth 0: a rule nested inside @media belongs to that at-rule, and this
    scanner exists to find component rules sitting in the plain cascade.
    """
    rules = []
    for block in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S | re.I):
        css_start, css_end = block.start(1), block.end(1)
        i = css_start
        depth = 0
        selector_start = None
        body_start = None
        while i < css_end:
            j = _skip_css_comment(text, i)
            if j != i:
                i = j
                continue
            ch = text[i]
            if ch == "{":
                if depth == 0:
                    body_start = i + 1
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and selector_start is not None and body_start is not None:
                    selector = re.sub(r"\s+", " ", text[selector_start:body_start - 1]).strip()
                    rules.append(CssRule(selector, selector_start, body_start, i, i + 1))
                    selector_start = None
                    body_start = None
            elif depth == 0 and selector_start is None and not ch.isspace():
                selector_start = i
            i += 1
    return rules


def split_declarations(css):
    """[(property, value)] in source order; parentheses are respected."""
    out = []
    depth = 0
    buffer = []
    for char in css:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == ";" and depth == 0:
            piece, buffer = "".join(buffer), []
            if ":" in piece:
                name, value = piece.split(":", 1)
                out.append((name.strip(), re.sub(r"\s+", " ", value).strip()))
            continue
        buffer.append(char)
    piece = "".join(buffer)
    if ":" in piece:
        name, value = piece.split(":", 1)
        out.append((name.strip(), re.sub(r"\s+", " ", value).strip()))
    return out


def find_function_span(text, name):
    """(start, end) of `function NAME(...) { ... }`, braces balanced."""
    match = re.search(r"function\s+%s\s*\([^)]*\)\s*\{" % re.escape(name), text)
    if not match:
        return None
    return match.start(), matching_brace(text, match.end() - 1, css=False)


# --------------------------------------------------------------------------
# The manifest
# --------------------------------------------------------------------------

class Lesson:
    __slots__ = ("ordinal", "slug", "title", "description", "source")

    def __init__(self, ordinal, slug, title, description, source):
        self.ordinal = ordinal
        self.slug = slug
        self.title = title
        self.description = description
        self.source = source


def load_manifest(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise IntakeError("cannot read manifest %s: %s" % (path, exc))
    if not isinstance(data, dict) or not isinstance(data.get("lessons"), list):
        raise IntakeError("%s has no `lessons` array" % path)
    return data


def resolve_lessons(manifest, source):
    """Pair every manifest entry with its file, in manifest order.

    Two source layouts are understood, and which one is in play is decided by
    where the manifest's own hrefs land:

      * a generated PACKAGE, flat:      <source>/06-macd.html
      * an already-normalized TREE:     <source>/macd/index.html

    The second exists so this tool can be pointed at a published course to prove
    it is a no-op there.
    """
    entries = manifest["lessons"]
    flat_hits = sum(1 for e in entries if (source / Path(e.get("href", "")).name).is_file())
    layout = "package" if flat_hits else "tree"

    lessons = []
    missing = []
    for index, entry in enumerate(entries, start=1):
        href = entry.get("href") or ""
        title = (entry.get("title") or "").strip()
        description = (entry.get("description") or "").strip()
        ordinal = str(entry.get("id") or "").strip() or "%02d" % index
        if not href or not title or not description:
            raise IntakeError(
                "manifest entry %d is incomplete (needs href, title, description)" % index
            )
        slug = slug_from_href(href)
        candidate = (
            source / Path(href).name if layout == "package" else source / slug / "index.html"
        )
        if not candidate.is_file():
            missing.append("%s (expected %s)" % (href, candidate))
        lessons.append(Lesson(ordinal, slug, title, description, candidate))

    if missing:
        raise IntakeError(
            "manifest declares %d lesson(s) with no file:\n    %s"
            % (len(missing), "\n    ".join(missing))
        )

    slugs = [lesson.slug for lesson in lessons]
    duplicates = sorted({s for s in slugs if slugs.count(s) > 1})
    if duplicates:
        raise IntakeError("two manifest entries derive the same slug: %s" % ", ".join(duplicates))

    # File-count agreement, both directions. A file the manifest does not
    # declare is a lesson that would never be published and never be noticed.
    if layout == "package":
        found = sorted(p.name for p in source.glob("*.html"))
        declared = sorted(Path(e["href"]).name for e in entries)
    else:
        found = sorted(p.parent.name for p in source.glob("*/index.html"))
        declared = sorted(slugs)
    if found != declared:
        raise IntakeError(
            "manifest / file-count mismatch: manifest declares %d lesson(s), the "
            "source holds %d.\n    only in source:   %s\n    only in manifest: %s"
            % (
                len(declared),
                len(found),
                ", ".join(sorted(set(found) - set(declared))) or "-",
                ", ".join(sorted(set(declared) - set(found))) or "-",
            )
        )

    count = manifest.get("lessonCount")
    if isinstance(count, int) and count != len(lessons):
        raise IntakeError(
            "manifest lessonCount is %d but it declares %d lessons" % (count, len(lessons))
        )
    return lessons, layout


# --------------------------------------------------------------------------
# Preflight: everything that must be true before a byte is written
# --------------------------------------------------------------------------

def theme_storage_sites(text):
    """Every localStorage key the document actually calls with, literal or named."""
    return INV.TestThemeKey.storage_keys(text)


def theme_keys(text):
    return {k for k in theme_storage_sites(text) if INV.THEMEISH_KEY_RE.search(k)}


def preflight_lesson(lesson, text):
    """Problems that make this page unsafe to normalize. Empty list means go."""
    problems = []

    violations = scan_self_containment(text, {CANONICAL_HOST})
    if violations:
        problems.append(
            "references an external resource (%d): %s"
            % (len(violations), "; ".join(violations[:4]))
        )

    if not INV.HEAD_RE.search(text):
        problems.append("no <head> element")
    if "<style" not in text:
        problems.append("no <style> block to hold the palette")
    for tag, count in (("<header", 1), ("<footer", 1)):
        found = len(re.findall(re.escape(tag) + r"\b", text))
        if found != count:
            problems.append("expected exactly %d %s>, found %d" % (count, tag, found))
    toggles = len(re.findall(r"<button\b[^>]*\bid=\"themeToggle\"", text))
    if toggles != 1:
        problems.append("expected exactly one #themeToggle button, found %d" % toggles)

    # The theme key must be rewritable. This tool replaces setupTheme() whole --
    # it is shell -- so every theme storage call has to live inside it. A key
    # used from anywhere else is content, and content is not this tool's to edit.
    keys = theme_keys(text)
    if keys - {THEME_STORAGE_KEY}:
        span = find_function_span(text, "setupTheme")
        if span is None:
            problems.append(
                "theme key(s) %s but no `function setupTheme(){...}` to rewrite; "
                "this shape cannot be normalized safely"
                % ", ".join(sorted(repr(k) for k in keys))
            )
        else:
            outside = text[: span[0]] + text[span[1] :]
            stray = theme_keys(outside) - {THEME_STORAGE_KEY}
            if stray:
                problems.append(
                    "theme key(s) %s used outside setupTheme(); this shape cannot "
                    "be normalized safely" % ", ".join(sorted(repr(k) for k in stray))
                )

    retired = [m for m in RETIRED_PAGER_MARKUP if m in text]
    if retired:
        problems.append(
            "carries retired pager markup that is not this tool's to remove: %s"
            % ", ".join(repr(m) for m in retired)
        )

    head = INV.HEAD_RE.search(text)
    if head:
        start = text.index(head.group(1), head.start())
        style = text.find("<style", start)
        if style == -1:
            problems.append("no <style> inside <head>")
        else:
            leftovers = head_region_leftovers(text[start:style])
            if leftovers:
                problems.append(
                    "unrecognized element(s) in the head metadata region, which "
                    "this tool overwrites: %s" % ", ".join(leftovers)
                )

    media = find_rule_span(text, INV.LIGHT_MEDIA_PRELUDE)
    if media:
        inner = text[media[0] : media[1]]
        body = inner[inner.index("{") + 1 : -1]
        rules = [s for _c, s, _d in INV.css_rules(body)]
        if rules != [INV.LIGHT_MEDIA_SELECTOR]:
            problems.append(
                "the light @media block holds %s, not just the palette; this tool "
                "will not rewrite it blind" % (rules or "nothing")
            )
    return problems


HEAD_ALLOWED_RE = re.compile(
    r"<!--.*?-->|<meta\b[^>]*>|<title\b[^>]*>.*?</title>|<link\b[^>]*>", re.S | re.I
)


def head_region_leftovers(region):
    """Anything in the head metadata region that is not meta/title/link/comment."""
    rest = HEAD_ALLOWED_RE.sub(" ", region).strip()
    if not rest:
        return []
    return [re.sub(r"\s+", " ", rest)[:120]]


# --------------------------------------------------------------------------
# The normalization steps. Each is check-then-repair, and idempotent.
# --------------------------------------------------------------------------

def step_html_tag(text, ctx):
    """`<html lang="en">` -- and no hardcoded data-theme.

    The generator ships <html lang="en" data-theme="dark">, which is an EXPLICIT
    choice as far as the CSS is concerned: it beats :root:not([data-theme="dark"])
    and pins every reader to dark whatever their OS says and whatever they stored.
    """
    match = re.search(r"<html\b([^>]*)>", text, re.I)
    if not match:
        raise IntakeError("no <html> element")
    lang = re.search(r'\blang="([^"]*)"', match.group(1))
    wanted = '<html lang="%s">' % (lang.group(1) if lang else "en")
    if match.group(0) == wanted:
        return text, False
    return text[: match.start()] + wanted + text[match.end() :], True


def build_head_metadata(ctx, icon_href):
    title = "%s · %s" % (ctx["lesson"].title, ctx["course_title"])
    description = ctx["lesson"].description
    url = ctx["canonical"]
    lines = [
        '<meta charset="utf-8" />',
        '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        '<meta name="description" content="%s" />' % attr_escape(description),
        "<title>%s</title>" % text_escape(title),
        '<link rel="canonical" href="%s" />' % url,
        '<meta name="author" content="%s" />' % META_AUTHOR,
        '<meta name="theme-color" content="%s" media="(prefers-color-scheme: dark)" />'
        % THEME_COLOR_DARK,
        '<meta name="theme-color" content="%s" media="(prefers-color-scheme: light)" />'
        % THEME_COLOR_LIGHT,
        '<meta property="og:type" content="article" />',
        '<meta property="og:site_name" content="%s" />' % CANONICAL_HOST,
        '<meta property="og:locale" content="en_US" />',
        '<meta property="og:title" content="%s" />' % attr_escape(title),
        '<meta property="og:description" content="%s" />' % attr_escape(description),
        '<meta property="og:url" content="%s" />' % url,
        OG_IMAGE_NOTE,
        '<meta name="twitter:card" content="summary" />',
        '<meta name="twitter:title" content="%s" />' % attr_escape(title),
        '<meta name="twitter:description" content="%s" />' % attr_escape(description),
        '<meta name="twitter:url" content="%s" />' % url,
        '<link rel="icon" href="%s" />' % icon_href,
    ]
    return "\n" + "".join("  %s\n" % line for line in lines) + "  "


def step_head_metadata(text, ctx):
    """Overwrite everything in <head> before the first <style>.

    The generator emits four of these tags and a placeholder description; it
    cannot emit the rest, because canonical/og/twitter all need the published URL
    and the generator does not know the slug it will be published under.
    """
    head = INV.HEAD_RE.search(text)
    start = text.index(head.group(1), head.start())
    style = text.find("<style", start)
    region = text[start:style]

    icon = re.search(r'<link\b[^>]*\brel="icon"[^>]*\bhref="([^"]*)"[^>]*>', region, re.I)
    icon_href = icon.group(1) if icon else DEFAULT_ICON_HREF

    wanted = build_head_metadata(ctx, icon_href)
    if region == wanted:
        return text, False
    return text[:start] + wanted + text[style:], True


def declared_root_tokens(text):
    tokens = {}
    for context, selector, declarations in INV.css_rules(INV.stylesheet(text)):
        if not context and selector == ":root":
            tokens.update(INV.css_variables(declarations))
    return tokens


def root_declares_color_scheme(text, selector):
    for context, sel, declarations in INV.css_rules(INV.stylesheet(text)):
        if not context and sel == selector and "color-scheme" in declarations:
            return True
    return False


def expand_to_full_lines(text, start, end):
    """Widen (start, end) to whole lines when the rest of those lines is blank.

    Deleting a rule mid-line would leave a ragged line; deleting whole lines
    unconditionally would eat someone else's code. Whitespace outside the span
    this tool owns is never touched -- that is why there is no global
    "tidy blank lines" pass anywhere in this file.
    """
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    line_end = len(text) if line_end == -1 else line_end + 1
    if not text[line_start:start].strip() and not text[end : line_end - 1].strip():
        return line_start, line_end
    return start, end


def token_name(selector, prop):
    base = re.sub(r"[^a-z0-9]+", "-", selector.lower().lstrip(".#")).strip("-")
    return "--%s-%s" % (base, prop)


def plan_component_overrides(text):
    """Turn `[data-theme="light"] .foo {…}` into tokens, or explain why it cannot.

    Returns (edits, tokens) where tokens maps name -> (dark value, light value).

    WHY THIS IS THE TOOL'S BUSINESS AT ALL. A component rule scoped to
    [data-theme="light"] reaches the reader who CLICKED the toggle and not the
    reader whose OS is light, so that second reader gets the light ground with
    dark-theme ink on that one component. The suite forbids it outright
    (test_no_component_is_scoped_to_the_toggle_path_alone) and prescribes the
    remedy: components read tokens and nothing else.

    WHY IT IS STILL NOT A RE-SKIN. This extracts the two literal colours the
    generator already wrote -- the dark one from the base rule, the light one
    from the override -- into a custom property and points the base rule at it.
    Every rendered colour in every theme state is bit-identical afterwards. No
    value is chosen, invented or "improved"; only the mechanism by which the
    component reaches its colour changes, and the mechanism is shell.

    It refuses, loudly, the moment the transform would stop being exact: a
    grouped or compound selector, a base rule that is missing or duplicated, a
    property the base does not set as a literal, or a token name already in use
    for something else. Those are judgement calls, and judgement calls belong to
    a person -- see docs/INTAKE.md.
    """
    rules = top_level_css_rules(text)
    overrides = [
        rule
        for rule in rules
        if INV.LIGHT_TOGGLE_SELECTOR in rule.selector
        and rule.selector != INV.LIGHT_TOGGLE_SELECTOR
    ]
    if not overrides:
        return [], {}

    existing = {}
    for rule in rules:
        for name, value in split_declarations(rule.declarations(text)):
            if name.startswith("--"):
                existing.setdefault(name, value)

    edits = []
    tokens = {}
    rewritten_bases = set()
    for override in overrides:
        selector = override.selector
        rest = selector[len(INV.LIGHT_TOGGLE_SELECTOR) :].strip()
        if "," in selector or not rest or "[" in rest:
            raise IntakeError(
                "component light override %r is not a plain `%s <selector>` rule; "
                "rewrite it onto palette tokens by hand"
                % (selector, INV.LIGHT_TOGGLE_SELECTOR)
            )
        bases = [rule for rule in rules if rule.selector == rest]
        if len(bases) != 1:
            raise IntakeError(
                "component light override %r has %d base rule(s) for %r; expected "
                "exactly one to point at a token" % (selector, len(bases), rest)
            )
        base = bases[0]
        if base.body_start in rewritten_bases:
            # Two overrides of one base rule would produce two edits to the same
            # span, and the second would be applied to stale text.
            raise IntakeError(
                "two component light overrides target the base rule %r; rewrite "
                "them onto tokens by hand" % rest
            )
        rewritten_bases.add(base.body_start)
        base_declarations = split_declarations(base.declarations(text))
        base_edits = []
        for prop, light_value in split_declarations(override.declarations(text)):
            matches = [v for name, v in base_declarations if name == prop]
            if len(matches) != 1:
                raise IntakeError(
                    "component light override %r sets %r, which the base rule %r "
                    "declares %d time(s); cannot extract a token exactly"
                    % (selector, prop, rest, len(matches))
                )
            dark_value = matches[0]
            if "var(" in dark_value or "var(" in light_value:
                raise IntakeError(
                    "component light override %r already mixes var() into %r; "
                    "finish moving it onto tokens by hand" % (selector, prop)
                )
            name = token_name(rest, prop)
            if name in existing and existing[name] != dark_value:
                raise IntakeError(
                    "token %s is already declared as %r; refusing to reuse the name "
                    "for %s of %r" % (name, existing[name], prop, rest)
                )
            if name in tokens and tokens[name] != (dark_value, light_value):
                raise IntakeError("token %s would need two different values" % name)
            tokens[name] = (dark_value, light_value)
            base_edits.append((prop, dark_value, name))

        # Point the base rule's declarations at the new tokens, in place.
        body = text[base.body_start : base.body_end]
        for prop, dark_value, name in base_edits:
            pattern = re.compile(
                r"(\b%s\s*:\s*)%s(\s*[;}]|\s*$)"
                % (re.escape(prop), re.escape(dark_value))
            )
            body, count = pattern.subn(lambda m: "%svar(%s)%s" % (m.group(1), name, m.group(2)), body, count=1)
            if count != 1:
                raise IntakeError(
                    "could not rewrite %r in the base rule for %r" % (prop, rest)
                )
        edits.append((base.body_start, base.body_end, body))

        # Drop the override, and its whole line when nothing else shares it.
        edits.append(expand_to_full_lines(text, override.start, override.end) + ("",))

    return edits, tokens


def step_component_light_overrides(text, ctx):
    """Move `[data-theme="light"] .foo` components onto tokens (see above)."""
    edits, tokens = plan_component_overrides(text)
    if not edits:
        ctx["extra_light_tokens"] = {}
        return text, False

    toggle = find_rule_span(text, INV.LIGHT_TOGGLE_SELECTOR)
    if toggle is None:
        raise IntakeError(
            "component light override(s) but no `%s { ... }` palette rule to sit "
            "the extracted tokens beside" % INV.LIGHT_TOGGLE_SELECTOR
        )
    dark_rule = (
        "/* Component colours the generator scoped to the toggle path alone, "
        "lifted\n   into tokens by scripts/intake_course.py so BOTH light paths "
        "reach them.\n   Values are unchanged. */\n:root {\n%s}\n\n"
        % "".join("  %s: %s;\n" % (name, dark) for name, (dark, _l) in tokens.items())
    )
    edits.append((toggle[0], toggle[0], dark_rule))

    for start, end, replacement in sorted(edits, key=lambda e: e[0], reverse=True):
        text = text[:start] + replacement + text[end:]

    ctx["extra_light_tokens"] = {name: light for name, (_d, light) in tokens.items()}
    return text, True


def light_palette_is_pinned(text):
    """The test suite's own predicate, plus completeness and color-scheme.

    Completeness is the part the suite cannot state page by page: it allows a
    page to declare only the tokens it uses, so "declares --bg and nothing else"
    passes there. Here the bar is that every PINNED token the page's own :root
    declares gets a light value -- otherwise the accents stay at their dark
    values on a light ground, which is defect 1.
    """
    paths = INV.light_paths(text)
    if len(paths["toggle"]) != 1 or len(paths["media"]) != 1:
        return False
    toggle, media = paths["toggle"][0], paths["media"][0]
    if toggle != media:
        return False
    for token, value in toggle.items():
        if token in LIGHT_PALETTE and LIGHT_PALETTE[token] != value:
            return False
    needed = {t for t in declared_root_tokens(text) if t in LIGHT_PALETTE}
    if needed - set(toggle):
        return False
    if not root_declares_color_scheme(text, ":root"):
        return False
    if not root_declares_color_scheme(text, '[data-theme="dark"]'):
        return False
    return True


def build_light_blocks(text, extra=None):
    """Both light paths, value-identical, from LIGHT_PALETTE plus any extras.

    `extra` holds the light values of tokens lifted out of component overrides.
    They are page-local rather than pinned, so the suite only requires that the
    library agrees on them -- which it does, because every page they appear on
    got them from the same generator output through this same function.
    """
    values = [(t, LIGHT_PALETTE[t]) for t in LIGHT_PALETTE if t in declared_root_tokens(text)]
    values += sorted((extra or {}).items())
    body = "".join("    %s: %s;\n" % (name, value) for name, value in values)
    body_flat = "".join("  %s: %s;\n" % (name, value) for name, value in values)

    parts = []
    if not root_declares_color_scheme(text, ":root"):
        # Must precede the light blocks: :root and [data-theme="light"] have the
        # same specificity, so whichever comes last wins the property.
        parts.append(":root { color-scheme: dark; }\n\n")
    parts.append(
        "/* System preference, only when the reader has NOT made an explicit choice.\n"
        '   The :not([data-theme="dark"]) guard is what lets an explicit "dark" pick\n'
        "   survive on a light-mode OS. Values are pinned in LIGHT_PALETTE\n"
        "   (tests/test_site_invariants.py) and written here by\n"
        "   scripts/intake_course.py. */\n"
        "%s {\n  %s {\n    color-scheme: light;\n%s  }\n}\n\n"
        % (INV.LIGHT_MEDIA_PRELUDE, INV.LIGHT_MEDIA_SELECTOR, body)
    )
    parts.append(
        "/* Explicit choice (localStorage key: %s). Value-identical to the\n"
        "   media block above - the two light paths must never disagree. */\n"
        "%s {\n  color-scheme: light;\n%s}\n"
        % (THEME_STORAGE_KEY, INV.LIGHT_TOGGLE_SELECTOR, body_flat)
    )
    if not root_declares_color_scheme(text, '[data-theme="dark"]'):
        parts.append('\n[data-theme="dark"] { color-scheme: dark; }\n')
    return "".join(parts)


def step_light_palette(text, ctx):
    """Replace both light paths with the pinned palette.

    The generator ships the neutrals only and no system-preference block at all
    (defects 1 and 2). The values come from LIGHT_PALETTE in the test suite --
    the one place they are written down.
    """
    extra = ctx.get("extra_light_tokens") or {}
    if not extra and light_palette_is_pinned(text):
        return text, False

    toggle = find_rule_span(text, INV.LIGHT_TOGGLE_SELECTOR)
    if toggle is None:
        raise IntakeError(
            "no `%s { ... }` rule to replace; the page declares no light theme at "
            "all and this tool will not guess where to put one"
            % INV.LIGHT_TOGGLE_SELECTOR
        )
    blocks = build_light_blocks(text, extra)
    media = find_rule_span(text, INV.LIGHT_MEDIA_PRELUDE)

    edits = [(toggle[0], toggle[1], blocks)]
    if media:
        edits.append(expand_to_full_lines(text, media[0], media[1]) + ("",))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text, True


def step_chrome_css(text, ctx):
    """Styles for the breadcrumb and pager, injected only when absent."""
    css = INV.stylesheet(text)
    if all(selector in css for selector in CHROME_CSS_SELECTORS):
        return text, False
    close = text.find("</style>")
    if close == -1:
        raise IntakeError("no </style> to append the chrome styles to")
    return text[:close] + CHROME_CSS + text[close:], True


def step_theme_prepaint(text, ctx):
    """The pre-paint read, last in <head>."""
    head = INV.HEAD_RE.search(text)
    if INV.PREPAINT_THEME_READ_RE.search(head.group(1)):
        return text, False
    close = text.index("</head>", head.start())
    return text[:close] + PREPAINT_SCRIPT + text[close:], True


def step_theme_toggle(text, ctx):
    """The pinned toggle, verbatim.

    The generated button names the NEXT state ("Use light theme") and has its
    label rewritten from script on every click. The pinned label is
    direction-neutral, so it is accurate in both states and nothing has to be
    rewritten at runtime.
    """
    if text.count(TOGGLE_ELEMENT) == 1:
        return text, False
    pattern = re.compile(r"<button\b[^>]*\bid=\"themeToggle\"[^>]*>.*?</button>", re.S)
    new_text, count = pattern.subn(lambda _m: TOGGLE_ELEMENT, text)
    if count != 1:
        raise IntakeError("expected exactly one #themeToggle element, replaced %d" % count)
    return new_text, True


def step_theme_script(text, ctx):
    """Replace setupTheme() with the pinned implementation.

    This is the storage-key fix (defect 3) and the scripted-aria-label fix at
    once. Preflight has already proved that every theme storage call site lives
    inside this one function, so replacing it whole cannot touch lesson code.
    """
    keys = theme_keys(text)
    scripted = [
        m.group(0)
        for m in INV.SCRIPTED_LABEL_RE.finditer(text)
        if INV.THEMEISH_KEY_RE.search(m.group(2) or "")
    ]
    if keys == {THEME_STORAGE_KEY} and not scripted:
        return text, False
    span = find_function_span(text, "setupTheme")
    if span is None:
        raise IntakeError("no `function setupTheme(){...}` to replace")
    new_text = text[: span[0]] + SETUP_THEME_JS + text[span[1] :]
    # Post-condition, because the replacement depends on a brace scan: if the
    # scan cut the function short, a retired key would survive here rather than
    # at publish time.
    survivors = theme_keys(new_text)
    if survivors != {THEME_STORAGE_KEY}:
        raise IntakeError(
            "after replacing setupTheme() the page still uses theme key(s) %s; "
            "the function boundaries could not be determined safely"
            % ", ".join(sorted(repr(k) for k in survivors))
        )
    return new_text, True


def build_breadcrumb(ctx, indent="    "):
    lesson = ctx["lesson"]
    label = "Lesson %s &middot; %s" % (lesson.ordinal, text_escape(lesson.title))
    return (
        '{i}<nav class="crumbs" aria-label="Breadcrumb">\n'
        '{i}  <a href="../../">Learn library</a>\n'
        '{i}  <span class="crumb-sep" aria-hidden="true">/</span>\n'
        '{i}  <a href="../">{course}</a>\n'
        '{i}  <span class="crumb-sep" aria-hidden="true">/</span>\n'
        '{i}  <span class="crumb-current" aria-current="page">{label}</span>\n'
        "{i}</nav>"
    ).format(i=indent, course=text_escape(ctx["course_title"]), label=label)


def step_breadcrumb(text, ctx):
    """One breadcrumb, right after the masthead (defect 4, half of it)."""
    existing = re.search(r'[ \t]*<nav class="crumbs"[^>]*>.*?</nav>', text, re.S)
    if existing:
        indent = re.match(r"[ \t]*", existing.group(0)).group(0)
        wanted = build_breadcrumb(ctx, indent)
        if existing.group(0) == wanted:
            return text, False
        return text[: existing.start()] + wanted + text[existing.end() :], True

    close = text.find("</header>")
    if close == -1:
        raise IntakeError("no </header> to hang the breadcrumb on")
    indent = re.search(r"([ \t]*)</header>", text).group(1)
    return text[: close + len("</header>")] + "\n" + build_breadcrumb(ctx, indent) + text[
        close + len("</header>") :
    ], True


def build_pager(ctx, indent="    "):
    lessons, index = ctx["lessons"], ctx["index"]
    rows = []
    if index > 0:
        prev = lessons[index - 1]
        rows.append(
            '{i}  <a class="lesson-link prev" href="../{slug}/" rel="prev">'
            "<span>Previous lesson</span><strong>{n} &middot; {title}</strong></a>".format(
                i=indent, slug=prev.slug, n=prev.ordinal, title=text_escape(prev.title)
            )
        )
    if index < len(lessons) - 1:
        nxt = lessons[index + 1]
        rows.append(
            '{i}  <a class="lesson-link next" href="../{slug}/" rel="next">'
            "<span>Next lesson</span><strong>{n} &middot; {title}</strong></a>".format(
                i=indent, slug=nxt.slug, n=nxt.ordinal, title=text_escape(nxt.title)
            )
        )
    else:
        # The course home is not the next DOCUMENT in the sequence, so the link
        # out of the course carries no rel and no ordinal in its label.
        rows.append(
            '{i}  <a class="lesson-link next" href="../">'
            "<span>Next</span><strong>Course home</strong></a>".format(i=indent)
        )
    return "%s%s\n%s\n%s</nav>" % (indent, LESSON_NAV_MARKUP, "\n".join(rows), indent)


def step_pager(text, ctx):
    """One pinned pager, immediately before the footer (defect 4, other half)."""
    existing = re.search(r'[ \t]*<nav class="lesson-nav"[^>]*>.*?</nav>', text, re.S)
    if existing:
        indent = re.match(r"[ \t]*", existing.group(0)).group(0)
        wanted = build_pager(ctx, indent)
        if existing.group(0) == wanted:
            return text, False
        return text[: existing.start()] + wanted + text[existing.end() :], True

    match = re.search(r"([ \t]*)<footer\b", text)
    if not match:
        raise IntakeError("no <footer> to place the pager before")
    indent = match.group(1)
    at = match.start()
    return text[:at] + build_pager(ctx, indent) + "\n\n" + text[at:], True


def step_footer(text, ctx):
    """Keep the generator's notice; add the library's identity lines.

    The notice is CONTENT -- it is written for this course's subject and this
    tool moves it verbatim. The copyright, the licence and the link back to the
    library are SHELL, identical on every page, and the generator ships none of
    them (including the "Educational use only" string the suite requires).
    """
    match = re.search(r"([ \t]*)(<footer\b[^>]*>)(.*?)(</footer>)", text, re.S)
    if not match:
        raise IntakeError("no <footer> element")
    indent, open_tag, inner, close_tag = match.groups()
    if FOOTER_IDENTITY_P in inner and FOOTER_SITE_LINK_P in inner:
        return text, False

    notice = inner.strip()
    if notice and not notice.lstrip().startswith("<p"):
        notice = "<p>%s</p>" % notice
    paragraphs = [p for p in (notice, FOOTER_IDENTITY_P, FOOTER_SITE_LINK_P) if p]
    rebuilt = "%s%s\n%s\n%s%s" % (
        indent,
        open_tag,
        "\n".join("%s  %s" % (indent, p) for p in paragraphs),
        indent,
        close_tag,
    )
    return text[: match.start()] + rebuilt + text[match.end() :], True


STEPS = (
    ("html-root-tag", step_html_tag),
    ("head-metadata", step_head_metadata),
    ("component-light-overrides", step_component_light_overrides),
    ("light-palette", step_light_palette),
    ("chrome-css", step_chrome_css),
    ("prepaint-theme-script", step_theme_prepaint),
    ("theme-toggle", step_theme_toggle),
    ("theme-storage-key", step_theme_script),
    ("breadcrumb", step_breadcrumb),
    ("lesson-pager", step_pager),
    ("footer", step_footer),
)


def normalize(text, ctx):
    """Apply every step in order. Returns (text, [names of steps that changed])."""
    changed = []
    for name, step in STEPS:
        text, did = step(text, ctx)
        if did:
            changed.append(name)
    return text, changed


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

ASSET_SKIP = {"lessons-manifest.json", "README.md", "readme.md"}


def course_assets(source):
    """Files beside the lessons that are published as-is (schemas, data)."""
    return sorted(
        p
        for p in source.iterdir()
        if p.is_file() and p.suffix.lower() != ".html" and p.name not in ASSET_SKIP
    )


def check_position(slug, position, manifest, notes):
    declared = manifest.get("courseNumber")
    if isinstance(declared, int) and declared != position:
        raise IntakeError(
            "--position %d disagrees with the manifest's courseNumber %d"
            % (position, declared)
        )
    homes = [home for _t, home, _s in COURSES]
    home = "/%s/" % slug
    if home in homes:
        expected = homes.index(home) + 1
        if expected != position:
            raise IntakeError(
                "--position %d, but COURSES in tests/test_site_invariants.py puts "
                "%s at position %d" % (position, home, expected)
            )
        notes.append("course is declared in COURSES at position %d" % expected)
    else:
        notes.append(
            "course %s is NOT yet declared in COURSES (tests/test_site_invariants.py); "
            "add it, plus the site index and the path page, by hand" % home
        )


def check_declared_slugs(slug, lessons, notes):
    home = "/%s/" % slug
    for title, course_home, slugs in COURSES:
        if course_home != home:
            continue
        derived = tuple(lesson.slug for lesson in lessons)
        if derived != slugs:
            raise IntakeError(
                "lesson slugs derived from the manifest disagree with the order "
                "declared for %r in tests/test_site_invariants.py:\n"
                "    manifest: %s\n    declared: %s"
                % (title, ", ".join(derived), ", ".join(slugs))
            )
        notes.append("lesson order matches the declared syllabus (%d lessons)" % len(slugs))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="intake_course.py",
        description="Apply the site's pinned standards to a generated course package.",
    )
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--position", required=True, type=int)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "site")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--diff",
        action="store_true",
        help="with --dry-run, print a unified diff for every changed file",
    )
    args = parser.parse_args(argv)

    source = args.source.resolve()
    if not source.is_dir():
        parser.error("--source %s is not a directory" % source)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("--slug must be a lowercase kebab-case URL segment")
    manifest_path = args.manifest or (source / "lessons-manifest.json")

    notes = []
    try:
        manifest = load_manifest(manifest_path)
        lessons, layout = resolve_lessons(manifest, source)
        check_position(args.slug, args.position, manifest, notes)
        check_declared_slugs(args.slug, lessons, notes)

        # -- preflight: read everything, decide nothing is written on failure --
        texts = {}
        failures = []
        for lesson in lessons:
            text = lesson.source.read_text(encoding="utf-8")
            texts[lesson.slug] = text
            for problem in preflight_lesson(lesson, text):
                failures.append("%s: %s" % (lesson.source.name, problem))
        if failures:
            raise IntakeError(
                "preflight failed on %d point(s):\n    %s"
                % (len(failures), "\n    ".join(failures))
            )

        # -- normalize in memory --
        plan = []
        for index, lesson in enumerate(lessons):
            ctx = {
                "lesson": lesson,
                "lessons": lessons,
                "index": index,
                "course_title": args.title,
                "slug": args.slug,
                "canonical": "%s/%s/%s/" % (CANONICAL_ORIGIN, args.slug, lesson.slug),
            }
            try:
                new_text, changed = normalize(texts[lesson.slug], ctx)
            except IntakeError as exc:
                raise IntakeError("%s: %s" % (lesson.source.name, exc))
            plan.append((lesson, new_text, changed))
    except IntakeError as exc:
        print("intake_course: FAILED -- nothing was written", file=sys.stderr)
        print("  %s" % exc, file=sys.stderr)
        return 1

    out_course = (args.out / args.slug).resolve()
    verb = "would write" if args.dry_run else "wrote"
    print(
        "intake_course: %s -> %s\n  source layout: %s, %d lesson(s), course %d (%s)"
        % (source, out_course, layout, len(lessons), args.position, args.title)
    )
    for note in notes:
        print("  note: %s" % note)

    tally = {}
    touched = 0
    for lesson, new_text, changed in plan:
        target = out_course / lesson.slug / "index.html"
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == new_text:
            continue
        touched += 1
        reasons = changed or ["file-does-not-exist" if current is None else "content-differs"]
        for reason in reasons:
            tally[reason] = tally.get(reason, 0) + 1
        print("  %s %s/index.html  [%s]" % (verb, lesson.slug, ", ".join(reasons)))
        if args.diff and current is not None:
            sys.stdout.writelines(
                difflib.unified_diff(
                    current.splitlines(True),
                    new_text.splitlines(True),
                    fromfile="a/%s/index.html" % lesson.slug,
                    tofile="b/%s/index.html" % lesson.slug,
                )
            )
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new_text, encoding="utf-8")

    assets = 0
    for asset in course_assets(source):
        target = out_course / asset.name
        same = target.is_file() and target.read_bytes() == asset.read_bytes()
        if same:
            continue
        assets += 1
        print("  %s %s  [published asset, copied as-is]" % (verb, asset.name))
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, target)

    if touched or assets:
        print("  ---")
        for reason, count in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])):
            print("  %-24s %d lesson(s)" % (reason, count))
        print("  %d of %d lesson(s) changed, %d asset(s)" % (touched, len(lessons), assets))
    else:
        print("  no changes: every lesson already meets the pinned standards")

    home = out_course / "index.html"
    if not home.is_file():
        print(
            "  TODO: %s does not exist. The course home is not generated and not "
            "this tool's to write -- see docs/INTAKE.md." % home
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
