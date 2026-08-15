# Market Structure Lab

An interactive, self-contained lesson on market structure — bullish, bearish,
ranging, and shifting — plus the **Learn** catalog page that indexes it. Every
page is a single HTML file with its CSS, JavaScript, and graphics inline: it
loads no fonts, no frameworks, no analytics, and no third-party requests of any
kind.

## URL layout

The site is published under one subdomain, `learn.geterdone.io`:

| URL | Page | Source |
| --- | --- | --- |
| `https://learn.geterdone.io/` | Learn catalog landing | `site/index.html` |
| `https://learn.geterdone.io/market-structure/` | Market Structure Lab lesson | `site/market-structure/index.html` |

`site/` **is** the document root: its tree maps one-to-one onto public paths.

The apex `geterdone.io` is a separate, live GitHub Pages site. It is not part of
this project and nothing here touches it.

## Local preview

No build step, no dependencies:

```sh
python3 -m http.server 8000 --directory site
```

Then open <http://127.0.0.1:8000/>. Directory URLs resolve to `index.html`, so
`http://127.0.0.1:8000/market-structure/` previews the lesson exactly as the
public path will serve it.

Opening the HTML file directly with `file://` also works, but the local server is
the accurate preview because it exercises the same directory-index behavior as
production.

The same checks CI runs are reproducible locally, with no installation step:

```sh
python3 -m unittest discover -s tests -v        # on-disk invariants
python3 scripts/smoke.py http://127.0.0.1:8000  # acceptance checks against the preview
```

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
.github/workflows/release.yml  protected-main build, publish, release metadata
AGENTS.md                 working agreement — read before changing anything
```

## Deployment model (brief)

The target platform serves applications **only** as containers behind
`reverse_proxy 127.0.0.1:<port>`; it has no file server and no host document
root. So this static site ships as an image: `Containerfile.release` copies
`site/` into `/srv` behind a small in-container Caddy that also answers
`GET /healthz` with `200`.

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
built until a human allocates them. A future host deploy would consume that metadata through a
root-owned wrapper on a self-hosted runner; the deploy job in `release.yml` is
committed but **inert**, and the public route and DNS for `learn.geterdone.io`
are a separate, human-reviewed edge transaction.

The normative rules live in `dmedellin/platform-ops`
(`docs/DEPLOYMENT_CONTRACT.md`, `docs/EDGE_ROUTING_CONTRACT.md`,
`docs/APP_ONBOARDING.md`). See [AGENTS.md](AGENTS.md).

## STATUS

**NOT YET DEPLOYED. `https://learn.geterdone.io` does not resolve to this site.**

As of 2026-08-15, all of the following are still open:

- **Platform onboarding is unbuilt.** The Hetzner host has no registry entry for
  `market-structure-lab`, no self-hosted repository-scoped runner, and no
  installed deploy wrapper for this app. Nothing has been installed on any host.
- **The loopback port and app subnet are UNALLOCATED.** They appear throughout as
  the literal placeholders `__LOOPBACK_PORT__` and `__APP_SUBNET__`. Allocation is
  an explicit human decision plus a live host preflight and is deliberately not
  automated.
- **No DNS record and no edge route exist** for `learn.geterdone.io`. Creating
  them is a separate reviewed transaction, not a release.
- **The release deploy job is inert** (`if: false` in `release.yml`) and depends
  on a self-hosted runner that does not exist and a human-approved `production`
  environment that has not been created.
- **No production acceptance has occurred.** No build, deployment, smoke run, or
  SRE acceptance for this repository has ever run. Any statement to the contrary
  is wrong.

## License

[MIT](LICENSE) © 2026 dmedellin.
