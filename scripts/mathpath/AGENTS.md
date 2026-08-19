# scripts/mathpath — the shared renderer, and the arithmetic

Root `AGENTS.md` applies. This adds what is specific to this directory.

**There is no local change here.** One edit to `chrome.py`, `theme.py`,
`render.py`, `progress.py` or `feedback.py` lands on all 336 lessons, and it
reaches the hand-written trading pages too, because
`scripts/add_progress_marks.py` takes its CSS and scripts from `progress.py` and
`feedback.py`. Check both families before calling anything done.

Model: this is the **frontier tier** (`gpt-5.6-sol`, or `codex -p deep`). Small
diffs here are not small changes.

## Chrome mistakes that have shipped, all passing every check at the time

- A container query cannot style its own container. Put `container-type` on the
  child, never on the element you want to size.
- `[hidden]` is `display: none` at USER-AGENT precedence, so any author class
  that sets `display` silently defeats it — `.btn` sets `inline-flex`.
- `topbar()` escapes a mark that is not already markup, so a bare `&#10003;`
  reaches the reader as the literal text `&#10003;`.
- A `<style>` inside `<noscript>` applies only when scripting is OFF.
- `justify-content: space-between` spreads CHILDREN, so a new control must join
  an existing grouped child or it is stranded in open space.

Chrome is the one area the tests cannot answer. Render it and look:
`python3 -m http.server --directory site` then `google-chrome --headless
--screenshot`. Both themes; both light paths are real.

## labs/ — the arithmetic

`node scripts/mathcheck.js` is the check that matters. It executes the shipped
JavaScript extracted from these modules, so it tests what readers run rather
than a reimplementation. **Nothing else in the repository can tell you the
arithmetic is wrong**: a lab reporting the wrong roots renders correctly, passes
HTML validation and passes `labcheck.js`.

When you add arithmetic, add a case to `mathcheck.js`, then break the code on
purpose and confirm the case fails. A test that has never failed has not been
shown to test anything.

`algebra_systems.py` is 264 KB — about 66,000 tokens. Read the function you are
changing, never the module.

## After any change here

    python3 scripts/build_paths.py
    python3 scripts/add_progress_marks.py     # idempotent; second run rewrites nothing
    node scripts/mathcheck.js && node scripts/labcheck.js --generated
    node scripts/progresscheck.js && node scripts/feedbackcheck.js
    python3 -m unittest discover -s tests
