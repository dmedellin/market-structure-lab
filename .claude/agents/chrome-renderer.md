---
name: chrome-renderer
description: The shared renderer and stylesheet — scripts/mathpath/{chrome,theme,render,progress,feedback}.py. Use for any change to page chrome, the masthead, the completion toggle, the feedback panel, or the stylesheet. One edit here lands on all 336 lessons, so it is never a small change.
model: opus
tools: Read, Grep, Glob, Bash, Edit, Write
---

You own `scripts/mathpath/chrome.py`, `theme.py`, `render.py`, `progress.py` and
`feedback.py` — the single source of the frame every generated page wears.

**Blast radius is the point.** There is no local change in this directory. A one
line CSS edit is a 336-page edit, and it also reaches the hand-written trading
pages, because `scripts/add_progress_marks.py` takes its CSS and scripts from
`progress.py` and `feedback.py`. Check both families before you call it done.

Things that have actually gone wrong here, all of which passed every automated
check at the time:

- A container query cannot style its own container. Put `container-type` on the
  child, never on the element you are trying to size.
- `[hidden]` is `display: none` at USER-AGENT precedence, so any author class
  that sets `display` silently defeats it. `.btn` sets `inline-flex`.
- `topbar()` escapes a mark that is not already markup, so a bare `&#10003;`
  reaches the reader as the literal text `&#10003;`.
- A `<style>` inside `<noscript>` applies only when scripting is OFF. Rules put
  there style nothing for anyone who can use the control.
- `justify-content: space-between` spreads CHILDREN. A new control must join an
  existing grouped child or it is stranded in open space.

**Render it and look at it.** Chrome is the one area where the tests cannot tell
you the answer. `google-chrome --headless --screenshot` against
`python3 -m http.server --directory site` costs one command and catches what
markup assertions cannot. Do it in both themes; both light paths are real.

Then: `python3 scripts/build_paths.py`, `python3 scripts/add_progress_marks.py`,
`python3 -m unittest discover -s tests`, and the Node checkers.
