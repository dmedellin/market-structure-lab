# market-structure-lab

**[AGENTS.md](AGENTS.md) is the working agreement and it is normative.** Read it
before changing anything. This file is deliberately short: it loads into every
session, so anything duplicated here is paid for on every turn and drifts from
the original the first time one of them is edited.

Two things worth knowing before your first tool call:

**Do not read `site/`.** It is 87% of the repository by bytes — about 10 million
tokens — and one Algebra lesson page alone is ~55,000. For the two generated
paths it is output rebuilt from `content/`; for the trading path the page is the
source, but you still want a grep and a range, not the whole file. The measured
budget and the cheap alternatives are in AGENTS.md §8.

**Route the work.** Nine subagents own distinct areas, and the model tier follows
blast radius rather than apparent difficulty — see AGENTS.md §9 for the table and
the reasoning. Use `site-architect` before changing what URLs exist,
`chrome-renderer` for anything under `scripts/mathpath/`, `lab-arithmetic` for a
number a reader will trust, `invariants` for the guard suite, `release-safety`
(read-only) for the path to production, and `test-triage` to run the lanes.

Verify with the commands in AGENTS.md §7 and the Node checkers in §8. Some
invariants exist only in `.github/workflows/ci.yml`; run the workflow's own steps
locally before pushing rather than discovering them remotely.
