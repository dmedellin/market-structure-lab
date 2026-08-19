# release/ — the path to production

Root `AGENTS.md` applies, and sections 3, 4 and 5 are the relevant ones.

Model: **frontier tier, read-only** (`codex -p safety` — `gpt-5.6-sol` with
`sandbox_mode = "read-only"`). Mistakes here are expensive and hard to reverse,
so the sandbox enforces what instructions only ask for.

**Do not read `contract.json` or `contract.example.json`.** They are 832 KB
between them — roughly 208,000 tokens of generated URL manifest. Query them:

    python3 -c "import json;d=json.load(open('release/contract.json'));print(len(d['acceptance']['checks']))"

## What actually goes wrong here

- **Port and subnet allocation is a human decision and must not be automated.**
  Templates keep `__LOOPBACK_PORT__` and `__APP_SUBNET__`; the contract keeps the
  integers. Never `10.89.2.0/24`. A rendered port committed into a template is a
  release failure, and papering over it is worse than the failure itself.
- **Digests, not tags.** A deployment references `@sha256:<manifest digest>`.
  Layer digests scraped from a build log are NOT the manifest digest. The package
  is public, so an anonymous ghcr pull token is enough — "blocked on credentials"
  is almost always the wrong conclusion.
- **The release workflow's deploy job is INERT.** Cutover is manual. Green
  workflows mean an image exists, not that anything is live.
- **Key run queries to the head SHA.** Listing "the latest runs" returns the
  previous commit's results before the new ones appear, and reads as green.
- Some invariants live only in `.github/workflows/ci.yml`. Run the workflow's own
  steps locally before concluding a change is safe.

The normative contract is in `dmedellin/platform-ops`, and the root-owned host
registry wins over anything written here. Read the real document rather than
reconstructing it from this summary.
