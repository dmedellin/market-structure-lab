"""The arithmetic every algebra lab is built on.

Algebra is the first subject on this library where the reader's own answer is a
SYMBOL rather than a number -- "x = 3/7", "(x - 2)(x + 5)", "no real solution".
A lab that answered 0.42857142857142855 would be answering a different question
from the one the lesson asked, so four pieces are shared by every lab here:

  RATIONAL_JS  exact rationals over BigInt. Every coefficient, every solution
               and every intermediate step is a fraction in lowest terms. A
               third is 1/3 and stays 1/3 through an arbitrary number of steps.
  POLY_JS      polynomials over those rationals: add, multiply, divide with
               remainder, evaluate, differentiate, gcd, and factor over Q via
               the rational root theorem. Factoring is SEARCHED, not looked up.
  EXPR_JS      a parser for what a reader actually types -- 2x, 3(x+1)^2,
               sqrt(x-1), (x^2-4)/(x-2) -- with implicit multiplication.
  PLOT_JS      an SVG grapher. Curves are sampled from the function; nothing is
               a stored path string. Where a lab draws a parabola through a
               vertex it computed, the drawing and the number come from the
               same evaluation, so they cannot disagree.

Floating point appears in exactly two places, both deliberate: PLOT_JS maps
world coordinates to pixels, and lessons whose subject IS approximation (a
logarithm, an irrational root) say so where they use it.
"""

# --------------------------------------------------------------- rationals

RATIONAL_JS = r"""
  /* Exact rational arithmetic over BigInt.

     Every number a lesson calls "the answer" lives in this type. BigInt rather
     than Number because a few steps of elimination on a 3x3 system produces
     numerators that leave the exact-integer range of a double, and a solution
     that is silently wrong in the last digits is worse than no solution. */
  function bgcd(a, b) {
    if (a < 0n) a = -a;
    if (b < 0n) b = -b;
    while (b) { var t = a % b; a = b; b = t; }
    return a;
  }
  function R(n, d) {
    if (d === undefined) d = 1n;
    n = BigInt(n); d = BigInt(d);
    if (d === 0n) throw new Error('division by zero');
    if (d < 0n) { n = -n; d = -d; }
    var g = bgcd(n, d) || 1n;
    return { n: n / g, d: d / g };
  }
  var R0 = R(0n), R1 = R(1n);
  function Radd(a, b) { return R(a.n * b.d + b.n * a.d, a.d * b.d); }
  function Rsub(a, b) { return R(a.n * b.d - b.n * a.d, a.d * b.d); }
  function Rmul(a, b) { return R(a.n * b.n, a.d * b.d); }
  function Rdiv(a, b) { return R(a.n * b.d, a.d * b.n); }
  function Rneg(a) { return R(-a.n, a.d); }
  function Rabs(a) { return a.n < 0n ? Rneg(a) : a; }
  function Rinv(a) { return R(a.d, a.n); }
  function Rzero(a) { return a.n === 0n; }
  function Rsign(a) { return a.n === 0n ? 0 : (a.n < 0n ? -1 : 1); }
  function Requ(a, b) { return a.n === b.n && a.d === b.d; }
  function Rcmp(a, b) { var l = a.n * b.d, r = b.n * a.d; return l < r ? -1 : (l > r ? 1 : 0); }
  function Rint(a) { return a.d === 1n; }
  function Rpow(a, k) {
    var out = R1, base = a, e = k < 0 ? -k : k;
    while (e > 0) { if (e & 1) out = Rmul(out, base); base = Rmul(base, base); e >>= 1; }
    return k < 0 ? Rinv(out) : out;
  }
  /* The reader's form: "3", "-7/4". Never "3/1", never "0/5". */
  function Rtext(a) { return a.d === 1n ? String(a.n) : a.n + '/' + a.d; }
  /* Parenthesised when it would otherwise glue onto a neighbouring symbol. */
  function Rterm(a) { return (a.n < 0n || a.d !== 1n) ? '(' + Rtext(a) + ')' : Rtext(a); }
  function Rnum(a) { return Number(a.n) / Number(a.d); }
  /* A decimal, for the one place a lesson asks for one. Exact when it can be. */
  function Rdec(a, places) {
    if (places === undefined) places = 6;
    var v = Rnum(a);
    if (Rint(a)) return String(a.n);
    var s = v.toFixed(places);
    return s.indexOf('.') >= 0 ? s.replace(/0+$/, '').replace(/\.$/, '') : s;
  }
  function Rparse(text) {
    var s = String(text).trim();
    var m = /^([+-]?\d+)\s*\/\s*(\d+)$/.exec(s);
    if (m) return R(BigInt(m[1]), BigInt(m[2]));
    m = /^([+-]?\d+)$/.exec(s);
    if (m) return R(BigInt(m[1]));
    m = /^([+-]?)(\d*)\.(\d+)$/.exec(s);
    if (m) {
      var whole = m[2] || '0', frac = m[3];
      var num = BigInt(whole + frac), den = 10n ** BigInt(frac.length);
      return R(m[1] === '-' ? -num : num, den);
    }
    return null;
  }
  /* Is this rational a perfect square? Needed wherever a lesson must decide
     between an exact answer and a radical one -- sqrt(4/9) is 2/3 and belongs
     on the page as 2/3, while sqrt(2) must stay sqrt(2). */
  function bisqrt(n) {
    if (n < 0n) return null;
    if (n < 2n) return n;
    var x = n, y = (x + 1n) / 2n;
    while (y < x) { x = y; y = (x + n / x) / 2n; }
    return x * x === n ? x : null;
  }
  function Rsqrt(a) {
    if (a.n < 0n) return null;
    var p = bisqrt(a.n), q = bisqrt(a.d);
    return (p === null || q === null) ? null : R(p, q);
  }
"""


# ------------------------------------------------------------- polynomials

POLY_JS = r"""
  /* A polynomial is a dense array of rationals, index = power of x, with the
     zero polynomial as []. Nothing here is a special case for "nice" numbers:
     the same routines divide 2x^3 - 3x + 1 by x - 1/2 as divide it by x - 1. */
  function Pnorm(p) {
    var out = p.slice();
    while (out.length && Rzero(out[out.length - 1])) out.pop();
    return out;
  }
  function Pdeg(p) { return Pnorm(p).length - 1; }
  function Pzero(p) { return Pnorm(p).length === 0; }
  function Plead(p) { var q = Pnorm(p); return q.length ? q[q.length - 1] : R0; }
  function Padd(a, b) {
    var out = [], n = Math.max(a.length, b.length);
    for (var i = 0; i < n; i += 1) out.push(Radd(a[i] || R0, b[i] || R0));
    return Pnorm(out);
  }
  function Psub(a, b) {
    var out = [], n = Math.max(a.length, b.length);
    for (var i = 0; i < n; i += 1) out.push(Rsub(a[i] || R0, b[i] || R0));
    return Pnorm(out);
  }
  function Pmul(a, b) {
    if (!a.length || !b.length) return [];
    var out = [];
    for (var i = 0; i < a.length + b.length - 1; i += 1) out.push(R0);
    for (var j = 0; j < a.length; j += 1) {
      for (var k = 0; k < b.length; k += 1) out[j + k] = Radd(out[j + k], Rmul(a[j], b[k]));
    }
    return Pnorm(out);
  }
  function Pscale(p, r) { return Pnorm(p.map(function (c) { return Rmul(c, r); })); }
  function Ppow(p, k) { var out = [R1]; for (var i = 0; i < k; i += 1) out = Pmul(out, p); return out; }
  function Peval(p, x) {
    var acc = R0;
    for (var i = p.length - 1; i >= 0; i -= 1) acc = Radd(Rmul(acc, x), p[i]);
    return acc;
  }
  function Pderiv(p) {
    var out = [];
    for (var i = 1; i < p.length; i += 1) out.push(Rmul(p[i], R(BigInt(i))));
    return Pnorm(out);
  }
  /* Long division, which is lesson material in its own right -- the step list a
     lab shows IS this loop, printed. */
  function Pdivmod(a, b) {
    a = Pnorm(a); b = Pnorm(b);
    if (!b.length) throw new Error('division by the zero polynomial');
    var q = [], r = a.slice(), steps = [];
    var db = b.length - 1, lb = b[db];
    while (Pnorm(r).length - 1 >= db && Pnorm(r).length) {
      r = Pnorm(r);
      var dr = r.length - 1, coef = Rdiv(r[dr], lb), shift = dr - db;
      var term = [];
      for (var i = 0; i < shift; i += 1) term.push(R0);
      term.push(coef);
      var product = Pmul(term, b);
      steps.push({ term: Ptext(term), product: Ptext(product), before: Ptext(r) });
      r = Psub(r, product);
      q = Padd(q, term);
    }
    return { q: Pnorm(q), r: Pnorm(r), steps: steps };
  }
  function Pmonic(p) { var l = Plead(p); return Rzero(l) ? p : Pscale(p, Rinv(l)); }
  function Pgcd(a, b) {
    a = Pnorm(a); b = Pnorm(b);
    while (b.length) { var r = Pdivmod(a, b).r; a = b; b = r; }
    return a.length ? Pmonic(a) : a;
  }

  /* Reader-facing form. The rules here are the ones a marker applies: an
     implicit coefficient of 1 is not written, a negative term joins with a
     minus rather than a plus, and a fractional coefficient is bracketed so
     3/4x^2 can never be misread as 3/(4x^2). */
  function Ptext(p, v) {
    v = v || 'x';
    p = Pnorm(p);
    if (!p.length) return '0';
    var out = '';
    for (var i = p.length - 1; i >= 0; i -= 1) {
      var c = p[i];
      if (Rzero(c)) continue;
      var neg = Rsign(c) < 0, mag = Rabs(c);
      out += out === '' ? (neg ? '-' : '') : (neg ? ' - ' : ' + ');
      var one = Requ(mag, R1);
      var coef = one && i > 0 ? '' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')');
      var power = i === 0 ? '' : (i === 1 ? v : v + '^' + i);
      out += coef + power;
    }
    return out;
  }
  /* Bracketed when it is a sum, so (x + 1)(x - 2) prints correctly. */
  function Pfactortext(p, v) {
    var t = Ptext(p, v);
    return (t.indexOf(' + ') >= 0 || t.indexOf(' - ') >= 0) ? '(' + t + ')' : t;
  }

  /* ---- factoring over the rationals ----
     The rational root theorem, applied rather than quoted: clear denominators,
     list the divisors of the constant and leading terms, and TEST each
     candidate. A reader who runs this on x^2 + 1 sees the search come back
     empty, which is the point of the lesson that pairs with it. */
  function bdivisors(n) {
    if (n < 0n) n = -n;
    if (n === 0n) return [];
    var out = [], i = 1n;
    while (i * i <= n) {
      if (n % i === 0n) { out.push(i); if (i * i !== n) out.push(n / i); }
      i += 1n;
      if (out.length > 512) break;   /* lesson-sized numbers only; see Pfactor */
    }
    out.sort(function (a, b) { return a < b ? -1 : (a > b ? 1 : 0); });
    return out;
  }
  /* The same polynomial with integer, coprime coefficients and a positive
     leading term, plus the rational that was taken out. */
  function Pprimitive(p) {
    p = Pnorm(p);
    if (!p.length) return { poly: [], content: R1 };
    var den = 1n;
    p.forEach(function (c) { den = den * c.d / bgcd(den, c.d); });
    var ints = p.map(function (c) { return c.n * (den / c.d); });
    var g = 0n;
    ints.forEach(function (v) { g = bgcd(g, v); });
    if (g === 0n) g = 1n;
    if (ints[ints.length - 1] < 0n) g = -g;
    return {
      poly: ints.map(function (v) { return R(v / g); }),
      content: R(g, den)
    };
  }
  function Prationalroots(p) {
    var prim = Pprimitive(p).poly;
    if (prim.length < 2) return [];
    var roots = [], seen = {};
    var a0 = prim[0].n, an = prim[prim.length - 1].n;
    if (a0 === 0n) { roots.push(R0); seen['0/1'] = 1; }
    var ps = bdivisors(a0 === 0n ? an : a0), qs = bdivisors(an);
    for (var i = 0; i < ps.length; i += 1) {
      for (var j = 0; j < qs.length; j += 1) {
        for (var s = 0; s < 2; s += 1) {
          var cand = R(s ? -ps[i] : ps[i], qs[j]);
          var key = Rtext(cand);
          if (seen[key]) continue;
          seen[key] = 1;
          if (Rzero(Peval(prim, cand))) roots.push(cand);
        }
      }
    }
    roots.sort(Rcmp);
    return roots;
  }
  /* Full factorisation over Q: a rational content, integer linear factors with
     their multiplicities, and whatever is left that has no rational root.
     `complete` is false when the leftover is not linear or quadratic -- the lab
     says so rather than implying the factorisation finished. */
  function Pfactor(p) {
    p = Pnorm(p);
    if (!p.length) return { content: R0, factors: [], rest: [], complete: true };
    var prim = Pprimitive(p);
    var content = prim.content, work = prim.poly, factors = [];
    var guard = 0;
    while (Pdeg(work) > 0 && guard < 64) {
      guard += 1;
      var roots = Prationalroots(work);
      if (!roots.length) break;
      var r = roots[0];
      /* root p/q  ->  integer factor (qx - p), which keeps every coefficient
         whole and is the form the reader is asked to produce. */
      var factor = [Rneg(R(r.n)), R(r.d)];
      var mult = 0;
      while (Pdeg(work) > 0) {
        var dm = Pdivmod(work, factor);
        if (!Pzero(dm.r)) break;
        work = dm.q; mult += 1;
      }
      factors.push({ poly: factor, mult: mult, root: r });
    }
    /* Whatever scalar the integer divisions left behind belongs to the content. */
    if (Pdeg(work) === 0) { content = Rmul(content, work[0]); work = [R1]; }
    var rest = Pdeg(work) > 0 ? work : [];
    return { content: content, factors: factors, rest: rest, complete: Pdeg(work) <= 2 };
  }
  function Pfactortextfull(p, v) {
    var f = Pfactor(p);
    if (!f.factors.length && !f.rest.length) return Rtext(f.content);
    var pieces = [];
    f.factors.forEach(function (item) { pieces.push({ poly: item.poly, mult: item.mult }); });
    if (f.rest.length) pieces.push({ poly: f.rest, mult: 1 });
    /* A polynomial that does not factor is written as itself. Bracketing a
       lone factor -- "(x^2 + 1)" -- suggests something was multiplied by
       something, which is the opposite of what that result says. */
    if (pieces.length === 1 && pieces[0].mult === 1 && Requ(f.content, R1)) {
      return Ptext(pieces[0].poly, v);
    }
    var out = '';
    if (!Requ(f.content, R1)) out += Requ(f.content, R(-1n)) ? '-' : Rterm(f.content);
    pieces.forEach(function (item) {
      out += Pfactortext(item.poly, v) + (item.mult > 1 ? '^' + item.mult : '');
    });
    return out || '1';
  }
"""


# ------------------------------------------------------- expression parsing

EXPR_JS = r"""
  /* A parser for what a reader actually types.

     It accepts implicit multiplication -- 2x, 3(x+1), (x+1)(x-2), 4x^2 --
     because that is how algebra is written on paper, and a lab that rejected
     "2x" would be teaching its own notation rather than the subject's. A
     single letter is a variable; a name of two or more letters is a function,
     which is what lets xy mean x times y while sqrt(x) stays one call. */
  function Etokenize(src) {
    var out = [], i = 0, s = String(src);
    while (i < s.length) {
      var c = s[i];
      if (c === ' ' || c === '\t') { i += 1; continue; }
      if (/[0-9.]/.test(c)) {
        var j = i;
        while (j < s.length && /[0-9.]/.test(s[j])) j += 1;
        out.push({ t: 'num', v: s.slice(i, j) }); i = j; continue;
      }
      if (/[A-Za-z]/.test(c)) {
        var k = i;
        while (k < s.length && /[A-Za-z]/.test(s[k])) k += 1;
        var word = s.slice(i, k);
        if (word.length > 1 && FUNCS[word.toLowerCase()]) {
          out.push({ t: 'fn', v: word.toLowerCase() }); i = k; continue;
        }
        /* Not a known function: every letter is its own variable, so "xy" is a
           product and a typo like "sqrtt(x)" fails loudly instead of silently
           becoming a product of six variables named s, q, r, t, t. */
        if (word.length > 1 && /^[a-z]+$/.test(word) && word.length > 3) {
          throw new Error('unknown function "' + word + '"');
        }
        for (var m = i; m < k; m += 1) out.push({ t: 'var', v: s[m] });
        i = k; continue;
      }
      if ('+-*/^(),'.indexOf(c) >= 0) { out.push({ t: c }); i += 1; continue; }
      throw new Error('unexpected character "' + c + '"');
    }
    return out;
  }

  var FUNCS = {
    sqrt: function (v) { return Math.sqrt(v); },
    cbrt: function (v) { return Math.cbrt(v); },
    abs: function (v) { return Math.abs(v); },
    ln: function (v) { return Math.log(v); },
    log: function (v) { return Math.log(v) / Math.LN10; },
    log2: function (v) { return Math.log(v) / Math.LN2; },
    exp: function (v) { return Math.exp(v); }
  };

  function Eparse(src) {
    var toks = Etokenize(src), pos = 0;
    function peek() { return toks[pos]; }
    function eat(t) { if (toks[pos] && toks[pos].t === t) { pos += 1; return true; } return false; }
    function expect(t) { if (!eat(t)) throw new Error('expected "' + t + '"'); }

    function primary() {
      var tk = peek();
      if (!tk) throw new Error('the expression ends early');
      if (tk.t === 'num') { pos += 1; return { k: 'num', v: tk.v }; }
      if (tk.t === 'var') { pos += 1; return { k: 'var', v: tk.v }; }
      if (tk.t === 'fn') { pos += 1; expect('('); var a = sum(); expect(')'); return { k: 'fn', v: tk.v, a: a }; }
      if (tk.t === '(') { pos += 1; var e = sum(); expect(')'); return e; }
      if (tk.t === '-') { pos += 1; return { k: 'neg', a: unary() }; }
      if (tk.t === '+') { pos += 1; return unary(); }
      throw new Error('unexpected "' + (tk.v || tk.t) + '"');
    }
    /* ^ binds tighter than unary minus on the left and is right-associative,
       so -x^2 is -(x^2) and 2^3^2 is 2^9. Both are the conventions a reader
       is marked against. */
    function power() {
      var base = primary();
      if (eat('^')) return { k: 'pow', a: base, b: unary() };
      return base;
    }
    function unary() {
      if (eat('-')) return { k: 'neg', a: unary() };
      if (eat('+')) return unary();
      return power();
    }
    function implicit(node) {
      /* juxtaposition is multiplication: 2x, 3(x+1), (x+1)(x-2), 2sqrt(x) */
      while (peek() && (peek().t === 'num' || peek().t === 'var' || peek().t === 'fn' || peek().t === '(')) {
        node = { k: 'mul', a: node, b: power() };
      }
      return node;
    }
    function product() {
      var node = implicit(unary());
      while (peek() && (peek().t === '*' || peek().t === '/')) {
        var op = peek().t; pos += 1;
        node = { k: op === '*' ? 'mul' : 'div', a: node, b: implicit(unary()) };
      }
      return node;
    }
    function sum() {
      var node = product();
      while (peek() && (peek().t === '+' || peek().t === '-')) {
        var op = peek().t; pos += 1;
        node = { k: op === '+' ? 'add' : 'sub', a: node, b: product() };
      }
      return node;
    }
    var tree = sum();
    if (pos < toks.length) throw new Error('unexpected "' + (toks[pos].v || toks[pos].t) + '"');
    return tree;
  }

  /* Numeric evaluation, for drawing. Returns NaN outside the domain rather
     than throwing, because a grapher must be able to ask for f(-1) on sqrt(x)
     and simply not plot a point there. */
  function Eeval(node, env) {
    switch (node.k) {
      case 'num': return parseFloat(node.v);
      case 'var': return (env && node.v in env) ? env[node.v] : NaN;
      case 'neg': return -Eeval(node.a, env);
      case 'add': return Eeval(node.a, env) + Eeval(node.b, env);
      case 'sub': return Eeval(node.a, env) - Eeval(node.b, env);
      case 'mul': return Eeval(node.a, env) * Eeval(node.b, env);
      case 'div': return Eeval(node.a, env) / Eeval(node.b, env);
      case 'pow': return Math.pow(Eeval(node.a, env), Eeval(node.b, env));
      case 'fn': return FUNCS[node.v](Eeval(node.a, env));
    }
    return NaN;
  }

  /* The same tree as a polynomial over Q in one variable, or null when it is
     not one. This is what lets a reader type a polynomial and have the EXACT
     machinery -- factoring, division, the rational root search -- run on it,
     rather than a floating-point approximation of it. */
  function Epoly(node, v) {
    v = v || 'x';
    switch (node.k) {
      case 'num': { var r = Rparse(node.v); return r === null ? null : (Rzero(r) ? [] : [r]); }
      case 'var': return node.v === v ? [R0, R1] : null;
      case 'neg': { var a = Epoly(node.a, v); return a === null ? null : Pscale(a, R(-1n)); }
      case 'add': case 'sub': case 'mul': {
        var l = Epoly(node.a, v), r2 = Epoly(node.b, v);
        if (l === null || r2 === null) return null;
        return node.k === 'add' ? Padd(l, r2) : (node.k === 'sub' ? Psub(l, r2) : Pmul(l, r2));
      }
      case 'div': {
        var num = Epoly(node.a, v), den = Epoly(node.b, v);
        if (num === null || den === null || Pdeg(den) !== 0) return null;
        return Pscale(num, Rinv(den[0]));   /* division by a constant only */
      }
      case 'pow': {
        var base = Epoly(node.a, v), ex = Epoly(node.b, v);
        if (base === null || ex === null || Pdeg(ex) > 0) return null;
        var e = ex.length ? ex[0] : R0;
        if (!Rint(e) || e.n < 0n || e.n > 64n) return null;
        return Ppow(base, Number(e.n));
      }
    }
    return null;
  }
  function Epolyof(src, v) {
    try { return Epoly(Eparse(src), v || 'x'); } catch (e) { return null; }
  }
"""


# ---------------------------------------------------------------- graphing

PLOT_JS = r"""
  /* The grapher.

     Every curve on this path is SAMPLED from the function the lesson is about.
     There is not one stored path string anywhere in these labs, which is what
     makes a drawing evidence rather than decoration: when a lab prints a vertex
     at (3, -4) and draws the parabola through it, the label and the picture
     came out of the same evaluation and cannot disagree.

     Coordinates are the one deliberate use of floating point here -- a pixel is
     a pixel. Everything the reader is told in words comes from the exact side. */
  var PLOT_W = 660, PLOT_H = 420, PAD_L = 44, PAD_R = 16, PAD_T = 16, PAD_B = 34;

  function svgel(name, attrs) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) el.setAttribute(k, attrs[k]);
    return el;
  }
  /* A grid step a reader can count on: 1, 2 or 5 times a power of ten, chosen
     so the axis carries roughly eight divisions whatever the window is. */
  function nicestep(span) {
    var raw = span / 8, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
    var n = raw / mag;
    return (n < 1.5 ? 1 : (n < 3.5 ? 2 : (n < 7.5 ? 5 : 10))) * mag;
  }
  function ticktext(v, step) {
    if (Math.abs(v) < step / 1000) return '0';
    var places = Math.max(0, -Math.floor(Math.log(step) / Math.LN10));
    return v.toFixed(Math.min(places, 4)).replace(/\.?0+$/, function (m) {
      return m.indexOf('.') === 0 ? '' : m;
    });
  }

  function Plot(svg, win) {
    var xmin = win.xmin, xmax = win.xmax, ymin = win.ymin, ymax = win.ymax;
    var iw = PLOT_W - PAD_L - PAD_R, ih = PLOT_H - PAD_T - PAD_B;
    svg.setAttribute('viewBox', '0 0 ' + PLOT_W + ' ' + PLOT_H);
    svg.setAttribute('role', 'img');
    svg.textContent = '';

    function sx(x) { return PAD_L + (x - xmin) / (xmax - xmin) * iw; }
    function sy(y) { return PAD_T + (ymax - y) / (ymax - ymin) * ih; }

    var defs = svgel('defs', {});
    var clip = svgel('clipPath', { id: 'plotclip' });
    clip.appendChild(svgel('rect', { x: PAD_L, y: PAD_T, width: iw, height: ih }));
    defs.appendChild(clip);
    svg.appendChild(defs);

    var plotted = svgel('g', { 'clip-path': 'url(#plotclip)' });

    var api = {
      sx: sx, sy: sy, win: win,
      /* Grid, axes, ticks. Drawn first so every curve sits on top of them. */
      frame: function () {
        var gx = nicestep(xmax - xmin), gy = nicestep(ymax - ymin);
        var g = svgel('g', {});
        var start = Math.ceil(xmin / gx) * gx, v;
        for (v = start; v <= xmax + gx / 2; v += gx) {
          if (Math.abs(v) < gx / 1000) continue;
          g.appendChild(svgel('line', { class: 'plot-grid', x1: sx(v), y1: PAD_T, x2: sx(v), y2: PAD_T + ih }));
        }
        start = Math.ceil(ymin / gy) * gy;
        for (v = start; v <= ymax + gy / 2; v += gy) {
          if (Math.abs(v) < gy / 1000) continue;
          g.appendChild(svgel('line', { class: 'plot-grid', x1: PAD_L, y1: sy(v), x2: PAD_L + iw, y2: sy(v) }));
        }
        /* The axes sit at zero when zero is in view and at the near edge when
           it is not, so a window like 10 <= x <= 20 still has a labelled frame
           rather than two axes drawn off-screen. */
        var ay = ymin <= 0 && ymax >= 0 ? sy(0) : (ymin > 0 ? PAD_T + ih : PAD_T);
        var ax = xmin <= 0 && xmax >= 0 ? sx(0) : (xmin > 0 ? PAD_L : PAD_L + iw);
        g.appendChild(svgel('line', { class: 'plot-axis', x1: PAD_L, y1: ay, x2: PAD_L + iw, y2: ay }));
        g.appendChild(svgel('line', { class: 'plot-axis', x1: ax, y1: PAD_T, x2: ax, y2: PAD_T + ih }));
        for (v = Math.ceil(xmin / gx) * gx; v <= xmax + gx / 2; v += gx) {
          var tx = svgel('text', { class: 'plot-tick', x: sx(v), y: PAD_T + ih + 15, 'text-anchor': 'middle' });
          tx.textContent = ticktext(v, gx);
          g.appendChild(tx);
        }
        for (v = Math.ceil(ymin / gy) * gy; v <= ymax + gy / 2; v += gy) {
          if (Math.abs(v) < gy / 1000) continue;
          var ty = svgel('text', { class: 'plot-tick', x: PAD_L - 7, y: sy(v) + 3.5, 'text-anchor': 'end' });
          ty.textContent = ticktext(v, gy);
          g.appendChild(ty);
        }
        svg.appendChild(g);
        svg.appendChild(plotted);
        return api;
      },
      /* Sample the function across the drawing width and join the samples.
         A segment is BROKEN where the value stops being a real number and
         where it jumps by more than three window heights between neighbouring
         pixels -- that jump is a pole, and joining across it would draw a
         vertical line that is not part of the graph. Readers meet exactly that
         line in every graphing tool, and it is the reason they think 1/x is
         connected. */
      curve: function (fn, cls) {
        var runs = [], run = [], prev = null, steps = 480;
        for (var i = 0; i <= steps; i += 1) {
          var x = xmin + (xmax - xmin) * i / steps, y = fn(x);
          if (typeof y !== 'number' || !isFinite(y)) { if (run.length > 1) runs.push(run); run = []; prev = null; continue; }
          if (prev !== null && Math.abs(y - prev) > 3 * (ymax - ymin)) {
            if (run.length > 1) runs.push(run);
            run = [];
          }
          run.push(sx(x) + ',' + sy(Math.max(ymin - (ymax - ymin), Math.min(ymax + (ymax - ymin), y))));
          prev = y;
        }
        if (run.length > 1) runs.push(run);
        runs.forEach(function (pts) {
          plotted.appendChild(svgel('polyline', { class: cls || 'plot-curve', points: pts.join(' ') }));
        });
        return api;
      },
      point: function (x, y, cls, label) {
        if (!isFinite(x) || !isFinite(y)) return api;
        plotted.appendChild(svgel('circle', { class: cls || 'plot-point', cx: sx(x), cy: sy(y), r: 5 }));
        if (label) {
          var t = svgel('text', { class: 'plot-label', x: sx(x) + 9, y: sy(y) - 8 });
          t.textContent = label;
          plotted.appendChild(t);
        }
        return api;
      },
      hole: function (x, y) {
        if (!isFinite(x) || !isFinite(y)) return api;
        plotted.appendChild(svgel('circle', { class: 'plot-hole', cx: sx(x), cy: sy(y), r: 5 }));
        return api;
      },
      vline: function (x, cls, label) {
        plotted.appendChild(svgel('line', { class: cls || 'plot-asym', x1: sx(x), y1: PAD_T, x2: sx(x), y2: PAD_T + ih }));
        if (label) {
          var t = svgel('text', { class: 'plot-label', x: sx(x) + 6, y: PAD_T + 14 });
          t.textContent = label;
          plotted.appendChild(t);
        }
        return api;
      },
      hline: function (y, cls, label) {
        plotted.appendChild(svgel('line', { class: cls || 'plot-asym', x1: PAD_L, y1: sy(y), x2: PAD_L + iw, y2: sy(y) }));
        if (label) {
          var t = svgel('text', { class: 'plot-label', x: PAD_L + 6, y: sy(y) - 6 });
          t.textContent = label;
          plotted.appendChild(t);
        }
        return api;
      },
      segment: function (x1, y1, x2, y2, cls) {
        plotted.appendChild(svgel('line', { class: cls || 'plot-aux', x1: sx(x1), y1: sy(y1), x2: sx(x2), y2: sy(y2) }));
        return api;
      },
      /* The solution set of an inequality, shaded by testing the predicate on
         a grid of sample points rather than by reasoning about the boundary. */
      shade: function (test, cls) {
        var cols = 90, rows = 58;
        for (var i = 0; i < cols; i += 1) {
          for (var j = 0; j < rows; j += 1) {
            var x = xmin + (xmax - xmin) * (i + 0.5) / cols;
            var y = ymin + (ymax - ymin) * (j + 0.5) / rows;
            if (!test(x, y)) continue;
            plotted.appendChild(svgel('rect', {
              class: cls || 'plot-shade', x: sx(x) - iw / cols / 2, y: sy(y) - ih / rows / 2,
              width: iw / cols + 0.6, height: ih / rows + 0.6
            }));
          }
        }
        return api;
      },
      label: function (x, y, text, cls) {
        var t = svgel('text', { class: cls || 'plot-label', x: sx(x), y: sy(y) });
        t.textContent = text;
        plotted.appendChild(t);
        return api;
      },
      describe: function (text) { svg.setAttribute('aria-label', text); return api; }
    };
    return api;
  }

  /* A one-dimensional cousin: the number line every inequality lesson needs. */
  function NumberLine(svg, lo, hi) {
    var W = 660, H = 88, pad = 30, iw = W - 2 * pad;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    svg.textContent = '';
    function sx(x) { return pad + (x - lo) / (hi - lo) * iw; }
    svg.appendChild(svgel('line', { class: 'plot-axis', x1: pad, y1: 44, x2: W - pad, y2: 44 }));
    var step = nicestep(hi - lo);
    for (var v = Math.ceil(lo / step) * step; v <= hi + step / 2; v += step) {
      svg.appendChild(svgel('line', { class: 'plot-tickmark', x1: sx(v), y1: 38, x2: sx(v), y2: 50 }));
      var t = svgel('text', { class: 'plot-tick', x: sx(v), y: 68, 'text-anchor': 'middle' });
      t.textContent = ticktext(v, step);
      svg.appendChild(t);
    }
    return {
      sx: sx,
      /* Closed ends are filled, open ends are hollow -- the distinction the
         lesson is usually about. */
      interval: function (a, b, closedA, closedB) {
        var x1 = sx(Math.max(a, lo)), x2 = sx(Math.min(b, hi));
        svg.appendChild(svgel('line', { class: 'plot-interval', x1: x1, y1: 44, x2: x2, y2: 44 }));
        if (a >= lo) svg.appendChild(svgel('circle', { class: closedA ? 'plot-end closed' : 'plot-end open', cx: x1, cy: 44, r: 6 }));
        if (b <= hi) svg.appendChild(svgel('circle', { class: closedB ? 'plot-end closed' : 'plot-end open', cx: x2, cy: 44, r: 6 }));
        return this;
      },
      point: function (x, closed) {
        svg.appendChild(svgel('circle', { class: closed ? 'plot-end closed' : 'plot-end open', cx: sx(x), cy: 44, r: 6 }));
        return this;
      },
      describe: function (text) { svg.setAttribute('aria-label', text); return this; }
    };
  }
"""


# ------------------------------------------------------------------ surds

SURD_JS = r"""
  /* Exact irrational answers.

     sqrt(D) for a rational D is either rational or irrational, and the second
     case is not a failure -- it is the answer. A lesson that solves
     x^2 - 2x - 4 = 0 wants "1 +- sqrt(5)", not "3.2360679...", so the roots of
     every quadratic on this path are carried as  p + q*sqrt(k)  with p and q
     exact rationals and k a squarefree integer. */
  function bsqrtsimp(n) {
    /* n = s^2 * k with k squarefree; returns [s, k]. */
    var s = 1n, k = n, f = 2n;
    while (f * f <= k) {
      while (k % (f * f) === 0n) { k /= f * f; s *= f; }
      f += 1n;
      if (f > 100000n) break;   /* lesson-sized radicands */
    }
    return [s, k];
  }
  /* sqrt(a) for a rational a >= 0, as { q, k } meaning q * sqrt(k). k === 1n
     exactly when the root is rational. */
  function Rsurd(a) {
    if (a.n < 0n) return null;
    if (a.n === 0n) return { q: R0, k: 1n };
    /* sqrt(p/d) = sqrt(p*d)/d */
    var pair = bsqrtsimp(a.n * a.d);
    return { q: R(pair[0], a.d), k: pair[1] };
  }
  function surdtext(s) {
    if (s.k === 1n) return Rtext(s.q);
    if (Requ(s.q, R1)) return 'sqrt(' + s.k + ')';
    return Rterm(s.q) + 'sqrt(' + s.k + ')';
  }
  /* "p +- q sqrt(k)", the form a reader is expected to write down. */
  function pmtext(p, s, imaginary) {
    var unit = imaginary ? 'i' : '';
    if (s.k === 1n && Rzero(s.q)) return Rtext(p);
    var mag = surdtext(s);
    if (s.k !== 1n && Requ(Rabs(s.q), R1)) mag = 'sqrt(' + s.k + ')';
    else if (s.k !== 1n) mag = Rterm(Rabs(s.q)) + 'sqrt(' + s.k + ')';
    else mag = Rtext(Rabs(s.q));
    var right = unit ? (mag === '1' ? 'i' : mag + 'i') : mag;
    if (Rzero(p)) return '+-' + right;
    return Rtext(p) + ' +- ' + right;
  }
  /* The exact roots of ax^2 + bx + c, whatever the discriminant does.
     Returns { disc, kind, p, s, roots } where each root is p +- s (times i when
     the discriminant is negative), and `roots` holds the rational ones only. */
  function quadroots(a, b, c) {
    var disc = Rsub(Rmul(b, b), Rmul(R(4n), Rmul(a, c)));
    var p = Rdiv(Rneg(b), Rmul(R(2n), a));
    var sign = Rsign(disc);
    var mag = Rsurd(sign < 0 ? Rneg(disc) : disc);
    var s = { q: Rdiv(mag.q, Rabs(Rmul(R(2n), a))), k: mag.k };
    var kind = sign < 0 ? 'complex' : (sign === 0 ? 'double' : (s.k === 1n ? 'rational' : 'irrational'));
    var roots = [];
    if (kind === 'double') roots = [p];
    else if (kind === 'rational') roots = [Radd(p, s.q), Rsub(p, s.q)].sort(Rcmp);
    return { disc: disc, kind: kind, p: p, s: s, roots: roots };
  }
"""
