---
name: self-containment
description: The zero-network-request invariant and its declaration sites. Use to audit a change for external loads, or when adding a page that is allowed to talk to the network. This is the one rule the repository does not trade away.
model: sonnet
tools: Read, Grep, Glob, Bash, Edit, Write
---

Every page under `site/` must render with **zero network requests**. That is why
the material works offline and carries no third party. Read `AGENTS.md` §2; it is
normative and this is not a substitute for it.

The rule is declared in four independent places and each must be told separately:

1. `tests/test_site_invariants.py` — the on-disk sweep
2. the "Self-containment invariant" step in `.github/workflows/ci.yml`
3. the publish guard in `.github/workflows/pages.yml`
4. `scripts/smoke.py` — against the served site

**Know what the rule actually forbids.** It is about LOADS: `fetch`,
`XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, `importScripts`,
`navigator.serviceWorker`, `<script src>`, remote `<link>`, `@import`, remote
`url()`. It is not a ban on every use of a URL. A `blob:` URL handed to an
`<a download>` is a local save and is allowed; an absolute URL sitting in a JSON
dataset loads nothing; XML namespace identifiers and `rel=canonical` describe
rather than fetch.

Exactly two pages are exempt, by name — `/oauth2/spa/callback/` and `/progress/` —
and only for `login.microsoftonline.com` and `graph.microsoft.com`. The exemption
is per page AND per origin. It buys nothing else: those pages still carry the
pinned palette, both light paths, the shared theme key and a correct canonical.

If a change needs a shared file to save bytes, the answer is no. See the page
weight note in `AGENTS.md` §1a: the fix for a heavy page is a smaller lab, never
a file two pages both load.
