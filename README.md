# Market Structure Lab

**Market Structure Lab** — *simple, technical, and fits an interactive format* —
is a seven-part interactive course on how price actually moves, published behind
a catalog of courses. Every page is a single HTML file with its CSS, JavaScript,
and graphics inline — it loads no fonts, no frameworks, no analytics, and no
third-party requests of any kind.

## URL layout

The site is published under one subdomain, `learn.geterdone.io`, and the URL
space is **two levels deep: courses, then lessons**.

```text
/                                   catalog of courses (one course today)
└── /market-structure-lab/          course home — lists the seven labs
    ├── /market-structure-lab/market-structure/                  lab 01
    ├── … five more …
    └── /market-structure-lab/options-contract-selection/        lab 07
```

Nine published URLs, and nothing else is served:

| # | URL | Page | Source |
| --- | --- | --- | --- |
| — | `https://learn.geterdone.io/` | Catalog of courses | `site/index.html` |
| — | `https://learn.geterdone.io/market-structure-lab/` | **Market Structure Lab** — course home | `site/market-structure-lab/index.html` |
| 01 | `https://learn.geterdone.io/market-structure-lab/market-structure/` | Market Structure Lab | `site/market-structure-lab/market-structure/index.html` |
| 02 | `https://learn.geterdone.io/market-structure-lab/ranges-breakouts-liquidity/` | Ranges, Breakouts & Liquidity Sweeps Lab | `site/market-structure-lab/ranges-breakouts-liquidity/index.html` |
| 03 | `https://learn.geterdone.io/market-structure-lab/multi-timeframe-market-structure/` | Multi-Timeframe Market Structure Lab | `site/market-structure-lab/multi-timeframe-market-structure/index.html` |
| 04 | `https://learn.geterdone.io/market-structure-lab/pullbacks-entry-models/` | Pullbacks & Entry Models Lab | `site/market-structure-lab/pullbacks-entry-models/index.html` |
| 05 | `https://learn.geterdone.io/market-structure-lab/invalidation-stops-risk-reward/` | Invalidation, Stops & Reward-to-Risk Lab | `site/market-structure-lab/invalidation-stops-risk-reward/index.html` |
| 06 | `https://learn.geterdone.io/market-structure-lab/volume-relative-strength/` | Volume & Relative Strength Lab | `site/market-structure-lab/volume-relative-strength/index.html` |
| 07 | `https://learn.geterdone.io/market-structure-lab/options-contract-selection/` | Options Contract Selection Lab | `site/market-structure-lab/options-contract-selection/index.html` |

The course and lab 01 share the name *Market Structure Lab*: the course is the
whole seven-lab sequence, lab 01 is its first lesson on structure itself. Both
titles are authoritative and neither changes; navigation numbers the labs so a
reader can tell them apart.

`site/` **is** the document root: its tree maps one-to-one onto public paths, so
a lesson lives one directory below its course both on disk and in the URL.

Because a lesson is now two segments deep, its links up are `../` to the course
home and `../../` to the catalog. Nothing may use a root-absolute `/…` path: the
suite rejects them so the tree also previews correctly under a subpath.

**The seven flat URLs (`/market-structure/`, `/ranges-breakouts-liquidity/`, …)
are gone.** Retiring them was a deliberate, accepted break: there are no redirect
stubs, nothing serves them, and no guard or contract lists them. A request for
one is a plain 404. Do not re-add them to any page map — a path in these maps is
a path that must exist.

That map is declared in five places, and all five must agree:

- `tests/test_site_invariants.py` → `REQUIRED_PAGES` (files on disk);
- `scripts/smoke.py` → `COURSE_PATH` + `COURSE_LESSONS` (served responses);
- `release/contract.json` → `acceptance.checks`, one check id per page
  (`learn-index`, `course-home`, `lesson-page` for lab 01, `lesson-<slug>` for
  the rest);
- `.github/workflows/ci.yml` → the "Published URL space is complete" step;
- `Containerfile.release` and `.github/workflows/pages.yml` (publish-time guards).

A page added to one of them and not the others is a page nothing checks.

Every page below the catalog — the course home as well as all seven labs — is
trading material and carries the same `Educational use only` disclaimer; the
invariant suite fails the build if one loses it.

The apex `geterdone.io` is a separate, live GitHub Pages site. It is not part of
this project and nothing here touches it.

## Local preview

No build step, no dependencies:

```sh
python3 -m http.server 8000 --directory site
```

Then open <http://127.0.0.1:8000/>. Directory URLs resolve to `index.html`, so
`http://127.0.0.1:8000/market-structure-lab/` previews the course home and
`http://127.0.0.1:8000/market-structure-lab/market-structure/` previews lab 01,
exactly as the public paths will serve them.

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

`smoke.py` checks all nine published URLs. Against the plain
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
custom domain). Before uploading it re-checks self-containment and asserts that
all nine pages exist. This path does not touch platform-ops, the shared Caddy
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
tree — the catalog, the course home, and all seven labs — from the `pages.yml`
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
