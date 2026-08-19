#!/usr/bin/env node
/* Tests the recommendation feature that /progress/ and the lessons actually ship.
 *
 * Three things here are not visible to any other check in this repo. The store
 * is only exercised by clicking; the Markdown export is generated text that no
 * page renders; and the list is the FIRST place on this site where text a
 * person typed is put back into the page, so escaping is now load-bearing.
 *
 * As with progresscheck.js the script under test is extracted from the built
 * page rather than reimplemented, so there is no second copy to drift.
 *
 * Run: node scripts/feedbackcheck.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execFileSync } = require('child_process');

const REPO = path.resolve(__dirname, '..');
/* BOTH builders. The lesson panel is rendered by build_paths.py and the
 * aggregate by build_auth_pages.py, and this file reads a page from each. An
 * earlier version rebuilt only the auth pages, so a deliberate break in the
 * lesson script was not caught: the harness was reading a stale page. */
execFileSync('python3', [path.join(REPO, 'scripts', 'build_paths.py')], { stdio: 'pipe' });
execFileSync('python3', [path.join(REPO, 'scripts', 'build_auth_pages.py')], { stdio: 'pipe' });

function htmlOf(file) { return fs.readFileSync(path.join(REPO, file), 'utf8'); }

function scriptOf(html) {
  const blocks = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g) || [];
  const last = blocks[blocks.length - 1];
  return last.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
}

const LESSON_HTML = htmlOf('site/logic-and-proof/truth-tables/index.html');
const PROGRESS = scriptOf(htmlOf('site/progress/index.html'));
const LESSON = scriptOf(LESSON_HTML);

/* The panel reads its lesson id off its own root element, so the harness has
 * to carry the REAL attributes the page ships -- reading them out of the built
 * markup rather than restating them, or this would test a lesson id I made up. */
const PANEL_ATTRS = (function () {
  const tag = /<section class="lesson-feedback"[\s\S]*?>/.exec(LESSON_HTML)[0];
  const attrs = {};
  const re = /([a-z-]+)="([^"]*)"/g;
  let m;
  while ((m = re.exec(tag))) attrs[m[1]] = m[2];
  return attrs;
})();
if (PANEL_ATTRS['data-lesson-id'] !== 'logic-and-proof/truth-tables') {
  console.error('unexpected panel id: ' + PANEL_ATTRS['data-lesson-id']);
  process.exit(1);
}

/* --- the smallest DOM these scripts need -------------------------------- */
function makeEl(id, attrs) {
  const el = {
    // `value`, `style`, `dataset` and friends exist because the lesson's own
    // lab script shares this page and runs first; the harness has to be a
    // plausible enough DOM for it to get out of the way.
    id, textContent: '', innerHTML: '', hidden: false, className: '',
    value: '', checked: false, disabled: false, style: {}, dataset: {},
    children: [], options: [], files: [],
    attrs: Object.assign({}, attrs || {}),
    handlers: {},
    setAttribute(k, v) { this.attrs[k] = String(v); },
    getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
    classList: { add() {}, remove() {}, toggle() {} },
    addEventListener(kind, fn) { (this.handlers[kind] = this.handlers[kind] || []).push(fn); },
    appendChild() {}, removeChild() {}, focus() {}, click() {},
    fire(kind, event) { (this.handlers[kind] || []).forEach(fn => fn(event || { preventDefault() {} })); },
  };
  return el;
}

function run(source, seed) {
  const els = {};
  const store = Object.assign({}, seed || {});
  const downloads = [];
  const sandbox = {
    document: {
      getElementById: (id) =>
        (els[id] = els[id] || makeEl(id, id === 'lessonFeedback' ? PANEL_ATTRS : null)),
      querySelectorAll: () => [],
      querySelector: () => null,
      createElement: () => {
        const a = makeEl('a');
        a.click = function () { downloads.push({ name: a.download, href: a.href }); };
        return a;
      },
      body: { appendChild() {}, removeChild() {} },
      documentElement: { dataset: {} },
      addEventListener() {},
    },
    localStorage: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = v; },
      removeItem: (k) => { delete store[k]; },
    },
    sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    location: { href: '', search: '', replace() {} },
    history: { replaceState() {} },
    matchMedia: () => ({ matches: false, addEventListener() {}, addListener() {} }),
    crypto: { getRandomValues: (a) => a, subtle: { digest: () => Promise.resolve(new Uint8Array(32)) } },
    TextEncoder, Blob: function (parts, opts) { this.parts = parts; this.opts = opts; },
    URL: { createObjectURL: (b) => 'blob:' + b.parts.join(''), revokeObjectURL() {} },
    btoa: (s) => Buffer.from(s, 'binary').toString('base64'),
    atob: (s) => Buffer.from(s, 'base64').toString('binary'),
    setTimeout, console, Math, JSON, Date,
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { timeout: 5000 });
  return { els, store, downloads, F: sandbox.window.learnFeedback };
}

let failures = 0;
function check(name, got, want) {
  if (String(got) === String(want)) { console.log('ok    ' + name); return; }
  failures++;
  console.log('FAIL  ' + name + '\n      got  ' + got + '\n      want ' + want);
}

/* --- the store ---------------------------------------------------------- */
let r = run(LESSON);
const F = r.F;
check('store: exists on a lesson page', typeof F, 'object');
check('store: a fresh lesson has no recommendations', F.list('a/b').length, 0);

F.add('a/b', '  Explain the warm-up first  ');
check('store: adding one records it', F.list('a/b').length, 1);
check('store: whitespace is trimmed', F.list('a/b')[0].text, 'Explain the warm-up first');
check('store: a new item is open', F.list('a/b')[0].done, 'false');
check('store: blank text is refused', F.add('a/b', '   '), 'null');
check('store: refusing blank did not record anything', F.list('a/b').length, 1);

const first = F.list('a/b')[0].id;
F.add('a/b', 'Second note');
check('store: ids are distinct', F.list('a/b')[1].id === first, false);

F.toggle('a/b', first);
check('store: toggling marks it done', F.list('a/b')[0].done, 'true');
check('store: a done item records when', /^\d{4}-\d\d-\d\d$/.test(F.list('a/b')[0].closed), true);
F.toggle('a/b', first);
check('store: toggling again reopens it', F.list('a/b')[0].done, 'false');
check('store: reopening clears the closed date', F.list('a/b')[0].closed, 'null');

F.remove('a/b', first);
check('store: removing drops just that one', F.list('a/b').length, 1);
check('store: the survivor is the other one', F.list('a/b')[0].text, 'Second note');
F.remove('a/b', F.list('a/b')[0].id);
check('store: emptying a lesson removes its key entirely',
      Object.prototype.hasOwnProperty.call(F.read(), 'a/b'), false);

/* --- separation from progress ------------------------------------------ */
r = run(LESSON, { 'learn-progress': JSON.stringify({ 'x/y': '2026-08-19' }) });
r.F.add('x/y', 'A note');
check('store: recommendations do not live in the progress key',
      JSON.parse(r.store['learn-progress'])['x/y'], '2026-08-19');
check('store: they live in their own key',
      Object.keys(JSON.parse(r.store['learn-feedback']))[0], 'x/y');

/* --- Markdown export ---------------------------------------------------- */
r = run(LESSON);
r.F.add('c/d', 'Open one');
r.F.add('c/d', 'Closed one');
const items = r.F.list('c/d');
r.F.toggle('c/d', items[1].id);
const md = r.F.markdown([{ title: 'A Lesson', url: '/c/d/', items: r.F.list('c/d') }], 'Feedback');
check('export: heading', md.split('\n')[0], '# Feedback');
check('export: an open item is an unchecked box', /- \[ \] Open one/.test(md), true);
check('export: a done item is a checked box', /- \[x\] Closed one/.test(md), true);
check('export: a done item carries both dates', /- \[x\] Closed one _\(added \d{4}-\d\d-\d\d, done \d{4}-\d\d-\d\d\)_/.test(md), true);
check('export: the lesson url is included', md.indexOf('/c/d/') !== -1, true);
r.F.add('c/d', 'line one\nline two');
const md2 = r.F.markdown([{ title: 'A Lesson', url: '/c/d/', items: r.F.list('c/d') }], 'Feedback');
check('export: newlines are flattened so the checklist stays a checklist',
      /- \[ \] line one line two/.test(md2), true);
check('export: nothing recorded says so',
      /_No recommendations recorded._/.test(r.F.markdown([], 'Feedback')), true);

/* --- the download is local, not a request ------------------------------- */
r = run(LESSON);
r.F.add('e/f', 'note');
r.F.download('x.md', 'hello');
check('export: a download happened', r.downloads.length, 1);
check('export: it is a blob url, not a remote one', /^blob:/.test(r.downloads[0].href), true);
check('export: the file is named', r.downloads[0].name, 'x.md');

/* --- escaping: the first user-typed text this site renders --------------- */
r = run(LESSON);
const nasty = '<img src=x onerror=alert(1)>"&';
// Driven the way a person drives it -- type, then submit -- because the page
// only repaints when its own handler accepts the text.
r.els.fbText.value = nasty;
r.els.fbForm.fire('submit');
const painted = r.els.fbList.innerHTML;
check('escaping: the raw tag never reaches the DOM string',
      painted.indexOf('<img src=x') === -1, true);
check('escaping: it is present, escaped', painted.indexOf('&lt;img src=x') !== -1, true);
check('escaping: the quote is escaped too', painted.indexOf('&quot;') !== -1, true);

/* --- the lesson panel counts ------------------------------------------- */
r = run(LESSON);
const LID = 'logic-and-proof/truth-tables';
['one', 'two', 'three'].forEach(function (text) {
  r.els.fbText.value = text;
  r.els.fbForm.fire('submit');
});
check('panel: the textarea is cleared after adding', r.els.fbText.value, '');
check('panel: three recommendations recorded', r.F.list(LID).length, 3);
// Tick the first one through the list's own click handler, as a click would.
const target = r.F.list(LID)[0].id;
r.els.fbList.fire('click', {
  preventDefault() {},
  target: { closest: () => ({ getAttribute: (k) => (k === 'data-act' ? 'toggle' : target) }) },
});
check('panel: counts open and done', r.els.fbCount.textContent, '2 open · 1 done');
check('panel: the empty note is hidden once there is something', r.els.fbEmpty.hidden, true);
// And removing through the same handler.
const victim = r.F.list(LID)[1].id;
r.els.fbList.fire('click', {
  preventDefault() {},
  target: { closest: () => ({ getAttribute: (k) => (k === 'data-act' ? 'remove' : victim) }) },
});
check('panel: removing through the list drops one', r.F.list(LID).length, 2);

/* --- the aggregate on /progress/ ---------------------------------------- */
const seeded = {};
seeded['learn-feedback'] = JSON.stringify({
  'logic-and-proof/truth-tables': [
    { id: 'a1', text: 'Aggregate open', done: false, created: '2026-08-19', closed: null },
    { id: 'a2', text: 'Aggregate done', done: true, created: '2026-08-18', closed: '2026-08-19' },
  ],
  'a-retired-course/gone': [
    { id: 'b1', text: 'Orphan note', done: false, created: '2026-07-01', closed: null },
  ],
});
r = run(PROGRESS, seeded);
const host = r.els.feedback.innerHTML;
check('aggregate: totals count across lessons', r.els.fbTotals.textContent,
      '2 open · 1 done · 2 lessons');
check('aggregate: a known lesson is named, not slugged',
      host.indexOf('Truth Tables') !== -1, true);
check('aggregate: it says which course and subject',
      host.indexOf('Logic and Proof') !== -1, true);
check('aggregate: a note on a retired lesson is still shown',
      host.indexOf('Orphan note') !== -1, true);
check('aggregate: and is labelled as retired',
      host.indexOf('no longer in the library') !== -1, true);
check('aggregate: a done item is marked done', /fb-item is-done/.test(host), true);

console.log(failures ? '\n' + failures + ' FAILED' : '\nall checks passed');
process.exit(failures ? 1 : 0);
