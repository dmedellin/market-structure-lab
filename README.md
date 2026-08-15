# Market Structure Lab

`market-structure-lab` is the repository, the application slug and the image
title. What it publishes at `https://learn.geterdone.io/` is a **library of two
interactive courses**, 22 lessons in all, presented as one ordered learning path.
Every page is a single HTML file with its CSS, JavaScript and graphics inline —
it loads no fonts, no frameworks, no analytics, and no third-party requests of
any kind.

## The learning path

The site index is not a menu, it is a **sequence**. Course 1 teaches you to read
what price is doing; course 2 turns that read into a plan you can size, place,
manage and review. A reader is expected to walk them in order, which is why the
two courses share one theme setting, one visual system, and one set of guards.

### Course 1 — Market Structure Lab (7 lessons)

How price actually moves: structure, ranges and liquidity, multi-timeframe
alignment, entry models, invalidation and reward-to-risk, participation, and
finally how the read maps onto an options contract.

| # | Lesson |
| --- | --- |
| 01 | Market Structure Lab |
| 02 | Ranges, Breakouts & Liquidity Sweeps Lab |
| 03 | Multi-Timeframe Market Structure Lab |
| 04 | Pullbacks & Entry Models Lab |
| 05 | Invalidation, Stops & Reward-to-Risk Lab |
| 06 | Volume & Relative Strength Lab |
| 07 | Options Contract Selection Lab |

### Course 2 — Trade Setup and Execution (15 lessons)

Turning a read into an executed, reviewed trade: thesis, levels, confluence, the
three setup families, entry confirmation, stops, targets, reward-to-risk, sizing,
management, backtesting, journaling, and performance review.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Trade Thesis | Build a conditional trade plan from context, setup, trigger, invalidation, target, and no-trade conditions. |
| 02 | Support and Resistance | Place support and resistance zones, classify reactions, and distinguish rejection from acceptance and role reversal. |
| 03 | Confluence | Evaluate setup quality using independent evidence from context, location, trigger, participation, and relative performance. |
| 04 | Breakout Setups | Replay confirmed, retested, failed, and crowded breakouts and evaluate entry, wait, or no-trade decisions. |
| 05 | Pullback Setups | Explore pullback depth, structural validity, reaction evidence, and local structure shifts. |
| 06 | Reversal Setups | Advance through trend maturity, reaction, structure break, retest, and continuation. |
| 07 | Entry Confirmation | Compare reaction, structure-shift, and retest entry models and select the first candle that satisfies each rule. |
| 08 | Stop-Loss Placement | Drag a stop around structural invalidation and see how distance changes illustrative position size. |
| 09 | Profit Targets | Place structural targets, compare R multiples, and evaluate single-target, scale-out, and trailing plans. |
| 10 | Risk-to-Reward | Calculate risk, reward, break-even win rate, and expectancy for adjustable long and short plans. |
| 11 | Position Sizing | Calculate maximum share and long-option quantities from equity, risk percentage, stop distance, premium loss, and costs. |
| 12 | Trade Management | Simulate holding, scaling, break-even stops, trailing, and exits while scoring adherence to a plan. |
| 13 | Backtesting | Generate synthetic trade samples, inspect equity, drawdown, distributions, and compare in-sample with out-of-sample. |
| 14 | Trading Journal | Create, edit, store, import, and export structured journal entries with R outcomes, adherence, and mistake tags. |
| 15 | Performance Review | Import journal data, filter and segment performance, diagnose recurring mistakes, and generate one improvement rule. |

Course 2 ships one supporting file, `trade-journal-schema.json`. Lesson 14
exports `trade-journal-v1` JSON, lesson 15 imports that export directly, and the
schema documents the exchange shape. It is published like any other URL and is
checked by every guard listed below — as JSON, not as a page.

### Data and risk notice

All charts, trades, prices, fills, and performance results across both courses
are synthetic educational examples. The pages contain no live data and no trading
signals. Real outcomes can differ because of spread, slippage, commissions, gaps,
taxes, liquidity, assignment, exercise, implied volatility, time decay, and other
factors. Every page below the learning path carries an `Educational use only`
disclaimer and the invariant suite fails the build if one loses it.

## URL layout

The site is published under one subdomain, `learn.geterdone.io`, and the URL
space is **two levels deep: courses, then lessons**.

```text
/                                       the learning path (both courses)
├── /market-structure-lab/              course 1 home — lists its seven lessons
│   ├── /market-structure-lab/market-structure/                 lesson 1.01
│   ├── … five more …
│   └── /market-structure-lab/options-contract-selection/       lesson 1.07
└── /trade-setup-execution/             course 2 home — lists its fifteen lessons
    ├── /trade-setup-execution/trade-thesis/                    lesson 2.01
    ├── … thirteen more …
    ├── /trade-setup-execution/performance-review/              lesson 2.15
    └── /trade-setup-execution/trade-journal-schema.json        published asset
```

**25 pages and one asset. Nothing else is served:**

| # | URL | Page | Source |
| --- | --- | --- | --- |
| — | `https://learn.geterdone.io/` | Learning path (catalog of courses) | `site/index.html` |
| — | `https://learn.geterdone.io/market-structure-lab/` | **Market Structure Lab** — course 1 home | `site/market-structure-lab/index.html` |
| 1.01 | `https://learn.geterdone.io/market-structure-lab/market-structure/` | Market Structure Lab | `site/market-structure-lab/market-structure/index.html` |
| 1.02 | `https://learn.geterdone.io/market-structure-lab/ranges-breakouts-liquidity/` | Ranges, Breakouts & Liquidity Sweeps Lab | `site/market-structure-lab/ranges-breakouts-liquidity/index.html` |
| 1.03 | `https://learn.geterdone.io/market-structure-lab/multi-timeframe-market-structure/` | Multi-Timeframe Market Structure Lab | `site/market-structure-lab/multi-timeframe-market-structure/index.html` |
| 1.04 | `https://learn.geterdone.io/market-structure-lab/pullbacks-entry-models/` | Pullbacks & Entry Models Lab | `site/market-structure-lab/pullbacks-entry-models/index.html` |
| 1.05 | `https://learn.geterdone.io/market-structure-lab/invalidation-stops-risk-reward/` | Invalidation, Stops & Reward-to-Risk Lab | `site/market-structure-lab/invalidation-stops-risk-reward/index.html` |
| 1.06 | `https://learn.geterdone.io/market-structure-lab/volume-relative-strength/` | Volume & Relative Strength Lab | `site/market-structure-lab/volume-relative-strength/index.html` |
| 1.07 | `https://learn.geterdone.io/market-structure-lab/options-contract-selection/` | Options Contract Selection Lab | `site/market-structure-lab/options-contract-selection/index.html` |
| — | `https://learn.geterdone.io/trade-setup-execution/` | **Trade Setup and Execution** — course 2 home | `site/trade-setup-execution/index.html` |
| 2.01 | `https://learn.geterdone.io/trade-setup-execution/trade-thesis/` | Trade Thesis | `site/trade-setup-execution/trade-thesis/index.html` |
| 2.02 | `https://learn.geterdone.io/trade-setup-execution/support-resistance/` | Support and Resistance | `site/trade-setup-execution/support-resistance/index.html` |
| 2.03 | `https://learn.geterdone.io/trade-setup-execution/confluence/` | Confluence | `site/trade-setup-execution/confluence/index.html` |
| 2.04 | `https://learn.geterdone.io/trade-setup-execution/breakout-setups/` | Breakout Setups | `site/trade-setup-execution/breakout-setups/index.html` |
| 2.05 | `https://learn.geterdone.io/trade-setup-execution/pullback-setups/` | Pullback Setups | `site/trade-setup-execution/pullback-setups/index.html` |
| 2.06 | `https://learn.geterdone.io/trade-setup-execution/reversal-setups/` | Reversal Setups | `site/trade-setup-execution/reversal-setups/index.html` |
| 2.07 | `https://learn.geterdone.io/trade-setup-execution/entry-confirmation/` | Entry Confirmation | `site/trade-setup-execution/entry-confirmation/index.html` |
| 2.08 | `https://learn.geterdone.io/trade-setup-execution/stop-loss-placement/` | Stop-Loss Placement | `site/trade-setup-execution/stop-loss-placement/index.html` |
| 2.09 | `https://learn.geterdone.io/trade-setup-execution/profit-targets/` | Profit Targets | `site/trade-setup-execution/profit-targets/index.html` |
| 2.10 | `https://learn.geterdone.io/trade-setup-execution/risk-to-reward/` | Risk-to-Reward | `site/trade-setup-execution/risk-to-reward/index.html` |
| 2.11 | `https://learn.geterdone.io/trade-setup-execution/position-sizing/` | Position Sizing | `site/trade-setup-execution/position-sizing/index.html` |
| 2.12 | `https://learn.geterdone.io/trade-setup-execution/trade-management/` | Trade Management | `site/trade-setup-execution/trade-management/index.html` |
| 2.13 | `https://learn.geterdone.io/trade-setup-execution/backtesting/` | Backtesting | `site/trade-setup-execution/backtesting/index.html` |
| 2.14 | `https://learn.geterdone.io/trade-setup-execution/trading-journal/` | Trading Journal | `site/trade-setup-execution/trading-journal/index.html` |
| 2.15 | `https://learn.geterdone.io/trade-setup-execution/performance-review/` | Performance Review | `site/trade-setup-execution/performance-review/index.html` |
| asset | `https://learn.geterdone.io/trade-setup-execution/trade-journal-schema.json` | Trade journal exchange schema (JSON, not a page) | `site/trade-setup-execution/trade-journal-schema.json` |

Course 1 and its lesson 01 share the name *Market Structure Lab*: the course is
the whole seven-lesson sequence, lesson 01 is its first lesson on structure
itself. Both titles are authoritative and neither changes; navigation numbers the
lessons so a reader can tell them apart, and every guard identifies a page by its
own full `<link rel="canonical" …>` tag rather than by a title or a path
fragment, because course and lesson paths overlap by prefix and a course home
links to all of its own lessons.

`site/` **is** the document root: its tree maps one-to-one onto public paths, so
a lesson lives one directory below its course both on disk and in the URL.

Because a lesson is two segments deep, its links up are `../` to its own course
home and `../../` to the learning path. Nothing may use a root-absolute `/…` path: the
suite rejects them so the tree also previews correctly under a subpath.

**The seven flat URLs (`/market-structure/`, `/ranges-breakouts-liquidity/`, …)
are gone.** Retiring them was a deliberate, accepted break: there are no redirect
stubs, nothing serves them, and no guard or contract lists them. A request for
one is a plain 404. Do not re-add them to any page map — a path in these maps is
a path that must exist.

That map is declared in five places, and all five must agree:

- `tests/test_site_invariants.py` → `REQUIRED_PAGES` (pages on disk) and
  `NON_HTML_ASSETS` (the JSON asset, declared as an asset rather than by
  loosening any page check);
- `scripts/smoke.py` → `COURSE_PATH`, `COURSE_LESSONS`, `COURSE_2_PATH`,
  `COURSE_2_LESSONS` and `PUBLISHED_ASSETS` (served responses);
- `release/contract.json` → `acceptance.checks`, one check id per URL
  (`learn-index`; `course-home` and `lesson-page`/`lesson-<slug>` for course 1;
  `course2-home` and `course2-lesson-<slug>` for course 2 — course-scoped
  because a slug is unique only within a course; `journal-schema` for the asset);
- `.github/workflows/ci.yml` → the "Published URL space is complete" step;
- `Containerfile.release` and `.github/workflows/pages.yml` (publish-time guards).

A page added to one of them and not the others is a page nothing checks.

Two further site-wide invariants exist because two courses now share one origin:

- **One theme key.** Every page persists the reader's light/dark choice under the
  single `localStorage` key `learn-theme`. The per-course keys the two courses
  shipped with (`marketStructureTheme` and `market-lab-theme`) silently reset a
  reader's choice at the course boundary; standardizing cost one stored
  preference, once, and the suite now fails any page that invents its own key.
- **One complete pager per course.** `prev`/`next` links must walk each course in
  the order declared in `COURSES`, so a reordered syllabus and a reordered pager
  cannot disagree, and no lesson can become a dead end.

The apex `geterdone.io` is a separate, live GitHub Pages site. It is not part of
this project and nothing here touches it.

## Local preview

No build step, no dependencies:

```sh
python3 -m http.server 8000 --directory site
```

Then open <http://127.0.0.1:8000/>. Directory URLs resolve to `index.html`, so
`http://127.0.0.1:8000/trade-setup-execution/` previews course 2's home and
`http://127.0.0.1:8000/trade-setup-execution/trade-thesis/` previews its lesson
01, exactly as the public paths will serve them.

Opening the HTML file directly with `file://` also works, but the local server is
the accurate preview because it exercises the same directory-index behavior as
production.

The same checks CI runs are reproducible locally, with no installation step:

```sh
python3 -m unittest discover -s tests -v        # on-disk invariants
python3 scripts/smoke.py http://127.0.0.1:8000  # acceptance checks against the preview
python3 scripts/validate_release_contract.py \
    release/contract.json release/contract.example.json
```

`smoke.py` checks all 25 published pages plus the JSON asset — one report line
per URL, each demanding that document's own canonical tag. Against the plain
`python3 -m http.server` preview the `internal-health` and `security-headers`
checks fail by design: `/healthz` and the header policy come from the
in-container Caddy (`deploy/Caddyfile`), not from anything in `site/`.

## Repository layout

```text
site/                     the published document root — nothing else is served
Containerfile.release     builds the release image (static files + Caddy)
compose.template.yaml     immutable Compose template rendered by the deploy wrapper
deploy/Caddyfile          in-container web server: headers, cache policy, /healthz
deploy/registry-entry.PROPOSED.yaml   proposed platform registry entry (for review)
release/contract.json                 committed release-contract source (see below)
release/contract.schema.json          release-contract schema
release/contract.example.json         shape reference; never staged as a release
scripts/validate_release_contract.py  stdlib JSON Schema checker for the two above
scripts/smoke.py          standard-library acceptance smoke client
tests/                    on-disk invariant suite (standard library, no install)
.github/workflows/ci.yml       PR checks: HTML, self-containment, links, container
.github/workflows/pages.yml    GitHub Pages publish (the live delivery path)
.github/workflows/release.yml  protected-main build, publish, release metadata
AGENTS.md                 working agreement — read before changing anything
```

## Two delivery paths

**1. GitHub Pages — live.** `.github/workflows/pages.yml` uploads `site/` on every
push to `main` and deploys it to `learn.geterdone.io` (`site/CNAME` holds the
custom domain). Before uploading it re-checks self-containment, asserts that all
25 pages exist, and parses the published JSON asset. This path does not touch platform-ops, the shared Caddy
edge, or any registry reservation, and it is **not** a shortcut around those
gates — they govern the Hetzner platform, which is a different path.

**2. The Hetzner container platform — not built.** That platform serves
applications **only** as containers behind `reverse_proxy 127.0.0.1:<port>`; it
has no file server and no host document root. So the site would ship as an image:
`Containerfile.release` copies `site/` into `/srv` behind a small in-container
Caddy that also answers `GET /healthz` with `200`.

A push to protected `main` re-runs the full check set, renders the deployment
placeholders, builds the image, pushes it to
`ghcr.io/dmedellin/market-structure-lab` by **immutable digest**, and emits the
immutable release contract plus release metadata (image digest, git revision,
release-contract sha256, compose template and rendered-Compose sha256).

`release/contract.json` is the committed contract source and the **single source
of truth for `__LOOPBACK_PORT__` and `__APP_SUBNET__`**. The release workflow
renders `Containerfile.release`, `deploy/Caddyfile` and
`deploy/compose.template.yaml` from it, fills in only the fields the run can
prove, and validates the emitted document against `release/contract.schema.json`.
Because the port and subnet are still unallocated, that render step **fails the
workflow on purpose** with a message naming the allocation gate; no image can be
built until a human allocates them. A future host deploy would consume that
metadata through a root-owned wrapper on a self-hosted runner; the deploy job in
`release.yml` is committed but **inert**, and a public route and DNS pointing at
that host would be a separate, human-reviewed edge transaction.

The normative rules live in `dmedellin/platform-ops`
(`docs/DEPLOYMENT_CONTRACT.md`, `docs/EDGE_ROUTING_CONTRACT.md`,
`docs/APP_ONBOARDING.md`). See [AGENTS.md](AGENTS.md).

## STATUS

**Deployed on GitHub Pages.** `https://learn.geterdone.io/` serves this `site/`
tree — the learning path, both course homes, all 22 lessons and the trade journal
schema — from the `pages.yml` workflow.

**The Hetzner container path remains UNBUILT.** No image of this repository has
ever been built, deployed, or accepted on that platform. As of 2026-08-15, all of
the following are still open:

- **Platform onboarding is unbuilt.** The Hetzner host has no registry entry for
  `market-structure-lab`, no self-hosted repository-scoped runner, and no
  installed deploy wrapper for this app. Nothing has been installed on any host.
- **The loopback port and app subnet are UNALLOCATED.** They appear throughout as
  the literal placeholders `__LOOPBACK_PORT__` and `__APP_SUBNET__`. Allocation is
  an explicit human decision plus a live host preflight and is deliberately not
  automated.
- **No edge route exists** for `learn.geterdone.io` on that host. DNS for the
  subdomain points at GitHub Pages; nothing points at Hetzner, and creating a
  route there is a separate reviewed transaction, not a release.
- **The release deploy job is inert** (`if: false` in `release.yml`) and depends
  on a self-hosted runner that does not exist and a human-approved `production`
  environment that has not been created.
- **No container acceptance has occurred.** No image build, container deployment,
  container smoke run, or SRE acceptance for this repository has ever run. Any
  statement to the contrary is wrong.

## License

[MIT](LICENSE) © 2026 dmedellin.
