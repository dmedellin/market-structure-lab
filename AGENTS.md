# Working agreement for market-structure-lab

Read this before changing anything. It is the contract between whoever (human or
agent) edits this repository and the platform that will eventually serve it.

## 1. What this repository is

An educational static site published as **Learn** at `https://learn.geterdone.io`:

The published URL space is two levels deep — courses, then lessons:

| URL | Served from |
| --- | --- |
| `learn.geterdone.io/` | `site/index.html` — the catalog of courses |
| `learn.geterdone.io/market-structure-lab/` | `site/market-structure-lab/index.html` — the Market Structure Lab course home |
| `learn.geterdone.io/market-structure-lab/<lesson>/` | `site/market-structure-lab/<lesson>/index.html` — one of the seven labs |

`site/` is the document root. Whatever `site/` contains is exactly what `/` serves;
an extra directory level in `site/` becomes an extra path segment in the public URL.

The full nine-URL map is in [README.md](README.md#url-layout), and it is enforced
in five places that must agree: `REQUIRED_PAGES` in `tests/test_site_invariants.py`,
`scripts/smoke.py`, `acceptance.checks` in `release/contract.json`, the
"Published URL space is complete" step in `.github/workflows/ci.yml`, and the
publish guards in `.github/workflows/pages.yml` and `Containerfile.release`.

The seven FLAT lesson URLs (`/market-structure/` and its siblings) were retired
when the course moved under `/market-structure-lab/`. Breaking them was accepted
deliberately: no redirect stubs exist, and no guard, test, or contract may list
them again.

The apex `geterdone.io` is a **separate, live GitHub Pages site that this repository
does not control**. Do not deploy to it, reconfigure it, or write anything that
implies we own its records. Linking to it is fine; changing it is out of scope.

## 2. The self-containment invariant (non-negotiable)

**Every page under `site/` must render completely with zero network requests beyond
the document itself.** No external origin, no CDN, no web font, no analytics, no
build step, no package manager. CSS goes in `<style>`, JavaScript in `<script>`,
images inline as SVG or `data:` URIs.

Forbidden anywhere in `site/`:

- absolute `http(s)://` or protocol-relative `//host/` references;
- `<script src=...>` in any form — all JavaScript is inline;
- `<link>` to a remote origin, and any `@import`;
- `fetch()`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`,
  `importScripts`, dynamic `import()`, service workers.

Exactly three narrow exceptions exist, all enforced in
`.github/workflows/ci.yml` (step "Self-containment invariant"):

1. **Reviewed navigation origins.** A plain `<a href>` fetches nothing until a
   reader clicks it. The allowlist is the constant `ALLOWED_LINK_ORIGINS` in the
   CI step and currently holds `https://learn.geterdone.io` and
   `https://geterdone.io`. Adding an origin is a reviewed code change — never a
   runtime exception.
2. **XML namespace identifiers** (`http://www.w3.org/2000/svg` and friends) in
   `xmlns` attributes and `createElementNS` calls. They are identifiers, not URLs
   that get fetched.
3. **Same-origin metadata URLs** in `<link rel="canonical">`/`rel="alternate"` and
   `og:url`/`twitter:url`, which describe the page rather than load anything.

Why this matters beyond principle: the in-container Content-Security-Policy in
`deploy/Caddyfile` is `default-src 'none'` with no external origins. A page that
violates the invariant does not degrade — it breaks in production while passing a
casual local file:// check.

## 3. The site is served as a container, not as files

The platform has **no `file_server` and no host document root**. It serves apps
only as `reverse_proxy 127.0.0.1:<port>` to a container
(`platform-ops/docs/EDGE_ROUTING_CONTRACT.md` sections 5–7). Consequences:

- The static site ships inside an image built from `Containerfile.release`, with
  an in-container web server (`deploy/Caddyfile`) that serves `/srv` and answers
  `GET /healthz` with `200`. The health route is required by the deployment
  contract and is produced by that config, not by any file in `site/`.
- Host-native Caddy owns public TLS, ports 80/443, redirects and HSTS. The
  container speaks **plain HTTP** and must never add TLS, certificates, an
  HTTP→HTTPS redirect, HSTS, or trust in `X-Forwarded-*`.
- The container runs as UID 1000 with a read-only root filesystem, `cap_drop:
  [ALL]`, `no-new-privileges`, and bounded CPU/memory/PIDs. Do not weaken any of
  those; they are frozen registry fields, and a routine release may not change
  them.

## 4. Port and subnet allocation is forbidden to automate

Loopback port and private subnet allocation is an **explicit human decision**
validated by a **live host preflight** immediately before onboarding
(`platform-ops/docs/EDGE_ROUTING_CONTRACT.md` section 5). No script, workflow, or
agent may pick one.

- Use the literal placeholders `__LOOPBACK_PORT__` and `__APP_SUBNET__` wherever a
  value is needed. They must be rendered to the same value in every artifact
  (`deploy/Caddyfile`, `Containerfile.release`, `compose.template.yaml`, and the
  registry entry) at release time.
- **Never `10.89.2.0/24`.** The live baseline proves `platform-private-edge` owns
  it. `platform-ops/deployments/pixelbattle-landing/compose.template.yaml` still
  carries that subnet; that file is stale — copy its shape, never its values.
- Registry validation rejects subnet **overlap**, not just equality.
- CI enforces this: the "Unallocated resources stay unallocated" step fails the
  build on a hardcoded loopback mapping, `loopback_port`, `internal_port`, or
  `subnet` in any deployment input file, and on any CIDR that **overlaps** a
  reserved network (not merely one that equals it). Documentation blocks and
  comments that name a forbidden value are prose and are skipped on purpose.

Internal container ports are namespaced and may repeat in general, but this app
publishes `127.0.0.1:<loopback>:<internal>` straight through: `deploy/Caddyfile`
binds the port, `Containerfile.release` EXPOSEs it, and the registry entry repeats
it, so `internal_port` carries the same `__LOOPBACK_PORT__` token and is allocated
in the same human decision. Do not pin it to a number because "internal ports are
free" - 8080 is already claimed on this host.

## 5. Where authority actually lives

The platform contract is normative and lives outside this repository, in
`dmedellin/platform-ops`:

- `docs/DEPLOYMENT_CONTRACT.md` — workflow split, wrapper interface, release
  metadata, pointer/rollback invariants, evidence.
- `docs/EDGE_ROUTING_CONTRACT.md` — registry shape, domains, allocation, Caddy.
- `docs/APP_ONBOARDING.md` — the one-time onboarding transaction and its gates.
- `docs/IMMUTABLE_RELEASE_AND_ACTIVATION.md` — release identity and staging.
- `apps/registry.yaml` and `schemas/app-registry.schema.json` — the registry entry.

Read the real documents; do not reconstruct their rules from memory or from this
summary. **The root-owned host registry wins over anything in this repository.**
Release metadata may narrow behavior; it may never expand scope.

Ownership boundary: this repo owns the site, its tests, PR CI, the protected-main
build/publish job, the immutable Compose template, the release-contract schema and
the smoke client. The platform repo owns the registry, the deploy/rollback
wrapper, runner definitions, sudoers and Caddy fragments. The production host owns
credentials, release directories, pointers and audit records. Do not write a file
here that belongs on the other side of that line —
`deploy/registry-entry.PROPOSED.yaml` is a *proposal for review*, not an installed
registry.

## 6. Never commit

- Secrets of any kind: tokens, registry credentials, runner registration tokens,
  API keys, `.env` files, `*.key`, `*.pem`, certificates. The only credential this
  repository may use is the automatic `GITHUB_TOKEN`. If a secret ever lands in a
  commit, rotate it — deleting the file is not sufficient.
- **A hand-written image digest.** If you cannot verify a real digest against a
  registry, write `__BASE_IMAGE_DIGEST__` and stop. A plausible-looking invented
  `sha256:` is worse than an obvious placeholder: it looks verified.
- An invented loopback port or subnet (see section 4), including "just for now".
- CI status badges, or any claim that a build, deployment, or acceptance passed.
  Nothing here has been deployed and no runner exists; write what is true.
- Vendored third-party assets without shipping rights and recorded provenance.
- Generated build output, `node_modules/`, or anything in `.gitignore`.

## 7. Verifying a change

CI runs on every pull request to `main` and again on the merged commit. It checks
HTML well-formedness, the self-containment invariant, internal link resolution,
the Containerfile, the allocation guard, and that no credential-shaped file is
tracked. Nothing is installed from the network, so it is reproducible locally:

```sh
python3 -m unittest discover -s tests -v       # on-disk invariant suite
python3 -m http.server 8000 --directory site   # then open http://127.0.0.1:8000/
python3 scripts/smoke.py http://127.0.0.1:8000 # acceptance checks against a running server
```

Do not add a package manager, bundler, or test framework to make a check easier.
Dependency-light is a deliberate property of this repository, not an accident.
