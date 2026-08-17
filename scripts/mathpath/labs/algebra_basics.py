"""Courses 1-4: the algebra a reader has to be able to do without thinking.

Four labs live here, and each one exists because a specific thing goes wrong in
this material. The teaching decision behind each is stated with its function, so
here is only what they share.

EVERY ONE OF THESE LESSONS IS ABOUT A RULE THE READER ALREADY HALF-KNOWS. That
makes them different from the quadratic: nobody guesses the quadratic formula,
but everybody has an opinion about 8 - 3 + 2, about (a + b)^2, and about whether
sqrt(2) + sqrt(3) is sqrt(5). A lab that only printed the right answer would be
one more assertion competing with the reader's existing one. So each lab here is
built to make a WRONG method run alongside the right one and be seen to break:

  * expression/order    prints the queue of pending operations, so the reader
                        can see the operation their eye wanted to do first sit
                        in the queue behind the one that actually goes first.
  * expression/property tests each named law on the reader's own numbers and
                        includes laws that are FALSE. On (4, 4, 4) subtraction
                        looks commutative, and the lab then goes and finds a
                        counterexample by search.
  * exponents/laws      verifies every law twice: once by the law, and once by
                        writing the powers out and multiplying them one at a
                        time. Agreement between two independent computations is
                        the evidence. (a + b)^n = a^n + b^n is on the same list
                        and it disagrees, which is the point.
  * radicals/solve      squares both sides and then CHECKS, exactly, in the
                        original equation. The extraneous root is drawn as a
                        hollow point where the two curves do not meet.

Both house rules hold throughout. Nothing below is a stored answer: the file
contains presets (which expression to look at) and never results. Everything is
exact -- rationals over BigInt for coefficients and steps, and for irrational
answers a surd type carrying q*sqrt(k). The one place a decimal appears is where
a lesson is ABOUT approximation (is sqrt(2) bigger than 1.414?), and it is
labelled as a rounding where it appears.
"""

import json

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# --------------------------------------------------------------- formatting

# Shared by all four labs: the table, row and chip helpers. Every lab on this
# path builds its output as HTML strings from computed values, so these are the
# only place the markup conventions live.
FORMAT_JS = r"""
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function td(text, cls) { return '<td' + (cls ? ' class="' + cls + '"' : '') + '>' + text + '</td>'; }
  function tdl(text, cls) {
    return '<td style="text-align:left;"' + (cls ? ' class="' + cls + '"' : '') + '>' + text + '</td>';
  }
  function th(text) { return '<th>' + text + '</th>'; }
  function rowhead(text) { return '<th class="rowhead">' + text + '</th>'; }
  function tr(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.join('') + '</tr>'; }
  function table(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption><tbody>'
      + rows.join('') + '</tbody></table></div>';
  }
  function step(label, detail) { return tr([rowhead(label), tdl(detail)]); }
  function chip(text, kind) { return '<span class="chip' + (kind ? ' ' + kind : '') + '">' + text + '</span>'; }
  function tone(text, kind) { return '<span class="tone-' + kind + '">' + text + '</span>'; }
  /* Rparse throws on a denominator of zero, and 1/0 is a thing a reader can
     type. Every call on reader input goes through this instead, so a bad
     fraction becomes an explanation rather than an exception. */
  function Rread(text) {
    try { return Rparse(String(text).trim()); } catch (err) { return null; }
  }
  /* A decimal that a lesson has decided to show. Never used to decide anything;
     every comparison and every verdict on this path is made on the exact side. */
  function approx(x, places) {
    var v = Number(x);
    if (!isFinite(v)) return 'not a real number';
    return v.toFixed(places === undefined ? 6 : places);
  }
"""

# --------------------------------------------------------------- monomials

# The first algebra a reader meets is not in one variable. 4xy - y^2 + 2 is an
# ordinary expression and a lab that could only hold polynomials in x would have
# to refuse it, so terms carry a map from letter to exponent. That map is also
# exactly what "like terms" compares, which is why the like-terms mode is three
# lines of code on top of this and not a special case.
MONO_JS = r"""
  function Vkey(v) {
    var ks = [], k;
    for (k in v) if (v.hasOwnProperty(k) && v[k]) ks.push(k);
    ks.sort();
    return ks.map(function (n) { return n + '^' + v[n]; }).join(' ');
  }
  function Vdeg(v) { var d = 0, k; for (k in v) if (v.hasOwnProperty(k)) d += v[k]; return d; }
  function Vmul(a, b) {
    var out = {}, k;
    for (k in a) if (a.hasOwnProperty(k)) out[k] = a[k];
    for (k in b) if (b.hasOwnProperty(k)) out[k] = (out[k] || 0) + b[k];
    return out;
  }
  /* The variable part as the reader writes it: x^2y, with the letters in
     alphabetical order so that 3yx and 3xy come out identical -- which is the
     whole content of the like-terms lesson. */
  function Vtext(v) {
    var ks = [], k;
    for (k in v) if (v.hasOwnProperty(k) && v[k]) ks.push(k);
    ks.sort();
    return ks.map(function (n) { return v[n] === 1 ? n : n + '^' + v[n]; }).join('');
  }
  function Mnorm(list) {
    var byKey = {}, order = [];
    list.forEach(function (t) {
      var key = Vkey(t.v);
      if (!byKey[key]) { byKey[key] = { c: R0, v: t.v, key: key }; order.push(key); }
      byKey[key].c = Radd(byKey[key].c, t.c);
    });
    var out = [];
    order.forEach(function (key) { if (!Rzero(byKey[key].c)) out.push(byKey[key]); });
    /* Highest total degree first, and within a degree the way a reader writes
       it: x^2y before xy^2, because the exponent of the alphabetically first
       letter is compared first and the larger one leads. */
    out.sort(function (a, b) {
      var da = Vdeg(a.v), db = Vdeg(b.v);
      if (da !== db) return db - da;
      var names = {}, k;
      for (k in a.v) if (a.v.hasOwnProperty(k) && a.v[k]) names[k] = 1;
      for (k in b.v) if (b.v.hasOwnProperty(k) && b.v[k]) names[k] = 1;
      var ks = Object.keys(names).sort();
      for (var i = 0; i < ks.length; i += 1) {
        var ea = a.v[ks[i]] || 0, eb = b.v[ks[i]] || 0;
        if (ea !== eb) return eb - ea;
      }
      return 0;
    });
    return out;
  }
  function Madd(a, b) { return Mnorm(a.concat(b)); }
  function Mneg(a) { return a.map(function (t) { return { c: Rneg(t.c), v: t.v }; }); }
  function Msub(a, b) { return Mnorm(a.concat(Mneg(b))); }
  function Mmul(a, b) {
    var out = [];
    a.forEach(function (s) {
      b.forEach(function (t) { out.push({ c: Rmul(s.c, t.c), v: Vmul(s.v, t.v) }); });
    });
    return Mnorm(out);
  }
  function Mpow(a, k) { var out = [{ c: R1, v: {} }]; for (var i = 0; i < k; i += 1) out = Mmul(out, a); return out; }
  function Mconst(a) { return a.length === 0 || (a.length === 1 && Vdeg(a[0].v) === 0); }
  function Mequ(a, b) { return Msub(a, b).length === 0; }
  /* One term, with the conventions a marker applies: an implicit coefficient of
     1 is not written, and a fraction is bracketed so (3/4)x cannot be misread
     as 3/(4x). */
  function Mtermtext(t) {
    var vt = Vtext(t.v), one = Requ(Rabs(t.c), R1);
    var sign = Rsign(t.c) < 0 ? '-' : '';
    var mag = Rabs(t.c);
    if (one && vt) return sign + vt;
    return sign + (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')') + vt;
  }
  function Mtext(list) {
    if (!list.length) return '0';
    var out = '';
    list.forEach(function (t) {
      var neg = Rsign(t.c) < 0, mag = Rabs(t.c), vt = Vtext(t.v);
      out += out === '' ? (neg ? '-' : '') : (neg ? ' - ' : ' + ');
      var one = Requ(mag, R1);
      out += (one && vt ? '' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')')) + vt;
    });
    return out;
  }
  /* The parse tree as a sum of monomials, or a thrown explanation. Everything
     that can go wrong here is something a reader can legitimately type, so each
     failure says what it was rather than returning null. */
  function Mof(node) {
    switch (node.k) {
      case 'num': {
        var r = Rread(node.v);
        if (r === null) throw new Error('"' + esc(node.v) + '" is not a number I can read exactly');
        return Rzero(r) ? [] : [{ c: r, v: {} }];
      }
      case 'var': { var v = {}; v[node.v] = 1; return [{ c: R1, v: v }]; }
      case 'neg': return Mneg(Mof(node.a));
      case 'add': return Madd(Mof(node.a), Mof(node.b));
      case 'sub': return Msub(Mof(node.a), Mof(node.b));
      case 'mul': return Mmul(Mof(node.a), Mof(node.b));
      case 'div': {
        var d = Mof(node.b);
        if (!d.length) throw new Error('this divides by zero, and nothing divided by zero has a value');
        if (!Mconst(d)) throw new Error('dividing by ' + Mtext(d) + ' does not give a polynomial, so this lesson cannot take it apart into terms');
        return Mmul(Mof(node.a), [{ c: Rinv(d[0].c), v: {} }]);
      }
      case 'pow': {
        var e = Mof(node.b);
        if (!Mconst(e)) throw new Error('an exponent with a letter in it is a later lesson');
        var k = e.length ? e[0].c : R0;
        if (!Rint(k) || k.n < 0n) throw new Error('the exponent ' + Rtext(k) + ' is not a whole number, so this is a root rather than a polynomial term');
        if (k.n > 12n) throw new Error('powers above 12 are more than this lesson needs');
        return Mpow(Mof(node.a), Number(k.n));
      }
      case 'fn': throw new Error(node.v + '(...) is not a polynomial term');
    }
    throw new Error('I cannot read that expression');
  }
"""

# ------------------------------------------------------ order of operations

# The queue.
#
# A parse tree already encodes precedence -- that is what parsing IS -- so the
# next operation to perform is always the leftmost node whose two operands are
# already numbers, and running that rule to exhaustion reproduces the order of
# operations exactly. 8 - 3 + 2 parses as (8 - 3) + 2 and so subtracts first;
# 2 + 3 * 4 parses as 2 + (3 * 4) and so multiplies first; -3^2 parses as
# -(3^2). Nothing here special-cases those; they fall out.
#
# The reader is shown the queue rather than the answer, because the mistake
# being corrected is one of ORDER and an answer alone does not locate it.
STEP_JS = r"""
  /* `sub` marks a number that arrived by substitution. Those are printed
     inside brackets wherever they sit, because the habit the lesson is trying
     to build is bracketing the value every time rather than only when it turns
     out to matter -- and the reader cannot tell in advance which time that is. */
  function numnode(r, sub) { return { k: 'num', v: Rtext(r), r: r, sub: !!sub }; }
  function nodeR(node) {
    if (node.r) return node.r;
    var r = Rread(node.v);
    if (r === null) throw new Error('"' + esc(node.v) + '" is not a number I can read exactly');
    return r;
  }
  var PREC = { add: 1, sub: 1, mul: 2, div: 2, neg: 3, pow: 4 };
  var OPSYM = { add: '+', sub: '-', mul: '*', div: '/' };
  function precof(n) { return PREC[n.k] === undefined ? 5 : PREC[n.k]; }

  /* Brackets are printed where the expression needs them and nowhere else, so
     the printed line is always a faithful reading of the tree being reduced. */
  function parenNeeded(parent, child, side) {
    if (child.k === 'num') {
      if (child.sub) return parent.k !== 'fn';
      var r = child.r || Rread(child.v);
      /* -3 and 3/4 are bracketed as operands, the same convention Rterm uses:
         2 + (-3) and (3/4) * 2 can never be misread. */
      return !!(r && (Rsign(r) < 0 || !Rint(r)) && parent.k !== 'fn');
    }
    if (parent.k === 'fn') return false;
    var pc = precof(child), pp = precof(parent);
    if (parent.k === 'pow') return side === 'l' ? pc <= 4 : pc < 5;
    if (parent.k === 'neg') return pc <= 2;
    if (pc < pp) return true;
    return pc === pp && side === 'r' && (parent.k === 'sub' || parent.k === 'div');
  }
  function Eshow(node, target, cls) {
    function kid(child, side) {
      var s = Eshow(child, target, cls);
      return parenNeeded(node, child, side) ? '(' + s + ')' : s;
    }
    var body;
    if (node.k === 'num') body = node.r ? Rtext(node.r) : node.v;
    else if (node.k === 'var') body = node.v;
    else if (node.k === 'neg') body = '-' + kid(node.a, 'r');
    else if (node.k === 'fn') body = node.v + '(' + Eshow(node.a, target, cls) + ')';
    else if (node.k === 'pow') body = kid(node.a, 'l') + '^' + kid(node.b, 'r');
    else body = kid(node.a, 'l') + ' ' + OPSYM[node.k] + ' ' + kid(node.b, 'r');
    if (target && node === target && cls) body = '<span class="' + cls + '">' + body + '</span>';
    return body;
  }
  function isnum(n) { return n.k === 'num'; }
  /* The next operation: leftmost, innermost, both operands already numbers. */
  function findTarget(node) {
    if (node.k === 'num' || node.k === 'var') return null;
    if (node.k === 'neg' || node.k === 'fn') {
      var t = findTarget(node.a);
      return t ? t : (isnum(node.a) ? node : null);
    }
    var l = findTarget(node.a);
    if (l) return l;
    var r = findTarget(node.b);
    if (r) return r;
    return (isnum(node.a) && isnum(node.b)) ? node : null;
  }
  /* Is the operation inside brackets in the printed line? Answered by walking
     the path to it and asking the printer, so the rule quoted to the reader and
     the brackets they can see always come from the same decision. */
  function bracketed(root, target) {
    var found = false;
    (function walk(node, wrapped) {
      if (node === target) { found = wrapped; return true; }
      if (node.k === 'num' || node.k === 'var') return false;
      if (node.k === 'neg' || node.k === 'fn') return walk(node.a, wrapped || parenNeeded(node, node.a, 'r'));
      if (walk(node.a, wrapped || parenNeeded(node, node.a, 'l'))) return true;
      return walk(node.b, wrapped || parenNeeded(node, node.b, 'r'));
    })(root, false);
    return found;
  }
  function ruleFor(root, target) {
    if (bracketed(root, target)) return 'brackets first: this one is inside a bracket';
    if (target.k === 'fn') return 'the function acts on the number inside its brackets';
    if (target.k === 'pow') return 'powers before multiplying and dividing';
    if (target.k === 'neg') return 'the minus sign in front applies last, to the whole power';
    if (target.k === 'mul' || target.k === 'div') return 'multiply and divide before adding, left to right';
    return 'add and subtract last, left to right';
  }
  function Estep(node) {
    var a = node.a ? nodeR(node.a) : null, b = node.b ? nodeR(node.b) : null;
    if (node.k === 'neg') return Rneg(a);
    if (node.k === 'add') return Radd(a, b);
    if (node.k === 'sub') return Rsub(a, b);
    if (node.k === 'mul') return Rmul(a, b);
    if (node.k === 'div') {
      if (Rzero(b)) throw new Error('this expression divides by zero, and nothing divided by zero has a value');
      return Rdiv(a, b);
    }
    if (node.k === 'pow') {
      if (!Rint(b)) throw new Error('the exponent ' + Rtext(b) + ' is a fraction, which makes this a root: the radicals lesson does those');
      if (Rzero(a) && b.n < 0n) throw new Error('0 to a negative power means dividing by zero');
      if (b.n > 40n || b.n < -40n) throw new Error('the exponent ' + Rtext(b) + ' is larger than this lesson needs');
      return Rpow(a, Number(b.n));
    }
    throw new Error('the function ' + (node.v || node.k) + ' is not part of this lesson');
  }
  function Ereplace(node, target, repl) {
    if (node === target) return repl;
    if (node.k === 'num' || node.k === 'var') return node;
    if (node.k === 'neg' || node.k === 'fn') return { k: node.k, v: node.v, a: Ereplace(node.a, target, repl) };
    return { k: node.k, v: node.v, a: Ereplace(node.a, target, repl), b: Ereplace(node.b, target, repl) };
  }
  /* Reduce to a number, collecting the queue on the way. Throws with a reader-
     facing sentence; every caller puts that sentence in the status banner. */
  function Equeue(tree) {
    var node = tree, steps = [], guard = 0;
    while (guard < 60) {
      guard += 1;
      var t = findTarget(node);
      if (!t) break;
      var rule = ruleFor(node, t), before = Eshow(node, t, 'tone-cyan');
      var did = t.k === 'neg' ? '-(' + Eshow(t.a, null, '') + ')' : Eshow(t, null, '');
      var value;
      /* A step that cannot be done stops the queue where it stopped. The
         reader is shown the operations that did run and the one that could
         not, which locates the problem; a bare error message does not. */
      try { value = Estep(t); }
      catch (err) { return { steps: steps, value: null, rest: Eshow(node, t, 'tone-red'), error: err.message, stuck: did }; }
      node = Ereplace(node, t, numnode(value));
      steps.push({ rule: rule, before: before, did: did, value: value, after: Eshow(node, null, '') });
    }
    if (node.k !== 'num') return { steps: steps, value: null, rest: Eshow(node, null, ''), error: null };
    return { steps: steps, value: nodeR(node), rest: null, error: null };
  }
  /* The same expression read the way a reader who ignores precedence reads it.
     `right` false groups strictly left to right; `right` true does the last
     operation first, which is what "8 - 3 + 2 is 8 - 5" and "24 / 4 / 2 is
     24 / 2" actually are. Neither is a straw man -- between them they are most
     of the wrong answers -- and the lab computes both rather than asserting
     that they differ. */
  function Enaive(src, right) {
    var toks = Etokenize(src), pos = 0;
    function prim() {
      var tk = toks[pos];
      if (!tk) throw new Error('the expression ends early');
      if (tk.t === 'num') { pos += 1; return { k: 'num', v: tk.v }; }
      if (tk.t === 'var') { pos += 1; return { k: 'var', v: tk.v }; }
      if (tk.t === '-') { pos += 1; return { k: 'neg', a: prim() }; }
      if (tk.t === '+') { pos += 1; return prim(); }
      if (tk.t === 'fn') {
        pos += 1;
        if (toks[pos] && toks[pos].t === '(') pos += 1;
        var a = chain();
        if (toks[pos] && toks[pos].t === ')') pos += 1;
        return { k: 'fn', v: tk.v, a: a };
      }
      if (tk.t === '(') {
        pos += 1;
        var e = chain();
        if (toks[pos] && toks[pos].t === ')') pos += 1; else throw new Error('a bracket is never closed');
        return e;
      }
      throw new Error('unexpected symbol "' + (tk.v || tk.t) + '"');
    }
    function chain() {
      var node = prim();
      while (pos < toks.length) {
        var tk = toks[pos], kinds = { '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '^': 'pow' };
        if (tk.t === ')' || tk.t === ',') break;
        if (kinds[tk.t]) {
          pos += 1;
          if (right) return { k: kinds[tk.t], a: node, b: chain() };
          node = { k: kinds[tk.t], a: node, b: prim() };
          continue;
        }
        if (tk.t === 'num' || tk.t === 'var' || tk.t === '(' || tk.t === 'fn') {
          if (right) return { k: 'mul', a: node, b: chain() };
          node = { k: 'mul', a: node, b: prim() };
          continue;
        }
        break;
      }
      return node;
    }
    var tree = chain();
    if (pos < toks.length) throw new Error('unexpected symbol');
    return tree;
  }
  /* The terms AS WRITTEN: the top-level + and - only. 5(x + 2) is ONE term
     until somebody expands it, and the difference between that and the two
     terms it becomes is the whole of the distributive lesson. */
  function Esplit(node, sign, out) {
    if (node.k === 'add') { Esplit(node.a, sign, out); Esplit(node.b, sign, out); return out; }
    if (node.k === 'sub') { Esplit(node.a, sign, out); Esplit(node.b, -sign, out); return out; }
    if (node.k === 'neg') { Esplit(node.a, -sign, out); return out; }
    out.push({ node: node, sign: sign });
    return out;
  }
  function Efactors(node, out) {
    if (node.k === 'mul') { Efactors(node.a, out); Efactors(node.b, out); return out; }
    if (node.k === 'neg') { out.push(numnode(R(-1n))); Efactors(node.a, out); return out; }
    out.push(node);
    return out;
  }
  function Evars(node, out) {
    if (node.k === 'var') { if (out.indexOf(node.v) < 0) out.push(node.v); return out; }
    if (node.a) Evars(node.a, out);
    if (node.b) Evars(node.b, out);
    return out;
  }
"""

# =====================================================================
#                          THE EXPRESSION LAB
# =====================================================================

# Presets are WHICH expression to look at, never what comes out of it. Each
# list is chosen so a lesson can walk it and meet the failure on the way: the
# order presets include the two that a left-to-right reading gets wrong, the
# property presets include (4, 4, 4), where subtraction looks commutative, and
# the terms presets include 5(x + 2), which is one term and looks like two.
EXPR_PRESETS = {
    "order": [
        ("2 * (3 + 4)^2 - 10 / 5", "2 * (3 + 4)^2 - 10 / 5"),
        ("8 - 3 + 2", "8 - 3 + 2"),
        ("24 / 4 / 2", "24 / 4 / 2"),
        ("2 + 3 * 4^2", "2 + 3 * 4^2"),
        ("-3^2", "-3^2"),
        ("(-3)^2", "(-3)^2"),
    ],
    "property": [
        ("a = 2, b = 5, c = 3", "2|5|3"),
        ("a = 4, b = 4, c = 4", "4|4|4"),
        ("a = 1, b = 1, c = 1", "1|1|1"),
        ("a = 0, b = 7, c = 1", "0|7|1"),
        ("a = 1/2, b = -3, c = 2/3", "1/2|-3|2/3"),
        ("a = 6, b = 3, c = 2", "6|3|2"),
    ],
    "terms": [
        ("3x^2 - 5x + 7", "3x^2 - 5x + 7"),
        ("4xy - y^2 + 2", "4xy - y^2 + 2"),
        ("-x + (2/3)x^2 - 5", "-x + (2/3)x^2 - 5"),
        ("5(x + 2)", "5(x + 2)"),
        ("x^2y - 3xy^2", "x^2y - 3xy^2"),
        ("5x - 5x + 4", "5x - 5x + 4"),
    ],
    "distribute": [
        ("3(x + 4)", "3|x + 4"),
        ("-2(x - 5)", "-2|x - 5"),
        ("-(x - 7)", "-1|x - 7"),
        ("(x + 2)(x - 3)", "x + 2|x - 3"),
        ("(2x - 1)(3x + 4)", "2x - 1|3x + 4"),
        ("(1/2)(4x - 6)", "1/2|4x - 6"),
    ],
    "like": [
        ("3x + 4y - x + 2y", "3x + 4y - x + 2y"),
        ("5x^2 + 2x - 3x^2 + x", "5x^2 + 2x - 3x^2 + x"),
        ("3xy + 2yx - xy", "3xy + 2yx - xy"),
        ("5x^2y - 2xy^2", "5x^2y - 2xy^2"),
        ("2x + 3 - 5 - 2x", "2x + 3 - 5 - 2x"),
        ("4a - 3b + 2a - b + 7", "4a - 3b + 2a - b + 7"),
    ],
    "evaluate": [
        ("x^2  at  x = -3", "x^2|x = -3"),
        ("-x^2  at  x = -3", "-x^2|x = -3"),
        ("2x^2 - 3x + 1  at  x = -1/2", "2x^2 - 3x + 1|x = -1/2"),
        ("5 - 2x  at  x = -4", "5 - 2x|x = -4"),
        ("x^2 - y^2  at  x = -3, y = 2", "x^2 - y^2|x = -3, y = 2"),
        ("1/(x - 2)  at  x = 2", "1/(x - 2)|x = 2"),
    ],
    "translate": [
        ("five less than a number n", "five less than a number n|n - 5|5 - n"),
        ("twice the sum of n and 3", "twice the sum of n and 3|2(n + 3)|2n + 3"),
        ("the sum of twice n and 3", "the sum of twice n and 3|2n + 3|2(n + 3)"),
        ("three less than the square of n", "three less than the square of n|n^2 - 3|(n - 3)^2"),
        ("half of n, increased by 4", "half of n, increased by 4|n/2 + 4|n/(2 + 4)"),
        ("the quotient of n and 4, decreased by 1", "the quotient of n and 4, decreased by 1|n/4 - 1|n/(4 - 1)"),
    ],
}

EXPR_TITLES = {
    "order": ("The queue of pending operations", "Which operation goes first, and why"),
    "property": ("The named properties", "Tested on your numbers, then searched for a counterexample"),
    "terms": ("The parts of an expression", "Terms, coefficients, factors, degree"),
    "distribute": ("Multiplying out", "Every term against every term"),
    "like": ("Like terms", "Same letters, same exponents, or they are not like"),
    "evaluate": ("Substitution", "Brackets round the value, every time"),
    "translate": ("English into algebra", "Two readings, tested against each other"),
}

EXPR_LEGEND = {
    "order": '<span class="tone-cyan"><i class="legend-swatch"></i>next in the queue</span>'
             '<span class="tone-amber"><i class="legend-swatch"></i>read left to right instead</span>',
    "property": '<span class="tone-green"><i class="legend-swatch"></i>held</span>'
                '<span class="tone-red"><i class="legend-swatch"></i>failed</span>',
    "terms": '<span class="tone-cyan"><i class="legend-swatch"></i>as written</span>'
             '<span class="tone-purple"><i class="legend-swatch"></i>after expanding</span>',
    "distribute": '<span class="tone-cyan"><i class="legend-swatch"></i>each product</span>'
                  '<span class="tone-green"><i class="legend-swatch"></i>collected</span>',
    "like": '<span class="tone-cyan"><i class="legend-swatch"></i>a group of like terms</span>',
    "evaluate": '<span class="tone-cyan"><i class="legend-swatch"></i>with brackets</span>'
                '<span class="tone-red"><i class="legend-swatch"></i>without them</span>',
    "translate": '<span class="tone-green"><i class="legend-swatch"></i>agrees</span>'
                 '<span class="tone-red"><i class="legend-swatch"></i>differs</span>',
}

EXPR_KPIS = {
    "order": ("Operations", "Exact value", "Misreadings that differ"),
    "property": ("Claims tested", "Held on yours", "False in general"),
    "terms": ("Terms as written", "After expanding", "Degree"),
    "distribute": ("Products", "Before collecting", "After collecting"),
    "like": ("Terms", "Groups", "After collecting"),
    "evaluate": ("Letters", "With brackets", "Without brackets"),
    "translate": ("Test values", "Agreements", "Verdict"),
}

EXPR_HINTS = {
    "order": "Write it as you would type it into a calculator: <code>2 * (3 + 4)^2 - 10 / 5</code>. "
             "Only numbers here &mdash; the evaluate mode is the one with letters in it.",
    "property": "Each of a, b and c is a whole number or a fraction such as <code>-3/2</code>.",
    "terms": "Letters, numbers, <code>^</code> for powers, brackets, and juxtaposition for "
             "multiplication: <code>4xy - y^2 + 2</code>.",
    "distribute": "Each factor is an expression: <code>2x - 1</code> and <code>3x + 4</code>. "
                  "A single number is a perfectly good factor.",
    "like": "One expression, several terms: <code>3x + 4y - x + 2y</code>.",
    "evaluate": "The values are written the way you would say them: <code>x = -3, y = 2</code>. "
                "Fractions such as <code>-1/2</code> are exact.",
    "translate": "Use <code>n</code> for the number the phrase is about. "
                 "<code>2(n + 3)</code> and <code>2n + 3</code> are both valid algebra; "
                 "only one of them is what the phrase says.",
}

EXPR_FIELDS = {
    "order": [("exExpr", "Expression")],
    "property": [("exA", "a"), ("exB", "b"), ("exC", "c")],
    "terms": [("exExpr", "Expression")],
    "distribute": [("exLeft", "First factor"), ("exRight", "Second factor")],
    "like": [("exExpr", "Expression")],
    "evaluate": [("exExpr", "Expression"), ("exVals", "Values")],
    "translate": [("exExpr", "Your expression in n")],
}

EXPR_PANEL = {
    "order": ("Choose or type an expression",
              "Nothing is evaluated until the queue is built. Change the expression and the "
              "queue, the rule behind each step and both answers are recomputed."),
    "property": ("Choose three numbers",
                 "Every claim below is checked on your a, b and c, and then searched for a "
                 "counterexample over 512 triples. The lab is not told which claims are laws."),
    "terms": ("Choose or type an expression",
              "The expression is split at its top-level plus and minus signs &mdash; which is "
              "what counting terms means &mdash; and then expanded, so you can see when the two "
              "counts differ."),
    "distribute": ("Choose two factors",
                   "Every term of the first is multiplied by every term of the second, in a grid, "
                   "and the products are then collected."),
    "like": ("Choose or type an expression",
             "Terms are grouped by their variable part. Two terms are like exactly when those "
             "parts are identical, which the alphabetical ordering makes visible."),
    "evaluate": ("Choose an expression and values",
                 "The substitution is done twice: with brackets round each value and without "
                 "them, so you can see when the second one changes the answer."),
    "translate": ("Choose a phrase",
                  "The box starts with the reading most readers give the phrase. Both readings "
                  "are evaluated at seven values of n and compared, and the polynomials are also "
                  "compared exactly."),
}

# The shared front of every expression mode: the handles, and the one function
# that has to work when the reader's input does not.
EXPR_PRELUDE = r"""
  var preset = document.getElementById('exPreset');
  var stage = document.getElementById('exStage');
  var work = document.getElementById('exWork');
  var status = document.getElementById('exStatus');
  var subOut = document.getElementById('exSub');
  var kA = document.getElementById('exK1'), kB = document.getElementById('exK2'), kC = document.getElementById('exK3');
  function kpis(a, b, c) { kA.textContent = a; kB.textContent = b; kC.textContent = c; }
  /* Bad input is a state the lab has to be able to be in. It says what is
     wrong, keeps the panel populated, and never throws. */
  function fail(lead, detail) {
    stage.innerHTML = table('nothing computed yet', [step('input', tone(esc(lead), 'red'))]);
    work.innerHTML = '';
    kpis('&mdash;', '&mdash;', '&mdash;');
    status.innerHTML = '<strong>' + lead + '</strong> ' + detail + ' ' + HINT;
  }
"""

EXPR_BODY = {}

EXPR_BODY["order"] = r"""
  var input = document.getElementById('exExpr');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = src ? src : 'nothing typed yet';
    if (!src) { fail('Type an arithmetic expression.', 'The box is empty, so there is no queue to build.'); return; }
    var tree;
    try { tree = Eparse(src); }
    catch (err) { fail('That expression does not parse.', esc(err.message) + '.'); return; }
    var letters = Evars(tree, []);
    if (letters.length) {
      fail('This mode works on numbers only.', 'The expression contains the letter '
        + letters.join(', ') + ', and an operation on a letter cannot be carried out until the '
        + 'letter has a value. Substitution is the mode that does that first.');
      return;
    }
    var q = Equeue(tree);

    /* The same string as a reader who ignores precedence reads it: strictly
       left to right, brackets honoured and nothing else. Computed rather than
       asserted, so the lab can also report the cases where it agrees. */
    function reading(right) {
      var out = { value: null, why: null, text: '&mdash;' };
      try {
        var nt = Enaive(src, right);
        out.text = Eshow(nt, null, '');
        var nq = Equeue(nt);
        if (nq.value) out.value = nq.value; else out.why = nq.error || 'it does not reduce to a number';
      } catch (err) { out.why = err.message; }
      return out;
    }
    var ltr = reading(false), rtl = reading(true);

    var headline = q.steps.length ? q.steps[0].before : Eshow(tree, null, '');
    stage.innerHTML = table('the expression, with the operation at the head of the queue marked', [
      step('as written', esc(src)),
      step('as it is read', headline),
      step('operations pending', String(q.steps.length + (q.error ? 1 : 0))),
      step('value', q.value ? Rtext(q.value) : tone('the queue stopped', 'red')),
    ]);

    var rows = [tr([th('#'), th('the rule that puts it here'), th('operation'), th('what is left')])];
    q.steps.forEach(function (s, i) {
      rows.push(tr([td(String(i + 1)), tdl(s.rule), td(s.did + ' = ' + Rtext(s.value)), tdl(s.after)],
        i === 0 ? 'focus' : ''));
    });
    if (q.error) {
      rows.push(tr([td(String(q.steps.length + 1)), tdl(tone('cannot be done', 'red')),
        td(q.stuck), tdl(esc(q.error))], 'focus'));
    }
    if (!q.steps.length && !q.error) rows.push(tr([tdl('&mdash;'), tdl('there is nothing to do: this is already a number'), tdl('&mdash;'), tdl(esc(src))]));

    function readingRow(label, r) {
      var same = q.value && r.value && Requ(q.value, r.value);
      return tr([
        tdl(label), tdl(r.text),
        td(r.value ? Rtext(r.value) : tone(esc(r.why || 'no value'), 'red')),
        tdl(same ? '<span class="chip ok">same answer here</span>' : '<span class="chip no">a different answer</span>'),
      ], same ? '' : 'focus');
    }
    var compare = [tr([th('read as'), th('which groups it as'), th('value'), th('same as the queue?')])];
    compare.push(tr([tdl('the queue above: brackets, powers, then times and divide, then plus and minus'),
      tdl(Eshow(tree, null, '')), td(q.value ? Rtext(q.value) : tone('stopped', 'red')), tdl('&mdash;')]));
    compare.push(readingRow('strictly left to right, ignoring precedence', ltr));
    compare.push(readingRow('the last operation first', rtl));
    var differ = 0;
    [ltr, rtl].forEach(function (r) { if (!(q.value && r.value && Requ(q.value, r.value))) differ += 1; });

    work.innerHTML = table('The queue: every operation, in the order the expression forces', rows)
      + table('The same string, read three ways', compare);

    kpis(String(q.steps.length), q.value ? Rtext(q.value) : 'stopped', differ + ' of 2');

    var msg;
    if (q.error) {
      msg = '<strong>The queue stops at ' + q.stuck + '.</strong> ' + esc(q.error)
        + '. Everything above that line was carried out; nothing below it can be.';
    } else if (!differ) {
      msg = '<strong>' + esc(src) + ' = ' + Rtext(q.value) + ', and both of the other readings give '
        + 'that too.</strong> This expression is forgiving, which is not a rule: the operations here '
        + 'happen to sit in an order that precedence would have chosen anyway. The presets that '
        + 'follow are not forgiving.';
    } else {
      var lines = [];
      if (ltr.value && !Requ(q.value, ltr.value)) lines.push('read strictly left to right it groups as ' + ltr.text + ' and comes to ' + Rtext(ltr.value));
      if (rtl.value && !Requ(q.value, rtl.value)) lines.push('doing the last operation first it groups as ' + rtl.text + ' and comes to ' + Rtext(rtl.value));
      msg = '<strong>' + esc(src) + ' = ' + Rtext(q.value) + '.</strong> The same symbols, '
        + 'read differently, give different numbers: ' + lines.join('; ') + '. The queue above is not '
        + 'a convention somebody chose to be awkward. It is what the brackets, the powers and the '
        + 'left-to-right rule for equal precedence force, one operation at a time, and the rule '
        + 'column says which of those put each operation where it is.';
    }
    if (q.value && !Rint(q.value)) {
      msg += ' The answer ' + Rtext(q.value) + ' is exact; as a decimal it is '
        + Rdec(q.value, 6) + (Rdec(q.value, 6).length > 8 ? ', rounded' : '') + '.';
    }
    status.innerHTML = msg;
  }
"""

EXPR_BODY["property"] = r"""
  var inA = document.getElementById('exA'), inB = document.getElementById('exB'), inC = document.getElementById('exC');
  var INPUTS = [inA, inB, inC];
  function applyPreset(parts) {
    inA.value = (parts[0] || '').trim(); inB.value = (parts[1] || '').trim(); inC.value = (parts[2] || '').trim();
  }

  /* The claims. A name here is a NAME -- "commutative" is what we call an
     operation that does not care about order -- and naming one is not the same
     as it being true of a given operation. Which of these are laws is decided
     below by arithmetic, not by this list. */
  var LAWS = [
    { pat: 'commutative', op: 'addition',
      text: function (A, B, C) { return A + ' + ' + B + ' = ' + B + ' + ' + A; },
      l: function (a, b, c) { return Radd(a, b); }, r: function (a, b, c) { return Radd(b, a); } },
    { pat: 'commutative', op: 'multiplication',
      text: function (A, B, C) { return A + ' * ' + B + ' = ' + B + ' * ' + A; },
      l: function (a, b, c) { return Rmul(a, b); }, r: function (a, b, c) { return Rmul(b, a); } },
    { pat: 'commutative', op: 'subtraction',
      text: function (A, B, C) { return A + ' - ' + B + ' = ' + B + ' - ' + A; },
      l: function (a, b, c) { return Rsub(a, b); }, r: function (a, b, c) { return Rsub(b, a); } },
    { pat: 'commutative', op: 'division',
      text: function (A, B, C) { return A + ' / ' + B + ' = ' + B + ' / ' + A; },
      l: function (a, b, c) { return Rdiv(a, b); }, r: function (a, b, c) { return Rdiv(b, a); } },
    { pat: 'associative', op: 'addition',
      text: function (A, B, C) { return '(' + A + ' + ' + B + ') + ' + C + ' = ' + A + ' + (' + B + ' + ' + C + ')'; },
      l: function (a, b, c) { return Radd(Radd(a, b), c); }, r: function (a, b, c) { return Radd(a, Radd(b, c)); } },
    { pat: 'associative', op: 'multiplication',
      text: function (A, B, C) { return '(' + A + ' * ' + B + ') * ' + C + ' = ' + A + ' * (' + B + ' * ' + C + ')'; },
      l: function (a, b, c) { return Rmul(Rmul(a, b), c); }, r: function (a, b, c) { return Rmul(a, Rmul(b, c)); } },
    { pat: 'associative', op: 'subtraction',
      text: function (A, B, C) { return '(' + A + ' - ' + B + ') - ' + C + ' = ' + A + ' - (' + B + ' - ' + C + ')'; },
      l: function (a, b, c) { return Rsub(Rsub(a, b), c); }, r: function (a, b, c) { return Rsub(a, Rsub(b, c)); } },
    { pat: 'associative', op: 'division',
      text: function (A, B, C) { return '(' + A + ' / ' + B + ') / ' + C + ' = ' + A + ' / (' + B + ' / ' + C + ')'; },
      l: function (a, b, c) { return Rdiv(Rdiv(a, b), c); }, r: function (a, b, c) { return Rdiv(a, Rdiv(b, c)); } },
    { pat: 'distributive', op: 'multiplication over addition',
      text: function (A, B, C) { return A + '(' + B + ' + ' + C + ') = ' + A + ' * ' + B + ' + ' + A + ' * ' + C; },
      l: function (a, b, c) { return Rmul(a, Radd(b, c)); }, r: function (a, b, c) { return Radd(Rmul(a, b), Rmul(a, c)); } },
    { pat: 'distributive', op: 'multiplication over multiplication',
      text: function (A, B, C) { return A + '(' + B + ' * ' + C + ') = ' + A + ' * ' + B + ' * ' + A + ' * ' + C; },
      l: function (a, b, c) { return Rmul(a, Rmul(b, c)); }, r: function (a, b, c) { return Rmul(Rmul(a, b), Rmul(a, c)); } },
    { pat: 'distributive', op: 'a minus sign over a sum',
      text: function (A, B, C) { return '-(' + B + ' + ' + C + ') = -' + B + ' - ' + C; },
      l: function (a, b, c) { return Rneg(Radd(b, c)); }, r: function (a, b, c) { return Rsub(Rneg(b), c); } },
    { pat: 'distributive', op: 'a minus sign over a difference',
      text: function (A, B, C) { return '-(' + B + ' - ' + C + ') = -' + B + ' - ' + C; },
      l: function (a, b, c) { return Rneg(Rsub(b, c)); }, r: function (a, b, c) { return Rsub(Rneg(b), c); } },
    { pat: 'identity', op: 'addition',
      text: function (A, B, C) { return A + ' + 0 = ' + A; },
      l: function (a, b, c) { return Radd(a, R0); }, r: function (a, b, c) { return a; } },
    { pat: 'identity', op: 'multiplication',
      text: function (A, B, C) { return A + ' * 1 = ' + A; },
      l: function (a, b, c) { return Rmul(a, R1); }, r: function (a, b, c) { return a; } },
    { pat: 'inverse', op: 'addition',
      text: function (A, B, C, a) { return A + ' + ' + Rterm(Rneg(a)) + ' = 0'; },
      l: function (a, b, c) { return Radd(a, Rneg(a)); }, r: function (a, b, c) { return R0; } },
    { pat: 'inverse', op: 'multiplication',
      text: function (A, B, C) { return A + ' * (1 / ' + A + ') = 1'; },
      l: function (a, b, c) { return Rmul(a, Rinv(a)); }, r: function (a, b, c) { return R1; } }
  ];

  /* Eight values, every ordered triple: 512 tests per claim. Small and ugly on
     purpose -- zero, one, a negative and a fraction are where claims die. */
  var GRID = ['-2', '-1', '-1/2', '0', '1/2', '1', '2', '3'].map(Rparse);
  function counterexample(law) {
    var skipped = 0;
    for (var i = 0; i < GRID.length; i += 1) {
      for (var j = 0; j < GRID.length; j += 1) {
        for (var k = 0; k < GRID.length; k += 1) {
          var l, r;
          /* A triple where the claim is undefined is not a counterexample to it.
             They are counted rather than quietly dropped, because "no
             counterexample" means less when a tenth of the tests never ran. */
          try { l = law.l(GRID[i], GRID[j], GRID[k]); r = law.r(GRID[i], GRID[j], GRID[k]); }
          catch (err) { skipped += 1; continue; }
          if (!Requ(l, r)) return { found: [GRID[i], GRID[j], GRID[k]], skipped: skipped };
        }
      }
    }
    return { found: null, skipped: skipped };
  }

  function redraw() {
    var a = Rread(inA.value.trim()), b = Rread(inB.value.trim()), c = Rread(inC.value.trim());
    if (a === null || b === null || c === null) {
      fail('Each of a, b and c has to be a number.',
        'Whole numbers such as 4, or fractions such as -3/2 and 1/2.');
      return;
    }
    var A = Rterm(a), B = Rterm(b), C = Rterm(c);
    subOut.textContent = 'a = ' + Rtext(a) + ', b = ' + Rtext(b) + ', c = ' + Rtext(c);

    var rows = [tr([th('pattern'), th('applied to'), th('the claim on your numbers'), th('left'), th('right'), th('here'), th('in general')])];
    var held = 0, general = 0, undef = 0;
    LAWS.forEach(function (law) {
      var l = null, r = null, why = null;
      try { l = law.l(a, b, c); r = law.r(a, b, c); }
      catch (err) { why = err.message; }
      var same = l !== null && r !== null && Requ(l, r);
      if (same) held += 1;
      if (why) undef += 1;
      var search = counterexample(law), cx = search.found;
      if (!cx) general += 1;
      var verdict = why ? td('undefined') : td(same ? 'true' : 'false', same ? 't' : 'f');
      var tested = 512 - search.skipped;
      var inGeneral = cx
        ? tdl('<span class="chip no">fails at a = ' + Rtext(cx[0]) + ', b = ' + Rtext(cx[1]) + ', c = ' + Rtext(cx[2]) + '</span>')
        : tdl('<span class="chip ok">nothing found in ' + tested + ' triples</span>'
            + (search.skipped ? '<span class="chip">' + search.skipped + ' undefined</span>' : ''));
      rows.push(tr([
        td(law.pat), tdl(law.op), tdl(law.text(A, B, C, a, b, c)),
        td(why ? tone('undefined', 'red') : Rtext(l)),
        td(why ? tone('undefined', 'red') : Rtext(r)),
        verdict, inGeneral
      ], why ? '' : (same === (cx === null) ? '' : 'focus')));
    });

    stage.innerHTML = table('your three numbers', [
      step('a', Rtext(a)), step('b', Rtext(b)), step('c', Rtext(c)),
      step('claims that hold on them', held + ' of ' + LAWS.length),
      step('claims with no counterexample anywhere in the search', general + ' of ' + LAWS.length),
    ]);
    work.innerHTML = table('Every claim, checked on your numbers and then searched', rows);
    kpis(String(LAWS.length), String(held), String(LAWS.length - general));

    var misleading = held - general;
    var msg = '<strong>' + held + ' of the ' + LAWS.length + ' claims are true for a = ' + Rtext(a)
      + ', b = ' + Rtext(b) + ', c = ' + Rtext(c) + ', and ' + general + ' of them survived a search '
      + 'over 512 triples.</strong> ';
    if (misleading > 0) {
      msg += 'The ' + misleading + ' row' + (misleading === 1 ? '' : 's') + ' in between '
        + (misleading === 1 ? 'is' : 'are') + ' worth staring at: they are true for '
        + 'your three numbers and false in general, and the counterexample in the last column was '
        + 'found by testing, not looked up. One example is not a proof, and this is what that '
        + 'sentence looks like.';
    } else {
      msg += 'No claim here is true for your numbers and false elsewhere, so this triple does not '
        + 'flatter any of the false ones. Try a = 4, b = 4, c = 4, where subtraction looks '
        + 'commutative, or a = 1, b = 1, c = 1, where almost everything looks true.';
    }
    if (undef) {
      msg += ' ' + undef + ' claim' + (undef === 1 ? ' is' : 's are') + ' undefined for these '
        + 'numbers rather than false &mdash; dividing by zero is not a wrong answer, it is not an '
        + 'answer.';
    }
    msg += ' A search finding nothing is evidence and not proof: the claims that survive it are the '
      + 'field axioms and their consequences, and those are proved once, for every number at once.';
    status.innerHTML = msg;
  }
"""

# Substituting a value into a tree and evaluating a collected polynomial are two
# different computations, and several modes below run both and compare them.
EXPR_SHARED_JS = r"""
  function Esubst(node, env) {
    if (node.k === 'var') return env[node.v] === undefined ? node : numnode(env[node.v], true);
    if (node.k === 'num') return node;
    if (node.k === 'neg' || node.k === 'fn') return { k: node.k, v: node.v, a: Esubst(node.a, env) };
    return { k: node.k, v: node.v, a: Esubst(node.a, env), b: Esubst(node.b, env) };
  }
  function Meval(list, env) {
    var acc = R0;
    list.forEach(function (t) {
      var term = t.c, k;
      for (k in t.v) if (t.v.hasOwnProperty(k)) {
        if (env[k] === undefined) throw new Error('no value was given for ' + k);
        term = Rmul(term, Rpow(env[k], t.v[k]));
      }
      acc = Radd(acc, term);
    });
    return acc;
  }
  /* Substitute, then reduce the tree operation by operation. Returns null where
     the arithmetic has no value (a division by zero), never throws. */
  function treeValue(tree, env) {
    var q = Equeue(Esubst(tree, env));
    return q.value ? q.value : null;
  }
"""

EXPR_BODY["terms"] = r"""
  var input = document.getElementById('exExpr');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = src || 'nothing typed yet';
    if (!src) { fail('Type an expression.', 'The box is empty, so there are no terms to find.'); return; }
    var tree;
    try { tree = Eparse(src); }
    catch (err) { fail('That expression does not parse.', esc(err.message) + '.'); return; }
    var written = Esplit(tree, 1, []);
    var expanded;
    try { expanded = Mof(tree); }
    catch (err) { fail('I can read that, but not take it apart into terms.', esc(err.message) + '.'); return; }

    var rows = [tr([th('#'), th('the term, as written'), th('factors'), th('coefficient'), th('variable part'), th('degree')])];
    var mixed = 0;
    written.forEach(function (item, i) {
      var shown = (item.sign < 0 ? '-' : '') + Eshow(item.node, null, '');
      var factors = Efactors(item.node, []).map(function (f) { return Eshow(f, null, ''); });
      var mono = null, why = null;
      try {
        mono = Mof(item.node);
        if (item.sign < 0) mono = Mneg(mono);
      } catch (err) { why = err.message; }
      if (mono && mono.length > 1) { mixed += 1; }
      var coef, vpart, deg;
      if (why) { coef = tone(esc(why), 'red'); vpart = '&mdash;'; deg = '&mdash;'; }
      else if (!mono.length) { coef = '0'; vpart = 'none'; deg = '&mdash;'; }
      else if (mono.length > 1) {
        coef = tone('not one term yet', 'purple');
        vpart = 'expands to ' + mono.length + ' terms: ' + Mtext(mono);
        deg = String(Vdeg(mono[0].v));
      } else {
        coef = Rtext(mono[0].c);
        vpart = Vtext(mono[0].v) || 'none: this is the constant term';
        deg = String(Vdeg(mono[0].v));
      }
      rows.push(tr([td(String(i + 1)), tdl(shown), tdl(String(factors.length) + ': ' + factors.join(' * ')),
        td(coef), tdl(vpart), td(deg)], i === 0 ? 'focus' : ''));
    });

    var degree = 0, constant = R0;
    expanded.forEach(function (t) {
      degree = Math.max(degree, Vdeg(t.v));
      if (Vdeg(t.v) === 0) constant = t.c;
    });
    var after = [tr([th('after expanding'), th('terms'), th('degree'), th('constant term')])];
    after.push(tr([tdl(Mtext(expanded)), td(String(expanded.length)), td(String(degree)), td(Rtext(constant))]));

    stage.innerHTML = table('the expression, split at its own plus and minus signs', [
      step('as written', esc(src)),
      step('terms as written', String(written.length)),
      step('expanded', Mtext(expanded)),
      step('terms after expanding', String(expanded.length)),
    ]);
    work.innerHTML = table('Every term as it stands in the expression', rows)
      + table('The same expression once every bracket is multiplied out', after);
    kpis(String(written.length), String(expanded.length), String(degree));

    var msg = '<strong>As written this expression has ' + written.length + ' term'
      + (written.length === 1 ? '' : 's') + ', and expanded it has ' + expanded.length + '.</strong> ';
    if (mixed) {
      msg += 'They differ because a term such as ' + esc(src) + ' is a PRODUCT: a bracket counts as '
        + 'one factor of one term until it is multiplied out. Counting the plus signs you can see '
        + 'is not the same as counting terms, and this is the case where that goes wrong.';
    } else if (written.length !== expanded.length) {
      msg += 'They differ because like terms cancelled or combined when the expression was '
        + 'collected: nothing was lost, two terms became one.';
    } else {
      msg += 'Terms are separated by + and -, and the sign in front belongs to the term: in '
        + Mtext(expanded) + ' the coefficients are ' + expanded.map(function (t) { return Rtext(t.c); }).join(', ')
        + ', signs included. Degree ' + degree + ' is the largest total degree of any term.';
    }
    msg += ' Factors are what a term is multiplied FROM; terms are what an expression is added FROM. '
      + 'The factor column above is the same term read the other way.';
    status.innerHTML = msg;
  }
"""

EXPR_BODY["distribute"] = r"""
  var inL = document.getElementById('exLeft'), inR = document.getElementById('exRight');
  var INPUTS = [inL, inR];
  function applyPreset(parts) { inL.value = (parts[0] || '').trim(); inR.value = (parts[1] || '').trim(); }

  function redraw() {
    var ls = inL.value.trim(), rs = inR.value.trim();
    subOut.textContent = '(' + (ls || '?') + ')(' + (rs || '?') + ')';
    if (!ls || !rs) { fail('Both factors are needed.', 'Put an expression in each box; a single number is a perfectly good factor.'); return; }
    var lt, rt, A, B;
    try { lt = Eparse(ls); rt = Eparse(rs); }
    catch (err) { fail('One of the factors does not parse.', esc(err.message) + '.'); return; }
    try { A = Mof(lt); B = Mof(rt); }
    catch (err) { fail('I can read the factors but not multiply them out.', esc(err.message) + '.'); return; }
    if (!A.length || !B.length) {
      var which = !A.length ? 'first' : 'second';
      stage.innerHTML = table('a factor of zero', [step(which + ' factor', '0'), step('product', '0')]);
      work.innerHTML = table('Multiplying by zero', [
        step('the ' + which + ' factor is 0', 'every product formed below would be 0'),
        step('the whole product', '0'),
      ]);
      kpis('0', '0', '0');
      status.innerHTML = '<strong>One factor is zero, so the product is zero.</strong> There is no '
        + 'grid to build: distributing zero over a sum gives a sum of zeros. That is the zero '
        + 'product property read forwards, and the factoring lesson reads it backwards.';
      return;
    }

    /* The grid: every term of the first factor against every term of the
       second. Nothing is skipped and nothing is combined yet, because the two
       mistakes this lesson exists to stop are missing a product and collecting
       terms that are not like. */
    var headerCells = [rowhead('&times;')];
    B.forEach(function (t) { headerCells.push(th(Mtermtext(t))); });
    var grid = [tr(headerCells)];
    var products = [];
    A.forEach(function (s) {
      var cells = [rowhead(Mtermtext(s))];
      B.forEach(function (t) {
        var p = { c: Rmul(s.c, t.c), v: Vmul(s.v, t.v) };
        products.push(p);
        cells.push(td(Mtermtext(p), 'on'));
      });
      grid.push(tr(cells));
    });

    var collected = Mnorm(products);
    var groups = {}, order = [];
    products.forEach(function (p) {
      var key = Vkey(p.v);
      if (!groups[key]) { groups[key] = []; order.push(key); }
      groups[key].push(p);
    });
    var collectRows = [tr([th('variable part'), th('the products with it'), th('coefficients added'), th('one term')])];
    order.forEach(function (key) {
      var list = groups[key];
      var sum = R0;
      list.forEach(function (p) { sum = Radd(sum, p.c); });
      collectRows.push(tr([
        td(Vtext(list[0].v) || 'constant'),
        tdl(list.map(function (p) { return Mtermtext(p); }).join('  ')),
        tdl(list.map(function (p) { return Rtext(p.c); }).join(' + ') + ' = ' + Rtext(sum)),
        td(Rzero(sum) ? '0, it cancels' : Mtermtext({ c: sum, v: list[0].v })),
      ], list.length > 1 ? 'focus' : ''));
    });

    /* An independent check. The product was built by multiplying monomials; this
       evaluates the ORIGINAL two factors at a point and multiplies the two
       numbers. Different code, same number, or the grid above is wrong. */
    var letters = Evars(lt, Evars(rt, []));
    var env = {}, at = [];
    letters.forEach(function (name, i) {
      env[name] = R(BigInt(i + 2));
      at.push(name + ' = ' + Rtext(env[name]));
    });
    var checkRows = [tr([th('checked at'), th('first factor'), th('second factor'), th('their product'), th('the expansion'), th('same?')])];
    var lv = treeValue(lt, env), rv = treeValue(rt, env), ev = null, ok = false;
    try { ev = Meval(collected, env); } catch (err) { ev = null; }
    if (lv && rv && ev) {
      var direct = Rmul(lv, rv);
      ok = Requ(direct, ev);
      checkRows.push(tr([tdl(at.length ? at.join(', ') : 'no letters to give values to'),
        td(Rtext(lv)), td(Rtext(rv)), td(Rtext(direct)), td(Rtext(ev)),
        td(ok ? 'yes' : 'no', ok ? 't' : 'f')]));
    } else {
      checkRows.push(tr([tdl('the check could not be run on these factors'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;'), td('&mdash;')]));
    }

    stage.innerHTML = table('the product, before and after collecting', [
      step('first factor', Mtext(A) + '  (' + A.length + ' term' + (A.length === 1 ? '' : 's') + ')'),
      step('second factor', Mtext(B) + '  (' + B.length + ' term' + (B.length === 1 ? '' : 's') + ')'),
      step('products formed', String(A.length * B.length)),
      step('the expansion', Mtext(collected)),
    ]);
    work.innerHTML = table('Each term of the first factor times each term of the second', grid)
      + table('Collecting: only terms with an identical variable part may be added', collectRows)
      + table('An independent check: evaluate the factors, then multiply the numbers', checkRows);
    kpis(String(A.length * B.length), String(products.length), String(collected.length));

    var msg = '<strong>' + A.length + ' term' + (A.length === 1 ? '' : 's') + ' times ' + B.length
      + ' term' + (B.length === 1 ? '' : 's') + ' makes ' + (A.length * B.length)
      + ' product' + (A.length * B.length === 1 ? '' : 's') + ', which collect to ' + collected.length
      + '.</strong> Distributing is not a special rule for brackets: it is the statement that a sum '
      + 'multiplied by something is the sum of the pieces multiplied by it, and the grid above is '
      + 'that statement laid out so no pair is missed. ';
    if (Rsign(A[0].c) < 0 || Rsign(B[0].c) < 0) {
      msg += 'One of the factors leads with a minus, and the sign travels into every product it '
        + 'touches &mdash; that is where this goes wrong most often. ';
    }
    msg += ok
      ? 'The check agrees: the factors evaluated separately and multiplied give the same number as '
        + 'the expansion evaluated directly, so no product was dropped and nothing was collected '
        + 'that should not have been.'
      : 'The independent check did not run on these factors, so treat the expansion above as the '
        + 'only computation here.';
    status.innerHTML = msg;
  }
"""

EXPR_BODY["like"] = r"""
  var input = document.getElementById('exExpr');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = src || 'nothing typed yet';
    if (!src) { fail('Type an expression with several terms.', 'The box is empty, so there is nothing to group.'); return; }
    var tree;
    try { tree = Eparse(src); }
    catch (err) { fail('That expression does not parse.', esc(err.message) + '.'); return; }
    var written = Esplit(tree, 1, []);
    var terms = [], bad = null;
    written.forEach(function (item) {
      if (bad) return;
      try {
        var mono = Mof(item.node);
        if (item.sign < 0) mono = Mneg(mono);
        if (mono.length > 1) { bad = 'the term ' + Eshow(item.node, null, '') + ' is a product of sums; multiply it out first, which is the distributing mode'; return; }
        terms.push({ shown: (item.sign < 0 ? '-' : '') + Eshow(item.node, null, ''), mono: mono.length ? mono[0] : { c: R0, v: {} } });
      } catch (err) { bad = err.message; }
    });
    if (bad) { fail('I cannot group these terms yet.', esc(bad) + '.'); return; }

    /* Grouping is done on the variable part alone, with the letters sorted, so
       3xy and 2yx land in the same group without a rule about writing order. */
    var groups = {}, order = [];
    terms.forEach(function (t, i) {
      var key = Vkey(t.mono.v);
      if (!groups[key]) { groups[key] = { list: [], v: t.mono.v, index: order.length + 1 }; order.push(key); }
      groups[key].list.push(t);
      t.group = groups[key].index;
    });

    var rows = [tr([th('#'), th('term'), th('coefficient'), th('variable part'), th('group'), th('like anything else?')])];
    terms.forEach(function (t, i) {
      var key = Vkey(t.mono.v), size = groups[key].list.length;
      rows.push(tr([
        td(String(i + 1)), tdl(t.shown), td(Rtext(t.mono.c)),
        td(Vtext(t.mono.v) || 'none (a constant)'), td(String(t.group), size > 1 ? 'on' : ''),
        tdl(size > 1 ? '<span class="chip hi">like ' + (size - 1) + ' other' + (size === 2 ? '' : 's') + '</span>'
                     : '<span class="chip">on its own</span>'),
      ]));
    });

    var groupRows = [tr([th('group'), th('variable part'), th('coefficients'), th('sum'), th('the single term it becomes')])];
    order.forEach(function (key) {
      var g = groups[key], sum = R0;
      g.list.forEach(function (t) { sum = Radd(sum, t.mono.c); });
      groupRows.push(tr([
        td(String(g.index)), td(Vtext(g.v) || 'constant'),
        tdl(g.list.map(function (t) { return Rtext(t.mono.c); }).join(' + ')),
        td(Rtext(sum)),
        tdl(Rzero(sum) ? tone('0: this group cancels completely', 'red') : Mtermtext({ c: sum, v: g.v })),
      ], g.list.length > 1 ? 'focus' : ''));
    });

    var collected = Mnorm(terms.map(function (t) { return t.mono; }));
    var combinable = order.filter(function (key) { return groups[key].list.length > 1; }).length;

    stage.innerHTML = table('terms grouped by their variable part', [
      step('as written', esc(src)),
      step('terms', String(terms.length)),
      step('groups', String(order.length)),
      step('collected', Mtext(collected)),
    ]);
    work.innerHTML = table('Every term, with the part that decides what it is like', rows)
      + table('One group, one term: add the coefficients and keep the variable part', groupRows);
    kpis(String(terms.length), String(order.length), String(collected.length));

    var msg = '<strong>' + terms.length + ' terms fall into ' + order.length + ' group'
      + (order.length === 1 ? '' : 's') + ', and collecting gives ' + Mtext(collected) + '.</strong> ';
    if (!combinable) {
      msg += 'No two of these terms are like, so nothing can be added: this expression is already '
        + 'as short as it goes. "It looks similar" is not the test &mdash; the variable parts have '
        + 'to be identical, exponents included, and here they all differ.';
    } else {
      msg += 'Only the coefficients are added; the variable part is carried along unchanged, '
        + 'because 3x + 2x is (3 + 2) copies of the same x and nothing has been done to x itself. ';
    }
    /* The pair that catches everybody: two groups built from the same letters
       whose exponents differ. Found rather than assumed, so the sentence only
       appears when the expression actually contains such a pair. */
    function lettersOf(v) {
      var ks = [], k;
      for (k in v) if (v.hasOwnProperty(k) && v[k]) ks.push(k);
      return ks.sort().join('');
    }
    var pair = null;
    for (var i = 0; i < order.length && !pair; i += 1) {
      for (var j = i + 1; j < order.length && !pair; j += 1) {
        var vi = groups[order[i]].v, vj = groups[order[j]].v;
        if (lettersOf(vi) && lettersOf(vi) === lettersOf(vj)) pair = [Vtext(vi), Vtext(vj)];
      }
    }
    if (pair) {
      msg += ' Notice ' + pair[0] + ' and ' + pair[1] + ': the same letters, different exponents, '
        + 'and so different variable parts. Nothing lets those two meet, however similar they look.';
    }
    status.innerHTML = msg;
  }
"""

EXPR_BODY["evaluate"] = r"""
  var input = document.getElementById('exExpr'), vals = document.getElementById('exVals');
  var INPUTS = [input, vals];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); vals.value = (parts[1] || '').trim(); }

  function parseVals(text) {
    var out = {}, count = 0, parts = String(text).split(',');
    for (var i = 0; i < parts.length; i += 1) {
      var s = parts[i].trim();
      if (!s) continue;
      var m = /^([A-Za-z])\s*=\s*(.+)$/.exec(s);
      if (!m) throw new Error('"' + esc(s) + '" is not of the form  x = -3');
      var r = Rread(m[2].trim());
      if (r === null) throw new Error('"' + esc(m[2].trim()) + '" is not a number I can read exactly');
      out[m[1]] = r; count += 1;
    }
    return { env: out, count: count };
  }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = (src || '?') + '  at  ' + (vals.value.trim() || '?');
    if (!src) { fail('Type an expression.', 'The box is empty, so there is nothing to substitute into.'); return; }
    var tree;
    try { tree = Eparse(src); }
    catch (err) { fail('That expression does not parse.', esc(err.message) + '.'); return; }
    var got;
    try { got = parseVals(vals.value); }
    catch (err) { fail('I cannot read the values.', esc(err.message) + '.'); return; }
    var letters = Evars(tree, []);
    var missing = letters.filter(function (n) { return got.env[n] === undefined; });
    if (missing.length) {
      fail('No value was given for ' + missing.join(', ') + '.',
        'The expression uses ' + letters.join(', ') + ', so every one of those letters needs a value '
        + 'before anything can be worked out.');
      return;
    }

    /* Two substitutions of the same values into the same expression: one that
       brackets each value, and one that drops the brackets the way a hurried
       hand does. Both are then evaluated by the same machinery. */
    var bracketed = Esubst(tree, got.env);
    var withText = Eshow(bracketed, null, '');
    var plain = src.replace(/[A-Za-z]/g, function (ch) {
      return got.env[ch] === undefined ? ch : Rtext(got.env[ch]);
    });
    var qb = Equeue(bracketed);
    var plainValue = null, plainWhy = null, plainGroups = plain;
    try {
      var pt = Eparse(plain);
      plainGroups = Eshow(pt, null, '');
      var qp = Equeue(pt);
      if (qp.value) plainValue = qp.value; else plainWhy = qp.error || 'it does not reduce to a number';
    } catch (err) { plainWhy = err.message; }

    var subRows = [tr([th('letter'), th('value'), th('every occurrence becomes')])];
    letters.forEach(function (name) {
      subRows.push(tr([td(name), td(Rtext(got.env[name])), tdl(Rterm(got.env[name]))]));
    });
    subRows.push(step('with brackets', tone(withText, 'cyan')));
    subRows.push(step('brackets dropped', tone(esc(plain), 'red')));
    subRows.push(step('which reads as', plainGroups));

    var qRows = [tr([th('#'), th('rule'), th('operation'), th('what is left')])];
    qb.steps.forEach(function (s, i) {
      qRows.push(tr([td(String(i + 1)), tdl(s.rule), td(s.did + ' = ' + Rtext(s.value)), tdl(s.after)], i === 0 ? 'focus' : ''));
    });
    if (qb.error) {
      qRows.push(tr([td(String(qb.steps.length + 1)), tdl(tone('cannot be done', 'red')), td(qb.stuck), tdl(esc(qb.error))], 'focus'));
    }

    stage.innerHTML = table('the same values, substituted twice', [
      step('expression', esc(src)),
      step('values', letters.map(function (n) { return n + ' = ' + Rtext(got.env[n]); }).join(',  ') || 'none needed'),
      step('with brackets', withText + ' = ' + (qb.value ? Rtext(qb.value) : 'no value')),
      step('without brackets', esc(plain) + ' = ' + (plainValue ? Rtext(plainValue) : 'no value')),
    ]);
    work.innerHTML = table('Substitution, done both ways', subRows)
      + table('Evaluating the bracketed form, one operation at a time', qRows);
    kpis(String(letters.length), qb.value ? Rtext(qb.value) : 'undefined', plainValue ? Rtext(plainValue) : 'undefined');

    var msg;
    if (!qb.value) {
      msg = '<strong>' + esc(src) + ' has no value at these numbers.</strong> The queue stopped: '
        + esc(qb.error || 'an operation could not be carried out')
        + '. An expression is not a function of every input: this one is undefined here, and '
        + '"undefined" is the answer rather than a failure to find one.';
    } else if (plainValue && Requ(plainValue, qb.value)) {
      msg = '<strong>' + withText + ' = ' + Rtext(qb.value) + ', and dropping the brackets gives the '
        + 'same answer this time.</strong> That is luck: with these values nothing in the expression '
        + 'reaches across a bracket. Try x = -3 in x^2, where -3^2 and (-3)^2 are different numbers.';
    } else {
      msg = '<strong>' + withText + ' = ' + Rtext(qb.value) + ', but ' + esc(plain) + ' = '
        + (plainValue ? Rtext(plainValue) : 'nothing at all') + '.</strong> The two strings differ by '
        + 'brackets alone, and they group as ' + withText + ' against ' + plainGroups + '. Substituting '
        + 'a negative value or a fraction without bracketing it changes which symbols the power and '
        + 'the division are attached to, which is why the brackets are part of the substitution and '
        + 'not decoration on it.';
    }
    if (qb.value && !Rint(qb.value)) {
      msg += ' The value ' + Rtext(qb.value) + ' is exact: ' + Rdec(qb.value, 6) + ' is a rounding of it.';
    }
    status.innerHTML = msg;
  }
"""

EXPR_BODY["translate"] = r"""
  var input = document.getElementById('exExpr');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[2] || '').trim(); }

  /* Eight values of n, chosen to include the value at which each phrase's two
     readings happen to agree -- n = 5 for one preset, n = 2 for another,
     n = -12 for two more. That value is why "I checked it with a number" is not
     a method. Which value it is for a given phrase is not written down here:
     the lab solves for it below, from the two expressions. */
  var TESTS = ['-12', '-3', '-1', '0', '1/2', '2', '3', '5'].map(Rparse);

  function valueOf(src, n) {
    var tree;
    try { tree = Eparse(src); } catch (err) { return { v: null, why: err.message }; }
    var env = { n: n };
    var q = Equeue(Esubst(tree, env));
    if (q.value) return { v: q.value, why: null };
    return { v: null, why: q.error || 'it does not reduce to a number' };
  }

  function redraw() {
    var parts = preset.value.split('|');
    var phrase = parts[0], intended = parts[1] || '', tempting = parts[2] || '';
    var mine = input.value.trim();
    subOut.textContent = phrase;
    if (!mine) { fail('Type an expression in n.', 'The phrase is "' + esc(phrase) + '", and the box is empty.'); return; }
    try { Eparse(mine); }
    catch (err) { fail('Your expression does not parse.', esc(err.message) + '.'); return; }

    var rows = [tr([th('n'), th('the phrase: ' + esc(intended)), th('yours: ' + esc(mine)), th('the usual misreading: ' + esc(tempting)), th('yours agrees?')])];
    var agree = 0, defined = 0;
    TESTS.forEach(function (n) {
      var a = valueOf(intended, n), b = valueOf(mine, n), c = valueOf(tempting, n);
      var same = a.v && b.v && Requ(a.v, b.v);
      if (a.v && b.v) defined += 1;
      if (same) agree += 1;
      rows.push(tr([
        td(Rtext(n)),
        td(a.v ? Rtext(a.v) : tone('undefined', 'red')),
        td(b.v ? Rtext(b.v) : tone('undefined', 'red')),
        td(c.v ? Rtext(c.v) : tone('undefined', 'red')),
        td(same ? 'yes' : 'no', same ? 't' : 'f'),
      ], same ? '' : 'focus'));
    });

    /* The test values are evidence. When both readings are polynomials the lab
       can do better than evidence: it compares them coefficient by coefficient,
       and it solves for the values of n at which the misreading passes. */
    var exact = null, exactWhy = null;
    try {
      var pa = Mof(Eparse(intended)), pb = Mof(Eparse(mine));
      exact = Mequ(pa, pb);
      exactWhy = 'expanded, the phrase is ' + Mtext(pa) + ' and yours is ' + Mtext(pb);
    } catch (err) { exactWhy = 'one of them is not a polynomial (' + esc(err.message) + '), so the ' + TESTS.length + ' test values are all the evidence there is'; }

    function agreesWhere(one, other) {
      var d;
      try { d = Msub(Mof(Eparse(one)), Mof(Eparse(other))); }
      catch (err) { return null; }
      if (!d.length) return 'everywhere: these are the same expression written two ways';
      var deg = 0;
      d.forEach(function (t) { deg = Math.max(deg, Vdeg(t.v)); });
      if (deg === 0) return 'nowhere: the two readings differ by ' + Rtext(d[0].c) + ' at every value of n';
      if (deg === 1 && d.length <= 2) {
        var a = R0, b = R0;
        d.forEach(function (t) { if (Vdeg(t.v) === 1) a = t.c; else b = t.c; });
        return 'at n = ' + Rtext(Rdiv(Rneg(b), a)) + ' and nowhere else, since they differ by ' + Mtext(d);
      }
      return 'exactly where ' + Mtext(d) + ' = 0';
    }
    var whereTempting = agreesWhere(intended, tempting);

    var tempSame = 0;
    TESTS.forEach(function (n) {
      var a = valueOf(intended, n), c = valueOf(tempting, n);
      if (a.v && c.v && Requ(a.v, c.v)) tempSame += 1;
    });

    stage.innerHTML = table('one phrase, two readings', [
      step('the phrase', esc(phrase)),
      step('what it says', esc(intended)),
      step('what it is usually read as', esc(tempting)),
      step('yours', esc(mine)),
      step('agreement with the phrase', agree + ' of ' + TESTS.length + ' test values'),
    ]);
    work.innerHTML = table('Both readings, evaluated at ' + TESTS.length + ' values of n', rows)
      + table('The exact comparison', [
        step('yours against the phrase', exact === null ? 'not available: ' + exactWhy
          : (exact ? '<span class="chip ok">identical as expressions</span> &mdash; ' + exactWhy
                   : '<span class="chip no">different expressions</span> &mdash; ' + exactWhy)),
        step('the usual misreading against the phrase', tempSame + ' of ' + TESTS.length
          + ' test values agree'),
        step('and it agrees with the phrase', whereTempting || 'only at the test values above'),
      ]);
    kpis(String(TESTS.length), agree + '/' + TESTS.length,
      exact === null ? (agree === TESTS.length ? 'agrees' : 'differs') : (exact ? 'the same' : 'different'));

    var msg;
    if (exact === true || (exact === null && agree === TESTS.length)) {
      msg = '<strong>Your expression says what the phrase says.</strong> ';
      msg += exact === true
        ? 'That is not a matter of the seven values above: expanded, both are ' + Mtext(Mof(Eparse(mine)))
          + ', so they agree at every number there is.'
        : 'They agree at all seven test values, which is strong evidence but not a proof here.';
    } else {
      msg = '<strong>Your expression is not what the phrase says.</strong> It agrees at ' + agree
        + ' of the ' + TESTS.length + ' test values and differs at the rest. ';
    }
    msg += ' The last column is the reading most people give this phrase. It matches the phrase '
      + (whereTempting ? whereTempting : 'at ' + tempSame + ' of the ' + TESTS.length + ' test values')
      + (tempSame === 1 ? ', and one of the test values above is exactly that number: check your '
          + 'algebra against a single value of n and that is the value you can be unlucky enough '
          + 'to pick.' : '.')
      + ' Word order in English is not the order of operations. A phrase usually names the last '
      + 'thing you do first &mdash; "twice the SUM of n and 3" &mdash; and the bracket is where '
      + 'that reversal shows up in the algebra.';
    status.innerHTML = msg;
  }
"""

# One wiring for every mode: the preset fills the boxes, the boxes redraw, and
# the first preset is applied before the first paint so the page never opens on
# an empty widget.
EXPR_WIRE = r"""
  preset.addEventListener('change', function () { applyPreset(preset.value.split('|')); redraw(); });
  INPUTS.forEach(function (el) { el.addEventListener('input', redraw); });
  applyPreset(preset.value.split('|'));
  redraw();
  window.redrawLab = redraw;
"""

EXPR_SELECT_LABEL = {
    "order": "Expression",
    "property": "Your three numbers",
    "terms": "Expression",
    "distribute": "Product",
    "like": "Expression",
    "evaluate": "Expression and values",
    "translate": "Phrase",
}


def _attr(text):
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def _jsstr(text):
    """A Python string as a JS string literal that cannot close the script tag."""
    return json.dumps(text).replace("</", "<\\/")


def _options(presets):
    return "".join(
        '<option value="%s">%s</option>' % (_attr(value), label)
        for label, value in presets
    )


def _fields(spec, first):
    parts = first.split("|")
    out = []
    for i, (fid, label) in enumerate(spec):
        value = parts[i] if i < len(parts) else ""
        out.append(
            '        <div class="field">\n'
            '          <label for="%s">%s</label>\n'
            '          <input id="%s" type="text" value="%s" inputmode="text" autocomplete="off">\n'
            "        </div>\n" % (fid, label, fid, _attr(value))
        )
    return "".join(out)


def _kpis(labels, prefix):
    cells = "".join(
        '<div class="kpi"><span>%s</span><strong id="%sK%d">&mdash;</strong></div>' % (label, prefix, i + 1)
        for i, label in enumerate(labels)
    )
    return '        <div class="kpi-grid">%s</div>\n' % cells


def expression_lab(cfg):
    """Modes: order, property, terms, distribute, like, evaluate, translate.

    THE TEACHING DECISION. Everything in this lesson is a rule about READING --
    which operation a string of symbols means first, which rearrangements are
    allowed, which pieces are the terms, what a bracket does to a substituted
    value. A reader who gets these wrong is not failing to know a fact; they are
    reading the same string differently from everybody else, and being told the
    right answer does not tell them where their reading and the intended one
    parted company.

    So no mode here prints an answer on its own. Every one of them prints the
    reader's own reading beside the intended one and lets arithmetic separate
    them: the queue against a strictly left-to-right pass, the named properties
    against a counterexample search, the terms as written against the terms
    after expanding, the substitution with brackets against the same
    substitution without. Where the two agree, the lab says so rather than
    manufacturing a disagreement -- 8 - 3 + 2 comes out at 7 both ways, and a
    lab that implied otherwise would be teaching suspicion instead of order.
    """
    mode = cfg.get("mode", "order")
    if mode not in EXPR_BODY:
        mode = "order"
    presets = cfg.get("presets") or EXPR_PRESETS[mode]
    title, subtitle = EXPR_TITLES[mode]
    first = presets[0][1]

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong>%s</strong><span id="exSub"></span></div>\n'
        '        <div class="inline-legend">%s</div>\n'
        "      </div>\n"
        '      <div class="lab-stage" id="exStage"></div>\n'
        '      <div id="exWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="exStatus" style="margin-top:12px;"></div>'
        % (title, EXPR_LEGEND[mode])
    )

    controls = (
        '        <div class="field">\n'
        '          <label for="exPreset">%s</label>\n'
        '          <select id="exPreset">%s</select>\n'
        "        </div>\n"
        "%s%s"
        '        <p class="small-copy" style="margin:0;">%s</p>'
        % (
            EXPR_SELECT_LABEL[mode], _options(presets),
            _fields(EXPR_FIELDS[mode], first),
            _kpis(EXPR_KPIS[mode], "ex"),
            EXPR_HINTS[mode],
        )
    )

    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + FORMAT_JS + MONO_JS + STEP_JS + EXPR_SHARED_JS
        + "\n  var HINT = " + _jsstr(EXPR_HINTS[mode]) + ";\n"
        + EXPR_PRELUDE + EXPR_BODY[mode] + EXPR_WIRE
    )

    panel_title, panel_intro = EXPR_PANEL[mode]
    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", panel_title),
        panel_intro=cfg.get("panel_intro", panel_intro),
        script=script,
    )

# =====================================================================
#                          THE REAL LINE LAB
# =====================================================================

# An exact number for a lesson about the line.
#
# Placing 1.4, 1.41, 1.414 and sqrt(2) in order is the whole point of that
# lesson, and it cannot be done in floating point: the reader is being asked
# whether sqrt(2) is bigger than 1.414, and 1.4142135623730951 is not sqrt(2).
# So a value here is q*sqrt(k) with q an exact rational and k a squarefree
# integer, and comparison squares both sides instead of evaluating them. The
# decimal column exists, is clearly a rounding, and decides nothing.
XNUM_JS = r"""
  function bisqrtfloor(n) {
    if (n < 0n) return null;
    if (n < 2n) return n;
    var x = n, y = (x + 1n) / 2n;
    while (y < x) { x = y; y = (x + n / x) / 2n; }
    return x;
  }
  function bfloordiv(n, d) {
    var q = n / d;
    if (n % d !== 0n && ((n < 0n) !== (d < 0n))) q -= 1n;
    return q;
  }
  function Xmake(q, k) {
    if (k === undefined) k = 1n;
    if (Rzero(q) || k === 0n) return { q: R0, k: 1n };
    var pair = bsqrtsimp(k);          /* k = s^2 * rest; the s comes outside */
    return { q: Rmul(q, R(pair[0])), k: pair[1] };
  }
  function Xrat(r) { return { q: r, k: 1n }; }
  function Xzero(x) { return Rzero(x.q); }
  function Xneg(x) { return { q: Rneg(x.q), k: x.k }; }
  function Xmul(a, b) { return Xmake(Rmul(a.q, b.q), a.k * b.k); }
  function Xdiv(a, b) {
    if (Xzero(b)) throw new Error('this divides by zero, and nothing divided by zero has a value');
    /* a / (q sqrt(k)) = (a / (q k)) sqrt(k): the denominator is rationalised
       here rather than left as a root, which is the radicals lesson done early. */
    return Xmake(Rdiv(a.q, Rmul(b.q, R(b.k))), a.k * b.k);
  }
  function Xadd(a, b) {
    if (Xzero(a)) return b;
    if (Xzero(b)) return a;
    if (a.k !== b.k) {
      throw new Error('sqrt(' + a.k + ') and sqrt(' + b.k + ') do not add into a single q*sqrt(k), '
        + 'and this lesson places one root at a time');
    }
    return { q: Radd(a.q, b.q), k: a.k };
  }
  function Xsub(a, b) { return Xadd(a, Xneg(b)); }
  function Xsqrtof(x) {
    if (x.k !== 1n) throw new Error('a square root of a square root is more than this lesson needs');
    if (Rsign(x.q) < 0) throw new Error('sqrt(' + Rtext(x.q) + ') is not a real number: no real number squares to a negative');
    var s = Rsurd(x.q);
    return { q: s.q, k: s.k };
  }
  function Xpow(x, e) {
    var out = Xrat(R1);
    for (var i = 0; i < e; i += 1) out = Xmul(out, x);
    return out;
  }
  /* The comparison the lesson is about, done exactly. Signs first, then squares:
     for two positives, a < b exactly when a^2 < b^2, and a^2 is a rational. */
  function Xcmp(a, b) {
    var sa = Rsign(a.q), sb = Rsign(b.q);
    if (sa !== sb) return sa < sb ? -1 : 1;
    if (sa === 0) return 0;
    var A = Rmul(Rmul(a.q, a.q), R(a.k)), B = Rmul(Rmul(b.q, b.q), R(b.k));
    var c = Rcmp(A, B);
    return sa > 0 ? c : -c;
  }
  function Xequ(a, b) { return Xcmp(a, b) === 0; }
  function Xtext(x) { return x.k === 1n ? Rtext(x.q) : surdtext(x); }
  /* Pixels and the decimal column only. Nothing is decided from this. */
  function Xnum(x) { return Rnum(x.q) * Math.sqrt(Number(x.k)); }
  function Xfloor(x) {
    var n = x.q.n, d = x.q.d;
    if (x.k === 1n) return bfloordiv(n, d);
    if (n >= 0n) return bisqrtfloor(n * n * x.k) / d;
    var m = -n, S = m * m * x.k, r = bisqrtfloor(S);
    return -(r * r === S ? (r + d - 1n) / d : r / d + 1n);
  }
  function Xof(node) {
    switch (node.k) {
      case 'num': {
        var r = Rread(node.v);
        if (r === null) throw new Error('"' + esc(node.v) + '" is not a number I can read exactly');
        return Xrat(r);
      }
      case 'var': throw new Error('a letter has no place on the line until it has a value');
      case 'neg': return Xneg(Xof(node.a));
      case 'add': return Xadd(Xof(node.a), Xof(node.b));
      case 'sub': return Xsub(Xof(node.a), Xof(node.b));
      case 'mul': return Xmul(Xof(node.a), Xof(node.b));
      case 'div': return Xdiv(Xof(node.a), Xof(node.b));
      case 'pow': {
        var e = Xof(node.b);
        if (e.k !== 1n || !Rint(e.q) || e.q.n < 0n || e.q.n > 12n) {
          throw new Error('the exponent has to be a whole number from 0 to 12 here');
        }
        return Xpow(Xof(node.a), Number(e.q.n));
      }
      case 'fn': {
        if (node.v === 'sqrt') return Xsqrtof(Xof(node.a));
        throw new Error(node.v + '(...) is not part of this lesson; sqrt is');
      }
    }
    throw new Error('I cannot read that value');
  }
  function Xread(text) { return Xof(Eparse(text)); }
"""

RL_PRESETS = {
    "place": [
        ("-3, -3/2, 0, 2/3, 1.75, 3", "-3, -3/2, 0, 2/3, 1.75, 3"),
        ("sqrt(2), 1.4, 1.41, 1.414, 3/2", "sqrt(2), 1.4, 1.41, 1.414, 3/2"),
        ("-sqrt(9), -3, sqrt(4), 2", "-sqrt(9), -3, sqrt(4), 2"),
        ("1/3, 0.333, 0.3333, 2/5", "1/3, 0.333, 0.3333, 2/5"),
        ("-sqrt(6), -5/2, -2.5, sqrt(6)", "-sqrt(6), -5/2, -2.5, sqrt(6)"),
        ("sqrt(2), 2/sqrt(2), sqrt(8)/2", "sqrt(2), 2/sqrt(2), sqrt(8)/2"),
    ],
    "absolute": [
        ("a = -4, b = 6, |x - a| = 3", "-4|6|3"),
        ("a = 3, b = 3, |x - a| = 0", "3|3|0"),
        ("a = 2, b = -5, |x - a| = -1", "2|-5|-1"),
        ("a = -3/2, b = 5/2, |x - a| = 7/2", "-3/2|5/2|7/2"),
        ("a = 0, b = -7, |x - a| = 5", "0|-7|5"),
        ("a = 5, b = -5, |x - a| = 10", "5|-5|10"),
    ],
}

RL_TITLES = {
    "place": ("Placing numbers on the line", "Ordered by exact comparison, not by decimal"),
    "absolute": ("Absolute value as distance", "Both cases of the definition, and the one that applies"),
}

RL_LEGEND = {
    "place": '<span class="tone-cyan"><i class="legend-swatch"></i>your values</span>'
             '<span class="tone-muted"><i class="legend-swatch"></i>a rational strictly between the closest two</span>',
    "absolute": '<span class="tone-cyan"><i class="legend-swatch"></i>the distance being measured</span>'
                '<span class="tone-green"><i class="legend-swatch"></i>solutions of the equation</span>',
}

RL_KPIS = {
    "place": ("Values", "Irrational", "Distinct places"),
    "absolute": ("|a|", "distance a to b", "Solutions"),
}

RL_HINTS = {
    "place": "Separate the values with commas. Whole numbers, fractions such as "
             "<code>-3/2</code>, decimals such as <code>1.414</code>, and square roots such as "
             "<code>sqrt(2)</code>, <code>2sqrt(3)</code> or <code>sqrt(8)/2</code>.",
    "absolute": "Each of a, b and c is a whole number or a fraction. c is allowed to be negative, "
                "and what happens then is the point of one of the presets.",
}

RL_PANEL = {
    "place": ("Type the values to place",
              "Every comparison below is made by squaring, not by rounding, so "
              "<code>sqrt(2)</code> and <code>1.414</code> are separated correctly however close "
              "they look. The decimal column is a rounding and says so."),
    "absolute": ("Choose a, b and c",
                 "The two-case definition is applied to your a, with the case that applies "
                 "highlighted, and the equation |x - a| = c is solved and then checked."),
}

RL_FIELDS = {
    "place": [("nlList", "Values, comma separated")],
    "absolute": [("nlA", "a"), ("nlB", "b"), ("nlC", "c")],
}

RL_BODY = {}

RL_PRELUDE = r"""
  var preset = document.getElementById('nlPreset');
  var svg = document.getElementById('nlPlot');
  var work = document.getElementById('nlWork');
  var status = document.getElementById('nlStatus');
  var subOut = document.getElementById('nlSub');
  var kA = document.getElementById('nlK1'), kB = document.getElementById('nlK2'), kC = document.getElementById('nlK3');
  function kpis(a, b, c) { kA.textContent = a; kB.textContent = b; kC.textContent = c; }
  /* The number line has no label method of its own; these two put a value above
     the axis and keep neighbouring labels from sitting on each other. */
  function markAt(line, x, label, closed, cls, level) {
    line.point(x, closed === undefined ? true : closed);
    if (!label) return;
    var t = svgel('text', { class: cls || 'plot-label', x: line.sx(x), y: level ? 16 : 30, 'text-anchor': 'middle' });
    t.textContent = label;
    svg.appendChild(t);
  }
  function fail(lead, detail) {
    svg.textContent = '';
    work.innerHTML = table('nothing placed yet', [step('input', tone(esc(lead), 'red'))]);
    kpis('&mdash;', '&mdash;', '&mdash;');
    status.innerHTML = '<strong>' + lead + '</strong> ' + detail + ' ' + HINT;
  }
"""

RL_BODY["place"] = r"""
  var input = document.getElementById('nlList');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); }

  /* Between any two different numbers there is a rational. This finds one
     rather than quoting the theorem: multiply by ten until the gap is wide
     enough to contain a whole number, take the next whole number up, divide
     back. The loop stopping IS the Archimedean property doing its work. */
  function rationalBetween(a, b) {
    var pow = 1n;
    for (var m = 0; m <= 14; m += 1) {
      var t = Xfloor({ q: Rmul(a.q, R(pow)), k: a.k }) + 1n;
      var cand = Xrat(R(t, pow));
      if (Xcmp(a, cand) < 0 && Xcmp(cand, b) < 0) return { value: cand, power: m };
      pow *= 10n;
    }
    return null;
  }

  function classify(x) {
    if (x.k !== 1n) {
      return { name: 'irrational', why: 'every square factor has been taken out and ' + x.k
        + ' is left, and the square root of a whole number bigger than 1 with no square factor is '
        + 'irrational' };
    }
    if (Rint(x.q)) {
      if (x.q.n > 0n) return { name: 'natural', why: 'a whole number bigger than zero' };
      return { name: 'integer', why: 'a whole number, and its denominator is 1' };
    }
    return { name: 'rational', why: 'a ratio of two whole numbers, ' + x.q.n + ' over ' + x.q.d };
  }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = src || 'nothing typed yet';
    if (!src) { fail('Type some values, separated by commas.', 'The box is empty, so there is nothing to place.'); return; }
    var pieces = src.split(','), values = [], bad = null;
    pieces.forEach(function (piece) {
      var text = piece.trim();
      if (!text || bad) return;
      try { values.push({ text: text, x: Xread(text) }); }
      catch (err) { bad = '"' + esc(text) + '" could not be read: ' + esc(err.message); }
    });
    if (bad) { fail('One of the values did not come out.', bad + '.'); return; }
    if (!values.length) { fail('Type some values, separated by commas.', 'Commas alone are not values.'); return; }

    var sorted = values.slice().sort(function (p, q) { return Xcmp(p.x, q.x); });
    var chain = '', irrational = 0, distinct = 0;
    sorted.forEach(function (item, i) {
      if (i) chain += Xequ(sorted[i - 1].x, item.x) ? ' = ' : ' &lt; ';
      chain += Xtext(item.x);
      if (i === 0 || !Xequ(sorted[i - 1].x, item.x)) distinct += 1;
      if (item.x.k !== 1n) irrational += 1;
    });

    var rows = [tr([th('as typed'), th('exact value'), th('kind'), th('why'), th('decimal, rounded to 6 places')])];
    values.forEach(function (item) {
      var c = classify(item.x);
      rows.push(tr([
        tdl(esc(item.text)), td(Xtext(item.x)), td(c.name), tdl(c.why),
        td(approx(Xnum(item.x), 6)),
      ], item.x.k !== 1n ? 'focus' : ''));
    });

    /* The closest two distinct values, and a rational strictly between them. */
    var closest = null;
    for (var i = 1; i < sorted.length; i += 1) {
      if (Xequ(sorted[i - 1].x, sorted[i].x)) continue;
      var gap = Math.abs(Xnum(sorted[i].x) - Xnum(sorted[i - 1].x));
      if (!closest || gap < closest.gap) closest = { lo: sorted[i - 1].x, hi: sorted[i].x, gap: gap };
    }
    var between = closest ? rationalBetween(closest.lo, closest.hi) : null;

    var lo = Xnum(sorted[0].x), hi = Xnum(sorted[sorted.length - 1].x);
    if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
    var pad = (hi - lo) * 0.15 + 0.2;
    var line = NumberLine(svg, lo - pad, hi + pad);
    if (between) line.interval(Xnum(closest.lo), Xnum(closest.hi), true, true);
    sorted.forEach(function (item, i) {
      markAt(line, Xnum(item.x), Xtext(item.x), true, 'plot-label', i % 2 === 1);
    });
    if (between) markAt(line, Xnum(between.value), Rtext(between.value.q), true, 'plot-label', true);
    line.describe('The values ' + sorted.map(function (v) { return Xtext(v.x); }).join(', ')
      + ' placed in order on a number line.');

    var extra = [step('in order', chain)];
    if (between) {
      extra.push(step('the closest two', Xtext(closest.lo) + ' and ' + Xtext(closest.hi)));
      extra.push(step('a rational strictly between them',
        Rtext(between.value.q) + ', found by multiplying by 10^' + between.power
        + ' until a whole number fitted in the gap'));
      extra.push(step('so the line has no gaps to fall through',
        'the same construction runs between any two different numbers, however close'));
    } else {
      extra.push(step('the closest two', 'every value here is the same number, so there is no gap to look inside'));
    }
    work.innerHTML = table('Every value, classified from its exact form', rows)
      + table('Order, and what fits between', extra);
    kpis(String(values.length), String(irrational), String(distinct));

    var msg = '<strong>' + chain + '.</strong> ';
    if (irrational) {
      msg += irrational + ' of these ' + (irrational === 1 ? 'is' : 'are') + ' irrational, and the '
        + 'order above was decided by squaring rather than by comparing decimals: for two positive '
        + 'numbers, a is less than b exactly when a squared is less than b squared, and those '
        + 'squares are fractions. The decimal column is rounded to 6 places and is not what any '
        + 'comparison here used.';
    } else {
      msg += 'Every value here is rational, so each one is a ratio of whole numbers and the order '
        + 'is a comparison of fractions: a/b against c/d is ad against cb.';
    }
    if (distinct < values.length) {
      msg += ' ' + (values.length - distinct) + ' of the entries repeat a number that is already '
        + 'there under a different name, so they sit on a point that is already occupied: a number '
        + 'has many names and one place.';
    }
    if (between) {
      msg += ' Between the closest two there is ' + Rtext(between.value.q) + ', which was found and '
        + 'not assumed; between that one and either neighbour there is another, and so on without end.';
    }
    status.innerHTML = msg;
  }
"""

RL_BODY["absolute"] = r"""
  var inA = document.getElementById('nlA'), inB = document.getElementById('nlB'), inC = document.getElementById('nlC');
  var INPUTS = [inA, inB, inC];
  function applyPreset(parts) {
    inA.value = (parts[0] || '').trim(); inB.value = (parts[1] || '').trim(); inC.value = (parts[2] || '').trim();
  }
  function absOf(r) { return Rsign(r) < 0 ? Rneg(r) : r; }

  function redraw() {
    var a = Rread(inA.value), b = Rread(inB.value), c = Rread(inC.value);
    if (a === null || b === null || c === null) {
      fail('Each of a, b and c has to be a number.', 'Whole numbers such as -4, or fractions such as 7/2.');
      return;
    }
    subOut.textContent = 'a = ' + Rtext(a) + ', b = ' + Rtext(b) + ', |x - a| = ' + Rtext(c);

    /* The definition, both branches evaluated, with the branch that applies
       marked. The reader is shown the branch that does NOT apply as well,
       because "|x| = -x" looks wrong until you have seen which x it is for. */
    var negative = Rsign(a) < 0;
    var caseRows = [tr([th('case'), th('the condition, on your a'), th('what the definition gives'), th('applies here?')])];
    caseRows.push(tr([
      tdl('x &gt;= 0'), tdl(Rtext(a) + ' &gt;= 0 is ' + (negative ? 'false' : 'true')),
      tdl('|x| = x, so |' + Rtext(a) + '| = ' + Rtext(a)),
      td(negative ? 'no' : 'yes', negative ? 'f' : 't'),
    ], negative ? '' : 'focus'));
    caseRows.push(tr([
      tdl('x &lt; 0'), tdl(Rtext(a) + ' &lt; 0 is ' + (negative ? 'true' : 'false')),
      tdl('|x| = -x, so |' + Rtext(a) + '| = ' + Rtext(Rneg(a))),
      td(negative ? 'yes' : 'no', negative ? 't' : 'f'),
    ], negative ? 'focus' : ''));

    var absA = absOf(a), absB = absOf(b);
    /* A second, independent route to the same number: |x| is also sqrt(x^2),
       and that computation never looks at the sign at all. */
    var viaSquare = Rsurd(Rmul(a, a));
    var squareText = viaSquare && viaSquare.k === 1n ? Rtext(viaSquare.q) : 'not rational';
    var agree = viaSquare && viaSquare.k === 1n && Requ(viaSquare.q, absA);

    var dAB = absOf(Rsub(a, b)), dBA = absOf(Rsub(b, a));
    var sumAbs = Radd(absA, absB), absSum = absOf(Radd(a, b));
    var triangleEq = Requ(absSum, sumAbs);
    var prodAbs = absOf(Rmul(a, b)), absProd = Rmul(absA, absB);

    var factRows = [tr([th('statement'), th('left'), th('right'), th('here')])];
    factRows.push(tr([tdl('|a| by the definition, and as sqrt(a^2)'), td(Rtext(absA)), td(squareText),
      td(agree ? 'agree' : 'differ', agree ? 't' : 'f')]));
    factRows.push(tr([tdl('|a - b| against |b - a|'), td(Rtext(dAB)), td(Rtext(dBA)),
      td(Requ(dAB, dBA) ? 'equal' : 'differ', Requ(dAB, dBA) ? 't' : 'f')]));
    factRows.push(tr([tdl('|a + b| against |a| + |b|'), td(Rtext(absSum)), td(Rtext(sumAbs)),
      td(triangleEq ? 'equal' : 'less', 't')]));
    factRows.push(tr([tdl('|ab| against |a||b|'), td(Rtext(prodAbs)), td(Rtext(absProd)),
      td(Requ(prodAbs, absProd) ? 'equal' : 'differ', Requ(prodAbs, absProd) ? 't' : 'f')]));

    /* |x - a| = c, solved by cases. Each case produces a candidate and each
       candidate is then tested against BOTH the case it came from and the
       original equation, which is where a negative c dies. */
    var candidates = [
      { name: 'x - a &gt;= 0, so x - a = c', x: Radd(a, c), condition: 'x &gt;= ' + Rtext(a) },
      { name: 'x - a &lt; 0, so -(x - a) = c', x: Rsub(a, c), condition: 'x &lt; ' + Rtext(a) }
    ];
    var solRows = [tr([th('case'), th('gives'), th('does it satisfy that case?'), th('|x - a|'), th('equals c?')])];
    var solutions = [];
    candidates.forEach(function (cand, i) {
      var fitsCase = i === 0 ? Rcmp(cand.x, a) >= 0 : Rcmp(cand.x, a) < 0;
      var lhs = absOf(Rsub(cand.x, a));
      var solves = Requ(lhs, c);
      if (fitsCase && solves) solutions.push(cand.x);
      solRows.push(tr([
        tdl(cand.name), td('x = ' + Rtext(cand.x)),
        td(fitsCase ? 'yes' : 'no', fitsCase ? 't' : 'f'),
        td(Rtext(lhs)), td(solves ? 'yes' : 'no', solves ? 't' : 'f'),
      ], fitsCase && solves ? 'focus' : ''));
    });
    /* x = a + c and x = a - c coincide when c is 0; one solution, not two. */
    var unique = [];
    solutions.forEach(function (x) {
      var seen = false;
      unique.forEach(function (y) { if (Requ(x, y)) seen = true; });
      if (!seen) unique.push(x);
    });

    var points = [0, Rnum(a), Rnum(b)];
    unique.forEach(function (x) { points.push(Rnum(x)); });
    var lo = Math.min.apply(null, points), hi = Math.max.apply(null, points);
    if (hi - lo < 1e-9) { lo -= 2; hi += 2; }
    var pad = (hi - lo) * 0.18 + 0.3;
    var line = NumberLine(svg, lo - pad, hi + pad);
    line.interval(Math.min(0, Rnum(a)), Math.max(0, Rnum(a)), true, true);
    markAt(line, 0, '0', true, 'plot-label', false);
    markAt(line, Rnum(a), 'a = ' + Rtext(a), true, 'plot-label', true);
    markAt(line, Rnum(b), 'b = ' + Rtext(b), true, 'plot-label', false);
    unique.forEach(function (x, i) { markAt(line, Rnum(x), 'x = ' + Rtext(x), true, 'plot-label', i % 2 === 0); });
    line.describe('A number line with 0, a = ' + Rtext(a) + ' and b = ' + Rtext(b)
      + ' marked, the distance from 0 to a drawn as a segment, and '
      + unique.length + ' solution(s) of |x - a| = ' + Rtext(c) + ' marked.');

    work.innerHTML = table('The definition has two cases, and exactly one of them applies', caseRows)
      + table('What that distance obeys, on your numbers', factRows)
      + table('Solving |x - a| = ' + Rtext(c) + ' by cases, then checking each candidate', solRows);
    kpis(Rtext(absA), Rtext(dAB), String(unique.length));

    var msg = '<strong>|' + Rtext(a) + '| = ' + Rtext(absA) + ', and the distance from '
      + Rtext(a) + ' to ' + Rtext(b) + ' is ' + Rtext(dAB) + '.</strong> ';
    msg += negative
      ? 'Because a is negative, the definition uses its second line: |x| = -x, and -(' + Rtext(a)
        + ') = ' + Rtext(absA) + '. That minus sign is not making the answer negative, it is '
        + 'undoing one.'
      : 'Because a is not negative, the definition uses its first line and leaves a alone.';
    msg += ' Distance has no direction, which is why |a - b| and |b - a| came out equal above.';
    if (!unique.length) {
      msg += ' <strong>The equation |x - a| = ' + Rtext(c) + ' has no solution.</strong> '
        + (Rsign(c) < 0
          ? 'Both cases produce a candidate, and both candidates fail: a distance is never negative, '
            + 'so no x on the whole line is ' + Rtext(c) + ' away from ' + Rtext(a) + '. Solving the '
            + 'two cases and stopping there would have handed back two answers that are not answers.'
          : 'Neither candidate survives its own case condition.');
    } else if (unique.length === 1) {
      msg += ' The equation |x - a| = 0 has the single solution x = ' + Rtext(unique[0])
        + ': the two cases give the same number, because the only point at distance 0 from a is a.';
    } else {
      msg += ' The equation |x - a| = ' + Rtext(c) + ' has two solutions, x = '
        + unique.map(Rtext).join(' and x = ') + ', one on each side of ' + Rtext(a)
        + '. Two is what a distance equation should give: the line has two directions.';
    }
    msg += triangleEq
      ? ' Here |a + b| and |a| + |b| are equal, which happens exactly when a and b point the same '
        + 'way or one of them is 0.'
      : ' Here |a + b| is strictly less than |a| + |b|, because a and b have opposite signs and '
        + 'partly cancel. That inequality is the triangle inequality, and this is the case that '
        + 'makes it an inequality rather than an equation.';
    status.innerHTML = msg;
  }
"""

RL_WIRE = r"""
  preset.addEventListener('change', function () { applyPreset(preset.value.split('|')); redraw(); });
  INPUTS.forEach(function (el) { el.addEventListener('input', redraw); });
  applyPreset(preset.value.split('|'));
  redraw();
  window.redrawLab = redraw;
"""


def realline_lab(cfg):
    """Modes: place, absolute.

    THE TEACHING DECISION. The number line is the first picture in algebra that
    is not a picture of a shape, and it gets taught with decimals, which quietly
    replaces the subject with a different one. Asked to place sqrt(2), 1.4, 1.41
    and 1.414 in order, a reader who compares 1.4142135... to 1.414 is comparing
    two roundings and getting the right answer for a reason that will fail them
    later; and a lab that did the same would be teaching that.

    So every value in this lab is exact -- a rational, or q*sqrt(k) with k
    squarefree -- and every comparison squares both sides rather than evaluating
    them. The decimal column is present because readers want it, is rounded to
    six places, says so, and decides nothing. The density construction is run
    rather than quoted: the lab multiplies by ten until a whole number fits in
    the gap between the closest two values, which is the Archimedean argument
    itself and stops with an actual fraction to show.

    The absolute value mode exists to make the second line of the definition
    survivable. |x| = -x looks like a sign error until you have seen it applied
    to a negative x, so both branches are always shown and the one that applies
    is highlighted -- and then the equation |x - a| = c is solved by those cases
    and each candidate is CHECKED against its own case, which is what kills the
    two false answers when c is negative.
    """
    mode = cfg.get("mode", "place")
    if mode not in RL_BODY:
        mode = "place"
    presets = cfg.get("presets") or RL_PRESETS[mode]
    title, subtitle = RL_TITLES[mode]
    first = presets[0][1]

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong>%s</strong><span id="nlSub"></span></div>\n'
        '        <div class="inline-legend">%s</div>\n'
        "      </div>\n"
        '      <div class="lab-stage"><svg id="nlPlot"></svg></div>\n'
        '      <div id="nlWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="nlStatus" style="margin-top:12px;"></div>'
        % (title, RL_LEGEND[mode])
    )

    controls = (
        '        <div class="field">\n'
        '          <label for="nlPreset">%s</label>\n'
        '          <select id="nlPreset">%s</select>\n'
        "        </div>\n"
        "%s%s"
        '        <p class="small-copy" style="margin:0;">%s</p>'
        % (
            "Values" if mode == "place" else "a, b and c",
            _options(presets), _fields(RL_FIELDS[mode], first),
            _kpis(RL_KPIS[mode], "nl"), RL_HINTS[mode],
        )
    )

    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + SURD_JS + PLOT_JS + FORMAT_JS + XNUM_JS
        + "\n  var HINT = " + _jsstr(RL_HINTS[mode]) + ";\n"
        + RL_PRELUDE + RL_BODY[mode] + RL_WIRE
    )

    panel_title, panel_intro = RL_PANEL[mode]
    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", panel_title),
        panel_intro=cfg.get("panel_intro", panel_intro),
        script=script,
    )

# =====================================================================
#                           THE EXPONENTS LAB
# =====================================================================

# Writing a power out in full is the whole argument for every exponent law, and
# it is also a second, independent computation of the answer. b^3 * b^4 is
# (b*b*b)*(b*b*b*b), and counting the b's is the proof that the exponents add.
# So this lab never computes a power once: it computes it by the law, and it
# computes it again by building the list of factors and multiplying them one at
# a time, and it prints both. Where they disagree the claim is not a law.
POWER_JS = r"""
  /* b^e as an explicit product. Returns the factor list, the running products
     that built it, and the value -- or a reason it has none. */
  function expandPow(b, e) {
    var k = e < 0 ? -e : e, factors = [], running = [], acc = R1;
    for (var i = 0; i < k; i += 1) { factors.push(Rterm(b)); acc = Rmul(acc, b); running.push(Rtext(acc)); }
    var body = k === 0 ? '1, the empty product' : factors.join(' * ');
    if (e < 0) {
      if (Rzero(acc)) {
        return { text: '1 / (' + body + ')', running: running, value: null,
                 why: '0 has no reciprocal, so a negative power of 0 is not a number' };
      }
      return { text: '1 / (' + body + ')', running: running, value: Rdiv(R1, acc), why: null };
    }
    return { text: body, running: running, value: acc, why: null };
  }
  function powOr(b, e) {
    /* The law side. Rpow itself divides by zero for 0^negative, which is the
       thing the reader needs told rather than thrown. */
    if (Rzero(b) && e < 0) return { value: null, why: '0 to a negative power divides by zero' };
    return { value: Rpow(b, e), why: null };
  }
  function powtext(base, e) { return base + '^' + (e < 0 ? '(' + e + ')' : e); }
  function expText(b, e) { return powtext(Rterm(b), e); }
"""

PW_PRESETS = {
    "laws": [
        ("a = 2, b = 3, m = 3, n = 4", "2|3|3|4"),
        ("a = 2, b = 3, m = 2, n = 5", "2|3|2|5"),
        ("a = -2, b = 5, m = 3, n = 2", "-2|5|3|2"),
        ("a = 2/3, b = -3/4, m = 4, n = 0", "2/3|-3/4|4|0"),
        ("a = 0, b = 7, m = 0, n = 3", "0|7|0|3"),
        ("a = 3, b = 4, m = 2, n = 2", "3|4|2|2"),
    ],
    "scientific": [
        ("6.02e23 and 1.6e-19", "6.02|23|1.6|-19"),
        ("3e8 and 2e-3", "3|8|2|-3"),
        ("1.2e5 and 3.4e4", "1.2|5|3.4|4"),
        ("9.9e3 and 2e2", "9.9|3|2|2"),
        ("5e-7 and 2e-3", "5|-7|2|-3"),
        ("45.6e3 and 0.004e2", "45.6|3|0.004|2"),
    ],
}

PW_TITLES = {
    "laws": ("The exponent laws, twice each", "By the law, and by writing the powers out"),
    "scientific": ("Scientific notation", "Normalised exactly, and arithmetic done in it"),
}

PW_LEGEND = {
    "laws": '<span class="tone-cyan"><i class="legend-swatch"></i>by the law</span>'
            '<span class="tone-purple"><i class="legend-swatch"></i>written out in full</span>'
            '<span class="tone-red"><i class="legend-swatch"></i>the two disagree</span>',
    "scientific": '<span class="tone-cyan"><i class="legend-swatch"></i>normalised form</span>'
                  '<span class="tone-green"><i class="legend-swatch"></i>checked against the plain number</span>',
}

PW_KPIS = {
    "laws": ("By the law", "Written out", "Laws that hold"),
    "scientific": ("Result", "Power of ten", "Digits in the mantissa"),
}

PW_HINTS = {
    "laws": "a and b may be fractions such as <code>-3/4</code>; m and n are whole numbers "
            "between -12 and 12, negative ones included.",
    "scientific": "A mantissa may be any number, normalised or not: <code>45.6</code> and "
                  "<code>0.004</code> are both accepted and both get normalised. The power of ten "
                  "is a whole number between -60 and 60.",
}

PW_PANEL = {
    "laws": ("Choose a law and some numbers",
             "Each law is computed twice from your numbers: once by the law itself, and once by "
             "writing every power out as a product and multiplying the factors one at a time. "
             "The last row of the summary is not a law, and it is on the list for that reason."),
    "scientific": ("Choose two numbers and an operation",
                   "Both numbers are normalised exactly, the arithmetic is done in scientific "
                   "form, and the answer is checked against the same calculation done on the "
                   "plain numbers."),
}

PW_FIELDS = {
    "laws": [("pwA", "a"), ("pwB", "b"), ("pwM", "m"), ("pwN", "n")],
    "scientific": [("pwM1", "first mantissa"), ("pwE1", "first power of ten"),
                   ("pwM2", "second mantissa"), ("pwE2", "second power of ten")],
}

PW_BODY = {}

PW_PRELUDE = r"""
  var preset = document.getElementById('pwPreset');
  var stage = document.getElementById('pwStage');
  var work = document.getElementById('pwWork');
  var status = document.getElementById('pwStatus');
  var subOut = document.getElementById('pwSub');
  var kA = document.getElementById('pwK1'), kB = document.getElementById('pwK2'), kC = document.getElementById('pwK3');
  function kpis(a, b, c) { kA.textContent = a; kB.textContent = b; kC.textContent = c; }
  function fail(lead, detail) {
    stage.innerHTML = table('nothing computed yet', [step('input', tone(esc(lead), 'red'))]);
    work.innerHTML = '';
    kpis('&mdash;', '&mdash;', '&mdash;');
    status.innerHTML = '<strong>' + lead + '</strong> ' + detail + ' ' + HINT;
  }
"""

PW_BODY["laws"] = r"""
  var lawSel = document.getElementById('pwLaw');
  var inA = document.getElementById('pwA'), inB = document.getElementById('pwB');
  var inM = document.getElementById('pwM'), inN = document.getElementById('pwN');
  var INPUTS = [inA, inB, inM, inN], EXTRA = [lawSel];
  function applyPreset(parts) {
    inA.value = (parts[0] || '').trim(); inB.value = (parts[1] || '').trim();
    inM.value = (parts[2] || '').trim(); inN.value = (parts[3] || '').trim();
  }

  /* Each claim knows how to state itself, how to work itself out by the law,
     and how to work itself out from the definition of a power. It does NOT
     know whether it is true; that is the last column, and it is computed. */
  var LAWS = {
    product: {
      name: 'multiplying powers of the same base',
      claim: function (A, B, m, n) { return powtext(B, m) + ' * ' + powtext(B, n) + ' = ' + powtext(B, m + n); },
      law: function (a, b, m, n) {
        var r = powOr(b, m + n);
        return { value: r.value, why: r.why, how: 'add the exponents: ' + m + ' + ' + n + ' = ' + (m + n) + ', so the answer is ' + expText(b, m + n) };
      },
      full: function (a, b, m, n) {
        var l = expandPow(b, m), r = expandPow(b, n);
        if (l.value === null || r.value === null) return { value: null, why: l.why || r.why, how: '&mdash;' };
        return { value: Rmul(l.value, r.value), why: null,
                 how: '(' + l.text + ') * (' + r.text + '), ' + (m >= 0 && n >= 0
                   ? 'which is ' + (m + n) + ' factors of ' + Rterm(b) + ' in one row'
                   : 'and once the reciprocals cancel against the factors above them, ' + (m + n) + ' net factors are left') };
      }
    },
    quotient: {
      name: 'dividing powers of the same base',
      claim: function (A, B, m, n) { return powtext(B, m) + ' / ' + powtext(B, n) + ' = ' + powtext(B, m - n); },
      law: function (a, b, m, n) {
        var r = powOr(b, m - n);
        return { value: r.value, why: r.why, how: 'subtract the exponents: ' + m + ' - ' + n + ' = ' + (m - n) + ', so the answer is ' + expText(b, m - n) };
      },
      full: function (a, b, m, n) {
        var l = expandPow(b, m), r = expandPow(b, n);
        if (l.value === null || r.value === null || Rzero(r.value)) {
          return { value: null, why: l.why || r.why || 'the bottom is 0, so this is a division by zero', how: '&mdash;' };
        }
        return { value: Rdiv(l.value, r.value), why: null,
                 how: '(' + l.text + ') / (' + r.text + ')' + (m >= 0 && n >= 0
                   ? ', and ' + Math.min(m, n) + ' factor(s) cancel top and bottom'
                   : '') };
      }
    },
    power: {
      name: 'a power of a power',
      claim: function (A, B, m, n) { return powtext('(' + powtext(B, m) + ')', n) + ' = ' + powtext(B, m * n); },
      law: function (a, b, m, n) {
        var r = powOr(b, m * n);
        return { value: r.value, why: r.why, how: 'multiply the exponents: ' + m + ' * ' + n + ' = ' + (m * n) + ', so the answer is ' + expText(b, m * n) };
      },
      full: function (a, b, m, n) {
        var inner = expandPow(b, m);
        if (inner.value === null) return { value: null, why: inner.why, how: '&mdash;' };
        var outer = expandPow(inner.value, n);
        if (outer.value === null) return { value: null, why: outer.why, how: '&mdash;' };
        return { value: outer.value, why: null,
                 how: n + ' cop' + (n === 1 ? 'y' : 'ies') + ' of (' + inner.text + '), which is ' + Math.abs(m * n) + ' factors of ' + Rterm(b) };
      }
    },
    product_base: {
      name: 'a power of a product',
      claim: function (A, B, m, n) { return powtext('(' + A + ' * ' + B + ')', n) + ' = ' + powtext(A, n) + ' * ' + powtext(B, n); },
      law: function (a, b, m, n) {
        var l = powOr(a, n), r = powOr(b, n);
        if (l.value === null || r.value === null) return { value: null, why: l.why || r.why, how: '&mdash;' };
        return { value: Rmul(l.value, r.value), why: null,
                 how: 'give each factor the exponent: ' + expText(a, n) + ' * ' + expText(b, n) };
      },
      full: function (a, b, m, n) {
        var e = expandPow(Rmul(a, b), n);
        return { value: e.value, why: e.why,
                 how: n + ' cop' + (n === 1 ? 'y' : 'ies') + ' of (' + Rterm(a) + ' * ' + Rterm(b) + '), which is ' + e.text };
      }
    },
    zero: {
      name: 'the zero exponent',
      claim: function (A, B, m, n) { return powtext(B, 0) + ' = 1'; },
      law: function (a, b, m, n) {
        return { value: R1, why: null,
                 how: expText(b, n) + ' / ' + expText(b, n) + ' is ' + expText(b, n - n) + ' by the quotient law, and anything nonzero over itself is 1' };
      },
      full: function (a, b, m, n) {
        var e = expandPow(b, n);
        if (e.value === null || Rzero(e.value)) {
          return { value: null, why: 'with b = 0 there is nothing to cancel: 0/0 is not 1, it is nothing at all', how: '&mdash;' };
        }
        return { value: Rdiv(e.value, e.value), why: null,
                 how: '(' + e.text + ') / (' + e.text + '): every factor cancels and an empty product is left, which is 1' };
      }
    },
    negative: {
      name: 'a negative exponent',
      claim: function (A, B, m, n) { return powtext(B, -n) + ' = 1 / ' + powtext(B, n); },
      law: function (a, b, m, n) {
        var r = powOr(b, -n);
        return { value: r.value, why: r.why, how: 'a negative exponent is the reciprocal of the positive one' };
      },
      full: function (a, b, m, n) {
        var e = expandPow(b, n);
        if (e.value === null || Rzero(e.value)) return { value: null, why: '1 divided by 0 is not a number', how: '&mdash;' };
        return { value: Rdiv(R1, e.value), why: null, how: '1 / (' + e.text + ')' };
      }
    },
    sum: {
      name: 'a power of a SUM, which is the one everybody wants to be a law',
      claim: function (A, B, m, n) { return powtext('(' + A + ' + ' + B + ')', n) + ' = ' + powtext(A, n) + ' + ' + powtext(B, n); },
      law: function (a, b, m, n) {
        var l = powOr(a, n), r = powOr(b, n);
        if (l.value === null || r.value === null) return { value: null, why: l.why || r.why, how: '&mdash;' };
        return { value: Radd(l.value, r.value), why: null, how: 'give each term the exponent: ' + expText(a, n) + ' + ' + expText(b, n) };
      },
      full: function (a, b, m, n) {
        var e = expandPow(Radd(a, b), n);
        return { value: e.value, why: e.why,
                 how: n + ' cop' + (n === 1 ? 'y' : 'ies') + ' of (' + Rterm(a) + ' + ' + Rterm(b) + ') = ' + Rterm(Radd(a, b)) + ', which is ' + e.text };
      }
    }
  };
  var ORDER = ['product', 'quotient', 'power', 'product_base', 'zero', 'negative', 'sum'];

  /* Agreement on one set of numbers is not much. For the claim on screen the
     lab also goes looking: 256 combinations of base and exponent, and the first
     one on which the two routes disagree. A claim that survives that is a law;
     a claim that does not is a claim whose counterexample is printed. */
  var GBASE = ['2', '3', '-2', '1/2'].map(Rparse), GEXP = [2, 3, 1, 0];
  function separates(law) {
    for (var i = 0; i < GBASE.length; i += 1) {
      for (var j = 0; j < GBASE.length; j += 1) {
        for (var p = 0; p < GEXP.length; p += 1) {
          for (var q = 0; q < GEXP.length; q += 1) {
            var bl, fl;
            try { bl = law.law(GBASE[i], GBASE[j], GEXP[p], GEXP[q]); fl = law.full(GBASE[i], GBASE[j], GEXP[p], GEXP[q]); }
            catch (err) { continue; }
            if (bl.value === null || fl.value === null) continue;
            if (!Requ(bl.value, fl.value)) {
              return { a: GBASE[i], b: GBASE[j], m: GEXP[p], n: GEXP[q], law: bl.value, full: fl.value };
            }
          }
        }
      }
    }
    return null;
  }

  function redraw() {
    var a = Rread(inA.value), b = Rread(inB.value), m = Rread(inM.value), n = Rread(inN.value);
    if (a === null || b === null || m === null || n === null) {
      fail('a, b, m and n all have to be numbers.', 'a and b may be fractions; m and n must be whole numbers.');
      return;
    }
    if (!Rint(m) || !Rint(n)) {
      fail('m and n have to be whole numbers here.',
        'A fractional exponent is a root, and the radicals lab is where those live.');
      return;
    }
    if (m.n > 12n || m.n < -12n || n.n > 12n || n.n < -12n) {
      fail('Keep m and n between -12 and 12.',
        'Every power below is written out as an actual list of factors, and a list of a thousand '
        + 'factors teaches nothing that a list of seven does not.');
      return;
    }
    var mi = Number(m.n), ni = Number(n.n);
    var key = lawSel.value, law = LAWS[key] || LAWS.product;
    subOut.textContent = 'a = ' + Rtext(a) + ', b = ' + Rtext(b) + ', m = ' + mi + ', n = ' + ni;

    var byLaw = law.law(a, b, mi, ni), inFull = law.full(a, b, mi, ni);
    var same = byLaw.value !== null && inFull.value !== null && Requ(byLaw.value, inFull.value);
    var claim = law.claim(Rterm(a), Rterm(b), mi, ni);

    stage.innerHTML = table('the claim, worked out both ways', [
      step('the claim', claim),
      step('by the law', byLaw.value === null ? tone(esc(byLaw.why), 'red') : tone(Rtext(byLaw.value), 'cyan')),
      step('written out in full', inFull.value === null ? tone(esc(inFull.why), 'red') : tone(Rtext(inFull.value), 'purple')),
      step('the same number?', byLaw.value === null || inFull.value === null
        ? '<span class="chip">one side has no value</span>'
        : (same ? '<span class="chip ok">yes</span>' : '<span class="chip no">no, and so this is not a law</span>')),
    ]);

    var cx = separates(law);
    var detail = [tr([th('route'), th('what it does'), th('answer')])];
    detail.push(tr([tdl('by the law'), tdl(byLaw.how), td(byLaw.value === null ? tone(esc(byLaw.why), 'red') : Rtext(byLaw.value))]));
    detail.push(tr([tdl('written out in full'), tdl(inFull.how), td(inFull.value === null ? tone(esc(inFull.why), 'red') : Rtext(inFull.value))], 'focus'));
    detail.push(tr([tdl('the same search over 256 other cases'),
      tdl(cx ? 'a case where the two routes part company was found'
             : 'no case anywhere in the search made the two routes disagree'),
      tdl(cx ? '<span class="chip no">a = ' + Rtext(cx.a) + ', b = ' + Rtext(cx.b) + ', m = ' + cx.m
            + ', n = ' + cx.n + ': ' + Rtext(cx.law) + ' against ' + Rtext(cx.full) + '</span>'
             : '<span class="chip ok">nothing found</span>')]));

    var growth = [tr([th('power'), th('as a product'), th('value')])];
    for (var e = 0; e <= Math.max(1, Math.abs(ni) || Math.abs(mi)); e += 1) {
      var ex = expandPow(b, e);
      growth.push(tr([td(expText(b, e)), tdl(e === 0 ? 'an empty product' : ex.text), td(ex.value === null ? '&mdash;' : Rtext(ex.value))], e === 0 ? 'focus' : ''));
    }

    /* Every claim on the list, on the same numbers. The point of the summary is
       that it is one list: the true ones and the false one are computed the
       same way and only the last column tells them apart. */
    var all = [tr([th('claim'), th('by the law'), th('written out'), th('agree?')])];
    var holds = 0, total = 0;
    ORDER.forEach(function (id) {
      var L = LAWS[id];
      var bl = L.law(a, b, mi, ni), fl = L.full(a, b, mi, ni);
      var ok = bl.value !== null && fl.value !== null && Requ(bl.value, fl.value);
      if (bl.value !== null && fl.value !== null) { total += 1; if (ok) holds += 1; }
      all.push(tr([
        tdl(L.claim(Rterm(a), Rterm(b), mi, ni)),
        td(bl.value === null ? 'undefined' : Rtext(bl.value)),
        td(fl.value === null ? 'undefined' : Rtext(fl.value)),
        td(bl.value === null || fl.value === null ? '&mdash;' : (ok ? 'yes' : 'no'), bl.value === null || fl.value === null ? '' : (ok ? 't' : 'f')),
      ], id === key ? 'focus' : ''));
    });

    work.innerHTML = table('The chosen claim: ' + law.name, detail)
      + table('Powers of ' + Rterm(b) + ', each one written out', growth)
      + table('Every claim on the list, on these same numbers', all);
    kpis(byLaw.value === null ? 'undefined' : Rtext(byLaw.value),
      inFull.value === null ? 'undefined' : Rtext(inFull.value), holds + ' of ' + total);

    var msg;
    if (byLaw.value === null || inFull.value === null) {
      msg = '<strong>' + claim + ' has no value for these numbers.</strong> '
        + esc(byLaw.why || inFull.why) + '. That is not a failure of the law: the law is about '
        + 'numbers, and this expression is not one.';
    } else if (same && cx) {
      msg = '<strong>' + claim + ' comes out true on these numbers &mdash; both routes give '
        + Rtext(byLaw.value) + ' &mdash; and it is still not a law.</strong> The search found '
        + 'a = ' + Rtext(cx.a) + ', b = ' + Rtext(cx.b) + ', m = ' + cx.m + ', n = ' + cx.n
        + ', where the rule gives ' + Rtext(cx.law) + ' and writing the powers out gives '
        + Rtext(cx.full) + '. Numbers like the ones in the boxes cannot tell the two apart, which '
        + 'is exactly how a wrong rule survives being checked.';
    } else if (same) {
      msg = '<strong>' + claim + ', and both routes give ' + Rtext(byLaw.value) + '.</strong> '
        + 'The second route did not use the law at all &mdash; it wrote every power out as a list '
        + 'of factors and multiplied them one at a time &mdash; so the agreement is evidence for '
        + 'the law rather than a restatement of it, and no case in the 256 searched separated them '
        + 'either. That is also the proof in miniature: counting the factors on each side is the '
        + 'whole argument.';
    } else {
      msg = '<strong>' + claim + ' is false: the law side gives ' + Rtext(byLaw.value)
        + ' and writing it out gives ' + Rtext(inFull.value) + '.</strong> Exponents distribute '
        + 'over multiplication and division, and over nothing else. A power of a sum has to be '
        + 'multiplied out, which is the distributing lesson, and for n = 2 that is where the '
        + 'middle term comes from.';
    }
    if (Rzero(b) && (mi === 0 || ni === 0)) {
      msg += ' With b = 0 and a zero exponent, the summary above shows 0^0 as 1, and that is a '
        + 'convention rather than a computation: the empty product is 1, while 0 to every positive '
        + 'power is 0, and the two habits pull in opposite directions. Analysis leaves 0^0 '
        + 'undefined for exactly that reason.';
    }
    status.innerHTML = msg;
  }
"""

PW_BODY["scientific"] = r"""
  var opSel = document.getElementById('pwOp');
  var inM1 = document.getElementById('pwM1'), inE1 = document.getElementById('pwE1');
  var inM2 = document.getElementById('pwM2'), inE2 = document.getElementById('pwE2');
  var INPUTS = [inM1, inE1, inM2, inE2], EXTRA = [opSel];
  function applyPreset(parts) {
    inM1.value = (parts[0] || '').trim(); inE1.value = (parts[1] || '').trim();
    inM2.value = (parts[2] || '').trim(); inE2.value = (parts[3] || '').trim();
  }

  var TEN = R(10n);
  /* Normalising is done by moving the point, exactly, and counting the moves.
     No logarithm and no rounding: 45.6 and 0.004 both land in [1, 10) and the
     exponent absorbs every move. */
  function normalise(m, e) {
    if (Rzero(m)) return { m: R0, e: 0, moves: 0 };
    var moves = 0, guard = 0;
    while (Rcmp(Rabs(m), TEN) >= 0 && guard < 400) { m = Rdiv(m, TEN); e += 1; moves += 1; guard += 1; }
    while (Rcmp(Rabs(m), R1) < 0 && guard < 400) { m = Rmul(m, TEN); e -= 1; moves -= 1; guard += 1; }
    return { m: m, e: e, moves: moves };
  }
  /* A mantissa is written as a decimal, which is the whole convention: 6.02,
     not 301/50. It is CARRIED as an exact rational and only written this way,
     and when a mantissa has no terminating decimal it is shown as the fraction
     rather than rounded. */
  function mtext(r) { var d = plaindec(r); return d === null ? Rtext(r) : d; }
  function mterm(r) { var t = mtext(r); return Rsign(r) < 0 ? '(' + t + ')' : t; }
  function sciText(m, e) { return mtext(m) + ' &times; 10^' + e; }
  function valueOf(m, e) { return Rmul(m, Rpow(TEN, e)); }
  /* The plain number, exactly. A rational has a terminating decimal exactly
     when its denominator is built from 2s and 5s, and this returns null rather
     than a rounding when it does not. */
  function plaindec(r) {
    var d = r.d, twos = 0, fives = 0;
    while (d % 2n === 0n) { d /= 2n; twos += 1; }
    while (d % 5n === 0n) { d /= 5n; fives += 1; }
    if (d !== 1n) return null;
    var places = Math.max(twos, fives);
    var scaled = r.n * (10n ** BigInt(places)) / r.d;
    var sign = scaled < 0n ? '-' : '';
    var digits = (scaled < 0n ? -scaled : scaled).toString();
    if (places === 0) return sign + digits;
    while (digits.length <= places) digits = '0' + digits;
    var out = digits.slice(0, digits.length - places) + '.' + digits.slice(digits.length - places);
    out = out.replace(/0+$/, '').replace(/\.$/, '');
    return sign + out;
  }
  function digitsOf(r) {
    var text = plaindec(r);
    if (text === null) return null;
    return text.replace(/[-.]/g, '').replace(/^0+/, '').length;
  }

  var OPS = {
    times: { word: 'multiplied by', symbol: '*', run: function (m1, e1, m2, e2) {
      return { m: Rmul(m1, m2), e: e1 + e2, steps: [
        ['the mantissas multiply', mterm(m1) + ' * ' + mterm(m2) + ' = ' + mtext(Rmul(m1, m2))],
        ['the powers of ten add', '10^' + e1 + ' * 10^' + e2 + ' = 10^' + (e1 + e2)
          + ', by the law that adds exponents on a common base'],
      ] };
    } },
    over: { word: 'divided by', symbol: '/', run: function (m1, e1, m2, e2) {
      if (Rzero(m2)) return { why: 'the second number is 0, and nothing is divided by 0' };
      return { m: Rdiv(m1, m2), e: e1 - e2, steps: [
        ['the mantissas divide', mterm(m1) + ' / ' + mterm(m2) + ' = ' + mtext(Rdiv(m1, m2))],
        ['the powers of ten subtract', '10^' + e1 + ' / 10^' + e2 + ' = 10^' + (e1 - e2)],
      ] };
    } },
    plus: { word: 'plus', symbol: '+', run: function (m1, e1, m2, e2) { return addsub(m1, e1, m2, e2, 1); } },
    minus: { word: 'minus', symbol: '-', run: function (m1, e1, m2, e2) { return addsub(m1, e1, m2, e2, -1); } }
  };
  /* Adding is the one that is not term-by-term: the powers have to match first,
     and that step is where scientific notation is usually got wrong. */
  function addsub(m1, e1, m2, e2, sign) {
    var e = Math.min(e1, e2);
    var s1 = Rmul(m1, Rpow(TEN, e1 - e)), s2 = Rmul(m2, Rpow(TEN, e2 - e));
    var steps = [];
    if (e1 === e2) {
      steps.push(['the powers already match', 'both are 10^' + e + ', so the mantissas can be combined at once']);
    } else {
      steps.push(['the powers do not match', '10^' + e1 + ' and 10^' + e2 + ' are different sizes, and mantissas over different powers cannot be added']);
      steps.push(['rewrite over the smaller power', sciText(m1, e1) + ' = ' + sciText(s1, e)
        + '   and   ' + sciText(m2, e2) + ' = ' + sciText(s2, e)]);
    }
    steps.push([sign > 0 ? 'now the mantissas add' : 'now the mantissas subtract',
      mterm(s1) + (sign > 0 ? ' + ' : ' - ') + mterm(s2) + ' = ' + mtext(sign > 0 ? Radd(s1, s2) : Rsub(s1, s2))]);
    return { m: sign > 0 ? Radd(s1, s2) : Rsub(s1, s2), e: e, steps: steps };
  }

  function redraw() {
    var m1 = Rread(inM1.value), e1 = Rread(inE1.value), m2 = Rread(inM2.value), e2 = Rread(inE2.value);
    if (m1 === null || m2 === null || e1 === null || e2 === null) {
      fail('All four boxes have to be numbers.', 'The mantissas may be decimals or fractions; the powers of ten must be whole numbers.');
      return;
    }
    if (!Rint(e1) || !Rint(e2) || e1.n > 60n || e1.n < -60n || e2.n > 60n || e2.n < -60n) {
      fail('The powers of ten have to be whole numbers between -60 and 60.',
        'Every number below is written out in full as an exact integer or decimal, and outside that '
        + 'range the full form stops being something a reader can look at.');
      return;
    }
    var p1 = Number(e1.n), p2 = Number(e2.n);
    var n1 = normalise(m1, p1), n2 = normalise(m2, p2);
    var opKey = opSel.value, op = OPS[opKey] || OPS.times;
    subOut.textContent = sciText(m1, p1) + '  ' + op.symbol + '  ' + sciText(m2, p2);

    var inputRows = [tr([th('as typed'), th('normalised'), th('why'), th('as a plain number')])];
    [[m1, p1, n1], [m2, p2, n2]].forEach(function (item) {
      var raw = item[0], pw = item[1], nn = item[2];
      var plain = plaindec(valueOf(raw, pw));
      inputRows.push(tr([
        tdl(sciText(raw, pw)), tdl(sciText(nn.m, nn.e)),
        tdl(nn.moves === 0 ? 'already between 1 and 10' :
          (nn.moves > 0 ? 'the point moved ' + nn.moves + ' place(s) left, so the power went up by ' + nn.moves
                        : 'the point moved ' + (-nn.moves) + ' place(s) right, so the power went down by ' + (-nn.moves))),
        tdl(plain === null ? 'a fraction with no terminating decimal: ' + Rtext(valueOf(raw, pw)) : plain),
      ], nn.moves === 0 ? '' : 'focus'));
    });

    var result = op.run(n1.m, n1.e, n2.m, n2.e);
    if (result.why) {
      stage.innerHTML = table('no result', [step('the calculation', subOut.textContent), step('why not', tone(esc(result.why), 'red'))]);
      work.innerHTML = table('The two numbers, normalised', inputRows);
      kpis('undefined', '&mdash;', '&mdash;');
      status.innerHTML = '<strong>This calculation has no answer.</strong> ' + esc(result.why)
        + '. Scientific notation does not change that: 0 is 0 however it is written, and dividing '
        + 'by it is not an operation on numbers.';
      return;
    }
    var final = normalise(result.m, result.e);
    var steps = result.steps.map(function (pair) { return step(pair[0], pair[1]); });
    steps.push(step('collect', sciText(result.m, result.e)));
    if (final.moves !== 0) {
      steps.push(step('normalise the answer', mtext(result.m) + ' is not between 1 and 10, so move the point again: '
        + sciText(final.m, final.e)));
    } else {
      steps.push(step('already normalised', mtext(final.m) + ' is between 1 and 10, so nothing more to do'));
    }

    /* The same calculation on the plain numbers, as a check. The scientific
       route and the plain route are different arithmetic, and they have to
       land on the same rational. */
    var v1 = valueOf(m1, p1), v2 = valueOf(m2, p2);
    var direct = opKey === 'times' ? Rmul(v1, v2)
      : (opKey === 'over' ? Rdiv(v1, v2) : (opKey === 'plus' ? Radd(v1, v2) : Rsub(v1, v2)));
    var viaSci = valueOf(final.m, final.e);
    var agree = Requ(direct, viaSci);
    var plainResult = plaindec(direct);
    var digits = digitsOf(final.m);

    var checkRows = [tr([th('route'), th('answer as a plain number'), th('same?')])];
    checkRows.push(tr([tdl('in scientific form, then written out'),
      tdl(plaindec(viaSci) === null ? Rtext(viaSci) : plaindec(viaSci)), td(agree ? 'yes' : 'no', agree ? 't' : 'f')]));
    checkRows.push(tr([tdl('on the plain numbers from the start'),
      tdl(plainResult === null ? Rtext(direct) : plainResult), td(agree ? 'yes' : 'no', agree ? 't' : 'f')]));

    stage.innerHTML = table('the calculation, in scientific form', [
      step('first number', sciText(n1.m, n1.e)),
      step('operation', op.word),
      step('second number', sciText(n2.m, n2.e)),
      step('answer', sciText(final.m, final.e)),
      step('written out', plaindec(viaSci) === null ? Rtext(viaSci) + ' (a fraction with no terminating decimal)' : plaindec(viaSci)),
    ]);
    work.innerHTML = table('The two numbers, normalised', inputRows)
      + table('The arithmetic, done in scientific form', steps)
      + table('The same calculation done on the plain numbers', checkRows);
    kpis(sciText(final.m, final.e), '10^' + final.e, digits === null ? 'a fraction' : String(digits));

    var msg = '<strong>' + sciText(n1.m, n1.e) + ' ' + op.symbol + ' ' + sciText(n2.m, n2.e)
      + ' = ' + sciText(final.m, final.e) + '.</strong> ';
    if (opKey === 'plus' || opKey === 'minus') {
      msg += p1 === p2
        ? 'Both powers were the same, so the mantissas could be combined directly. Change one of '
          + 'the powers and the first step changes: mantissas over different powers of ten are not '
          + 'the same kind of thing and cannot be added as they stand.'
        : 'The powers differed, so the first move was to write both over 10^' + Math.min(n1.e, n2.e)
          + '. Adding the mantissas without doing that is the standard way to lose a factor of ten: '
          + 'it is the same mistake as adding 3 metres to 3 centimetres and writing 6.';
    } else {
      msg += 'Multiplying and dividing are the easy direction: the mantissas '
        + (opKey === 'times' ? 'multiply and the exponents add' : 'divide and the exponents subtract')
        + ', because a power of ten is just a factor and the exponent laws apply to it like any other base.';
    }
    if (final.moves !== 0) {
      msg += ' The answer needed normalising again afterwards &mdash; ' + mtext(result.m)
        + ' is outside 1 to 10 &mdash; which is where a power of ten gets gained or lost if the '
        + 'step is skipped.';
    }
    msg += agree
      ? ' The check agrees: the same calculation carried out on the plain numbers gives the same '
        + 'exact value, so no power of ten went missing.'
      : ' The check DISAGREES, which means something above is wrong.';
    if (digits !== null) {
      msg += ' The mantissa ' + mtext(final.m) + ' carries ' + digits + ' digit'
        + (digits === 1 ? '' : 's') + '. Nothing here has been rounded: every value on the page is '
        + 'exact, and where an answer has no terminating decimal it is shown as a fraction rather '
        + 'than cut off.';
      if (digits > 12) {
        msg += ' Those ' + digits + ' digits are what the exact answer needs, and they are the '
          + 'argument for significant figures: the two numbers are so far apart in size that '
          + 'rounding the answer to the three or four digits the inputs were measured to would '
          + 'discard the smaller one completely. Scientific notation makes that visible instead of '
          + 'hiding it.';
      }
    }
    status.innerHTML = msg;
  }
"""

PW_WIRE = r"""
  preset.addEventListener('change', function () { applyPreset(preset.value.split('|')); redraw(); });
  EXTRA.forEach(function (el) { el.addEventListener('change', redraw); });
  INPUTS.forEach(function (el) { el.addEventListener('input', redraw); });
  applyPreset(preset.value.split('|'));
  redraw();
  window.redrawLab = redraw;
"""

PW_LAW_OPTIONS = [
    ("product", "b^m * b^n = b^(m+n)"),
    ("quotient", "b^m / b^n = b^(m-n)"),
    ("power", "(b^m)^n = b^(mn)"),
    ("product_base", "(ab)^n = a^n b^n"),
    ("zero", "b^0 = 1"),
    ("negative", "b^(-n) = 1 / b^n"),
    ("sum", "(a+b)^n = a^n + b^n"),
]

PW_OP_OPTIONS = [
    ("times", "multiply"),
    ("over", "divide"),
    ("plus", "add"),
    ("minus", "subtract"),
]


def exponents_lab(cfg):
    """Modes: laws, scientific.

    THE TEACHING DECISION. An exponent law is not a fact to be remembered; it is
    a sentence about counting factors, and a reader who has the sentence never
    needs the fact. b^3 * b^4 is (b*b*b)(b*b*b*b), and the reason the exponents
    add is that there are now seven b's in a row.

    So this lab computes every claim twice and prints both: once by applying the
    law, and once by building the actual list of factors and multiplying them
    one at a time. Those are different code paths, and their agreement is the
    evidence. The seventh claim on the list, (a + b)^n = a^n + b^n, is written in
    exactly the same shape as the other six and computed the same way -- and it
    disagrees, on every preset except the ones where it accidentally cannot.
    Putting it on the same list as the real laws is deliberate: the reader who
    "remembers the rules" has no way to tell it from them, and the reader who
    writes the factors out has no way to fall for it.

    Scientific notation is here because it is the exponent laws being used for
    something. The normalising is done by moving the decimal point exactly and
    counting the moves rather than by a logarithm, addition is made to show the
    alignment step that everybody skips, and the answer is checked against the
    same calculation done on the plain numbers.
    """
    mode = cfg.get("mode", "laws")
    if mode not in PW_BODY:
        mode = "laws"
    presets = cfg.get("presets") or PW_PRESETS[mode]
    title, subtitle = PW_TITLES[mode]
    first = presets[0][1]

    if mode == "laws":
        extra_select = (
            '        <div class="field">\n'
            '          <label for="pwLaw">Claim</label>\n'
            '          <select id="pwLaw">%s</select>\n'
            "        </div>\n" % "".join(
                '<option value="%s">%s</option>' % (value, _attr(label))
                for value, label in PW_LAW_OPTIONS
            )
        )
    else:
        extra_select = (
            '        <div class="field">\n'
            '          <label for="pwOp">Operation</label>\n'
            '          <select id="pwOp">%s</select>\n'
            "        </div>\n" % "".join(
                '<option value="%s">%s</option>' % (value, label)
                for value, label in PW_OP_OPTIONS
            )
        )

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong>%s</strong><span id="pwSub"></span></div>\n'
        '        <div class="inline-legend">%s</div>\n'
        "      </div>\n"
        '      <div class="lab-stage" id="pwStage"></div>\n'
        '      <div id="pwWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="pwStatus" style="margin-top:12px;"></div>'
        % (title, PW_LEGEND[mode])
    )

    controls = (
        "%s"
        '        <div class="field">\n'
        '          <label for="pwPreset">Numbers</label>\n'
        '          <select id="pwPreset">%s</select>\n'
        "        </div>\n"
        "%s%s"
        '        <p class="small-copy" style="margin:0;">%s</p>'
        % (
            extra_select, _options(presets), _fields(PW_FIELDS[mode], first),
            _kpis(PW_KPIS[mode], "pw"), PW_HINTS[mode],
        )
    )

    script = (
        RATIONAL_JS + FORMAT_JS + POWER_JS
        + "\n  var HINT = " + _jsstr(PW_HINTS[mode]) + ";\n"
        + PW_PRELUDE + PW_BODY[mode] + PW_WIRE
    )

    panel_title, panel_intro = PW_PANEL[mode]
    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", panel_title),
        panel_intro=cfg.get("panel_intro", panel_intro),
        script=script,
    )

# =====================================================================
#                           THE RADICALS LAB
# =====================================================================

# Three pieces of arithmetic no other lab here needs.
#
#  * the prime factorisation, because "pull the perfect squares out" IS the
#    factorisation read a certain way, and a reader who is shown 72 = 2^3 * 3^2
#    can see which factors leave and why, instead of hunting for the largest
#    square factor by inspection.
#  * exact integer nth roots, so that "is this a perfect cube?" is decided and
#    not estimated.
#  * a sum of surds, c1*sqrt(k1) + c2*sqrt(k2) + ..., with exact rational
#    coefficients and squarefree kernels. This is the type in which sqrt(8) and
#    sqrt(18) turn out to be like terms, in which (2 + sqrt(3))(2 - sqrt(3)) is
#    exactly 1, and in which a conjugate clears a denominator.
RADICAL_JS = r"""
  function bpow(b, e) { var out = 1n; for (var i = 0; i < e; i += 1) out *= b; return out; }
  function bfactorise(n) {
    var out = [], f = 2n;
    if (n < 0n) n = -n;
    while (f * f <= n) {
      var e = 0;
      while (n % f === 0n) { n /= f; e += 1; }
      if (e) out.push([f, e]);
      f += 1n;
      if (f > 300000n) break;      /* lesson-sized radicands */
    }
    if (n > 1n) out.push([n, 1]);
    return out;
  }
  /* floor of the k-th root, by binary search on integers: exact, and it never
     asks a float what a BigInt knows. */
  function bnthrootFloor(n, k) {
    if (n < 0n) return null;
    if (n < 2n) return n;
    var lo = 0n, hi = 1n;
    while (bpow(hi, k) <= n) hi *= 2n;
    while (lo + 1n < hi) {
      var mid = (lo + hi) / 2n;
      if (bpow(mid, k) <= n) lo = mid; else hi = mid;
    }
    return lo;
  }
  function bnthroot(n, k) {
    if (n < 0n) {
      if (k % 2 === 0) return null;
      var r = bnthroot(-n, k);
      return r === null ? null : -r;
    }
    var f = bnthrootFloor(n, k);
    return bpow(f, k) === n ? f : null;
  }
  function Rnthroot(r, k) {
    var a = bnthroot(r.n, k), b = bnthroot(r.d, k);
    return (a === null || b === null) ? null : R(a, b);
  }
  /* The k-th root of a positive integer n, split into what comes out and what
     stays in, prime by prime. */
  function rootsimp(n, k) {
    var rows = bfactorise(n).map(function (pair) {
      var p = pair[0], e = pair[1];
      return { p: p, e: e, out: Math.floor(e / k), rest: e % k };
    });
    var outside = 1n, inside = 1n;
    rows.forEach(function (row) { outside *= bpow(row.p, row.out); inside *= bpow(row.p, row.rest); });
    return { outside: outside, inside: inside, rows: rows };
  }
  function rootText(k, radicand) {
    if (k === 2) return 'sqrt(' + radicand + ')';
    if (k === 3) return 'cbrt(' + radicand + ')';
    return 'root' + k + '(' + radicand + ')';
  }

  /* ---- sums of surds ---- */
  function SVterm(c, k) {
    var out = {};
    if (Rzero(c)) return out;
    var pair = bsqrtsimp(k);                 /* sqrt(12) = 2 sqrt(3) on the way in */
    out[String(pair[1])] = Rmul(c, R(pair[0]));
    return out;
  }
  function SVfromR(r) { return SVterm(r, 1n); }
  function SVadd(a, b) {
    var out = {}, key;
    for (key in a) if (a.hasOwnProperty(key)) out[key] = a[key];
    for (key in b) if (b.hasOwnProperty(key)) {
      out[key] = out[key] ? Radd(out[key], b[key]) : b[key];
      if (Rzero(out[key])) delete out[key];
    }
    return out;
  }
  function SVneg(a) {
    var out = {}, key;
    for (key in a) if (a.hasOwnProperty(key)) out[key] = Rneg(a[key]);
    return out;
  }
  function SVsub(a, b) { return SVadd(a, SVneg(b)); }
  function SVmul(a, b) {
    var out = {}, i, j;
    for (i in a) if (a.hasOwnProperty(i)) {
      for (j in b) if (b.hasOwnProperty(j)) {
        /* sqrt(i) * sqrt(j) = sqrt(ij), and ij needs simplifying again */
        var piece = SVterm(Rmul(a[i], b[j]), BigInt(i) * BigInt(j));
        out = SVadd(out, piece);
      }
    }
    return out;
  }
  function SVterms(a) {
    var out = [], key;
    for (key in a) if (a.hasOwnProperty(key) && !Rzero(a[key])) out.push({ c: a[key], k: BigInt(key) });
    out.sort(function (p, q) { return p.k < q.k ? -1 : (p.k > q.k ? 1 : 0); });
    return out;
  }
  function SVzero(a) { return SVterms(a).length === 0; }
  function SVrational(a) {
    var t = SVterms(a);
    return t.length === 0 || (t.length === 1 && t[0].k === 1n);
  }
  function SVtoR(a) {
    var t = SVterms(a);
    if (!t.length) return R0;
    if (t.length === 1 && t[0].k === 1n) return t[0].c;
    return null;
  }
  function SVtermtext(t) {
    if (t.k === 1n) return Rtext(t.c);
    var mag = Rabs(t.c);
    var head = Requ(mag, R1) ? '' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')');
    return (Rsign(t.c) < 0 ? '-' : '') + head + 'sqrt(' + t.k + ')';
  }
  function SVtext(a) {
    var t = SVterms(a);
    if (!t.length) return '0';
    var out = '';
    t.forEach(function (item, i) {
      var neg = Rsign(item.c) < 0, mag = Rabs(item.c);
      out += i === 0 ? (neg ? '-' : '') : (neg ? ' - ' : ' + ');
      if (item.k === 1n) out += Rtext(mag);
      else out += (Requ(mag, R1) ? '' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')')) + 'sqrt(' + item.k + ')';
    });
    return out;
  }
  /* The one place this lab uses floating point: a decimal beside an exact
     answer, and the demonstration that sqrt(2) + sqrt(3) is not sqrt(5). Every
     verdict on the page is decided on the exact side. */
  function SVnum(a) {
    var v = 0;
    SVterms(a).forEach(function (t) { v += Rnum(t.c) * Math.sqrt(Number(t.k)); });
    return v;
  }
  function SVsqrt(a) {
    var r = SVtoR(a);
    if (r === null) throw new Error('a square root of something that already contains a root is a nested radical, which this course does not do');
    if (Rsign(r) < 0) throw new Error('sqrt(' + Rtext(r) + ') is not a real number: no real number squares to a negative');
    var s = Rsurd(r);
    return SVterm(s.q, s.k);
  }
  /* Dividing by a surd. One term is cleared by the root itself, two terms by
     the conjugate, and three terms are not cleared by either -- which the
     rationalising mode is built to show rather than to avoid. */
  function SVdiv(a, b) {
    var t = SVterms(b);
    if (!t.length) throw new Error('this divides by zero, and nothing divided by zero has a value');
    if (t.length === 1) {
      var c = t[0].c, k = t[0].k;
      if (k === 1n) return SVmul(a, SVfromR(Rinv(c)));
      /* 1 / (c sqrt(k)) = sqrt(k) / (c k) */
      return SVmul(a, SVterm(Rinv(Rmul(c, R(k))), k));
    }
    if (t.length === 2) {
      var conj = SVadd(SVterm(t[0].c, t[0].k), SVneg(SVterm(t[1].c, t[1].k)));
      var den = SVtoR(SVmul(b, conj));
      if (den === null) throw new Error('the conjugate did not clear this denominator');
      if (Rzero(den)) throw new Error('the denominator times its conjugate is zero, so the denominator was zero');
      return SVmul(SVmul(a, conj), SVfromR(Rinv(den)));
    }
    throw new Error('this denominator has ' + t.length + ' terms; one conjugate clears two of them at a time and cannot clear three in one step');
  }
  function SVof(node) {
    switch (node.k) {
      case 'num': {
        var r = Rread(node.v);
        if (r === null) throw new Error('"' + esc(node.v) + '" is not a number I can read exactly');
        return SVfromR(r);
      }
      case 'var': throw new Error('the letter ' + node.v + ' has no value in this mode');
      case 'neg': return SVneg(SVof(node.a));
      case 'add': return SVadd(SVof(node.a), SVof(node.b));
      case 'sub': return SVsub(SVof(node.a), SVof(node.b));
      case 'mul': return SVmul(SVof(node.a), SVof(node.b));
      case 'div': return SVdiv(SVof(node.a), SVof(node.b));
      case 'pow': {
        var e = SVtoR(SVof(node.b));
        if (e === null || !Rint(e) || e.n < 0n || e.n > 8n) {
          throw new Error('the exponent has to be a whole number from 0 to 8 in this mode');
        }
        var out = SVfromR(R1), base = SVof(node.a);
        for (var i = 0; i < Number(e.n); i += 1) out = SVmul(out, base);
        return out;
      }
      case 'fn': {
        if (node.v === 'sqrt') return SVsqrt(SVof(node.a));
        throw new Error(node.v + '(...) is not part of this lesson; sqrt is');
      }
    }
    throw new Error('I cannot read that expression');
  }
  /* The sign of p + q*sqrt(k), exactly: compare squares when the two parts
     disagree. Used to decide whether a candidate solution is a solution. */
  function signPQ(p, q, k) {
    var sp = Rsign(p), sq = Rsign(q);
    if (sq === 0) return sp;
    if (sp === 0) return sq;
    if (sp === sq) return sp;
    var left = Rmul(p, p), right = Rmul(Rmul(q, q), R(k));
    var c = Rcmp(left, right);
    return sp > 0 ? (c > 0 ? 1 : (c === 0 ? 0 : -1)) : (c > 0 ? -1 : (c === 0 ? 0 : 1));
  }
"""

SR_PRESETS = {
    "simplify": [
        ("sqrt(72)", "72|2"),
        ("sqrt(30)", "30|2"),
        ("sqrt(18/25)", "18/25|2"),
        ("sqrt(1/2)", "1/2|2"),
        ("cbrt(54)", "54|3"),
        ("sqrt(-9)", "-9|2"),
    ],
    "rational": [
        ("8^(2/3)", "8|2|3"),
        ("16^(-3/4)", "16|-3|4"),
        ("(-8)^(1/3)", "-8|1|3"),
        ("(-8)^(2/6)", "-8|2|6"),
        ("2^(1/2)", "2|1|2"),
        ("(-4)^(1/2)", "-4|1|2"),
    ],
    "reduce": [
        ("the 4th root of 9", "9|4"),
        ("the 6th root of 8", "8|6"),
        ("the 12th root of 64", "64|12"),
        ("the 4th root of 16", "16|4"),
        ("the 6th root of 25", "25|6"),
        ("the 6th root of -8", "-8|6"),
    ],
    "operate": [
        ("sqrt(8) + sqrt(18)", "sqrt(8) + sqrt(18)"),
        ("sqrt(2) + sqrt(3)", "sqrt(2) + sqrt(3)"),
        ("3sqrt(12) - sqrt(27)", "3sqrt(12) - sqrt(27)"),
        ("2sqrt(50) - 5sqrt(2) + sqrt(8)", "2sqrt(50) - 5sqrt(2) + sqrt(8)"),
        ("sqrt(2) * sqrt(6)", "sqrt(2) * sqrt(6)"),
        ("(2 + sqrt(3))(2 - sqrt(3))", "(2 + sqrt(3))(2 - sqrt(3))"),
    ],
    "rationalize": [
        ("1 / sqrt(3)", "1|sqrt(3)"),
        ("6 / (2sqrt(3))", "6|2sqrt(3)"),
        ("3 / (2 + sqrt(5))", "3|2 + sqrt(5)"),
        ("(sqrt(2) + 1) / (sqrt(2) - 1)", "sqrt(2) + 1|sqrt(2) - 1"),
        ("1 / (1 + sqrt(2) + sqrt(3))", "1|1 + sqrt(2) + sqrt(3)"),
        ("4 / (3 - sqrt(9))", "4|3 - sqrt(9)"),
    ],
    "solve": [
        ("sqrt(x + 2) = x", "1|2|1|0"),
        ("sqrt(2x + 5) = x + 1", "2|5|1|1"),
        ("sqrt(x + 7) = x + 5", "1|7|1|5"),
        ("sqrt(x - 1) = -3", "1|-1|0|-3"),
        ("sqrt(3x + 1) = 4", "3|1|0|4"),
        ("sqrt(2 - x) = x - 4", "-1|2|1|-4"),
    ],
}

SR_TITLES = {
    "simplify": ("Simplifying a radical", "The factorisation decides what comes out"),
    "rational": ("Rational exponents", "Root first or power first, computed both ways"),
    "reduce": ("Reducing the index", "A common factor in the index and the exponents"),
    "operate": ("Adding radicals", "Like radicals only, once everything is simplified"),
    "rationalize": ("Clearing a denominator", "One term by the root, two by the conjugate"),
    "solve": ("Radical equations", "Square both sides, then check what squaring let in"),
}

SR_LEGEND = {
    "simplify": '<span class="tone-green"><i class="legend-swatch"></i>comes out</span>'
                '<span class="tone-cyan"><i class="legend-swatch"></i>stays in</span>',
    "rational": '<span class="tone-cyan"><i class="legend-swatch"></i>root first</span>'
                '<span class="tone-purple"><i class="legend-swatch"></i>power first</span>',
    "reduce": '<span class="tone-cyan"><i class="legend-swatch"></i>before</span>'
              '<span class="tone-green"><i class="legend-swatch"></i>after</span>',
    "operate": '<span class="tone-cyan"><i class="legend-swatch"></i>a group of like radicals</span>'
               '<span class="tone-red"><i class="legend-swatch"></i>cannot be combined</span>',
    "rationalize": '<span class="tone-cyan"><i class="legend-swatch"></i>the multiplier</span>'
                   '<span class="tone-green"><i class="legend-swatch"></i>rational denominator</span>',
    "solve": '<span class="tone-cyan"><i class="legend-swatch"></i>the radical</span>'
             '<span class="tone-purple"><i class="legend-swatch"></i>the other side</span>'
             '<span class="tone-green"><i class="legend-swatch"></i>a real solution</span>'
             '<span class="tone-red"><i class="legend-swatch"></i>rejected by the check</span>',
}

SR_KPIS = {
    "simplify": ("Comes out", "Stays in", "Exact form"),
    "rational": ("Root first", "Power first", "Agree?"),
    "reduce": ("As given", "Reduced", "Index divided by"),
    "operate": ("Terms in", "Terms out", "Exact value"),
    "rationalize": ("Denominator", "Result", "Steps needed"),
    "solve": ("Candidates", "Solutions", "Extraneous"),
}

SR_HINTS = {
    "simplify": "The radicand may be a whole number or a fraction such as <code>18/25</code>, "
                "and it is allowed to be negative.",
    "rational": "The base may be a fraction and may be negative; p and q are whole numbers with "
                "q at least 2. Try the same exponent written two ways, such as 1/3 and 2/6.",
    "reduce": "A whole number radicand and an index from 2 to 12.",
    "operate": "Write roots as <code>sqrt(8)</code>, coefficients in front of them: "
               "<code>2sqrt(50) - 5sqrt(2)</code>. Products and brackets are allowed.",
    "rationalize": "Numerator and denominator separately. The denominator may have one, two or "
                   "three terms; what happens with three is the point of one preset.",
    "solve": "The equation is <code>sqrt(px + q) = rx + s</code>. Set r to 0 to make the right "
             "side a constant.",
}

SR_PANEL = {
    "simplify": ("Choose a radicand and an index",
                 "The radicand is factorised into primes, and each prime leaves in complete "
                 "groups of the index. Everything below is derived from that one factorisation."),
    "rational": ("Choose a base and an exponent p/q",
                 "The same power is worked out twice: the root taken first, and the power taken "
                 "first. On one of the presets the two do not agree, and that is not a bug."),
    "reduce": ("Choose a radicand and an index",
               "When the index and every exponent in the radicand share a factor, the index "
               "comes down. The result is checked by raising it back."),
    "operate": ("Type a sum of radicals",
                "Every term is simplified first, and only then grouped: sqrt(8) and sqrt(18) are "
                "like terms and do not look it until they are."),
    "rationalize": ("Choose a numerator and a denominator",
                    "The lab looks at the denominator, picks the multiplier that clears it, and "
                    "repeats if one step is not enough."),
    "solve": ("Choose the four coefficients",
              "Squaring both sides is not reversible, so every candidate it produces is "
              "substituted back into the original equation before it counts as a solution."),
}

SR_FIELDS = {
    "simplify": [("srN", "Radicand")],
    "rational": [("srB", "Base b"), ("srP", "p (top of the exponent)"), ("srQ", "q (bottom of the exponent)")],
    "reduce": [("srN", "Radicand")],
    "operate": [("srExpr", "Expression")],
    "rationalize": [("srNum", "Numerator"), ("srDen", "Denominator")],
    "solve": [("srP", "p"), ("srQ", "q"), ("srR", "r"), ("srS", "s")],
}

SR_INDEX_OPTIONS = [("2", "square root"), ("3", "cube root"), ("4", "4th root"),
                    ("5", "5th root"), ("6", "6th root"), ("12", "12th root")]

SR_BODY = {}

SR_PRELUDE = r"""
  var preset = document.getElementById('srPreset');
  var stage = document.getElementById('srStage');
  var work = document.getElementById('srWork');
  var status = document.getElementById('srStatus');
  var subOut = document.getElementById('srSub');
  var kA = document.getElementById('srK1'), kB = document.getElementById('srK2'), kC = document.getElementById('srK3');
  var EXTRA = [], CLEAR = null;
  function kpis(a, b, c) { kA.textContent = a; kB.textContent = b; kC.textContent = c; }
  function fail(lead, detail) {
    if (CLEAR) CLEAR();
    stage.innerHTML = table('nothing computed yet', [step('input', tone(esc(lead), 'red'))]);
    work.innerHTML = '';
    kpis('&mdash;', '&mdash;', '&mdash;');
    status.innerHTML = '<strong>' + lead + '</strong> ' + detail + ' ' + HINT;
  }
"""

SR_BODY["simplify"] = r"""
  var inN = document.getElementById('srN'), idx = document.getElementById('srIdx');
  var INPUTS = [inN];
  EXTRA = [idx];
  function applyPreset(parts) { inN.value = (parts[0] || '').trim(); idx.value = (parts[1] || '2').trim(); }

  function redraw() {
    var r = Rread(inN.value), k = parseInt(idx.value, 10);
    if (r === null) { fail('The radicand has to be a number.', 'A whole number such as 72, or a fraction such as 18/25.'); return; }
    if (!(k >= 2 && k <= 12)) { fail('Choose an index from the list.', 'The index is the small number on the root sign.'); return; }
    var name = rootText(k, Rtext(r));
    subOut.textContent = name;

    if (Rsign(r) < 0 && k % 2 === 0) {
      stage.innerHTML = table('this one has no real value', [
        step('the radical', name),
        step('the radicand', Rtext(r) + ', which is negative'),
        step('the index', k + ', which is even'),
      ]);
      work.innerHTML = table('Why there is nothing to simplify', [
        step('an even power is never negative', 'x^' + k + ' is a product of an even number of copies of x, so the minus signs pair off whatever x is'),
        step('so nothing to the power ' + k + ' is ' + Rtext(r), 'and ' + name + ' is not a real number'),
        step('the odd case is different', rootText(3, Rtext(r)) + ' does exist, because an odd number of negative factors stays negative'),
      ]);
      kpis('&mdash;', '&mdash;', 'not real');
      status.innerHTML = '<strong>' + name + ' is not a real number.</strong> The index is even and '
        + 'the radicand is negative, and no real number raised to an even power comes out negative. '
        + 'This is not the same as the answer being hard to write: there is no real number here to '
        + 'write. Change the index to 3 and the same radicand has an answer.';
      return;
    }

    var neg = Rsign(r) < 0, mag = Rabs(r);
    /* A fractional radicand is turned into a whole one first: the k-th root of
       n/d is the k-th root of n*d^(k-1), over d. That is the rationalising step
       done at the start rather than at the end. */
    var radicand = mag.n * bpow(mag.d, k - 1), outsideDen = mag.d;
    var simp = rootsimp(radicand, k);
    var coef = R(simp.outside, outsideDen);
    if (neg) coef = Rneg(coef);
    var inside = simp.inside;
    var exact = inside === 1n ? Rtext(coef)
      : (Requ(Rabs(coef), R1) ? (Rsign(coef) < 0 ? '-' : '') : Rterm(coef)) + rootText(k, inside);

    var rows = [tr([th('prime'), th('exponent in the radicand'), th('complete groups of ' + k), th('comes out'), th('stays in')])];
    simp.rows.forEach(function (row) {
      rows.push(tr([
        td(String(row.p)), td(String(row.e)), td(String(row.out)),
        td(row.out ? String(row.p) + '^' + row.out : '&mdash;', row.out ? 't' : ''),
        td(row.rest ? String(row.p) + '^' + row.rest : '&mdash;'),
      ], row.out ? 'focus' : ''));
    });
    if (!simp.rows.length) rows.push(tr([tdl('1 has no prime factors'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;')]));

    /* Two routes to the same simplification for a square root: this
       factorisation, and the shared bsqrtsimp helper, which pulls square
       factors out by a different loop. They have to agree. */
    var checkRows = [tr([th('check'), th('what it gives'), th('same?')])];
    var back = Rmul(Rpow(coef, k), R(inside));
    var backOk = Requ(back, r);
    checkRows.push(tr([tdl('raise the answer back to the power ' + k),
      tdl('(' + exact + ')^' + k + ' = ' + Rtext(back)), td(backOk ? 'yes' : 'no', backOk ? 't' : 'f')]));
    if (k === 2) {
      var pair = bsqrtsimp(radicand);
      var alt = R(pair[0], outsideDen);
      var altOk = Requ(Rabs(coef), alt) && pair[1] === inside;
      checkRows.push(tr([tdl('the same radical through the shared square-root simplifier'),
        tdl(Rtext(alt) + ' outside, ' + pair[1] + ' inside'), td(altOk ? 'yes' : 'no', altOk ? 't' : 'f')]));
    }

    var steps = [];
    if (outsideDen !== 1n) {
      steps.push(step('clear the fraction first', rootText(k, Rtext(mag)) + ' = ' + rootText(k, Rtext(mag.n) + ' * ' + Rtext(R(bpow(mag.d, k - 1)))) + ' / ' + Rtext(R(outsideDen))
        + ', because multiplying inside by ' + Rtext(R(bpow(mag.d, k - 1))) + ' makes the bottom a perfect ' + k + 'th power'));
    }
    steps.push(step('factorise the radicand', Rtext(R(radicand)) + ' = '
      + (simp.rows.length ? simp.rows.map(function (row) { return row.p + '^' + row.e; }).join(' * ') : '1')));
    steps.push(step('take out complete groups of ' + k, 'each prime leaves floor(exponent / ' + k + ') copies of itself outside'));
    steps.push(step('what is left inside', String(inside) + (inside === 1n ? ', so the root disappears entirely' : ', which has no ' + k + 'th power factor left')));
    steps.push(step('the exact form', exact));

    stage.innerHTML = table('the radical, simplified from its factorisation', [
      step('as given', name),
      step('exact form', exact),
      step('as a decimal, rounded to 6 places', approx(Rnum(coef) * Math.pow(Number(inside), 1 / k), 6)),
    ]);
    work.innerHTML = table('Every prime in the radicand', rows)
      + table('The steps, in order', steps)
      + table('Checks', checkRows);
    kpis(Rtext(coef), String(inside), exact);

    var msg;
    if (inside === 1n) {
      msg = '<strong>' + name + ' = ' + exact + ' exactly, with no radical left.</strong> Every '
        + 'prime in the radicand had an exponent that was a multiple of ' + k + ', which is what '
        + 'being a perfect ' + k + 'th power means.';
    } else if (Requ(Rabs(coef), R1) && outsideDen === 1n) {
      msg = '<strong>' + name + ' is already as simple as it goes.</strong> No prime in '
        + radicand + ' has an exponent of ' + k + ' or more, so nothing can leave the root. '
        + 'That is a fact about the factorisation, not a failure to spot something: the table '
        + 'above is the whole search.';
    } else {
      msg = '<strong>' + name + ' = ' + exact + '.</strong> The primes that came out did so in '
        + 'complete groups of ' + k + ', because ' + k + ' copies of a prime inside a ' + k
        + 'th root is one copy outside. What is left inside has no such group left, which is what '
        + '"simplified" means &mdash; not "smaller", but "nothing more can leave".';
    }
    if (outsideDen !== 1n) {
      msg += ' The fraction was cleared before any of that, by making the bottom a perfect '
        + k + 'th power. A radical in a denominator is not wrong, but it is not the standard form, '
        + 'and clearing it here is the same move the rationalising mode makes.';
    }
    msg += ' The decimal above is rounded to 6 places and is the only inexact thing on the page.';
    status.innerHTML = msg;
  }
"""

SR_BODY["rational"] = r"""
  var inB = document.getElementById('srB'), inP = document.getElementById('srP'), inQ = document.getElementById('srQ');
  var INPUTS = [inB, inP, inQ];
  function applyPreset(parts) {
    inB.value = (parts[0] || '').trim(); inP.value = (parts[1] || '').trim(); inQ.value = (parts[2] || '').trim();
  }

  function redraw() {
    var b = Rread(inB.value), p = Rread(inP.value), q = Rread(inQ.value);
    if (b === null || p === null || q === null) { fail('b, p and q all have to be numbers.', 'b may be a fraction; p and q must be whole numbers.'); return; }
    if (!Rint(p) || !Rint(q)) { fail('p and q have to be whole numbers.', 'They are the top and bottom of the exponent, not its value.'); return; }
    if (q.n < 2n || q.n > 12n || p.n > 12n || p.n < -12n) {
      fail('Keep q between 2 and 12, and p between -12 and 12.',
        'Outside that range the numbers stop being something a reader can check by hand.');
      return;
    }
    var pi = Number(p.n), qi = Number(q.n);
    var claim = Rterm(b) + '^(' + pi + '/' + qi + ')';
    subOut.textContent = claim;

    /* Route one: take the root first, then the power. Route two: the power
       first, then the root. The exponent law says these are the same number.
       For a negative base they are not always, and that is the lesson. */
    var rootFirst = { value: null, why: null, detail: '' };
    var root = Rnthroot(b, qi);
    if (root === null) {
      rootFirst.why = 'the ' + qi + 'th root of ' + Rtext(b) + ' is not a rational number'
        + (Rsign(b) < 0 && qi % 2 === 0 ? ', and with an even index and a negative radicand it is not a real number at all' : '');
      rootFirst.detail = rootText(qi, Rtext(b)) + ' is not rational, so this route stops here';
    } else if (Rzero(root) && pi < 0) {
      rootFirst.why = 'the root is 0 and the exponent is negative, which divides by zero';
      rootFirst.detail = 'stops at 0^' + pi;
    } else {
      rootFirst.value = Rpow(root, pi);
      rootFirst.detail = rootText(qi, Rtext(b)) + ' = ' + Rtext(root) + ', then ' + Rterm(root) + '^' + (pi < 0 ? '(' + pi + ')' : pi) + ' = ' + Rtext(rootFirst.value);
    }

    var powerFirst = { value: null, why: null, detail: '' };
    var inner = null;
    if (Rzero(b) && pi < 0) {
      powerFirst.why = '0 to a negative power divides by zero';
      powerFirst.detail = 'stops at 0^' + pi;
    } else {
      inner = Rpow(b, pi);
      var outer = Rnthroot(inner, qi);
      if (outer === null) {
        powerFirst.why = 'the ' + qi + 'th root of ' + Rtext(inner) + ' is not a rational number'
          + (Rsign(inner) < 0 && qi % 2 === 0 ? ', and with an even index and a negative radicand it is not a real number at all' : '');
        powerFirst.detail = Rterm(b) + '^' + (pi < 0 ? '(' + pi + ')' : pi) + ' = ' + Rtext(inner) + ', and ' + rootText(qi, Rtext(inner)) + ' is not rational';
      } else {
        powerFirst.value = outer;
        powerFirst.detail = Rterm(b) + '^' + (pi < 0 ? '(' + pi + ')' : pi) + ' = ' + Rtext(inner) + ', then ' + rootText(qi, Rtext(inner)) + ' = ' + Rtext(outer);
      }
    }

    var both = rootFirst.value !== null && powerFirst.value !== null;
    var agree = both && Requ(rootFirst.value, powerFirst.value);
    var reduced = R(p.n, q.n);

    var rows = [tr([th('route'), th('what it does'), th('answer')])];
    rows.push(tr([tdl('the root first: (' + rootText(qi, 'b') + ')^p'), tdl(rootFirst.detail),
      td(rootFirst.value === null ? tone(esc(rootFirst.why), 'red') : tone(Rtext(rootFirst.value), 'cyan'))]));
    rows.push(tr([tdl('the power first: ' + rootText(qi, 'b^p')), tdl(powerFirst.detail),
      td(powerFirst.value === null ? tone(esc(powerFirst.why), 'red') : tone(Rtext(powerFirst.value), 'purple'))], 'focus'));

    /* When neither route is rational the answer is still exact for a square
       root, and otherwise it is genuinely irrational and the decimal says so. */
    var surdText = null;
    if (!both && qi === 2 && inner !== null && Rsign(inner) >= 0) {
      var s = Rsurd(inner);
      surdText = surdtext(s);
    }
    var decimal = null;
    if (!both) {
      var bv = Rnum(b);
      var dv = (bv < 0 && qi % 2 === 0) ? NaN : (bv < 0 ? -Math.pow(-bv, pi / qi) : Math.pow(bv, pi / qi));
      decimal = isFinite(dv) ? approx(dv, 6) : 'not a real number';
    }

    var extra = [tr([th('question'), th('answer')])];
    extra.push(tr([tdl('is the exponent in lowest terms?'), tdl(Requ(reduced, R(p.n, q.n)) && (Rabs(reduced).n !== p.n || reduced.d !== q.n)
      ? pi + '/' + qi + ' reduces to ' + Rtext(reduced) + ', and the two forms are the same rational number'
      : pi + '/' + qi + ' is already in lowest terms')]));
    extra.push(tr([tdl('what the exponent law claims'), tdl('b^(p/q) means the same thing whichever way round it is taken, so long as the root exists')]));
    if (surdText) extra.push(tr([tdl('the exact value as a surd'), tdl(surdText)]));
    if (decimal) extra.push(tr([tdl('as a decimal, rounded to 6 places'), tdl(decimal)]));

    stage.innerHTML = table('one power, two routes', [
      step('the power', claim),
      step('root first', rootFirst.value === null ? tone(esc(rootFirst.why), 'red') : Rtext(rootFirst.value)),
      step('power first', powerFirst.value === null ? tone(esc(powerFirst.why), 'red') : Rtext(powerFirst.value)),
      step('the same?', both ? (agree ? '<span class="chip ok">yes</span>' : '<span class="chip no">no</span>')
        : '<span class="chip">one route has no answer</span>'),
    ]);
    work.innerHTML = table('The two routes', rows) + table('What that leaves', extra);
    kpis(rootFirst.value === null ? 'none' : Rtext(rootFirst.value),
      powerFirst.value === null ? 'none' : Rtext(powerFirst.value),
      both ? (agree ? 'yes' : 'no') : 'one route fails');

    var msg;
    if (both && agree) {
      msg = '<strong>' + claim + ' = ' + Rtext(rootFirst.value) + ', by either route.</strong> '
        + 'Taking the root first keeps the numbers small, which is the only reason to prefer it: '
        + qi + 'th root then power, or power then ' + qi + 'th root, is the same number here.';
    } else if (both && !agree) {
      msg = '<strong>The two routes disagree: ' + Rtext(rootFirst.value) + ' one way and '
        + Rtext(powerFirst.value) + ' the other.</strong> That is what a negative base does to a '
        + 'fractional exponent, and it is why b^(p/q) is defined only for b at least 0 once q is '
        + 'even. Nothing here is a rounding error; both answers are exact, and the notation is what '
        + 'is at fault.';
    } else if (Rsign(b) < 0 && qi % 2 === 0) {
      msg = '<strong>' + claim + ' has no real value taken as a root of a negative number.</strong> '
        + 'The route that squares first does have an answer, because squaring destroyed the sign '
        + 'before the root was taken. Writing the same exponent as ' + Rtext(reduced) + ' would '
        + 'give a third story. This is the reason textbooks require a non-negative base before '
        + 'they allow fractional exponents at all.';
    } else if (rootFirst.value === null && powerFirst.value === null) {
      msg = '<strong>' + claim + ' is irrational.</strong> Neither route lands on a fraction: '
        + esc(rootFirst.why) + '. '
        + (surdText ? 'Exactly, it is ' + surdText + '. ' : '')
        + 'The decimal above is a rounding of it and not the number itself.';
    } else {
      msg = '<strong>One route works and the other does not.</strong> ' + claim + ' is '
        + (rootFirst.value !== null ? Rtext(rootFirst.value) + ' taking the root first' : Rtext(powerFirst.value) + ' taking the power first')
        + ', while the other route runs into: ' + esc(rootFirst.why || powerFirst.why) + '.';
    }
    status.innerHTML = msg;
  }
"""

SR_BODY["reduce"] = r"""
  var inN = document.getElementById('srN'), idx = document.getElementById('srIdx');
  var INPUTS = [inN];
  EXTRA = [idx];
  function applyPreset(parts) { inN.value = (parts[0] || '').trim(); idx.value = (parts[1] || '2').trim(); }
  function gcdInt(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }

  function redraw() {
    var r = Rread(inN.value), k = parseInt(idx.value, 10);
    if (r === null || !Rint(r)) { fail('The radicand has to be a whole number here.', 'Index reduction is about the exponents in its factorisation.'); return; }
    if (!(k >= 2 && k <= 12)) { fail('Choose an index from the list.', 'The index is the small number on the root sign.'); return; }
    var name = rootText(k, Rtext(r));
    subOut.textContent = name;

    if (Rsign(r) < 0 && k % 2 === 0) {
      stage.innerHTML = table('nothing to reduce', [
        step('the radical', name),
        step('why not', 'an even index and a negative radicand: there is no real number here'),
      ]);
      work.innerHTML = table('Why the reduction cannot even start', [
        step('the value does not exist', name + ' is not a real number, because an even power is never negative'),
        step('and the reduction would hide that', 'if the index and the exponents shared a factor, cancelling it would produce an odd index, which DOES have a value: ' + rootText(3, Rtext(r)) + ' = ' + (bnthroot(r.n, 3) === null ? 'irrational' : String(bnthroot(r.n, 3)))),
        step('so the rule needs its condition', 'index reduction is stated for a non-negative radicand, and this is the case that shows why'),
      ]);
      kpis(name, 'no real value', '&mdash;');
      status.innerHTML = '<strong>' + name + ' is not a real number, so there is nothing to reduce.</strong> '
        + 'This preset is here because the cancelling looks so harmless: the index ' + k + ' and the '
        + 'exponents in ' + Rtext(Rabs(r)) + ' do share a factor, and cancelling it would leave a root '
        + 'that has a perfectly good value. The two are not equal, because the first one does not '
        + 'exist. The rule that lets an index be reduced is stated for radicands that are not '
        + 'negative, and this is what that condition is protecting.';
      return;
    }

    var mag = Rabs(r);
    var factors = bfactorise(mag.n);
    var g = k;
    factors.forEach(function (pair) { g = gcdInt(g, pair[1]); });
    if (!factors.length) g = k;
    var newIndex = k / g;
    var newRadicand = 1n;
    factors.forEach(function (pair) { newRadicand *= bpow(pair[0], pair[1] / g); });

    var rows = [tr([th('prime'), th('exponent'), th('exponent divided by ' + g), th('in the reduced radicand')])];
    factors.forEach(function (pair) {
      rows.push(tr([td(String(pair[0])), td(String(pair[1])), td(String(pair[1] / g)),
        td(String(pair[0]) + '^' + (pair[1] / g))], g > 1 ? 'focus' : ''));
    });
    if (!factors.length) rows.push(tr([tdl('1 has no prime factors'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;')]));

    var before = name, after = newIndex === 1 ? Rtext(R(newRadicand)) : rootText(newIndex, newRadicand);
    /* The check: raise the reduced radical back to the reduced index, and
       raise the whole thing to the original index. Both have to land on the
       radicand, and both are integer arithmetic. */
    var backOne = bpow(newRadicand, g);
    var checkRows = [tr([th('check'), th('what it gives'), th('the radicand'), th('same?')])];
    checkRows.push(tr([tdl('raise the reduced radicand to the power ' + g),
      td(String(newRadicand) + '^' + g + ' = ' + String(backOne)), td(String(mag.n)),
      td(backOne === mag.n ? 'yes' : 'no', backOne === mag.n ? 't' : 'f')]));
    var perfect = bnthroot(mag.n, k);
    if (perfect !== null && k % 2 === 0) {
      var negBack = bpow(-perfect, k);
      checkRows.push(tr([tdl('the other number whose ' + k + 'th power is ' + mag.n),
        td('(-' + perfect + ')^' + k + ' = ' + String(negBack)), td(String(mag.n)),
        td(negBack === mag.n ? 'yes' : 'no', negBack === mag.n ? 't' : 'f')]));
    }

    stage.innerHTML = table('the same number, with a smaller index', [
      step('as given', before),
      step('the common factor', g === 1 ? 'the index and the exponents share nothing: 1' : String(g)),
      step('reduced', after),
      step('as a decimal, rounded to 6 places', approx(Math.pow(Number(mag.n), 1 / k) * (Rsign(r) < 0 ? -1 : 1), 6)),
    ]);
    work.innerHTML = table('The factorisation, and what the common factor does to it', rows)
      + table('Checks', checkRows);
    kpis(before, after, String(g));

    var msg;
    if (g === 1) {
      msg = '<strong>' + before + ' cannot have its index reduced.</strong> The index ' + k
        + ' and the exponents in the factorisation of ' + mag.n + ' have no common factor bigger '
        + 'than 1, so there is nothing to cancel. An index comes down only when every exponent '
        + 'inside can be divided by the same number as the index.';
    } else {
      msg = '<strong>' + before + ' = ' + after + '.</strong> The index and every exponent inside '
        + 'shared the factor ' + g + ', and dividing both by it leaves the same number written '
        + 'with a smaller root. In rational-exponent form that is the whole argument: '
        + mag.n + '^(1/' + k + ') is ' + newRadicand + '^(' + g + '/' + k + ') = '
        + newRadicand + '^(1/' + newIndex + '), and the fraction in the exponent was simply not in '
        + 'lowest terms.';
    }
    if (perfect !== null && k % 2 === 0) {
      msg += ' Notice the second check: (-' + perfect + ')^' + k + ' is also ' + mag.n + ', and '
        + name + ' is still ' + perfect + ' and not -' + perfect + '. An even root is defined to be '
        + 'the non-negative one, which is why the general rule for an even index carries an '
        + 'absolute value.';
    }
    status.innerHTML = msg;
  }
"""

SR_BODY["operate"] = r"""
  var input = document.getElementById('srExpr');
  var INPUTS = [input];
  function applyPreset(parts) { input.value = (parts[0] || '').trim(); }

  function redraw() {
    var src = input.value.trim();
    subOut.textContent = src || 'nothing typed yet';
    if (!src) { fail('Type a sum of radicals.', 'The box is empty, so there is nothing to combine.'); return; }
    var tree;
    try { tree = Eparse(src); }
    catch (err) { fail('That expression does not parse.', esc(err.message) + '.'); return; }
    var result;
    try { result = SVof(tree); }
    catch (err) { fail('I can read that, but not evaluate it exactly.', esc(err.message) + '.'); return; }

    /* Every term is simplified BEFORE anything is grouped, because that is the
       step that makes sqrt(8) and sqrt(18) like terms. Grouping first and
       simplifying afterwards finds nothing to group. */
    var pieces = Esplit(tree, 1, []), rows = [tr([th('term as written'), th('simplified'), th('coefficient'), th('the radical it is a multiple of')])];
    var flat = [], trouble = null;
    pieces.forEach(function (item, i) {
      var sv;
      try { sv = SVof(item.node); }
      catch (err) { trouble = err.message; return; }
      if (item.sign < 0) sv = SVneg(sv);
      var terms = SVterms(sv);
      terms.forEach(function (t) { flat.push(t); });
      rows.push(tr([
        tdl((item.sign < 0 ? '-' : '') + Eshow(item.node, null, '')),
        tdl(SVtext(sv)),
        tdl(terms.map(function (t) { return Rtext(t.c); }).join(', ') || '0'),
        tdl(terms.map(function (t) { return t.k === 1n ? 'no radical' : 'sqrt(' + t.k + ')'; }).join(', ') || '&mdash;'),
      ]));
    });
    if (trouble) { fail('One of the terms could not be evaluated exactly.', esc(trouble) + '.'); return; }

    var groups = {}, order = [];
    flat.forEach(function (t) {
      var key = String(t.k);
      if (!groups[key]) { groups[key] = { list: [], k: t.k }; order.push(key); }
      groups[key].list.push(t);
    });
    var groupRows = [tr([th('radical'), th('coefficients'), th('added'), th('the single term'), th('combined?')])];
    order.forEach(function (key) {
      var g = groups[key], sum = R0;
      g.list.forEach(function (t) { sum = Radd(sum, t.c); });
      groupRows.push(tr([
        td(g.k === 1n ? 'no radical' : 'sqrt(' + g.k + ')'),
        tdl(g.list.map(function (t) { return Rtext(t.c); }).join(', ')),
        tdl(g.list.map(function (t) { return Rtext(t.c); }).join(' + ') + ' = ' + Rtext(sum)),
        tdl(Rzero(sum) ? '0, this group cancels' : SVtermtext({ c: sum, k: g.k })),
        tdl(g.list.length > 1 ? '<span class="chip ok">yes, ' + g.list.length + ' like terms</span>'
                              : '<span class="chip">nothing else is like it</span>'),
      ], g.list.length > 1 ? 'focus' : ''));
    });

    /* An approximate check, and it is labelled as one: the parse tree is
       evaluated in floating point and compared with the exact answer. Different
       arithmetic, same number to ten places, or something above is wrong. */
    var floatValue = NaN;
    try { floatValue = Eeval(tree, {}); } catch (err) { floatValue = NaN; }
    var exactValue = SVnum(result);
    var close = isFinite(floatValue) && Math.abs(floatValue - exactValue) < 1e-9 * (1 + Math.abs(exactValue));
    var checkRows = [tr([th('route'), th('value'), th('agree to 9 places?')])];
    checkRows.push(tr([tdl('the exact answer, ' + SVtext(result) + ', as a decimal'), td(approx(exactValue, 9)), td(close ? 'yes' : 'no', close ? 't' : 'f')]));
    checkRows.push(tr([tdl('the expression as typed, evaluated in floating point'), td(approx(floatValue, 9)), td(close ? 'yes' : 'no', close ? 't' : 'f')]));

    var irr = SVterms(result).filter(function (t) { return t.k !== 1n; });
    if (irr.length >= 2) {
      var k1 = Number(irr[0].k), k2 = Number(irr[1].k);
      checkRows.push(tr([
        tdl('the collapse that is not allowed: sqrt(' + k1 + ') + sqrt(' + k2 + ') against sqrt(' + (k1 + k2) + ')'),
        td(approx(Math.sqrt(k1) + Math.sqrt(k2), 6) + ' against ' + approx(Math.sqrt(k1 + k2), 6)),
        td('no', 'f'),
      ], 'focus'));
    }

    stage.innerHTML = table('the sum, simplified then collected', [
      step('as written', esc(src)),
      step('terms as written', String(pieces.length)),
      step('exact value', SVtext(result)),
      step('terms in the answer', String(SVterms(result).length)),
      step('as a decimal, rounded to 9 places', approx(exactValue, 9)),
    ]);
    work.innerHTML = table('Each term, simplified first', rows)
      + table('Then grouped: only identical radicals may be added', groupRows)
      + table('Checks', checkRows);
    kpis(String(pieces.length), String(SVterms(result).length), SVtext(result));

    var combined = order.filter(function (key) { return groups[key].list.length > 1; }).length;
    var msg = '<strong>' + esc(src) + ' = ' + SVtext(result) + ' exactly.</strong> ';
    if (SVrational(result) && !SVzero(result)) {
      msg += 'Every radical cancelled: the answer is a plain rational number even though the '
        + 'expression is full of roots. A product of two irrational numbers is perfectly capable '
        + 'of being rational, and that is what a conjugate pair is for.';
    } else if (!combined) {
      msg += 'Nothing could be combined. The radicals in this expression are different after '
        + 'simplifying, and different radicals are as unlike as x and y: there is no rule that '
        + 'turns sqrt(2) + sqrt(3) into a single root, and the decimals above show that sqrt(5) '
        + 'is not it.';
    } else {
      msg += 'Simplifying came first, and that is the whole trick: the terms that got combined did '
        + 'not look like each other as written. Once every radicand has had its square factors '
        + 'taken out, like radicals are the ones with the same number under the root, and their '
        + 'coefficients add exactly the way like terms in x do.';
    }
    msg += close
      ? ' The floating-point check agrees to nine places, which is evidence and not proof; the '
        + 'answer above was computed exactly and is not a rounding of anything.'
      : ' The floating-point check does NOT agree, which means something above needs looking at.';
    status.innerHTML = msg;
  }
"""

SR_BODY["rationalize"] = r"""
  var inNum = document.getElementById('srNum'), inDen = document.getElementById('srDen');
  var INPUTS = [inNum, inDen];
  function applyPreset(parts) { inNum.value = (parts[0] || '').trim(); inDen.value = (parts[1] || '').trim(); }

  function redraw() {
    var ns = inNum.value.trim(), ds = inDen.value.trim();
    subOut.textContent = '(' + (ns || '?') + ') / (' + (ds || '?') + ')';
    if (!ns || !ds) { fail('Both halves are needed.', 'Put an expression in each box; a plain number is a perfectly good numerator.'); return; }
    var num, den;
    try { num = SVof(Eparse(ns)); den = SVof(Eparse(ds)); }
    catch (err) { fail('One of the two did not come out.', esc(err.message) + '.'); return; }

    if (SVzero(den)) {
      stage.innerHTML = table('there is nothing to rationalise', [
        step('numerator', SVtext(num)),
        step('denominator as written', esc(ds)),
        step('denominator simplified', '0'),
      ]);
      work.innerHTML = table('Why this one stops before it starts', [
        step('simplify the denominator first', esc(ds) + ' = ' + SVtext(den)),
        step('and it is zero', 'sqrt(9) is 3, not an unresolved radical, so this denominator is 3 - 3'),
        step('so the fraction has no value', 'no multiplier will fix that: rationalising changes how a number is written, and this is not a number'),
      ]);
      kpis('0', 'undefined', '&mdash;');
      status.innerHTML = '<strong>The denominator is zero, so there is no fraction here to '
        + 'rationalise.</strong> It does not look like zero, which is the point: a radical whose '
        + 'radicand is a perfect square is a plain number in disguise, and simplifying the '
        + 'denominator before doing anything else is what catches it. Reaching for the conjugate '
        + 'first would have produced a confident answer to a question with no answer.';
      return;
    }

    /* The algorithm, run rather than described: while the denominator has more
       than one term, multiply top and bottom by the sign-flipped last term.
       That is what "the conjugate" is, and it is not guaranteed to finish in
       one step -- which is exactly what the three-term preset shows. */
    var steps = [], n = num, d = den, rounds = 0;
    while (SVterms(d).length > 1 && rounds < 4) {
      rounds += 1;
      var t = SVterms(d);
      var last = SVterm(t[t.length - 1].c, t[t.length - 1].k);
      var rest = SVsub(d, last);
      var mult = SVsub(rest, last);
      var nd = SVmul(d, mult);
      steps.push([
        'step ' + rounds + ': the denominator has ' + t.length + ' terms',
        'multiply top and bottom by ' + SVtext(mult) + ', which flips the sign of the last term. '
          + '(' + SVtext(d) + ')(' + SVtext(mult) + ') = ' + SVtext(nd)
          + ', because the cross terms cancel and squares are left'
      ]);
      n = SVmul(n, mult);
      d = nd;
    }
    var singleTerm = SVterms(d);
    if (singleTerm.length === 1 && singleTerm[0].k !== 1n) {
      var k = singleTerm[0].k;
      var mult2 = SVterm(R1, k);
      steps.push([
        'step ' + (rounds + 1) + ': one radical left on the bottom',
        'multiply top and bottom by sqrt(' + k + '): (' + SVtext(d) + ')(sqrt(' + k + ')) = '
          + SVtext(SVmul(d, mult2)) + ', because sqrt(' + k + ') times itself is ' + k
      ]);
      n = SVmul(n, mult2);
      d = SVmul(d, mult2);
      rounds += 1;
    }

    var denR = SVtoR(d);
    var finished = denR !== null;
    var result = null;
    if (finished && !Rzero(denR)) result = SVmul(n, SVfromR(Rinv(denR)));

    var rows = steps.map(function (pair) { return step(pair[0], pair[1]); });
    rows.unshift(step('start', SVtext(num) + '  over  ' + SVtext(den)));
    if (finished) {
      rows.push(step('the denominator is now rational', SVtext(n) + '  over  ' + Rtext(denR)));
      rows.push(step('divide through', SVtext(result)));
    } else {
      rows.push(step('still not rational', 'after ' + rounds + ' step(s) the denominator is '
        + SVtext(d) + ', which still contains a root'));
    }

    /* Approximate check, labelled: the original fraction and the answer in
       floating point. Rationalising must not change the number. */
    var before = SVnum(num) / SVnum(den);
    var after = result === null ? NaN : SVnum(result);
    var close = isFinite(after) && Math.abs(before - after) < 1e-9 * (1 + Math.abs(before));
    var checkRows = [tr([th('form'), th('as a decimal, rounded to 9 places'), th('same number?')])];
    checkRows.push(tr([tdl('as typed: ' + SVtext(num) + ' over ' + SVtext(den)), td(approx(before, 9)), td(close ? 'yes' : 'no', close ? 't' : 'f')]));
    checkRows.push(tr([tdl('rationalised: ' + (result === null ? 'not reached' : SVtext(result))), td(approx(after, 9)), td(close ? 'yes' : 'no', close ? 't' : 'f')]));

    stage.innerHTML = table('the same number, with nothing irrational underneath', [
      step('as typed', SVtext(num) + '  over  ' + SVtext(den)),
      step('terms in the denominator', String(SVterms(den).length)),
      step('rationalised', result === null ? tone('not reached in ' + rounds + ' steps', 'red') : SVtext(result)),
    ]);
    work.innerHTML = table('Clearing the denominator, one multiplier at a time', rows)
      + table('Checks', checkRows);
    kpis(SVtext(den), result === null ? 'not reached' : SVtext(result), String(rounds));

    var msg;
    if (result === null) {
      msg = '<strong>Four rounds of conjugates did not clear this denominator.</strong> The trick '
        + 'is not magic: multiplying by a conjugate turns a difference of two things into a '
        + 'difference of their squares, and each round can only deal with two terms at a time.';
    } else if (SVterms(den).length === 1) {
      msg = '<strong>' + SVtext(num) + ' over ' + SVtext(den) + ' = ' + SVtext(result) + '.</strong> '
        + 'With a single radical underneath, the multiplier is that radical itself: sqrt(k) times '
        + 'sqrt(k) is k, and k is rational. Nothing has been approximated and the number has not '
        + 'changed &mdash; only the way it is written.';
    } else if (rounds === 1) {
      msg = '<strong>' + SVtext(num) + ' over ' + SVtext(den) + ' = ' + SVtext(result) + '.</strong> '
        + 'The conjugate works because (a + b)(a - b) = a^2 - b^2 and squaring a square root '
        + 'removes it. The cross terms are what cancel, and they cancel because the two middle '
        + 'products differ only in sign.';
    } else {
      msg = '<strong>' + SVtext(num) + ' over ' + SVtext(den) + ' = ' + SVtext(result)
        + ', after ' + rounds + ' steps.</strong> One conjugate was not enough: with three terms '
        + 'underneath, the first multiplier pairs two of them off and leaves a shorter denominator, '
        + 'and the process then repeats on what is left. The one-step conjugate rule is the '
        + 'two-term case of this, not the whole of it.';
    }
    msg += close
      ? ' The decimal check agrees to nine places, which is a check and not the computation: every '
        + 'step above was done in exact arithmetic.'
      : ' The decimal check does not agree, which means something above needs looking at.';
    status.innerHTML = msg;
  }
"""

SR_BODY["solve"] = r"""
  var inP = document.getElementById('srP'), inQ = document.getElementById('srQ');
  var inR = document.getElementById('srR'), inS = document.getElementById('srS');
  var INPUTS = [inP, inQ, inR, inS];
  var svg = document.getElementById('srPlot');
  CLEAR = function () { svg.textContent = ''; };
  function applyPreset(parts) {
    inP.value = (parts[0] || '').trim(); inQ.value = (parts[1] || '').trim();
    inR.value = (parts[2] || '').trim(); inS.value = (parts[3] || '').trim();
  }
  /* The sign of a candidate, exactly. A candidate is carried as a sum of surds,
     so this decides p + q*sqrt(k) against 0 by comparing squares. */
  function svSign(v) {
    var t = SVterms(v);
    if (!t.length) return 0;
    if (t.length === 1) return t[0].k === 1n ? Rsign(t[0].c) : Rsign(t[0].c);
    if (t.length === 2 && t[0].k === 1n) return signPQ(t[0].c, t[1].c, t[1].k);
    return null;
  }

  function redraw() {
    var p = Rread(inP.value), q = Rread(inQ.value), r = Rread(inR.value), s = Rread(inS.value);
    if (p === null || q === null || r === null || s === null) {
      fail('All four coefficients have to be numbers.', 'Whole numbers or fractions; r may be 0.');
      return;
    }
    var lhsText = 'sqrt(' + Ptext([q, p]) + ')', rhsText = Ptext([s, r]);
    var eq = lhsText + ' = ' + rhsText;
    subOut.textContent = eq;
    if (Rzero(p) && Rzero(r)) {
      fail('With p = 0 and r = 0 there is no equation in x.',
        'Both sides are constants, so nothing is being solved. Give p or r a value.');
      return;
    }

    /* Squaring: (rx + s)^2 = px + q, collected as r^2 x^2 + (2rs - p) x + (s^2 - q) = 0. */
    var A = Rmul(r, r), B = Rsub(Rmul(R(2n), Rmul(r, s)), p), C = Rsub(Rmul(s, s), q);
    var squared = Ptext([C, B, A]) + ' = 0';
    var candidates = [], degenerate = null, disc = null;
    if (Rzero(A)) {
      if (Rzero(B)) {
        degenerate = Rzero(C)
          ? 'after squaring, every x satisfies the squared equation, so the check below is the only thing deciding anything'
          : 'after squaring, the equation says ' + Rtext(C) + ' = 0, which is false, so the squared equation has no solution at all';
      } else {
        candidates.push(SVfromR(Rdiv(Rneg(C), B)));
      }
    } else {
      var roots = quadroots(A, B, C);
      disc = roots.disc;
      if (roots.kind === 'complex') {
        degenerate = 'the discriminant of the squared equation is ' + Rtext(roots.disc)
          + ', which is negative, so even the squared equation has no real solution';
      } else if (roots.kind === 'double') {
        candidates.push(SVfromR(roots.p));
      } else if (roots.kind === 'rational') {
        roots.roots.forEach(function (x) { candidates.push(SVfromR(x)); });
      } else {
        candidates.push(SVadd(SVfromR(roots.p), SVterm(roots.s.q, roots.s.k)));
        candidates.push(SVsub(SVfromR(roots.p), SVterm(roots.s.q, roots.s.k)));
      }
    }

    /* Each candidate goes back into the ORIGINAL equation. Squaring is not
       reversible: it turns -2 = 2 into 4 = 4, and this is where that shows up. */
    var rows = [tr([th('candidate x'), th('the radicand px + q'), th('the left side'), th('the right side'), th('equal?')])];
    var good = [], bad = [];
    candidates.forEach(function (x) {
      var radicand = SVadd(SVmul(SVfromR(p), x), SVfromR(q));
      var rhs = SVadd(SVmul(SVfromR(r), x), SVfromR(s));
      var rhsSign = svSign(rhs), radSign = svSign(radicand);
      var lhs = null, why = '';
      try { lhs = SVsqrt(radicand); } catch (err) { lhs = null; why = err.message; }
      var ok;
      if (radSign !== null && radSign < 0) {
        ok = false;
        why = 'the radicand is negative, so the left side is not a real number';
      } else if (lhs !== null) {
        ok = SVzero(SVsub(lhs, rhs));
        if (!ok) why = 'the square root is never negative, and the right side here is';
      } else {
        /* An irrational candidate: it satisfies the squared equation, so the
           left side squared IS the right side squared. The only question left
           is the sign of the right side, and that is decided exactly. */
        ok = rhsSign !== null && rhsSign >= 0;
        why = ok ? 'the two sides have equal squares and the right side is not negative'
                 : 'the two sides have equal squares, but the right side is negative and a square root is not';
      }
      (ok ? good : bad).push(x);
      rows.push(tr([
        td(SVtext(x)), td(SVtext(radicand)),
        td(lhs === null ? 'sqrt(' + SVtext(radicand) + ')' : SVtext(lhs)),
        td(SVtext(rhs)),
        td(ok ? 'yes' : 'no', ok ? 't' : 'f'),
      ], ok ? 'focus' : ''));
    });
    if (!candidates.length) rows.push(tr([tdl(degenerate || 'no candidates'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;'), tdl('&mdash;')]));

    var steps = [
      step('the equation', eq),
      step('square both sides', '(' + rhsText + ')^2 = ' + Ptext([q, p])),
      step('collect', squared),
    ];
    if (disc !== null) steps.push(step('the discriminant of that quadratic', Rtext(disc)));
    steps.push(step('candidates it produces', candidates.length
      ? candidates.map(SVtext).join(',   ') : 'none: ' + (degenerate || 'the squared equation gave nothing')));
    steps.push(step('why a check is not optional', 'squaring turns a false statement into a true one: '
      + '-2 = 2 is false, and squaring it gives 4 = 4. Every candidate above has to go back into '
      + 'the original equation, and the ones that fail were never solutions of it'));

    /* The picture: the radical and the line, both evaluated, with the genuine
       intersections filled and the rejected candidates hollow. A rejected
       candidate is drawn where the reader expected a crossing and there is
       none. */
    var pv = Rnum(p), qv = Rnum(q), rv = Rnum(r), sv = Rnum(s);
    var f = function (x) { var t = pv * x + qv; return t < 0 ? NaN : Math.sqrt(t); };
    var g = function (x) { return rv * x + sv; };
    var xs = [];
    candidates.forEach(function (x) { xs.push(SVnum(x)); });
    if (!Rzero(p)) xs.push(-qv / pv);
    xs.push(0);
    var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs);
    if (hi - lo < 2) { lo -= 2; hi += 2; }
    var padx = (hi - lo) * 0.35 + 0.5;
    var xmin = lo - padx, xmax = hi + padx;
    var ys = [];
    for (var i = 0; i <= 60; i += 1) {
      var xx = xmin + (xmax - xmin) * i / 60;
      var yy = f(xx);
      if (isFinite(yy)) ys.push(yy);
      ys.push(g(xx));
    }
    var ylo = Math.min.apply(null, ys), yhi = Math.max.apply(null, ys);
    var pady = Math.max(1, (yhi - ylo) * 0.2);
    var plot = Plot(svg, { xmin: xmin, xmax: xmax, ymin: ylo - pady, ymax: yhi + pady });
    plot.frame();
    plot.curve(f, 'plot-curve');
    plot.curve(g, 'plot-curve alt');
    good.forEach(function (x) { plot.point(SVnum(x), SVnum(SVadd(SVmul(SVfromR(r), x), SVfromR(s))), 'plot-point root', 'x = ' + SVtext(x)); });
    bad.forEach(function (x) {
      var xv = SVnum(x);
      plot.hole(xv, g(xv));
      plot.label(xv, g(xv) - (yhi - ylo) * 0.08, 'rejected: x = ' + SVtext(x));
      if (isFinite(f(xv))) plot.segment(xv, g(xv), xv, f(xv), 'plot-aux');
    });
    plot.describe('The curve ' + lhsText + ' and the line ' + rhsText + ' drawn by evaluating both, with '
      + good.length + ' genuine crossing(s) filled and ' + bad.length + ' rejected candidate(s) hollow.');

    stage.innerHTML = table('the equation, and what squaring produced', [
      step('the equation', eq),
      step('after squaring', squared),
      step('candidates', candidates.length ? candidates.map(SVtext).join(',   ') : 'none'),
      step('solutions', good.length ? good.map(SVtext).join(',   ') : 'none'),
      step('rejected by the check', bad.length ? bad.map(SVtext).join(',   ') : 'none'),
    ]);
    work.innerHTML = table('Solving', steps)
      + table('The check, in the original equation', rows);
    kpis(String(candidates.length), String(good.length), String(bad.length));

    var msg;
    if (!candidates.length) {
      msg = '<strong>' + eq + ' has no solution.</strong> ' + (degenerate ? degenerate.charAt(0).toUpperCase() + degenerate.slice(1) : 'The squared equation produced no candidate')
        + '. Squaring can only add solutions, never lose them, so a squared equation with nothing '
        + 'in it settles the original equation as well.';
    } else if (!good.length) {
      msg = '<strong>' + eq + ' has no solution, and squaring said otherwise.</strong> It produced '
        + candidates.length + ' candidate' + (candidates.length === 1 ? '' : 's') + ' &mdash; '
        + candidates.map(SVtext).join(', ') + ' &mdash; and every one of them fails in the original '
        + 'equation. A square root is never negative, and the right side at those values is. '
        + 'Stopping at the squared equation would have produced confident wrong answers here, which '
        + 'is why the check is part of the method and not a formality.';
    } else if (!bad.length) {
      msg = '<strong>' + eq + ' has ' + (good.length === 1 ? 'one solution, x = ' : 'the solutions x = ')
        + good.map(SVtext).join(' and x = ') + ', and nothing was extraneous.</strong> The check '
        + 'still had to be done: it is not possible to tell in advance which candidates a squaring '
        + 'invented, and the only way to know is to put them back.';
    } else {
      msg = '<strong>' + eq + ': x = ' + good.map(SVtext).join(' and x = ') + ' solve it, and x = '
        + bad.map(SVtext).join(', ') + ' do' + (bad.length === 1 ? 'es' : '') + ' not.</strong> '
        + 'The rejected value satisfies the SQUARED equation perfectly, which is exactly the '
        + 'problem: squaring both sides is not a reversible move, and it merges the equation with '
        + 'the one where the right side has the opposite sign. On the graph it is drawn hollow, at '
        + 'the point where the line is but the curve is not.';
    }
    status.innerHTML = msg;
  }
"""

SR_WIRE = r"""
  preset.addEventListener('change', function () { applyPreset(preset.value.split('|')); redraw(); });
  EXTRA.forEach(function (el) { el.addEventListener('change', redraw); });
  INPUTS.forEach(function (el) { el.addEventListener('input', redraw); });
  applyPreset(preset.value.split('|'));
  redraw();
  window.redrawLab = redraw;
"""


def radicals_lab(cfg):
    """Modes: simplify, rational, reduce, operate, rationalize, solve.

    THE TEACHING DECISION. Radicals are where a reader first meets an answer
    that cannot be finished. sqrt(72) does not become a number; it becomes
    6sqrt(2), and a reader who believes the point of a question is to produce a
    decimal has nothing to hold on to. So every mode here treats the exact form
    as the answer and the decimal as a comment: values are carried as sums of
    c*sqrt(k) with exact rational coefficients and squarefree kernels, and where
    a decimal appears it is rounded, labelled, and never used to decide
    anything.

    Two modes exist specifically because the obvious method breaks in them.
    Rational exponents: (-8)^(1/3) is -2, and the same exponent written 2/6
    gives +2 if the power is taken first, so the two routes are computed
    separately and printed side by side rather than reconciled. Solving:
    squaring both sides is not reversible, it turns -2 = 2 into 4 = 4, and the
    candidates it invents are indistinguishable from solutions until they are
    substituted back. That check is done exactly -- including for irrational
    candidates, where the sign of p + q*sqrt(k) is settled by comparing squares
    -- and the rejected values are drawn as hollow points on the graph, at the
    place where the line is and the curve is not.
    """
    mode = cfg.get("mode", "simplify")
    if mode not in SR_BODY:
        mode = "simplify"
    presets = cfg.get("presets") or SR_PRESETS[mode]
    title, subtitle = SR_TITLES[mode]
    first = presets[0][1]

    if mode == "solve":
        stage = ('      <div class="lab-stage"><svg id="srPlot"></svg></div>\n'
                 '      <div id="srStage" style="margin-top:12px;"></div>\n')
    else:
        stage = '      <div class="lab-stage" id="srStage"></div>\n'

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong>%s</strong><span id="srSub"></span></div>\n'
        '        <div class="inline-legend">%s</div>\n'
        "      </div>\n"
        "%s"
        '      <div id="srWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="srStatus" style="margin-top:12px;"></div>'
        % (title, SR_LEGEND[mode], stage)
    )

    index_field = ""
    if mode in ("simplify", "reduce"):
        index_field = (
            '        <div class="field">\n'
            '          <label for="srIdx">Index</label>\n'
            '          <select id="srIdx">%s</select>\n'
            "        </div>\n" % "".join(
                '<option value="%s">%s</option>' % (value, label)
                for value, label in SR_INDEX_OPTIONS
            )
        )

    controls = (
        '        <div class="field">\n'
        '          <label for="srPreset">Example</label>\n'
        '          <select id="srPreset">%s</select>\n'
        "        </div>\n"
        "%s%s%s"
        '        <p class="small-copy" style="margin:0;">%s</p>'
        % (
            _options(presets), _fields(SR_FIELDS[mode], first), index_field,
            _kpis(SR_KPIS[mode], "sr"), SR_HINTS[mode],
        )
    )

    parts = [RATIONAL_JS, SURD_JS, FORMAT_JS, RADICAL_JS]
    if mode in ("operate", "rationalize"):
        parts += [EXPR_JS, STEP_JS]
    if mode == "solve":
        parts += [POLY_JS, PLOT_JS]
    script = (
        "".join(parts)
        + "\n  var HINT = " + _jsstr(SR_HINTS[mode]) + ";\n"
        + SR_PRELUDE + SR_BODY[mode] + SR_WIRE
    )

    panel_title, panel_intro = SR_PANEL[mode]
    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", panel_title),
        panel_intro=cfg.get("panel_intro", panel_intro),
        script=script,
    )
