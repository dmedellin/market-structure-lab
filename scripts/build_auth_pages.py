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

def page(*, title, description, canonical_path, up, body, script):
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
                    canonical_path=canonical_path, favicon=chrome.FAVICON_PATH),
        chrome.topbar(home_href=up, home_label="Back to the Learn library",
                      mark="&#10003;", strong="Learn", sub="geterdone.io",
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

PROGRESS_BODY = """    <h1>Your progress</h1>
    <p class="lead">Completion marks are yours: you tick a lesson when you have done it. Nothing checks
    them and nothing is graded.</p>

    <div class="card">
      <div class="row" style="justify-content:space-between;">
        <div>
          <strong id="who">Not signed in</strong>
          <p class="muted" style="margin:4px 0 0;" id="whoNote">Marks are saved in this browser only.</p>
        </div>
        <div class="row">
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
      <p class="row">
        <button class="btn" id="sync" type="button">Sync now</button>
        <span class="muted" id="syncNote"></span>
      </p>
    </div>

    <div class="status" id="status" hidden></div>

    <h2>Marked complete</h2>
    <div id="list"><p class="muted">Nothing marked yet. Open a lesson and use the button at the foot of the page.</p></div>

    <div class="card">
      <h2 style="margin-top:0;">What signing in does not do</h2>
      <p>It does not unlock anything. Every lesson, every lab and every word of the material is readable
      without an account, and always will be. Signing in only moves your own ticks between your own devices.</p>
      <p class="muted">Clearing your browser data clears local marks. If you have synced, they are still in your OneDrive.</p>
      <p class="row"><a class="btn" href="../">Back to the library</a></p>
    </div>
"""

PROGRESS_PAGE_JS = """
  (function () {
    var KEY = 'learn-progress';
    function read() { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
    function write(m) { try { localStorage.setItem(KEY, JSON.stringify(m)); } catch (e) {} }
    var statusEl = document.getElementById('status');
    function say(text, kind) {
      statusEl.hidden = false;
      statusEl.textContent = text;
      statusEl.className = 'status' + (kind ? ' ' + kind : '');
    }
    function pretty(id) {
      var bits = id.split('/');
      var title = function (s) { return s.replace(/-/g, ' ').replace(/^./, function (c) { return c.toUpperCase(); }); };
      return bits.length === 2 ? [title(bits[0]), title(bits[1])] : [id, ''];
    }
    function paint() {
      var marks = read();
      var ids = Object.keys(marks).sort();
      var list = document.getElementById('list');
      if (!ids.length) {
        list.innerHTML = '<p class="muted">Nothing marked yet. Open a lesson and use the button at the foot of the page.</p>';
        return;
      }
      var rows = ids.map(function (id) {
        var p = pretty(id);
        return '<tr><td class="tick">&#10003;</td><td>' + p[1] + '</td><td class="muted">' + p[0] +
               '</td><td class="muted">' + marks[id] + '</td></tr>';
      }).join('');
      list.innerHTML = '<p class="muted">' + ids.length + ' lesson' + (ids.length === 1 ? '' : 's') +
        ' marked complete.</p><table><thead><tr><th></th><th>Lesson</th><th>Course</th><th>Marked</th></tr></thead><tbody>' +
        rows + '</tbody></table>';
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
    pages = [
        ("oauth2/spa/callback/index.html", "/oauth2/spa/callback/", "../../../",
         "Signing in | Learn \u00b7 geterdone.io",
         "Receives the Microsoft sign-in redirect. Holds no course material.",
         CALLBACK_BODY, auth + CALLBACK_JS),
        ("progress/index.html", "/progress/", "../",
         "Your progress | Learn \u00b7 geterdone.io",
         "Your completion marks, kept in this browser. Sign in with Microsoft to "
         "carry them to another device. Nothing here is graded and no material is locked.",
         PROGRESS_BODY, auth + SYNC_JS + PROGRESS_PAGE_JS),
    ]
    for relative, canonical, up, title, description, body, script in pages:
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(title=title, description=description,
                               canonical_path=canonical, up=up, body=body, script=script),
                          encoding="utf-8")
        print("wrote site/%s (%d bytes)" % (relative, target.stat().st_size))


if __name__ == "__main__":
    main()
