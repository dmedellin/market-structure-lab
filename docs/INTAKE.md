# Onboarding a generated course

The lesson generator produces good **content** and does not keep to this site's
**standards**. Every one of the seven packages that has arrived shipped the same
defects, the first four were repaired by hand, and twice that repair drifted —
at one point a single course carried three incompatible pager families.

`scripts/intake_course.py` is the deterministic fix. It applies the pinned
standards to a fresh package so that onboarding a course is content work and
nothing else.

The generator does not emit one implementation of the theme control, either: it
has emitted **three** so far and has never repeated itself. The tool no longer
tries to memorize them. It reads the theme region statement by statement and
classifies each statement by what it **does**. See
[The theme block](#the-theme-block-classified-not-memorized) — read that section
before touching the tool for the next package.

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
| Its own `localStorage` theme key — **seven** distinct keys, one per package | Classifies the theme region statement by statement and rewrites it to the pinned implementation on `learn-theme` |
| Theme applied after first paint | Injects the pre-paint script last in `<head>`, plus a `<noscript>` rule that hides the JS-only toggle — and **removes** the statement classified as *applies the stored theme at load*, so the stored theme is applied exactly once |
| A toggle whose `aria-label` is rewritten from script, or whose id is the package's own (`themeBtn`) | Replaces **that button only** with the pinned, direction-neutral toggle, and points the icon swap and click listener at the pinned id. In courses 6–7 the button sits in a `.top-actions` div beside a `#resetBtn`: the reset button, its id and its handler are untouched |
| Light values for tokens the palette does not pin (course 5 ships `--bg2`/`--panel2`/`--panel3`/`--line2` where courses 1–4 ship `--bg-2`/`--panel-2`/…) | Carries the package's own light declaration across verbatim, so rewriting the block does not delete it. No value is chosen — a token the package never gave a light value still has none |
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

## The theme block: classified, not memorized

The generator is consistent about the defects and **not** consistent about the
code that carries them. Seven packages have produced **three** theme
implementations, sharing no code and no names:

| | courses 1–4 | course 5 | courses 6–7 |
| --- | --- | --- | --- |
| Toggle | `<button id="themeToggle">`, `aria-label` rewritten from script | `<button id="themeBtn">`, `textContent` swapped between `☀` and `☾` | `<button id="themeBtn">` **inside a `.top-actions` div beside a `#resetBtn`** |
| Theme functions | one `function setupTheme(){…}` holding every storage call | `storedTheme()` + `setTheme(theme)` | `setTheme(theme)` collapsed to a **one-liner**, no reader function |
| Reading the stored value | inside `setupTheme()` | `function storedTheme(){try{return localStorage.getItem("vof-theme")}catch{return null}}` | **inline**: `let saved=null;try{saved=localStorage.getItem('trm-theme')}catch{};` |
| When the stored theme is applied | inside `setupTheme()` | `setTheme(storedTheme()\|\|"dark")` at the end of the script — after first paint, so the page flashes | `setTheme(saved\|\|'dark');` — same flash |
| Repaint hook | `onThemeChange()`, called only if the lesson defines one | `window.redrawLab()` | `window.redrawLab()` |
| Quote style | single | double | single |
| Storage key | `marketStructureTheme`, `market-lab-theme`, `options-course-theme`, `technical-indicators-theme` | `vof-theme` | `trm-theme`, `bts-theme` |

Seven packages, seven keys. **The generator has never shipped this block twice
the same way.**

### Why sequence matching was abandoned

Courses 1–5 were handled by matching fixed statement **sequences** — "these
statements, in this order, and nothing between them". The instinct is right:
never delete script you cannot name. The implementation cannot survive a
generator that rewrites the block every time. Courses 6–7 broke it on three
points at once, and the tool refused with:

> the SHAPE_SET_THEME theme block is not the one this tool recognizes (expected
> `storedTheme()` + `setTheme()` + the post-paint `setTheme(storedTheme()||"dark")`
> + the toggle listener, in that order). It will not delete script it cannot
> account for statement by statement.

That refusal was correct and nothing was written. But the fix could not be
another row: a fourth package would break the fourth row, and the only way to
make one pattern span the variants would be to loosen it until the tool started
guessing — the exact failure the refusal exists to prevent.

So the question asked of the region changed. It is no longer

> are these the statements I memorized, in that order?

but, statement by statement,

> what does this one **do**, and can I account for every token in it?

### The roles

`plan_theme_region()` splits the page script into top-level statements and
classifies each one. The roles are:

| Role | Recognized by |
| --- | --- |
| reads the theme key from localStorage | `localStorage.getItem(<themeish key>)` |
| writes the theme key to localStorage | `localStorage.setItem`/`removeItem(<themeish key>, …)` |
| sets `document.documentElement.dataset.theme` | assignment to `.dataset.theme`, or `setAttribute("data-theme", …)` |
| swaps the toggle glyph | `textContent`/`innerText` written on the toggle element |
| registers the toggle click listener | `addEventListener("click", …)` on the toggle element |
| applies the stored theme at load | a bare top-level call to a function the region defines — **the post-paint flash**, and the one role that is removed rather than reproduced |
| calls a redraw hook | `window.<name>()`, discovered **by name** rather than assumed |
| holds a value only the theme statements read | a declaration (`let saved=null`) referenced by classified statements and by nothing else |

A statement is **classified** only when every role it performs is one of those
**and** every identifier and string literal in it is one the tool can name
(`THEME_VOCABULARY`, plus the names the scan discovers in the file itself:
theme functions, theme-locals, the toggle id, the repaint hook). Classified
statements are deleted and the pinned implementation is written once in their
place. Order does not matter. Whitespace does not matter. Quote style does not
matter.

**Everything else in the region keeps its bytes and its offset.** Course 6 hangs
`$('#resetBtn').addEventListener(…)` in the middle of its theme block; that
handler is the generator's, not the tool's, and it comes through untouched.

Two things follow that are worth stating plainly:

- **The repaint hook is read, not assumed.** `window.redrawLab()` is the
  generator's own hook — the labs resolve every colour from CSS custom
  properties at draw time, so a canvas keeps the ink it was painted with until
  that hook runs. Dropping it would leave a course of charts painted in
  dark-theme ink on the light ground and nothing would fail; it would just look
  broken. The classifier reads the hook's real name out of the statements it is
  about to delete, writes that name into the pinned implementation
  (`build_theme_js(hook)`), and asserts the call survived.
- **The glyph is shell.** The tool already pins the character the button ships
  with, so a package that picks different marks is normalized to `☀`/`☾` rather
  than refused. Courses 6–7 also had the direction inverted (sun while dark);
  the pinned implementation shows the sun in the light theme, as courses 1–5 do.

Run `--explain-theme` to see the classification for every lesson before writing
anything:

```sh
python3 scripts/intake_course.py --source <package> --slug <slug> \
    --title "<Title>" --position N --dry-run --explain-theme
```

```
01-risk-management-fundamentals.html [SHAPE_CLASSIFIED]
  writes the theme key … + sets …dataset.theme + swaps the toggle glyph + calls a redraw hook
                                     function setTheme(theme){document.documentElement…
  holds a value only the theme statements read      let saved=null;
  reads the theme key from localStorage             try{saved=localStorage.getItem('trm-theme')}catch{}
  applies the stored theme at load                  setTheme(saved||'dark');
  registers the toggle click listener               $('#themeBtn').addEventListener('click',…
  toggle: #themeBtn | repaint hook: window.redrawLab()
```

### The two rows that are left

`SHAPES` in `scripts/intake_course.py` still has rows, and a file must still
match **exactly one** — matching none is a refusal, matching two is a refusal:

- **`SHAPE_SETUP_THEME`** is recognized **by name**: courses 1–4 are published
  with `function setupTheme(){…}` and that name is the family. Its pinned
  implementation calls `byId()` and `onThemeChange()`, which the later packages
  do not have, so it stays its own row and its own constant.
- **`SHAPE_CLASSIFIED`** is recognized **by behaviour**. It has no signature to
  widen. It deliberately **declines** any file carrying the `setupTheme`
  signature, so a general recognizer sitting beside a specific one can never
  turn into an ambiguity.

`SHAPE_CLASSIFIED` is not a catch-all. It matches a file whose theme it can
account for, or a file whose theme it can **see and cannot** account for — and
the second case is a refusal that quotes the offending statement. A file with no
theme region at all matches nothing and is still refused.

### Finding the toggle

The toggle is located from the **markup**: every `<button>` whose id,
`aria-label` or `title` names the theme (`themeish_button_ids()`). That id must
then agree with the element the classified statements address. Zero candidates,
two candidates, or a disagreement between markup and script is a refusal —
guessing which button is the theme control is exactly the guess that would strip
course 6's reset button.

### When the eighth package brings a fourth variant

It probably will not need code. Re-ordered statements, a different quote style,
a different glyph, a renamed local, an extra unrelated neighbour, a differently
named repaint hook — all of those are already handled, because none of them
changes what a statement *does*.

If it does refuse, the message names the file and quotes the statement. Then:

1. **Read the statement it quoted.** The refusal is a claim that this tool
   cannot account for a piece of theme logic. Decide whether that is true.
2. **If the statement performs a role the list above is missing**, add the role:
   a detector in `_account_for()` and, if the pinned implementation must
   reproduce it, a line in `THEME_JS_TEMPLATE`. Adding a role is a decision
   about behaviour and belongs in a review.
3. **If the statement is ordinary lesson code the vocabulary does not cover
   yet**, extend `THEME_VOCABULARY` — but only for a token that genuinely
   belongs to theme machinery. The vocabulary is what stops the classifier
   deleting a statement it does not understand; every entry is a small promise.
4. **Never** relax the toggle resolution or the repaint-hook assertion to get a
   package through. Those two are the ones that fail silently in a browser
   rather than loudly in CI.
5. **Prove all four things** before running it for real:

   ```sh
   # 1. the new package normalizes
   python3 scripts/intake_course.py --source <package> --slug <slug> \
       --title "<Title>" --position N --out /tmp/out --dry-run --explain-theme

   # 2. it is idempotent: a second pass reports nothing, and so does a pass
   #    over the normalized TREE
   python3 scripts/intake_course.py --source /tmp/out/<slug> \
       --manifest content/<slug>.manifest.json --slug <slug> \
       --title "<Title>" --position N --out /tmp/out --dry-run

   # 3. the courses already published did not move: still a no-op
   python3 scripts/intake_course.py --source site/technical-indicators \
       --manifest content/technical-indicators.manifest.json \
       --slug technical-indicators --title "Technical Indicators" \
       --position 4 --dry-run
   python3 scripts/intake_course.py --source site/volume-and-order-flow \
       --manifest content/volume-and-order-flow.manifest.json \
       --slug volume-and-order-flow --title "Volume and Order Flow" \
       --position 5 --dry-run

   # 4. a mangled theme block is still refused. Copy one lesson into a scratch
   #    package, add `$('#themeBtn').classList.toggle('x')` to its theme block,
   #    and confirm: exit 1, "nothing was written", the statement quoted, zero
   #    files under the output root.
   ```

   Check 3 and check 4 are the ones worth being stubborn about. Check 3 says the
   change did not disturb what is live; check 4 says the tool did not become
   permissive on the way in.

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
- **an unknown theme shape** — the file matches none of the rows in `SHAPES`
  (no theme control it can recognize at all), or matches two of them. The error
  names every row the tool knows;
- **a statement touching the theme that the tool cannot account for** — it
  performs a role that is not in the list, or it names an identifier or a string
  literal that belongs to no theme role. The error quotes the statement. This is
  the refusal that matters most: *"I do not understand this theme statement"*
  still stops the run, and a neighbouring statement that has nothing to do with
  the theme no longer does;
- **a toggle that cannot be located unambiguously** — no `<button>` whose id,
  label or title names the theme, or two of them, or a markup button and a
  script that address different elements;
- **a repaint hook lost in the rewrite** — the hook the region called is not
  called afterwards, or the region called two of them and the pinned
  implementation calls one;
- **a name the theme region defined and lesson code uses** — `storedTheme()`
  called from a lab is content, and content is not the tool's to edit;
- **a theme key outside every statement the tool classified** — same reason;
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

Three checks, all cheap, and all worth repeating whenever the tool changes.

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

**A theme it cannot account for still refuses.** The classifier being more
tolerant of *irrelevant* statements must never make it looser about *theme*
statements. Copy one lesson into a scratch package with a one-entry manifest and
run it once per mutation:

```sh
python3 scripts/intake_course.py --source /tmp/fixture --slug <slug> \
    --title "<Title>" --position N --out /tmp/fixture-out
```

Each must exit 1, print `nothing was written`, and leave `/tmp/fixture-out`
empty. Five fixtures worth keeping, each with its own message:

| Fixture | Expected refusal |
| --- | --- |
| `$('#themeBtn').classList.toggle('is-spinning')` added to the block | names `classList`, `toggle`, which is not part of any theme role |
| a second `<button aria-label="Theme">` | the toggle element cannot be located unambiguously |
| a second repaint hook inside `setTheme()` | the theme region calls 2 repaint hooks |
| the theme block deleted outright | no theme control was found that this tool can recognize |
| lesson code reading the theme key into a lab | the statement is quoted and refused |

And the mirror image, which must **pass**: a statement that is none of the
tool's business dropped into the middle of the theme block (course 6's
`#resetBtn` handler is exactly this in the real package). It must normalize, and
that statement must survive byte for byte at its own offset.
