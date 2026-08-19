"""The one stylesheet every Discrete Mathematics page carries.

Written once, embedded verbatim in all 117 pages of the path. That is the point:
TestPinnedConventions exists because eight trading packages each arrived with
their own light palette, and a token that is only ever written HERE cannot pick
up a different value on page 40.

THEME RULE. The palette flips through two independent paths -- the explicit
toggle ([data-theme="light"]) and the system preference, for the reader who
never touches the toggle. A component-level `[data-theme="light"] .foo {...}`
rule reaches only the first, so a light-OS reader gets the light ground with
dark-theme ink on that one component. There are none in this file: every
component reads a token.

Light values are the library's pinned ones (LIGHT_PALETTE in
tests/test_site_invariants.py), contrast-checked against --bg #edf4f8.
"""

# The light palette, written once and interpolated into both light paths below,
# so the two can never disagree by a digit. tests/test_site_invariants.py pins
# these same values and fails any page that re-tunes one.
LIGHT_TOKENS = """      color-scheme: light;
      --bg: #edf4f8;
      --bg-2: #f9fbfd;
      --panel: rgba(255, 255, 255, 0.94);
      --panel-solid: #ffffff;
      --panel-2: #f3f8fb;
      --panel-3: #eaf2f7;
      --text: #102433;
      --muted: #586c7c;
      --line: rgba(24, 62, 88, 0.13);
      --line-strong: rgba(24, 62, 88, 0.24);
      --cyan: #0e7382;
      --cyan-2: #0b6d79;
      --green: #10784f;
      --red: #c22a34;
      --amber: #8a5a06;
      --purple: #6b46d6;
      --blue: #1d5fd0;
      --on-accent: #ffffff;
      --shadow: 0 22px 55px rgba(39, 77, 101, 0.14);"""


from . import feedback


def _light_block(selector, indent):
    body = "\n".join(
        (indent + line.strip()) if line.strip() else line
        for line in LIGHT_TOKENS.splitlines()
    )
    return "%s%s {\n%s\n%s}" % (indent[:-2], selector, body, indent[:-2])


STYLESHEET = """
    /* ---------------------------------------------------------------------
       DESIGN TOKENS -- the only place a theme-dependent colour may live.

       Two light paths, value-identical, both generated from one Python
       constant (theme.LIGHT_TOKENS): the explicit toggle and the system
       preference. Components read tokens and never name a theme.
       --------------------------------------------------------------------- */
    :root {
      color-scheme: dark;
      --bg: #071019;
      --bg-2: #0b1622;
      --panel: rgba(16, 31, 46, 0.91);
      --panel-solid: #101f2e;
      --panel-2: #142638;
      --panel-3: #182d41;
      --text: #edf7ff;
      --muted: #95aabd;
      --line: rgba(170, 202, 226, 0.16);
      --line-strong: rgba(170, 202, 226, 0.3);
      --cyan: #37d7e7;
      --cyan-2: #91f4ff;
      --green: #41e39b;
      --red: #ff7b86;
      --amber: #ffc857;
      --purple: #b69cff;
      --blue: #8fb6ff;
      --on-accent: #041116;
      --shadow: 0 24px 70px rgba(0, 0, 0, 0.34);
      --radius: 20px;
      --radius-sm: 12px;
      --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    }

    /* System preference, only while the reader has made NO explicit choice.
       The :not([data-theme="dark"]) guard is what lets an explicit dark pick
       survive on a light-mode OS. */
__MEDIA_LIGHT__

    /* Explicit choice (localStorage key: learn-theme). Value-identical to the
       block above -- both are generated from the same constant. */
__TOGGLE_LIGHT__

    [data-theme="dark"] { color-scheme: dark; }

    * { box-sizing: border-box; }

    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        radial-gradient(circle at 12% 6%, rgba(55, 215, 231, 0.13), transparent 31rem),
        radial-gradient(circle at 88% 13%, rgba(182, 156, 255, 0.12), transparent 29rem),
        linear-gradient(180deg, var(--bg), var(--bg-2));
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
    }

    button { font: inherit; color: inherit; }
    a { color: inherit; }
    svg { max-width: 100%; }
    p { overflow-wrap: anywhere; }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
    }

    :focus-visible {
      outline: 3px solid var(--cyan);
      outline-offset: 3px;
      border-radius: 6px;
    }

    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      margin: -1px;
      padding: 0;
      overflow: hidden;
      clip: rect(0 0 0 0);
      white-space: nowrap;
      border: 0;
    }

    .skip-link {
      position: absolute;
      left: 12px;
      top: -100px;
      z-index: 60;
      padding: 11px 15px;
      border-radius: 12px;
      color: var(--on-accent);
      background: var(--cyan-2);
      font-weight: 800;
      font-size: 0.88rem;
      text-decoration: none;
      transition: top 140ms ease;
    }
    .skip-link:focus-visible { top: 12px; }

    .shell {
      width: min(1220px, calc(100% - 28px));
      margin: 0 auto;
      padding: 22px 0 64px;
    }

    /* ---------- Top bar ---------- */
    .topbar {
      position: sticky;
      top: 12px;
      z-index: 20;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: color-mix(in srgb, var(--panel-solid) 82%, transparent);
      backdrop-filter: blur(18px);
      box-shadow: var(--shadow);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 11px;
      text-decoration: none;
      min-width: 0;
    }

    .brand-mark {
      display: grid;
      place-items: center;
      width: 38px;
      height: 38px;
      flex: none;
      border-radius: 11px;
      color: var(--on-accent);
      background: linear-gradient(135deg, var(--cyan-2), var(--cyan));
      font-weight: 800;
      font-size: 0.92rem;
      letter-spacing: 0.02em;
    }
    .brand-mark svg { width: 22px; height: 22px; }

    .brand-copy { display: flex; flex-direction: column; min-width: 0; }
    .brand-copy strong { font-size: 0.98rem; letter-spacing: -0.01em; }
    .brand-copy span {
      font-size: 0.74rem;
      color: var(--muted);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .topnav { display: flex; gap: 6px; flex-wrap: wrap; }
    .topnav a {
      padding: 8px 12px;
      border-radius: 10px;
      color: var(--muted);
      text-decoration: none;
      font-size: 0.87rem;
      font-weight: 650;
    }
    .topnav a:hover { color: var(--text); background: var(--panel-2); }
    .topnav a[aria-current="page"] { color: var(--text); background: var(--panel-2); }

    /* The masthead is space-between, so the right-hand controls have to be
       ONE child or they get spread apart with the sign-in stranded in the
       middle of the bar. */
    /* The browser's own [hidden] rule is `display: none` at UA precedence, so
       ANY class that sets display beats it. .btn sets inline-flex, which is why
       "Sign out" sat next to "Sign in" on a page that said "Not signed in":
       the attribute was set correctly and did nothing. Author-level and
       !important so hidden means hidden regardless of what else matches. */
    [hidden] { display: none !important; }

    .topbar-actions { display: flex; align-items: center; gap: 8px; flex: none; }

    /* The masthead sign-in. Sized to sit beside the theme toggle rather than
       compete with it: this library locks nothing, so the control has to be
       findable without reading like the price of entry. The dot goes solid
       green only once a session is actually found. */
    .signin-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      flex: none;
      padding: 0 12px;
      height: 40px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel-2);
      color: var(--muted);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 650;
      white-space: nowrap;
    }
    .signin-btn:hover { color: var(--text); border-color: var(--line-strong); }
    .signin-btn[aria-current="page"] { color: var(--text); border-color: var(--line-strong); }
    .signin-mark { font-size: 0.6rem; color: var(--line-strong); line-height: 1; }
    .signin-btn.is-in .signin-mark { color: var(--green); }

    /* Narrow masthead: the word goes, the dot stays. The label is hidden
       visually but stays in the DOM, so the control keeps "Sign in" as its
       accessible name rather than becoming an unlabelled target. */
    @media (max-width: 560px) {
      .signin-label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap; }
      .signin-btn { padding: 0; width: 40px; justify-content: center; }
    }

    .icon-btn {
      display: grid;
      place-items: center;
      width: 40px;
      height: 40px;
      flex: none;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel-2);
      cursor: pointer;
      font-size: 1.05rem;
    }
    .icon-btn:hover { border-color: var(--line-strong); }

    /* ---------- Breadcrumb ---------- */
    .crumbs {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin: 18px 2px 0;
      font-size: 0.82rem;
      color: var(--muted);
    }
    .crumbs a { text-decoration: none; font-weight: 650; }
    .crumbs a:hover { color: var(--text); text-decoration: underline; }
    .crumb-sep { opacity: 0.5; }
    .crumb-current { color: var(--text); font-weight: 650; }

    .noscript-note {
      margin: 18px 0 0;
      padding: 14px 16px;
      border: 1px solid var(--amber);
      border-radius: var(--radius-sm);
      background: var(--panel-2);
      font-size: 0.9rem;
    }

    /* ---------- Hero ---------- */
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
      gap: 26px;
      align-items: center;
      margin-top: 26px;
      padding: 30px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--panel);
      box-shadow: var(--shadow);
    }
    @media (max-width: 900px) { .hero { grid-template-columns: minmax(0, 1fr); } }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 11px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-2);
      color: var(--cyan);
      font-size: 0.75rem;
      font-weight: 750;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .pulse {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--cyan);
      box-shadow: 0 0 0 4px color-mix(in srgb, var(--cyan) 22%, transparent);
    }

    .hero h1 {
      margin: 14px 0 10px;
      font-size: clamp(1.85rem, 4.1vw, 2.9rem);
      line-height: 1.1;
      letter-spacing: -0.03em;
    }
    .hero p { margin: 0; color: var(--muted); font-size: 1.02rem; }
    .gradient-text {
      background: linear-gradient(120deg, var(--cyan-2), var(--purple));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }

    .hero-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 11px 17px;
      border: 1px solid var(--line-strong);
      border-radius: 12px;
      background: var(--panel-2);
      color: var(--text);
      font-weight: 700;
      font-size: 0.9rem;
      text-decoration: none;
      cursor: pointer;
    }
    .btn:hover { border-color: var(--cyan); }
    .btn.primary {
      border-color: transparent;
      background: linear-gradient(120deg, var(--cyan-2), var(--cyan));
      color: var(--on-accent);
    }
    .btn.small { padding: 8px 13px; font-size: 0.83rem; }

    .hero-visual {
      position: relative;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: var(--radius-sm);
      background: var(--panel-2);
    }
    .hero-visual svg { display: block; width: 100%; height: auto; }
    .float-label {
      position: absolute;
      padding: 5px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: color-mix(in srgb, var(--panel-solid) 88%, transparent);
      color: var(--muted);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    /* ---------- Sections and cards ---------- */
    .section { margin-top: 34px; }
    .section-head {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr);
      gap: 18px;
      align-items: end;
      margin-bottom: 16px;
    }
    @media (max-width: 820px) { .section-head { grid-template-columns: minmax(0, 1fr); } }
    .section-head h2 {
      margin: 4px 0 0;
      font-size: clamp(1.3rem, 2.6vw, 1.75rem);
      letter-spacing: -0.02em;
    }
    .section-head > p { margin: 0; color: var(--muted); font-size: 0.94rem; }
    .kicker {
      margin: 0;
      color: var(--cyan);
      font-size: 0.74rem;
      font-weight: 800;
      letter-spacing: 0.09em;
      text-transform: uppercase;
    }

    .card {
      border: 1px solid var(--line);
      border-radius: var(--radius-sm);
      background: var(--panel);
      box-shadow: var(--shadow);
    }
    .card-pad { padding: 18px; }

    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 14px; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; }
    .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(215px, 1fr)); gap: 14px; }

    .concept-card { padding: 17px; }
    .concept-card h3 { margin: 11px 0 7px; font-size: 1.02rem; letter-spacing: -0.01em; }
    .concept-card p { margin: 0; color: var(--muted); font-size: 0.9rem; }
    .icon {
      display: grid;
      place-items: center;
      width: 32px;
      height: 32px;
      border-radius: 9px;
      background: var(--panel-3);
      color: var(--cyan);
      font-weight: 800;
      font-size: 0.85rem;
    }

    /* ---------- Mathematical notation ----------
       No web font, no MathML dependency, no external renderer: notation is
       plain characters in a monospace run, styled so it reads as an expression
       rather than as prose. Everything a lesson needs (set builder, quantifiers,
       congruences, binomials) is expressible in Unicode this way, and it stays
       selectable, searchable and screen-reader legible. */
    .math {
      padding: 1px 5px;
      border-radius: 5px;
      background: var(--panel-3);
      font-family: var(--mono);
      font-size: 0.92em;
      white-space: nowrap;
    }
    .mathblock {
      margin: 12px 0;
      padding: 13px 15px;
      border: 1px solid var(--line);
      border-left: 3px solid var(--cyan);
      border-radius: 9px;
      background: var(--panel-2);
      color: var(--text);
      font-family: var(--mono);
      font-size: 0.92rem;
      line-height: 1.75;
      overflow-x: auto;
      white-space: pre;
    }

    .defbox, .thm, .example {
      margin: 14px 0;
      padding: 14px 16px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
    }
    .defbox { border-left: 3px solid var(--purple); }
    .thm { border-left: 3px solid var(--amber); }
    .example { border-left: 3px solid var(--green); }
    .defbox > .label, .thm > .label, .example > .label {
      display: block;
      margin-bottom: 6px;
      font-size: 0.71rem;
      font-weight: 800;
      letter-spacing: 0.09em;
      text-transform: uppercase;
    }
    .defbox > .label { color: var(--purple); }
    .thm > .label { color: var(--amber); }
    .example > .label { color: var(--green); }
    .defbox p, .thm p, .example p { margin: 0 0 8px; font-size: 0.92rem; }
    .defbox p:last-child, .thm p:last-child, .example p:last-child { margin-bottom: 0; }

    .proof { margin: 12px 0 0; padding-left: 14px; border-left: 2px solid var(--line-strong); }
    .proof p { margin: 0 0 8px; font-size: 0.9rem; color: var(--muted); }
    .proof p:last-child { margin-bottom: 0; }
    .qed { color: var(--cyan); font-weight: 800; }

    .prose p { font-size: 0.95rem; }
    .prose p:first-child { margin-top: 0; }
    .prose p:last-child { margin-bottom: 0; }
    .prose ul, .prose ol { margin: 10px 0; padding-left: 22px; font-size: 0.93rem; }
    .prose li { margin-bottom: 6px; }
    .prose h3 { margin: 0 0 10px; font-size: 1.05rem; letter-spacing: -0.01em; }

    /* ---------- The lab ---------- */
    .lab-layout {
      display: grid;
      grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr);
      gap: 14px;
      align-items: start;
    }
    @media (max-width: 980px) { .lab-layout { grid-template-columns: minmax(0, 1fr); } }

    .lab-main { padding: 16px; }
    .lab-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
    }
    .lab-title { display: flex; flex-direction: column; }
    .lab-title strong { font-size: 0.98rem; }
    .lab-title span { color: var(--muted); font-size: 0.79rem; }
    .inline-legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.76rem; color: var(--muted); }
    .inline-legend span { display: inline-flex; align-items: center; gap: 6px; }
    .legend-swatch { width: 10px; height: 10px; border-radius: 3px; background: currentColor; }
    .tone-cyan { color: var(--cyan); }
    .tone-purple { color: var(--purple); }
    .tone-green { color: var(--green); }
    .tone-amber { color: var(--amber); }
    .tone-red { color: var(--red); }
    .tone-blue { color: var(--blue); }
    .tone-muted { color: var(--muted); }

    .lab-stage {
      min-height: 210px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
      overflow-x: auto;
    }
    .lab-stage svg { display: block; width: 100%; height: auto; }

    /* ---------- Graphs ----------
       Tokens only. A component override scoped to [data-theme="light"] would
       light the toggle path and leave the reader whose OS is light with a dark
       graph on a light page, which is the exact failure this library pins
       against elsewhere. Everything below inherits from the palette instead. */
    .plot-grid { stroke: var(--line); stroke-width: 1; }
    .plot-axis { stroke: var(--line-strong); stroke-width: 1.6; }
    .plot-tick { fill: var(--muted); font-family: var(--mono); font-size: 11px; }
    .plot-tickmark { stroke: var(--line-strong); stroke-width: 1.6; }
    .plot-curve { fill: none; stroke: var(--cyan); stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
    .plot-curve.alt { stroke: var(--purple); }
    .plot-curve.parent { stroke: var(--muted); stroke-width: 1.8; stroke-dasharray: 5 5; }
    .plot-curve.warn { stroke: var(--red); }
    .plot-curve.good { stroke: var(--green); }
    .plot-point { fill: var(--amber); stroke: var(--bg); stroke-width: 1.6; }
    .plot-point.root { fill: var(--green); }
    .plot-point.vertex { fill: var(--purple); }
    /* An open circle is a point the function does NOT take -- a hole, an open
       endpoint. Filled versus hollow is the whole content of several lessons,
       so the two never differ by colour alone. */
    .plot-hole { fill: var(--panel-2); stroke: var(--cyan); stroke-width: 2.2; }
    .plot-asym { stroke: var(--red); stroke-width: 1.5; stroke-dasharray: 6 5; }
    .plot-aux { stroke: var(--muted); stroke-width: 1.4; stroke-dasharray: 4 4; }
    .plot-label { fill: var(--text); font-family: var(--mono); font-size: 12px; }
    .plot-shade { fill: var(--cyan); opacity: 0.16; }
    .plot-shade.alt { fill: var(--purple); opacity: 0.16; }
    .plot-interval { stroke: var(--cyan); stroke-width: 4; }
    .plot-end { stroke: var(--cyan); stroke-width: 2.4; }
    .plot-end.closed { fill: var(--cyan); }
    .plot-end.open { fill: var(--panel-2); }

    .side-panel { display: flex; flex-direction: column; gap: 13px; padding: 17px; }
    .side-panel h3 { margin: 0; font-size: 1rem; }
    .side-panel > p { margin: 0; color: var(--muted); font-size: 0.86rem; }

    .field { display: flex; flex-direction: column; gap: 6px; }
    .field label { color: var(--muted); font-size: 0.78rem; font-weight: 700; }
    .field select, .field input[type="text"], .field input[type="number"] {
      width: 100%;
      padding: 9px 11px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--panel-2);
      color: var(--text);
      font: inherit;
      font-size: 0.88rem;
    }
    .field select { font-family: inherit; }
    .field input[type="text"], .field input[type="number"] { font-family: var(--mono); }

    .range-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
    .range-value {
      padding: 2px 8px;
      border-radius: 7px;
      background: var(--panel-3);
      color: var(--cyan);
      font-family: var(--mono);
      font-size: 0.82rem;
      font-weight: 700;
    }
    input[type="range"] { width: 100%; accent-color: var(--cyan); }

    .small-copy { color: var(--muted); font-size: 0.8rem; }

    .btn-row { display: flex; gap: 8px; flex-wrap: wrap; }

    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(94px, 1fr)); gap: 8px; }
    .kpi {
      display: flex;
      flex-direction: column;
      gap: 3px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--panel-2);
    }
    .kpi span { color: var(--muted); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
    .kpi strong { font-family: var(--mono); font-size: 0.98rem; overflow-wrap: anywhere; }

    .status-banner {
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-left: 3px solid var(--cyan);
      border-radius: 9px;
      background: var(--panel-2);
      color: var(--text);
      font-size: 0.86rem;
    }

    /* ---------- Tables: truth tables, matrices, traces ---------- */
    .table-wrap { overflow-x: auto; }
    table.tt {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--mono);
      font-size: 0.83rem;
    }
    table.tt caption {
      margin-bottom: 8px;
      color: var(--muted);
      font-family: inherit;
      font-size: 0.8rem;
      text-align: left;
    }
    table.tt th, table.tt td {
      padding: 6px 9px;
      border: 1px solid var(--line);
      text-align: center;
      white-space: nowrap;
    }
    table.tt th { background: var(--panel-3); color: var(--muted); font-weight: 700; }
    table.tt td.t { color: var(--green); font-weight: 700; }
    table.tt td.f { color: var(--red); font-weight: 700; }
    table.tt tr.focus td { background: color-mix(in srgb, var(--cyan) 14%, transparent); }
    table.tt td.on { background: color-mix(in srgb, var(--cyan) 18%, transparent); color: var(--text); }
    table.tt th.rowhead { background: var(--panel-3); text-align: right; }

    .chip {
      display: inline-block;
      margin: 2px 4px 2px 0;
      padding: 3px 9px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-2);
      font-family: var(--mono);
      font-size: 0.79rem;
    }
    .chip.ok { border-color: var(--green); color: var(--green); }
    .chip.no { border-color: var(--red); color: var(--red); }
    .chip.hi { border-color: var(--cyan); color: var(--cyan); }

    /* ---------- Practice ---------- */
    .practice { display: flex; flex-direction: column; gap: 11px; padding: 18px; }
    .practice-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
    .practice-head h3 { margin: 0; font-size: 1rem; }
    .score {
      padding: 4px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-2);
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 700;
    }
    .choice-grid { display: grid; gap: 8px; }
    .choice {
      padding: 10px 13px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
      color: var(--text);
      font-size: 0.88rem;
      text-align: left;
      cursor: pointer;
    }
    .choice:hover { border-color: var(--cyan); }
    .choice.right { border-color: var(--green); color: var(--green); }
    .choice.wrong { border-color: var(--red); color: var(--red); }
    .feedback {
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--panel-2);
      color: var(--muted);
      font-size: 0.85rem;
    }

    /* ---------- Lists, callouts, notes ---------- */
    .lesson-list { display: flex; flex-direction: column; gap: 10px; }
    .lesson-row { display: flex; gap: 12px; align-items: flex-start; }
    .lesson-row .num {
      display: grid;
      place-items: center;
      width: 26px;
      height: 26px;
      flex: none;
      border-radius: 8px;
      background: var(--panel-3);
      color: var(--cyan);
      font-family: var(--mono);
      font-size: 0.78rem;
      font-weight: 800;
    }
    .lesson-row strong { display: block; font-size: 0.92rem; }
    .lesson-row span { display: block; color: var(--muted); font-size: 0.85rem; }

    .callout { display: flex; gap: 12px; align-items: flex-start; }
    .callout .mark {
      display: grid;
      place-items: center;
      width: 28px;
      height: 28px;
      flex: none;
      border-radius: 9px;
      background: var(--panel-3);
      color: var(--green);
      font-weight: 800;
    }
    .callout strong { display: block; font-size: 0.94rem; }
    .callout p { margin: 5px 0 0; color: var(--muted); font-size: 0.88rem; }

    .note {
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: var(--panel-2);
      color: var(--muted);
      font-size: 0.85rem;
    }
    .note strong { color: var(--text); }

    .rule-output {
      padding: 13px 15px;
      border: 1px dashed var(--line-strong);
      border-radius: 10px;
      background: var(--panel-2);
      color: var(--muted);
      font-size: 0.89rem;
    }

    /* ---------- Course home: syllabus ---------- */
    .syllabus { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
    .syllabus-item {
      display: flex;
      gap: 13px;
      align-items: flex-start;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel);
      text-decoration: none;
      box-shadow: var(--shadow);
    }
    .syllabus-item:hover { border-color: var(--cyan); }
    .syllabus-item .num {
      display: grid;
      place-items: center;
      width: 32px;
      height: 32px;
      flex: none;
      border-radius: 9px;
      background: var(--panel-3);
      color: var(--cyan);
      font-family: var(--mono);
      font-size: 0.82rem;
      font-weight: 800;
    }
    .syllabus-item strong { display: block; font-size: 0.95rem; letter-spacing: -0.01em; }
    .syllabus-item span { display: block; margin-top: 4px; color: var(--muted); font-size: 0.85rem; }

    /* ---------- Path page: the spine ---------- */
    .spine { display: flex; flex-direction: column; gap: 12px; }
    .spine-item {
      display: grid;
      grid-template-columns: 46px minmax(0, 1fr);
      gap: 15px;
      align-items: start;
      padding: 17px;
      border: 1px solid var(--line);
      border-radius: 13px;
      background: var(--panel);
      text-decoration: none;
      box-shadow: var(--shadow);
    }
    .spine-item:hover { border-color: var(--cyan); }
    .spine-num {
      display: grid;
      place-items: center;
      width: 46px;
      height: 46px;
      border-radius: 13px;
      background: linear-gradient(135deg, var(--cyan-2), var(--cyan));
      color: var(--on-accent);
      font-family: var(--mono);
      font-size: 1rem;
      font-weight: 800;
    }
    .spine-body strong { display: block; font-size: 1.05rem; letter-spacing: -0.01em; }
    .spine-body p { margin: 6px 0 0; color: var(--muted); font-size: 0.9rem; }
    .spine-meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 9px;
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .spine-meta span {
      padding: 3px 9px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel-2);
    }

    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin: 0; }
    .stats > div {
      padding: 13px 15px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel-2);
    }
    .stats dt { color: var(--muted); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; }
    .stats dd { margin: 5px 0 0; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; }
    .stats dd small { display: block; margin-top: 2px; color: var(--muted); font-size: 0.76rem; font-weight: 600; letter-spacing: 0; }

    /* ---------- The lesson pager ---------- */
    .lesson-nav {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
      margin-top: 34px;
    }
    .lesson-link {
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 15px 17px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel-2);
      text-decoration: none;
    }
    .lesson-link:hover { border-color: var(--cyan); }
    .lesson-link span { color: var(--muted); font-size: 0.74rem; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; }
    .lesson-link strong { font-size: 0.94rem; letter-spacing: -0.01em; }
    .lesson-link.next { text-align: right; }
    .lesson-link.prev + .lesson-link.next { grid-column: auto; }

    /* ---------- Course pager (path-nav) ----------
       The course-to-course control, matching the library's existing shape:
       nav.path-nav holding a.path-move prev / a.path-move next. Distinct from
       the LESSON pager (.lesson-nav) on purpose -- one moves within a course,
       the other between courses, and collapsing them would make "next" mean
       two things. */
    .path-nav {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
      margin-top: 30px;
    }
    .path-move {
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 15px 17px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel-2);
      text-decoration: none;
    }
    .path-move:hover { border-color: var(--cyan); }
    .path-move span { color: var(--muted); font-size: 0.74rem; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; }
    .path-move strong { font-size: 0.94rem; letter-spacing: -0.01em; }
    .path-move.next { text-align: right; }
    .path-move.is-complete { border-color: var(--line-strong); background: var(--panel-3); }

    /* ---------- Completion marks ----------
       A note the reader makes to themselves, kept in localStorage. Never a
       network request on a lesson page, and never a gate: the material reads
       identically whether or not anything is ticked. */
    .progress-bar {
      display: flex;
      flex-direction: column;
      gap: 7px;
      margin-top: 22px;
      padding: 15px 17px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel-2);
    }
    .progress-toggle {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      align-self: flex-start;
      padding: 10px 16px;
      border: 1px solid var(--line-strong);
      border-radius: 10px;
      background: var(--panel);
      color: var(--text);
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }
    .progress-toggle:hover { border-color: var(--cyan); }
    .progress-toggle .progress-tick {
      display: grid;
      place-items: center;
      width: 20px;
      height: 20px;
      border-radius: 6px;
      border: 1px solid var(--line-strong);
      background: var(--panel-2);
      color: transparent;
      font-size: 0.8rem;
      font-weight: 900;
    }
    .progress-toggle.is-done { border-color: var(--green); color: var(--green); }
    .progress-toggle.is-done .progress-tick {
      border-color: var(--green);
      background: var(--green);
      color: var(--on-accent);
    }
    .progress-note { margin: 0; color: var(--muted); font-size: 0.82rem; }
    .progress-note a { color: var(--cyan); }
    .course-progress {
      margin: 0;
      color: var(--muted);
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .syllabus-item.is-done .num { background: var(--green); color: var(--on-accent); }
    .spine-progress { color: var(--green); font-weight: 750; }

    /* ---------- Footer ---------- */
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 0.84rem;
    }
    .footer p { margin: 0 0 7px; }
    .footer a { font-weight: 650; }
"""


def stylesheet():
    """The stylesheet, with both light paths rendered from LIGHT_TOKENS."""
    return (
        STYLESHEET
        .replace(
            "__MEDIA_LIGHT__",
            "    @media (prefers-color-scheme: light) {\n"
            + _light_block(':root:not([data-theme="dark"])', "        ")
            + "\n    }",
        )
        .replace("__TOGGLE_LIGHT__", _light_block('[data-theme="light"]', "      "))
    ) + feedback.CSS
