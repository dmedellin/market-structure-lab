# Market Structure Lab

`market-structure-lab` is the repository, the application slug and the image
title. What it publishes at `https://learn.geterdone.io/` is a **library of three
interactive courses**, 38 lessons in all, presented as one ordered learning path.
Every page is a single HTML file with its CSS, JavaScript and graphics inline —
it loads no fonts, no frameworks, no analytics, and no third-party requests of
any kind.

## The learning path

The site index is not a menu, it is a **sequence**. Course 1 teaches you to read
what price is doing; course 2 turns that read into a plan you can size, place,
manage and review; course 3 takes that plan into options, where the instrument
itself carries risk the stock chart does not show. A reader is expected to walk
them in order, which is why the three courses share one theme setting, one visual
system, one navigation model, and one set of guards.

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

### Course 3 — Options Trading (16 lessons)

The contract itself: what an option is, what it costs and why, how its value
moves with price, time and volatility, the core single-leg and two-leg
strategies, and what actually happens at expiration.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Options Contract Fundamentals | Decode option contract terms, holder rights, writer obligations, multipliers, premium cash flow, and expiration payoff. |
| 02 | Calls and Puts | Compare long and short calls and puts using rights, obligations, payoff charts, breakeven, and maximum risk. |
| 03 | Moneyness | Classify calls and puts as ITM, ATM, or OTM and calculate intrinsic value from stock and strike. |
| 04 | Option Premium | Decompose theoretical option premium into intrinsic and extrinsic value and change core pricing inputs. |
| 05 | Option Chain and Liquidity | Read option-chain fields, quantify bid-ask friction, inspect activity, and evaluate a limit-order selection. |
| 06 | Expiration and Time Decay | Visualize long-option value by days remaining and inspect theoretical theta, intrinsic value, and extrinsic value. |
| 07 | Implied Volatility | Model option-value changes from IV expansion and contraction separately from underlying movement. |
| 08 | Delta and Gamma | Compare delta-only and delta-plus-gamma estimates with full theoretical repricing and visualize delta across stock prices. |
| 09 | Theta and Vega | Apply time and IV shocks, compare theta-plus-vega estimates with full repricing, and visualize volatility-dependent decay. |
| 10 | Long Calls and Long Puts | Plan long calls and puts with expiration breakeven, premium risk, modeled early-exit value, and payoff charts. |
| 11 | Covered Calls | Build covered calls, compare them with stock-only payoff, and calculate breakeven, maximum profit, and downside risk. |
| 12 | Cash-Secured Puts | Calculate cash reservation, effective purchase price, payoff, maximum premium profit, and downside risk for cash-secured puts. |
| 13 | Vertical Debit Spreads | Construct bull call and bear put debit spreads and calculate debit, breakeven, maximum loss, and maximum profit. |
| 14 | Vertical Credit Spreads | Construct bull put and bear call credit spreads and calculate credit, breakeven, maximum profit, and maximum loss. |
| 15 | Exercise, Assignment, and Expiration | Simulate expiration outcomes, exercise and assignment obligations, resulting shares, and broker-handling risks. |
| 16 | Options Trade Planning | Score a complete options plan across thesis, strategy fit, timing, spread, risk budget, event exposure, and exit rules. |

Course 3 ships one supporting file, `options-trade-plan-schema.json`. Lesson 16
scores a complete options plan and exports it as `options-trade-plan-v1` JSON;
the schema documents that shape. Like course 2's journal schema it is published
as a real URL and checked as JSON, never as a page.

Course 3 also carries outbound reference links to four authoritative,
non-commercial sources — the Options Industry Council (`optionseducation.org`),
FINRA, the SEC's `investor.gov`, and Cboe. They are reviewed origins listed in
`ci.yml`; a link navigates and loads nothing, so the pages stay self-contained.

### Data and risk notice

All charts, trades, prices, fills, and performance results across all three
courses are synthetic educational examples. The pages contain no live data and no
trading signals. Real outcomes can differ because of spread, slippage,
commissions, gaps, taxes, liquidity, assignment, exercise, implied volatility,
time decay, and other factors. Every page below the learning path carries an
`Educational use only` disclaimer and the invariant suite fails the build if one
loses it.

**Options carry their own risk notice, and course 3 states it on the page.**
Options involve risk and are not suitable for every investor. Course 3 is
educational and provides no personalized investment advice and no live trading
signals. Its demonstrations use synthetic prices and a simplified European
Black-Scholes model; they do not model every listed-product feature, dividend,
early-exercise decision, fee, tax, margin rule, or market microstructure effect.
Contract specifications and broker procedures must be verified independently.

## URL layout

The site is published under one subdomain, `learn.geterdone.io`, and the URL
space is **two levels deep: courses, then lessons**.

```text
/                                       the learning path (all three courses)
├── /market-structure-lab/              course 1 home — lists its seven lessons
│   ├── /market-structure-lab/market-structure/                 lesson 1.01
│   ├── … five more …
│   └── /market-structure-lab/options-contract-selection/       lesson 1.07
├── /trade-setup-execution/             course 2 home — lists its fifteen lessons
│   ├── /trade-setup-execution/trade-thesis/                    lesson 2.01
│   ├── … thirteen more …
│   ├── /trade-setup-execution/performance-review/              lesson 2.15
│   └── /trade-setup-execution/trade-journal-schema.json        published asset
└── /options-trading/                   course 3 home — lists its sixteen lessons
    ├── /options-trading/options-contract-fundamentals/         lesson 3.01
    ├── … fourteen more …
    ├── /options-trading/options-trade-planning/                lesson 3.16
    └── /options-trading/options-trade-plan-schema.json         published asset
```

**42 pages and two assets. Nothing else is served:**

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
| — | `https://learn.geterdone.io/options-trading/` | **Options Trading** — course 3 home | `site/options-trading/index.html` |
| 3.01 | `https://learn.geterdone.io/options-trading/options-contract-fundamentals/` | Options Contract Fundamentals | `site/options-trading/options-contract-fundamentals/index.html` |
| 3.02 | `https://learn.geterdone.io/options-trading/calls-and-puts/` | Calls and Puts | `site/options-trading/calls-and-puts/index.html` |
| 3.03 | `https://learn.geterdone.io/options-trading/moneyness/` | Moneyness | `site/options-trading/moneyness/index.html` |
| 3.04 | `https://learn.geterdone.io/options-trading/option-premium/` | Option Premium | `site/options-trading/option-premium/index.html` |
| 3.05 | `https://learn.geterdone.io/options-trading/option-chain-and-liquidity/` | Option Chain and Liquidity | `site/options-trading/option-chain-and-liquidity/index.html` |
| 3.06 | `https://learn.geterdone.io/options-trading/expiration-and-time-decay/` | Expiration and Time Decay | `site/options-trading/expiration-and-time-decay/index.html` |
| 3.07 | `https://learn.geterdone.io/options-trading/implied-volatility/` | Implied Volatility | `site/options-trading/implied-volatility/index.html` |
| 3.08 | `https://learn.geterdone.io/options-trading/delta-and-gamma/` | Delta and Gamma | `site/options-trading/delta-and-gamma/index.html` |
| 3.09 | `https://learn.geterdone.io/options-trading/theta-and-vega/` | Theta and Vega | `site/options-trading/theta-and-vega/index.html` |
| 3.10 | `https://learn.geterdone.io/options-trading/long-calls-and-long-puts/` | Long Calls and Long Puts | `site/options-trading/long-calls-and-long-puts/index.html` |
| 3.11 | `https://learn.geterdone.io/options-trading/covered-calls/` | Covered Calls | `site/options-trading/covered-calls/index.html` |
| 3.12 | `https://learn.geterdone.io/options-trading/cash-secured-puts/` | Cash-Secured Puts | `site/options-trading/cash-secured-puts/index.html` |
| 3.13 | `https://learn.geterdone.io/options-trading/vertical-debit-spreads/` | Vertical Debit Spreads | `site/options-trading/vertical-debit-spreads/index.html` |
| 3.14 | `https://learn.geterdone.io/options-trading/vertical-credit-spreads/` | Vertical Credit Spreads | `site/options-trading/vertical-credit-spreads/index.html` |
| 3.15 | `https://learn.geterdone.io/options-trading/exercise-assignment-and-expiration/` | Exercise, Assignment, and Expiration | `site/options-trading/exercise-assignment-and-expiration/index.html` |
| 3.16 | `https://learn.geterdone.io/options-trading/options-trade-planning/` | Options Trade Planning | `site/options-trading/options-trade-planning/index.html` |
| asset | `https://learn.geterdone.io/options-trading/options-trade-plan-schema.json` | Options trade plan schema (JSON, not a page) | `site/options-trading/options-trade-plan-schema.json` |

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
  `NON_HTML_ASSETS` (both JSON schemas, each declared as an asset rather than by
  loosening any page check);
- `scripts/smoke.py` → `COURSE_PATH`, `COURSE_LESSONS`, `COURSE_2_PATH`,
  `COURSE_2_LESSONS`, `COURSE_3_PATH`, `COURSE_3_LESSONS` and
  `PUBLISHED_ASSETS` (served responses);
- `release/contract.json` → `acceptance.checks`, one check id per URL
  (`learn-index`; `course-home` and `lesson-page`/`lesson-<slug>` for course 1;
  `course2-home` and `course2-lesson-<slug>` for course 2; `course3-home` and
  `course3-lesson-<slug>` for course 3 — course-scoped because a slug is unique
  only within a course; `journal-schema` and `trade-plan-schema` for the two
  assets, each fetched and parsed as JSON);
- `.github/workflows/ci.yml` → the "Published URL space is complete" step;
- `Containerfile.release` and `.github/workflows/pages.yml` (publish-time guards).

A page added to one of them and not the others is a page nothing checks.

Further site-wide invariants exist because three courses now share one origin.
Each of them is something a reader carries across a course boundary, so each is
pinned once and asserted on all 42 pages (`TestPinnedConventions`):

- **One theme key.** Every page persists the reader's light/dark choice under the
  single `localStorage` key `learn-theme`. The per-course keys the three courses
  shipped with (`marketStructureTheme`, `market-lab-theme` and
  `options-course-theme`) silently reset a reader's choice at every course
  boundary; standardizing cost one stored preference, once, and the suite now
  fails any page that invents its own key.
- **One complete pager per course, in one markup.** `prev`/`next` links must walk
  each course in the order declared in `COURSES`, so a reordered syllabus and a
  reordered pager cannot disagree and no lesson becomes a dead end — and the
  pager is always `nav.lesson-nav` with `a.lesson-link.prev` / `a.lesson-link.next`
  anchors. The first lesson omits the prev anchor entirely; the last lesson's
  forward link points at the course home and carries **no** `rel`, because the
  course home is not the next document in the sequence.
- **One light palette.** The light theme has two paths — the explicit toggle
  (`[data-theme="light"]`) and `@media (prefers-color-scheme: light)` for the
  reader who never touches it — and both declare the same token values. Every
  page that declares a light token declares the pinned value for it; component
  rules read tokens, so a `[data-theme="light"] .foo` override (which reaches
  the toggle path only) fails the suite.
- **One theme toggle.** `<button class="icon-btn" id="themeToggle" type="button">`
  with a static, direction-neutral `aria-label` plus `title`. A label rewritten
  from JavaScript has to choose between naming the current theme and the next
  one, and the courses chose differently; a static label is accurate in both
  states and cannot diverge.

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

`smoke.py` checks all 42 published pages plus both JSON assets — one report line
per URL, each page demanding that document's own canonical tag and each asset
fetched, typed and parsed as JSON. Against the plain
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
42 pages exist, and parses both published JSON assets. This path does not touch platform-ops, the shared Caddy
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
tree — the learning path, all three course homes, all 38 lessons, the trade
journal schema and the options trade plan schema — from the `pages.yml`
workflow.

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
