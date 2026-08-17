#!/usr/bin/env node
/*
 * Run every published lab, headlessly, and fail if one throws.
 *
 * WHY THIS EXISTS. `node --check` proves a script parses. It does not prove the
 * lab draws anything, and a lab that throws on its first redraw ships a blank
 * panel that looks like a styling problem and passes every markup test in the
 * suite. Nothing else in this repository executes the JavaScript it publishes.
 *
 * WHAT IT IS NOT. This is a minimal DOM: enough of getElementById, createElement,
 * appendChild, textContent/innerHTML, classList, dataset and addEventListener for
 * the labs to initialise and redraw. It is not a browser, it lays nothing out,
 * and it renders nothing. A lab that runs here can still look wrong; a lab that
 * fails here is broken for every reader.
 *
 * SCOPE. --generated runs the pages listed in scripts/generated-pages.txt, which
 * scripts/build_discrete_math.py writes as it builds them. That is deliberate
 * and it is not a way of avoiding awkward results: the trading path's widgets
 * use DOM features this shim does not implement -- querySelector, namespaced
 * SVG nodes, listeners on elements it returns null for -- so running them here
 * produces failures that are facts about the harness rather than about those
 * pages, which shipped working. Extending the shim to cover them is worth
 * doing; reporting its gaps as their defects is not.
 *
 * --all still runs everything, for anyone extending the shim.
 *
 * Usage:  node scripts/labcheck.js site/<course>/<lesson>/index.html ...
 *         node scripts/labcheck.js --generated    (the generated path)
 *         node scripts/labcheck.js --all          (every page under site/)
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// ---------------------------------------------------------------- the DOM

class ClassList {
  constructor(el) { this.el = el; }
  _list() { return (this.el.className || '').split(/\s+/).filter(Boolean); }
  add(...names) { const s = new Set(this._list()); names.forEach((n) => s.add(n)); this.el.className = [...s].join(' '); }
  remove(...names) { const s = new Set(this._list()); names.forEach((n) => s.delete(n)); this.el.className = [...s].join(' '); }
  contains(name) { return this._list().includes(name); }
  toggle(name) { this.contains(name) ? this.remove(name) : this.add(name); }
}

class Element {
  constructor(tag, doc) {
    this.tagName = (tag || 'div').toUpperCase();
    this._doc = doc;
    this.children = [];
    this.parentElement = null;
    this.attributes = {};
    this.dataset = {};
    this.style = new Proxy({}, { set: (t, k, v) => { t[k] = v; return true; } });
    this.className = '';
    this.classList = new ClassList(this);
    this._text = '';
    this._html = '';
    this._value = '';
    this.hidden = false;
    this.checked = false;
    this.listeners = {};
  }
  get textContent() { return this._text; }
  set textContent(v) { this._text = String(v); if (v === '') this.children = []; }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); }
  get value() { return this._value; }
  set value(v) { this._value = String(v); }
  appendChild(child) { child.parentElement = this; this.children.push(child); return child; }
  removeChild(child) { this.children = this.children.filter((c) => c !== child); return child; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
  addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); }
  removeEventListener() {}
  dispatch(type, event) { (this.listeners[type] || []).forEach((fn) => fn.call(this, event || { target: this })); }
  closest() { return null; }
  querySelector() { return null; }
  querySelectorAll() { return []; }
  focus() {}
  get firstChild() { return this.children[0] || null; }
}

class Doc {
  constructor(ids) {
    this.byId = new Map();
    this.documentElement = new Element('html', this);
    this.body = new Element('body', this);
    for (const [id, tag] of ids) {
      const el = new Element(tag, this);
      el.id = id;
      // A control's initial value is what the markup gave it; the labs set the
      // ones they care about explicitly, and an empty string is a fine default
      // for the rest because every lab reads through a parse or a lookup.
      this.byId.set(id, el);
    }
  }
  getElementById(id) { return this.byId.get(id) || null; }
  createElement(tag) { return new Element(tag, this); }
  createElementNS(_ns, tag) { return new Element(tag, this); }
  querySelector() { return null; }
  querySelectorAll() { return []; }
  addEventListener() {}
}

// -------------------------------------------------------- page inspection

/* Element ids present in the document, with the tag that declares each, so a
   <select> behaves like a select and a <div> like a div. Parsed rather than
   guessed: a lab that reads an id the page does not declare must fail here. */
function idsOf(markup) {
  const body = markup.replace(/<script[\s\S]*?<\/script>/gi, ' ');
  const ids = [];
  const tagRe = /<([a-zA-Z][\w-]*)\b([^>]*)>/g;
  let m;
  while ((m = tagRe.exec(body))) {
    const attrs = m[2];
    const idm = /\bid="([^"]+)"/.exec(attrs);
    if (idm) ids.push([idm[1], m[1].toLowerCase()]);
  }
  return ids;
}

/* Initial value of a <select> (its selected option, else its first) and of an
   <input> (its value attribute), so a lab that reads a control before writing
   it sees what a browser would see. */
function initialValues(markup) {
  const out = new Map();
  const selectRe = /<select\b([^>]*)>([\s\S]*?)<\/select>/gi;
  let m;
  while ((m = selectRe.exec(markup))) {
    const idm = /\bid="([^"]+)"/.exec(m[1]);
    if (!idm) continue;
    const options = [...m[2].matchAll(/<option\b([^>]*)>/g)].map((o) => o[1]);
    let chosen = options.find((a) => /\bselected\b/.test(a)) || options[0];
    if (chosen === undefined) continue;
    const v = /\bvalue="([^"]*)"/.exec(chosen);
    out.set(idm[1], v ? v[1] : '');
  }
  const inputRe = /<input\b([^>]*)>/gi;
  while ((m = inputRe.exec(markup))) {
    const idm = /\bid="([^"]+)"/.exec(m[1]);
    const vm2 = /\bvalue="([^"]*)"/.exec(m[1]);
    if (idm) out.set(idm[1], vm2 ? vm2[1] : '');
  }
  return out;
}

function scriptsOf(markup) {
  return [...markup.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
}

// ------------------------------------------------------------------- run

function runPage(file) {
  const markup = fs.readFileSync(file, 'utf8');
  const doc = new Doc(idsOf(markup));
  for (const [id, value] of initialValues(markup)) {
    const el = doc.getElementById(id);
    if (el) el.value = value;
  }

  const sandbox = {
    document: doc,
    console: { log() {}, warn() {}, error() {} },
    localStorage: {
      _s: new Map(),
      getItem(k) { return this._s.has(k) ? this._s.get(k) : null; },
      setItem(k, v) { this._s.set(k, String(v)); },
      removeItem(k) { this._s.delete(k); },
    },
    performance: { now: () => 0 },
    setTimeout: (fn) => { fn(); return 0; },
    clearTimeout() {},
    requestAnimationFrame: (fn) => { fn(0); return 0; },
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  sandbox.window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });

  const context = vm.createContext(sandbox);
  const problems = [];
  scriptsOf(markup).forEach((src, i) => {
    try {
      vm.runInContext(src, context, { filename: `${path.basename(path.dirname(file))}#script${i}`, timeout: 10000 });
    } catch (err) {
      problems.push(`script ${i}: ${err && err.message}`);
    }
  });

  // A lab that initialised must be able to redraw again -- that is the code
  // path every control change takes, and the one a first-paint-only test misses.
  if (typeof sandbox.redrawLab === 'function') {
    try { sandbox.redrawLab(); } catch (err) { problems.push(`redrawLab(): ${err && err.message}`); }
  } else if (/window\.redrawLab/.test(markup)) {
    problems.push('the page assigns window.redrawLab but it is not callable after load');
  }

  // The quiz is data, and every question must be answerable: the correct index
  // has to point at a real choice.
  const quizMatch = /var QUIZ = (\[[\s\S]*?\]);\n/.exec(markup);
  if (quizMatch) {
    try {
      const quiz = JSON.parse(quizMatch[1].replace(/<\\\//g, '</'));
      quiz.forEach((q, i) => {
        if (!Array.isArray(q.a) || q.a.length < 2) problems.push(`quiz ${i}: fewer than two choices`);
        if (!(q.c >= 0 && q.c < q.a.length)) problems.push(`quiz ${i}: correct index ${q.c} is out of range`);
        if (!q.why) problems.push(`quiz ${i}: no explanation`);
      });
    } catch (err) {
      problems.push(`quiz data does not parse: ${err && err.message}`);
    }
  }
  return problems;
}

function collect(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...collect(full));
    else if (entry.name.endsWith('.html')) out.push(full);
  }
  return out;
}

function main(argv) {
  let files = argv.slice(2);
  if (files[0] === '--all') {
    files = collect(path.join(__dirname, '..', 'site'));
  } else if (files[0] === '--generated') {
    const manifest = path.join(__dirname, 'generated-pages.txt');
    if (!fs.existsSync(manifest)) {
      console.error('no manifest at ' + manifest + '; run scripts/build_discrete_math.py');
      return 2;
    }
    files = fs.readFileSync(manifest, 'utf8')
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((rel) => path.join(__dirname, '..', rel));
  }
  if (!files.length) {
    console.error('usage: node scripts/labcheck.js <page.html> ... | --generated | --all');
    return 2;
  }
  let failed = 0;
  for (const file of files) {
    const problems = runPage(file);
    if (problems.length) {
      failed += 1;
      console.log(`FAIL ${path.relative(process.cwd(), file)}`);
      problems.forEach((p) => console.log(`      ${p}`));
    }
  }
  console.log(`${files.length} page(s) executed, ${failed} failing`);
  return failed ? 1 : 0;
}

process.exit(main(process.argv));
