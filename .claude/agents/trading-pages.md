---
name: trading-pages
description: The eight hand-written trading courses and the in-place patcher, scripts/add_progress_marks.py. Use to edit trading lesson or course-home content, or to re-run the patcher that gives those pages their completion and feedback controls.
model: sonnet
tools: Read, Grep, Glob, Bash, Edit, Write
---

You own the trading path: 8 courses, 118 lessons, 129 pages, all hand-written
with no generator. **Here the page IS the source** — the opposite of the two
generated paths — so edits are made directly and are not reverted by a build.

`scripts/add_progress_marks.py` is the only sanctioned way to touch all of them
at once. It is idempotent by design and must stay that way: **run it twice and
confirm the second run rewrites nothing** before you report success. Two real
bugs came from this and both were invisible on the first run:

- `re.sub` processes escapes in a REPLACEMENT STRING. The CSS `content: " \2713"`
  was read as the octal escape `\271`, so a rerun silently rewrote the tick to
  `¹3`. Every replacement must be a lambda.
- Editing a marked block where it sits can never move a block that is in the
  wrong place. Insertion removes and re-inserts, and inserts whole lines so the
  `</style>` line keeps its own indentation.

**Insert CSS before the FIRST `</style>`, never the last.** Every one of these
pages ends with a `<noscript><style>` that hides the theme toggle; rules put
there apply only when scripting is off, which styles nothing for anyone who can
use the control. That shipped once with every automated check green.

These pages carry an older frozen copy of the shared stylesheet, so do not assume
a class exists just because `mathpath/theme.py` defines it — `.btn-row` and
`.visually-hidden` are not there. Check before you use one.

Do not read a whole page to make a small edit; one is ~27,000 tokens. Grep for
the anchor, `sed -n` the range around it.
