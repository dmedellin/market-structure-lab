# Working agreement for market-structure-lab

Read this before changing anything. It is the contract between whoever (human or
agent) edits this repository and the platform that will eventually serve it.

## 1. What this repository is

An educational static site published as **Learn** at `https://learn.geterdone.io`:

The site is a subject-agnostic LIBRARY OF PATHS. A path is an ordered sequence of
courses on one subject. There are three: **Trading** (8 courses, 118 lessons,
hand-authored and normalized at intake), **Discrete Mathematics** (8 courses, 106
lessons, GENERATED from `content/discrete_math/`) and **Algebra** (9 courses, 112
lessons, GENERATED from `content/algebra/`). 25 courses and 336 lessons in all.
The published URL space:

| URL | Served from |
| --- | --- |
| `learn.geterdone.io/` | `site/index.html` — the site index: the paths, plus course search |
| `learn.geterdone.io/paths/<subject>/` | `site/paths/<subject>/index.html` — one page per path: `trading`, `discrete-math`, `algebra` |
| `learn.geterdone.io/<course>/` | `site/<course>/index.html` — one of the 25 course homes |
| `learn.geterdone.io/<course>/<lesson>/` | `site/<course>/<lesson>/index.html` — one of the 336 lessons |

The site index and the path pages are SHARED CHROME: they must not assume the
subject is trading — not in copy, not in a footer, not in metadata. Only course
and lesson pages are subject-specific. A path page is neither a course home nor a
lesson, even though it is two segments deep like a lesson; every guard declares
it separately rather than classifying pages by URL shape.

`site/` is the document root. Whatever `site/` contains is exactly what `/` serves;
an extra directory level in `site/` becomes an extra path segment in the public URL.

The full 369-page map (plus eight published JSON assets) is in
[README.md](README.md#url-layout), and it is enforced in five places that must
agree: `REQUIRED_PAGES` in `tests/test_site_invariants.py`, `scripts/smoke.py`,
`acceptance.checks` in `release/contract.json`, the "Published URL space is
complete" step in `.github/workflows/ci.yml`, and the publish guards in
`.github/workflows/pages.yml` and `Containerfile.release`.

Every lesson carries a completion toggle and a feedback panel, so a lesson page
is also a piece of UI. The trading lessons are hand-written and were given those
controls in place by `scripts/add_progress_marks.py`, which is idempotent and is
the only sanctioned way to edit all 129 trading pages at once.

Three sets of URLs are retired, with no redirect stubs: the seven FLAT lesson URLs
course 1 published first, and the whole `/market-structure-lab/` prefix it used
until the paths layer landed (that slug names the repository and the application,
not the course, so the course took its own name — `/market-structure/`), and
`/systems-matrices-and-sequences/`, retired when that course was split in two.
Breaking all three was accepted deliberately, and no guard, test, or contract may
list them again.

The apex `geterdone.io` is a **separate, live GitHub Pages site that this repository
does not control**. Do not deploy to it, reconfigure it, or write anything that
implies we own its records. Linking to it is fine; changing it is out of scope.

## 1a. One path is authored, two are generated

The paths are built in opposite directions and must be edited differently.

**Trading** arrived as eight hand-authored HTML packages and was normalized INTO
the library's conventions by `scripts/intake_course.py`. Its pages are the source
of truth. Edit them directly.

**Discrete Mathematics** and **Algebra** are generated. `content/discrete_math/`
and `content/algebra/` hold them as data — one Python module per course, with the
lessons as dicts — and `scripts/build_paths.py` renders every page from
`scripts/mathpath/` (one stylesheet, one chrome renderer, one lab kit). **Never
edit a page under one of those course slugs by hand**: the next build reverts it,
so the change appears to work and then vanishes.

    python3 scripts/build_paths.py                     # rebuild both
    python3 scripts/build_paths.py --check             # fail if any page is stale
    node scripts/mathcheck.js                          # check the arithmetic itself
    node scripts/labcheck.js --generated               # execute every lab

The last two are different questions and CI runs both. `labcheck.js` proves each
published lab runs, redraws, and survives every value of its own controls;
`mathcheck.js` proves the arithmetic those labs are built on is right, by
executing the shipped JavaScript extracted from
`scripts/mathpath/labs/algebra_core.py`. A lab that reports confidently wrong
roots passes the first and fails the second.

`TestGeneratedPathIsCurrent` fails if a published page differs from what the
content package renders, and if a slug tuple in the test file disagrees with its
content package. Both are silent failures otherwise.

Adding a path: import it in `scripts/build_paths.py` and add it to
`GENERATED_PATHS`; that is the whole registration. It is deliberately not a scan
of `content/` — which paths are published is a decision, and it should be
readable in one place.

Adding a lesson: add a dict to the course module, run the build, then add the URL
to the five declarations listed in section 1 — the suite tells you which are
missing.

**Each path states its own material clause.** The licence line in the shared
footer ends with a sentence naming the intellectual hazard of that subject:
discrete mathematics warns that a worked example is not a proof, algebra that a
step which gives the right answer here is not thereby a valid rule. That clause
is a required `"material"` key on the PATH dict, not a module constant, because
it was a module constant once and became false the moment a second subject
rendered through the same chrome. A disclaimer that is false is worse than none.
`TestGeneratedPathIsCurrent` asserts every generated path states one, that no two
share it, and that it matches the pattern the page sweeps look for.

### A note on page weight

Self-containment means every lesson inlines the whole lab it uses, and the
generated labs share a large exact-arithmetic core. So pages get heavier as the
labs get richer:

| page | raw | gzipped |
| --- | --- | --- |
| Discrete Mathematics lesson | ~57 KB | ~15 KB |
| Algebra, course 1 (5-mode lab) | ~89 KB | ~24 KB |
| Algebra, course 9 (11-mode lab) | ~183 KB | ~50 KB |

The second factor is the number of MODES a lab has. One function serves every
mode of a lab, so a page ships all of them: a reader on the sigma-notation
lesson downloads the annuity and Pascal code as well. Emitting only the active
mode is a real optimisation and a real change to the lab kit; it has not been
made, and 50 KB on the wire does not justify making it yet.

38 KB on the wire is not a problem and needs no action. It IS the number to
check before anyone proposes "just extract the shared JavaScript into one file
both paths load" -- that would halve the bytes and break the invariant in
section 2, which is the one rule this repository does not trade away. If page
weight ever does become a problem, the fix is a smaller lab, not a shared file.

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

## 8. Reading this repository without burning a context window

**87% of this repository by bytes is generated output that nobody should read.**
Measured, tracked files only:

| area | files | bytes | ≈ tokens |
| --- | ---: | ---: | ---: |
| `site/` | 378 | 41.4 MB | **~10,400,000** |
| `content/` | 62 | 2.9 MB | ~714,000 |
| `scripts/` | 36 | 1.9 MB | ~470,000 |
| `release/` | 3 | 1.0 MB | ~245,000 |
| `tests/` | 1 | 0.2 MB | ~52,000 |

One Algebra course-9 lesson is 220 KB — **about 55,000 tokens**. Three of them
do not fit in a context window. This is not a hypothetical cost; it is the
single largest thing that can go wrong with an automated change here.

**Never read these whole. There is no task that requires it:**

- `site/**/*.html` — output. For the two generated paths it is rebuilt from
  `content/` by `scripts/build_paths.py`, so the source of truth is the content
  package and the renderer, never the page. For the trading path the page IS the
  source, but you still want a targeted range, not 27,000 tokens of inlined lab.
- `release/contract.json`, `release/contract.example.json` — 832 KB of generated
  URL manifest between them. Query them; do not open them.
- `scripts/mathpath/labs/algebra_systems.py` (264 KB) and its siblings — read the
  function you are changing.
- `tests/test_site_invariants.py` — 4,000+ lines. Find the class, read the class.

**Do this instead.** Every one of these answers a real question for a few
hundred tokens:

```sh
grep -rl 'data-lesson=' site | wc -l                 # which pages carry a hook
grep -n 'class TestSelfContainment' tests/test_site_invariants.py
sed -n '620,700p' tests/test_site_invariants.py      # then read just that range
python3 -c "import json;d=json.load(open('release/contract.json'));print(len(d['acceptance']['checks']))"
git diff --stat                                      # what actually changed
python3 scripts/build_paths.py --check               # is any page stale (no rebuild)
```

Prefer running a check over reading the thing it checks. The suites in section 7
and the Node checkers below are cheap and they answer questions that reading
cannot: `mathcheck.js` proves the arithmetic, `labcheck.js` proves every lab
runs, `progresscheck.js` proves the completion figures agree with each other,
`feedbackcheck.js` proves the recommendation panel records, ticks, escapes and
exports.

Some invariants exist ONLY in `.github/workflows/ci.yml` and the local suite will
not catch them — "exactly one `<title>` per document" is one, and an SVG
`<title>` violates it. Before pushing, run the workflow's own steps locally
rather than discovering them remotely.

## 9. Which agent does what, and on which model

The work here splits along blast radius, and the model should follow it. The
question is not "how hard is this task" but **"if this goes wrong, how long does
it stay wrong?"** A confidently wrong lab passes every markup check. A wrong
test passes silently, forever. Those get the strongest model regardless of how
small the diff looks.

| agent | tier | Claude | Codex | owns | why this tier |
| --- | --- | --- | --- | --- | --- |
| `site-architect` | deep | opus | `-p deep` | URL space, cross-path design, retirements | one decision reshapes five declarations and the public URL space |
| `chrome-renderer` | deep | opus | `-p deep` | `scripts/mathpath/{chrome,theme,render,progress,feedback}.py` | one edit lands on all 336 lessons at once |
| `lab-arithmetic` | deep | opus | `-p deep` | `scripts/mathpath/labs/`, `scripts/mathcheck.js` | exact rational arithmetic; a wrong answer is invisible to every other check |
| `invariants` | deep | opus | `-p deep` | `tests/test_site_invariants.py` | a test that is wrong passes, and keeps passing |
| `release-safety` | safety | opus | `-p safety` | `release/`, `Containerfile.release`, `.github/workflows/`, `deploy/` | irreversible and expensive; **read-only** |
| `content-author` | build | sonnet | `-p build` | `content/discrete_math/`, `content/algebra/` | high volume, and `mathcheck`/`labcheck` are real gates behind it |
| `trading-pages` | build | sonnet | `-p build` | the eight trading course trees, `scripts/add_progress_marks.py` | hand-authored, blast radius is one course |
| `self-containment` | build | sonnet | `-p build` | the invariant across its declaration sites | a pattern sweep with a fixed rule |
| `test-triage` | triage | haiku | `-p triage` | run the suites, read failures, report which ones and where | mechanical, high volume, no design judgement |

Two rules that matter more than the table:

1. **Escalate on evidence, not on nerves.** If a sonnet agent finds it is
   reasoning about the URL space, the release contract, or whether a test is
   itself correct, it should stop and hand back rather than proceed carefully.
2. **Never let a cheap model decide it is finished.** `test-triage` reports; it
   does not judge whether a failure is acceptable. That is the requesting
   agent's call.

Model names are also the only thing here that dates quickly. The tiers are the
contract; the specific model behind a tier is not.

### Running these

**Claude Code** discovers the nine agents in `.claude/agents/`; each carries its
own model and tool set, and the two that touch production have no edit or write
tool at all.

**Codex** takes the same tiers as profiles in `$CODEX_HOME`, verified against
this machine (CLI 0.144.6):

    codex -p deep      # gpt-5.6-sol   xhigh   workspace-write
    codex -p build     # gpt-5.6-terra medium  workspace-write
    codex -p triage    # gpt-5.6-luna  low     read-only
    codex -p safety    # gpt-5.6-sol   high    read-only

The read-only sandbox is enforced by the runtime, not merely requested in a
prompt — which is the whole reason the production tiers use it. Note that
`codex exec` sets `approval: never` because it is non-interactive; the sandbox
still applies, and that is what stops it.

Codex also reads **nested `AGENTS.md`** files, whose scope is the directory tree
they sit in, with the deepest file winning. `scripts/mathpath/`, `content/`,
`tests/`, `release/` and `.github/` each carry one, so an agent working there
gets that area's rules without the root document having to hold them all. The
root doc has a size budget (`project_doc_max_bytes`, 32 KB by default) and is
already at ~20 KB, so new detail belongs in a nested file, not here.

`site/` deliberately has NO `AGENTS.md`, even though it is the directory that
most needs the warning: everything under `site/` is published, and
`tests/test_site_invariants.py` fails on any published file that is not a
declared URL. Its rule lives in §8 above, which every agent loads anyway.
