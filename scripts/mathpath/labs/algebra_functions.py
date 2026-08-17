"""Course 3: lines, the plane, and everything a function has.

Four labs live here because they share one idea and one toolkit. The idea is
that a FUNCTION IS A RULE, and every claim this course makes about a rule --
its slope, its zeros, its domain, its inverse -- is derived from the rule in
the reader's browser rather than stored beside it. The toolkit is the exact
arithmetic in algebra_core: rationals over BigInt, polynomials over those
rationals, a parser for what a reader types, and a grapher that samples the
function it was handed.

The consequence worth stating, because it is what makes these four labs
evidence rather than illustration: a picture and the numbers printed under it
come from the SAME evaluation. When funcops marks a hole at (2, 4) it is
because Erat found the factor (x - 2) in both numerator and denominator and
Peval gave 4 for the cancelled form -- not because a preset said so. Change the
formula to one that has no hole and the dot disappears, because nothing was
drawn that was not computed.

Shared machinery, used by more than one lab in this file:

  Erat          an expression as one polynomial over another, when it is one.
                This is what makes a removable discontinuity findable exactly.
  constraintsOf what a formula forbids: sqrt needs a non-negative argument, a
                quotient needs a non-zero denominator, a log needs a positive
                one -- each collected as a constraint on a polynomial so its
                boundary is a root and not a place where the drawing stopped.
  domainOf      those constraints turned into a union of intervals, by testing
                exactly between and at every boundary. Two rays, one interval,
                a single point removed and "all real numbers" all come out of
                the same loop; nothing is special-cased by the shape of the
                formula.
  trace         a curve that is not a function of x -- a sideways parabola, a
                graph reflected in y = x -- drawn from sampled points.

Where a value is genuinely irrational (sqrt(2) as a domain boundary, the
decimal beside an exact surd) the lab prints the exact form and says that the
decimal is a rounding of it.
"""

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

BASE_JS = RATIONAL_JS + POLY_JS + SURD_JS + EXPR_JS + PLOT_JS


SHARED_JS = r"""
  /* ------------------------------------------------------------------ */
  /* Shared by the labs in this file. Everything here is exact; the only  */
  /* floating point is a pixel or a genuinely irrational quantity, and    */
  /* every place that prints one of those says which it is.               */
  /* ------------------------------------------------------------------ */

  function row(label, detail) {
    return '<tr><th class="rowhead">' + label + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function table(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption
      + '</caption><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  function chip(text, kind) {
    return '<span class="chip' + (kind ? ' ' + kind : '') + '">' + text + '</span>';
  }
  function muted(text) { return '<span class="tone-muted">' + text + '</span>'; }

  /* Rparse throws on a zero denominator, which is precisely what a reader types
     when they are exploring what "undefined" means. Every lab in this file
     reads through here so that 1/0 produces an explanation rather than a
     stack trace. */
  function readR(text) {
    try { return Rparse(text); } catch (err) { return null; }
  }

  /* The reader writes "y = 2x - 1" or "f(x) = 2x - 1", because that is what a
     function looks like. Rejecting the left-hand side would be teaching our
     notation rather than the subject's. */
  function bodyof(src) {
    var s = String(src === undefined || src === null ? '' : src).trim();
    var m = /^(?:y|[fgh]\s*\(\s*[a-z]\s*\))\s*=\s*([\s\S]*)$/i.exec(s);
    return (m ? m[1] : s).trim();
  }

  /* Whole coefficients: multiply out the denominators, divide by the gcd, and
     make the first non-zero one positive. Standard form is only standard when
     it is written like that, and the lab DERIVES it rather than printing back
     what a preset handed it. */
  function clearden(coeffs) {
    var den = 1n, i;
    coeffs.forEach(function (c) { den = den * c.d / bgcd(den, c.d); });
    var ints = coeffs.map(function (c) { return c.n * (den / c.d); });
    var g = 0n;
    ints.forEach(function (v) { g = bgcd(g, v); });
    if (g === 0n) g = 1n;
    for (i = 0; i < ints.length; i += 1) {
      if (ints[i] !== 0n) { if (ints[i] < 0n) g = -g; break; }
    }
    return ints.map(function (v) { return R(v / g); });
  }

  /* a + b and a - b with the signs already tidied: "3 - 2" rather than
     "3 + -2", which is the form a reader is asked to produce. */
  function sumtext(a, b) {
    return Rsign(b) < 0 ? Rtext(a) + ' - ' + Rtext(Rabs(b)) : Rtext(a) + ' + ' + Rtext(b);
  }
  function subtext(a, b) {
    return Rtext(a) + ' - ' + (Rsign(b) < 0 ? '(' + Rtext(b) + ')' : Rtext(b));
  }
  /* "x - 3", "x + 3", "x": the shift as a reader writes it. Point-slope form
     is the place where a minus sign in front of a negative number turns into
     the plus that confuses everybody, so it is built once, here. */
  function shifttext(v, sym) {
    if (Rzero(v)) return sym;
    return sym + (Rsign(v) > 0 ? ' - ' : ' + ') + Rtext(Rabs(v));
  }
  /* A coefficient in front of a bracket: 1 and -1 are not written out. */
  function coeftext(m) {
    if (Requ(m, R1)) return '';
    if (Requ(m, R(-1n))) return '-';
    return Rterm(m);
  }

  /* Replace the variable x inside a formula the reader typed, leaving function
     names alone -- the x in "exp" is not a variable. This is how a substitution
     is SHOWN the way it is written on paper, and how a composite formula is
     built for the parser to read back. */
  function subx(src, repl) {
    var out = '', i = 0;
    while (i < src.length) {
      var c = src[i];
      if (/[A-Za-z]/.test(c)) {
        var j = i;
        while (j < src.length && /[A-Za-z]/.test(src[j])) j += 1;
        var word = src.slice(i, j);
        out += (word.length > 1 && FUNCS[word.toLowerCase()]) ? word : word.replace(/x/g, repl);
        i = j;
        continue;
      }
      out += c;
      i += 1;
    }
    return out;
  }

  /* A curve that is not a function of x -- a sideways parabola, a graph
     reflected in y = x -- from sampled points, broken wherever a sample stops
     being a real number, for the same reason Plot.curve breaks. */
  function trace(plot, pts, cls) {
    var prev = null;
    for (var i = 0; i < pts.length; i += 1) {
      var p = pts[i];
      var ok = p && isFinite(p[0]) && isFinite(p[1]);
      if (ok && prev) plot.segment(prev[0], prev[1], p[0], p[1], cls || 'plot-curve');
      prev = ok ? p : null;
    }
    return plot;
  }

  /* f(g(x)) for polynomials: Horner on the coefficients of f with the whole of
     g in place of x. Exact, and it is the same operation whether the lesson
     calls it a composition or a transformation. */
  function Pcompose(f, g) {
    var out = [];
    for (var i = f.length - 1; i >= 0; i -= 1) out = Padd(Pmul(out, g), [f[i]]);
    return Pnorm(out);
  }

  /* Numeric evaluation of an exact polynomial, for pixels only. */
  function Pnumeval(p, xv) {
    var acc = 0;
    for (var i = p.length - 1; i >= 0; i -= 1) acc = acc * xv + Rnum(p[i]);
    return acc;
  }

  /* ---- an expression as one polynomial over another ----
     This is what makes a HOLE findable exactly. (x^2 - 4)/(x - 2) is x + 2 at
     every x except 2, and the difference between "the graph is a line" and
     "the graph is a line with one point missing" is the whole of that lesson.
     Deliberately NOT reduced: the un-cancelled denominator is what the domain
     is computed from, and cancelling first is exactly the mistake the lesson
     is about. */
  function Erat(node, v) {
    v = v || 'x';
    if (!node) return null;
    var a, b, l, r;
    switch (node.k) {
      case 'num': {
        var q = Rparse(node.v);
        return q === null ? null : { n: Rzero(q) ? [] : [q], d: [R1] };
      }
      case 'var': return node.v === v ? { n: [R0, R1], d: [R1] } : null;
      case 'neg':
        a = Erat(node.a, v);
        return a === null ? null : { n: Pscale(a.n, R(-1n)), d: a.d };
      case 'add': case 'sub':
        a = Erat(node.a, v); b = Erat(node.b, v);
        if (a === null || b === null) return null;
        l = Pmul(a.n, b.d); r = Pmul(b.n, a.d);
        return { n: node.k === 'add' ? Padd(l, r) : Psub(l, r), d: Pmul(a.d, b.d) };
      case 'mul':
        a = Erat(node.a, v); b = Erat(node.b, v);
        if (a === null || b === null) return null;
        return { n: Pmul(a.n, b.n), d: Pmul(a.d, b.d) };
      case 'div':
        a = Erat(node.a, v); b = Erat(node.b, v);
        if (a === null || b === null || Pzero(b.n)) return null;
        return { n: Pmul(a.n, b.d), d: Pmul(a.d, b.n) };
      case 'pow': {
        var base = Erat(node.a, v), ex = Epoly(node.b, v);
        if (base === null || ex === null || Pdeg(ex) > 0) return null;
        var e = ex.length ? ex[0] : R0;
        if (!Rint(e) || e.n > 24n || e.n < -24n) return null;
        var k = Number(e.n);
        var unit = k < 0 ? { n: base.d, d: base.n } : base;
        if (k < 0 && Pzero(base.n)) return null;
        var out = { n: [R1], d: [R1] };
        for (var i = 0; i < Math.abs(k); i += 1) out = { n: Pmul(out.n, unit.n), d: Pmul(out.d, unit.d) };
        return out;
      }
    }
    return null;
  }
  /* The cancelled form, and the factor that was cancelled -- which is exactly
     the set of holes. */
  function ratreduce(f) {
    if (!f || Pzero(f.d)) return null;
    if (Pzero(f.n)) return { n: [], d: [R1], cancelled: [] };
    var g = Pgcd(f.n, f.d);
    if (Pdeg(g) < 1) return { n: f.n, d: f.d, cancelled: [] };
    return { n: Pdivmod(f.n, g).q, d: Pdivmod(f.d, g).q, cancelled: g };
  }
  /* A quotient written the way it should be handed in: no 1 as a
     denominator, no minus sign left on the bottom, no brackets around a term
     that does not need them. */
  function ratformula(n, d, v) {
    v = v || 'x';
    if (Rsign(Plead(d)) < 0) { n = Pscale(n, R(-1n)); d = Pscale(d, R(-1n)); }
    if (Pzero(n)) return '0';
    if (Pdeg(d) === 0) {
      if (Requ(d[0], R1)) return Ptext(n, v);
      return Pfactortext(n, v) + '/' + Rterm(d[0]);
    }
    return Pfactortext(n, v) + '/' + Pfactortext(d, v);
  }
  function rattext(f, v) {
    v = v || 'x';
    if (Pdeg(f.d) < 1 && Requ(Plead(f.d), R1)) return Ptext(f.n, v);
    return Pfactortext(f.n, v) + ' / ' + Pfactortext(f.d, v);
  }

  /* ---- what a formula forbids ----
     Three things restrict a domain, and each is collected as a constraint on a
     POLYNOMIAL so that its boundary is an exact root rather than the place
     where a drawing stopped:
        sqrt(u)      needs  u >= 0
        anything / u needs  u != 0
        ln(u)        needs  u > 0
     A constraint whose argument is not a polynomial is recorded with a null
     polynomial, and the lab then SAYS the domain was not fully derived rather
     than printing one it guessed. */
  function mkcon(rel, sub, v, why) {
    var p = Epoly(sub, v);
    if (p === null) {
      var rr = Erat(sub, v);
      if (rr) p = rr.n;          /* a quotient is zero where its numerator is */
    }
    return { rel: rel, poly: p, why: why, text: p ? Ptext(p, v) : null };
  }
  function constraintsOf(node, v, out) {
    out = out || [];
    if (!node || typeof node !== 'object') return out;
    if (node.k === 'fn' && node.v === 'sqrt') out.push(mkcon('ge', node.a, v, 'sqrt'));
    if (node.k === 'fn' && (node.v === 'ln' || node.v === 'log' || node.v === 'log2')) {
      out.push(mkcon('gt', node.a, v, 'log'));
    }
    if (node.k === 'div') {
      var d = node.b;
      if (d.k === 'fn' && d.v === 'sqrt') out.push(mkcon('ne', d.a, v, 'denominator-root'));
      else out.push(mkcon('ne', d, v, 'denominator'));
    }
    constraintsOf(node.a, v, out);
    constraintsOf(node.b, v, out);
    return out;
  }

  /* p +- q sqrt(k) as one boundary point: exact text, plus a float used only
     for ordering and for choosing a rational test point between boundaries. */
  function surdpoint(p, s, sign, owner) {
    var val = Rnum(p) + sign * Rnum(s.q) * Math.sqrt(Number(s.k));
    var mag = Requ(Rabs(s.q), R1) ? 'sqrt(' + s.k + ')' : Rterm(Rabs(s.q)) + 'sqrt(' + s.k + ')';
    var text = Rzero(p) ? (sign < 0 ? '-' + mag : mag)
                        : Rtext(p) + (sign < 0 ? ' - ' : ' + ') + mag;
    return { r: null, text: text, val: val, owner: owner, irrational: true };
  }

  /* Every place a constraint can change sign. Rational roots come out of the
     rational root search; a leftover quadratic contributes its two surds,
     which are exact; a leftover of higher degree is reported as NOT derived
     rather than quietly dropped. */
  function boundariesOf(cons) {
    var pts = [], exact = true;
    cons.forEach(function (c, idx) {
      if (!c.poly) { exact = false; return; }
      if (Pdeg(c.poly) < 1) return;
      var f = Pfactor(c.poly);
      f.factors.forEach(function (item) {
        pts.push({ r: item.root, text: Rtext(item.root), val: Rnum(item.root), owner: idx });
      });
      if (f.rest.length) {
        if (Pdeg(f.rest) === 2) {
          var q = quadroots(f.rest[2], f.rest[1], f.rest[0]);
          if (q.kind === 'irrational') {
            pts.push(surdpoint(q.p, q.s, -1, idx));
            pts.push(surdpoint(q.p, q.s, 1, idx));
          } else if (q.kind !== 'complex') { exact = false; }
        } else { exact = false; }
      }
    });
    pts.sort(function (a, b) { return a.val - b.val; });
    var out = [];
    pts.forEach(function (p) {
      if (out.length && Math.abs(out[out.length - 1].val - p.val) < 1e-12) return;
      out.push(p);
    });
    return { points: out, exact: exact };
  }

  /* Does this x satisfy every constraint? At a rational x the test is exact
     arithmetic. At an irrational boundary the constraint that PRODUCED it is
     zero there by construction, and any other constraint is evaluated
     numerically -- which is recorded, so the lab can say so. */
  function testAt(cons, pt) {
    var ok = true, sure = true;
    for (var i = 0; i < cons.length; i += 1) {
      var c = cons[i], sign;
      if (!c.poly) { sure = false; continue; }
      if (pt.r) {
        sign = Rsign(Peval(c.poly, pt.r));
      } else if (pt.owner === i) {
        sign = 0;
      } else {
        var val = Pnumeval(c.poly, pt.val);
        if (Math.abs(val) < 1e-9) { sign = 0; sure = false; }
        else { sign = val < 0 ? -1 : 1; }
      }
      if (c.rel === 'ge' && sign < 0) ok = false;
      if (c.rel === 'gt' && sign <= 0) ok = false;
      if (c.rel === 'ne' && sign === 0) ok = false;
    }
    return { ok: ok, sure: sure };
  }

  /* The domain as a union of intervals. Nothing about the shape of the formula
     is assumed: one interval, two rays, a single point removed and "every real
     number" all fall out of the same walk along the boundaries. */
  function domainOf(cons) {
    var b = boundariesOf(cons), pts = b.points, sure = b.exact, segs = [], i;

    function between(lo, hi) {
      if (lo === null && hi === null) return R0;
      if (lo === null) return R(BigInt(Math.floor(hi.val) - 1));
      if (hi === null) return R(BigInt(Math.ceil(lo.val) + 1));
      if (lo.r && hi.r) return Rdiv(Radd(lo.r, hi.r), R(2n));
      var t = (lo.val + hi.val) / 2, q = Rparse(t.toFixed(6));
      return q === null ? R(BigInt(Math.round(t))) : q;
    }

    for (i = 0; i <= pts.length; i += 1) {
      var lo = i === 0 ? null : pts[i - 1], hi = i === pts.length ? null : pts[i];
      var probe = { r: between(lo, hi), owner: null };
      probe.val = Rnum(probe.r);
      var t1 = testAt(cons, probe);
      if (!t1.sure) sure = false;
      segs.push({ kind: 'open', lo: lo, hi: hi, inside: t1.ok });
      if (hi) {
        var t2 = testAt(cons, hi);
        if (!t2.sure) sure = false;
        segs.push({ kind: 'point', at: hi, inside: t2.ok });
      }
    }

    var out = [], cur = null;
    segs.forEach(function (s) {
      if (!s.inside) { cur = null; return; }
      if (cur === null) {
        cur = s.kind === 'open'
          ? { lo: s.lo, loClosed: false, hi: s.hi, hiClosed: false }
          : { lo: s.at, loClosed: true, hi: s.at, hiClosed: true };
        out.push(cur);
      } else if (s.kind === 'open') {
        cur.hi = s.hi; cur.hiClosed = false;
      } else {
        cur.hi = s.at; cur.hiClosed = true;
      }
    });
    return { intervals: out, exact: sure, boundaries: pts };
  }

  function ivtext(iv) {
    var lo = iv.lo === null ? '-inf' : iv.lo.text;
    var hi = iv.hi === null ? 'inf' : iv.hi.text;
    if (iv.lo && iv.hi && iv.loClosed && iv.hiClosed && iv.lo.val === iv.hi.val) return '{' + lo + '}';
    return (iv.loClosed ? '[' : '(') + lo + ', ' + hi + (iv.hiClosed ? ']' : ')');
  }
  function domaintext(ivs) {
    if (!ivs.length) return 'empty: no real number is allowed in';
    if (ivs.length === 1 && ivs[0].lo === null && ivs[0].hi === null) return '(-inf, inf)';
    return ivs.map(ivtext).join(' U ');
  }
  function inDomain(ivs, xv) {
    for (var i = 0; i < ivs.length; i += 1) {
      var iv = ivs[i];
      var loOk = iv.lo === null || (iv.loClosed ? xv >= iv.lo.val - 1e-12 : xv > iv.lo.val + 1e-12);
      var hiOk = iv.hi === null || (iv.hiClosed ? xv <= iv.hi.val + 1e-12 : xv < iv.hi.val - 1e-12);
      if (loOk && hiOk) return true;
    }
    return false;
  }

  /* The exact cube root of a rational, when it has one. cbrt(-8) is -2 and
     belongs on the page as -2, not as -1.9999999; cbrt(2) has no rational
     value at all and is printed as the rounded decimal it is. */
  function bicbrt(n) {
    var neg = n < 0n;
    if (neg) n = -n;
    if (n < 2n) return neg ? -n : n;
    var x = n, y = (2n * x + n / (x * x)) / 3n;
    while (y < x) { x = y; y = (2n * x + n / (x * x)) / 3n; }
    return x * x * x === n ? (neg ? -x : x) : null;
  }
  function Rcbrt(a) {
    var p = bicbrt(a.n), q = bicbrt(a.d);
    return (p === null || q === null) ? null : R(p, q);
  }

  /* ---- exact evaluation, where an exact value exists ----
     Eeval returns a double because a grapher needs pixels. This returns a
     RATIONAL, or null when the value is not a rational number. sqrt(4/9) comes
     back as 2/3 and sqrt(2) comes back as null, so a table can print the first
     exactly and label the second as the rounding it is. */
  function Eexact(node, x, v) {
    v = v || 'x';
    if (!node) return null;
    var a, b;
    switch (node.k) {
      case 'num': return Rparse(node.v);
      case 'var': return node.v === v ? x : null;
      case 'neg': a = Eexact(node.a, x, v); return a === null ? null : Rneg(a);
      case 'add': case 'sub': case 'mul':
        a = Eexact(node.a, x, v); b = Eexact(node.b, x, v);
        if (a === null || b === null) return null;
        return node.k === 'add' ? Radd(a, b) : (node.k === 'sub' ? Rsub(a, b) : Rmul(a, b));
      case 'div':
        a = Eexact(node.a, x, v); b = Eexact(node.b, x, v);
        if (a === null || b === null || Rzero(b)) return null;
        return Rdiv(a, b);
      case 'pow': {
        a = Eexact(node.a, x, v); b = Eexact(node.b, x, v);
        if (a === null || b === null || !Rint(b) || b.n > 32n || b.n < -32n) return null;
        if (Rzero(a) && b.n < 0n) return null;
        return Rpow(a, Number(b.n));
      }
      case 'fn': {
        a = Eexact(node.a, x, v);
        if (a === null) return null;
        if (node.v === 'sqrt') return Rsqrt(a);        /* null unless a perfect square */
        if (node.v === 'cbrt') return Rcbrt(a);        /* null unless a perfect cube */
        if (node.v === 'abs') return Rabs(a);
        return null;
      }
    }
    return null;
  }
  /* One value of a function, printed the way the reader should write it: the
     exact rational when there is one, otherwise the decimal WITH the word
     rounded next to it. */
  function valuetext(tree, x, v) {
    var e = Eexact(tree, x, v);
    if (e !== null) return Rtext(e);
    var y = evalAt(tree, Rnum(x), v);
    if (!isFinite(y)) return 'not a real number';
    return approx(y, 5) + ' (rounded)';
  }

  /* A y-window that a pole cannot ruin: the middle 96% of the finite samples,
     which keeps 1/(x-2) on the page instead of scaling it to a flat line. */
  function ywindow(fn, xmin, xmax) {
    var vals = [], i;
    for (i = 0; i <= 240; i += 1) {
      var y = fn(xmin + (xmax - xmin) * i / 240);
      if (typeof y === 'number' && isFinite(y)) vals.push(y);
    }
    if (!vals.length) return { lo: -6, hi: 6 };
    vals.sort(function (a, b) { return a - b; });
    var lo = vals[Math.floor(vals.length * 0.02)], hi = vals[Math.floor((vals.length - 1) * 0.98)];
    lo = Math.min(lo, 0); hi = Math.max(hi, 0);
    if (hi - lo < 4) { var c = (hi + lo) / 2; lo = c - 2; hi = c + 2; }
    var pad = (hi - lo) * 0.12;
    return { lo: lo - pad, hi: hi + pad };
  }

  /* A safe numeric evaluator for a parsed tree: NaN rather than an exception
     wherever the value is not a real number, so a grapher can ask for f(-1) on
     sqrt(x) and simply not plot a point. */
  function evalAt(tree, xv, name) {
    var env = {};
    env[name || 'x'] = xv;
    var y;
    try { y = Eeval(tree, env); } catch (err) { return NaN; }
    return (typeof y === 'number' && isFinite(y)) ? y : NaN;
  }

  /* A decimal that is honest about being one. */
  function approx(v, places) {
    if (!isFinite(v)) return 'undefined';
    var p = places === undefined ? 4 : places;
    var s = v.toFixed(p);
    if (s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    return s === '-0' ? '0' : s;
  }
"""


# ===========================================================================
#  line: the straight line, four ways
# ===========================================================================

# Presets are "x1|y1|x2|y2|m2|b2". The last two matter only in parallel mode,
# where the second line is given the way a question gives it -- by a slope and
# an intercept rather than by two more points.
LINE_PRESETS = {
    "graph": [
        ("through (0, -2) and (3, 4)", "0|-2|3|4|2|-3"),
        ("through (-3, 4) and (1, -2): falling", "-3|4|1|-2|2|-3"),
        ("through (1, 1) and (4, 3): slope 2/3", "1|1|4|3|2|-3"),
        ("through (-4, 3) and (2, 3): horizontal", "-4|3|2|3|2|-3"),
        ("through (2, -5) and (2, 1): vertical", "2|-5|2|1|2|-3"),
        ("through (2, 3) and (2, 3): one point twice", "2|3|2|3|2|-3"),
    ],
    "slope": [
        ("rise 3, run 4: (0, 0) to (4, 3)", "0|0|4|3|2|-3"),
        ("negative: (-2, 5) to (3, -5)", "-2|5|3|-5|2|-3"),
        ("a fraction: (1, 2) to (4, 3)", "1|2|4|3|2|-3"),
        ("horizontal: (-3, 2) to (5, 2), m = 0", "-3|2|5|2|2|-3"),
        ("vertical: (4, -1) to (4, 6), no slope", "4|-1|4|6|2|-3"),
        ("the same point twice: (2, 2) to (2, 2)", "2|2|2|2|2|-3"),
    ],
    "forms": [
        ("(0, 3) and (4, 5)", "0|3|4|5|2|-3"),
        ("(1, -2) and (5, 6): slope 2", "1|-2|5|6|2|-3"),
        ("(-2, 1) and (3, -4): slope -1", "-2|1|3|-4|2|-3"),
        ("(1, 2) and (4, 3): fractions cleared", "1|2|4|3|2|-3"),
        ("(-5, 2) and (4, 2): horizontal", "-5|2|4|2|2|-3"),
        ("(3, -1) and (3, 5): no slope-intercept form", "3|-1|3|5|2|-3"),
    ],
    "pointslope": [
        ("(2, 5) and (6, 13)", "2|5|6|13|2|-3"),
        ("(-3, 4) and (1, -4)", "-3|4|1|-4|2|-3"),
        ("(1, 1) and (7, 5): slope 2/3", "1|1|7|5|2|-3"),
        ("(0, -4) and (5, -4): slope 0", "0|-4|5|-4|2|-3"),
        ("(-6, -1) and (-2, 5)", "-6|-1|-2|5|2|-3"),
        ("(2, 3) and (2, 9): vertical", "2|3|2|9|2|-3"),
    ],
    "parallel": [
        ("parallel: m = 2 and m = 2", "0|1|2|5|2|-3"),
        ("the same line written twice", "0|1|2|5|2|1"),
        ("perpendicular: 2 and -1/2", "0|1|2|5|-1/2|2"),
        ("perpendicular in fractions: 2/3 and -3/2", "0|0|3|2|-3/2|4"),
        ("neither: 3 and 2", "0|0|1|3|2|1"),
        ("vertical and horizontal: no product to take", "2|-3|2|4|0|1"),
    ],
}

LINE_TITLES = {
    "graph": ("The line on the plane", "Two points, the line through them, and what it crosses"),
    "slope": ("Slope", "Rise over run, drawn as the triangle it is"),
    "forms": ("Three forms of one line", "Slope-intercept, point-slope and standard, derived separately"),
    "pointslope": ("Point-slope form", "Either point gives the same line, and the lab proves it"),
    "parallel": ("Parallel and perpendicular", "The product of the slopes, and when there is no product"),
}

LINE_KPIS = {
    "graph": ("Slope", "y-intercept", "x-intercept"),
    "slope": ("Rise", "Run", "Slope"),
    "forms": ("Slope", "y-intercept", "Standard form"),
    "pointslope": ("Slope", "From P1", "From P2"),
    "parallel": ("Slope m1", "Slope m2", "m1 * m2"),
}

LINE_INTRO = {
    "graph": "Pick the two points. The line, its intercepts and the table of values are all "
             "computed from them, so moving a point moves everything.",
    "slope": "Pick the two points and watch the triangle. Rise and run are the sides of it, and "
             "the slope is the fraction they make, reduced exactly.",
    "forms": "Pick the two points. The three forms below are each derived from those points "
             "independently, then checked by substituting both points back in.",
    "pointslope": "Pick the two points. Point-slope form is written from each of them in turn, "
                  "expanded, and the two results are compared as polynomials.",
    "parallel": "The first line comes from the two points; the second is typed as a slope and an "
                "intercept. The product of the slopes decides the question -- when there is one.",
}


def line_lab(cfg):
    """Lines: slope as a drawn triangle, and one line written three ways.

    The teaching decision. A reader who has been shown y = mx + b, then
    y - y1 = m(x - x1), then Ax + By = C tends to file them as three topics.
    They are one line. So every form on this page is derived from the SAME two
    points by its own route -- slope-intercept from m and b, point-slope from a
    point and m, standard by clearing the denominators of the first -- and then
    each is CHECKED by substituting both points back into it. Three independent
    derivations agreeing is evidence that they are the same line; one derivation
    printed three ways would be a claim.

    The second decision is that the failures are on the menu. A vertical line
    has no slope, and the slope formula divides by zero when it meets one --
    so a vertical preset sits in every mode, and the lab explains the division
    rather than throwing or quietly printing "Infinity". The same for two
    points that are the same point: they do not determine a line, and the lab
    says which piece of information is missing.
    """
    mode = cfg.get("mode", "graph")
    if mode not in LINE_PRESETS:
        mode = "graph"
    presets = cfg.get("presets") or LINE_PRESETS[mode]
    title, subtitle = LINE_TITLES[mode]
    ka, kb, kc = LINE_KPIS[mode]
    is_parallel = mode == "parallel"

    options = "".join('<option value="%s">%s</option>' % (value, label) for label, value in presets)
    coords = "".join('<option value="%d">%d</option>' % (n, n) for n in range(-8, 9))

    def coord_field(ident, label):
        return ('        <div class="field">\n'
                '          <label for="%s">%s</label>\n'
                '          <select id="%s">%s</select>\n'
                '        </div>\n' % (ident, label, ident, coords))

    second = ""
    if is_parallel:
        second = ('        <div class="field">\n'
                  '          <label for="lnM2">Second line: slope m2</label>\n'
                  '          <input id="lnM2" type="text" value="2" autocomplete="off">\n'
                  '        </div>\n'
                  '        <div class="field">\n'
                  '          <label for="lnB2">Second line: intercept b2</label>\n'
                  '          <input id="lnB2" type="text" value="-3" autocomplete="off">\n'
                  '        </div>\n')

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="lnTitle">A line</strong><span id="lnSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>the line</span><span class="tone-amber"><i class="legend-swatch"></i>your two points</span><span class="tone-green"><i class="legend-swatch"></i>intercepts</span><span class="tone-purple"><i class="legend-swatch"></i>second line</span></div>
      </div>
      <div class="lab-stage"><svg id="lnPlot"></svg></div>
      <div id="lnWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="lnStatus" style="margin-top:12px;"></div>"""

    controls = ('        <div class="field">\n'
                '          <label for="lnPreset">Example</label>\n'
                '          <select id="lnPreset">' + options + '</select>\n'
                '        </div>\n'
                + coord_field("lnX1", "P1: x")
                + coord_field("lnY1", "P1: y")
                + coord_field("lnX2", "P2: x")
                + coord_field("lnY2", "P2: y")
                + second
                + '        <div class="kpi-grid">\n'
                  '          <div class="kpi"><span>' + ka + '</span><strong id="lnKa">&mdash;</strong></div>\n'
                  '          <div class="kpi"><span>' + kb + '</span><strong id="lnKb">&mdash;</strong></div>\n'
                  '          <div class="kpi"><span>' + kc + '</span><strong id="lnKc">&mdash;</strong></div>\n'
                  '        </div>\n'
                  '        <p class="small-copy" id="lnHint" style="margin:0;">Every number below is recomputed '
                  'from the two points as exact fractions &mdash; nothing is rounded, and nothing is stored.</p>\n')

    second_js = ""
    if is_parallel:
        second_js = ("  inM2 = document.getElementById('lnM2');\n"
                     "  inB2 = document.getElementById('lnB2');\n"
                     "  [inM2, inB2].forEach(function (el) { el.addEventListener('input', redraw); });\n")

    script = BASE_JS + SHARED_JS + r"""
  var MODE = '""" + mode + r"""';
  var preset = document.getElementById('lnPreset');
  var selX1 = document.getElementById('lnX1'), selY1 = document.getElementById('lnY1');
  var selX2 = document.getElementById('lnX2'), selY2 = document.getElementById('lnY2');
  var work = document.getElementById('lnWork'), status = document.getElementById('lnStatus');
  var titleOut = document.getElementById('lnTitle'), subOut = document.getElementById('lnSub');
  var kA = document.getElementById('lnKa'), kB = document.getElementById('lnKb'), kC = document.getElementById('lnKc');
  var svg = document.getElementById('lnPlot');
  var inM2 = null, inB2 = null;

  function ptext(p) { return '(' + Rtext(p.x) + ', ' + Rtext(p.y) + ')'; }

  /* The line through two points, or the reason there is not one. Nothing here
     is a special case bolted on afterwards: a vertical line and a repeated
     point are answers the slope formula genuinely gives, and they are returned
     as answers. */
  function lineOf(p1, p2) {
    var dx = Rsub(p2.x, p1.x), dy = Rsub(p2.y, p1.y);
    if (Rzero(dx) && Rzero(dy)) return { kind: 'point', dx: dx, dy: dy };
    if (Rzero(dx)) return { kind: 'vertical', x: p1.x, dx: dx, dy: dy };
    var m = Rdiv(dy, dx);
    return { kind: 'line', m: m, b: Rsub(p1.y, Rmul(m, p1.x)), dx: dx, dy: dy };
  }

  /* Ax + By = C with whole, coprime coefficients and A >= 0, written out. */
  function standardOf(L) {
    var abc = L.kind === 'vertical'
      ? clearden([R1, R0, L.x])
      : clearden([L.m, R(-1n), Rneg(L.b)]);
    return { A: abc[0], B: abc[1], C: abc[2] };
  }
  function standardtext(s) {
    var left = '';
    if (!Rzero(s.A)) left += coeftext(s.A) + 'x';
    if (!Rzero(s.B)) {
      var neg = Rsign(s.B) < 0, mag = Rabs(s.B);
      left += (left === '' ? (neg ? '-' : '') : (neg ? ' - ' : ' + ')) + (Requ(mag, R1) ? '' : Rterm(mag)) + 'y';
    }
    if (left === '') left = '0';
    return left + ' = ' + Rtext(s.C);
  }
  function slopeinttext(L) { return 'y = ' + Ptext([L.b, L.m]); }
  function pointslopetext(m, p) {
    return shifttext(p.y, 'y') + ' = ' + coeftext(m) + '(' + shifttext(p.x, 'x') + ')';
  }

  function drawline(plot, L, cls) {
    if (L.kind === 'vertical') { plot.vline(Rnum(L.x), cls); return; }
    if (L.kind !== 'line') return;
    var mv = Rnum(L.m), bv = Rnum(L.b);
    plot.curve(function (x) { return mv * x + bv; }, cls);
  }

  function redraw() {
    var p1 = { x: readR(selX1.value), y: readR(selY1.value) };
    var p2 = { x: readR(selX2.value), y: readR(selY2.value) };
    if (p1.x === null || p1.y === null || p2.x === null || p2.y === null) {
      status.innerHTML = '<strong>Both coordinates of both points are needed.</strong> '
        + 'Choose a whole number for each of the four.';
      work.innerHTML = '';
      Plot(svg, { xmin: -8, xmax: 8, ymin: -8, ymax: 8 }).frame();
      return;
    }
    var L = lineOf(p1, p2);
    var std = L.kind === 'point' ? null : standardOf(L);

    /* ---- the window, chosen around the reader's points ---- */
    var x1v = Rnum(p1.x), y1v = Rnum(p1.y), x2v = Rnum(p2.x), y2v = Rnum(p2.y);
    var xlo = Math.min(x1v, x2v) - 4, xhi = Math.max(x1v, x2v) + 4;
    var cand = [y1v, y2v, 0];
    if (L.kind === 'line') {
      cand.push(Rnum(L.m) * xlo + Rnum(L.b));
      cand.push(Rnum(L.m) * xhi + Rnum(L.b));
    }
    var ylo = Math.min.apply(null, cand), yhi = Math.max.apply(null, cand);
    if (yhi - ylo > 3 * (xhi - xlo)) {
      var cy = (y1v + y2v) / 2, half = 1.5 * (xhi - xlo);
      ylo = cy - half; yhi = cy + half;
    }
    var padY = Math.max(1.5, (yhi - ylo) * 0.15);
    var plot = Plot(svg, { xmin: xlo, xmax: xhi, ymin: ylo - padY, ymax: yhi + padY });
    plot.frame();

    var m2 = null, b2 = null, L2 = null;
    if (MODE === 'parallel' && inM2 && inB2) {
      m2 = readR(inM2.value); b2 = readR(inB2.value);
      if (m2 !== null && b2 !== null) L2 = { kind: 'line', m: m2, b: b2 };
    }
    if (L2) drawline(plot, L2, 'plot-curve alt');
    drawline(plot, L, 'plot-curve');

    if (MODE === 'slope' && L.kind !== 'point') {
      /* The triangle IS the definition: along by the run, up by the rise. */
      plot.segment(x1v, y1v, x2v, y1v, 'plot-aux');
      plot.segment(x2v, y1v, x2v, y2v, 'plot-aux');
      plot.label((x1v + x2v) / 2, y1v - (yhi - ylo) * 0.06, 'run = ' + Rtext(L.dx));
      plot.label(x2v + (xhi - xlo) * 0.02, (y1v + y2v) / 2, 'rise = ' + Rtext(L.dy));
    }
    if (L.kind === 'line') {
      plot.point(0, Rnum(L.b), 'plot-point root', 'y-int ' + Rtext(L.b));
      if (!Rzero(L.m)) {
        var xint = Rdiv(Rneg(L.b), L.m);
        plot.point(Rnum(xint), 0, 'plot-point root', 'x-int ' + Rtext(xint));
      }
    } else if (L.kind === 'vertical') {
      plot.point(Rnum(L.x), 0, 'plot-point root', 'x-int ' + Rtext(L.x));
    }
    plot.point(x1v, y1v, 'plot-point', 'P1 ' + ptext(p1));
    if (!(Requ(p1.x, p2.x) && Requ(p1.y, p2.y))) plot.point(x2v, y2v, 'plot-point', 'P2 ' + ptext(p2));

    var headline = L.kind === 'point' ? 'no line yet'
      : (L.kind === 'vertical' ? 'x = ' + Rtext(L.x) : slopeinttext(L));
    titleOut.textContent = headline;
    subOut.textContent = 'P1 ' + ptext(p1) + '   P2 ' + ptext(p2);
    plot.describe('The line through ' + ptext(p1) + ' and ' + ptext(p2)
      + ', drawn by evaluating it across the window, with the points and intercepts marked.');

    /* ---- the numbers ---- */
    var blocks = [], msg;
    var slopeText = L.kind === 'line' ? Rtext(L.m)
      : (L.kind === 'vertical' ? 'undefined' : 'not determined');

    if (L.kind === 'point') {
      kA.textContent = 'undefined'; kB.innerHTML = '&mdash;'; kC.innerHTML = '&mdash;';
      blocks.push(table('Two points that are one point', [
        row('P1 and P2', ptext(p1) + ' and ' + ptext(p2) + ' are the same point'),
        row('rise', 'y2 - y1 = ' + Rtext(L.dy)),
        row('run', 'x2 - x1 = ' + Rtext(L.dx)),
        row('slope', '0/0, which is not a number: every line through this point fits'),
      ]));
      work.innerHTML = blocks.join('');
      status.innerHTML = '<strong>One point does not determine a line.</strong> '
        + 'The slope formula gives 0/0 here, and that is not "zero" &mdash; it is the arithmetic '
        + 'saying the question is underdetermined. Infinitely many lines pass through '
        + ptext(p1) + '. Move either point and exactly one of them is selected.';
      return;
    }

    if (MODE === 'slope') {
      kA.textContent = Rtext(L.dy); kB.textContent = Rtext(L.dx); kC.textContent = slopeText;
    } else if (MODE === 'parallel') {
      kA.textContent = slopeText;
      kB.textContent = m2 === null ? 'unreadable' : Rtext(m2);
      kC.textContent = (L.kind === 'vertical' || m2 === null) ? 'undefined' : Rtext(Rmul(L.m, m2));
    } else if (MODE === 'pointslope') {
      kA.textContent = slopeText;
      kB.textContent = L.kind === 'vertical' ? 'x = ' + Rtext(L.x) : pointslopetext(L.m, p1);
      kC.textContent = L.kind === 'vertical' ? 'x = ' + Rtext(L.x) : pointslopetext(L.m, p2);
    } else if (MODE === 'forms') {
      kA.textContent = slopeText;
      kB.textContent = L.kind === 'vertical' ? 'none' : Rtext(L.b);
      kC.textContent = standardtext(std);
    } else {
      kA.textContent = slopeText;
      kB.textContent = L.kind === 'vertical' ? 'none' : Rtext(L.b);
      kC.textContent = L.kind === 'vertical' ? Rtext(L.x)
        : (Rzero(L.m) ? (Rzero(L.b) ? 'every x' : 'none') : Rtext(Rdiv(Rneg(L.b), L.m)));
    }

    if (MODE === 'graph') {
      var rows = [
        row('the two points', ptext(p1) + ' and ' + ptext(p2)),
        row('slope', L.kind === 'vertical'
          ? 'undefined: the run is 0, and ' + Rtext(L.dy) + '/0 is not a number'
          : Rtext(L.dy) + ' / ' + Rtext(L.dx) + ' = ' + Rtext(L.m)),
        row('equation', L.kind === 'vertical' ? 'x = ' + Rtext(L.x) : slopeinttext(L)),
      ];
      if (L.kind === 'vertical') {
        rows.push(row('crosses the x-axis', 'at (' + Rtext(L.x) + ', 0)'));
        rows.push(row('crosses the y-axis', Rzero(L.x) ? 'it IS the y-axis' : 'never: a vertical line misses it unless it is the axis'));
      } else {
        rows.push(row('crosses the y-axis', 'at (0, ' + Rtext(L.b) + '), because x = 0 gives y = ' + Rtext(L.b)));
        rows.push(row('crosses the x-axis', Rzero(L.m)
          ? (Rzero(L.b) ? 'everywhere: this IS the x-axis' : 'never: a horizontal line at height ' + Rtext(L.b) + ' has no zero')
          : 'at (' + Rtext(Rdiv(Rneg(L.b), L.m)) + ', 0), from 0 = ' + Ptext([L.b, L.m])));
        rows.push(row('direction', Rzero(L.m) ? 'horizontal: every x gives the same y'
          : (Rsign(L.m) > 0 ? 'rising: y grows by ' + Rtext(L.m) + ' for every 1 across'
                            : 'falling: y drops by ' + Rtext(Rabs(L.m)) + ' for every 1 across')));
      }
      blocks.push(table('What the picture says, computed', rows));
      var vals = [];
      for (var i = -2; i <= 2; i += 1) {
        var xv = Radd(p1.x, R(BigInt(i)));
        vals.push('<tr><td>' + Rtext(xv) + '</td><td>'
          + (L.kind === 'vertical' ? (Requ(xv, L.x) ? 'every y' : 'no y') : Rtext(Peval([L.b, L.m], xv)))
          + '</td></tr>');
      }
      blocks.push('<div class="table-wrap"><table class="tt"><caption>A table of values, evaluated one at a time'
        + '</caption><thead><tr><th>x</th><th>y</th></tr></thead><tbody>' + vals.join('') + '</tbody></table></div>');
      msg = L.kind === 'vertical'
        ? '<strong>This line is vertical, so it is not a function of x.</strong> The equation is x = '
          + Rtext(L.x) + ' &mdash; it says nothing about y, because every y is on it. There is no '
          + 'y = mx + b for this line, which is the first sign that "line" and "linear function" '
          + 'are not the same word.'
        : '<strong>' + slopeinttext(L) + '.</strong> The slope ' + Rtext(L.m)
          + ' was computed from your two points as ' + Rtext(L.dy) + '/' + Rtext(L.dx)
          + ', and the intercept from y1 - m*x1 = ' + Rtext(p1.y) + ' - (' + Rtext(L.m) + ')('
          + Rtext(p1.x) + ') = ' + Rtext(L.b) + '. Both marked points sit on the drawn line because '
          + 'the drawing evaluates that same equation.';
    }

    if (MODE === 'slope') {
      if (L.kind === 'vertical') {
        blocks.push(table('The slope formula meets a vertical line', [
          row('rise', 'y2 - y1 = ' + subtext(p2.y, p1.y) + ' = ' + Rtext(L.dy)),
          row('run', 'x2 - x1 = ' + subtext(p2.x, p1.x) + ' = 0'),
          row('m = rise/run', Rtext(L.dy) + ' / 0, which is not a number'),
          row('so', 'this line has NO slope. That is different from slope 0, which is a horizontal line.'),
        ]));
        msg = '<strong>No slope is not slope zero.</strong> A horizontal line has slope 0: go across 1, '
          + 'rise 0. This line goes up ' + Rtext(L.dy) + ' while going across 0, and dividing by 0 is '
          + 'not an operation. Pick two points with different x values and the formula starts working again.';
      } else {
        var third = { x: Radd(p1.x, Rmul(R(2n), L.dx)), y: Radd(p1.y, Rmul(R(2n), L.dy)) };
        blocks.push(table('Rise over run, on your two points', [
          row('rise = y2 - y1', subtext(p2.y, p1.y) + ' = ' + Rtext(L.dy)),
          row('run = x2 - x1', subtext(p2.x, p1.x) + ' = ' + Rtext(L.dx)),
          row('m = rise / run', Rtext(L.dy) + ' / ' + Rtext(L.dx) + ' = ' + Rtext(L.m)),
          row('the other order', '(y1 - y2)/(x1 - x2) = ' + Rtext(Rneg(L.dy)) + ' / ' + Rtext(Rneg(L.dx))
            + ' = ' + Rtext(Rdiv(Rneg(L.dy), Rneg(L.dx)))
            + ' &mdash; the same, because both signs flipped'),
          row('a different pair', 'from ' + ptext(p1) + ' to ' + ptext(third) + ': '
            + Rtext(Rsub(third.y, p1.y)) + ' / ' + Rtext(Rsub(third.x, p1.x)) + ' = '
            + Rtext(Rdiv(Rsub(third.y, p1.y), Rsub(third.x, p1.x)))),
        ]));
        msg = '<strong>Slope ' + Rtext(L.m) + ': the triangle above has sides ' + Rtext(L.dy)
          + ' and ' + Rtext(L.dx) + '.</strong> The last row picks a third point on the same line and '
          + 'gets the same fraction, which is the fact that makes slope a property of the LINE rather '
          + 'than of the two points you happened to pick. '
          + (Rzero(L.m) ? 'Here the rise is 0, so the slope is 0 and the line is horizontal.'
             : 'Reducing ' + Rtext(L.dy) + '/' + Rtext(L.dx) + ' to ' + Rtext(L.m)
               + ' is exact fraction arithmetic, not a decimal.');
      }
    }

    if (MODE === 'forms') {
      if (L.kind === 'vertical') {
        blocks.push(table('Three forms, one of which does not exist', [
          row('slope-intercept', muted('y = mx + b needs a slope m, and this line has none')),
          row('point-slope', muted('y - y1 = m(x - x1) needs the same m')),
          row('standard: Ax + By = C', standardtext(std) + ', with B = 0'),
          row('why standard survives', 'B = 0 is allowed, so standard form can write every line. '
            + 'That is the reason it exists.'),
        ]));
        msg = '<strong>Standard form is the only one of the three that can write this line.</strong> '
          + 'Ax + By = C with B = 0 gives ' + standardtext(std) + '. Slope-intercept and point-slope '
          + 'both require a slope, and a vertical line has none &mdash; so a question that says '
          + '"write it in y = mx + b form" has no answer here.';
      } else {
        var si = [L.b, L.m];
        var check1 = Peval(si, p1.x), check2 = Peval(si, p2.x);
        var stdL1 = Radd(Rmul(std.A, p1.x), Rmul(std.B, p1.y));
        var stdL2 = Radd(Rmul(std.A, p2.x), Rmul(std.B, p2.y));
        blocks.push(table('The same line, three ways, each derived on its own', [
          row('slope-intercept', slopeinttext(L) + '   (m from the two points, b = y1 - m*x1)'),
          row('point-slope, from P1', pointslopetext(L.m, p1)),
          row('point-slope, from P2', pointslopetext(L.m, p2)),
          row('standard form', standardtext(std) + '   (denominators cleared, gcd divided out, A >= 0)'),
        ]));
        blocks.push(table('Checked by substitution, not by assertion', [
          row('P1 in y = mx + b', 'm(' + Rtext(p1.x) + ') + b = ' + Rtext(check1) + ', and y1 = '
            + Rtext(p1.y) + ' ' + (Requ(check1, p1.y) ? chip('agrees', 'ok') : chip('disagrees', 'no'))),
          row('P2 in y = mx + b', 'm(' + Rtext(p2.x) + ') + b = ' + Rtext(check2) + ', and y2 = '
            + Rtext(p2.y) + ' ' + (Requ(check2, p2.y) ? chip('agrees', 'ok') : chip('disagrees', 'no'))),
          row('P1 in Ax + By', Rtext(std.A) + '(' + Rtext(p1.x) + ') + ' + Rterm(std.B) + '('
            + Rtext(p1.y) + ') = ' + Rtext(stdL1) + ', and C = ' + Rtext(std.C) + ' '
            + (Requ(stdL1, std.C) ? chip('agrees', 'ok') : chip('disagrees', 'no'))),
          row('P2 in Ax + By', Rtext(std.A) + '(' + Rtext(p2.x) + ') + ' + Rterm(std.B) + '('
            + Rtext(p2.y) + ') = ' + Rtext(stdL2) + ', and C = ' + Rtext(std.C) + ' '
            + (Requ(stdL2, std.C) ? chip('agrees', 'ok') : chip('disagrees', 'no'))),
        ]));
        var mult = L.m.d * L.b.d / bgcd(L.m.d, L.b.d);
        msg = '<strong>One line, three spellings.</strong> ' + slopeinttext(L) + ' and '
          + standardtext(std) + ' are the same set of points: '
          + (mult === 1n
             ? 'the slope and the intercept are already whole numbers here, so standard form only '
               + 'needed the terms moved to one side and the gcd divided out'
             : 'the standard form came from multiplying the slope-intercept form by ' + mult
               + ' to clear the denominators and then dividing by the gcd of the coefficients')
          + '. Which form you want depends on the question &mdash; '
          + 'slope-intercept to sketch, point-slope to write a line through a known point, standard to '
          + 'keep whole numbers and to survive the vertical case.';
      }
    }

    if (MODE === 'pointslope') {
      if (L.kind === 'vertical') {
        blocks.push(table('Point-slope needs a slope', [
          row('the two points', ptext(p1) + ' and ' + ptext(p2)),
          row('m', 'undefined: the run is 0'),
          row('y - y1 = m(x - x1)', muted('cannot be written: there is no m to put in it')),
          row('the line is still a line', 'x = ' + Rtext(L.x)),
        ]));
        msg = '<strong>Every form that starts "y =" fails on a vertical line.</strong> '
          + 'Point-slope is one of them. The line through your two points is x = ' + Rtext(L.x)
          + ', and it is written that way precisely because y is not a function of x here.';
      } else {
        var e1 = Padd(Pmul([L.m], [Rneg(p1.x), R1]), [p1.y]);
        var e2 = Padd(Pmul([L.m], [Rneg(p2.x), R1]), [p2.y]);
        var same = Pzero(Psub(e1, e2));
        blocks.push(table('The same line from either point', [
          row('slope', Rtext(L.dy) + ' / ' + Rtext(L.dx) + ' = ' + Rtext(L.m)),
          row('from P1 ' + ptext(p1), pointslopetext(L.m, p1)),
          row('expand', 'y = ' + Rterm(L.m) + '(' + shifttext(p1.x, 'x') + ') + ' + Rtext(p1.y)
            + ' = ' + Ptext(e1)),
          row('from P2 ' + ptext(p2), pointslopetext(L.m, p2)),
          row('expand', 'y = ' + Rterm(L.m) + '(' + shifttext(p2.x, 'x') + ') + ' + Rtext(p2.y)
            + ' = ' + Ptext(e2)),
          row('subtract the two', Ptext(e1) + ' - (' + Ptext(e2) + ') = ' + Ptext(Psub(e1, e2)) + ' '
            + (same ? chip('identical', 'ok') : chip('different', 'no'))),
        ]));
        msg = '<strong>Two different-looking equations, one line.</strong> '
          + pointslopetext(L.m, p1) + ' and ' + pointslopetext(L.m, p2)
          + ' expand to the same ' + slopeinttext(L) + ', and the lab checks that by subtracting them '
          + 'as polynomials and getting ' + Ptext(Psub(e1, e2)) + '. So "which point do I use?" has the '
          + 'answer: either. Point-slope is the form to reach for when a question hands you a point and '
          + 'a slope, because no rearranging is needed to write it down.';
      }
    }

    if (MODE === 'parallel') {
      if (m2 === null || b2 === null) {
        blocks.push(table('The second line', [
          row('what was typed', 'm2 = "' + (inM2 ? inM2.value : '') + '", b2 = "' + (inB2 ? inB2.value : '') + '"'),
          row('the problem', 'each must be a whole number or a fraction such as -3/2'),
        ]));
        msg = '<strong>The second line could not be read.</strong> Type its slope and its y-intercept '
          + 'as whole numbers or fractions &mdash; for example m2 = -1/2 and b2 = 4. The first line, '
          + 'from your two points, is drawn above and is unaffected.';
      } else if (L.kind === 'vertical') {
        var meet = { x: L.x, y: Radd(Rmul(m2, L.x), b2) };
        blocks.push(table('One vertical line and one with a slope', [
          row('line 1', 'x = ' + Rtext(L.x) + ', slope undefined'),
          row('line 2', 'y = ' + Ptext([b2, m2]) + ', slope ' + Rtext(m2)),
          row('m1 * m2', muted('there is no m1 to multiply: the test needs both slopes to exist')),
          row('perpendicular?', Rzero(m2)
            ? chip('yes', 'ok') + ' a vertical line and a horizontal line meet at a right angle, and the '
              + 'product test simply cannot see it'
            : chip('no', 'no') + ' they meet at ' + '(' + Rtext(meet.x) + ', ' + Rtext(meet.y) + ') but not squarely'),
          row('they meet at', '(' + Rtext(meet.x) + ', ' + Rtext(meet.y) + ')'),
        ]));
        plot.point(Rnum(meet.x), Rnum(meet.y), 'plot-point vertex', 'meet');
        msg = '<strong>The rule m1*m2 = -1 has an exception, and this is it.</strong> '
          + 'A vertical line has no slope, so there is no product to take. '
          + (Rzero(m2)
             ? 'These two ARE perpendicular &mdash; x = ' + Rtext(L.x) + ' and y = ' + Rtext(b2)
               + ' meet at a right angle &mdash; and the product test still says nothing. A rule that '
               + 'is silent on a case is not the same as a rule that is false there, but you have to '
               + 'know which case you are in.'
             : 'Rotate the second line to horizontal (m2 = 0) and the pair becomes perpendicular '
               + 'without the product ever existing.');
      } else {
        var prod = Rmul(L.m, m2);
        var same = Requ(L.m, m2), sameLine = same && Requ(L.b, b2);
        var perp = Requ(prod, R(-1n));
        var rows2 = [
          row('line 1, from your points', slopeinttext(L) + '   (m1 = ' + Rtext(L.m) + ')'),
          row('line 2, as typed', 'y = ' + Ptext([b2, m2]) + '   (m2 = ' + Rtext(m2) + ')'),
          row('m1 * m2', Rterm(L.m) + ' * ' + Rterm(m2) + ' = ' + Rtext(prod)),
          row('parallel?', sameLine
            ? chip('same line', 'hi') + ' one line written twice, which is not what parallel means'
            : (same ? chip('yes', 'ok') + ' equal slopes, different intercepts'
                    : chip('no', 'no') + ' the slopes differ')),
          row('perpendicular?', perp ? chip('yes', 'ok') + ' the product is exactly -1'
            : chip('no', 'no') + ' the product is ' + Rtext(prod) + ', not -1'),
        ];
        if (sameLine) {
          rows2.push(row('solve line1 = line2', Ptext([L.b, L.m]) + ' = ' + Ptext([b2, m2])
            + ' holds for every x: these are the same line, and every point on it is an intersection'));
        } else if (same) {
          rows2.push(row('solve line1 = line2', Ptext([L.b, L.m]) + ' = ' + Ptext([b2, m2])
            + ' gives ' + Rtext(L.b) + ' = ' + Rtext(b2) + ', which is false: no intersection at all'));
        } else {
          var xi = Rdiv(Rsub(b2, L.b), Rsub(L.m, m2));
          var yi = Radd(Rmul(L.m, xi), L.b);
          var yi2 = Radd(Rmul(m2, xi), b2);
          rows2.push(row('solve line1 = line2', 'x = (b2 - b1)/(m1 - m2) = ' + Rtext(Rsub(b2, L.b)) + ' / '
            + Rtext(Rsub(L.m, m2)) + ' = ' + Rtext(xi)));
          rows2.push(row('the meeting point', '(' + Rtext(xi) + ', ' + Rtext(yi) + '), and line 2 gives y = '
            + Rtext(yi2) + ' there ' + (Requ(yi, yi2) ? chip('agrees', 'ok') : chip('disagrees', 'no'))));
          plot.point(Rnum(xi), Rnum(yi), 'plot-point vertex', 'meet');
        }
        blocks.push(table('Two lines, compared', rows2));
        if (sameLine) {
          msg = '<strong>These are the same line, not two parallel ones.</strong> Equal slopes AND equal '
            + 'intercepts. "Parallel" is usually taken to mean two distinct lines that never meet; this pair '
            + 'meets everywhere. The algebra says so too: setting them equal reduces to '
            + Rtext(L.b) + ' = ' + Rtext(b2) + ', which is true for every x.';
        } else if (same) {
          msg = '<strong>Parallel: equal slopes, different intercepts.</strong> Setting the two right-hand '
            + 'sides equal cancels the x terms and leaves ' + Rtext(L.b) + ' = ' + Rtext(b2)
            + ', which is false &mdash; and "the algebra ends in a false statement" is exactly what '
            + '"these lines never meet" looks like when you solve it.';
        } else if (perp) {
          msg = '<strong>Perpendicular: m1 * m2 = ' + Rtext(L.m) + ' * ' + Rtext(m2) + ' = -1.</strong> '
            + 'Each slope is the negative reciprocal of the other: flip ' + Rtext(L.m) + ' to get '
            + Rtext(Rinv(L.m)) + ', then negate. Note that this is not "the slopes are opposite" &mdash; '
            + Rtext(Rneg(L.m)) + ' would be a reflection, not a right angle.';
        } else {
          msg = '<strong>Neither: the product is ' + Rtext(prod) + '.</strong> Parallel needs the slopes '
            + 'equal and perpendicular needs the product to be exactly -1, so these two lines simply cross. '
            + 'They cross once, because two lines with different slopes always do.';
        }
      }
    }

    work.innerHTML = blocks.join('');
    status.innerHTML = msg;
  }

  preset.addEventListener('change', function () {
    var parts = preset.value.split('|');
    selX1.value = parts[0]; selY1.value = parts[1];
    selX2.value = parts[2]; selY2.value = parts[3];
    if (inM2 && inB2) { inM2.value = parts[4]; inB2.value = parts[5]; }
    redraw();
  });
  [selX1, selY1, selX2, selY2].forEach(function (el) { el.addEventListener('change', redraw); });
""" + second_js + r"""
  var first = preset.value.split('|');
  selX1.value = first[0]; selY1.value = first[1];
  selX2.value = first[2]; selY2.value = first[3];
  if (inM2 && inB2) { inM2.value = first[4]; inB2.value = first[5]; }
  redraw();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose the two points"),
        panel_intro=cfg.get("panel_intro", LINE_INTRO[mode]),
        script=script,
    )


# ===========================================================================
#  grapher: the reader's own function, drawn and analysed
# ===========================================================================

GRAPHER_PRESETS = {
    "plane": [
        ("one point in each quadrant", "(2, 3) (-2, 3) (-2, -3) (2, -3)"),
        ("points on the axes, and the origin", "(0, 4) (-3, 0) (0, 0)"),
        ("a vertical pair: same x", "(2, 1) (2, 5)"),
        ("a 3-4-5 triangle", "(0, 0) (3, 4) (3, 0)"),
        ("a distance that is irrational", "(0, 0) (1, 1)"),
        ("fractional coordinates", "(1/2, 3/2) (-5/2, 1/2)"),
    ],
    "polynomial": [
        ("x^3 - x", "x^3 - x"),
        ("x^3 - 3x + 2", "x^3 - 3x + 2"),
        ("x^4 - 5x^2 + 4", "x^4 - 5x^2 + 4"),
        ("2x^3 - 3x^2 - 11x + 6", "2x^3 - 3x^2 - 11x + 6"),
        ("x^2 + 1", "x^2 + 1"),
        ("x^3", "x^3"),
    ],
    "radical": [
        ("sqrt(x - 3)", "sqrt(x - 3)"),
        ("sqrt(9 - x^2)", "sqrt(9 - x^2)"),
        ("sqrt(x^2 - 4)", "sqrt(x^2 - 4)"),
        ("1/sqrt(x - 1)", "1/sqrt(x - 1)"),
        ("sqrt(x) + sqrt(2 - x)", "sqrt(x) + sqrt(2 - x)"),
        ("cbrt(x)", "cbrt(x)"),
    ],
}

GRAPHER_TITLES = {
    "plane": ("The coordinate plane", "Points, quadrants, midpoints and exact distances"),
    "polynomial": ("Graphing a polynomial", "Zeros with their multiplicity, and where the ends go"),
    "radical": ("A domain that stops", "Where a square root refuses, computed from the radicand"),
}

GRAPHER_KPIS = {
    "plane": ("Points read", "Quadrants used", "P1 to P2"),
    "polynomial": ("Degree", "Real zeros", "y-intercept"),
    "radical": ("Domain", "Endpoints", "y-intercept"),
}

GRAPHER_LABELS = {
    "plane": "Points, as (x, y)",
    "polynomial": "y = f(x)",
    "radical": "y = f(x)",
}

GRAPHER_HINTS = {
    "plane": "Write each point in brackets: <code>(2, -3)</code>. Fractions are allowed, "
             "and every distance below is exact.",
    "polynomial": "Type any polynomial: <code>2x^3 - 3x^2 - 11x + 6</code>. Implicit "
                  "multiplication and <code>^</code> both work.",
    "radical": "Type a formula with <code>sqrt(...)</code> or <code>cbrt(...)</code> in it. "
               "The domain below is solved from the radicand, not read off the picture.",
}

GRAPHER_INTRO = {
    "plane": "Type points and they are plotted. The quadrant, the midpoint and the distance "
             "are computed from the coordinates as exact fractions and surds.",
    "polynomial": "Type a polynomial. Its zeros are SEARCHED for with the rational root theorem, "
                  "each one's multiplicity is found by dividing, and the end behaviour comes from "
                  "the leading term.",
    "radical": "Type a formula with a square root in it. The lab collects what the root demands, "
               "solves it, and draws the graph only where the function is a real number.",
}


def grapher_lab(cfg):
    """The free grapher: the reader's formula, drawn and then interrogated.

    The teaching decision. A graphing tool that only draws teaches reading
    pictures, and a picture cannot tell you whether a curve touches the axis or
    crosses it, or whether it stops at 3 or at 2.999. So this lab draws the
    curve by sampling the reader's own formula AND analyses the same formula
    exactly, and the two are shown together:

      plane       coordinates are the subject, so there is no formula at all --
                  points, their quadrants, an exact midpoint, and a distance
                  that is a surd when it is a surd.
      polynomial  the zeros come out of the rational root search, their
                  multiplicities out of repeated division, and the end
                  behaviour out of the leading term. A polynomial with no
                  rational zero returns an EMPTY search, and the lab says so
                  rather than drawing a picture and letting the reader guess.
      radical     the domain is solved from the radicand. The curve is drawn
                  only where the function is real, so the drawing stops in the
                  same place the algebra says it stops.

    The presets are chosen to include what breaks: a polynomial whose only
    rational root is 1/2 (which the "try the divisors of the constant" version
    of the theorem misses), one with no real zero at all, a domain with a gap
    in the middle, and a root whose endpoint is excluded because it sits under
    a division.
    """
    mode = cfg.get("mode", "polynomial")
    if mode not in GRAPHER_PRESETS:
        mode = "polynomial"
    presets = cfg.get("presets") or GRAPHER_PRESETS[mode]
    title, subtitle = GRAPHER_TITLES[mode]
    ka, kb, kc = GRAPHER_KPIS[mode]

    options = "".join('<option value="%s">%s</option>' % (value, label) for label, value in presets)
    spans = [("5", "-5 to 5"), ("8", "-8 to 8"), ("12", "-12 to 12"), ("20", "-20 to 20")]
    span_options = "".join('<option value="%s">x from %s</option>' % (v, t) for v, t in spans)

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="grTitle">Grapher</strong><span id="grSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>the graph</span><span class="tone-green"><i class="legend-swatch"></i>zeros</span><span class="tone-amber"><i class="legend-swatch"></i>points and intercepts</span><span class="tone-red"><i class="legend-swatch"></i>excluded</span></div>
      </div>
      <div class="lab-stage"><svg id="grPlot"></svg></div>
      <div id="grWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="grStatus" style="margin-top:12px;"></div>"""

    controls = ('        <div class="field">\n'
                '          <label for="grPreset">Example</label>\n'
                '          <select id="grPreset">' + options + '</select>\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <label for="grExpr">' + GRAPHER_LABELS[mode] + '</label>\n'
                '          <input id="grExpr" type="text" value="" autocomplete="off" spellcheck="false">\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <label for="grSpan">Window</label>\n'
                '          <select id="grSpan">' + span_options + '</select>\n'
                '        </div>\n'
                '        <div class="kpi-grid">\n'
                '          <div class="kpi"><span>' + ka + '</span><strong id="grKa">&mdash;</strong></div>\n'
                '          <div class="kpi"><span>' + kb + '</span><strong id="grKb">&mdash;</strong></div>\n'
                '          <div class="kpi"><span>' + kc + '</span><strong id="grKc">&mdash;</strong></div>\n'
                '        </div>\n'
                '        <p class="small-copy" id="grHint" style="margin:0;">' + GRAPHER_HINTS[mode] + '</p>\n')

    script = BASE_JS + SHARED_JS + r"""
  var MODE = '""" + mode + r"""';
  var preset = document.getElementById('grPreset');
  var input = document.getElementById('grExpr');
  var spanSel = document.getElementById('grSpan');
  var work = document.getElementById('grWork'), status = document.getElementById('grStatus');
  var titleOut = document.getElementById('grTitle'), subOut = document.getElementById('grSub');
  var kA = document.getElementById('grKa'), kB = document.getElementById('grKb'), kC = document.getElementById('grKc');
  var svg = document.getElementById('grPlot');

  /* ---- reading points, for the plane ---- */
  function readpoints(src) {
    var out = [], bad = [], re = /\(([^()]*)\)/g, m;
    while ((m = re.exec(src))) {
      var parts = m[1].split(',');
      if (parts.length !== 2) { bad.push(m[0]); continue; }
      var x = readR(parts[0].trim()), y = readR(parts[1].trim());
      if (x === null || y === null) { bad.push(m[0]); continue; }
      out.push({ x: x, y: y });
    }
    return { points: out, bad: bad };
  }
  function quadrant(p) {
    var sx = Rsign(p.x), sy = Rsign(p.y);
    if (sx === 0 && sy === 0) return 'the origin';
    if (sx === 0) return 'on the y-axis, in no quadrant';
    if (sy === 0) return 'on the x-axis, in no quadrant';
    if (sy > 0) return sx > 0 ? 'I' : 'II';
    return sx > 0 ? 'IV' : 'III';
  }
  function ptext(p) { return '(' + Rtext(p.x) + ', ' + Rtext(p.y) + ')'; }
  /* Exact distance: d^2 is a rational, and its square root is either rational
     or a surd. Both are answers; only one of them is a decimal. */
  function distance(a, b) {
    var dx = Rsub(b.x, a.x), dy = Rsub(b.y, a.y);
    var sq = Radd(Rmul(dx, dx), Rmul(dy, dy));
    var s = Rsurd(sq);
    return { dx: dx, dy: dy, sq: sq, surd: s,
             text: surdtext(s), exact: s.k === 1n,
             num: Rnum(s.q) * Math.sqrt(Number(s.k)) };
  }

  function redraw() {
    var span = parseFloat(spanSel.value) || 8;
    var raw = input.value, body = bodyof(raw);
    var blocks = [], msg = '';

    /* ------------------------------------------------------ plane mode --- */
    if (MODE === 'plane') {
      var got = readpoints(raw);
      var pts = got.points;
      var xs = pts.map(function (p) { return Rnum(p.x); });
      var ys = pts.map(function (p) { return Rnum(p.y); });
      var half = Math.max(span, 2);
      xs.concat(ys).forEach(function (v) { half = Math.max(half, Math.abs(v) + 1); });
      var plot = Plot(svg, { xmin: -half, xmax: half, ymin: -half, ymax: half });
      plot.frame();
      pts.forEach(function (p, i) {
        plot.point(Rnum(p.x), Rnum(p.y), 'plot-point', 'P' + (i + 1) + ' ' + ptext(p));
      });
      if (pts.length >= 2) {
        var d = distance(pts[0], pts[1]);
        /* The distance formula IS Pythagoras: draw the two legs it uses. */
        plot.segment(Rnum(pts[0].x), Rnum(pts[0].y), Rnum(pts[1].x), Rnum(pts[0].y), 'plot-aux');
        plot.segment(Rnum(pts[1].x), Rnum(pts[0].y), Rnum(pts[1].x), Rnum(pts[1].y), 'plot-aux');
        plot.segment(Rnum(pts[0].x), Rnum(pts[0].y), Rnum(pts[1].x), Rnum(pts[1].y), 'plot-curve');
        var mid = { x: Rdiv(Radd(pts[0].x, pts[1].x), R(2n)), y: Rdiv(Radd(pts[0].y, pts[1].y), R(2n)) };
        plot.point(Rnum(mid.x), Rnum(mid.y), 'plot-point vertex', 'midpoint ' + ptext(mid));
      }
      plot.describe(pts.length + ' points plotted from the coordinates typed.');

      titleOut.textContent = pts.length + (pts.length === 1 ? ' point' : ' points');
      subOut.textContent = pts.map(ptext).join('  ');
      var quads = {};
      pts.forEach(function (p) { var q = quadrant(p); if (q.length <= 3) quads[q] = 1; });
      kA.textContent = String(pts.length);
      kB.textContent = Object.keys(quads).sort().join(', ') || 'none';
      if (pts.length >= 2) kC.textContent = distance(pts[0], pts[1]).text;
      else kC.innerHTML = '&mdash;';

      if (!pts.length) {
        status.innerHTML = '<strong>No point could be read from that.</strong> '
          + 'Write each one in brackets with a comma between the coordinates, like '
          + '<code>(2, -3)</code>, and separate them with spaces. Fractions such as '
          + '<code>(1/2, -5/2)</code> are fine. '
          + (got.bad.length ? 'What could not be read: ' + got.bad.join(' ') + '.' : '');
        work.innerHTML = '';
        return;
      }
      var prows = pts.map(function (p, i) {
        var dist = distance({ x: R0, y: R0 }, p);
        return '<tr><td>P' + (i + 1) + '</td><td>' + Rtext(p.x) + '</td><td>' + Rtext(p.y)
          + '</td><td>' + quadrant(p) + '</td><td>' + dist.text
          + (dist.exact ? '' : ' = ' + approx(dist.num, 4) + ' rounded') + '</td></tr>';
      });
      blocks.push('<div class="table-wrap"><table class="tt"><caption>Each point, read from its two '
        + 'coordinates</caption><thead><tr><th>point</th><th>x</th><th>y</th><th>quadrant</th>'
        + '<th>distance from (0, 0)</th></tr></thead><tbody>' + prows.join('') + '</tbody></table></div>');

      if (pts.length >= 2) {
        var d2 = distance(pts[0], pts[1]);
        var mid2 = { x: Rdiv(Radd(pts[0].x, pts[1].x), R(2n)), y: Rdiv(Radd(pts[0].y, pts[1].y), R(2n)) };
        blocks.push(table('P1 to P2, computed from the four coordinates', [
          row('across', 'x2 - x1 = ' + subtext(pts[1].x, pts[0].x) + ' = ' + Rtext(d2.dx)),
          row('up', 'y2 - y1 = ' + subtext(pts[1].y, pts[0].y) + ' = ' + Rtext(d2.dy)),
          row('d^2 = dx^2 + dy^2', Rtext(Rmul(d2.dx, d2.dx)) + ' + ' + Rtext(Rmul(d2.dy, d2.dy))
            + ' = ' + Rtext(d2.sq)),
          row('d', 'sqrt(' + Rtext(d2.sq) + ')'
            + (d2.text === 'sqrt(' + Rtext(d2.sq) + ')' ? ', which is already in simplest form'
                                                        : ' = ' + d2.text)
            + (d2.exact ? '  ' + chip('exact and rational', 'ok')
                        : '  ' + chip('irrational: ' + approx(d2.num, 6) + ' is rounded', 'hi'))),
          row('midpoint', '((' + sumtext(pts[0].x, pts[1].x) + ')/2, ('
            + sumtext(pts[0].y, pts[1].y) + ')/2) = ' + ptext(mid2)),
        ]));
        msg = '<strong>The distance from P1 to P2 is ' + d2.text + '.</strong> '
          + (d2.exact
             ? 'It came out rational this time because ' + Rtext(d2.sq) + ' is a perfect square. '
             : 'sqrt(' + Rtext(d2.sq) + ') is irrational, so ' + d2.text + ' IS the answer; '
               + approx(d2.num, 6) + ' is a rounding of it and loses information. ')
          + 'The two dashed legs above are the dx and dy in the formula &mdash; the distance formula is '
          + 'Pythagoras applied to that triangle, which is why it has a square root in it at all.';
      } else {
        msg = '<strong>One point is ' + quadrant(pts[0]) + '.</strong> Add a second point in brackets '
          + 'and the lab computes the distance and midpoint between them.';
      }
      if (got.bad.length) {
        msg += ' Ignored, because they are not a pair of numbers: ' + got.bad.join(' ') + '.';
      }
      work.innerHTML = blocks.join('');
      status.innerHTML = msg;
      return;
    }

    /* --------------------------------------------- a formula the reader typed */
    var tree = null, err = null;
    if (!body) {
      err = 'nothing to graph yet';
    } else {
      try { tree = Eparse(body); } catch (e) { err = e && e.message; }
    }
    if (tree === null) {
      Plot(svg, { xmin: -span, xmax: span, ymin: -span, ymax: span }).frame();
      titleOut.textContent = 'y = ?';
      subOut.textContent = '';
      kA.innerHTML = '&mdash;'; kB.innerHTML = '&mdash;'; kC.innerHTML = '&mdash;';
      work.innerHTML = '';
      status.innerHTML = '<strong>That formula could not be read: ' + err + '.</strong> '
        + 'Write it the way you would on paper &mdash; <code>2x^3 - 3x + 1</code>, '
        + '<code>sqrt(x - 3)</code>, <code>(x + 1)/(x - 2)</code>. Multiplication can be implicit, '
        + 'powers use <code>^</code>, and every bracket needs its partner.';
      return;
    }

    var poly = Epoly(tree, 'x');
    var fn = function (x) { return evalAt(tree, x, 'x'); };
    var xmin = -span, xmax = span;
    var yw = ywindow(fn, xmin, xmax);
    var plot = Plot(svg, { xmin: xmin, xmax: xmax, ymin: yw.lo, ymax: yw.hi });
    plot.frame();
    plot.curve(fn);
    titleOut.textContent = 'y = ' + body;
    subOut.textContent = poly ? 'a polynomial of degree ' + Pdeg(poly) : 'not a polynomial';

    /* ------------------------------------------------- polynomial mode --- */
    if (MODE === 'polynomial') {
      if (poly === null) {
        kA.innerHTML = '&mdash;'; kB.innerHTML = '&mdash;'; kC.textContent = approx(fn(0), 4);
        blocks.push(table('This is not a polynomial', [
          row('what was typed', body),
          row('why it is not', 'a polynomial is built from x with +, - and * only, and every power '
            + 'must be a whole number that is not negative'),
          row('what still works', 'the curve above is drawn by evaluating your formula, but the exact '
            + 'zero search below needs a polynomial'),
        ]));
        work.innerHTML = blocks.join('');
        status.innerHTML = '<strong>Drawn, but not analysed.</strong> The rational root theorem, '
          + 'multiplicity and end behaviour are all statements about polynomials, and '
          + body + ' is not one. Try <code>x^3 - 3x + 2</code>, or switch to the radical lab '
          + 'for a formula with a root in it.';
        return;
      }
      if (Pzero(poly)) {
        kA.textContent = 'none'; kB.textContent = 'every x'; kC.textContent = '0';
        blocks.push(table('The zero polynomial', [
          row('f(x)', '0, for every x'),
          row('degree', 'undefined: there is no leading term to take the degree of'),
          row('zeros', 'every real number, which is why the zero polynomial is excluded from the '
            + 'factor theorem and from the rational root theorem'),
        ]));
        work.innerHTML = blocks.join('');
        status.innerHTML = '<strong>Every x is a zero of the zero function.</strong> That is not a '
          + 'useful sentence, which is exactly why the theorems about roots all begin "let f be a '
          + 'non-zero polynomial".';
        return;
      }
      var deg = Pdeg(poly), lead = Plead(poly), c0 = Peval(poly, R0);
      var fact = Pfactor(poly);
      var zeros = [];
      fact.factors.forEach(function (item) { zeros.push({ r: item.root, mult: item.mult }); });
      zeros.sort(function (a, b) { return Rcmp(a.r, b.r); });
      var total = 0;
      zeros.forEach(function (z) { total += z.mult; });

      kA.textContent = String(deg);
      kB.textContent = String(zeros.length);
      kC.textContent = Rtext(c0);

      zeros.forEach(function (z) {
        plot.point(Rnum(z.r), 0, 'plot-point root', 'x = ' + Rtext(z.r)
          + (z.mult > 1 ? ' (x' + z.mult + ')' : ''));
      });
      plot.point(0, Rnum(c0), 'plot-point', 'y-int ' + Rtext(c0));
      plot.describe('y = ' + Ptext(poly) + ' with its ' + zeros.length + ' rational zeros marked.');

      var right = Rsign(lead) > 0 ? 'up' : 'down';
      var left = (deg % 2 === 0) === (Rsign(lead) > 0) ? 'up' : 'down';
      blocks.push(table('Read off the polynomial itself', [
        row('f(x)', Ptext(poly)),
        row('degree and leading term', 'degree ' + deg + ', leading coefficient ' + Rtext(lead)),
        row('end behaviour', 'as x -> +inf, f(x) -> ' + (right === 'up' ? '+inf' : '-inf')
          + ';  as x -> -inf, f(x) -> ' + (left === 'up' ? '+inf' : '-inf')
          + '  (degree is ' + (deg % 2 === 0 ? 'even' : 'odd') + ' and the leading coefficient is '
          + (Rsign(lead) > 0 ? 'positive' : 'negative') + ')'),
        row('y-intercept', 'f(0) = ' + Rtext(c0)),
        row('factored over Q', Pfactortextfull(poly)),
      ]));

      /* The claim in the "at the axis" column is then CHECKED by evaluating f
         a little way either side, on a step small enough that no other zero can
         be inside it. Multiplicity predicts the sign change; this measures it. */
      function sidestep(r) {
        var step = R1;
        zeros.forEach(function (other) {
          if (Requ(other.r, r)) return;
          var gap = Rdiv(Rabs(Rsub(other.r, r)), R(2n));
          if (Rcmp(gap, step) < 0) step = gap;
        });
        return step;
      }
      function signtext(v) { return Rsign(v) < 0 ? '-' : (Rsign(v) > 0 ? '+' : '0'); }
      var zrows = zeros.map(function (z) {
        var step = sidestep(z.r);
        var left = Peval(poly, Rsub(z.r, step)), right = Peval(poly, Radd(z.r, step));
        var changed = Rsign(left) * Rsign(right) < 0;
        return '<tr><td>x = ' + Rtext(z.r) + '</td><td>' + z.mult + '</td><td>'
          + (z.mult % 2 === 0 ? 'touches and turns back'
             : (z.mult === 1 ? 'crosses straight through' : 'crosses, flattening as it goes'))
          + '</td><td>' + (Rzero(Peval(poly, z.r)) ? chip('f = 0 exactly', 'ok') : chip('not a zero', 'no'))
          + '</td><td>' + signtext(left) + ' to ' + signtext(right) + ' across a step of '
          + Rtext(step) + ' ' + (changed === (z.mult % 2 === 1) ? chip('as predicted', 'ok')
                                                                : chip('disagrees', 'no'))
          + '</td></tr>';
      });
      if (!zrows.length) {
        zrows.push('<tr><td colspan="5">the rational root search returned nothing</td></tr>');
      }
      blocks.push('<div class="table-wrap"><table class="tt"><caption>Zeros, each one SEARCHED for and '
        + 'then verified by substitution</caption><thead><tr><th>zero</th><th>multiplicity</th>'
        + '<th>at the axis</th><th>f = 0?</th><th>sign either side</th></tr></thead><tbody>'
        + zrows.join('') + '</tbody></table></div>');

      var vrows = [];
      for (var i = -3; i <= 3; i += 1) {
        var xv = R(BigInt(i));
        vrows.push('<tr><td>' + i + '</td><td>' + Rtext(Peval(poly, xv)) + '</td></tr>');
      }
      blocks.push('<div class="table-wrap"><table class="tt"><caption>A table of values, each one an '
        + 'exact evaluation</caption><thead><tr><th>x</th><th>f(x)</th></tr></thead><tbody>'
        + vrows.join('') + '</tbody></table></div>');

      if (!zeros.length) {
        msg = '<strong>No rational zero exists, and the search proves it rather than assuming it.</strong> '
          + 'Every candidate p/q with p dividing ' + Rtext(c0) + ' and q dividing ' + Rtext(lead)
          + ' was substituted, and none gave 0. '
          + (fact.rest.length && Pdeg(fact.rest) === 2 && Rsign(quadroots(fact.rest[2], fact.rest[1], fact.rest[0]).disc) < 0
             ? 'The discriminant of what is left is negative, so this polynomial has no real zero at all &mdash; '
               + 'which is why the curve above never reaches the axis.'
             : 'The curve may still cross the axis at an irrational value; a rational root search says '
               + 'nothing about those.');
      } else {
        var pieces = zeros.map(function (z) {
          return 'x = ' + Rtext(z.r) + (z.mult > 1 ? ' (' + z.mult + ' times)' : '');
        });
        var facText = Pfactortextfull(poly);
        msg = '<strong>' + (facText === Ptext(poly)
            ? Ptext(poly) + ' is already in factored form.'
            : Ptext(poly) + ' = ' + facText + '.') + '</strong> '
          + 'The zeros are ' + pieces.join(', ') + '. '
          + (zeros.some(function (z) { return z.mult % 2 === 0; })
             ? 'A zero of even multiplicity TOUCHES the axis and turns back &mdash; the factor is squared, '
               + 'so the sign of f does not change as x passes it. '
             : 'Each zero here has odd multiplicity, so the graph crosses the axis at every one of them. ')
          + (total < deg
             ? 'Those account for ' + total + ' of the ' + deg + ' roots; the leftover factor '
               + Pfactortext(fact.rest) + ' has no rational root, so the rest are irrational or complex.'
             : 'That is ' + total + ' roots for a degree ' + deg + ' polynomial, so the factorisation is complete.');
      }
      work.innerHTML = blocks.join('');
      status.innerHTML = msg;
      return;
    }

    /* ---------------------------------------------------- radical mode --- */
    var cons = constraintsOf(tree, 'x', []);
    var dom = domainOf(cons);
    var ivs = dom.intervals;
    var roots = [];
    cons.forEach(function (c) {
      if (c.rel !== 'ge' || !c.poly || Pdeg(c.poly) < 1) return;
      Pfactor(c.poly).factors.forEach(function (item) { roots.push(item.root); });
    });

    kA.textContent = domaintext(ivs);
    kB.textContent = dom.boundaries.length
      ? dom.boundaries.map(function (b) { return b.text; }).join(', ') : 'none';
    var atZero = inDomain(ivs, 0) ? valuetext(tree, R0, 'x') : 'undefined: 0 is not in the domain';
    kC.textContent = atZero;

    /* Endpoints: filled when the domain contains them, hollow when it does not.
       That distinction is the entire content of the lesson, so it is drawn. */
    ivs.forEach(function (iv) {
      [[iv.lo, iv.loClosed], [iv.hi, iv.hiClosed]].forEach(function (pair) {
        if (!pair[0]) return;
        var xv = pair[0].val, yv = fn(xv);
        if (pair[1]) {
          if (isFinite(yv)) plot.point(xv, yv, 'plot-point root', 'x = ' + pair[0].text);
          return;
        }
        /* An excluded endpoint is a hollow circle only where the function
           approaches a finite height. Where it runs away instead, a hollow
           circle would be a lie about a value that does not exist, so the
           asymptote is drawn on its own. */
        var near = fn(xv + (yw.hi - yw.lo) * 1e-4 * (inDomain(ivs, xv + 1e-3) ? 1 : -1));
        plot.vline(xv, 'plot-asym', 'x = ' + pair[0].text);
        if (isFinite(near) && near >= yw.lo && near <= yw.hi) plot.hole(xv, near);
      });
    });
    plot.describe('y = ' + body + ', drawn only where it is a real number: ' + domaintext(ivs) + '.');

    var crows = cons.map(function (c) {
      var what = c.why === 'sqrt' ? 'inside a square root'
        : (c.why === 'log' ? 'inside a logarithm'
        : (c.why === 'denominator-root' ? 'a denominator, under the root' : 'a denominator'));
      var demand = c.rel === 'ge' ? ' >= 0' : (c.rel === 'gt' ? ' > 0' : ' != 0');
      return row(what, c.poly ? Ptext(c.poly) + demand : muted('the argument is not a polynomial, so this '
        + 'one was not solved exactly'));
    });
    if (!crows.length) {
      crows.push(row('nothing is forbidden', 'no square root, no division and no logarithm appears, so '
        + 'every real number is allowed in'));
    }
    blocks.push(table('What the formula demands', crows));

    var brows = dom.boundaries.map(function (b) {
      var inside = inDomain(ivs, b.val);
      return '<tr><td>x = ' + b.text + '</td><td>' + (b.r ? 'rational' : 'irrational')
        + '</td><td>' + (inside ? chip('in the domain', 'ok') : chip('excluded', 'no'))
        + '</td><td>' + (!inside ? 'no value here'
            : (b.r ? valuetext(tree, b.r, 'x') : approx(fn(b.val), 5) + ' (rounded)')) + '</td></tr>';
    });
    if (brows.length) {
      blocks.push('<div class="table-wrap"><table class="tt"><caption>The boundaries, solved from the '
        + 'demands above</caption><thead><tr><th>where</th><th>kind</th><th>verdict</th>'
        + '<th>f there</th></tr></thead><tbody>' + brows.join('') + '</tbody></table></div>');
    }

    var vrows2 = [];
    for (var j = -3; j <= 5; j += 1) {
      var xr = R(BigInt(j)), ok = inDomain(ivs, j);
      vrows2.push('<tr><td>' + j + '</td><td>' + (ok ? valuetext(tree, xr, 'x')
        : '<span class="tone-red">not defined</span>') + '</td><td>'
        + (ok ? chip('in', 'ok') : chip('out', 'no')) + '</td></tr>');
    }
    blocks.push('<div class="table-wrap"><table class="tt"><caption>Values, and the x that have '
      + 'none</caption><thead><tr><th>x</th><th>f(x)</th><th>domain</th></tr></thead><tbody>'
      + vrows2.join('') + '</tbody></table></div>');

    var zeroText = [];
    roots.forEach(function (r) {
      if (!inDomain(ivs, Rnum(r))) return;
      var val = Eexact(tree, r, 'x');
      if (val !== null && Rzero(val)) zeroText.push('x = ' + Rtext(r));
    });

    if (!ivs.length) {
      msg = '<strong>No real number satisfies this formula.</strong> The demands above cannot all be '
        + 'met at once, so the domain is empty and there is nothing to draw. That is an answer, not a '
        + 'failure &mdash; sqrt(x - 5) + sqrt(1 - x) is the same shape of problem.';
    } else if (!dom.boundaries.length) {
      msg = '<strong>The domain is ' + domaintext(ivs) + ': every real number.</strong> '
        + 'Nothing in this formula can refuse an input &mdash; a cube root accepts negatives, because '
        + 'a negative number does have a real cube root, and there is no denominator to make zero. '
        + 'The curve above therefore runs from edge to edge with no break in it.';
    } else {
      var irr = dom.boundaries.some(function (b) { return !b.r; });
      msg = '<strong>The domain is ' + domaintext(ivs) + '.</strong> '
        + 'It was found by solving ' + (cons.length === 1 ? 'the demand' : 'the demands')
        + ' above, not by looking at the picture: the boundary search &mdash; rational roots first, '
        + 'then the exact roots of whatever factor was left &mdash; located '
        + (dom.boundaries.length === 1 ? 'the boundary' : 'the boundaries') + ' at '
        + dom.boundaries.map(function (b) { return b.text; }).join(' and ')
        + ', and the demand was then tested exactly on each side. '
        + (irr ? 'Two of those boundaries are irrational and are written as surds, because that is '
                 + 'what they are. ' : '')
        + (ivs.length > 1
           ? 'Notice the GAP: the domain is ' + ivs.length + ' pieces, and the curve stops and starts '
             + 'again. A reader who solves this by taking a square root of both sides and writing '
             + 'x >= ' + ivs[ivs.length - 1].lo.text + ' keeps only the right-hand piece and loses '
             + ivtext(ivs[0]) + ' entirely. '
           : '')
        + (zeroText.length
           ? 'The graph meets the x-axis at ' + zeroText.join(' and ')
             + ', where the radicand is exactly zero. '
           : '')
        + (dom.exact ? 'Every boundary here is exact.'
                     : 'One boundary could not be solved exactly, so it was located numerically and is '
                       + 'shown rounded.');
    }
    work.innerHTML = blocks.join('');
    status.innerHTML = msg;
  }

  preset.addEventListener('change', function () { input.value = preset.value; redraw(); });
  input.addEventListener('input', redraw);
  spanSel.addEventListener('change', redraw);
  input.value = preset.value;
  redraw();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Type a formula, or take one of these"),
        panel_intro=cfg.get("panel_intro", GRAPHER_INTRO[mode]),
        script=script,
    )


# ===========================================================================
#  transform: a*f(b(x - h)) + k over a parent function
# ===========================================================================

# "parent|a|b|h|k". a and b are held on their sliders in HALVES, so a slider
# value of 3 means 3/2 -- which lets a preset ask for a half-size stretch
# without a text box, and keeps every coefficient an exact rational.
TRANSFORM_PRESETS = [
    ("f(x - 3): three to the RIGHT", "sq|2|2|3|0"),
    ("f(x + 3): three to the LEFT", "sq|2|2|-3|0"),
    ("f(2x): halved, not doubled", "sq|2|4|0|0"),
    ("-f(x): flipped over the x-axis", "rt|-2|2|0|0"),
    ("f(-x): flipped over the y-axis", "rt|2|-2|0|0"),
    ("2f(x - 1) - 3: all four at once", "rt|4|2|1|-3"),
]

# One mode, named so that a lesson asking for something else is corrected here
# rather than silently getting this widget under another name.
TRANSFORM_TITLES = {
    "all": ("Transformations of a graph", "a f(b(x - h)) + k, with the parent behind it"),
}

TRANSFORM_PARENTS = [
    ("id", "f(x) = x"),
    ("sq", "f(x) = x^2"),
    ("cu", "f(x) = x^3"),
    ("ab", "f(x) = |x|"),
    ("rt", "f(x) = sqrt(x)"),
    ("rc", "f(x) = 1/x"),
]


def transform_lab(cfg):
    """a*f(b(x - h)) + k, with the parent drawn dashed behind its image.

    The teaching decision. Everybody is told that f(x - 3) moves the graph
    RIGHT and nobody believes it, because the sign says left. Telling them
    again does not work. So this lab shows the same fact three ways at once,
    all computed:

      the picture      the parent is drawn dashed and the image solid, so the
                       direction is visible rather than asserted;
      the point map    a table of points on the parent, each with the exact
                       coordinates of where it lands -- (x0, y0) goes to
                       (x0/b + h, a*y0 + k), and the h is ADDED;
      the check        the drawn curve is then evaluated at that landing x and
                       compared with the predicted y, so the drawing and the
                       arithmetic have to agree in public.

    The reason for the direction is on the page as a sentence about inputs
    rather than about pictures: the image cannot produce y0 until the bracket
    inside f becomes x0, and with h subtracted inside, that needs an x that is
    h LARGER. Every other rule on the page (b squeezes rather than stretches,
    a and k do exactly what they say because they act after f) is stated the
    same way, and each is recomputed for the numbers the reader chose.

    Two degenerate settings are deliberately reachable on the sliders: b = 0
    collapses every input to one, and a = 0 flattens the image to y = k. Both
    are explained instead of drawn as an empty panel -- and for the 1/x parent,
    b = 0 makes the domain empty, which is the sharpest possible illustration
    of what the inside of a function does.
    """
    mode = cfg.get("mode", "all")
    if mode not in TRANSFORM_TITLES:
        mode = "all"
    title, subtitle = TRANSFORM_TITLES[mode]
    presets = cfg.get("presets") or TRANSFORM_PRESETS

    options = "".join('<option value="%s">%s</option>' % (value, label) for label, value in presets)
    parent_options = "".join('<option value="%s">%s</option>' % (key, label)
                             for key, label in TRANSFORM_PARENTS)

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="tfTitle">y = a f(b(x - h)) + k</strong><span id="tfSub"></span></div>
        <div class="inline-legend"><span class="tone-muted"><i class="legend-swatch"></i>parent, dashed</span><span class="tone-cyan"><i class="legend-swatch"></i>image</span><span class="tone-amber"><i class="legend-swatch"></i>a tracked point</span><span class="tone-purple"><i class="legend-swatch"></i>where it lands</span></div>
      </div>
      <div class="lab-stage"><svg id="tfPlot"></svg></div>
      <div id="tfWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="tfStatus" style="margin-top:12px;"></div>"""

    controls = ('        <div class="field">\n'
                '          <label for="tfPreset">Example</label>\n'
                '          <select id="tfPreset">' + options + '</select>\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <label for="tfParent">Parent function</label>\n'
                '          <select id="tfParent">' + parent_options + '</select>\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <div class="range-row"><label class="small-copy" for="tfA">a &mdash; vertical stretch</label><span class="range-value" id="tfAOut">1</span></div>\n'
                '          <input id="tfA" type="range" min="-8" max="8" value="2">\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <div class="range-row"><label class="small-copy" for="tfB">b &mdash; horizontal squeeze</label><span class="range-value" id="tfBOut">1</span></div>\n'
                '          <input id="tfB" type="range" min="-8" max="8" value="2">\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <div class="range-row"><label class="small-copy" for="tfH">h &mdash; inside the bracket</label><span class="range-value" id="tfHOut">0</span></div>\n'
                '          <input id="tfH" type="range" min="-6" max="6" value="0">\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <div class="range-row"><label class="small-copy" for="tfK">k &mdash; added at the end</label><span class="range-value" id="tfKOut">0</span></div>\n'
                '          <input id="tfK" type="range" min="-6" max="6" value="0">\n'
                '        </div>\n'
                '        <div class="kpi-grid">\n'
                '          <div class="kpi"><span>Horizontal</span><strong id="tfKa">&mdash;</strong></div>\n'
                '          <div class="kpi"><span>Vertical</span><strong id="tfKb">&mdash;</strong></div>\n'
                '          <div class="kpi"><span>Image domain</span><strong id="tfKc">&mdash;</strong></div>\n'
                '        </div>\n'
                '        <p class="small-copy" id="tfHint" style="margin:0;">a and b move in halves, so '
                '<code>1/2</code> and <code>3/2</code> are reachable. Every coordinate below is an exact '
                'fraction computed from these four numbers.</p>\n')

    script = BASE_JS + SHARED_JS + r"""
  var preset = document.getElementById('tfPreset');
  var parentSel = document.getElementById('tfParent');
  var inA = document.getElementById('tfA'), inB = document.getElementById('tfB');
  var inH = document.getElementById('tfH'), inK = document.getElementById('tfK');
  var outA = document.getElementById('tfAOut'), outB = document.getElementById('tfBOut');
  var outH = document.getElementById('tfHOut'), outK = document.getElementById('tfKOut');
  var work = document.getElementById('tfWork'), status = document.getElementById('tfStatus');
  var titleOut = document.getElementById('tfTitle'), subOut = document.getElementById('tfSub');
  var kA = document.getElementById('tfKa'), kB = document.getElementById('tfKb'), kC = document.getElementById('tfKc');
  var svg = document.getElementById('tfPlot');

  /* Each parent knows three things about itself: how to be drawn, how to be
     evaluated EXACTLY at a rational (so the point table is fractions and not
     decimals), and what it refuses. Nothing else in the lab is parent-specific,
     which is the point -- the transformation rules do not depend on f. */
  function sample(list) { return list.map(function (pair) { return R(BigInt(pair[0]), BigInt(pair[1])); }); }
  var PARENTS = {
    id: { name: 'x', fn: function (t) { return t; }, poly: [R0, R1],
          exact: function (r) { return r; }, restrict: null,
          xs: sample([[-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1]]) },
    sq: { name: 'x^2', fn: function (t) { return t * t; }, poly: [R0, R0, R1],
          exact: function (r) { return Rmul(r, r); }, restrict: null,
          xs: sample([[-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1]]) },
    cu: { name: 'x^3', fn: function (t) { return t * t * t; }, poly: [R0, R0, R0, R1],
          exact: function (r) { return Rmul(r, Rmul(r, r)); }, restrict: null,
          xs: sample([[-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1]]) },
    ab: { name: '|x|', fn: function (t) { return Math.abs(t); }, poly: null,
          exact: function (r) { return Rabs(r); }, restrict: null,
          xs: sample([[-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1]]) },
    rt: { name: 'sqrt(x)', fn: function (t) { return t < 0 ? NaN : Math.sqrt(t); }, poly: null,
          exact: function (r) { return Rsign(r) < 0 ? null : Rsqrt(r); }, restrict: 'ge0',
          xs: sample([[0, 1], [1, 1], [4, 1], [9, 1]]) },
    rc: { name: '1/x', fn: function (t) { return t === 0 ? NaN : 1 / t; }, poly: null,
          exact: function (r) { return Rzero(r) ? null : Rinv(r); }, restrict: 'ne0',
          xs: sample([[-2, 1], [-1, 1], [1, 2], [1, 1], [2, 1]]) }
  };

  function halves(el) { return R(BigInt(parseInt(el.value, 10) || 0), 2n); }
  function whole(el) { return R(BigInt(parseInt(el.value, 10) || 0)); }

  function redraw() {
    var P = PARENTS[parentSel.value] || PARENTS.sq;
    var a = halves(inA), b = halves(inB), h = whole(inH), k = whole(inK);
    outA.textContent = Rtext(a); outB.textContent = Rtext(b);
    outH.textContent = Rtext(h); outK.textContent = Rtext(k);

    var av = Rnum(a), bv = Rnum(b), hv = Rnum(h), kv = Rnum(k);
    var parentFn = P.fn;
    var imageFn = function (x) {
      var t = bv * (x - hv);
      var y = parentFn(t);
      return (typeof y === 'number' && isFinite(y)) ? av * y + kv : NaN;
    };

    /* The formula, written with the reader's own numbers in it. */
    var inside = Rzero(h) ? 'x' : '(' + shifttext(h, 'x') + ')';
    var arg = Rzero(b) ? '0'
            : (Requ(b, R1) ? (Rzero(h) ? 'x' : shifttext(h, 'x')) : coeftext(b) + inside);
    var formula = 'y = ' + (Requ(a, R1) ? '' : (Requ(a, R(-1n)) ? '-' : Rterm(a)))
      + 'f(' + arg + ')' + (Rzero(k) ? '' : (Rsign(k) > 0 ? ' + ' + Rtext(k) : ' - ' + Rtext(Rabs(k))));
    titleOut.textContent = formula;
    subOut.textContent = 'parent f(x) = ' + P.name + ',  a = ' + Rtext(a) + ', b = ' + Rtext(b)
      + ', h = ' + Rtext(h) + ', k = ' + Rtext(k);

    /* ---- the picture: parent behind, image in front ---- */
    var xlo = Math.min(-5, hv - 5) - 1, xhi = Math.max(5, hv + 5) + 1;
    var vals = [], i;
    for (i = 0; i <= 200; i += 1) {
      var xx = xlo + (xhi - xlo) * i / 200;
      [parentFn(xx), imageFn(xx)].forEach(function (y) {
        if (typeof y === 'number' && isFinite(y)) vals.push(y);
      });
    }
    var ylo = -6, yhi = 6;
    if (vals.length) {
      vals.sort(function (p, q) { return p - q; });
      ylo = Math.min(0, vals[Math.floor(vals.length * 0.03)]);
      yhi = Math.max(0, vals[Math.floor((vals.length - 1) * 0.97)]);
      if (yhi - ylo < 6) { var c = (yhi + ylo) / 2; ylo = c - 3; yhi = c + 3; }
    }
    var plot = Plot(svg, { xmin: xlo, xmax: xhi, ymin: ylo - 1, ymax: yhi + 1 });
    plot.frame();
    plot.curve(parentFn, 'plot-curve parent');
    plot.curve(imageFn, 'plot-curve');

    /* ---- where every sample point lands ---- */
    var moved = [], degenerate = Rzero(b);
    P.xs.forEach(function (x0) {
      var y0 = P.exact(x0);
      if (y0 === null) return;
      var x1 = degenerate ? null : Radd(Rdiv(x0, b), h);
      var y1 = Radd(Rmul(a, y0), k);
      moved.push({ x0: x0, y0: y0, x1: x1, y1: y1 });
    });
    var tracked = moved.length ? moved[Math.min(1, moved.length - 1)] : null;
    if (tracked) {
      plot.point(Rnum(tracked.x0), Rnum(tracked.y0), 'plot-point',
        '(' + Rtext(tracked.x0) + ', ' + Rtext(tracked.y0) + ')');
      if (tracked.x1 !== null) {
        plot.point(Rnum(tracked.x1), Rnum(tracked.y1), 'plot-point vertex',
          '(' + Rtext(tracked.x1) + ', ' + Rtext(tracked.y1) + ')');
        plot.segment(Rnum(tracked.x0), Rnum(tracked.y0), Rnum(tracked.x1), Rnum(tracked.y1), 'plot-aux');
      }
    }
    plot.describe('The parent f(x) = ' + P.name + ' dashed, and ' + formula + ' solid, both drawn by '
      + 'evaluating them across the window.');

    /* ---- the image domain, derived from b and h ---- */
    var domText;
    if (P.restrict === 'ge0') {
      domText = Rzero(b) ? '(-inf, inf), because b = 0 makes the inside 0 for every x'
        : (Rsign(b) > 0 ? '[' + Rtext(h) + ', inf)' : '(-inf, ' + Rtext(h) + ']');
    } else if (P.restrict === 'ne0') {
      domText = Rzero(b) ? 'empty: b = 0 sends every x to 0, and 1/0 is not a number'
        : 'every x except ' + Rtext(h);
    } else {
      domText = '(-inf, inf)';
    }

    kA.textContent = Rzero(b) ? 'collapsed'
      : (Rzero(h) ? 'no shift' : (Rsign(h) > 0 ? Rtext(h) + ' right' : Rtext(Rabs(h)) + ' left'));
    kB.textContent = Rzero(k) ? 'no shift'
      : (Rsign(k) > 0 ? Rtext(k) + ' up' : Rtext(Rabs(k)) + ' down');
    kC.textContent = domText;

    var blocks = [];

    /* ---- what each of the four numbers did ---- */
    function hdesc() {
      if (Rzero(h)) return 'h = 0: no horizontal shift';
      return 'h = ' + Rtext(h) + ': the graph moves ' + Rtext(Rabs(h)) + ' to the '
        + (Rsign(h) > 0 ? 'RIGHT' : 'LEFT') + ', the '
        + (Rsign(h) > 0 ? 'opposite' : 'same') + ' direction to the sign inside the bracket';
    }
    function bdesc() {
      if (Rzero(b)) return 'b = 0: every x is sent to the same input, so the image is one value repeated';
      var mag = Rabs(b), out = 'b = ' + Rtext(b) + ': horizontal distances are multiplied by '
        + Rtext(Rinv(mag)) + ', so the graph ';
      out += Rcmp(mag, R1) > 0 ? 'is SQUEEZED toward the vertical line x = ' + Rtext(h)
           : (Requ(mag, R1) ? 'keeps its width' : 'is stretched away from x = ' + Rtext(h));
      if (Rsign(b) < 0) out += ', and reflected in the vertical line x = ' + Rtext(h);
      return out;
    }
    function adesc() {
      if (Rzero(a)) return 'a = 0: every output is multiplied by 0, so the image is the line y = ' + Rtext(k);
      var mag = Rabs(a), out = 'a = ' + Rtext(a) + ': every output is multiplied by ' + Rtext(a) + ', so heights ';
      out += Rcmp(mag, R1) > 0 ? 'grow by a factor of ' + Rtext(mag)
           : (Requ(mag, R1) ? 'keep their size' : 'shrink by a factor of ' + Rtext(mag));
      if (Rsign(a) < 0) out += ', and the graph is flipped over the horizontal line y = ' + Rtext(k);
      return out;
    }
    blocks.push(table('The four numbers, and what each one did here', [
      row('inside: b', bdesc()),
      row('inside: h', hdesc()),
      row('outside: a', adesc()),
      row('outside: k', Rzero(k) ? 'k = 0: no vertical shift'
        : 'k = ' + Rtext(k) + ': every output has ' + Rtext(k) + ' added, so the graph moves '
          + Rtext(Rabs(k)) + ' ' + (Rsign(k) > 0 ? 'UP' : 'DOWN') + ', the same direction as the sign'),
      row('domain of the image', domText),
    ]));

    /* ---- the point map, checked against the drawn curve ---- */
    /* "9/(-1) - 3", not "9/-1 + -3": the arithmetic is the same and only one
       of them is what a reader is asked to produce. */
    function mapx(m) {
      var t = Requ(b, R1) ? Rtext(m.x0) : Rtext(m.x0) + '/' + Rterm(b);
      if (!Rzero(h)) t += Rsign(h) > 0 ? ' + ' + Rtext(h) : ' - ' + Rtext(Rabs(h));
      return t + ' = ' + Rtext(m.x1);
    }
    function mapy(m) {
      var t = Requ(a, R1) ? Rtext(m.y0) : Rterm(a) + '(' + Rtext(m.y0) + ')';
      if (!Rzero(k)) t += Rsign(k) > 0 ? ' + ' + Rtext(k) : ' - ' + Rtext(Rabs(k));
      return t + ' = ' + Rtext(m.y1);
    }
    var prows = moved.map(function (m) {
      if (m.x1 === null) {
        return '<tr><td>(' + Rtext(m.x0) + ', ' + Rtext(m.y0) + ')</td><td>&mdash;</td>'
          + '<td>' + Rtext(m.y1) + '</td><td>' + muted('no landing x: b = 0') + '</td></tr>';
      }
      var drawn = imageFn(Rnum(m.x1)), want = Rnum(m.y1);
      var agrees = isFinite(drawn) && Math.abs(drawn - want) < 1e-9;
      return '<tr><td>(' + Rtext(m.x0) + ', ' + Rtext(m.y0) + ')</td>'
        + '<td>' + mapx(m) + '</td>'
        + '<td>' + mapy(m) + '</td>'
        + '<td>' + (agrees ? chip('on the curve', 'ok') : chip('off the curve', 'no')) + '</td></tr>';
    });
    if (!prows.length) prows.push('<tr><td colspan="4">this parent has no value at the sample points</td></tr>');
    blocks.push('<div class="table-wrap"><table class="tt"><caption>Every sample point of the parent, and '
      + 'where it lands &mdash; then the drawn image is evaluated there to check'
      + '</caption><thead><tr><th>on the parent</th><th>new x</th><th>new y</th><th>check</th></tr></thead>'
      + '<tbody>' + prows.join('') + '</tbody></table></div>');

    /* ---- and, where the parent is a polynomial, the image multiplied out ---- */
    if (P.poly) {
      var g = [Rneg(Rmul(b, h)), b];                 /* b(x - h) = bx - bh */
      var composed = Pcompose(P.poly, g);
      var expanded = Padd(Pscale(composed, a), [k]);
      blocks.push(table('The image as one polynomial, multiplied out exactly', [
        row('inside the bracket', 'b(x - h) = ' + Ptext(g)),
        row('f of that', P.name.replace(/x/g, '(' + Ptext(g) + ')') + ' = ' + Ptext(composed)),
        row('times a, plus k', Rterm(a) + '(' + Ptext(composed) + ')'
          + (Rzero(k) ? '' : ' + ' + Rterm(k)) + ' = ' + Ptext(expanded)),
        row('check at x = ' + Rtext(Radd(h, R1)),
          'the expansion gives ' + Rtext(Peval(expanded, Radd(h, R1)))
          + ' and the drawn curve gives ' + approx(imageFn(hv + 1), 6) + ' '
          + (Math.abs(Rnum(Peval(expanded, Radd(h, R1))) - imageFn(hv + 1)) < 1e-9
             ? chip('agree', 'ok') : chip('disagree', 'no'))),
      ]));
    }

    work.innerHTML = blocks.join('');

    /* ---- the sentence the lesson exists for ---- */
    var msg;
    if (Rzero(b)) {
      msg = '<strong>b = 0 destroys the function.</strong> Every x is multiplied by 0 before f sees it, '
        + 'so f is only ever asked about one input. '
        + (P.restrict === 'ne0'
           ? 'For 1/x that input is 0, which has no reciprocal &mdash; so the image has an EMPTY domain '
             + 'and there is nothing at all to draw.'
           : 'The image is the horizontal line y = ' + Rtext(Radd(Rmul(a, P.exact(R0) === null ? R0 : P.exact(R0)), k))
             + ', because a f(0) + k is the same number for every x.')
        + ' A transformation with b = 0 is not a transformation; it is a collapse.';
    } else if (Rzero(a)) {
      msg = '<strong>a = 0 flattens everything to y = ' + Rtext(k) + '.</strong> The parent is evaluated, '
        + 'and then multiplied by zero. Whatever f did is gone, and the inside numbers b and h have '
        + 'nothing left to act on &mdash; which is a good way to see that a and k act AFTER f, on its '
        + 'output, while b and h act BEFORE it, on its input.';
    } else if (!Rzero(h)) {
      var x0 = tracked ? tracked.x0 : R0, y0 = tracked ? tracked.y0 : R0;
      var x1 = tracked ? tracked.x1 : h;
      msg = '<strong>' + shifttext(h, 'x') + ' inside the bracket moves the graph '
        + Rtext(Rabs(h)) + ' to the ' + (Rsign(h) > 0 ? 'RIGHT' : 'LEFT') + '.</strong> '
        + 'Here is the reason, in the numbers above: the parent takes the value ' + Rtext(y0)
        + ' at x = ' + Rtext(x0) + '. The image can only produce that value once the bracket inside f '
        + 'becomes ' + Rtext(x0) + ', and with h = ' + Rtext(h) + ' subtracted inside, that needs '
        + 'x = ' + Rtext(x1) + '. The output is unchanged; the x that produces it has '
        + (Rsign(h) > 0 ? 'grown' : 'shrunk') + '. A minus sign inside means "this function is running '
        + Rtext(Rabs(h)) + ' behind", and a function that is running behind appears further along.';
    } else if (Requ(Rabs(b), R1) && Rsign(b) < 0) {
      var far = P.xs[P.xs.length - 1];
      msg = '<strong>f(-x) reflects the graph in the y-axis.</strong> Nothing is stretched: every '
        + 'input is negated before f sees it, so the point at x = ' + Rtext(far)
        + ' moves to x = ' + Rtext(Rneg(far)) + ' and keeps its height. '
        + (P.restrict
           ? 'This parent only accepts some inputs, so the reflection takes its whole domain to the '
             + 'other side: the image is defined on ' + domText + '. That is the clearest way to see '
             + 'that b acts on the input rather than on the picture.'
           : 'For a parent that is symmetric about the y-axis this changes nothing at all &mdash; '
             + 'f(-x) = f(x) is exactly what "even function" means.');
    } else if (!Requ(b, R1)) {
      var far2 = P.xs[P.xs.length - 1];
      msg = '<strong>b = ' + Rtext(b) + ' scales the x-axis by ' + Rtext(Rinv(Rabs(b))) + ', not by '
        + Rtext(Rabs(b)) + '.</strong> A point that sat at x = ' + Rtext(far2)
        + ' on the parent is now at x = ' + Rtext(Rdiv(far2, b))
        + ', because the bracket has to reach ' + Rtext(far2) + ' and with b = ' + Rtext(b)
        + ' it gets there ' + Rtext(Rabs(b)) + ' times faster. So the image is '
        + Rtext(Rinv(Rabs(b))) + ' times as wide as the parent, which is the opposite of what '
        + Rtext(Rabs(b)) + ' suggests.'
        + (Rsign(b) < 0 ? ' The negative sign also reflects it in the y-axis.' : '');
    } else if (Rsign(a) < 0) {
      msg = '<strong>The minus sign in front of f flips the graph over the line y = ' + Rtext(k)
        + '.</strong> Every output is computed first and then multiplied by ' + Rtext(a)
        + ', so a point that was ' + Rtext(Rabs(P.exact(P.xs[P.xs.length - 1]) === null ? R1 : P.exact(P.xs[P.xs.length - 1])))
        + ' above the axis is now that far below it. Compare this with f(-x), which negates the INPUT '
        + 'and reflects sideways instead: -f(x) and f(-x) are different functions.';
    } else if (!Requ(a, R1) && !Rzero(k)) {
      msg = '<strong>a and k act on the OUTPUT, in that order.</strong> Every height is multiplied by '
        + Rtext(a) + ' first and only then is ' + Rtext(k) + ' added &mdash; which is why '
        + Rterm(a) + 'f(x) + ' + Rtext(k) + ' is not the same function as '
        + Rterm(a) + '(f(x) + ' + Rtext(k) + '); the second one would multiply the shift by '
        + Rtext(a) + ' as well. The inside numbers are the ones that behave backwards; these two do '
        + 'exactly what they say.';
    } else if (!Requ(a, R1)) {
      msg = '<strong>a = ' + Rtext(a) + ' multiplies every height by ' + Rtext(a) + '.</strong> '
        + 'The x-coordinates are untouched, so the graph is pulled '
        + (Rcmp(Rabs(a), R1) > 0 ? 'away from' : 'towards') + ' the x-axis and every zero stays '
        + 'exactly where it was &mdash; a vertical stretch cannot move a point that is already at '
        + 'height 0.';
    } else if (!Rzero(k)) {
      msg = '<strong>k = ' + Rtext(k) + ' moves the whole graph ' + Rtext(Rabs(k)) + ' '
        + (Rsign(k) > 0 ? 'up' : 'down') + '.</strong> It is added after f has finished, so it does '
        + 'exactly what its sign says &mdash; unlike h, which sits inside the bracket and appears to '
        + 'do the opposite. Every point moves the same distance vertically and none of them moves '
        + 'sideways.';
    } else {
      msg = '<strong>a = 1, b = 1, h = 0, k = 0: the image IS the parent.</strong> The solid curve sits '
        + 'exactly on the dashed one. Move any slider and watch which way the graph goes &mdash; the two '
        + 'inside numbers (b and h) will surprise you, and the two outside ones will not.';
    }
    status.innerHTML = msg;
  }

  preset.addEventListener('change', function () {
    var parts = preset.value.split('|');
    parentSel.value = parts[0];
    inA.value = parts[1]; inB.value = parts[2]; inH.value = parts[3]; inK.value = parts[4];
    redraw();
  });
  parentSel.addEventListener('change', redraw);
  [inA, inB, inH, inK].forEach(function (el) {
    el.addEventListener('input', redraw);
    el.addEventListener('change', redraw);
  });
  var first = preset.value.split('|');
  parentSel.value = first[0];
  inA.value = first[1]; inB.value = first[2]; inH.value = first[3]; inK.value = first[4];
  redraw();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a parent and move the four numbers"),
        panel_intro=cfg.get(
            "panel_intro",
            "The dashed curve is the parent and the solid one is the image. Change h and watch "
            "which way it goes; the table below says where every point lands and then checks the "
            "drawn curve against it.",
        ),
        script=script,
    )


# ===========================================================================
#  funcops: what a function IS, and everything you can do to one
# ===========================================================================

FUNCOPS_PRESETS = {
    "definition": [
        ("(1, 2) (2, 4) (3, 6)", "(1, 2) (2, 4) (3, 6)"),
        ("(1, 2) (2, 4) (1, 5): x = 1 twice", "(1, 2) (2, 4) (1, 5)"),
        ("(1, 3) (2, 3) (5, 3): one y, three times", "(1, 3) (2, 3) (5, 3)"),
        ("(2, -3) (2, 0) (2, 4): a vertical line", "(2, -3) (2, 0) (2, 4)"),
        ("x = y^2 - 1: the sideways parabola", "x = y^2 - 1"),
        ("x = y^3: sideways, but still a function", "x = y^3"),
    ],
    "notation": [
        ("f(x) = 2x^2 - 5x + 1", "2x^2 - 5x + 1"),
        ("f(x) = 3x - 7", "3x - 7"),
        ("f(x) = x^2", "x^2"),
        ("f(x) = x^3 - x", "x^3 - x"),
        ("f(x) = 1/x", "1/x"),
        ("f(x) = sqrt(x)", "sqrt(x)"),
    ],
    "domain": [
        ("1/(x - 2)", "1/(x - 2)"),
        ("(x + 1)/(x^2 - 4)", "(x + 1)/(x^2 - 4)"),
        ("(x^2 - 4)/(x - 2): a hole, not an asymptote", "(x^2 - 4)/(x - 2)"),
        ("sqrt(x - 3)", "sqrt(x - 3)"),
        ("x^2 - 4x + 1", "x^2 - 4x + 1"),
        ("1/(x^2 + 1)", "1/(x^2 + 1)"),
    ],
    "piecewise": [
        ("a join that meets", "x^2 on (-inf, 1); 2x - 1 on [1, inf)"),
        ("a jump of 3", "x + 1 on (-inf, 0); x - 2 on [0, inf)"),
        ("|x|, written out", "-x on (-inf, 0); x on [0, inf)"),
        ("three pieces", "x^2 on (-inf, -1]; x on (-1, 1); 2 on [1, inf)"),
        ("a gap: nothing on [0, 1]", "x^2 on (-inf, 0); 2 on (1, inf)"),
        ("an overlap: two values at x = 2", "x on (-inf, 2]; 5 - x on [2, inf)"),
    ],
    "compose": [
        ("f = 2x, g = x^2", "2x|x^2"),
        ("f = x + 1, g = x + 2: these commute", "x + 1|x + 2"),
        ("f = x^2, g = x - 3", "x^2|x - 3"),
        ("f = sqrt(x), g = x - 4", "sqrt(x)|x - 4"),
        ("f = 1/x, g = x - 2", "1/x|x - 2"),
        ("f = x^2 + 1, g = sqrt(x)", "x^2 + 1|sqrt(x)"),
    ],
    "inverse": [
        ("f(x) = 2x + 3", "2x + 3"),
        ("f(x) = x^2: needs a restriction", "x^2"),
        ("f(x) = x^2 - 4x + 1", "x^2 - 4x + 1"),
        ("f(x) = x^3", "x^3"),
        ("f(x) = 1/x: its own inverse", "1/x"),
        ("f(x) = 3: no inverse at all", "3"),
    ],
}

FUNCOPS_TITLES = {
    "definition": ("Is it a function?", "The vertical line test, drawn where it fails"),
    "notation": ("f(x) as a machine", "One input in, one output out, substituted in full"),
    "domain": ("Domain and range", "What the formula forbids, and what it can produce"),
    "piecewise": ("Piecewise definitions", "Open and closed endpoints, and the joins between pieces"),
    "compose": ("Composition, both ways round", "f(g(x)) and g(f(x)), computed separately"),
    "inverse": ("Inverses", "Reflect in y = x, and say which half you kept"),
}

FUNCOPS_KPIS = {
    "definition": ("A function?", "One-to-one?", "Witness"),
    "notation": ("f(a)", "f(x + 1)", "f(x) + 1"),
    "domain": ("Domain", "Excluded", "Range"),
    "piecewise": ("Pieces", "Domain", "At the joins"),
    "compose": ("f(g(x))", "g(f(x))", "Equal?"),
    "inverse": ("One-to-one?", "Inverse", "Restriction"),
}

FUNCOPS_MAIN_LABEL = {
    "definition": "A relation: points, or x = ...",
    "notation": "f(x) =",
    "domain": "f(x) =",
    "piecewise": "Pieces: expression on interval; ...",
    "compose": "f(x) =",
    "inverse": "f(x) =",
}

FUNCOPS_HINTS = {
    "definition": "Either a list of points such as <code>(1, 2) (2, 4)</code>, or a relation solved "
                  "for x, such as <code>x = y^2 - 1</code>.",
    "notation": "Type a formula in x. The substitution below is written out in full before it is "
                "evaluated, because that is where the mistakes happen.",
    "domain": "Type a formula. The exclusions come from its denominators and roots, and a hole is "
              "told apart from an asymptote by cancelling.",
    "piecewise": "Each piece is <code>expression on interval</code>, separated by semicolons. "
                 "Intervals use <code>[</code> for included and <code>(</code> for excluded, with "
                 "<code>-inf</code> and <code>inf</code> allowed.",
    "compose": "Two formulas. Both compositions are worked out, and the lab checks whether they "
               "are the same function rather than assuming they are not.",
    "inverse": "Type a formula. If it is not one-to-one the lab finds two inputs that collide and "
               "states the restriction that fixes it.",
}

FUNCOPS_INTRO = {
    "definition": "One input, one output. Type a relation and the lab looks for an x with two "
                  "different y &mdash; and draws the vertical line through them when it finds one.",
    "notation": "f(3) means substitute 3 for every x. The lab writes the substitution out before "
                "evaluating it, and computes f(x + 1) and f(x) + 1 side by side.",
    "domain": "The domain is what the formula allows and the range is what it can produce. Both are "
              "derived here; where the range cannot be proved the lab says it sampled.",
    "piecewise": "Each piece is drawn only on its own interval, with a filled dot where the endpoint "
                 "belongs to the piece and a hollow one where it does not.",
    "compose": "f(g(x)) means do g first. Both orders are computed and compared, and the domain of "
               "the composite is worked out from the composite formula.",
    "inverse": "An inverse undoes f, and it exists only when no two inputs share an output. The "
               "reflection in y = x is drawn whether or not a formula can be written down.",
}


def funcops_lab(cfg):
    """A function: the definition, the notation, and the four things done to one.

    The teaching decision. These six modes are one lab because they are one
    idea seen from six sides, and each mode is built around the moment the idea
    is usually mis-stated:

      definition  a relation fails to be a function at a SPECIFIC x, so the lab
                  finds that x and draws the vertical line through the two
                  points on it. "Same y twice" is offered as a preset because
                  it is legal and everybody thinks it is not.
      notation    f(x + 1) and f(x) + 1 are computed side by side, exactly.
                  They differ, and the reader can see by how much.
      domain      a hole and an asymptote are told apart by CANCELLING: the
                  common factor of numerator and denominator is found, and the
                  excluded x is still excluded afterwards.
      piecewise   endpoints are filled or hollow, an overlap makes the
                  definition fail to be a function at all, and a gap leaves an
                  interval undefined. Both failures are presets.
      compose     both orders, every time, plus the preset where they DO agree,
                  because "composition is not commutative" is a statement about
                  all pairs and not about every pair.
      inverse     the reflection in y = x is drawn from the sampled graph, so
                  it exists even when no formula can be written; the formula,
                  where one can be derived, is drawn on top of it and checked
                  by substitution.

    Where a fact cannot be proved by the machinery here -- that a sampled range
    really is the range, that a function with no rational witness really is
    one-to-one -- the lab says which it is doing. An unlabelled sample would be
    the page claiming a proof it does not have.
    """
    mode = cfg.get("mode", "definition")
    if mode not in FUNCOPS_PRESETS:
        mode = "definition"
    presets = cfg.get("presets") or FUNCOPS_PRESETS[mode]
    title, subtitle = FUNCOPS_TITLES[mode]
    ka, kb, kc = FUNCOPS_KPIS[mode]

    options = "".join('<option value="%s">%s</option>' % (value, label) for label, value in presets)

    aux_field = ""
    if mode == "compose":
        aux_field = ('        <div class="field">\n'
                     '          <label for="foAux">g(x) =</label>\n'
                     '          <input id="foAux" type="text" value="" autocomplete="off" spellcheck="false">\n'
                     '        </div>\n')
    at_field = ""
    if mode == "notation":
        at_values = ["-3", "-2", "-1", "-1/2", "0", "1/2", "1", "2", "3", "4"]
        at_options = "".join('<option value="%s">a = %s</option>' % (v, v) for v in at_values)
        at_field = ('        <div class="field">\n'
                    '          <label for="foAt">Evaluate at</label>\n'
                    '          <select id="foAt">' + at_options + '</select>\n'
                    '        </div>\n')

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="foTitle">A function</strong><span id="foSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>f</span><span class="tone-purple"><i class="legend-swatch"></i>the second curve</span><span class="tone-muted"><i class="legend-swatch"></i>dashed: y = x, or a discarded half</span><span class="tone-red"><i class="legend-swatch"></i>where it fails</span></div>
      </div>
      <div class="lab-stage"><svg id="foPlot"></svg></div>
      <div id="foWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="foStatus" style="margin-top:12px;"></div>"""

    controls = ('        <div class="field">\n'
                '          <label for="foPreset">Example</label>\n'
                '          <select id="foPreset">' + options + '</select>\n'
                '        </div>\n'
                '        <div class="field">\n'
                '          <label for="foMain">' + FUNCOPS_MAIN_LABEL[mode] + '</label>\n'
                '          <input id="foMain" type="text" value="" autocomplete="off" spellcheck="false">\n'
                '        </div>\n'
                + aux_field + at_field
                + '        <div class="kpi-grid">\n'
                  '          <div class="kpi"><span>' + ka + '</span><strong id="foKa">&mdash;</strong></div>\n'
                  '          <div class="kpi"><span>' + kb + '</span><strong id="foKb">&mdash;</strong></div>\n'
                  '          <div class="kpi"><span>' + kc + '</span><strong id="foKc">&mdash;</strong></div>\n'
                  '        </div>\n'
                  '        <p class="small-copy" id="foHint" style="margin:0;">' + FUNCOPS_HINTS[mode] + '</p>\n')

    reads = ""
    if mode == "compose":
        reads += "  inAux = document.getElementById('foAux');\n"
    if mode == "notation":
        reads += "  selAt = document.getElementById('foAt');\n"

    binds = ""
    if mode == "compose":
        binds += "  inAux.addEventListener('input', redraw);\n"
    if mode == "notation":
        binds += "  selAt.addEventListener('change', redraw);\n"

    script = BASE_JS + SHARED_JS + r"""
  var MODE = '""" + mode + r"""';
  var preset = document.getElementById('foPreset');
  var inMain = document.getElementById('foMain');
  var work = document.getElementById('foWork'), status = document.getElementById('foStatus');
  var titleOut = document.getElementById('foTitle'), subOut = document.getElementById('foSub');
  var kA = document.getElementById('foKa'), kB = document.getElementById('foKb'), kC = document.getElementById('foKc');
  var svg = document.getElementById('foPlot');
  var inAux = null, selAt = null;
""" + reads + r"""

  function ptext(p) { return '(' + Rtext(p.x) + ', ' + Rtext(p.y) + ')'; }
  function frame(half) {
    var h = half || 6;
    return Plot(svg, { xmin: -h, xmax: h, ymin: -h, ymax: h }).frame();
  }
  function parse(src) {
    try { return { tree: Eparse(src), err: null }; }
    catch (e) { return { tree: null, err: (e && e.message) || 'it could not be read' }; }
  }
  function blank(message) {
    frame(6);
    work.innerHTML = '';
    kA.innerHTML = '&mdash;'; kB.innerHTML = '&mdash;'; kC.innerHTML = '&mdash;';
    status.innerHTML = message;
  }

  /* ---------------------------------------------------------- definition */
  function runDefinition(raw) {
    var body = raw.replace(/^\s*x\s*=/, '').trim();
    var isCurve = /^\s*x\s*=/.test(raw);
    var blocks = [];
    if (isCurve) {
      var got = parse(body);
      if (!got.tree) {
        blank('<strong>That relation could not be read: ' + got.err + '.</strong> Write it solved for '
          + 'x, as in <code>x = y^2 - 1</code>, or give a list of points such as '
          + '<code>(1, 2) (2, 4)</code>.');
        return;
      }
      var g = Epoly(got.tree, 'y');
      var plot = frame(6);
      var pts = [];
      for (var t = -6; t <= 6.0001; t += 0.05) pts.push([evalAt(got.tree, t, 'y'), t]);
      trace(plot, pts, 'plot-curve');
      /* The vertical line test, performed rather than described: for each
         whole number x, solve the relation for y EXACTLY and count the
         answers. Two answers at one x is the failure, and the line is drawn
         through them. */
      var witness = null;
      if (g) {
        for (var xi = -5; xi <= 5 && !witness; xi += 1) {
          var target = Psub(g, [R(BigInt(xi))]);
          var ys = Prationalroots(target).filter(function (r) { return Rzero(Peval(target, r)); });
          if (ys.length >= 2) witness = { x: R(BigInt(xi)), ys: ys };
        }
      }
      if (witness) {
        plot.vline(Rnum(witness.x), 'plot-asym', 'x = ' + Rtext(witness.x));
        witness.ys.forEach(function (y) {
          plot.point(Rnum(witness.x), Rnum(y), 'plot-point', '(' + Rtext(witness.x) + ', ' + Rtext(y) + ')');
        });
      }
      titleOut.textContent = 'x = ' + body;
      subOut.textContent = g ? 'a polynomial in y of degree ' + Pdeg(g) : 'a relation in y';
      kA.textContent = witness ? 'no' : (g ? 'no counterexample found' : 'not decided');
      kB.textContent = g && Pdeg(g) === 1 ? 'yes' : (witness ? 'not applicable' : 'not decided');
      kC.textContent = witness ? 'x = ' + Rtext(witness.x) : 'none';
      blocks.push(table('The vertical line test, carried out', [
        row('the relation', 'x = ' + (g ? Ptext(g, 'y') : body)),
        row('what the test asks', 'is there an x with two different y? Solve x = f(y) for y at each '
          + 'whole number x and count the answers.'),
        row('the search', witness
          ? 'at x = ' + Rtext(witness.x) + ' the equation ' + (g ? Ptext(g, 'y') : body) + ' = '
            + Rtext(witness.x) + ' has the solutions y = ' + witness.ys.map(Rtext).join(' and y = ')
          : 'no whole-number x from -5 to 5 gave two rational solutions'),
        row('verdict', witness
          ? chip('not a function of x', 'no') + ' two points share the x-coordinate '
            + Rtext(witness.x) + ', and the red line above passes through both'
          : chip('no failure found', 'hi') + ' which is evidence, not a proof: the search only looked '
            + 'at whole-number x with rational y'),
      ]));
      work.innerHTML = blocks.join('');
      status.innerHTML = witness
        ? '<strong>Not a function.</strong> A function may give only one output per input, and at '
          + 'x = ' + Rtext(witness.x) + ' this relation gives ' + witness.ys.length + ': y = '
          + witness.ys.map(Rtext).join(' and y = ') + '. That is exactly what the vertical line test '
          + 'looks for, and the two marked points are why it fails. Solving for y would need a '
          + '+- in front of a root &mdash; the give-away.'
        : '<strong>No x with two y was found, so nothing here fails the vertical line test.</strong> '
          + 'A sideways cubic passes it because y^3 is one-to-one: each x has exactly one real cube '
          + 'root, so solving for y needs no +-. Note what the lab actually checked, though &mdash; '
          + 'whole-number x with rational y. That is evidence for the claim, not a proof of it.';
      return;
    }

    /* a list of points */
    var out = [], bad = [], re = /\(([^()]*)\)/g, m;
    while ((m = re.exec(raw))) {
      var parts = m[1].split(',');
      if (parts.length !== 2) { bad.push(m[0]); continue; }
      var px = readR(parts[0].trim()), py = readR(parts[1].trim());
      if (px === null || py === null) { bad.push(m[0]); continue; }
      out.push({ x: px, y: py });
    }
    if (!out.length) {
      blank('<strong>No point could be read from that.</strong> Write points as '
        + '<code>(1, 2) (2, 4)</code>, or write a relation as <code>x = y^2 - 1</code>. '
        + (bad.length ? 'These were not a pair of numbers: ' + bad.join(' ') + '.' : ''));
      return;
    }
    var half = 4;
    out.forEach(function (p) { half = Math.max(half, Math.abs(Rnum(p.x)) + 1, Math.abs(Rnum(p.y)) + 1); });
    var plot2 = Plot(svg, { xmin: -half, xmax: half, ymin: -half, ymax: half }).frame();
    /* Group by x. A repeated x with two different y is the failure; a repeated
       x with the SAME y is just the same point written twice, and is not. */
    var byX = {}, clashes = [], repeats = [];
    out.forEach(function (p) {
      var key = Rtext(p.x);
      byX[key] = byX[key] || { x: p.x, ys: [] };
      if (!byX[key].ys.some(function (y) { return Requ(y, p.y); })) byX[key].ys.push(p.y);
      else repeats.push(p);
    });
    Object.keys(byX).forEach(function (key) { if (byX[key].ys.length > 1) clashes.push(byX[key]); });
    var byY = {}, collide = [];
    out.forEach(function (p) {
      var key = Rtext(p.y);
      byY[key] = byY[key] || { y: p.y, xs: [] };
      if (!byY[key].xs.some(function (x) { return Requ(x, p.x); })) byY[key].xs.push(p.x);
    });
    Object.keys(byY).forEach(function (key) { if (byY[key].xs.length > 1) collide.push(byY[key]); });

    clashes.forEach(function (c) { plot2.vline(Rnum(c.x), 'plot-asym', 'x = ' + Rtext(c.x)); });
    out.forEach(function (p) { plot2.point(Rnum(p.x), Rnum(p.y), 'plot-point', ptext(p)); });
    plot2.describe(out.length + ' points, with a vertical line drawn at every x that occurs twice.');

    var isFn = clashes.length === 0;
    titleOut.textContent = out.length + ' ordered pairs';
    subOut.textContent = out.map(ptext).join('  ');
    kA.textContent = isFn ? 'yes' : 'no';
    kB.textContent = isFn ? (collide.length ? 'no' : 'yes') : 'not applicable';
    kC.textContent = clashes.length ? 'x = ' + Rtext(clashes[0].x) : 'none';

    var rows = Object.keys(byX).map(function (key) {
      var g2 = byX[key];
      return '<tr><td>' + Rtext(g2.x) + '</td><td>' + g2.ys.map(Rtext).join(', ') + '</td><td>'
        + (g2.ys.length > 1 ? chip(g2.ys.length + ' outputs', 'no') : chip('one output', 'ok')) + '</td></tr>';
    });
    blocks.push('<div class="table-wrap"><table class="tt"><caption>Every input, with the outputs it '
      + 'was given</caption><thead><tr><th>x</th><th>y values</th><th>verdict</th></tr></thead><tbody>'
      + rows.join('') + '</tbody></table></div>');
    blocks.push(table('The two questions, which are not the same question', [
      row('a function?', isFn
        ? chip('yes', 'ok') + ' no x appears with two different y'
        : chip('no', 'no') + ' x = ' + Rtext(clashes[0].x) + ' is paired with '
          + clashes[0].ys.map(Rtext).join(' and ')),
      row('one-to-one?', !isFn ? muted('the question does not arise until it is a function')
        : (collide.length
           ? chip('no', 'no') + ' y = ' + Rtext(collide[0].y) + ' comes from x = '
             + collide[0].xs.map(Rtext).join(' and ') + ', which is allowed'
           : chip('yes', 'ok') + ' no two inputs share an output')),
      row('duplicates ignored', repeats.length
        ? repeats.map(ptext).join(' ') + ' repeat a pair already listed; a set does not count a member twice'
        : 'none'),
    ]));
    work.innerHTML = blocks.join('');
    status.innerHTML = isFn
      ? '<strong>This is a function.</strong> Every x in the list has exactly one y. '
        + (collide.length
           ? 'Several inputs share an output &mdash; y = ' + Rtext(collide[0].y) + ' arrives from x = '
             + collide[0].xs.map(Rtext).join(' and ') + ' &mdash; and that is permitted. The rule is '
             + 'one output per input, never one input per output. It does mean this function is not '
             + 'one-to-one, so it has no inverse.'
           : 'No two inputs share an output either, so it is also one-to-one and an inverse exists.')
      : '<strong>Not a function: x = ' + Rtext(clashes[0].x) + ' is sent to '
        + clashes[0].ys.map(Rtext).join(' and to ') + '.</strong> The red line above is the vertical '
        + 'line test failing &mdash; it meets the relation more than once. One input may have only one '
        + 'output; that single sentence is the whole definition, and everything else in this course '
        + 'depends on it.';
  }

  /* ------------------------------------------------------------ notation */
  function runNotation(body) {
    var got = parse(body);
    if (!got.tree) {
      blank('<strong>That formula could not be read: ' + got.err + '.</strong> '
        + 'Try <code>2x^2 - 5x + 1</code>, <code>1/x</code> or <code>sqrt(x)</code>.');
      return;
    }
    var tree = got.tree, poly = Epoly(tree, 'x');
    var a = readR(selAt.value);
    if (a === null) a = R0;
    var plot = frame(6);
    plot.curve(function (x) { return evalAt(tree, x, 'x'); });
    var av = Rnum(a), fav = evalAt(tree, av, 'x');
    if (isFinite(fav)) plot.point(av, fav, 'plot-point', 'f(' + Rtext(a) + ')');
    titleOut.textContent = 'f(x) = ' + body;
    subOut.textContent = poly ? 'a polynomial of degree ' + Pdeg(poly) : 'not a polynomial';

    var exact = Eexact(tree, a, 'x');
    var substituted = subx(body, '(' + Rtext(a) + ')');
    var value = exact !== null ? Rtext(exact)
      : (isFinite(fav) ? approx(fav, 6) + ' (rounded)' : 'undefined');

    /* The two expressions everybody conflates, computed independently. */
    var shifted = poly ? Pcompose(poly, [R1, R1]) : null;   /* f(x + 1) */
    var plusone = poly ? Padd(poly, [R1]) : null;           /* f(x) + 1 */
    var differ = poly ? !Pzero(Psub(shifted, plusone)) : null;

    kA.textContent = value;
    kB.textContent = shifted ? Ptext(shifted) : 'needs a polynomial';
    kC.textContent = plusone ? Ptext(plusone) : 'needs a polynomial';

    var blocks = [table('f(' + Rtext(a) + '), substituted before it is evaluated', [
      row('the rule', 'f(x) = ' + body),
      row('put ' + Rtext(a) + ' everywhere x appears', 'f(' + Rtext(a) + ') = ' + substituted),
      row('evaluate', exact !== null
        ? 'f(' + Rtext(a) + ') = ' + Rtext(exact) + '  ' + chip('exact', 'ok')
        : (isFinite(fav)
           ? 'f(' + Rtext(a) + ') = ' + approx(fav, 6) + '  ' + chip('irrational, so rounded', 'hi')
           : 'f(' + Rtext(a) + ') is undefined: ' + Rtext(a) + ' is not in the domain  ' + chip('no value', 'no'))),
    ])];

    if (poly) {
      var witness = R(2n);
      blocks.push(table('f(x + 1) is not f(x) + 1', [
        row('f(x + 1)', 'replace x by (x + 1) inside the rule: ' + Ptext(shifted)),
        row('f(x) + 1', 'evaluate f, then add 1: ' + Ptext(plusone)),
        row('the difference', Ptext(Psub(shifted, plusone)) + '  '
          + (differ ? chip('different functions', 'no') : chip('the same here', 'ok'))),
        row('at x = 2', 'f(3) = ' + Rtext(Peval(poly, R(3n))) + ', while f(2) + 1 = '
          + Rtext(Peval(poly, witness)) + ' + 1 = ' + Rtext(Radd(Peval(poly, witness), R1))),
      ]));
      var negated = Pcompose(poly, [R0, R(-1n)]);
      var isEven = Pzero(Psub(negated, poly)), isOdd = Pzero(Padd(negated, poly));
      blocks.push(table('f(-x) against -f(x)', [
        row('f(-x)', Ptext(negated)),
        row('-f(x)', Ptext(Pscale(poly, R(-1n)))),
        row('verdict', isEven ? chip('even: f(-x) = f(x)', 'ok') + ' the graph is symmetric about the y-axis'
          : (isOdd ? chip('odd: f(-x) = -f(x)', 'ok') + ' the graph has half-turn symmetry about the origin'
                   : chip('neither', 'hi') + ' most functions are neither, and that is not a defect')),
      ]));
    }

    if (!poly) {
      /* No exact polynomial arithmetic available, so the two expressions are
         built by substitution and separated by a VALUE rather than by
         subtracting them. Which of the two the lab did is stated. */
      var shiftText = subx(body, '(x + 1)'), plusText = '(' + body + ') + 1';
      var shiftGot = parse(shiftText), plusGot = parse(plusText);
      var wit = null;
      for (var w = -3; w <= 4 && !wit; w += 1) {
        if (!shiftGot.tree || !plusGot.tree) break;
        var p1 = evalAt(shiftGot.tree, w, 'x'), p2 = evalAt(plusGot.tree, w, 'x');
        if (isFinite(p1) && isFinite(p2) && Math.abs(p1 - p2) > 1e-9) {
          wit = { x: w, a: p1, b: p2 };
        }
      }
      kB.textContent = shiftText;
      kC.textContent = plusText;
      blocks.push(table('f(x + 1) is not f(x) + 1', [
        row('f(x + 1)', 'replace x by (x + 1) inside the rule: ' + shiftText),
        row('f(x) + 1', 'evaluate f, then add 1: ' + plusText),
        row('a witness', wit
          ? 'at x = ' + wit.x + ' they give ' + approx(wit.a, 5) + ' and ' + approx(wit.b, 5) + '  '
            + chip('different functions', 'no')
          : muted('no whole number from -3 to 4 separated them; with a root or a quotient in the way '
                  + 'the lab compares values rather than polynomials, so this is evidence and not a proof')),
      ]));
    }

    var vals = ['-2', '-1', '0', '1', '2', '3'].map(function (t) {
      var xr = readR(t), ex = Eexact(tree, xr, 'x'), num = evalAt(tree, Rnum(xr), 'x');
      return '<tr><td>' + t + '</td><td>' + (ex !== null ? Rtext(ex)
        : (isFinite(num) ? approx(num, 5) + ' (rounded)' : 'undefined')) + '</td></tr>';
    });
    blocks.push('<div class="table-wrap"><table class="tt"><caption>The machine, run on six inputs'
      + '</caption><thead><tr><th>input</th><th>output</th></tr></thead><tbody>' + vals.join('')
      + '</tbody></table></div>');
    work.innerHTML = blocks.join('');

    status.innerHTML = exact === null && !isFinite(fav)
      ? '<strong>f(' + Rtext(a) + ') does not exist.</strong> The machine was handed an input it '
        + 'cannot process &mdash; ' + body + ' has no value at x = ' + Rtext(a) + '. A function is '
        + 'its rule AND its domain, and an input outside the domain does not produce an answer; it '
        + 'produces nothing at all.'
      : '<strong>f(' + Rtext(a) + ') = ' + value + '.</strong> Notation first: f(' + Rtext(a)
        + ') is not f times ' + Rtext(a) + '. It names the output when the input is ' + Rtext(a)
        + ', and the way to compute it is to write the rule out with ' + Rtext(a)
        + ' in every position x held &mdash; brackets included, which is what stops '
        + '(' + Rtext(a) + ')^2 turning into something else. '
        + (poly && differ
           ? 'The table above also settles the other confusion: f(x + 1) = ' + Ptext(shifted)
             + ' and f(x) + 1 = ' + Ptext(plusone) + ' are different functions, because the first '
             + 'changes the input and the second changes the output.'
           : '');
  }
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Type it, or take one of these"),
        panel_intro=cfg.get("panel_intro", FUNCOPS_INTRO[mode]),
        script=script + FUNCOPS_TAIL.replace('/*BINDINGS*/', binds),
    )


# The rest of the funcops script: the four modes that work on a formula, and
# the dispatcher that chooses one. Kept as a separate constant only because one
# 900-line string literal is harder to read than two.
FUNCOPS_TAIL = r"""
  /* -------------------------------------------------------------- domain */
  /* The range, where it can be PROVED, and a labelled sample where it cannot.
     Sampling and proving are both legitimate; presenting one as the other is
     not, so every branch below records which of the two it did. */
  function rangeOf(tree, poly, rat, ivs, holes, asyms) {
    /* A quotient whose denominator cancels away IS a polynomial, with some
       points removed. Reducing first is what lets (x^2 - 4)/(x - 2) be
       answered exactly instead of sampled. */
    var eff = poly, red0 = rat ? ratreduce(rat) : null;
    if (!eff && red0 && Pdeg(red0.d) === 0 && !Pzero(red0.d)) {
      eff = Pscale(red0.n, Rinv(red0.d[0]));
    }
    var missing = holes.map(function (hole) { return Rtext(hole.y); });
    function without(text) {
      return missing.length ? text + ', except ' + missing.join(' and ') + ' (the hole' 
        + (missing.length > 1 ? 's' : '') + ')' : text;
    }
    if (eff && Pzero(eff)) return { text: '{0}', proved: true, why: 'the function is the constant 0' };
    if (eff) {
      var d = Pdeg(eff);
      if (d === 0) return { text: '{' + Rtext(eff[0]) + '}', proved: true,
                            why: 'a constant function takes one value and no others' };
      if (d === 1) return { text: without('(-inf, inf)'), proved: true,
                            why: 'a line with non-zero slope reaches every height exactly once'
                                 + (missing.length ? ', and a hole removes the value it would have had there' : '') };
      if (d === 2) {
        var h = Rdiv(Rneg(eff[1]), Rmul(R(2n), eff[2])), k = Peval(eff, h);
        var up = Rsign(eff[2]) > 0;
        return { text: without(up ? '[' + Rtext(k) + ', inf)' : '(-inf, ' + Rtext(k) + ']'), proved: true,
                 why: 'the vertex is at (' + Rtext(h) + ', ' + Rtext(k) + '), and a parabola opening '
                      + (up ? 'upward has no value below it' : 'downward has none above it') };
      }
      if (d % 2 === 1) return { text: without('(-inf, inf)'), proved: true,
                                why: 'an odd-degree polynomial runs from -inf to +inf and is continuous, '
                                     + 'so it takes every value on the way' };
    }
    /* A quotient of two linear pieces: solve y = (px + q)/(rx + s) for x. The
       one y that cannot be reached is the one that kills the x term. */
    if (rat) {
      var red = ratreduce(rat);
      if (red && Pdeg(red.n) <= 1 && Pdeg(red.d) === 1) {
        var pnum = red.n.length > 1 ? red.n[1] : R0, q = red.n.length ? red.n[0] : R0;
        var r = red.d[1], sc = red.d[0];
        if (!Rzero(Rsub(Rmul(pnum, sc), Rmul(q, r)))) {
          var miss = Rdiv(pnum, r);
          return { text: 'every real number except ' + Rtext(miss)
                     + (missing.length ? ' and ' + missing.join(' and ') : ''),
                   proved: true,
                   why: 'solving y = ' + rattext(red) + ' for x gives x = ('
                        + Ptext([Rneg(q), sc], 'y') + ')/(' + Ptext([pnum, Rneg(r)], 'y')
                        + '), and that has no answer only when the bottom is 0, at y = ' + Rtext(miss)
                        + (missing.length ? '. A hole removes ' + missing.join(' and ') + ' as well' : '') };
        }
      }
    }
    /* sqrt of a line: the radicand runs over every non-negative value on the
       domain, and the square root of those is every non-negative value. */
    if (tree && tree.k === 'fn' && tree.v === 'sqrt') {
      var inner = Epoly(tree.a, 'x');
      if (inner && Pdeg(inner) === 1) {
        return { text: '[0, inf)', proved: true,
                 why: 'on its domain the radicand ' + Ptext(inner) + ' takes every value from 0 '
                      + 'upward, and the square root of those is every number from 0 upward' };
      }
    }
    if (asyms && asyms.length) {
      return { text: 'unbounded: the values run away near x = '
                 + asyms.map(Rtext).join(' and x = '), proved: false,
               why: 'a vertical asymptote sends the function past every bound, so no sampled interval '
                    + 'can be its range; deciding which values ARE reached needs the algebra, not the '
                    + 'picture' };
    }
    return null;
  }

  function runDomain(body) {
    var got = parse(body);
    if (!got.tree) {
      blank('<strong>That formula could not be read: ' + got.err + '.</strong> '
        + 'Try <code>1/(x - 2)</code>, <code>sqrt(x - 3)</code> or <code>(x^2 - 4)/(x - 2)</code>.');
      return;
    }
    var tree = got.tree, poly = Epoly(tree, 'x'), rat = Erat(tree, 'x');
    var cons = constraintsOf(tree, 'x', []);
    var dom = domainOf(cons);
    var ivs = dom.intervals;
    var fn = function (x) { return evalAt(tree, x, 'x'); };

    /* A hole and an asymptote look identical on a picture and are told apart
       by cancelling: a factor that divides BOTH numerator and denominator
       leaves a single missing point behind; one that divides only the
       denominator leaves an asymptote. */
    var holes = [], asyms = [], reduced = null;
    if (rat && Pdeg(rat.d) >= 1) {
      reduced = ratreduce(rat);
      Pfactor(rat.d).factors.forEach(function (item) {
        var r = item.root;
        if (reduced && !Rzero(Peval(reduced.d, r))) {
          var y = Rdiv(Peval(reduced.n, r), Peval(reduced.d, r));
          if (!holes.some(function (h) { return Requ(h.x, r); })) holes.push({ x: r, y: y });
        } else if (!asyms.some(function (v) { return Requ(v, r); })) {
          asyms.push(r);
        }
      });
    }

    var half = 8;
    dom.boundaries.forEach(function (b) { half = Math.max(half, Math.abs(b.val) + 3); });
    var yw = ywindow(fn, -half, half);
    var plot = Plot(svg, { xmin: -half, xmax: half, ymin: yw.lo, ymax: yw.hi });
    plot.frame();
    plot.curve(fn);
    asyms.forEach(function (r) { plot.vline(Rnum(r), 'plot-asym', 'x = ' + Rtext(r)); });
    holes.forEach(function (h) { plot.hole(Rnum(h.x), Rnum(h.y)); });
    ivs.forEach(function (iv) {
      if (iv.lo && iv.loClosed && isFinite(fn(iv.lo.val))) {
        plot.point(iv.lo.val, fn(iv.lo.val), 'plot-point root', 'x = ' + iv.lo.text);
      }
      if (iv.hi && iv.hiClosed && isFinite(fn(iv.hi.val))) {
        plot.point(iv.hi.val, fn(iv.hi.val), 'plot-point root', 'x = ' + iv.hi.text);
      }
    });
    plot.describe('y = ' + body + ' drawn on its domain ' + domaintext(ivs) + '.');

    var rng = rangeOf(tree, poly, rat, ivs, holes, asyms);
    if (!rng) {
      /* Not provable with what is here, so it is sampled -- and said to be. */
      var lo = Infinity, hi = -Infinity;
      for (var i = 0; i <= 2000; i += 1) {
        var xv = -half + 2 * half * i / 2000, yv = fn(xv);
        if (isFinite(yv)) { lo = Math.min(lo, yv); hi = Math.max(hi, yv); }
      }
      rng = isFinite(lo)
        ? { text: 'about [' + approx(lo, 3) + ', ' + approx(hi, 3) + ']', proved: false,
            why: 'sampled at 2001 points across the window drawn; this is what the function DID '
                 + 'produce there, not a proof of what it can produce' }
        : { text: 'nothing: the function has no value anywhere in the window', proved: false,
            why: 'no sample in the window was a real number' };
    }

    titleOut.textContent = 'f(x) = ' + body;
    subOut.textContent = rat && Pdeg(rat.d) >= 1 ? 'a rational function' : (poly ? 'a polynomial' : 'a formula');
    kA.textContent = domaintext(ivs);
    kB.textContent = dom.boundaries.length
      ? dom.boundaries.filter(function (b) { return !inDomain(ivs, b.val); })
          .map(function (b) { return b.text; }).join(', ') || 'nothing'
      : 'nothing';
    kC.textContent = rng.text;

    var crows = cons.map(function (c) {
      var what = c.why === 'sqrt' ? 'a square root needs' : (c.why === 'log' ? 'a logarithm needs' : 'a denominator needs');
      var demand = c.rel === 'ge' ? ' >= 0' : (c.rel === 'gt' ? ' > 0' : ' != 0');
      return row(what, c.poly ? Ptext(c.poly) + demand : muted('this argument is not a polynomial, so it was not solved exactly'));
    });
    if (!crows.length) crows.push(row('nothing is forbidden', 'no denominator, root or logarithm appears'));
    var blocks = [table('What the formula forbids', crows)];

    blocks.push(table('Domain and range', [
      row('domain', domaintext(ivs) + (dom.exact ? '' : '  ' + chip('one boundary was found numerically', 'hi'))),
      row('range', rng.text + '  ' + (rng.proved ? chip('derived', 'ok') : chip('not proved', 'hi'))),
      row('why', rng.why),
    ]));

    if (rat && Pdeg(rat.d) >= 1) {
      var hrows = [];
      holes.forEach(function (h) {
        hrows.push(row('a hole at x = ' + Rtext(h.x),
          'the factor ' + Pfactortext([Rneg(h.x), R1]) + ' divides the top and the bottom. After '
          + 'cancelling, ' + rattext(reduced) + ' has the value ' + Rtext(h.y) + ' there &mdash; but '
          + 'the ORIGINAL formula still has 0/0 at x = ' + Rtext(h.x) + ', so the point is missing. '
          + 'One point, drawn hollow.'));
      });
      asyms.forEach(function (r) {
        hrows.push(row('an asymptote at x = ' + Rtext(r),
          'the factor ' + Pfactortext([Rneg(r), R1]) + ' survives in the denominator after '
          + 'cancelling, so near x = ' + Rtext(r) + ' the values run away. Nothing can be filled in here.'));
      });
      if (hrows.length) {
        hrows.push(row('cancelled form', reduced ? rattext(reduced) : rattext(rat)));
        blocks.push(table('A hole or an asymptote: the difference is which factor cancels', hrows));
      }
    }

    var vrows = [];
    for (var j = -3; j <= 4; j += 1) {
      var xr = R(BigInt(j)), inside = inDomain(ivs, j);
      var hole = holes.filter(function (h) { return Requ(h.x, xr); })[0];
      vrows.push('<tr><td>' + j + '</td><td>'
        + (inside ? valuetext(tree, xr, 'x')
           : '<span class="tone-red">' + (hole ? 'a hole: the limit is ' + Rtext(hole.y)
                                              + ' but there is no value' : 'not defined') + '</span>')
        + '</td></tr>');
    }
    blocks.push('<div class="table-wrap"><table class="tt"><caption>Values, and the inputs that have '
      + 'none</caption><thead><tr><th>x</th><th>f(x)</th></tr></thead><tbody>' + vrows.join('')
      + '</tbody></table></div>');
    work.innerHTML = blocks.join('');

    var excluded = dom.boundaries.filter(function (b) { return !inDomain(ivs, b.val); });
    status.innerHTML = holes.length
      ? '<strong>x = ' + Rtext(holes[0].x) + ' is a hole, not an asymptote.</strong> The factor '
        + Pfactortext([Rneg(holes[0].x), R1]) + ' cancels, so the graph is '
        + rattext(reduced) + ' everywhere except at that one x &mdash; where the original formula '
        + 'asks for 0/0 and gets nothing. The domain is ' + domaintext(ivs) + ': cancelling changes '
        + 'the formula but NOT the domain, and that is the whole point of the lesson. The hollow '
        + 'circle marks the missing point at (' + Rtext(holes[0].x) + ', ' + Rtext(holes[0].y) + ').'
      : (excluded.length
         ? '<strong>The domain is ' + domaintext(ivs) + '.</strong> '
           + (excluded.length === 1 ? 'The value ' : 'The values ')
           + excluded.map(function (b) { return b.text; }).join(' and ')
           + (excluded.length === 1 ? ' is excluded' : ' are excluded')
           + ' because the formula asks for something impossible there. The range is ' + rng.text
           + ' &mdash; ' + rng.why + '.'
         : (ivs.length === 1 && ivs[0].lo === null && ivs[0].hi === null
            ? '<strong>The domain is every real number.</strong> '
              + 'No denominator can be zero and no root can be handed a negative, so nothing is '
              + 'excluded. The range is ' + rng.text + ', and that is the harder half of the '
              + 'question: ' + rng.why + '.'
            : '<strong>The domain is ' + domaintext(ivs) + ': it stops rather than having points '
              + 'punched out of it.</strong> Nothing inside is removed &mdash; the formula simply '
              + 'refuses every x outside that set, and the endpoint IS included, which is what the '
              + 'square bracket means. The range is ' + rng.text + ': ' + rng.why + '.'));
  }

  /* ----------------------------------------------------------- piecewise */
  function readinterval(text) {
    var m = /^\s*([\[(])\s*([^,]+?)\s*,\s*([^)\]]+?)\s*([\])])\s*$/.exec(text);
    if (!m) return null;
    function end(tok) {
      var t = tok.trim().toLowerCase();
      if (t === '-inf' || t === '-infinity') return { v: null };
      if (t === 'inf' || t === '+inf' || t === 'infinity') return { v: null };
      var r = readR(tok.trim());
      return r === null ? null : { v: r };
    }
    var lo = end(m[2]), hi = end(m[3]);
    if (!lo || !hi) return null;
    return { lo: lo.v, loClosed: m[1] === '[' && lo.v !== null,
             hi: hi.v, hiClosed: m[4] === ']' && hi.v !== null };
  }
  function ivHas(iv, x) {
    if (iv.lo !== null) {
      var c = Rcmp(x, iv.lo);
      if (c < 0 || (c === 0 && !iv.loClosed)) return false;
    }
    if (iv.hi !== null) {
      var d = Rcmp(x, iv.hi);
      if (d > 0 || (d === 0 && !iv.hiClosed)) return false;
    }
    return true;
  }
  function ivHasNum(iv, x) {
    if (iv.lo !== null && (x < Rnum(iv.lo) || (x === Rnum(iv.lo) && !iv.loClosed))) return false;
    if (iv.hi !== null && (x > Rnum(iv.hi) || (x === Rnum(iv.hi) && !iv.hiClosed))) return false;
    return true;
  }
  function ivText(iv) {
    return (iv.loClosed ? '[' : '(') + (iv.lo === null ? '-inf' : Rtext(iv.lo)) + ', '
      + (iv.hi === null ? 'inf' : Rtext(iv.hi)) + (iv.hiClosed ? ']' : ')');
  }
  /* Where two intervals overlap, exactly -- the test that decides whether a
     piecewise definition is a function at all. */
  function ivOverlap(A, B) {
    var lo, loC, hi, hiC;
    if (A.lo === null) { lo = B.lo; loC = B.loClosed; }
    else if (B.lo === null) { lo = A.lo; loC = A.loClosed; }
    else {
      var c = Rcmp(A.lo, B.lo);
      if (c > 0) { lo = A.lo; loC = A.loClosed; }
      else if (c < 0) { lo = B.lo; loC = B.loClosed; }
      else { lo = A.lo; loC = A.loClosed && B.loClosed; }
    }
    if (A.hi === null) { hi = B.hi; hiC = B.hiClosed; }
    else if (B.hi === null) { hi = A.hi; hiC = A.hiClosed; }
    else {
      var d = Rcmp(A.hi, B.hi);
      if (d < 0) { hi = A.hi; hiC = A.hiClosed; }
      else if (d > 0) { hi = B.hi; hiC = B.hiClosed; }
      else { hi = A.hi; hiC = A.hiClosed && B.hiClosed; }
    }
    if (lo === null || hi === null) return { lo: lo, loClosed: loC, hi: hi, hiClosed: hiC };
    var e = Rcmp(lo, hi);
    if (e > 0) return null;
    if (e === 0 && !(loC && hiC)) return null;
    return { lo: lo, loClosed: loC, hi: hi, hiClosed: hiC };
  }

  function runPiecewise(raw) {
    var chunks = raw.split(';').map(function (t) { return t.trim(); }).filter(Boolean);
    var pieces = [], bad = [];
    chunks.forEach(function (chunk) {
      var m = /^([\s\S]+?)\s+on\s+([\s\S]+)$/i.exec(chunk);
      if (!m) { bad.push(chunk); return; }
      var got = parse(m[1].trim()), iv = readinterval(m[2]);
      if (!got.tree || !iv) { bad.push(chunk); return; }
      pieces.push({ body: m[1].trim(), tree: got.tree, poly: Epoly(got.tree, 'x'), iv: iv });
    });
    if (!pieces.length) {
      blank('<strong>No piece could be read.</strong> Write each one as an expression, the word '
        + '<code>on</code>, and an interval: <code>x^2 on (-inf, 1); 2x - 1 on [1, inf)</code>. '
        + 'Square brackets include the endpoint and round brackets exclude it. '
        + (bad.length ? 'Not readable: ' + bad.join(' ; ') + '.' : ''));
      return;
    }
    pieces.sort(function (a, b) {
      if (a.iv.lo === null) return -1;
      if (b.iv.lo === null) return 1;
      return Rcmp(a.iv.lo, b.iv.lo);
    });

    /* Two pieces that overlap give one x two values, which is not a function. */
    var overlaps = [];
    for (var i = 0; i < pieces.length; i += 1) {
      for (var j = i + 1; j < pieces.length; j += 1) {
        var ov = ivOverlap(pieces[i].iv, pieces[j].iv);
        if (!ov) continue;
        var at = ov.lo !== null ? ov.lo : (ov.hi !== null ? ov.hi : R0);
        var va = Eexact(pieces[i].tree, at, 'x'), vb = Eexact(pieces[j].tree, at, 'x');
        overlaps.push({ a: i, b: j, iv: ov, at: at, va: va, vb: vb,
                        clash: !(va !== null && vb !== null && Requ(va, vb)) });
      }
    }
    /* A gap is a piece of the line that no interval covers. */
    var gaps = [];
    for (var g = 0; g + 1 < pieces.length; g += 1) {
      var left = pieces[g].iv, right = pieces[g + 1].iv;
      if (left.hi === null || right.lo === null) continue;
      var c2 = Rcmp(left.hi, right.lo);
      if (c2 < 0 || (c2 === 0 && !left.hiClosed && !right.loClosed)) {
        gaps.push({ lo: left.hi, loClosed: !left.hiClosed, hi: right.lo, hiClosed: !right.loClosed });
      }
    }

    var half = 6;
    pieces.forEach(function (p) {
      if (p.iv.lo !== null) half = Math.max(half, Math.abs(Rnum(p.iv.lo)) + 3);
      if (p.iv.hi !== null) half = Math.max(half, Math.abs(Rnum(p.iv.hi)) + 3);
    });
    var whole = function (x) {
      for (var q = 0; q < pieces.length; q += 1) {
        if (ivHasNum(pieces[q].iv, x)) return evalAt(pieces[q].tree, x, 'x');
      }
      return NaN;
    };
    var yw = ywindow(whole, -half, half);
    var plot = Plot(svg, { xmin: -half, xmax: half, ymin: yw.lo, ymax: yw.hi });
    plot.frame();
    pieces.forEach(function (p, idx) {
      plot.curve(function (x) {
        return ivHasNum(p.iv, x) ? evalAt(p.tree, x, 'x') : NaN;
      }, idx % 2 === 0 ? 'plot-curve' : 'plot-curve alt');
      [[p.iv.lo, p.iv.loClosed], [p.iv.hi, p.iv.hiClosed]].forEach(function (endp) {
        if (endp[0] === null) return;
        var xv = Rnum(endp[0]), yv = evalAt(p.tree, xv, 'x');
        if (!isFinite(yv)) return;
        if (endp[1]) plot.point(xv, yv, 'plot-point root');
        else plot.hole(xv, yv);
      });
    });
    overlaps.forEach(function (o) {
      if (o.clash) plot.vline(Rnum(o.at), 'plot-asym', 'x = ' + Rtext(o.at));
    });
    plot.describe(pieces.length + ' pieces, each drawn only on its own interval, with filled and '
      + 'hollow endpoints.');

    titleOut.textContent = pieces.length + ' pieces';
    subOut.textContent = pieces.map(function (p) { return p.body + ' on ' + ivText(p.iv); }).join(';  ');

    var clash = overlaps.filter(function (o) { return o.clash; })[0];
    kA.textContent = String(pieces.length);
    kB.textContent = pieces.map(function (p) { return ivText(p.iv); }).join(' U ')
      + (gaps.length ? '  (with a gap)' : '');
    kC.textContent = clash ? 'two values at x = ' + Rtext(clash.at)
      : (gaps.length ? 'a gap' : 'one value everywhere it is defined');

    var prows = pieces.map(function (p) {
      var lo = p.iv.lo === null ? null : Eexact(p.tree, p.iv.lo, 'x');
      var hi = p.iv.hi === null ? null : Eexact(p.tree, p.iv.hi, 'x');
      return '<tr><td>' + p.body + '</td><td>' + ivText(p.iv) + '</td><td>'
        + (p.iv.lo === null ? 'runs to -inf'
           : (lo === null ? 'no exact value' : Rtext(lo) + (p.iv.loClosed ? ' (filled)' : ' (hollow)')))
        + '</td><td>'
        + (p.iv.hi === null ? 'runs to inf'
           : (hi === null ? 'no exact value' : Rtext(hi) + (p.iv.hiClosed ? ' (filled)' : ' (hollow)')))
        + '</td></tr>';
    });
    var blocks = ['<div class="table-wrap"><table class="tt"><caption>Each piece, on its own interval'
      + '</caption><thead><tr><th>rule</th><th>where</th><th>at the left end</th>'
      + '<th>at the right end</th></tr></thead><tbody>' + prows.join('') + '</tbody></table></div>'];

    /* Continuity at each join, from the two formulas rather than the picture. */
    var joins = [], jumped = false;
    for (var b2 = 0; b2 + 1 < pieces.length; b2 += 1) {
      var L = pieces[b2], Rp = pieces[b2 + 1];
      if (L.iv.hi === null || Rp.iv.lo === null) continue;
      if (!Requ(L.iv.hi, Rp.iv.lo)) continue;
      var at2 = L.iv.hi;
      var vl = Eexact(L.tree, at2, 'x'), vr = Eexact(Rp.tree, at2, 'x');
      var owner = ivHas(L.iv, at2) && ivHas(Rp.iv, at2)
        ? 'BOTH pieces, which is the problem'
        : (ivHas(L.iv, at2) ? 'the left piece'
           : (ivHas(Rp.iv, at2) ? 'the right piece' : 'neither piece, so x = ' + Rtext(at2) + ' has no value'));
      if (!(vl !== null && vr !== null && Requ(vl, vr))) jumped = true;
      joins.push(row('at x = ' + Rtext(at2),
        'the left rule gives ' + (vl === null ? '?' : Rtext(vl)) + ', the right rule gives '
        + (vr === null ? '?' : Rtext(vr)) + '. '
        + (vl !== null && vr !== null && Requ(vl, vr)
           ? chip('they meet: no jump', 'ok') + ' the graph joins up here'
           : (vl !== null && vr !== null
              ? chip('a jump of ' + Rtext(Rsub(vr, vl)), 'no') + ' the graph breaks here'
              : chip('not comparable exactly', 'hi')))
        + '  The value at x = ' + Rtext(at2) + ' itself belongs to ' + owner + '.'));
    }
    if (joins.length) blocks.push(table('The joins, computed from both rules', joins));

    if (overlaps.length || gaps.length || bad.length) {
      var trouble = [];
      overlaps.forEach(function (o) {
        trouble.push(row('two pieces overlap on ' + ivText(o.iv), o.clash
          ? chip('not a function', 'no') + ' at x = ' + Rtext(o.at) + ' the rules give '
            + (o.va === null ? '?' : Rtext(o.va)) + ' and ' + (o.vb === null ? '?' : Rtext(o.vb))
            + ', so this definition sends one input to two outputs'
          : chip('agrees where they meet', 'ok') + ' both rules give '
            + (o.va === null ? 'the same value' : Rtext(o.va)) + ' at x = ' + Rtext(o.at)
            + ', so the overlap is harmless &mdash; untidy, but harmless'));
      });
      gaps.forEach(function (gp) {
        trouble.push(row('a gap', 'nothing is defined on '
          + (gp.loClosed ? '[' : '(') + Rtext(gp.lo) + ', ' + Rtext(gp.hi) + (gp.hiClosed ? ']' : ')')
          + '. That is allowed &mdash; it just means those x are not in the domain'));
      });
      bad.forEach(function (t) { trouble.push(row('could not be read', t)); });
      blocks.push(table('What the pieces do to each other', trouble));
    }
    work.innerHTML = blocks.join('');

    var jump = jumped;
    status.innerHTML = clash
      ? '<strong>This is not a function.</strong> The intervals overlap at x = ' + Rtext(clash.at)
        + ', where one rule gives ' + (clash.va === null ? '?' : Rtext(clash.va)) + ' and the other '
        + 'gives ' + (clash.vb === null ? '?' : Rtext(clash.vb)) + '. A piecewise DEFINITION is only a '
        + 'function when the intervals do not overlap &mdash; or when they agree wherever they do. '
        + 'Change one bracket from [ to ( and the definition is repaired.'
      : (gaps.length
         ? '<strong>There is a gap in the domain.</strong> Nothing is defined between '
           + Rtext(gaps[0].lo) + ' and ' + Rtext(gaps[0].hi) + ', so those inputs have no output at '
           + 'all. That is perfectly legal: the domain of a piecewise function is the union of its '
           + 'intervals, and the union here has a hole in the middle of it.'
         : (jump
            ? '<strong>The pieces do not meet.</strong> At the join the two rules give different '
              + 'values, so the graph jumps. The filled circle shows which value the function '
              + 'actually takes there and the hollow one shows the value it approaches but never '
              + 'reaches &mdash; that distinction is what the two kinds of circle are for.'
            : '<strong>The pieces meet, so the graph joins up.</strong> At every join the two rules '
              + 'agree, computed from the formulas rather than judged from the picture. Note that '
              + 'the endpoint still belongs to exactly one piece: an x cannot be in two intervals '
              + 'and still have one output.'));
  }

  /* ------------------------------------------------------------- compose */
  function runCompose(fBody, gBody) {
    var fGot = parse(fBody), gGot = parse(gBody);
    if (!fGot.tree || !gGot.tree) {
      blank('<strong>' + (!fGot.tree ? 'f' : 'g') + ' could not be read: '
        + (!fGot.tree ? fGot.err : gGot.err) + '.</strong> Both boxes need a formula in x, such as '
        + '<code>2x</code> and <code>x^2</code>.');
      return;
    }
    var fPoly = Epoly(fGot.tree, 'x'), gPoly = Epoly(gGot.tree, 'x');
    var fgText = subx(fBody, '(' + gBody + ')'), gfText = subx(gBody, '(' + fBody + ')');
    var fgGot = parse(fgText), gfGot = parse(gfText);
    if (!fgGot.tree || !gfGot.tree) {
      blank('<strong>The composite could not be assembled from those two formulas.</strong> '
        + 'Each box must hold a complete expression in x.');
      return;
    }
    var fgPoly = (fPoly && gPoly) ? Pcompose(fPoly, gPoly) : null;
    var gfPoly = (fPoly && gPoly) ? Pcompose(gPoly, fPoly) : null;

    var fgFn = function (x) { return evalAt(fGot.tree, evalAt(gGot.tree, x, 'x'), 'x'); };
    var gfFn = function (x) { return evalAt(gGot.tree, evalAt(fGot.tree, x, 'x'), 'x'); };
    var half = 6;
    var yw = ywindow(function (x) { var a = fgFn(x); return isFinite(a) ? a : gfFn(x); }, -half, half);
    var plot = Plot(svg, { xmin: -half, xmax: half, ymin: yw.lo, ymax: yw.hi });
    plot.frame();
    plot.curve(function (x) { return evalAt(fGot.tree, x, 'x'); }, 'plot-curve parent');
    plot.curve(function (x) { return evalAt(gGot.tree, x, 'x'); }, 'plot-curve parent');
    plot.curve(fgFn, 'plot-curve');
    plot.curve(gfFn, 'plot-curve alt');
    plot.describe('f and g dashed, f(g(x)) solid and g(f(x)) in the second colour.');

    var same = (fgPoly && gfPoly) ? Pzero(Psub(fgPoly, gfPoly)) : null;
    var witness = null;
    if (same === false) {
      for (var i = -4; i <= 4 && !witness; i += 1) {
        var xr = R(BigInt(i));
        var a = Peval(fgPoly, xr), b = Peval(gfPoly, xr);
        if (!Requ(a, b)) witness = { x: xr, fg: a, gf: b };
      }
    } else if (same === null) {
      for (var t = -4; t <= 4 && !witness; t += 1) {
        var av = fgFn(t), bv = gfFn(t);
        if (isFinite(av) && isFinite(bv) && Math.abs(av - bv) > 1e-9) {
          witness = { x: R(BigInt(t)), num: true, fg: av, gf: bv };
        }
      }
    }

    var cons = constraintsOf(fgGot.tree, 'x', []);
    var dom = domainOf(cons);

    titleOut.textContent = 'f(x) = ' + fBody + ',   g(x) = ' + gBody;
    subOut.textContent = 'f(g(x)) = ' + (fgPoly ? Ptext(fgPoly) : fgText);
    kA.textContent = fgPoly ? Ptext(fgPoly) : fgText;
    kB.textContent = gfPoly ? Ptext(gfPoly) : gfText;
    kC.textContent = same === null ? 'compared numerically' : (same ? 'yes' : 'no');

    var blocks = [table('Both orders, worked out separately', [
      row('f(g(x)): do g first', 'replace every x in f by (' + gBody + '):  ' + fgText
        + (fgPoly ? '  =  ' + Ptext(fgPoly) : '')),
      row('g(f(x)): do f first', 'replace every x in g by (' + fBody + '):  ' + gfText
        + (gfPoly ? '  =  ' + Ptext(gfPoly) : '')),
      row('are they the same function?', same === null
        ? chip('checked at sample points only', 'hi') + ' one of these is not a polynomial, so the '
          + 'two were compared numerically rather than by subtracting them'
        : (same ? chip('yes, here', 'ok') + ' the difference is the zero polynomial &mdash; for THIS '
                  + 'pair the order does not matter, which is why "composition is not commutative" is '
                  + 'a statement about pairs in general and not about every pair'
                : chip('no', 'no') + ' the difference is ' + Ptext(Psub(fgPoly, gfPoly)))),
      row('a witness', witness
        ? 'at x = ' + Rtext(witness.x) + ': f(g(x)) = '
          + (witness.num ? approx(witness.fg, 5) : Rtext(witness.fg)) + ', g(f(x)) = '
          + (witness.num ? approx(witness.gf, 5) : Rtext(witness.gf))
        : 'no x between -4 and 4 separated them'),
    ])];

    var drows = cons.map(function (c) {
      var what = c.why === 'sqrt' ? 'a square root inside needs' : (c.why === 'log' ? 'a logarithm needs' : 'a denominator needs');
      var demand = c.rel === 'ge' ? ' >= 0' : (c.rel === 'gt' ? ' > 0' : ' != 0');
      return row(what, c.poly ? Ptext(c.poly) + demand : muted('not solved exactly'));
    });
    drows.push(row('domain of f(g(x))', domaintext(dom.intervals)));
    drows.push(row('the trap', 'the composite may SIMPLIFY to something with a bigger domain, and the '
      + 'simplified formula is then the wrong answer: x has to survive g before f ever sees it.'));
    blocks.push(table('The domain of the composite, from the composite formula', drows));

    var vrows = [];
    for (var k = -2; k <= 4; k += 1) {
      var xk = R(BigInt(k));
      var gv = Eexact(gGot.tree, xk, 'x'), gnum = evalAt(gGot.tree, k, 'x');
      var fgv = fgFn(k), gfv = gfFn(k);
      vrows.push('<tr><td>' + k + '</td><td>'
        + (gv !== null ? Rtext(gv) : (isFinite(gnum) ? approx(gnum, 4) : 'undefined')) + '</td><td>'
        + (isFinite(fgv) ? (fgPoly ? Rtext(Peval(fgPoly, xk)) : approx(fgv, 4)) : 'undefined') + '</td><td>'
        + (isFinite(gfv) ? (gfPoly ? Rtext(Peval(gfPoly, xk)) : approx(gfv, 4)) : 'undefined') + '</td></tr>');
    }
    blocks.push('<div class="table-wrap"><table class="tt"><caption>One input, through both machines, '
      + 'in both orders</caption><thead><tr><th>x</th><th>g(x)</th><th>f(g(x))</th><th>g(f(x))</th>'
      + '</tr></thead><tbody>' + vrows.join('') + '</tbody></table></div>');
    work.innerHTML = blocks.join('');

    status.innerHTML = same === true
      ? '<strong>These two compose to the same function in both orders.</strong> f(g(x)) and g(f(x)) '
        + 'both come to ' + Ptext(fgPoly) + ', and the lab knows that by subtracting them and getting '
        + 'the zero polynomial &mdash; not by looking at the picture, where two identical curves are '
        + 'indistinguishable from one. Composition is not commutative IN GENERAL; particular pairs '
        + 'like these commute, and shifts always do.'
      : (witness
         ? '<strong>Order matters: f(g(x)) and g(f(x)) are different functions.</strong> At x = '
           + Rtext(witness.x) + ' the first gives ' + (witness.num ? approx(witness.fg, 5) : Rtext(witness.fg))
           + ' and the second gives ' + (witness.num ? approx(witness.gf, 5) : Rtext(witness.gf))
           + '. One number where they disagree is all it takes, and the two curves above separate '
           + 'exactly where the table says they do. The domain of f(g(x)) is '
           + domaintext(dom.intervals) + ' &mdash; every x has to survive g first.'
         : '<strong>No input between -4 and 4 told the two orders apart.</strong> That is not a proof '
           + 'that they are equal: with a root or a quotient in the way, the lab compares values '
           + 'rather than polynomials, and equal values at nine points is evidence and nothing more.');
  }

  /* ------------------------------------------------------------- inverse */
  function runInverse(body) {
    var got = parse(body);
    if (!got.tree) {
      blank('<strong>That formula could not be read: ' + got.err + '.</strong> '
        + 'Try <code>2x + 3</code>, <code>x^2</code> or <code>1/x</code>.');
      return;
    }
    var tree = got.tree, poly = Epoly(tree, 'x'), rat = Erat(tree, 'x');
    var fn = function (x) { return evalAt(tree, x, 'x'); };

    /* One-to-one, decided rather than assumed. For a polynomial the search is
       exact: f(x) - f(c) is a polynomial whose OTHER rational roots are inputs
       that collide with c. */
    var collide = null, restriction = null;
    if (poly && Pdeg(poly) === 0) {
      /* A constant is the extreme case: EVERY pair of inputs collides, so no
         search is needed and none is claimed. */
      collide = { a: R0, b: R1, value: poly.length ? poly[0] : R0, constant: true };
    } else if (poly) {
      for (var c = -3; c <= 3 && !collide; c += 1) {
        var cr = R(BigInt(c));
        var shifted = Psub(poly, [Peval(poly, cr)]);
        var roots = Prationalroots(shifted);
        for (var i = 0; i < roots.length && !collide; i += 1) {
          if (!Requ(roots[i], cr) && Rzero(Peval(shifted, roots[i]))) {
            collide = { a: cr, b: roots[i], value: Peval(poly, cr) };
          }
        }
      }
      if (Pdeg(poly) === 2) {
        var h = Rdiv(Rneg(poly[1]), Rmul(R(2n), poly[2]));
        restriction = { at: h, text: 'x >= ' + Rtext(h),
                        why: 'the vertex is at x = ' + Rtext(h) + ', and the parabola is a mirror '
                             + 'image about that line' };
      }
    }

    /* The inverse formula, derived where a derivation exists. */
    var invText = null, invWhy = null;
    if (poly && Pdeg(poly) === 1) {
      var m = poly[1], b0 = poly[0];
      invText = ratformula([Rneg(b0), R1], [m]);
      invWhy = 'swap x and y in y = ' + Ptext(poly) + ', giving x = ' + Ptext(poly, 'y')
        + ', then solve that for y';
    } else if (poly && Pdeg(poly) === 2) {
      var a2 = poly[2], h2 = Rdiv(Rneg(poly[1]), Rmul(R(2n), a2)), k2 = Peval(poly, h2);
      var innerQ = ratformula([Rneg(k2), R1], [a2]);
      invText = (Rzero(h2) ? '' : Rtext(h2) + ' + ') + 'sqrt(' + innerQ + ')';
      invWhy = 'complete the square: y = ' + coeftext(a2) + '(' + shifttext(h2, 'x') + ')^2'
        + (Rzero(k2) ? '' : (Rsign(k2) > 0 ? ' + ' + Rtext(k2) : ' - ' + Rtext(Rabs(k2))))
        + ', then swap x and y and solve. The +- that appears becomes a + because of the '
        + 'restriction below &mdash; and choosing which sign to keep IS the restriction.';
    } else if (poly && Pdeg(poly) === 3 && Rzero(poly[1]) && Rzero(poly[2])) {
      var a3 = poly[3], d3 = poly[0];
      invText = 'cbrt(' + ratformula([Rneg(d3), R1], [a3]) + ')';
      invWhy = 'swap and solve: every real number has exactly one real cube root, so no +- appears '
        + 'and no restriction is needed';
    } else if (rat) {
      var red = ratreduce(rat);
      if (red && Pdeg(red.n) <= 1 && Pdeg(red.d) <= 1 && Pdeg(red.d) + Pdeg(red.n) >= 1) {
        var pn = red.n.length > 1 ? red.n[1] : R0, qn = red.n.length ? red.n[0] : R0;
        var rd = red.d.length > 1 ? red.d[1] : R0, sd = red.d.length ? red.d[0] : R0;
        if (!Rzero(rd) && !Rzero(Rsub(Rmul(pn, sd), Rmul(qn, rd)))) {
          invText = ratformula([Rneg(qn), sd], [pn, Rneg(rd)]);
          invWhy = 'swap x and y, giving x = ' + ratformula(red.n, red.d, 'y')
            + ', multiply both sides by the denominator, and collect the y terms on one side';
        }
      }
    }
    var invGot = invText ? parse(invText) : { tree: null, err: null };

    /* The picture: f, the line y = x, and the reflection of f in it. The
       reflection is drawn from the sampled graph, so it exists even when no
       formula for it can be written down. */
    var half = 6;
    var plot = Plot(svg, { xmin: -half, xmax: half, ymin: -half, ymax: half });
    plot.frame();
    plot.segment(-half, -half, half, half, 'plot-aux');
    plot.curve(fn, 'plot-curve');
    var kept = [], dropped = [];
    for (var t = -half; t <= half + 0.001; t += 0.05) {
      var y = fn(t);
      var point = [y, t];
      /* Which half of the reflection to keep is a drawing decision, so it is
         taken in floating point; the restriction ITSELF is the exact rational
         printed beside the graph. */
      if (restriction && t < Rnum(restriction.at)) {
        dropped.push(point); kept.push(null);
      } else {
        kept.push(point); dropped.push(null);
      }
    }
    trace(plot, dropped, 'plot-curve parent');
    trace(plot, kept, 'plot-curve alt');
    if (invGot.tree) {
      plot.curve(function (x) { return evalAt(invGot.tree, x, 'x'); }, 'plot-curve good');
    }
    plot.describe('f in the first colour, the dashed line y = x, and f reflected in it.');

    titleOut.textContent = 'f(x) = ' + body;
    subOut.textContent = invText ? 'inverse: ' + invText : 'no inverse formula was derived';
    kA.textContent = collide ? 'no' : (poly ? 'no collision found' : 'not decided');
    kB.textContent = invText ? invText : 'none derived';
    kC.textContent = restriction ? restriction.text : (collide ? 'needed, but not derived' : 'none needed');

    var blocks = [table('Is there an inverse at all?', [
      row('one-to-one?', collide
        ? chip('no', 'no') + (collide.constant
            ? ' every input gives ' + Rtext(collide.value) + '; f(0) and f(1) are two of infinitely '
              + 'many pairs that collide'
            : ' f(' + Rtext(collide.a) + ') = f(' + Rtext(collide.b) + ') = '
              + Rtext(collide.value) + ', so an inverse would have to send ' + Rtext(collide.value)
              + ' back to two different places')
        : (poly
           ? chip('no collision found', 'hi') + ' for each whole number c from -3 to 3 the lab solved '
             + 'f(x) = f(c) exactly and found no second solution. That is a real search, but it is '
             + 'still only seven of them'
           : chip('not decided', 'hi') + ' the collision search solves f(x) = f(c) with the rational '
             + 'root theorem, which needs a polynomial; this formula is not one, so no search was run')),
      row('the restriction', restriction
        ? 'keep ' + restriction.text + ': ' + restriction.why
        : (collide
           ? (collide.constant
              ? 'no restriction to more than one input can help: every input has the same image'
              : 'a restriction is needed here, and this lab derives one only for quadratics')
           : 'none needed on the part shown')),
      row('the reflection', 'the second curve above is f reflected in y = x, point by point: every '
        + '(t, f(t)) redrawn as (f(t), t). That reflection exists whether or not a formula for it can '
        + 'be written down'
        + (restriction ? ', and the dashed half is the part the restriction throws away.' : '.')),
    ])];

    if (invText) {
      var checks = [];
      [R(2n), R(3n), R(-1n)].forEach(function (cv) {
        var y = Eexact(tree, cv, 'x');
        if (y === null || !invGot.tree) return;
        var back = Eexact(invGot.tree, y, 'x');
        if (back === null) return;
        var outside = restriction && Rcmp(cv, restriction.at) < 0;
        checks.push(row('f(' + Rtext(cv) + ') = ' + Rtext(y) + ', then back',
          'f-inverse(' + Rtext(y) + ') = ' + Rtext(back) + '  '
          + (Requ(back, cv)
             ? chip('returns ' + Rtext(cv), 'ok')
             : (outside
                ? chip('lands on ' + Rtext(back) + ', not ' + Rtext(cv), 'hi')
                  + ' &mdash; ' + Rtext(cv) + ' is outside the restriction ' + restriction.text
                  + ', so it is not in the restricted function\'s domain and nothing sends it back. '
                  + 'This row is the restriction doing its job, not the inverse failing'
                : chip('does not return ' + Rtext(cv), 'no')))));
      });
      if (!checks.length) checks.push(row('the round trip', 'no whole-number input gave an exact value '
        + 'on the way back, so the check was not run'));
      blocks.push(table('The inverse, derived and then checked by round trip', [
        row('the derivation', invWhy),
        row('f-inverse(x)', invText),
      ].concat(checks)));
    } else {
      blocks.push(table('No formula was derived', [
        row('why', collide && poly && Pdeg(poly) === 0
          ? 'a constant function sends every input to the same output, so nothing can undo it'
          : 'this lab derives inverse formulas for lines, quadratics, pure cubes and quotients of '
            + 'linear pieces. The reflection is still drawn above, because reflecting a graph needs '
            + 'no formula.'),
        row('what to do', collide && collide.constant
          ? 'nothing repairs a constant function. Swapping x and y here gives x = ' + Rtext(collide.value)
            + ', which is a vertical line and not a function of x at all &mdash; the reflection above '
            + 'is that line'
          : 'swap x and y and solve for y by hand; every step you take is a step this lab would have '
            + 'to take too'),
      ]));
    }
    work.innerHTML = blocks.join('');

    status.innerHTML = collide
      ? '<strong>f is not one-to-one, so it has no inverse as it stands.</strong> '
        + (collide.constant
           ? 'It is a constant: every input is sent to ' + Rtext(collide.value) + ', so the output '
             + 'carries no information at all about the input. No restriction repairs this &mdash; '
             + 'restricting to a single input would work, and a function on one point is not what '
             + 'anybody wants. This is the far end of the same problem the parabola has.'
           : 'f(' + Rtext(collide.a) + ') and f(' + Rtext(collide.b) + ') are both '
             + Rtext(collide.value) + ' &mdash; found by solving f(x) = ' + Rtext(collide.value)
             + ' exactly, not by looking. ')
        + (restriction
           ? 'Restrict the domain to ' + restriction.text + ' and it becomes one-to-one: ' + restriction.why
             + '. The inverse of the restricted function is ' + (invText || 'the reflected curve above')
             + ', and the dashed half of the reflection is what the restriction discards.'
           : (collide.constant ? ''
              : 'Some restriction of the domain would fix it, but this lab derives one only for '
                + 'quadratics, where the vertex says exactly where to cut.'))
      : '<strong>' + (invText
          ? 'The inverse is f-inverse(x) = ' + invText + '.'
          : 'No collision was found, so an inverse should exist.')
        + '</strong> '
        + (invText
           ? 'It was derived by swapping x and y and solving, then CHECKED by sending numbers through '
             + 'f and back &mdash; the round trip above returns each one. On the picture, the inverse '
             + 'is f reflected in the dashed line y = x, which is what swapping x and y means '
             + 'geometrically.'
           : 'The reflection above is that inverse; writing a formula for it needs a step this lab '
             + 'does not take for this shape.');
  }

  /* ----------------------------------------------------------- dispatch */
  function redraw() {
    var raw = inMain.value, body = bodyof(raw);
    if (MODE === 'definition') { runDefinition(raw); return; }
    if (MODE === 'piecewise') { runPiecewise(raw); return; }
    if (!body) {
      blank('<strong>The box is empty.</strong> Type a formula in x, or choose one of the examples '
        + 'above &mdash; every number on this page is computed from what is in that box.');
      return;
    }
    if (MODE === 'notation') { runNotation(body); return; }
    if (MODE === 'domain') { runDomain(body); return; }
    if (MODE === 'inverse') { runInverse(body); return; }
    if (MODE === 'compose') {
      var g = bodyof(inAux.value);
      if (!g) {
        blank('<strong>g(x) is empty.</strong> Composition needs both functions: type a formula for '
          + 'g, such as <code>x - 4</code>, and the lab will compose them both ways round.');
        return;
      }
      runCompose(body, g);
      return;
    }
    blank('<strong>Nothing to show.</strong>');
  }

  preset.addEventListener('change', function () {
    var value = preset.value;
    if (MODE === 'compose') {
      var parts = value.split('|');
      inMain.value = parts[0];
      inAux.value = parts.length > 1 ? parts[1] : '';
    } else {
      inMain.value = value;
    }
    redraw();
  });
  inMain.addEventListener('input', redraw);
/*BINDINGS*/
  var startValue = preset.value;
  if (MODE === 'compose') {
    var firstParts = startValue.split('|');
    inMain.value = firstParts[0];
    inAux.value = firstParts.length > 1 ? firstParts[1] : '';
  } else {
    inMain.value = startValue;
  }
  redraw();
  window.redrawLab = redraw;
"""
