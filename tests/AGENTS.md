# tests/ — the guard suite

Root `AGENTS.md` applies. This adds what is specific to this directory.

Model: **frontier tier** (`gpt-5.6-sol`, or `codex -p deep`). The diffs are small
and the failure mode is that a wrong test passes silently, forever.

**A test you cannot make fail is not a test.** Mutation-test every guard you add
before reporting it: break the thing it guards, watch the intended assertion fail
with a message naming the real problem, then restore. Do it on a copy —
`SITE_ROOT=/tmp/... python3 -m unittest ...` — not on the tree.

## Three ways guards here have actually been wrong

- **A test that switched itself off.** A `[hidden]` guard parsed CSS comments as
  rules, so the comment *explaining* the bug marked the class settled. This file
  already has `stylesheet()` and `css_rules()`, which strip comments and handle
  nesting. Use them instead of a fresh regex.
- **A guard encoding a coincidence.** An assertion compared against
  `LIBRARY.length` when it meant "the subjects this case touches". Equal at two
  paths, wrong at three. Derive expectations from the data the case creates.
- **A guard scoped to the wrong set.** Requiring a stylesheet rule on every page
  fails for pages that correctly do not need it. Scope to the CAPABILITY, not to
  a hand-kept list of URLs — then a new path inherits the guard for free.

Add a guard-the-guard assertion whenever a sweep could silently cover nothing
(`assertGreater(len(found), 100, ...)`). An empty sweep must never read as a pass.

**4,400 lines. Do not read it whole** — `grep -n 'class Test'` then `sed -n` the
range. The suite takes ~70s, close enough to a two-minute limit that chaining it
with anything else gets the pair killed part-way.
