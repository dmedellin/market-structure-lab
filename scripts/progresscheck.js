#!/usr/bin/env node
/* Tests the progress arithmetic that /progress/ actually ships.
 *
 * The numbers on that page are a promise: the ring, the four stats, the
 * per-subject meters and the list are four views of ONE set of marks, and a
 * reader who sees "12 of 218" next to a subject row reading "5 of 106" will
 * add them up. So the arithmetic is tested against the real shipped script --
 * extracted from build_auth_pages.py, not reimplemented here, because a
 * reimplementation would only prove that two copies of my own mistake agree.
 *
 * Run: node scripts/progresscheck.js
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const REPO = path.resolve(__dirname, '..');

/* Build the page the same way the site build does, then take the script out of
 * the rendered HTML. That way the inventory substitution is under test too. */
const html = (function () {
  execFileSync('python3', [path.join(REPO, 'scripts', 'build_auth_pages.py')], { stdio: 'pipe' });
  return fs.readFileSync(path.join(REPO, 'site', 'progress', 'index.html'), 'utf8');
})();

const blocks = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
if (blocks.length < 2) { console.error('expected the page to carry a script'); process.exit(1); }
const SCRIPT = blocks[blocks.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

/* --- the smallest DOM that lets the real script run ---------------------- */
function makeEl(id) {
  return { id: id, textContent: '', innerHTML: '', hidden: false, className: '',
           attrs: {}, setAttribute: function (k, v) { this.attrs[k] = v; },
           getAttribute: function (k) { return this.attrs[k]; },
           classList: { add: function () {}, remove: function () {} },
           addEventListener: function () {} };
}

function run(marks) {
  const els = {};
  const store = { 'learn-progress': JSON.stringify(marks) };
  const sandbox = {
    document: {
      getElementById: function (id) { return (els[id] = els[id] || makeEl(id)); },
      documentElement: { dataset: {} },
    },
    localStorage: {
      getItem: function (k) { return k in store ? store[k] : null; },
      setItem: function (k, v) { store[k] = v; },
      removeItem: function (k) { delete store[k]; },
    },
    sessionStorage: {
      getItem: function () { return null; }, setItem: function () {}, removeItem: function () {},
    },
    location: { href: '', search: '', replace: function () {} },
    history: { replaceState: function () {} },
    console: console, Math: Math, JSON: JSON, Date: Date,
    /* The shared theme script runs first and asks the browser things a
       sandbox has no answer for. Stub only what it touches. */
    matchMedia: function () { return { matches: false, addEventListener: function () {},
                                       addListener: function () {} }; },
    crypto: { getRandomValues: function (a) { return a; },
              subtle: { digest: function () { return Promise.resolve(new Uint8Array(32)); } } },
    TextEncoder: TextEncoder, btoa: function (s) { return Buffer.from(s, 'binary').toString('base64'); },
    atob: function (s) { return Buffer.from(s, 'base64').toString('binary'); },
    fetch: function () { return Promise.reject(new Error('no network in this harness')); },
  };
  sandbox.window = sandbox;
  const vm = require('vm');
  vm.createContext(sandbox);
  vm.runInContext(SCRIPT, sandbox, { timeout: 5000 });
  return els;
}

/* --- the library the page was built against ------------------------------ */
const LIBRARY = JSON.parse(/var LIBRARY = (\[.*?\]);\n/.exec(SCRIPT)[1]);
const ALL = [];
LIBRARY.forEach(p => p.courses.forEach(c => c.lessons.forEach(l => ALL.push(c.slug + '/' + l[0]))));
const TOTAL = ALL.length;
const TOTAL_COURSES = LIBRARY.reduce((n, p) => n + p.courses.length, 0);

let failures = 0;
function check(name, got, want) {
  const ok = String(got) === String(want);
  if (!ok) { failures++; console.log('FAIL  ' + name + '\n      got  ' + got + '\n      want ' + want); }
  else console.log('ok    ' + name);
}

/* 1. Nothing marked. */
let e = run({});
check('empty: ring reads 0%', e.ringPct.textContent, '0%');
check('empty: ring sub names the whole library', e.ringSub.textContent, '0 OF ' + TOTAL);
check('empty: lessons ticked', e.statLessons.textContent, '0');
check('empty: denominator is the tickable library', e.statLessonsOf.textContent, 'of ' + TOTAL + ' tickable');
check('empty: courses finished', e.statCourses.textContent, '0');
check('empty: subjects started', e.statPaths.textContent, '0');
check('empty: last marked is a dash', e.statLast.textContent, '—');
check('empty: recent invites a first tick', /Nothing marked yet/.test(e.recent.innerHTML), true);

/* 2. Everything marked. The interesting end of the range: a reader who has
 *    finished the library must see 100%, every course counted, no rounding
 *    that lands on 99. */
const every = {};
ALL.forEach(id => { every[id] = '2026-08-01'; });
e = run(every);
check('full: ring reads 100%', e.ringPct.textContent, '100%');
check('full: ring sub', e.ringSub.textContent, TOTAL + ' OF ' + TOTAL);
check('full: lessons ticked', e.statLessons.textContent, String(TOTAL));
check('full: every course finished', e.statCourses.textContent, String(TOTAL_COURSES));
check('full: every subject started', e.statPaths.textContent, String(LIBRARY.length));
check('full: ring is fully drawn (offset 0)', Number(e.ringFill.getAttribute('stroke-dashoffset')), 0);
check('full: the ring states its value to a screen reader',
      e.ring.getAttribute('aria-label'), TOTAL + ' of ' + TOTAL + ' lessons complete (100%)');

/* 3. One whole course, and nothing else. This is the case the old page could
 *    not express at all: it knew a mark existed but not what it was part of. */
const c0 = LIBRARY[0].courses[0];
const oneCourse = {};
c0.lessons.forEach(l => { oneCourse[c0.slug + '/' + l[0]] = '2026-08-02'; });
e = run(oneCourse);
check('one course: lessons ticked', e.statLessons.textContent, String(c0.lessons.length));
check('one course: exactly one course finished', e.statCourses.textContent, '1');
check('one course: exactly one subject started', e.statPaths.textContent, '1');
check('one course: that course row shows full', 
      new RegExp('>' + c0.lessons.length + ' / ' + c0.lessons.length + '<').test(e.paths.innerHTML), true);
check('one course: the finished row is marked done', /pg-course is-done/.test(e.paths.innerHTML), true);

/* 4. THE INVARIANT THE USER ASKED FOR: the per-subject meters must add up to
 *    the headline. If these ever disagree the page is lying to somebody. */
const scattered = {};
[0, 3, 7].forEach(i => { if (ALL[i]) scattered[ALL[i]] = '2026-08-03'; });
const last = LIBRARY[LIBRARY.length - 1];
const lastCourse = last.courses[last.courses.length - 1];
scattered[lastCourse.slug + '/' + lastCourse.lessons[0][0]] = '2026-08-04';
e = run(scattered);
const shown = Object.keys(scattered).length;
check('scattered: headline counts every mark', e.statLessons.textContent, String(shown));
const perPath = (e.paths.innerHTML.match(/(\d+) of \d+ lessons/g) || [])
  .map(s => Number(/(\d+) of/.exec(s)[1]));
check('scattered: subject meters sum to the headline',
      perPath.reduce((a, b) => a + b, 0), shown);
check('scattered: no course counted as finished', e.statCourses.textContent, '0');
// Derived from the marks this case actually makes, NOT from LIBRARY.length.
// Those two numbers were equal while there were two paths, and the assertion
// silently encoded the coincidence; a third path broke it.
const touched = new Set();
LIBRARY.forEach(p => p.courses.forEach(c => c.lessons.forEach(l => {
  if (scattered[c.slug + '/' + l[0]]) touched.add(p.slug);
})));
check('scattered: every subject with a mark counts as started',
      e.statPaths.textContent, String(touched.size));
check('scattered: latest date wins the "last marked" stat', e.statLast.textContent, '2026-08-04');

/* 4b. The trading path. Its 118 lessons were hand-written and untickable
 *     until add_progress_marks.py gave them the same toggle, so this asserts
 *     the thing that was actually broken: a trading tick has to count exactly
 *     like a mathematics one, in the same key space, toward the same totals. */
const trading = LIBRARY.filter(p => p.slug === 'trading');
check('trading: the path is in the inventory at all', trading.length, 1);
if (trading.length) {
  const tc = trading[0].courses[0];
  const one = {}; one[tc.slug + '/' + tc.lessons[0][0]] = '2026-08-19';
  const te = run(one);
  check('trading: a trading tick counts toward the headline', te.statLessons.textContent, '1');
  check('trading: it starts the trading subject', te.statPaths.textContent, '1');
  check('trading: it is not treated as a stale mark',
        /no longer in the library/.test(te.recent.innerHTML), false);
  check('trading: the lesson is named, not slugified',
        te.recent.innerHTML.indexOf(tc.lessons[0][1]) !== -1, true);
  check('trading: every trading lesson is reachable from the inventory',
        trading[0].courses.reduce((n, c) => n + c.lessons.length, 0), 118);
}

/* 5. A mark for a lesson that is no longer in the library. It must not inflate
 *    the totals, and it must not vanish either. */
e = run({ 'a-retired-course/a-retired-lesson': '2026-07-01' });
check('stale: not counted in the headline', e.statLessons.textContent, '0');
check('stale: not counted in the ring', e.ringPct.textContent, '0%');
check('stale: still shown to the reader', /no longer in the library/.test(e.recent.innerHTML), true);
check('stale: one stale mark reads in the singular',
      /1 mark refers to a lesson that is no longer/.test(e.recent.innerHTML), true);
e = run({ 'gone-a/x': '2026-07-01', 'gone-b/y': '2026-07-02' });
check('stale: two stale marks read in the plural',
      /2 marks refer to lessons that are no longer/.test(e.recent.innerHTML), true);

/* 6. Signed out, the sign-out button must be hidden and sign-in shown. */
e = run({});
check('signed out: sign-in offered', e.signin.hidden, false);
check('signed out: sign-out hidden', e.signout.hidden, true);
check('signed out: sync card hidden', e.syncCard.hidden, true);

console.log(failures ? '\n' + failures + ' FAILED' : '\nall checks passed');
process.exit(failures ? 1 : 0);
