"""Per-lesson feedback: recommendations you write, tick off, and export.

WHAT THIS IS FOR. A completion mark says "I have done this". A recommendation
says "this lesson should change" -- a note to act on later, by whoever is
improving the material. The two are deliberately separate keys: deleting your
progress must not delete your notes, and a lesson can carry open
recommendations long after it has been ticked.

STILL ZERO NETWORK REQUESTS. Every page under site/ renders without contacting
anyone, and this changes nothing about that. Recommendations live in
localStorage, and EXPORT is a local file: the text is put in a Blob and handed
to an <a download>. No request leaves the page -- `fetch`, XHR, WebSocket,
EventSource, sendBeacon and importScripts are all still absent, which is what
the self-containment sweeps actually forbid.

WHY MARKDOWN. The export exists to be acted on, so it is a checklist a person
can paste into an issue, a commit message or a document, with `- [ ]` and
`- [x]` carrying the done state that was ticked in the page. JSON is offered
alongside it for round-tripping, because Markdown is lossy.

ONE SOURCE, THREE CONSUMERS. The generated lessons (render.py), the
hand-written trading lessons (add_progress_marks.py) and the aggregate view on
/progress/ (build_auth_pages.py) all take the markup, styles and behaviour from
here. The trading pages carry a frozen copy of an older stylesheet, so the CSS
below is written to be self-sufficient: it uses the palette custom properties
and `.btn`, both of which exist on every page family, and defines everything
else itself rather than assuming `.btn-row` or `.visually-hidden`.
"""

STORAGE_KEY = "learn-feedback"

CSS = """
    .lesson-feedback {
      margin-top: 18px;
      padding: 17px 19px;
      border: 1px solid var(--line);
      border-radius: 13px;
      background: var(--panel);
    }
    .lesson-feedback h2 { margin: 0 0 6px; font-size: 1.06rem; letter-spacing: -0.01em; }
    .fb-lead { margin: 0 0 13px; color: var(--muted); font-size: 0.85rem; }
    .fb-sr {
      position: absolute; width: 1px; height: 1px;
      overflow: hidden; clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap;
    }
    .fb-text {
      display: block;
      width: 100%;
      box-sizing: border-box;
      padding: 11px 13px;
      border: 1px solid var(--line-strong);
      border-radius: 10px;
      background: var(--panel-2);
      color: var(--text);
      font: inherit;
      font-size: 0.9rem;
      resize: vertical;
    }
    .fb-text:focus { outline: 2px solid var(--cyan); outline-offset: 1px; }
    .fb-actions {
      display: flex;
      align-items: center;
      gap: 9px;
      flex-wrap: wrap;
      margin-top: 11px;
    }
    .fb-count { color: var(--muted); font-size: 0.82rem; font-weight: 650; }

    .fb-list { list-style: none; margin: 15px 0 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
    .fb-item {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      gap: 11px;
      align-items: start;
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel-2);
    }
    .fb-item.is-done { border-color: var(--green); }
    .fb-item.is-done .fb-body { color: var(--muted); text-decoration: line-through; }
    .fb-tick {
      display: grid;
      place-items: center;
      width: 24px;
      height: 24px;
      padding: 0;
      border: 1px solid var(--line-strong);
      border-radius: 7px;
      background: var(--panel);
      color: transparent;
      font-size: 0.78rem;
      font-weight: 900;
      cursor: pointer;
    }
    .fb-tick:hover { border-color: var(--cyan); }
    .fb-item.is-done .fb-tick {
      border-color: var(--green);
      background: var(--green);
      color: var(--on-accent);
    }
    .fb-body { margin: 0; font-size: 0.9rem; white-space: pre-wrap; overflow-wrap: anywhere; }
    .fb-when { display: block; margin-top: 4px; color: var(--muted); font-size: 0.76rem; font-weight: 600; }
    .fb-drop {
      border: 1px solid transparent;
      border-radius: 7px;
      background: none;
      color: var(--muted);
      font: inherit;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      padding: 3px 7px;
    }
    .fb-drop:hover { color: var(--red); border-color: var(--line); }
    .fb-empty { margin: 15px 0 0; color: var(--muted); font-size: 0.85rem; }
"""

# The store. Separate from learn-progress on purpose: a reader who clears their
# completion marks has not withdrawn their recommendations, and the two are
# read by different people for different reasons.
STORE_JS = """
  /* Recommendations. localStorage only: no request leaves the page. */
  (function () {
    var KEY = 'learn-feedback';
    function read() {
      try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
      catch (e) { return {}; }
    }
    function write(map) {
      try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (e) { /* private mode */ }
    }
    function today() { return new Date().toISOString().slice(0, 10); }
    var counter = 0;
    function newId() {
      counter += 1;
      return Date.now().toString(36) + '-' + counter.toString(36);
    }
    function list(lesson) {
      var all = read()[lesson];
      return Object.prototype.toString.call(all) === '[object Array]' ? all : [];
    }
    function save(lesson, items) {
      var map = read();
      if (items.length) { map[lesson] = items; } else { delete map[lesson]; }
      write(map);
    }
    function add(lesson, text) {
      text = String(text == null ? '' : text).trim();
      if (!text) return null;
      var items = list(lesson);
      var item = { id: newId(), text: text, done: false, created: today(), closed: null };
      items.push(item);
      save(lesson, items);
      return item;
    }
    function toggle(lesson, id) {
      var items = list(lesson);
      items.forEach(function (item) {
        if (item.id !== id) return;
        item.done = !item.done;
        item.closed = item.done ? today() : null;
      });
      save(lesson, items);
    }
    function remove(lesson, id) {
      save(lesson, list(lesson).filter(function (item) { return item.id !== id; }));
    }

    /* A checklist somebody can act on: the done state ticked in the page is the
       done state in the file. Titles are passed in because this store knows
       lesson IDS, not what they are called. */
    function markdown(entries, heading) {
      var out = ['# ' + heading, ''];
      entries.forEach(function (entry) {
        if (!entry.items.length) return;
        out.push('## ' + entry.title);
        if (entry.url) out.push('');
        if (entry.url) out.push(entry.url);
        out.push('');
        entry.items.forEach(function (item) {
          var when = item.done && item.closed
            ? ' _(added ' + item.created + ', done ' + item.closed + ')_'
            : ' _(added ' + item.created + ')_';
          out.push('- [' + (item.done ? 'x' : ' ') + '] ' +
                   String(item.text).replace(/\\r?\\n/g, ' ') + when);
        });
        out.push('');
      });
      if (out.length === 2) out.push('_No recommendations recorded._');
      return out.join('\\n');
    }

    /* A Blob and an <a download>. This is a LOCAL save, not a request: nothing
       is uploaded and no origin is contacted. */
    function download(filename, text, type) {
      var blob = new Blob([text], { type: (type || 'text/markdown') + ';charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 0);
    }
    function slugify(text) {
      return String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }

    window.learnFeedback = {
      key: KEY, read: read, list: list, add: add, toggle: toggle, remove: remove,
      markdown: markdown, download: download, slugify: slugify, today: today
    };
  })();
"""

# What a LESSON shows: the form, the list, and an export of its own notes.
MARKUP = """
    <section class="lesson-feedback" id="lessonFeedback"
             data-lesson-id="%(id)s" data-lesson-title="%(lesson)s" data-course-title="%(course)s">
      <h2>Feedback and recommendations</h2>
      <p class="fb-lead">Something to change about this lesson? Write it down, tick it off when it
        is handled, and export the list when you want to act on it. Kept in this browser only:
        nothing is sent anywhere, and nobody is notified.</p>
      <form class="fb-form" id="fbForm">
        <label class="fb-sr" for="fbText">Your recommendation for this lesson</label>
        <textarea class="fb-text" id="fbText" rows="3"
                  placeholder="e.g. the warm-up period should be explained before the first worked example"></textarea>
        <div class="fb-actions">
          <button class="btn primary" type="submit">Add recommendation</button>
          <button class="btn" type="button" id="fbExport">Export as Markdown</button>
          <span class="fb-count" id="fbCount"></span>
        </div>
      </form>
      <ul class="fb-list" id="fbList"></ul>
      <p class="fb-empty" id="fbEmpty">No recommendations yet for this lesson.</p>
    </section>
"""

LESSON_JS = """
  (function () {
    var root = document.getElementById('lessonFeedback');
    if (!root || !window.learnFeedback) return;
    var F = window.learnFeedback;
    var id = root.getAttribute('data-lesson-id');
    var lessonTitle = root.getAttribute('data-lesson-title') || id;
    var courseTitle = root.getAttribute('data-course-title') || '';
    var listEl = document.getElementById('fbList');
    var emptyEl = document.getElementById('fbEmpty');
    var countEl = document.getElementById('fbCount');
    var textEl = document.getElementById('fbText');

    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function paint() {
      var items = F.list(id);
      listEl.innerHTML = items.map(function (item) {
        var when = item.done && item.closed
          ? 'Added ' + item.created + ' \\u00b7 done ' + item.closed
          : 'Added ' + item.created;
        return '<li class="fb-item' + (item.done ? ' is-done' : '') + '">' +
          '<button class="fb-tick" type="button" data-act="toggle" data-id="' + esc(item.id) + '"' +
          ' aria-pressed="' + (item.done ? 'true' : 'false') + '"' +
          ' title="Mark this recommendation done"><span aria-hidden="true">&#10003;</span>' +
          '<span class="fb-sr">Mark done</span></button>' +
          '<span><p class="fb-body">' + esc(item.text) + '</p>' +
          '<span class="fb-when">' + when + '</span></span>' +
          '<button class="fb-drop" type="button" data-act="remove" data-id="' + esc(item.id) + '">Remove</button>' +
          '</li>';
      }).join('');
      var open = items.filter(function (i) { return !i.done; }).length;
      emptyEl.hidden = items.length > 0;
      listEl.hidden = items.length === 0;
      countEl.textContent = items.length
        ? open + ' open \\u00b7 ' + (items.length - open) + ' done'
        : '';
    }
    document.getElementById('fbForm').addEventListener('submit', function (event) {
      event.preventDefault();
      if (F.add(id, textEl.value)) { textEl.value = ''; paint(); }
      textEl.focus();
    });
    listEl.addEventListener('click', function (event) {
      var button = event.target.closest ? event.target.closest('[data-act]') : null;
      if (!button) return;
      var act = button.getAttribute('data-act');
      if (act === 'toggle') F.toggle(id, button.getAttribute('data-id'));
      if (act === 'remove') F.remove(id, button.getAttribute('data-id'));
      paint();
    });
    document.getElementById('fbExport').addEventListener('click', function () {
      var heading = 'Feedback \\u2014 ' + (courseTitle ? courseTitle + ' \\u00b7 ' : '') + lessonTitle;
      var body = F.markdown(
        [{ title: lessonTitle, url: '/' + id + '/', items: F.list(id) }], heading);
      F.download('feedback-' + F.slugify(id) + '.md', body);
    });
    paint();
  })();
"""
