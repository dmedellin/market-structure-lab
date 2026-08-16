# Onboarding a generated course

The lesson generator produces good **content** and does not keep to this site's
**standards**. Every one of the four packages that has arrived shipped the same
defects, every one was repaired by hand, and twice that repair drifted — at one
point a single course carried three incompatible pager families.

`scripts/intake_course.py` is the deterministic fix. It applies the pinned
standards to a fresh package so that onboarding a fifth course is content work
and nothing else.

---

## The rule: reuse vs. rebuild

This is the whole design, and it is worth stating before the steps.

**Reused as-is — copied through byte-for-byte, never re-rendered:**

- the lesson's body content and teaching prose;
- its inline SVG charts and every number behind them — anchor arrays, PRNG,
  thresholds, scoring logic;
- its interactive JavaScript;
- its own component CSS.

This is the valuable, hard-to-rebuild part, and it is also the part that is
tightly coupled to its own markup: the chart code addresses elements by id, the
CSS is written against the exact class names the generator emitted, the quiz
logic reads its own data structures. Re-skinning or re-rendering any of it would
break interactivity for no gain, because **none of it is what drifts**.

**Owned and overwritten — rewritten from pinned constants on every run:**

- the `<head>` metadata block: title, description, canonical, `og:*`,
  `twitter:*`, `theme-color`, icon;
- the light palette, both of its paths;
- the pre-paint theme script, the theme storage key, and the toggle;
- the breadcrumb;
- the lesson pager;
- the footer's identity lines.

These are **shell**. They are mechanical, they are identical in shape on every
page of the library, they are exactly what `tests/test_site_invariants.py` pins,
and they are exactly what a per-course generator has no way to get right — it
cannot know the course's URL, its neighbours in the path, or what the other
courses already do.

> **Rule of thumb for anything new:** if the reader carries it *across* a course
> boundary, the tool owns it. If it only makes sense inside one lesson, the
> generator owns it and the tool must not touch it.

One source of truth: the pinned values — `LIGHT_PALETTE`, `THEME_STORAGE_KEY`,
`THEME_TOGGLE_MARKUP`, `LESSON_NAV_MARKUP`, `CANONICAL_ORIGIN` — are **imported
from the test suite**, never re-typed. A tool that duplicated the palette would
be one more place for it to drift, which is the problem, not the fix.

---

## Onboard a course, in order

Steps 1–4 are the tool. Steps 5–9 are by hand, because each one is a decision
rather than a transformation.

### 1. Put the package somewhere and read its manifest

The package is a flat directory of `NN-name.html` lesson files plus
`lessons-manifest.json`. The manifest is authoritative for lesson **order**,
**titles** and **descriptions**; the tool derives each lesson's published slug
from its `href` (`06-macd.html` → `macd`).

Copy the manifest into `content/<slug>.manifest.json` — see
[`content/README.md`](../content/README.md). The packages arrive in scratch
directories that are not durable, and the manifest is the only record of the
intended copy.

### 2. Declare the course in the tests first

Add the course to `COURSES` in `tests/test_site_invariants.py`: its title, its
home URL, and its lesson slugs **in course order**. Also update the other places
the URL space is declared and which must agree — `scripts/smoke.py`,
`release/contract.json`, `.github/workflows/{ci,pages}.yml`,
`Containerfile.release`, and the map in `README.md`.

Declaring first is deliberate. The tool cross-checks `--position` and the slug
order it derived against `COURSES`, so a slug that does not match what the site
expects fails at intake instead of at publish.

### 3. Dry-run

```sh
python3 scripts/intake_course.py \
    --source /path/to/<course>-course \
    --slug   technical-indicators \
    --title  "Technical Indicators" \
    --position 4 \
    --dry-run
```

It prints one line per lesson listing the defect classes it would repair, then a
tally. Nothing is written. Add `--diff` for a unified diff of every change.

### 4. Run it

Drop `--dry-run`. Output lands in `site/<slug>/<lesson-slug>/index.html`, one
directory per lesson, plus any non-HTML asset the package ships (a JSON schema,
say) copied to `site/<slug>/` unchanged. `--out` redirects the whole tree
somewhere else, which is how the tool is verified without touching `site/`.

Re-run it as often as you like: it is idempotent. Every step checks the
invariant before repairing it, and files are byte-compared before writing, so a
second run reports nothing and writes nothing.

### 5. Write the course home — by hand

The tool does **not** write `site/<slug>/index.html`, because it is not shell.
The course home carries the syllabus, the course's position in the path, and the
course pager to its neighbours. Copy the previous course's home as a starting
point and edit the content. `TestPathPosition` and `TestLessonChain` will tell
you if the pager or the position is wrong.

### 6. Add the course to the path page and the site index — by hand

`site/paths/trading/index.html` and `site/index.html`. Both are shared chrome
and must stay subject-agnostic: `TestSharedChromeIsSubjectAgnostic` fails on
trading vocabulary in the masthead, the navigation or the footer.

### 7. Point the previous course's pager at the new one — by hand

The course before it in the path gains a forward link. This is one edit and the
suite catches it if you forget.

### 8. Run the suite

```sh
cd /home/dmedellin/market-structure-lab && python3 -m unittest discover -s tests
```

### 9. Do the content work

Intake is finished at this point, and what is left is the part that matters: the
teaching. In particular the **participation reading** on every chart — the
second layer that says what the structure implies about buyers and sellers.
The tool writes no teaching copy and never will.

---

## What the tool does

| Defect the generator ships | What intake does |
| --- | --- |
| Placeholder meta descriptions, no canonical, no `og:`/`twitter:` | Overwrites the whole head metadata block from the manifest and the published URL |
| `<html data-theme="dark">` hardcoded | Removes it — it is an explicit choice that beats both light paths |
| Light palette with the neutrals only | Rewrites both light paths from `LIGHT_PALETTE`, covering every pinned token the page's `:root` declares |
| No `@media (prefers-color-scheme: light)` block | Writes one, value-identical to the toggle path |
| No `color-scheme` | Declares `dark` for `:root` and `[data-theme="dark"]`, `light` in both light paths |
| `[data-theme="light"] .foo { … }` component overrides | Lifts the colours into a custom property both light paths declare. **Values are unchanged** — see the note below |
| Its own `localStorage` theme key | Replaces `setupTheme()` with the pinned implementation on `learn-theme` |
| Theme applied after first paint | Injects the pre-paint script last in `<head>`, plus a `<noscript>` rule that hides the JS-only toggle |
| A toggle whose `aria-label` is rewritten from script | Replaces it with the pinned, direction-neutral toggle |
| No breadcrumb, no pager | Injects both, with correct first/last handling: the first lesson omits the prev anchor rather than shipping a disabled one, and the last lesson's forward link points at the course home with no `rel` |
| A footer with no site identity | Keeps the generator's notice prose verbatim and adds the copyright, licence and library link |
| No styles for that chrome | Appends the pinned `.crumbs` / `.lesson-nav` / `.lesson-link` rules, only when absent |

### The one borderline case: component light overrides

A rule like `[data-theme="light"] .json-preview { background: #eef5f9 }` applies
when the reader clicked the toggle and **not** when their OS is light, so that
second reader gets the light ground with dark-theme ink on that one component.
The suite forbids it outright and prescribes the remedy: components read tokens
and nothing else.

Intake performs exactly that extraction and nothing more. It takes the two
literal colours the generator already wrote — the dark one from the base rule,
the light one from the override — puts them in a custom property, and points the
base rule at it. **Every rendered colour in every theme state is identical
afterwards.** No value is chosen, invented or improved; only the mechanism
changes, and the mechanism is shell.

It refuses, loudly, the moment that would stop being exact: a grouped or
compound selector, a base rule that is missing or duplicated, a property the
base does not set as a literal, or a token name already in use. Those are
judgement calls, and judgement calls belong to a person.

---

## What the tool deliberately does not do

- **It does not write the course home.** Not generated, not shell. Step 5.
- **It does not touch `site/index.html`, `site/paths/`, or the tests.** Steps 2,
  6 and 7 are by hand, on purpose: adding a course to the path is a decision
  about the curriculum.
- **It does not restructure the body.** The generator's `<main class="shell">`
  and its masthead stay exactly as shipped. Intake inserts the breadcrumb after
  `</header>` and the pager before `<footer>`; it moves nothing.
- **It does not re-skin or re-render charts, labs or component CSS**, and it
  changes no number used in a calculation.
- **It does not write teaching copy.** No participation readings, no lesson
  prose, no chart annotations. The only prose it moves is the footer notice,
  which it re-wraps verbatim.
- **It does not tidy whitespace.** Formatting outside the regions it owns is
  left alone, so a diff of an intake run is readable and every changed line is
  a line the tool is responsible for.
- **It has no `--force`.** A flag that skips a standard is how drift comes back.

---

## When it refuses

Preflight reads the whole package before a byte is written, and any of these
aborts the run with exit status 1 and **nothing written**:

- **manifest / file-count mismatch** — a declared lesson with no file, or a file
  the manifest does not declare;
- **an unknown theme key shape** — the storage calls must be confined to one
  `function setupTheme(){…}`, which is shell the tool replaces wholesale; a
  theme key touched from anywhere else is content, and content is not the tool's
  to edit;
- **an external resource reference** — scanned with `scripts/smoke.py`'s own
  scanner, the same one CI and the test suite use, so the on-disk verdict and
  the served verdict cannot disagree;
- **structural surprises** — no `<head>`, no `<style>`, more than one
  `<header>`/`<footer>`/theme toggle, an unrecognized element in the head
  metadata region, or a light `@media` block holding more than the palette;
- **retired pager markup** in the source — content the tool will not strip;
- **a component light override the tool cannot extract exactly** (above);
- **`--position` disagreeing** with the manifest's `courseNumber` or with
  `COURSES`, or derived slugs disagreeing with the order declared there.

Every failure names the file and the reason. Fix the package or fix the
declaration, then re-run.

---

## Verifying the tool itself

Two checks, both cheap, and both worth repeating whenever the tool changes.

**Idempotence.** Point it at a course that is already published:

```sh
python3 scripts/intake_course.py \
    --source site/technical-indicators \
    --manifest content/technical-indicators.manifest.json \
    --slug technical-indicators --title "Technical Indicators" \
    --position 4 --dry-run
```

It understands an already-normalized tree (`<slug>/index.html` per lesson) as
well as a flat package, and it must report *no changes*. That is a stronger
claim than "running it twice is stable": it says the tool is a fixed point on
the standard the site actually publishes.

**Output passes the suite.** Normalize a package into a scratch document root,
copy the course home in beside it, and run the suite against it:

```sh
python3 scripts/intake_course.py --source <package> --slug <slug> \
    --title "<Title>" --position N --out /path/to/scratch-site
SITE_ROOT=/path/to/scratch-site python3 -m unittest discover -s tests
```

`SITE_ROOT` must sit inside the repository — the suite reports paths relative to
the repo root.
