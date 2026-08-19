#!/usr/bin/env python3
"""Render the two pages that may talk to Microsoft.

EVERY OTHER PAGE ON THIS SITE MAKES ZERO NETWORK REQUESTS. That invariant is
why the material works offline and carries no third party. Signing in cannot
honour it -- OAuth is a conversation with an identity provider -- so the
conversation is confined to exactly two pages, declared by name, and the other
367 are untouched:

    /oauth2/spa/callback/   receives the authorization code and exchanges it
    /progress/              signs in, shows your marks, syncs them

WHAT SIGNING IN DOES AND DOES NOT DO. It does not gate one word of the course
material. Completion marks work signed out, in localStorage, on every lesson.
Signing in only lets the same marks follow you to another device. Nothing is
audited: the marks are a note you make to yourself.

WHERE PROGRESS IS STORED. In YOUR OneDrive, in this application's own folder
(Files.ReadWrite.AppFolder), as one small JSON file. Not on any server of mine.
This app is registered `persistence: stateless` and stays that way; adding a
database to hold other people's reading habits would be a different application
with different obligations.

NO CLIENT SECRET. Authorization code + PKCE is a public-client flow; the secret
exists to authenticate a confidential client and there isn't one. Nothing here
is a credential: the client ID and tenant are public identifiers by design.
"""

import pathlib
import sys

CLIENT_ID = "5eb7789c-2954-4d7d-bf0a-39f9ae5cc90f"
# "All Microsoft account users" -> the common authority, so personal accounts work.
AUTHORITY = "https://login.microsoftonline.com/common"
GRAPH = "https://graph.microsoft.com/v1.0"
ORIGIN = "https://learn.geterdone.io"
REDIRECT = ORIGIN + "/oauth2/spa/callback/"
SCOPES = "openid profile offline_access Files.ReadWrite.AppFolder"

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mathpath import feedback as _feedback  # noqa: E402

# The same store the 336 lesson pages write to. /progress/ only reads and ticks;
# recommendations are always WRITTEN on the lesson they are about.
FEEDBACK_STORE_JS = _feedback.STORE_JS

# The library's own brand glyph, the same one the site index draws. It is
# markup, so it reaches topbar() as markup; the previous "&#10003;" was escaped
# on the way through and shipped as the literal text &#10003;.
BRAND_MARK = (
    '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="6" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
    'focusable="false"><path d="M14 45L26 33L38 41L51 18" /></svg>'
)


def library_inventory():
    """Every lesson a reader can actually TICK, as compact JSON.

    The progress page cannot fetch this -- it is a page on a site that makes no
    network requests, and its two allowed origins are Microsoft's, not mine --
    so the inventory is embedded at build time from the same data the pages are
    generated from. There is therefore no second copy to drift: a lesson exists
    here only because build_paths.py built a page for it.

    The trading path is included now that its 118 lessons carry the same
    toggle (see add_progress_marks.py). It is read from the PUBLISHED pages
    rather than from a table here, because those pages are hand-written and
    have no generator -- the path page lists the courses in order and each
    course home lists its lessons, so a trading lesson is in this inventory
    precisely because a course home links to it. That is the same "no second
    copy" rule the generated paths get for free.

    Order matches the site index: Trading, then the two mathematics paths.
    """
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import build_paths
    import add_progress_marks

    trading = {
        "slug": "trading",
        "title": "Trading",
        "courses": [
            {
                "slug": course["slug"],
                "title": course["title"],
                "n": number,
                "lessons": [[l["slug"], l["title"]] for l in course["lessons"]],
            }
            for number, course in enumerate(add_progress_marks.trading_inventory(), start=1)
        ],
    }
    return [trading] + [
        {
            "slug": path["slug"],
            "title": path["title"],
            "courses": [
                {
                    "slug": course["slug"],
                    "title": course["title"],
                    "n": course["number"],
                    "lessons": [[l["slug"], l["title"]] for l in course["lessons"]],
                }
                for course in path["courses"]
            ],
        }
        for path in build_paths.GENERATED_PATHS
    ]


def page(*, title, description, canonical_path, up, body, script, extra_css=""):
    """One auth page, in the library's own chrome.

    Deliberately NOT a bespoke shell. These two pages are exempt from
    self-containment because OAuth is a conversation with an identity provider,
    and that is the ONLY invariant they are excused from. Palette, both light
    paths, the shared theme key, the theme toggle and the canonical tag are the
    library's and are satisfied here exactly as on a lesson page -- a page that
    looks foreign is a page a reader is right to distrust with a sign-in.
    """
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from mathpath import chrome
    return "".join([
        chrome.head(title=title, description=description,
                    canonical_path=canonical_path, favicon=chrome.FAVICON_PATH,
                    extra_css=extra_css),
        chrome.topbar(home_href=up, home_label="Back to the Learn library",
                      mark=BRAND_MARK, strong="Learn", sub="geterdone.io",
                      nav=[("Library", up, False)],
                      signin_href=up + "progress/",
                      signin_current=(canonical_path == "/progress/")),
        chrome.crumbs([("Learn library", up), (title.split(" |")[0], None)]),
        '\n    <main id="main">\n',
        body,
        "    </main>\n",
        chrome.footer(
            "<strong>Your progress.</strong> Completion marks are yours and are not "
            "audited: nothing checks them and nothing is graded. They are kept in "
            "this browser, and signing in only lets them follow you to another "
            "device &mdash; it unlocks no material, because none of it is locked.",
            "every figure is computed in your browser from the stated definition, "
            "and a step that gives the right answer here is not thereby a valid rule."),
        chrome.close(script),
    ])


# --- PKCE, hand-rolled -------------------------------------------------------
# Deliberately not a library from a CDN. A CDN script would be a third-party
# origin with write access to the token, on the two pages that handle tokens,
# and the CSP below would have to allow it. PKCE is a verifier, a SHA-256 and a
# base64url encode; SubtleCrypto does the only hard part.
AUTH_JS = """
  var CLIENT_ID = %(client_id)s;
  var AUTHORITY = %(authority)s;
  var REDIRECT  = %(redirect)s;
  var SCOPES    = %(scopes)s;
  var GRAPH     = %(graph)s;

  function b64url(bytes) {
    var s = btoa(String.fromCharCode.apply(null, new Uint8Array(bytes)));
    return s.replace(/\\+/g, '-').replace(/\\//g, '_').replace(/=+$/, '');
  }
  function randomVerifier() {
    var a = new Uint8Array(32);
    crypto.getRandomValues(a);
    return b64url(a);
  }
  function challenge(verifier) {
    return crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier)).then(b64url);
  }
  /* Tokens live in sessionStorage, not localStorage: they die with the tab.
     Progress marks live in localStorage and are not secret. */
  var Session = {
    get: function () {
      try { return JSON.parse(sessionStorage.getItem('learn-auth') || 'null'); }
      catch (e) { return null; }
    },
    set: function (v) { sessionStorage.setItem('learn-auth', JSON.stringify(v)); },
    clear: function () { sessionStorage.removeItem('learn-auth'); }
  };
  function signIn() {
    var verifier = randomVerifier();
    var state = randomVerifier();
    sessionStorage.setItem('learn-pkce', verifier);
    sessionStorage.setItem('learn-state', state);
    return challenge(verifier).then(function (ch) {
      var q = new URLSearchParams({
        client_id: CLIENT_ID, response_type: 'code', redirect_uri: REDIRECT,
        response_mode: 'query', scope: SCOPES, state: state,
        code_challenge: ch, code_challenge_method: 'S256'
      });
      location.assign(AUTHORITY + '/oauth2/v2.0/authorize?' + q.toString());
    });
  }
  function exchange(code, verifier) {
    return fetch(AUTHORITY + '/oauth2/v2.0/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: CLIENT_ID, grant_type: 'authorization_code', code: code,
        redirect_uri: REDIRECT, code_verifier: verifier, scope: SCOPES
      })
    }).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) throw new Error(j.error_description || j.error || ('token endpoint returned ' + r.status));
        return j;
      });
    });
  }
"""

# --- the progress store, in the reader's own OneDrive ------------------------
SYNC_JS = """
  var FILE = '/drive/special/approot:/learn-progress.json';
  function graph(path, options) {
    var s = Session.get();
    if (!s || !s.access_token) return Promise.reject(new Error('not signed in'));
    options = options || {};
    options.headers = Object.assign({ Authorization: 'Bearer ' + s.access_token }, options.headers || {});
    return fetch(GRAPH + path, options).then(function (r) {
      if (r.status === 404) return null;
      if (!r.ok) return r.text().then(function (t) { throw new Error('Graph ' + r.status + ': ' + t.slice(0, 200)); });
      return r.status === 204 ? null : r.json();
    });
  }
  function pull() { return graph(FILE + ':/content', {}); }
  function push(map) {
    return graph(FILE + ':/content', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(map, null, 1)
    });
  }
  /* Merge, never overwrite. Two devices that ticked different lessons should
     end with both ticks; the earliest date wins for a lesson both marked, so a
     sync can only ever move a completion date backwards to when it really
     happened. Nothing is ever deleted by a sync -- unticking is a local act. */
  function merge(a, b) {
    var out = {}, k;
    for (k in a) if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k];
    for (k in b) if (Object.prototype.hasOwnProperty.call(b, k)) {
      out[k] = (out[k] && out[k] < b[k]) ? out[k] : b[k];
    }
    return out;
  }
"""

CALLBACK_BODY = """    <h1>Signing you in</h1>
    <p class="lead" id="msg">Exchanging the authorization code&hellip;</p>
    <div class="card">
      <p class="muted">This page exists only to receive the redirect from Microsoft. It holds no course
      material. If it stays on this message, the sign-in did not complete and nothing was stored.</p>
      <p class="row"><a class="btn" href="../../../progress/">Back to progress</a><a class="btn" href="../../../">The library</a></p>
    </div>
"""

CALLBACK_JS = """
  (function () {
    var msg = document.getElementById('msg');
    function fail(text) { msg.textContent = text; msg.className = 'lead'; }
    var q = new URLSearchParams(location.search);
    if (q.get('error')) {
      return fail('Microsoft returned an error: ' + (q.get('error_description') || q.get('error')));
    }
    var code = q.get('code');
    var state = q.get('state');
    var expected = sessionStorage.getItem('learn-state');
    var verifier = sessionStorage.getItem('learn-pkce');
    if (!code) return fail('No authorization code in the redirect. Start again from the progress page.');
    /* The state check is what stops a code from another session being planted here. */
    if (!expected || state !== expected) return fail('State mismatch. Sign-in was not completed.');
    if (!verifier) return fail('The PKCE verifier is missing from this tab. Start again in the tab you began in.');
    sessionStorage.removeItem('learn-state');
    sessionStorage.removeItem('learn-pkce');
    exchange(code, verifier).then(function (token) {
      Session.set(token);
      history.replaceState({}, '', '/oauth2/spa/callback/');
      location.replace('/progress/');
    }).catch(function (e) { fail('Could not complete sign-in: ' + e.message); });
  })();
"""

# Page-scoped. These styles belong to ONE page, so they are not added to the
# shared stylesheet that every one of the other 240 pages inlines.
PROGRESS_CSS = """
    /* .hero-visual svg is width:100%, and (0,1,1) outranks a bare .pg-ring, so
       the ring has to be named through its parent or it stretches to the full
       width of the hero panel. */
    .hero-visual .pg-ring { width: min(210px, 100%); height: auto; margin: 0 auto; display: block; }
    .pg-ring circle { fill: none; stroke-width: 12; }
    /* NOT --panel-2: .hero-visual is already --panel-2, so a track in that
       colour is invisible and the arc reads as a stray floating pill. */
    .pg-ring .pg-ring-track { stroke: var(--line-strong); }
    .pg-ring .pg-ring-fill {
      stroke: var(--cyan);
      stroke-linecap: round;
      transform: rotate(-90deg);
      transform-origin: 50% 50%;
      transition: stroke-dashoffset 600ms ease;
    }
    .pg-ring-pct { font-size: 30px; font-weight: 800; fill: var(--text); }
    .pg-ring-sub { font-size: 11px; font-weight: 700; fill: var(--muted); letter-spacing: 0.08em; }

    .pg-bar { height: 7px; border-radius: 999px; background: var(--panel-2); overflow: hidden; }
    .pg-bar-fill { height: 100%; border-radius: 999px; background: var(--cyan); transition: width 500ms ease; }
    .pg-bar-fill.is-done { background: var(--green); }

    #main .card { padding: 18px; }
    #main > .card { margin-top: 14px; }
    .pg-path { margin-top: 14px; }
    .pg-path-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .pg-path-head h3 { margin: 0; font-size: 1.12rem; letter-spacing: -0.01em; }
    .pg-count { color: var(--muted); font-size: 0.84rem; font-weight: 700; white-space: nowrap; }

    .pg-courses { list-style: none; margin: 14px 0 0; padding: 0; display: flex; flex-direction: column; gap: 9px; }
    .pg-course {
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr) auto;
      gap: 13px;
      align-items: center;
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel-2);
      text-decoration: none;
      color: inherit;
    }
    .pg-course:hover { border-color: var(--line-strong); }
    .pg-num {
      display: grid;
      place-items: center;
      width: 34px;
      height: 34px;
      border-radius: 9px;
      background: var(--panel);
      border: 1px solid var(--line);
      font-size: 0.8rem;
      font-weight: 800;
      font-variant-numeric: tabular-nums;
    }
    .pg-course.is-done .pg-num { background: var(--green); color: var(--on-accent); border-color: transparent; }
    .pg-course-name { font-weight: 700; font-size: 0.94rem; margin-bottom: 6px; }

    .pg-recent { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
    .pg-recent li {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      gap: 11px;
      align-items: baseline;
      padding: 10px 13px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
    }
    .pg-recent .pg-tick { color: var(--green); font-weight: 800; }
    .pg-recent a { color: inherit; font-weight: 700; text-decoration: none; }
    .pg-recent a:hover { text-decoration: underline; }
    .pg-when { color: var(--muted); font-size: 0.8rem; font-variant-numeric: tabular-nums; white-space: nowrap; }
    .pg-where { display: block; color: var(--muted); font-size: 0.78rem; font-weight: 600; }

    .pg-account { display: flex; align-items: center; justify-content: space-between; gap: 15px; flex-wrap: wrap; }
"""

PROGRESS_BODY = """    <noscript>
      <div class="noscript-note">
        <strong>JavaScript is off, so none of the figures below can be filled in.</strong>
        Your completion marks are kept in this browser's own storage, and reading
        them needs a script &mdash; so the meters read zero here rather than
        reading your marks. Nothing has been lost: turn JavaScript on and the
        numbers come back. The course material itself needs none of this.
      </div>
    </noscript>

    <section class="hero">
      <div>
        <span class="eyebrow"><span class="pulse" aria-hidden="true"></span>Your progress</span>
        <h1>What you have <span class="gradient-text">finished so far.</span></h1>
        <p class="lead">A completion mark is a note you make to yourself: you tick a lesson when you
        have done it. Nothing checks them, nothing is graded, and no material is locked behind them.</p>
        <div class="hero-actions">
          <a class="btn primary" href="../">Back to the library</a>
          <a class="btn ghost" href="#account">Carry marks to another device</a>
        </div>
      </div>
      <div class="hero-visual">
        <svg class="pg-ring" id="ring" viewBox="0 0 120 120" role="img"
             aria-label="Overall completion: nothing marked yet.">
          <circle class="pg-ring-track" cx="60" cy="60" r="52" />
          <circle class="pg-ring-fill" id="ringFill" cx="60" cy="60" r="52"
                  stroke-dasharray="326.7" stroke-dashoffset="326.7" />
          <text class="pg-ring-pct" x="60" y="58" text-anchor="middle" id="ringPct">0%</text>
          <text class="pg-ring-sub" x="60" y="76" text-anchor="middle" id="ringSub">COMPLETE</text>
        </svg>
      </div>
    </section>

    <dl class="stats" id="stats">
      <div><dt>Lessons ticked</dt><dd><span id="statLessons">0</span><small id="statLessonsOf">&nbsp;</small></dd></div>
      <div><dt>Courses finished</dt><dd><span id="statCourses">0</span><small id="statCoursesOf">&nbsp;</small></dd></div>
      <div><dt>Subjects started</dt><dd><span id="statPaths">0</span><small id="statPathsOf">&nbsp;</small></dd></div>
      <div><dt>Last marked</dt><dd><span id="statLast">&#8212;</span><small id="statLastNote">&nbsp;</small></dd></div>
    </dl>

    <div class="status" id="status" hidden></div>

    <h2>By subject</h2>
    <div id="paths"></div>

    <h2>Recently marked</h2>
    <div id="recent"></div>

    <h2>Recommendations</h2>
    <p class="muted" style="margin-top:0;">Notes you left at the foot of a lesson about what should
    change there. Tick one off here or on the lesson itself &mdash; it is the same list. Export
    gives you a checklist you can paste somewhere and work through.</p>
    <div class="fb-actions" style="margin-bottom:14px;">
      <button class="btn primary" type="button" id="fbExportAll">Export all as Markdown</button>
      <button class="btn" type="button" id="fbExportJson">Export as JSON</button>
      <span class="fb-count" id="fbTotals"></span>
    </div>
    <div id="feedback"></div>

    <div class="card" id="account">
      <div class="pg-account">
        <div>
          <strong id="who">Not signed in</strong>
          <p class="muted" style="margin:4px 0 0;" id="whoNote">Marks are saved in this browser only.</p>
        </div>
        <div class="btn-row">
          <button class="btn primary" id="signin" type="button">Sign in with Microsoft</button>
          <button class="btn" id="signout" type="button" hidden>Sign out</button>
        </div>
      </div>
    </div>

    <div class="card" id="syncCard" hidden>
      <h2 style="margin-top:0;">Carry your marks between devices</h2>
      <p>Your marks are written to <strong>your own OneDrive</strong>, in this application's private folder,
      as one small JSON file. They are not stored on this server. Syncing merges both sides, so a lesson
      ticked on either device stays ticked.</p>
      <p class="btn-row">
        <button class="btn" id="sync" type="button">Sync now</button>
        <span class="muted" id="syncNote"></span>
      </p>
    </div>

    <div class="card">
      <h2 style="margin-top:0;">What signing in does not do</h2>
      <p>It does not unlock anything. Every lesson, every lab and every word of the material is readable
      without an account, and always will be. Signing in only moves your own ticks between your own devices.</p>
      <p class="muted">Clearing your browser data clears local marks. If you have synced, they are still in your OneDrive.</p>
    </div>
"""

PROGRESS_PAGE_JS = """
  (function () {
    var KEY = 'learn-progress';
    /* The whole tickable library, embedded at build time from the same data the
       lesson pages were generated from. It is what makes "12 of 218" a fact
       rather than a guess: without it this page could only count the marks it
       happens to hold and had no idea what the denominator was. */
    var LIBRARY = %(library)s;

    var TOTAL_LESSONS = 0, TOTAL_COURSES = 0;
    var LESSON_INDEX = {};   /* "course/lesson" -> {course, lesson, path} */
    LIBRARY.forEach(function (path) {
      TOTAL_COURSES += path.courses.length;
      path.courses.forEach(function (course) {
        TOTAL_LESSONS += course.lessons.length;
        course.lessons.forEach(function (pair) {
          LESSON_INDEX[course.slug + '/' + pair[0]] =
            { course: course, lesson: { slug: pair[0], title: pair[1] }, path: path };
        });
      });
    });

    function read() { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
    function write(m) { try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {} }

    var statusEl = document.getElementById('status');
    function say(text, kind) {
      statusEl.hidden = false;
      statusEl.textContent = text;
      statusEl.className = 'status' + (kind ? ' ' + kind : '');
    }
    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function pct(done, total) { return total ? Math.round((done / total) * 100) : 0; }
    function bar(done, total) {
      return '<div class="pg-bar" aria-hidden="true"><div class="pg-bar-fill' +
             (done === total && total ? ' is-done' : '') +
             '" style="width:' + pct(done, total) + '%%;"></div></div>';
    }

    /* One pass over the marks, producing every number the page shows. Each
       count comes from the SAME tally, so the ring, the stats, the per-subject
       meters and the list cannot disagree with each other. */
    function tally(marks) {
      var t = { done: 0, total: TOTAL_LESSONS, courses: 0, paths: 0, known: [], unknown: [] };
      Object.keys(marks).forEach(function (id) {
        (LESSON_INDEX[id] ? t.known : t.unknown).push(id);
      });
      t.done = t.known.length;
      t.byPath = LIBRARY.map(function (path) {
        var row = { path: path, done: 0, total: 0, courses: [] };
        path.courses.forEach(function (course) {
          var done = 0;
          course.lessons.forEach(function (pair) {
            if (marks[course.slug + '/' + pair[0]]) done++;
          });
          row.courses.push({ course: course, done: done, total: course.lessons.length });
          row.done += done;
          row.total += course.lessons.length;
          if (done === course.lessons.length && course.lessons.length) t.courses++;
        });
        if (row.done > 0) t.paths++;
        return row;
      });
      return t;
    }

    function paintRing(t) {
      var CIRC = 2 * Math.PI * 52;
      var p = pct(t.done, t.total);
      var fill = document.getElementById('ringFill');
      fill.setAttribute('stroke-dasharray', CIRC.toFixed(1));
      fill.setAttribute('stroke-dashoffset', (CIRC * (1 - p / 100)).toFixed(1));
      document.getElementById('ringPct').textContent = p + '%%';
      document.getElementById('ringSub').textContent = t.done + ' OF ' + t.total;
      document.getElementById('ring').setAttribute('aria-label',
        t.done + ' of ' + t.total + ' lessons complete (' + p + '%%)');
    }

    function paintStats(t) {
      document.getElementById('statLessons').textContent = t.done;
      document.getElementById('statLessonsOf').textContent = 'of ' + t.total + ' tickable';
      document.getElementById('statCourses').textContent = t.courses;
      document.getElementById('statCoursesOf').textContent = 'of ' + TOTAL_COURSES;
      document.getElementById('statPaths').textContent = t.paths;
      document.getElementById('statPathsOf').textContent = 'of ' + LIBRARY.length;
      var latest = null;
      Object.keys(read()).forEach(function (id) {
        var d = read()[id];
        if (typeof d === 'string' && (latest === null || d > latest)) latest = d;
      });
      document.getElementById('statLast').textContent = latest || '\u2014';
      document.getElementById('statLastNote').textContent = latest ? '' : 'nothing yet';
    }

    function paintPaths(t) {
      document.getElementById('paths').innerHTML = t.byPath.map(function (row) {
        var courses = row.courses.map(function (c) {
          var done = c.done === c.total && c.total;
          return '<a class="pg-course' + (done ? ' is-done' : '') + '" href="../' + esc(c.course.slug) + '/">' +
                 '<span class="pg-num">' + (done ? '&#10003;' : c.course.n) + '</span>' +
                 '<span><span class="pg-course-name">' + esc(c.course.title) + '</span>' + bar(c.done, c.total) + '</span>' +
                 '<span class="pg-count">' + c.done + ' / ' + c.total + '</span></a>';
        }).join('');
        return '<section class="card pg-path"><div class="pg-path-head">' +
               '<h3>' + esc(row.path.title) + '</h3>' +
               '<span class="pg-count">' + row.done + ' of ' + row.total + ' lessons &middot; ' +
               pct(row.done, row.total) + '%%</span></div>' +
               bar(row.done, row.total) +
               '<ul class="pg-courses">' + courses + '</ul></section>';
      }).join('');
    }

    function paintRecent(t, marks) {
      var el = document.getElementById('recent');
      if (!t.known.length && !t.unknown.length) {
        el.innerHTML = '<p class="muted">Nothing marked yet. Open a lesson and use the button at the ' +
          'foot of the page &mdash; it is the same tick that fills the meters above.</p>';
        return;
      }
      var rows = t.known.slice().sort(function (a, b) {
        var da = marks[a] || '', db = marks[b] || '';
        return da === db ? a.localeCompare(b) : (da < db ? 1 : -1);
      }).map(function (id) {
        var e = LESSON_INDEX[id];
        return '<li><span class="pg-tick" aria-hidden="true">&#10003;</span>' +
               '<span><a href="../' + esc(e.course.slug) + '/' + esc(e.lesson.slug) + '/">' +
               esc(e.lesson.title) + '</a>' +
               '<span class="pg-where">' + esc(e.course.title) + ' &middot; ' + esc(e.path.title) + '</span></span>' +
               '<span class="pg-when">' + esc(marks[id]) + '</span></li>';
      }).join('');
      var extra = '';
      /* A mark whose lesson is no longer in the library is still the reader's.
         Counting it in the totals would be wrong, and dropping it silently
         would be worse -- so it is shown, and shown as what it is. */
      if (t.unknown.length) {
        var one = t.unknown.length === 1;
        extra = '<p class="muted" style="margin-top:14px;">' + t.unknown.length +
          (one ? ' mark refers to a lesson that is no longer in the library, so it is not counted above: '
               : ' marks refer to lessons that are no longer in the library, so they are not counted above: ') +
          t.unknown.map(esc).join(', ') + '.</p>';
      }
      el.innerHTML = (rows ? '<ul class="pg-recent">' + rows + '</ul>' : '') + extra;
    }

    /* Every recommendation in the library, grouped by the lesson it is about.
       LESSON_INDEX supplies the titles, so a note reads as "Logic and Proof -
       Truth Tables" rather than as a slug. A note whose lesson has left the
       library still appears, under its raw id, for the same reason a stale
       completion mark does: it is the reader's and dropping it silently would
       be worse than showing it plainly. */
    function feedbackEntries() {
      var store = window.learnFeedback ? window.learnFeedback.read() : {};
      return Object.keys(store).sort().map(function (id) {
        var known = LESSON_INDEX[id];
        return {
          id: id,
          title: known ? known.lesson.title : id,
          where: known ? known.course.title + ' \u00b7 ' + known.path.title : 'no longer in the library',
          url: '../' + id + '/',
          known: !!known,
          items: store[id] || []
        };
      }).filter(function (entry) { return entry.items.length; });
    }

    function paintFeedback() {
      var host = document.getElementById('feedback');
      if (!host || !window.learnFeedback) return;
      var entries = feedbackEntries();
      var open = 0, total = 0;
      entries.forEach(function (e) {
        total += e.items.length;
        open += e.items.filter(function (i) { return !i.done; }).length;
      });
      document.getElementById('fbTotals').textContent = total
        ? open + ' open \u00b7 ' + (total - open) + ' done \u00b7 ' + entries.length +
          ' lesson' + (entries.length === 1 ? '' : 's')
        : '';
      if (!entries.length) {
        host.innerHTML = '<p class="muted">Nothing recorded yet. Open any lesson and use the ' +
          'feedback panel at the foot of the page.</p>';
        return;
      }
      host.innerHTML = entries.map(function (e) {
        var rows = e.items.map(function (item) {
          var when = item.done && item.closed
            ? 'Added ' + item.created + ' \u00b7 done ' + item.closed
            : 'Added ' + item.created;
          return '<li class="fb-item' + (item.done ? ' is-done' : '') + '">' +
            '<button class="fb-tick" type="button" data-lesson="' + esc(e.id) + '"' +
            ' data-id="' + esc(item.id) + '" aria-pressed="' + (item.done ? 'true' : 'false') +
            '" title="Mark this recommendation done"><span aria-hidden="true">&#10003;</span>' +
            '<span class="fb-sr">Mark done</span></button>' +
            '<span><p class="fb-body">' + esc(item.text) + '</p>' +
            '<span class="fb-when">' + when + '</span></span></li>';
        }).join('');
        return '<section class="card pg-path"><div class="pg-path-head">' +
          '<h3>' + (e.known ? '<a href="' + esc(e.url) + '">' + esc(e.title) + '</a>' : esc(e.title)) +
          '</h3><span class="pg-count">' + esc(e.where) + '</span></div>' +
          '<ul class="fb-list">' + rows + '</ul></section>';
      }).join('');
    }

    function paint() {
      var marks = read();
      var t = tally(marks);
      paintRing(t);
      paintStats(t);
      paintPaths(t);
      paintRecent(t, marks);
      paintFeedback();
    }

    function paintAuth() {
      var s = Session.get();
      var signedIn = !!(s && s.access_token);
      document.getElementById('signin').hidden = signedIn;
      document.getElementById('signout').hidden = !signedIn;
      document.getElementById('syncCard').hidden = !signedIn;
      document.getElementById('who').textContent = signedIn ? 'Signed in' : 'Not signed in';
      document.getElementById('whoNote').textContent = signedIn
        ? 'Your marks can be carried to another device.'
        : 'Marks are saved in this browser only.';
      if (!signedIn) return;
      /* The ID token names the account. It is read for display only; nothing
         here trusts it for authorisation, because there is nothing to authorise. */
      try {
        if (s.id_token) {
          var claims = JSON.parse(atob(s.id_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
          var name = claims.name || claims.preferred_username;
          if (name) document.getElementById('who').textContent = 'Signed in as ' + name;
        }
      } catch (e) { /* display only */ }
    }
    document.getElementById('signin').addEventListener('click', function () {
      signIn().catch(function (e) { say('Could not start sign-in: ' + e.message, 'bad'); });
    });
    document.getElementById('signout').addEventListener('click', function () {
      Session.clear(); paintAuth(); say('Signed out. Your local marks are untouched.', 'good');
    });
    document.getElementById('sync').addEventListener('click', function () {
      var local = read();
      say('Syncing\\u2026');
      pull().then(function (remote) {
        var merged = merge(local, remote || {});
        write(merged);
        return push(merged).then(function () {
          paint();
          var added = Object.keys(merged).length - Object.keys(local).length;
          say('Synced. ' + Object.keys(merged).length + ' lesson(s) marked' +
              (added > 0 ? ', ' + added + ' brought in from another device' : '') + '.', 'good');
        });
      }).catch(function (e) { say('Sync failed: ' + e.message, 'bad'); });
    });
    /* Ticking here and ticking on the lesson are the same operation on the
       same store, so the two views cannot disagree. */
    var feedbackHost = document.getElementById('feedback');
    if (feedbackHost) {
      feedbackHost.addEventListener('click', function (event) {
        var button = event.target.closest ? event.target.closest('.fb-tick') : null;
        if (!button || !window.learnFeedback) return;
        window.learnFeedback.toggle(button.getAttribute('data-lesson'), button.getAttribute('data-id'));
        paintFeedback();
      });
    }
    var exportAll = document.getElementById('fbExportAll');
    if (exportAll) {
      exportAll.addEventListener('click', function () {
        var entries = feedbackEntries();
        if (!entries.length) { say('Nothing to export yet.', ''); return; }
        var body = window.learnFeedback.markdown(entries, 'Learn \u2014 recommendations');
        window.learnFeedback.download('learn-recommendations-' + window.learnFeedback.today() + '.md', body);
      });
    }
    var exportJson = document.getElementById('fbExportJson');
    if (exportJson) {
      exportJson.addEventListener('click', function () {
        /* Markdown is lossy -- it drops ids and flattens newlines -- so the raw
           store is offered too, for anyone who wants to keep or move it. */
        var raw = JSON.stringify(window.learnFeedback.read(), null, 2);
        window.learnFeedback.download(
          'learn-recommendations-' + window.learnFeedback.today() + '.json', raw, 'application/json');
      });
    }

    paintAuth(); paint();
  })();
"""


def main():
    import json
    values = {
        "client_id": json.dumps(CLIENT_ID), "authority": json.dumps(AUTHORITY),
        "redirect": json.dumps(REDIRECT), "scopes": json.dumps(SCOPES),
        "graph": json.dumps(GRAPH),
    }
    auth = AUTH_JS % values
    progress_js = PROGRESS_PAGE_JS % {
        "library": json.dumps(library_inventory(), separators=(",", ":")),
    }
    pages = [
        ("oauth2/spa/callback/index.html", "/oauth2/spa/callback/", "../../../",
         "Signing in | Learn \u00b7 geterdone.io",
         "Receives the Microsoft sign-in redirect. Holds no course material.",
         CALLBACK_BODY, auth + CALLBACK_JS, ""),
        ("progress/index.html", "/progress/", "../",
         "Your progress | Learn \u00b7 geterdone.io",
         "Your completion marks, kept in this browser. Sign in with Microsoft to "
         "carry them to another device. Nothing here is graded and no material is locked.",
         PROGRESS_BODY, auth + SYNC_JS + FEEDBACK_STORE_JS + progress_js, PROGRESS_CSS),
    ]
    for relative, canonical, up, title, description, body, script, extra_css in pages:
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(title=title, description=description,
                               canonical_path=canonical, up=up, body=body, script=script,
                               extra_css=extra_css),
                          encoding="utf-8")
        print("wrote site/%s (%d bytes)" % (relative, target.stat().st_size))


if __name__ == "__main__":
    main()
