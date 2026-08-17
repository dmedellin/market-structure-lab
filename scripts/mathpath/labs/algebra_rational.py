"""Course 5 and the arrival of Course 6: rational expressions, and complex numbers.

Two labs live here because they share one decision, and the decision is the
whole teaching point of both:

  A RATIONAL EXPRESSION IS NOT ITS SIMPLIFIED FORM, AND A ROOT IS NOT ITS
  DECIMAL. Both labs keep the object the reader actually wrote and refuse to
  replace it with something that merely agrees with it in most places.

For `rationalfn` that means the rational function is carried as an UNREDUCED
pair of polynomials, together with the list of every polynomial the expression
divided by, collected while the reader's text is parsed. Cancelling happens
only when a lesson asks for it, and never before the domain has been read off
the denominators AS WRITTEN. That ordering is not a stylistic preference: once
(x^2 - 4)/(x - 2) has become x + 2 there is nothing left in the formula that
knows x = 2 was ever forbidden, and every lab on this course would be quietly
lying from that moment on. The hole in the graph is drawn from the same list.

For `complex` it means the real and imaginary parts are exact rationals, so
(1 + 2i)/(3 - i) is 1/10 + 7/10 i and not 0.1 + 0.7i, and the roots of a
quadratic with a negative discriminant are carried as p +- q*sqrt(k) i with p
and q exact and k a squarefree integer -- then multiplied back together to
recover the quadratic they came from. That multiplication is the proof, and it
is computed rather than asserted: the sum and product of the conjugate pair are
2p and p^2 + q^2 k, both rational, both compared against -b/a and c/a which are
formed independently from the coefficients the reader typed.

Floating point appears in exactly three places, all of them declared to the
reader where they happen: pixel coordinates in the grapher and the Argand
plane, the decimal shown beside an irrational solution, and the numeric
re-check of an irrational solution in `solve` mode. Every verdict -- in the
domain or not, extraneous or not, asymptote or hole, equal or not -- comes from
the exact side.
"""

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# --------------------------------------------------------------------------
# The rational-function layer.
#
# POLY_JS gives exact polynomials over Q. A rational function is a pair of
# them, and the only thing worth being careful about is WHEN they are allowed
# to cancel -- so nothing here cancels unless the caller asks by name.
# --------------------------------------------------------------------------

RF_JS = r"""
  /* ---- rational functions over Q ----

     { n: poly, d: poly } with NOTHING cancelled, ever, on construction. Two
     rational functions that are equal as functions on their common domain can
     have different n and d here, and that difference is exactly the subject of
     this course: (x^2 - 4)/(x - 2) and (x + 2) are the same rule at every x
     except one, and the one is the lesson. */
  function RFnew(n, d) { return { n: Pnorm(n), d: Pnorm(d) }; }
  function RFadd(a, b) { return RFnew(Padd(Pmul(a.n, b.d), Pmul(b.n, a.d)), Pmul(a.d, b.d)); }
  function RFsub(a, b) { return RFnew(Psub(Pmul(a.n, b.d), Pmul(b.n, a.d)), Pmul(a.d, b.d)); }
  function RFmul(a, b) { return RFnew(Pmul(a.n, b.n), Pmul(a.d, b.d)); }
  function RFdiv(a, b) { return RFnew(Pmul(a.n, b.d), Pmul(a.d, b.n)); }
  function RFneg(a) { return RFnew(Pscale(a.n, R(-1n)), a.d); }
  function RFconst(r) { return RFnew(Rzero(r) ? [] : [r], [R1]); }

  /* Clear the denominators of the coefficients and divide out the integer
     content of BOTH polynomials at once, then force the leading coefficient of
     the bottom positive. (x + 1)/(2x) rather than ((1/2)x + 1/2)/x, which is
     the same function written in a form no reader would hand in. */
  function RFint(n, d) {
    n = Pnorm(n); d = Pnorm(d);
    if (!n.length) return { n: [], d: [R1] };
    var den = 1n;
    n.concat(d).forEach(function (c) { den = den * c.d / bgcd(den, c.d); });
    var ni = n.map(function (c) { return c.n * (den / c.d); });
    var di = d.map(function (c) { return c.n * (den / c.d); });
    var g = 0n;
    ni.concat(di).forEach(function (v) { g = bgcd(g, v); });
    if (g === 0n) g = 1n;
    if (di[di.length - 1] < 0n) g = -g;
    return {
      n: ni.map(function (v) { return R(v / g); }),
      d: di.map(function (v) { return R(v / g); })
    };
  }
  /* Reduce to lowest terms. The polynomial gcd is SEARCHED for by Euclid's
     algorithm on polynomials, not matched against a table of patterns, so it
     finds the common factor of (x^3 - x) and (x^2 - 2x + 1) for the same
     reason it finds the common factor of 12 and 18. */
  function RFreduce(rf) {
    if (Pzero(rf.n)) return { rf: { n: [], d: [R1] }, gcd: [R1], cancelled: false };
    var g = Pgcd(rf.n, rf.d);
    var n = rf.n, d = rf.d, cancelled = false;
    if (Pdeg(g) > 0) { n = Pdivmod(n, g).q; d = Pdivmod(d, g).q; cancelled = true; }
    var out = RFint(n, d);
    return { rf: out, gcd: g, cancelled: cancelled };
  }
  function RFeq(a, b) { return Pzero(Psub(Pmul(a.n, b.d), Pmul(b.n, a.d))); }

  /* Is there a top-level + or - outside every bracket? That is the only case
     where a fraction's numerator or denominator needs wrapping. */
  function toplevelsum(t) {
    var depth = 0;
    for (var i = 0; i < t.length; i += 1) {
      var c = t.charAt(i);
      if (c === '(') depth += 1;
      else if (c === ')') depth -= 1;
      else if (depth === 0 && (c === '+' || c === '-') && i > 0 && t.charAt(i - 1) === ' ') return true;
    }
    return false;
  }
  function grouptext(t) { return toplevelsum(t) ? '(' + t + ')' : t; }
  /* A denominator is bracketed unless it is a single unmistakable token. "2x"
     written after a slash is not 2x: (x + 2)/2x reads as ((x + 2)/2)x to
     anyone applying the precedence rules the rest of the course insists on. */
  function denomtext(t) {
    return (/^[0-9]+$/.test(t) || /^[A-Za-z](\^[0-9]+)?$/.test(t)) ? t : '(' + t + ')';
  }
  function RFtext(rf, v) {
    if (Pzero(rf.n)) return '0';
    if (Pdeg(rf.d) === 0 && Requ(rf.d[0], R1)) return Ptext(rf.n, v);
    return grouptext(Ptext(rf.n, v)) + '/' + denomtext(Ptext(rf.d, v));
  }
  /* Factored, top and bottom. Square brackets rather than round ones because
     the factors already carry round brackets, and [(x+2)(x-2)] / [(x+3)(x-3)]
     is the only form of this that cannot be misread. */
  function RFfactortext(rf, v) {
    if (Pzero(rf.n)) return '0';
    var top = Pfactortextfull(rf.n, v);
    if (Pdeg(rf.d) === 0 && Requ(rf.d[0], R1)) return top;
    return '[' + top + '] / [' + Pfactortextfull(rf.d, v) + ']';
  }
  /* The least common multiple, as a polynomial: ab/gcd(a, b). Keeping the
     integer content (rather than taking the primitive part) is deliberate --
     the LCD of 2x and 3x has to be 6x if the multipliers the lesson writes
     down, 3 and 2, are going to be whole numbers. */
  function Plcm(a, b) {
    if (Pzero(a) || Pzero(b)) return [];
    var l = Pdivmod(Pmul(a, b), Pgcd(a, b)).q;
    if (Rsign(Plead(l)) < 0) l = Pscale(l, R(-1n));
    return l;
  }

  /* ---- the reader's text, as a rational function ----

     Two things come back, and the SECOND one is what this course is about:
       rf    the rational function, with nothing cancelled,
       bans  every polynomial the expression divided by, in the order it
             divided by them.
     `bans` cannot be recovered from `rf`. In 1/(1/x) the final denominator is
     1, and yet x = 0 is not in the domain; the ban list is the only place that
     survives. */
  function ErfBuild(node, v, bans) {
    var a, b, e, k;
    switch (node.k) {
      case 'num': {
        var r = Rparse(node.v);
        if (r === null) throw new Error('"' + node.v + '" is not a number this lab can hold exactly');
        return RFconst(r);
      }
      case 'var':
        if (node.v !== v) throw new Error('this lab works in one variable, ' + v + ', and found "' + node.v + '"');
        return RFnew([R0, R1], [R1]);
      case 'neg': return RFneg(ErfBuild(node.a, v, bans));
      case 'add': return RFadd(ErfBuild(node.a, v, bans), ErfBuild(node.b, v, bans));
      case 'sub': return RFsub(ErfBuild(node.a, v, bans), ErfBuild(node.b, v, bans));
      case 'mul': return RFmul(ErfBuild(node.a, v, bans), ErfBuild(node.b, v, bans));
      case 'div': {
        a = ErfBuild(node.a, v, bans); b = ErfBuild(node.b, v, bans);
        if (Pzero(b.n)) throw new Error('it divides by 0');
        bans.push(b.n);
        return RFdiv(a, b);
      }
      case 'pow': {
        a = ErfBuild(node.a, v, bans);
        b = ErfBuild(node.b, v, bans);
        if (Pdeg(b.n) > 0 || Pdeg(b.d) > 0) throw new Error('an exponent has to be a constant whole number here');
        e = Pzero(b.n) ? R0 : Rdiv(b.n[0], b.d.length ? b.d[0] : R1);
        if (!Rint(e) || e.n > 24n || e.n < -24n) throw new Error('an exponent has to be a whole number between -24 and 24 here');
        k = Number(e.n);
        if (k < 0) {
          if (Pzero(a.n)) throw new Error('it raises 0 to a negative power, which divides by 0');
          bans.push(a.n);
          return RFnew(Ppow(a.d, -k), Ppow(a.n, -k));
        }
        return RFnew(Ppow(a.n, k), Ppow(a.d, k));
      }
      case 'fn': throw new Error('"' + node.v + '(...)" is not a rational expression');
    }
    throw new Error('this is not a rational expression');
  }

  /* Substitution into the expression AS THE READER WROTE IT, in exact
     rationals. null means "undefined there", which is precisely what an
     extraneous solution does and precisely what the cleared equation can no
     longer tell you. Every check in solve mode runs through this, on the
     original tree, not on the tidied-up fraction. */
  function Eexact(node, v, x) {
    var a, b, k;
    switch (node.k) {
      case 'num': return Rparse(node.v);
      case 'var': return node.v === v ? x : null;
      case 'neg': a = Eexact(node.a, v, x); return a === null ? null : Rneg(a);
      case 'add': a = Eexact(node.a, v, x); b = Eexact(node.b, v, x); return (a === null || b === null) ? null : Radd(a, b);
      case 'sub': a = Eexact(node.a, v, x); b = Eexact(node.b, v, x); return (a === null || b === null) ? null : Rsub(a, b);
      case 'mul': a = Eexact(node.a, v, x); b = Eexact(node.b, v, x); return (a === null || b === null) ? null : Rmul(a, b);
      case 'div':
        a = Eexact(node.a, v, x); b = Eexact(node.b, v, x);
        return (a === null || b === null || Rzero(b)) ? null : Rdiv(a, b);
      case 'pow':
        a = Eexact(node.a, v, x); b = Eexact(node.b, v, x);
        if (a === null || b === null || !Rint(b) || b.n > 24n || b.n < -24n) return null;
        k = Number(b.n);
        if (k < 0 && Rzero(a)) return null;
        return Rpow(a, k);
      case 'fn': return null;
    }
    return null;
  }

  /* ---- where a polynomial is zero ----

     Rational zeros are named exactly, by the rational root search. A quadratic
     left over from that search is solved exactly and gives a conjugate surd
     pair or none at all. Anything of higher degree with no rational root is
     REPORTED as such: a lab that listed the rational exclusions and went quiet
     about the rest would be telling the reader a domain that is too big. */
  function zerosOf(poly) {
    var out = { rat: [], surd: [], unknown: null, nozero: null };
    if (Pdeg(poly) < 1) return out;
    var f = Pfactor(poly);
    f.factors.forEach(function (item) { out.rat.push(item.root); });
    if (f.rest.length) {
      if (Pdeg(f.rest) === 2) {
        var q = quadroots(f.rest[2], f.rest[1], f.rest[0]);
        if (q.kind === 'complex') out.nozero = f.rest;
        else out.surd.push({ p: q.p, s: q.s, min: Pmonic(f.rest), poly: f.rest });
      } else {
        out.unknown = f.rest;
      }
    }
    return out;
  }
  /* The union over every banned polynomial, de-duplicated. */
  function exclusionsOf(bans) {
    var rat = [], rseen = {}, surd = [], sseen = {}, unknown = [], nozero = [];
    bans.forEach(function (p) {
      if (Pdeg(p) < 1) return;
      var z = zerosOf(p);
      z.rat.forEach(function (r) { var k = Rtext(r); if (!rseen[k]) { rseen[k] = 1; rat.push(r); } });
      z.surd.forEach(function (s) { var k = Ptext(s.min); if (!sseen[k]) { sseen[k] = 1; surd.push(s); } });
      if (z.unknown) unknown.push(z.unknown);
      if (z.nozero) nozero.push(z.nozero);
    });
    rat.sort(Rcmp);
    return { rat: rat, surd: surd, unknown: unknown, nozero: nozero };
  }
  function excount(ex) {
    if (ex.unknown.length) return 'at least ' + (ex.rat.length + 2 * ex.surd.length);
    return String(ex.rat.length + 2 * ex.surd.length);
  }
  function extext(ex) {
    var parts = ex.rat.map(Rtext);
    ex.surd.forEach(function (s) { parts.push(pmtext(s.p, s.s)); });
    ex.unknown.forEach(function (p) {
      parts.push('the real zeros of ' + Pfactortext(p) + ', which are not rational and are not named here');
    });
    if (!parts.length) return 'none';
    return parts.join(', ');
  }
  /* Every excluded value as a floating-point coordinate, for drawing only. */
  function exfloats(ex) {
    var out = ex.rat.map(Rnum);
    ex.surd.forEach(function (s) {
      var sv = Rnum(s.s.q) * Math.sqrt(Number(s.s.k));
      out.push(Rnum(s.p) + sv, Rnum(s.p) - sv);
    });
    out.sort(function (a, b) { return a - b; });
    return out;
  }
  /* Numeric evaluation of a reduced rational function, for pixels. */
  function RFnumeric(rf) {
    var nn = rf.n.map(Rnum), dd = rf.d.map(Rnum);
    return function (x) {
      var num = 0, den = 0, i;
      for (i = nn.length - 1; i >= 0; i -= 1) num = num * x + nn[i];
      for (i = dd.length - 1; i >= 0; i -= 1) den = den * x + dd[i];
      if (den === 0) return NaN;
      return num / den;
    };
  }
"""


# --------------------------------------------------------------------------
# Lab 1: rational expressions.
# --------------------------------------------------------------------------

# Each preset is (label, first expression, second expression, operation). The
# second and the operation are ignored by the modes that take one expression.
# The presets are chosen to break things on purpose: the fraction that cancels
# to a polynomial and is still undefined somewhere, the division whose new
# exclusion comes from the DIVISOR'S NUMERATOR, the equation whose only
# candidate is extraneous, the denominator with no rational zero at all.
RF_PRESETS = {
    "domain": [
        ("(x^2 - 4)/(x - 2)          one exclusion, and simplifying hides it", "(x^2 - 4)/(x - 2)", "", "mul"),
        ("(x + 1)/(x^2 - 5x + 6)     two exclusions", "(x + 1)/(x^2 - 5x + 6)", "", "mul"),
        ("(x + 3)/(x^3 - x)          three exclusions", "(x + 3)/(x^3 - x)", "", "mul"),
        ("1/(1/x - 1/2)              an exclusion with no denominator to blame", "1/(1/x - 1/2)", "", "mul"),
        ("1/(x^2 + 1)                nothing is excluded", "1/(x^2 + 1)", "", "mul"),
        ("1/(x^2 - 2)                the exclusions are not rational", "1/(x^2 - 2)", "", "mul"),
    ],
    "simplify": [
        ("(x^2 - 4)/(x - 2)          cancels completely", "(x^2 - 4)/(x - 2)", "", "mul"),
        ("(x^2 - 9)/(x^2 + 6x + 9)   cancels once, and once is not enough", "(x^2 - 9)/(x^2 + 6x + 9)", "", "mul"),
        ("(2 - x)/(x^2 - 4)          the sign that goes missing", "(2 - x)/(x^2 - 4)", "", "mul"),
        ("(x^2 + 4)/(x^2 + 2x)       nothing cancels", "(x^2 + 4)/(x^2 + 2x)", "", "mul"),
        ("(x + 3)/(x^2 + 3x)         the answer keeps none of the evidence", "(x + 3)/(x^2 + 3x)", "", "mul"),
        ("(x^3 - x)/(x^2 - 2x + 1)   a repeated factor on the bottom", "(x^3 - x)/(x^2 - 2x + 1)", "", "mul"),
    ],
    "multiply": [
        ("divide: the exclusion comes from the DIVISOR'S TOP", "(x^2 - 4)/(x^2 - 9)", "(x - 2)/(x + 3)", "div"),
        ("multiply: everything cancels but the domain", "(x^2 - 1)/x", "x/(x - 1)", "mul"),
        ("divide: the answer is the constant 1", "(x^2 + x)/(x^2 - 1)", "x/(x - 1)", "div"),
        ("multiply: a repeated factor survives", "(x + 1)/(x^2 - 1)", "(x - 1)/(x^2 + 2x + 1)", "mul"),
        ("divide: the numbers cancel too", "3/(x - 2)", "6/(x^2 - 4)", "div"),
        ("divide by 0: the move that is never legal", "(x + 2)/(x - 1)", "0", "div"),
    ],
    "add": [
        ("the LCD is not the product", "1/(x^2 - 1)", "1/(x + 1)", "add"),
        ("subtract: the answer is 1, except where it is nothing", "x/(x - 2)", "2/(x - 2)", "sub"),
        ("the LCD IS the product", "1/x", "1/(x + 1)", "add"),
        ("subtract: the minus sign hits every term", "3x/(x^2 - 9)", "1/(x - 3)", "sub"),
        ("subtract: the answer is 0 and still has a hole", "1/(x - 1)", "1/(x - 1)", "sub"),
        ("add: the sum cancels a factor neither term had alone", "1/(x^2 + x)", "1/(x^2 - x)", "add"),
    ],
    "complex": [
        ("(1 + 2/x)/(1 - 4/x^2)", "(1 + 2/x)/(1 - 4/x^2)", "", "mul"),
        ("(1/x - 1/2)/(x - 2)", "(1/x - 1/2)/(x - 2)", "", "mul"),
        ("(1/(x + 1) + 1)/(1/(x + 1) - 1)", "(1/(x + 1) + 1)/(1/(x + 1) - 1)", "", "mul"),
        ("(1/x)/(1/x - 1/2)", "(1/x)/(1/x - 1/2)", "", "mul"),
        ("(1 + 1/x)/(1 + 1/x)        equal to 1, and undefined twice", "(1 + 1/x)/(1 + 1/x)", "", "mul"),
        ("(1/2 + 1/3)/(1/4)          the same method, on numbers", "(1/2 + 1/3)/(1/4)", "", "mul"),
    ],
    "solve": [
        ("the only candidate is extraneous", "x/(x - 2)", "2/(x - 2)", "mul"),
        ("one candidate survives, one does not", "x^2/(x - 1)", "1/(x - 1)", "mul"),
        ("the cancelled factor comes back to bite", "(x^2 - 4)/(x - 2)", "4", "mul"),
        ("a clean solution, checked anyway", "1/x + 1/2", "3/4", "mul"),
        ("no real solution at all", "x + 1/x", "1", "mul"),
        ("two irrational solutions, both genuine", "x + 1/x", "3", "mul"),
    ],
    "graph": [
        ("1/x                        the archetype", "1/x", "", "mul"),
        ("(x^2 - 4)/(x - 2)          a hole and no asymptote", "(x^2 - 4)/(x - 2)", "", "mul"),
        ("(2x + 1)/(x - 3)           equal degrees", "(2x + 1)/(x - 3)", "", "mul"),
        ("(x^2 - 1)/(x^2 - 4)        two asymptotes, two intercepts", "(x^2 - 1)/(x^2 - 4)", "", "mul"),
        ("(x^2 + 1)/(x - 1)          the asymptote is a slope", "(x^2 + 1)/(x - 1)", "", "mul"),
        ("1/(x^2 + 1)                no vertical asymptote at all", "1/(x^2 + 1)", "", "mul"),
    ],
}

RF_TITLES = {
    "domain": ("The domain, before anything else",
               "Every denominator, set to zero, while it is still there to set"),
    "simplify": ("Cancelling factors",
                 "The common factor found by Euclid, not by pattern-matching"),
    "multiply": ("Multiplying and dividing",
                 "Invert and multiply, and the exclusion that move creates"),
    "add": ("Adding and subtracting",
            "The least common denominator, and the minus sign that hits every term"),
    "complex": ("Complex fractions",
                "Two methods, computed separately, meeting at the same answer"),
    "solve": ("Rational equations, and the check",
              "Clear the denominators, solve, then substitute into the ORIGINAL"),
    "graph": ("Reading a rational graph",
              "Vertical asymptotes, holes and end behaviour, all from the factors"),
}

# Which controls each mode declares. A mode that does not use the second
# expression does not render it, so no lab ever reads an id that is not on its
# own page -- and no wrapper is ever found by walking up from a child.
RF_TWO = ("multiply", "add", "solve")
RF_OPS = {
    "multiply": [("mul", "multiply  (x)"), ("div", "divide  (/)")],
    "add": [("add", "add  (+)"), ("sub", "subtract  (-)")],
}
RF_STAGE = ("domain", "solve", "graph")

RF_LEGENDS = {
    "domain": '<span class="tone-cyan"><i class="legend-swatch"></i>the domain</span>'
              '<span class="tone-red"><i class="legend-swatch"></i>excluded values</span>',
    "solve": '<span class="tone-green"><i class="legend-swatch"></i>verified solution</span>'
             '<span class="tone-red"><i class="legend-swatch"></i>extraneous or excluded</span>',
    "graph": '<span class="tone-cyan"><i class="legend-swatch"></i>the curve</span>'
             '<span class="tone-red"><i class="legend-swatch"></i>asymptotes</span>'
             '<span class="tone-amber"><i class="legend-swatch"></i>intercepts</span>'
             '<span class="tone-muted"><i class="legend-swatch"></i>holes</span>',
}

RF_LABELS = {
    "domain": ("Expression", ""),
    "simplify": ("Expression", ""),
    "multiply": ("First expression", "Second expression"),
    "add": ("First expression", "Second expression"),
    "complex": ("Complex fraction  (top)/(bottom)", ""),
    "solve": ("Left side of the equation", "Right side of the equation"),
    "graph": ("Expression", ""),
}


RF_SCRIPT = r"""
  var MODE = '__MODE__', HASB = __HASB__, HASOP = __HASOP__, HASSTAGE = __HASSTAGE__;
  var LABEL_A = '__LABELA__', LABEL_B = '__LABELB__';

  var preset = document.getElementById('rfPreset');
  var inA = document.getElementById('rfExprA');
  var inB = HASB ? document.getElementById('rfExprB') : null;
  var opSel = HASOP ? document.getElementById('rfOp') : null;
  var labelB = HASB ? document.getElementById('rfLabelB') : null;
  var work = document.getElementById('rfWork');
  var status = document.getElementById('rfStatus');
  var titleOut = document.getElementById('rfTitle');
  var subOut = document.getElementById('rfSub');
  var svg = HASSTAGE ? document.getElementById('rfPlot') : null;
  var kval = [document.getElementById('rfK1'), document.getElementById('rfK2'), document.getElementById('rfK3')];
  var klab = [document.getElementById('rfK1Lab'), document.getElementById('rfK2Lab'), document.getElementById('rfK3Lab')];

  function row(label, detail) {
    return '<tr><th class="rowhead">' + label + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function focusrow(label, detail) {
    return '<tr class="focus"><th class="rowhead">' + label + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function table(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption
      + '</caption><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  function chip(kind, text) { return '<span class="chip ' + kind + '">' + text + '</span>'; }
  function setkpi(list) {
    for (var i = 0; i < 3; i += 1) {
      klab[i].textContent = list[i][0];
      kval[i].textContent = list[i][1];
    }
  }

  /* Bad input is answered, never thrown and never left blank. Every message
     below names the thing that went wrong and shows a form that works. */
  function readExpr(text, label) {
    var s = String(text === undefined || text === null ? '' : text).trim();
    if (!s) {
      return { ok: false, msg: '<strong>' + label + ' is empty.</strong> Type a rational expression in x '
        + '&mdash; something like <code>(x^2 - 4)/(x - 2)</code>, <code>1/x + 1/2</code> or '
        + '<code>3/(x - 1)</code>. Implicit multiplication is fine: <code>2x</code> and '
        + '<code>(x+1)(x-2)</code> both parse.' };
    }
    var tree;
    try { tree = Eparse(s); }
    catch (err) {
      return { ok: false, msg: '<strong>' + label + ' could not be read: ' + err.message + '.</strong> '
        + 'Check the brackets match and that every operator has something on both sides. '
        + 'The parser accepts + - * / ^ and implicit multiplication, in the single variable x.' };
    }
    var bans = [];
    try {
      var rf = ErfBuild(tree, 'x', bans);
      return { ok: true, src: s, tree: tree, rf: rf, bans: bans };
    } catch (err) {
      return { ok: false, msg: '<strong>' + label + ': ' + err.message + '.</strong> '
        + 'This lab holds every coefficient as an exact fraction, so it needs a ratio of '
        + 'polynomials in x &mdash; no roots, logarithms or second variables.' };
    }
  }

  function hiddenExclusions(ex, rf) {
    var rat = [], surd = [];
    ex.rat.forEach(function (r) { if (!Rzero(Peval(rf.d, r))) rat.push(r); });
    ex.surd.forEach(function (s) { if (!Pzero(Pdivmod(rf.d, s.min).r)) surd.push(s); });
    return { rat: rat, surd: surd, count: rat.length + 2 * surd.length };
  }
  function hiddentext(h) {
    var parts = h.rat.map(Rtext);
    h.surd.forEach(function (s) { parts.push(pmtext(s.p, s.s)); });
    return parts.length ? parts.join(', ') : 'none';
  }
  function domaintext(ex) {
    if (!ex.rat.length && !ex.surd.length && !ex.unknown.length) return 'every real number';
    return 'every real x except ' + extext(ex);
  }
  function intervaltext(ex) {
    if (ex.surd.length || ex.unknown.length) return '';
    var pts = ex.rat.map(Rtext);
    if (!pts.length) return '(-inf, inf)';
    var out = '(-inf, ' + pts[0] + ')';
    for (var i = 1; i < pts.length; i += 1) out += ' U (' + pts[i - 1] + ', ' + pts[i] + ')';
    return out + ' U (' + pts[pts.length - 1] + ', inf)';
  }
  /* The distinct denominators that can actually be zero: a constant
     denominator forbids nothing. */
  function banlist(bans) {
    var seen = {}, out = [];
    bans.forEach(function (p) {
      if (Pdeg(p) < 1) return;
      var key = Ptext(p);
      if (seen[key]) return;
      seen[key] = 1;
      out.push(p);
    });
    return out;
  }
  /* Every distinct denominator including the numeric ones, which forbid
     nothing but still have to be cleared when a complex fraction is tidied. */
  function banlistany(bans) {
    var seen = {}, out = [];
    bans.forEach(function (p) {
      if (Pdeg(p) === 0 && Requ(p[0], R1)) return;
      var key = Ptext(p);
      if (seen[key]) return;
      seen[key] = 1;
      out.push(p);
    });
    return out;
  }
  function zerosentence(p) {
    var z = zerosOf(p), found = [];
    z.rat.forEach(function (r) { found.push('x = ' + Rtext(r)); });
    z.surd.forEach(function (s) { found.push('x = ' + pmtext(s.p, s.s)); });
    if (z.nozero) {
      var q = quadroots(z.nozero[2], z.nozero[1], z.nozero[0]);
      found.push(Pfactortext(z.nozero) + ' has discriminant ' + Rtext(q.disc)
        + ', so it is never 0 for a real x');
    }
    if (z.unknown) {
      found.push('every real zero of ' + Pfactortext(z.unknown)
        + ', which has no rational root and so cannot be named as a fraction here');
    }
    return found.length ? found.join(', &nbsp;') : 'no real solution';
  }

  /* ---- the number line, for domain and solve ---- */
  function lineWindow(points) {
    var lo = -6, hi = 6;
    if (points.length) {
      var mn = Math.min.apply(null, points), mx = Math.max.apply(null, points);
      var pad = Math.max(2, (mx - mn) * 0.6);
      lo = Math.min(-1, mn - pad); hi = Math.max(1, mx + pad);
    }
    return { lo: lo, hi: hi };
  }

  /* ================================================================ domain */
  function modeDomain(A) {
    var ex = exclusionsOf(A.bans);
    var red = RFreduce(A.rf);
    var list = banlist(A.bans);
    var blocks = [], rows = [];
    if (!list.length) {
      rows.push(row('denominators involving x',
        'none &mdash; every division here is by a number, and a number that is not 0 forbids nothing'));
    }
    list.forEach(function (p) {
      rows.push(row(grouptext(Ptext(p)) + ' = 0',
        Pfactortextfull(p) + ' = 0 &nbsp;gives&nbsp; ' + zerosentence(p)));
    });
    blocks.push(table('Step 1 &middot; every denominator, set to zero, before anything is cancelled', rows));

    var r2 = [focusrow('domain', domaintext(ex))];
    var iv = intervaltext(ex);
    if (iv) r2.push(row('as intervals', iv));
    r2.push(row('how many values are lost', excount(ex)));
    blocks.push(table('Step 2 &middot; the domain', r2));

    var r3 = [row('as you wrote it', RFtext(A.rf)),
              row('factored', RFfactortext(A.rf)),
              row('reduced', RFtext(red.rf))];
    if (!ex.rat.length && !ex.surd.length) {
      r3.push(row('nothing to hide', 'no value was excluded in the first place, so the reduced form tells the whole truth here'));
    }
    ex.rat.forEach(function (r) {
      if (Rzero(Peval(red.rf.d, r))) {
        r3.push(row('x = ' + Rtext(r), chip('no', 'excluded, and visible')
          + ' the reduced bottom ' + grouptext(Ptext(red.rf.d)) + ' is 0 here too, so the reduced form refuses this value as well'));
      } else {
        var val = Rdiv(Peval(red.rf.n, r), Peval(red.rf.d, r));
        var why = (Rzero(Peval(A.rf.n, r)) && Rzero(Peval(A.rf.d, r)))
          ? 'the expression as written is 0/0 there'
          : 'the expression as written divides by 0 somewhere inside before it gets that far';
        r3.push(row('x = ' + Rtext(r), chip('hi', 'excluded, and INVISIBLE')
          + ' the reduced form returns ' + Rtext(val) + ' at x = ' + Rtext(r) + ', but ' + why
          + '. So ' + Rtext(r) + ' stays out of the domain and the graph has a hole at ('
          + Rtext(r) + ', ' + Rtext(val) + ')'));
      }
    });
    ex.surd.forEach(function (s) {
      if (Pzero(Pdivmod(red.rf.d, s.min).r)) {
        r3.push(row('x = ' + pmtext(s.p, s.s), chip('no', 'excluded, and visible')
          + ' ' + Ptext(s.min) + ' divides the reduced denominator exactly, so the reduced form '
          + 'refuses these two values as well'));
      } else {
        r3.push(row('x = ' + pmtext(s.p, s.s), chip('hi', 'excluded, and INVISIBLE')
          + ' ' + Ptext(s.min) + ' cancelled, so the reduced form returns an ordinary number at both '
          + 'of these values while the expression as written returns nothing'));
      }
    });
    blocks.push(table('Step 3 &middot; what simplifying would have destroyed', r3));

    if (svg) {
      var pts = exfloats(ex);
      var win = lineWindow(pts);
      var nl = NumberLine(svg, win.lo, win.hi);
      var prev = win.lo - 1;
      pts.forEach(function (p) { nl.interval(prev, p, false, false); prev = p; });
      nl.interval(prev, win.hi + 1, false, false);
      nl.describe('The real line with ' + pts.length + ' point(s) punched out: ' + domaintext(ex) + '.');
    }

    var hid = hiddenExclusions(ex, red.rf);
    var msg;
    if (!ex.rat.length && !ex.surd.length && !ex.unknown.length) {
      msg = '<strong>Nothing is excluded: the domain is every real number.</strong> '
        + (list.length
            ? 'There is a denominator with an x in it, but ' + list.map(function (p) { return grouptext(Ptext(p)); }).join(' and ')
              + ' has no real zero, so no real value of x can break this expression. '
              + 'A variable in a denominator is a warning, not a verdict.'
            : 'Every denominator here is a number, so the division was safe from the start.');
    } else {
      msg = '<strong>Excluded: ' + extext(ex) + '.</strong> Each one came from a denominator '
        + 'set to zero while that denominator was still on the page. ';
      if (hid.count) {
        msg += 'Now look at step 3: the reduced form ' + RFtext(red.rf) + ' returns a perfectly ordinary '
          + 'number at ' + hiddentext(hid) + '. That is the trap this whole course is built around. '
          + 'Simplifying is not a reversible move on the DOMAIN &mdash; it only preserves the values, '
          + 'and only where both forms are defined.';
      } else {
        msg += 'Here the reduced form ' + RFtext(red.rf) + ' still has all of them in its denominator, '
          + 'so nothing was lost by simplifying. The next preset is not so kind.';
      }
    }
    return {
      title: RFtext(A.rf),
      sub: 'domain read from ' + list.length + ' denominator(s), before simplifying',
      blocks: blocks,
      status: msg,
      kpi: [['Excluded', excount(ex)], ['Denominators', String(list.length)],
            ['Invisible after simplifying', String(hid.count)]]
    };
  }

  /* ============================================================== simplify */
  function modeSimplify(A) {
    var ex = exclusionsOf(A.bans);
    var red = RFreduce(A.rf);
    var g = red.gcd;
    var blocks = [];
    blocks.push(table('Step 1 &middot; factor the top and the bottom', [
      row('numerator', Ptext(A.rf.n) + ' &nbsp;=&nbsp; ' + Pfactortextfull(A.rf.n)),
      row('denominator', Ptext(A.rf.d) + ' &nbsp;=&nbsp; ' + Pfactortextfull(A.rf.d))
    ]));

    var r2 = [];
    if (Pdeg(g) > 0) {
      r2.push(focusrow('common factor', Pfactortextfull(g)));
      r2.push(row('numerator / common factor', Ptext(Pdivmod(A.rf.n, g).q)));
      r2.push(row('denominator / common factor', Ptext(Pdivmod(A.rf.d, g).q)));
      r2.push(row('tidied to whole numbers', RFtext(red.rf)));
    } else {
      r2.push(focusrow('common factor', '1 &mdash; there is none'));
      r2.push(row('what that means', 'Euclid&rsquo;s algorithm on these two polynomials ends at a constant, so '
        + 'no bracket is shared. Cancelling anything here would be cancelling a TERM, and a term is '
        + 'part of a sum, not a factor of it.'));
      r2.push(row('reduced', RFtext(red.rf) + ' &mdash; the same expression, tidied only'));
    }
    blocks.push(table('Step 2 &middot; the common factor, found by the polynomial gcd', r2));

    var check = RFeq(A.rf, red.rf);
    blocks.push(table('Step 3 &middot; the reduced form, and what it no longer says', [
      row('reduced', RFtext(red.rf)),
      row('factored', RFfactortext(red.rf)),
      row('equal as fractions?', check
        ? chip('ok', 'yes') + ' cross-multiplying gives the same polynomial both ways, so the two forms agree at every x where both are defined'
        : chip('no', 'no') + ' something is wrong; this should never appear'),
      row('domain of the ORIGINAL', domaintext(ex)),
      row('domain of the REDUCED form as written', (function () {
        var e2 = exclusionsOf([red.rf.d]);
        return domaintext(e2);
      })())
    ]));

    var hid = hiddenExclusions(ex, red.rf);
    var msg;
    if (Pdeg(g) === 0 && (Pdeg(A.rf.n) === 0 || Pdeg(A.rf.d) === 0)) {
      msg = '<strong>Nothing cancels, and nothing could.</strong> Cancelling needs a factor on both '
        + 'sides of the bar, and here one side is just the number '
        + (Pdeg(A.rf.n) === 0 ? Ptext(A.rf.n) : Ptext(A.rf.d))
        + '. A number shares no bracket with a polynomial, so the expression is already as reduced as '
        + 'it gets &mdash; which is not the same as saying it is defined everywhere.';
    } else if (Pdeg(g) === 0) {
      msg = '<strong>Nothing cancels.</strong> ' + Pfactortextfull(A.rf.n) + ' and '
        + Pfactortextfull(A.rf.d) + ' share no bracket, and the gcd search proves it rather than '
        + 'asserting it. The most common wrong move on this expression is to strike out matching '
        + 'SYMBOLS &mdash; an x on top and an x underneath &mdash; but x is a term in a sum here, and '
        + 'a sum has no factors until you factor it.';
    } else if (hid.count) {
      msg = '<strong>' + Pfactortextfull(g) + ' cancels, and takes ' + hiddentext(hid) + ' with it.</strong> '
        + RFtext(red.rf) + ' agrees with the original everywhere the original is defined, and it is '
        + 'defined in more places than the original ever was. Write the excluded value beside the '
        + 'answer: it is no longer recoverable from the answer itself.';
    } else {
      msg = '<strong>' + Pfactortextfull(g) + ' cancels, and no exclusion disappears.</strong> '
        + 'The factor that cancelled appears again in what is left of the denominator, so '
        + extext(ex) + ' is still excluded and still visible. This is the case where cancelling '
        + 'costs you nothing &mdash; and the reason it is safe is worth seeing next to the case where it is not.';
    }
    return {
      title: RFtext(A.rf) + '  =  ' + RFtext(red.rf),
      sub: Pdeg(g) > 0 ? 'cancelled ' + Pfactortextfull(g) : 'nothing to cancel',
      blocks: blocks,
      status: msg,
      kpi: [['Common factor', Pdeg(g) > 0 ? Pfactortextfull(g) : '1'],
            ['Reduced', RFtext(red.rf)],
            ['Exclusions hidden', String(hid.count)]]
    };
  }

  /* ============================================== multiplying and dividing */
  function modeMulDiv(A, B, op) {
    if (op === 'div' && Pzero(B.rf.n)) {
      return { fail: '<strong>The second expression is 0, and nothing may be divided by 0.</strong> '
        + 'Inverting a fraction whose numerator is 0 asks for 1/0, so this is not a step that '
        + 'produces a wrong answer &mdash; it is a step that produces no answer. '
        + 'Every other preset in this list divides by something that is only SOMETIMES zero, and '
        + 'that is where the interesting exclusions come from.' };
    }
    var bans = A.bans.concat(B.bans);
    /* Dividing by B adds a condition the reader did not write down: B itself
       must not be zero. It is the exclusion that is missed most often, because
       it comes from a NUMERATOR. */
    if (op === 'div') bans = bans.concat([B.rf.n]);
    var recip = RFnew(B.rf.d, B.rf.n);
    var prod = op === 'mul' ? RFmul(A.rf, B.rf) : RFmul(A.rf, recip);
    var red = RFreduce(prod);
    var ex = exclusionsOf(bans);
    var blocks = [];

    blocks.push(table('Step 1 &middot; factor everything, before anything moves', [
      row('first', RFtext(A.rf) + ' &nbsp;=&nbsp; ' + RFfactortext(A.rf)),
      row('second', RFtext(B.rf) + ' &nbsp;=&nbsp; ' + RFfactortext(B.rf))
    ]));

    var r2 = [];
    if (op === 'div') {
      r2.push(row('the division', RFtext(A.rf) + ' &divide; ' + RFtext(B.rf)));
      r2.push(focusrow('invert and multiply', RFtext(A.rf) + ' &times; ' + RFtext(recip)));
      r2.push(row('the condition this creates', 'the divisor may not be 0, so '
        + grouptext(Ptext(B.rf.n)) + ' = 0 is now forbidden: ' + zerosentence(B.rf.n)));
    } else {
      r2.push(focusrow('the multiplication', RFtext(A.rf) + ' &times; ' + RFtext(B.rf)));
      r2.push(row('tops times tops, bottoms times bottoms',
        grouptext(Ptext(prod.n)) + ' over ' + grouptext(Ptext(prod.d))));
    }
    r2.push(row('straight across, factored', RFfactortext(prod)));
    blocks.push(table('Step 2 &middot; the operation', r2));

    blocks.push(table('Step 3 &middot; cancel, and only now', [
      row('common factor', Pdeg(red.gcd) > 0 ? Pfactortextfull(red.gcd) : '1 &mdash; nothing cancels'),
      focusrow('answer', RFtext(red.rf)),
      row('answer, factored', RFfactortext(red.rf))
    ]));

    var hid = hiddenExclusions(ex, red.rf);
    blocks.push(table('Step 4 &middot; the domain, which the answer cannot carry', [
      row('excluded', domaintext(ex)),
      row('still visible in the answer', (function () {
        var vis = ex.rat.filter(function (r) { return Rzero(Peval(red.rf.d, r)); }).map(Rtext);
        return vis.length ? vis.join(', ') : 'none';
      })()),
      focusrow('invisible in the answer', hiddentext(hid))
    ]));

    var msg;
    if (op === 'div') {
      var newban = exclusionsOf([B.rf.n]);
      msg = '<strong>Dividing by ' + RFtext(B.rf) + ' forbids ' + extext(newban) + ' on top of everything else.</strong> '
        + 'That exclusion comes from the divisor&rsquo;s NUMERATOR, which is why it is the one that gets lost: '
        + 'a reader scanning for denominators will never look there. ';
    } else {
      msg = '<strong>' + RFtext(A.rf) + ' &times; ' + RFtext(B.rf) + ' = ' + RFtext(red.rf) + '.</strong> ';
    }
    if (hid.count) {
      msg += 'The answer ' + RFtext(red.rf) + ' is defined at ' + hiddentext(hid)
        + '; the expression you started from is not. Both statements are true, and only the second one '
        + 'is about the question that was asked.';
    } else {
      msg += 'Every excluded value is still visible in the answer&rsquo;s denominator, so this one is safe '
        + 'to hand in without a footnote &mdash; which is not true of most of the presets here.';
    }
    return {
      title: RFtext(A.rf) + (op === 'div' ? ' &divide; ' : ' &times; ') + RFtext(B.rf) + '  =  ' + RFtext(red.rf),
      sub: 'excluded: ' + extext(ex),
      blocks: blocks,
      status: msg,
      kpi: [['Operation', op === 'div' ? 'divide' : 'multiply'],
            ['Answer', RFtext(red.rf)],
            ['Exclusions hidden', String(hid.count)]]
    };
  }

  /* ============================================ adding and subtracting */
  function modeAddSub(A, B, op) {
    var d1 = A.rf.d, d2 = B.rf.d;
    var g = Pgcd(d1, d2), L = Plcm(d1, d2);
    var m1 = Pdivmod(L, d1).q, m2 = Pdivmod(L, d2).q;
    var n1 = Pmul(A.rf.n, m1), n2 = Pmul(B.rf.n, m2);
    var total = op === 'add' ? Padd(n1, n2) : Psub(n1, n2);
    var combined = RFnew(total, L);
    var red = RFreduce(combined);
    /* The same sum by the other road: a/b + c/d = (ad + cb)/(bd), with no
       thought given to a least anything. If the two disagree the lab is broken,
       and saying so is more useful than a single unchecked answer. */
    var direct = op === 'add' ? RFadd(A.rf, B.rf) : RFsub(A.rf, B.rf);
    var directRed = RFreduce(direct);
    var agree = RFeq(directRed.rf, red.rf);
    var ex = exclusionsOf(A.bans.concat(B.bans));
    var blocks = [];

    blocks.push(table('Step 1 &middot; the two denominators, factored', [
      row('first', RFtext(A.rf) + ', bottom = ' + Pfactortextfull(d1)),
      row('second', RFtext(B.rf) + ', bottom = ' + Pfactortextfull(d2)),
      row('shared factor', Pdeg(g) > 0 ? Pfactortextfull(g) : '1 &mdash; they share nothing'),
      focusrow('least common denominator', Pfactortextfull(L) + ' &nbsp;=&nbsp; ' + Ptext(L)),
      row('is that the product?', Pdeg(g) > 0
        ? chip('no', 'no') + ' the product would be ' + Ptext(Pmul(d1, d2)) + ', which is '
          + Pfactortextfull(g) + ' times too big &mdash; using it works, but you will cancel that factor back out at the end'
        : chip('ok', 'yes') + ' the denominators share nothing, so here the least common denominator really is the product')
    ]));

    function rewriteLabel(which, m) {
      return (Pdeg(m) === 0 && Requ(m[0], R1))
        ? which + ' is already over the LCD'
        : which + ' &times; ' + grouptext(Ptext(m)) + '/' + grouptext(Ptext(m));
    }
    blocks.push(table('Step 2 &middot; rewrite both over the LCD', [
      row(rewriteLabel('first', m1), grouptext(Ptext(n1)) + ' over ' + grouptext(Ptext(L))),
      row(rewriteLabel('second', m2), grouptext(Ptext(n2)) + ' over ' + grouptext(Ptext(L)))
    ]));

    var r3 = [];
    if (op === 'sub') {
      r3.push(focusrow('subtract the numerators', grouptext(Ptext(n1)) + ' - (' + Ptext(n2) + ')'));
      if (Pdeg(n2) > 0) {
        r3.push(row('distribute the minus', 'the bracket is not decoration: -(' + Ptext(n2) + ') = '
          + Ptext(Pscale(n2, R(-1n))) + ', and every term inside changes sign. Dropping it is the '
          + 'single most common way to get this question wrong.'));
      }
    } else {
      r3.push(focusrow('add the numerators', grouptext(Ptext(n1)) + ' + ' + grouptext(Ptext(n2))));
    }
    r3.push(row('numerator', Ptext(total)));
    r3.push(row('over the LCD', RFtext(combined)));
    blocks.push(table('Step 3 &middot; combine', r3));

    blocks.push(table('Step 4 &middot; simplify, and check by a second route', [
      row('common factor', Pdeg(red.gcd) > 0 ? Pfactortextfull(red.gcd) : '1 &mdash; nothing cancels'),
      focusrow('answer', RFtext(red.rf)),
      row('by the LCD', RFtext(red.rf)),
      row('by a/b ' + (op === 'add' ? '+' : '-') + ' c/d = (ad ' + (op === 'add' ? '+' : '-') + ' cb)/(bd)',
        RFtext(directRed.rf)),
      row('do they agree?', agree
        ? chip('ok', 'yes') + ' the two routes were computed independently and cross-multiply to the same polynomial'
        : chip('no', 'no') + ' this should never appear'),
      row('domain', domaintext(ex))
    ]));

    var hid = hiddenExclusions(ex, red.rf);
    var msg = '<strong>' + RFtext(A.rf) + (op === 'add' ? ' + ' : ' - ') + RFtext(B.rf)
      + ' = ' + RFtext(red.rf) + '.</strong> ';
    if (Pzero(red.rf.n)) {
      msg += 'The answer is 0 &mdash; but only where the question exists. At ' + extext(ex)
        + ' neither term is a number at all, so the expression is not 0 there; it is nothing there. '
        + '&ldquo;Equal to 0&rdquo; and &ldquo;defined and equal to 0&rdquo; part company exactly here.';
    } else if (hid.count) {
      msg += 'The LCD did its job and then the answer cancelled, taking ' + hiddentext(hid)
        + ' out of sight with it. Note where that value came from: it was in a denominator of one '
        + 'of the two terms you started with, and neither the final numerator nor the final '
        + 'denominator mentions it.';
    } else if (Pdeg(g) > 0) {
      msg += 'The two denominators shared ' + Pfactortextfull(g) + ', so the least common denominator was '
        + Ptext(L) + ' rather than their product. Using the product is not wrong; it just means the '
        + 'shared factor rides along through every line and has to be cancelled at the end.';
    } else {
      msg += 'The denominators shared nothing, so the LCD is the product and every step is forced. '
        + 'The exclusions are ' + extext(ex) + ', and they are still visible in the answer.';
    }
    return {
      title: RFtext(A.rf) + (op === 'add' ? '  +  ' : '  -  ') + RFtext(B.rf) + '  =  ' + RFtext(red.rf),
      sub: 'LCD = ' + Ptext(L),
      blocks: blocks,
      status: msg,
      kpi: [['LCD', Ptext(L)], ['Answer', RFtext(red.rf)], ['Excluded', extext(ex)]]
    };
  }

  /* ====================================================== complex fractions */
  function modeComplex(A) {
    if (A.tree.k !== 'div') {
      return { fail: '<strong>That is not a complex fraction.</strong> A complex fraction is one '
        + 'fraction divided by another, so this mode needs a top and a bottom: write it as '
        + '<code>(top)/(bottom)</code>, for instance <code>(1 + 2/x)/(1 - 4/x^2)</code>. '
        + 'What you typed, ' + A.src + ', has no outermost division for the two methods to work on.' };
    }
    var topBans = [], botBans = [], top, bot;
    try {
      top = ErfBuild(A.tree.a, 'x', topBans);
      bot = ErfBuild(A.tree.b, 'x', botBans);
    } catch (err) {
      return { fail: '<strong>' + err.message + '.</strong> Each half of a complex fraction has to be a '
        + 'rational expression in x on its own.' };
    }
    if (Pzero(bot.n)) {
      return { fail: '<strong>The bottom of this complex fraction is 0.</strong> '
        + 'Dividing by it is not a step with a bad answer, it is a step with no answer.' };
    }
    var everyInner = banlistany(topBans.concat(botBans));
    var inner = banlist(topBans.concat(botBans));
    /* The LCD has to clear every small denominator, and 1/2 is a small
       denominator. Taking only the ones containing x leaves a 2 underneath
       after method B and makes the two methods look like different answers. */
    var L = [R1], numl = 1n;
    everyInner.forEach(function (p) {
      if (Pdeg(p) > 0) { L = Plcm(L, p); return; }
      var c = Rabs(p[0]);
      if (Rint(c) && c.n > 0n) numl = numl * c.n / bgcd(numl, c.n);
    });
    if (numl !== 1n) L = Pscale(L, R(numl));

    /* Method A: turn each half into a single fraction, then multiply by the
       reciprocal. Method B: multiply top and bottom by the LCD of the small
       denominators until both halves are polynomials. They are computed from
       the same input and from nothing else, so agreement is evidence. */
    var mA = RFreduce(RFdiv(top, bot));
    var topL = RFreduce(RFmul(top, RFnew(L, [R1])));
    var botL = RFreduce(RFmul(bot, RFnew(L, [R1])));
    var mB = RFreduce(RFnew(Pmul(topL.rf.n, botL.rf.d), Pmul(topL.rf.d, botL.rf.n)));
    var agree = RFeq(mA.rf, mB.rf);
    var ex = exclusionsOf(topBans.concat(botBans).concat([bot.n]));
    var blocks = [];

    blocks.push(table('Step 0 &middot; the small denominators, and what they forbid', [
      row('top', RFtext(top)),
      row('bottom', RFtext(bot)),
      row('denominators inside', everyInner.length
        ? everyInner.map(function (p) { return grouptext(Ptext(p)); }).join(', ')
        : 'none &mdash; there is no fraction inside either half'),
      row('which of them can be 0', inner.length
        ? inner.map(function (p) { return grouptext(Ptext(p)); }).join(', ')
        : 'none &mdash; every small denominator here is a number, so none of them rules out a value of x'),
      focusrow('LCD of them', Ptext(L)),
      row('the bottom may not be 0', grouptext(Ptext(bot.n)) + ' = 0 &nbsp;gives&nbsp; ' + zerosentence(bot.n))
    ]));

    blocks.push(table('Method A &middot; combine each half, then multiply by the reciprocal', [
      row('top as one fraction', RFtext(top)),
      row('bottom as one fraction', RFtext(bot)),
      row('divide', RFtext(top) + ' &divide; ' + RFtext(bot) + ' = ' + RFtext(top) + ' &times; ' + RFtext(RFnew(bot.d, bot.n))),
      focusrow('answer', RFtext(mA.rf))
    ]));

    blocks.push(table('Method B &middot; multiply top and bottom by ' + Ptext(L), [
      row('top &times; ' + grouptext(Ptext(L)), RFtext(topL.rf)
        + (Pdeg(topL.rf.d) === 0 ? ' &mdash; no x left underneath: the small denominators are cleared'
                                 : ' &mdash; still has an x underneath, so the LCD was not big enough')),
      row('bottom &times; ' + grouptext(Ptext(L)), RFtext(botL.rf)
        + (Pdeg(botL.rf.d) === 0 ? ' &mdash; no x left underneath either'
                                 : ' &mdash; still has an x underneath')),
      focusrow('answer', RFtext(mB.rf))
    ]));

    blocks.push(table('Do the two methods agree?', [
      row('method A', RFtext(mA.rf)),
      row('method B', RFtext(mB.rf)),
      focusrow('cross-multiplied', agree
        ? chip('ok', 'identical') + ' the two routes were run independently on the same input and their cross-products are the same polynomial'
        : chip('no', 'they differ') + ' this should never appear'),
      row('domain', domaintext(ex))
    ]));

    var hid = hiddenExclusions(ex, mA.rf);
    var msg = '<strong>' + A.src + ' = ' + RFtext(mA.rf) + '.</strong> ';
    if (!inner.length) {
      msg += 'Not one of the small denominators contains an x, so nothing here can be zero and the '
        + 'domain is the whole real line. The two methods are still two methods &mdash; multiply out '
        + 'by ' + Ptext(L) + ' and the letters would behave exactly as these numbers do. That is the '
        + 'point of running this preset: the algebra is not a new rule, it is the arithmetic you '
        + 'already trust with a letter in it.';
    } else {
      msg += 'Method A combined each half first; method B cleared all the small denominators at once '
        + 'by multiplying above and below by ' + Ptext(L) + '. Neither is more correct. ';
    }
    if (hid.count) {
      msg += ' The answer hides ' + hiddentext(hid) + ': those values came from denominators INSIDE '
        + 'the fraction, or from the bottom half being zero, and the tidy answer has no room left to '
        + 'mention them.';
    } else if (ex.rat.length || ex.surd.length) {
      msg += ' Every exclusion here survives into the answer&rsquo;s denominator, so nothing is lost.';
    }
    return {
      title: A.src + '  =  ' + RFtext(mA.rf),
      sub: 'LCD of the inner denominators: ' + Ptext(L),
      blocks: blocks,
      status: msg,
      kpi: [['Method A', RFtext(mA.rf)], ['Method B', RFtext(mB.rf)],
            ['Agree?', agree ? 'yes' : 'NO']]
    };
  }

  /* ================================================================= solve */
  function modeSolve(A, B) {
    var bans = A.bans.concat(B.bans);
    var ex = exclusionsOf(bans);
    /* Multiply out: nL*dR - nR*dL = 0 has exactly the solutions of the original
       equation PLUS, possibly, some values where a denominator was zero. That
       "plus" is the entire lesson, and it is why the check below runs on the
       tree the reader typed rather than on this polynomial. */
    var E = Psub(Pmul(A.rf.n, B.rf.d), Pmul(B.rf.n, A.rf.d));
    var blocks = [];
    blocks.push(table('Step 1 &middot; the exclusions, written down before solving', [
      row('left side', RFtext(A.rf)),
      row('right side', RFtext(B.rf)),
      row('denominators', banlist(bans).length
        ? banlist(bans).map(function (p) { return grouptext(Ptext(p)); }).join(', ') : 'none'),
      focusrow('x may not be', extext(ex))
    ]));

    var cands = [], leftover = null, identity = false, impossible = false;
    if (Pzero(E)) identity = true;
    else if (Pdeg(E) === 0) impossible = true;
    else {
      var f = Pfactor(E);
      f.factors.forEach(function (item) { cands.push({ kind: 'rat', r: item.root, mult: item.mult }); });
      if (f.rest.length) {
        if (Pdeg(f.rest) === 2) {
          var q = quadroots(f.rest[2], f.rest[1], f.rest[0]);
          if (q.kind === 'complex') leftover = { why: 'complex', poly: f.rest, q: q };
          else cands.push({ kind: 'surd', p: q.p, s: q.s, min: Pmonic(f.rest), poly: f.rest });
        } else {
          leftover = { why: 'degree', poly: f.rest };
        }
      }
    }
    cands.sort(function (a, b) {
      var av = a.kind === 'rat' ? Rnum(a.r) : Rnum(a.p), bv = b.kind === 'rat' ? Rnum(b.r) : Rnum(b.p);
      return av - bv;
    });

    var r2 = [row('multiply both sides by every denominator',
                  grouptext(Ptext(A.rf.n)) + ' &middot; ' + grouptext(Ptext(B.rf.d)) + '  =  '
                  + grouptext(Ptext(B.rf.n)) + ' &middot; ' + grouptext(Ptext(A.rf.d))),
              focusrow('everything on one side', Ptext(E) + ' = 0')];
    if (identity) {
      r2.push(row('that is 0 = 0', 'the two sides are the same rational function, so the equation is an '
        + 'identity: every x IN THE DOMAIN is a solution, and ' + extext(ex) + ' still are not'));
    } else if (impossible) {
      r2.push(row('a constant that is not 0', 'clearing the denominators leaves ' + Ptext(E)
        + ' = 0, which no value of x can arrange. There is no solution.'));
    } else {
      r2.push(row('factored', Pfactortextfull(E) + ' = 0'));
      if (leftover && leftover.why === 'complex') {
        r2.push(row('the quadratic factor', Pfactortext(leftover.poly) + ' has discriminant '
          + Rtext(leftover.q.disc) + ', so it contributes no real candidate at all &mdash; its roots are '
          + pmtext(leftover.q.p, leftover.q.s, true)));
      }
      if (leftover && leftover.why === 'degree') {
        r2.push(row('a factor with no rational root', Pfactortext(leftover.poly)
          + ' &mdash; degree ' + Pdeg(leftover.poly) + ', and the rational root search came back empty. '
          + 'Any solutions it holds are not listed below, and this lab says so rather than implying there are none.'));
      }
    }
    blocks.push(table('Step 2 &middot; clear the denominators and solve', r2));

    var verified = [], extraneous = [];
    var r3 = [];
    cands.forEach(function (c) {
      if (c.kind === 'rat') {
        var bad = null;
        banlist(bans).forEach(function (p) { if (bad === null && Rzero(Peval(p, c.r))) bad = p; });
        var lv = Eexact(A.tree, 'x', c.r), rv = Eexact(B.tree, 'x', c.r);
        if (bad !== null || lv === null || rv === null) {
          extraneous.push(c);
          r3.push(row('x = ' + Rtext(c.r), chip('no', 'extraneous')
            + ' substituting into the ORIGINAL makes ' + (bad !== null ? grouptext(Ptext(bad)) : 'a denominator')
            + ' equal to 0, so the left side is not a number there. It solves the cleared equation and '
            + 'not the equation that was asked.'));
        } else if (Requ(lv, rv)) {
          verified.push(c);
          r3.push(row('x = ' + Rtext(c.r), chip('ok', 'verified')
            + ' left side = ' + Rtext(lv) + ', right side = ' + Rtext(rv)
            + ' &mdash; both computed from the expressions as you typed them'));
        } else {
          extraneous.push(c);
          r3.push(row('x = ' + Rtext(c.r), chip('no', 'fails')
            + ' left side = ' + Rtext(lv) + ' but right side = ' + Rtext(rv)));
        }
      } else {
        /* An irrational candidate cannot be substituted as a fraction, so the
           check is done exactly a different way: the candidate is a root of the
           irreducible quadratic min(x), and it makes a denominator zero exactly
           when min divides that denominator. Polynomial division decides it. */
        var badq = null;
        banlist(bans).forEach(function (p) { if (badq === null && Pzero(Pdivmod(p, c.min).r)) badq = p; });
        var sv = Rnum(c.s.q) * Math.sqrt(Number(c.s.k)), pv = Rnum(c.p);
        var num = '';
        try {
          var l1 = Eeval(A.tree, { x: pv + sv }), r1 = Eeval(B.tree, { x: pv + sv });
          num = ' A numeric re-check at x = ' + (pv + sv).toFixed(6) + ' (rounded) gives '
            + l1.toFixed(6) + ' and ' + r1.toFixed(6) + '.';
        } catch (err) { num = ''; }
        if (badq !== null) {
          extraneous.push(c);
          r3.push(row('x = ' + pmtext(c.p, c.s), chip('no', 'extraneous')
            + ' ' + Ptext(c.min) + ' divides the denominator ' + grouptext(Ptext(badq))
            + ' exactly, so both of these values make it 0'));
        } else {
          verified.push(c);
          r3.push(row('x = ' + pmtext(c.p, c.s), chip('ok', 'verified')
            + ' these are the roots of ' + Ptext(c.min) + ', which divides no denominator here '
            + '(polynomial division leaves a remainder in every case), so both are in the domain and '
            + 'both satisfy the cleared equation.' + num));
        }
      }
    });
    if (!cands.length) {
      r3.push(row('candidates', identity
        ? 'every x in the domain &mdash; there is nothing to check one at a time'
        : 'none &mdash; there was no candidate to check'));
    }
    blocks.push(table('Step 3 &middot; substitute every candidate into the ORIGINAL equation', r3));

    var solutions = verified.map(function (c) {
      return c.kind === 'rat' ? 'x = ' + Rtext(c.r) : 'x = ' + pmtext(c.p, c.s);
    });
    var lost = extraneous.map(function (c) {
      return c.kind === 'rat' ? Rtext(c.r) : pmtext(c.p, c.s);
    });

    if (svg) {
      var pts = exfloats(ex).slice();
      cands.forEach(function (c) {
        if (c.kind === 'rat') pts.push(Rnum(c.r));
        else { var s2 = Rnum(c.s.q) * Math.sqrt(Number(c.s.k)); pts.push(Rnum(c.p) + s2, Rnum(c.p) - s2); }
      });
      var win = lineWindow(pts);
      var nl = NumberLine(svg, win.lo, win.hi);
      exfloats(ex).forEach(function (p) { nl.point(p, false); });
      verified.forEach(function (c) {
        if (c.kind === 'rat') nl.point(Rnum(c.r), true);
        else { var s3 = Rnum(c.s.q) * Math.sqrt(Number(c.s.k)); nl.point(Rnum(c.p) + s3, true); nl.point(Rnum(c.p) - s3, true); }
      });
      extraneous.forEach(function (c) { if (c.kind === 'rat') nl.point(Rnum(c.r), false); });
      nl.describe('The real line with the excluded values as hollow points and the '
        + verified.length + ' verified solution(s) filled in.');
    }

    var unnamed = leftover && leftover.why === 'degree';
    var caveat = unnamed
      ? ' One factor, ' + Pfactortext(leftover.poly) + ', has no rational root, so the search that '
        + 'produced the list above could not name its zeros. Any solutions hiding in it are irrational '
        + 'and are NOT listed here &mdash; a search over the fractions has ruled out nothing about the '
        + 'numbers that are not fractions.'
      : '';
    var msg;
    if (identity) {
      msg = '<strong>Both sides are the same rational function, so this is an identity.</strong> '
        + 'Every x in the domain solves it &mdash; and ' + extext(ex) + ' still does not, because '
        + 'an identity is a statement about values that exist.';
    } else if (!solutions.length && lost.length) {
      msg = '<strong>' + (unnamed ? 'No solution among the values this lab can name. The rational candidate'
                                  : 'No solution. The only candidate')
        + (lost.length > 1 ? 's were ' : ' was ') + lost.join(' and ')
        + ', and ' + (lost.length > 1 ? 'both are ' : 'it is ') + 'extraneous.</strong> '
        + 'Multiplying both sides by a denominator is legal only when that denominator is not zero, and '
        + 'nothing in the cleared equation remembers the condition. That is why the check is not '
        + 'optional bookkeeping: here it is the difference between &ldquo;x = ' + lost[0]
        + '&rdquo; and &ldquo;there is no solution&rdquo;.';
    } else if (!solutions.length && unnamed) {
      msg = '<strong>No solution that can be written as a fraction.</strong> Clearing the denominators '
        + 'gave ' + Ptext(E) + ' = 0, and every rational candidate was tested and rejected. That is a '
        + 'much weaker statement than &ldquo;no solution&rdquo;, and this lab will not upgrade it: '
        + Pfactortext(leftover.poly) + ' may well cross zero somewhere irrational.';
    } else if (!solutions.length) {
      msg = '<strong>No real solution.</strong> Clearing the denominators gave ' + Ptext(E)
        + ' = 0' + (leftover && leftover.why === 'complex'
          ? ', whose discriminant is ' + Rtext(leftover.q.disc) + ' &mdash; negative, so no real x satisfies it. '
            + 'Course 6 gives those roots a home; on the real line there is nothing here.'
          : ', which no real x satisfies.');
    } else if (lost.length) {
      msg = '<strong>' + solutions.join(' and ') + ', and ' + lost.join(' and ') + ' is extraneous.</strong> '
        + 'Both came out of the same cleared equation and only one of them survives substitution into '
        + 'the original. An extraneous root is not an arithmetic slip &mdash; it is the honest consequence '
        + 'of a legal step, and substitution is the only thing that catches it.';
    } else {
      msg = '<strong>' + solutions.join(' and ') + '.</strong> Every candidate survived the check: none of '
        + 'them lands on ' + (extext(ex) === 'none' ? 'an excluded value, because there are none' : extext(ex))
        + '. The check still had to be done &mdash; you cannot know it was unnecessary until afterwards.';
    }
    msg += caveat;
    return {
      title: A.src + '  =  ' + B.src,
      sub: solutions.length ? solutions.join(',  ') : 'no solution',
      blocks: blocks,
      status: msg,
      kpi: [['Candidates', String(cands.length)],
            ['Verified', solutions.length ? solutions.join(', ') : 'none'],
            ['Extraneous', lost.length ? lost.join(', ') : 'none']]
    };
  }

  /* ================================================================= graph */
  function modeGraph(A) {
    var ex = exclusionsOf(A.bans);
    var red = RFreduce(A.rf);
    var rf = red.rf;
    var asym = [], asymSurd = [], holes = [], holeSurd = [];
    ex.rat.forEach(function (r) {
      if (Rzero(Peval(rf.d, r))) asym.push(r);
      else holes.push({ x: r, y: Rdiv(Peval(rf.n, r), Peval(rf.d, r)) });
    });
    ex.surd.forEach(function (s) {
      if (Pzero(Pdivmod(rf.d, s.min).r)) asymSurd.push(s); else holeSurd.push(s);
    });
    var dn = Pdeg(rf.n), dd = Pdeg(rf.d);
    var endKind, endText, endValue = null, oblique = null;
    if (Pzero(rf.n)) { endKind = 'zero'; endText = 'the expression is 0 wherever it is defined'; }
    else if (dd === 0) {
      endKind = 'poly';
      endText = 'no asymptote at all &mdash; once the common factor cancels this IS the polynomial '
        + Ptext(rf.n);
    }
    else if (dn < dd) { endKind = 'h'; endValue = R0; endText = 'y = 0'; }
    else if (dn === dd) { endKind = 'h'; endValue = Rdiv(Plead(rf.n), Plead(rf.d)); endText = 'y = ' + Rtext(endValue); }
    else if (dn === dd + 1) { oblique = Pdivmod(rf.n, rf.d).q; endKind = 'oblique'; endText = 'y = ' + Ptext(oblique); }
    else { endKind = 'none'; endText = 'no horizontal or slant asymptote &mdash; the top outruns the bottom by ' + (dn - dd) + ' degrees'; }

    var zn = zerosOf(rf.n);
    var xint = zn.rat.filter(function (r) {
      var out = true;
      ex.rat.forEach(function (e) { if (Requ(e, r)) out = false; });
      return out;
    });
    var yint = null;
    var zeroExcluded = false;
    ex.rat.forEach(function (e) { if (Rzero(e)) zeroExcluded = true; });
    if (!zeroExcluded && !Rzero(Peval(rf.d, R0))) yint = Rdiv(Peval(rf.n, R0), Peval(rf.d, R0));

    var blocks = [];
    blocks.push(table('Step 1 &middot; factor, then reduce &mdash; in that order', [
      row('as written', RFtext(A.rf)),
      row('factored', RFfactortext(A.rf)),
      row('reduced', RFtext(rf)),
      row('excluded by the ORIGINAL', domaintext(ex))
    ]));

    var r2 = [];
    if (!asym.length && !asymSurd.length) {
      r2.push(row('vertical asymptotes', 'none'));
    }
    asym.forEach(function (r) {
      r2.push(row('x = ' + Rtext(r), chip('no', 'asymptote')
        + ' the reduced bottom ' + grouptext(Ptext(rf.d)) + ' is 0 here and the top is not, so the '
        + 'value runs off to infinity on at least one side'));
    });
    asymSurd.forEach(function (s) {
      r2.push(row('x = ' + pmtext(s.p, s.s), chip('no', 'asymptote')
        + ' ' + Ptext(s.min) + ' divides the reduced denominator exactly'));
    });
    holes.forEach(function (h) {
      r2.push(row('x = ' + Rtext(h.x), chip('hi', 'hole')
        + ' the factor cancelled, so the reduced form gives ' + Rtext(h.y) + ' here &mdash; but the '
        + 'expression as written is undefined, and the curve has a single missing point at ('
        + Rtext(h.x) + ', ' + Rtext(h.y) + ')'));
    });
    holeSurd.forEach(function (s) {
      r2.push(row('x = ' + pmtext(s.p, s.s), chip('hi', 'hole') + ' cancelled out of the reduced form'));
    });
    ex.unknown.forEach(function (q) {
      r2.push(row('zeros of ' + Pfactortext(q), chip('no', 'not named')
        + ' this factor has no rational root, so the search cannot say where its zeros are. They are '
        + 'excluded all the same, and the curve breaks there whether or not a line is drawn for it.'));
    });
    blocks.push(table('Step 2 &middot; asymptote or hole? The reduced denominator decides', r2));

    var r3 = [row('degree of the top', String(dn)), row('degree of the bottom', String(dd))];
    if (endKind === 'h') {
      r3.push(focusrow('horizontal asymptote', endText + (dn === dd
        ? ' &mdash; equal degrees, so the ratio of the leading coefficients, ' + Rtext(Plead(rf.n)) + '/' + Rtext(Plead(rf.d))
        : ' &mdash; the bottom grows faster, so the quotient is squeezed to 0')));
    } else if (endKind === 'poly') {
      r3.push(focusrow('end behaviour', endText + '. A curve does not approach a line it is already '
        + 'on, so there is nothing here for an asymptote to do. The only mark this expression leaves '
        + 'is the hole where the cancelled factor used to be.'));
    } else if (endKind === 'oblique') {
      r3.push(focusrow('slant asymptote', endText + ' &mdash; the top is exactly one degree bigger, and '
        + 'polynomial division gives ' + RFtext(rf) + ' = ' + Ptext(oblique) + ' + '
        + RFtext(RFnew(Pdivmod(rf.n, rf.d).r, rf.d)) + ', whose second piece dies away'));
    } else {
      r3.push(focusrow('end behaviour', endText));
    }
    r3.push(row('x-intercepts', xint.length
      ? xint.map(function (r) { return '(' + Rtext(r) + ', 0)'; }).join(', ')
      : 'none &mdash; the reduced numerator has no rational zero outside the excluded set'));
    r3.push(row('y-intercept', yint === null
      ? 'none &mdash; x = 0 is not in the domain'
      : '(0, ' + Rtext(yint) + ')'));
    blocks.push(table('Step 3 &middot; end behaviour and intercepts', r3));

    /* ---- the picture. Every mark below is a float only in its pixel; the
       number that put it there came from the exact side above. ---- */
    if (svg) {
      var f = RFnumeric(rf);
      var marks = exfloats(ex).slice();
      xint.forEach(function (r) { marks.push(Rnum(r)); });
      if (yint !== null) marks.push(0);
      var lo = -6, hi = 6;
      if (marks.length) {
        var mn = Math.min.apply(null, marks), mx = Math.max.apply(null, marks);
        var pad = Math.max(3, (mx - mn) * 0.7);
        lo = mn - pad; hi = mx + pad;
      }
      var vfloats = asym.map(Rnum);
      asymSurd.forEach(function (s) {
        var sv = Rnum(s.s.q) * Math.sqrt(Number(s.s.k));
        vfloats.push(Rnum(s.p) + sv, Rnum(s.p) - sv);
      });
      var ys = [], i, x, y;
      for (i = 0; i <= 400; i += 1) {
        x = lo + (hi - lo) * i / 400;
        var near = false;
        vfloats.forEach(function (a) { if (Math.abs(x - a) < (hi - lo) / 45) near = true; });
        if (near) continue;
        y = f(x);
        if (isFinite(y)) ys.push(y);
      }
      ys.sort(function (a, b) { return a - b; });
      var ylo = -6, yhi = 6;
      if (ys.length > 12) { ylo = ys[Math.floor(ys.length * 0.06)]; yhi = ys[Math.floor(ys.length * 0.94)]; }
      else if (ys.length) { ylo = ys[0]; yhi = ys[ys.length - 1]; }
      if (endKind === 'h') { ylo = Math.min(ylo, Rnum(endValue)); yhi = Math.max(yhi, Rnum(endValue)); }
      holes.forEach(function (h) { ylo = Math.min(ylo, Rnum(h.y)); yhi = Math.max(yhi, Rnum(h.y)); });
      if (yint !== null) { ylo = Math.min(ylo, Rnum(yint)); yhi = Math.max(yhi, Rnum(yint)); }
      ylo = Math.min(ylo, 0); yhi = Math.max(yhi, 0);
      if (!(yhi - ylo > 0.8)) { ylo -= 2; yhi += 2; }
      var ypad = (yhi - ylo) * 0.16;
      var plot = Plot(svg, { xmin: lo, xmax: hi, ymin: ylo - ypad, ymax: yhi + ypad });
      plot.frame();
      asym.forEach(function (r) { plot.vline(Rnum(r), 'plot-asym', 'x = ' + Rtext(r)); });
      vfloats.forEach(function (a) {
        var known = false;
        asym.forEach(function (r) { if (Math.abs(Rnum(r) - a) < 1e-12) known = true; });
        if (!known) plot.vline(a, 'plot-asym', 'x ~ ' + a.toFixed(3));
      });
      if (endKind === 'h') plot.hline(Rnum(endValue), 'plot-asym', 'y = ' + Rtext(endValue));
      if (endKind === 'oblique' && oblique) {
        var qq = oblique.map(Rnum);
        var qat = function (t) { var acc = 0; for (var j = qq.length - 1; j >= 0; j -= 1) acc = acc * t + qq[j]; return acc; };
        plot.segment(lo, qat(lo), hi, qat(hi), 'plot-asym');
        plot.label(lo + (hi - lo) * 0.06, qat(lo + (hi - lo) * 0.06) + (yhi - ylo) * 0.06, 'y = ' + Ptext(oblique));
      }
      plot.curve(f);
      xint.forEach(function (r) { plot.point(Rnum(r), 0, 'plot-point root', Rtext(r)); });
      if (yint !== null) plot.point(0, Rnum(yint), 'plot-point', Rtext(yint));
      holes.forEach(function (h) { plot.hole(Rnum(h.x), Rnum(h.y)); });
      holeSurd.forEach(function (s) {
        var sv2 = Rnum(s.s.q) * Math.sqrt(Number(s.s.k));
        plot.hole(Rnum(s.p) + sv2, f(Rnum(s.p) + sv2));
        plot.hole(Rnum(s.p) - sv2, f(Rnum(s.p) - sv2));
      });
      plot.describe(RFtext(A.rf) + ' sampled at 480 points from its reduced form, with '
        + (asym.length + asymSurd.length) + ' vertical asymptote(s), ' + (holes.length + holeSurd.length)
        + ' hole(s), and end behaviour ' + endText + '.');
    }

    var nvert = asym.length + 2 * asymSurd.length, nhole = holes.length + 2 * holeSurd.length;
    var asymNames = asym.map(function (r) { return 'x = ' + Rtext(r); });
    asymSurd.forEach(function (sd) { asymNames.push('x = ' + pmtext(sd.p, sd.s)); });
    function plural(n, word) { return n + ' ' + word + (n === 1 ? '' : 's'); }
    var msg;
    if (nhole) {
      msg = '<strong>' + plural(nhole, 'hole') + ', ' + plural(nvert, 'vertical asymptote') + '.</strong> '
        + 'Both come from a denominator that is zero, and telling them apart is not a matter of looking '
        + 'at the picture: the factor that cancels leaves a hole, the factor that survives into the '
        + 'reduced denominator leaves an asymptote. '
        + (Pdeg(red.gcd) > 0
            ? 'Here ' + Pfactortextfull(red.gcd) + ' cancelled, so x = '
              + (holes.length ? Rtext(holes[0].x) : 'the excluded value')
              + ' is a single missing point on an otherwise ordinary curve, not a wall'
            : 'Here nothing cancelled at all: the ban came from a denominator INSIDE the expression, '
              + 'which never reached the outermost one, so x = '
              + (holes.length ? Rtext(holes[0].x) : 'the excluded value')
              + ' is forbidden by a fraction you can no longer see')
        + (endKind === 'poly'
            ? ', and what is left, ' + Ptext(rf.n) + ', is a polynomial, so there is no wall anywhere.'
            : '.');
    } else if (!nvert && ex.unknown.length) {
      msg = '<strong>There are vertical asymptotes here and this lab will not tell you where.</strong> '
        + ex.unknown.map(function (q) { return Pfactortext(q); }).join(' and ')
        + ' has no rational root, so the exact search that locates every other asymptote on this page '
        + 'comes back empty. An odd-degree polynomial always crosses zero somewhere; not being able to '
        + 'write that somewhere as a fraction is a fact about fractions, not about the curve. The '
        + 'break in the drawing above is real even though no line is labelled on it.';
    } else if (!nvert && Pdeg(rf.d) === 0) {
      msg = '<strong>No asymptote, because after cancelling there is no denominator left.</strong> '
        + 'What remains is the polynomial ' + Ptext(rf.n) + ', and a polynomial runs off to infinity '
        + 'without ever having to avoid a value of x.';
    } else if (!nvert) {
      msg = '<strong>No vertical asymptote anywhere.</strong> ' + grouptext(Ptext(rf.d))
        + ' has no real zero, so the denominator never vanishes and the curve is unbroken across the '
        + 'whole real line. A rational function is not obliged to have an asymptote; it has one '
        + 'exactly where its reduced denominator is 0.';
    } else {
      msg = '<strong>' + (nvert === 1 ? 'Vertical asymptote' : 'Vertical asymptotes') + ' at '
        + asymNames.join(', ') + '.</strong> ';
      if (endKind === 'oblique') {
        msg += 'The top is one degree bigger than the bottom, so the far ends do not flatten out &mdash; '
          + 'they follow the line ' + endText + ', which is what the polynomial part of the long division is. '
          + 'A horizontal asymptote is the special case of that line being flat.';
      } else if (endKind === 'h') {
        msg += 'Far out in both directions the curve settles on ' + endText + ', decided by the degrees '
          + 'alone: ' + (dn === dd ? 'equal degrees give the ratio of the leading coefficients'
                                   : 'a bigger bottom gives 0') + '.';
      } else {
        msg += endText + '.';
      }
    }
    return {
      title: RFtext(A.rf) + (red.cancelled ? '  =  ' + RFtext(rf) + '  (with holes)' : ''),
      sub: endText,
      blocks: blocks,
      status: msg,
      kpi: [['Vertical asymptotes', String(asym.length + asymSurd.length)],
            ['Holes', String(holes.length + holeSurd.length)],
            ['End behaviour', endText]]
    };
  }

  /* ================================================================ driver */
  function fail(msg) {
    status.innerHTML = msg;
    work.innerHTML = table('Nothing computed yet', [
      row('waiting for', 'a rational expression in the single variable x'),
      row('examples that work', '<code>(x^2 - 4)/(x - 2)</code>, <code>1/x + 1/2</code>, <code>3/(x - 1)</code>')
    ]);
    titleOut.textContent = 'Nothing to show';
    subOut.textContent = 'fix the expression above';
    if (svg) svg.textContent = '';
    setkpi([['Status', '--'], ['Status', '--'], ['Status', '--']]);
  }

  function redraw() {
    var A = readExpr(inA.value, LABEL_A);
    if (!A.ok) { fail(A.msg); return; }
    var B = null;
    if (HASB) {
      B = readExpr(inB.value, LABEL_B);
      if (!B.ok) { fail(B.msg); return; }
    }
    var op = opSel ? opSel.value : 'mul';
    if (labelB) labelB.textContent = LABEL_B;

    var out;
    try {
      if (MODE === 'domain') out = modeDomain(A);
      else if (MODE === 'simplify') out = modeSimplify(A);
      else if (MODE === 'multiply') out = modeMulDiv(A, B, op);
      else if (MODE === 'add') out = modeAddSub(A, B, op);
      else if (MODE === 'complex') out = modeComplex(A);
      else if (MODE === 'solve') out = modeSolve(A, B);
      else out = modeGraph(A);
    } catch (err) {
      fail('<strong>That expression is more than this lab can carry: ' + (err && err.message) + '.</strong> '
        + 'Everything here is done in exact fractions over the rationals, and a few inputs '
        + '&mdash; very high powers, coefficients with enormous denominators &mdash; run past what the '
        + 'exact machinery will do quickly. Try one of the presets, then edit it a little at a time.');
      return;
    }
    if (out.fail) { fail(out.fail); return; }
    titleOut.innerHTML = out.title;
    subOut.textContent = out.sub;
    work.innerHTML = out.blocks.join('');
    status.innerHTML = out.status;
    setkpi(out.kpi);
  }

  function loadPreset() {
    var parts = String(preset.value).split('|');
    inA.value = parts[0];
    if (inB) inB.value = parts[1] || '';
    if (opSel && parts[2]) opSel.value = parts[2];
  }
  preset.addEventListener('change', function () { loadPreset(); redraw(); });
  inA.addEventListener('input', redraw);
  if (inB) inB.addEventListener('input', redraw);
  if (opSel) opSel.addEventListener('change', redraw);
  loadPreset();
  redraw();
  window.redrawLab = redraw;
"""


def rationalfn_lab(cfg):
    """Rational expressions, with the domain computed before anything cancels.

    The teaching decision: the reader's expression is parsed into an UNREDUCED
    pair of polynomials plus the list of everything it divided by, and the
    exclusions are read off that list. Every mode then does its own work on top
    of the same object, so `simplify` and `graph` cannot disagree about where a
    hole is -- they are looking at the same two facts (what cancelled, and what
    was banned) from two directions.
    """
    mode = cfg.get("mode", "domain")
    if mode not in RF_PRESETS:
        mode = "domain"
    presets = cfg.get("presets") or RF_PRESETS[mode]
    title, subtitle = RF_TITLES[mode]
    has_b = mode in RF_TWO
    has_op = mode in RF_OPS
    has_stage = mode in RF_STAGE
    label_a, label_b = RF_LABELS[mode]

    options = "".join(
        '<option value="' + a + '|' + b + '|' + op + '">' + label + "</option>"
        for label, a, b, op in presets
    )

    legend = RF_LEGENDS.get(
        mode,
        '<span class="tone-cyan"><i class="legend-swatch"></i>exact rational arithmetic</span>'
        '<span class="tone-amber"><i class="legend-swatch"></i>what the answer hides</span>',
    )
    stage = (
        '      <div class="lab-stage" id="rfStage"><svg id="rfPlot"></svg></div>\n'
        if has_stage else ""
    )
    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="rfTitle">Rational expression</strong>'
        '<span id="rfSub"></span></div>\n'
        '        <div class="inline-legend">' + legend + "</div>\n"
        "      </div>\n"
        + stage
        + '      <div id="rfWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="rfStatus" style="margin-top:12px;"></div>'
    )

    op_field = ""
    if has_op:
        op_options = "".join(
            '<option value="' + value + '">' + text + "</option>"
            for value, text in RF_OPS[mode]
        )
        op_field = (
            '        <div class="field" id="rfFieldOp">\n'
            '          <label for="rfOp">Operation</label>\n'
            '          <select id="rfOp">' + op_options + "</select>\n"
            "        </div>\n"
        )
    b_field = ""
    if has_b:
        b_field = (
            '        <div class="field" id="rfFieldB">\n'
            '          <label for="rfExprB" id="rfLabelB">' + label_b + "</label>\n"
            '          <input id="rfExprB" type="text" value="" inputmode="text" autocomplete="off">\n'
            "        </div>\n"
        )

    controls = (
        '        <div class="field" id="rfFieldPreset">\n'
        '          <label for="rfPreset">Worked example</label>\n'
        '          <select id="rfPreset">' + options + "</select>\n"
        "        </div>\n"
        '        <div class="field" id="rfFieldA">\n'
        '          <label for="rfExprA" id="rfLabelA">' + label_a + "</label>\n"
        '          <input id="rfExprA" type="text" value="" inputmode="text" autocomplete="off">\n'
        "        </div>\n"
        + op_field
        + b_field
        + '        <div class="kpi-grid">\n'
        '          <div class="kpi"><span id="rfK1Lab">&mdash;</span><strong id="rfK1">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="rfK2Lab">&mdash;</span><strong id="rfK2">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="rfK3Lab">&mdash;</span><strong id="rfK3">&mdash;</strong></div>\n'
        "        </div>\n"
        '        <p class="small-copy" id="rfHint" style="margin:0;">Type any rational expression in '
        "<code>x</code>: <code>2x</code>, <code>(x+1)(x-2)</code> and <code>1/x + 1/2</code> all parse. "
        "Every coefficient below is an exact fraction, and every excluded value is found from the "
        "denominators as you wrote them.</p>"
    )

    script = (
        RATIONAL_JS + POLY_JS + SURD_JS + EXPR_JS + PLOT_JS + RF_JS
        + RF_SCRIPT
        .replace("__MODE__", mode)
        .replace("__HASB__", "true" if has_b else "false")
        .replace("__HASOP__", "true" if has_op else "false")
        .replace("__HASSTAGE__", "true" if has_stage else "false")
        .replace("__LABELA__", label_a.replace("'", "\\'"))
        .replace("__LABELB__", (label_b or label_a).replace("'", "\\'"))
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a worked example, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "Everything below is recomputed from what is in these boxes. The excluded values "
            "come from the denominators before anything cancels, which is the only order in "
            "which they can be found at all.",
        ),
        script=script,
    )


# --------------------------------------------------------------------------
# Lab 2: complex numbers.
# --------------------------------------------------------------------------

CX_JS = r"""
  /* ---- complex numbers with exact rational parts ----

     { a, b } meaning a + bi, with a and b rationals from RATIONAL_JS. Nothing
     here is a float, which is the only way (1 + 2i)/(3 - i) can come back as
     1/10 + 7/10 i instead of 0.1 + 0.7000000000000001 i. The Argand plane is
     the one place a coordinate becomes a float, and only to become a pixel. */
  function Cnew(a, b) { return { a: a, b: b }; }
  var C0 = Cnew(R0, R0), C1 = Cnew(R1, R0), CI = Cnew(R0, R1);
  function Cadd(z, w) { return Cnew(Radd(z.a, w.a), Radd(z.b, w.b)); }
  function Csub(z, w) { return Cnew(Rsub(z.a, w.a), Rsub(z.b, w.b)); }
  /* (a + bi)(c + di) = (ac - bd) + (ad + bc)i. The minus sign is i^2 = -1 and
     nothing else; it is the only place the definition is used. */
  function Cmul(z, w) {
    return Cnew(Rsub(Rmul(z.a, w.a), Rmul(z.b, w.b)), Radd(Rmul(z.a, w.b), Rmul(z.b, w.a)));
  }
  function Cneg(z) { return Cnew(Rneg(z.a), Rneg(z.b)); }
  function Cconj(z) { return Cnew(z.a, Rneg(z.b)); }
  function Czero(z) { return Rzero(z.a) && Rzero(z.b); }
  function Cequ(z, w) { return Requ(z.a, w.a) && Requ(z.b, w.b); }
  /* z * conj(z) = a^2 + b^2, a RATIONAL number. That fact is the whole method
     for division, so it is computed rather than assumed anywhere below. */
  function Cabs2(z) { return Radd(Rmul(z.a, z.a), Rmul(z.b, z.b)); }
  function Cdiv(z, w) {
    var m = Cabs2(w);
    if (Rzero(m)) return null;
    var t = Cmul(z, Cconj(w));
    return Cnew(Rdiv(t.a, m), Rdiv(t.b, m));
  }
  function Cpow(z, k) { var out = C1, i; for (i = 0; i < k; i += 1) out = Cmul(out, z); return out; }
  /* The imaginary part as a reader writes it: i, -i, 3i, (-3/4)i -- never 1i
     and never 3*i. */
  function Cimtext(b) {
    if (Requ(b, R1)) return 'i';
    if (Requ(b, R(-1n))) return '-i';
    return (Rint(b) ? Rtext(b) : '(' + Rtext(b) + ')') + 'i';
  }
  function Ctext(z) {
    if (Rzero(z.b)) return Rtext(z.a);
    if (Rzero(z.a)) return Cimtext(z.b);
    var mag = Rabs(z.b);
    var piece = Requ(mag, R1) ? 'i' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')') + 'i';
    return Rtext(z.a) + (Rsign(z.b) < 0 ? ' - ' : ' + ') + piece;
  }
  /* |z| exactly: sqrt of a rational, which is rational when it can be and a
     surd when it cannot. sqrt(25) is 5 and belongs on the page as 5. */
  function Cmod(z) { return Rsurd(Cabs2(z)); }
  function Cx(z) { return Rnum(z.a); }
  function Cy(z) { return Rnum(z.b); }
"""

# Presets. Each is (label, a, b, c, d); the modes that need fewer read fewer.
# The failures are on purpose: division by zero in `arith`, and two quadratics
# in `roots` whose discriminant is NOT negative, because a rule is only learned
# next to the case it does not cover.
CX_PRESETS = {
    "intro": [
        ("3 + 4i          the modulus is a whole number", "3", "4", "0", "0"),
        ("1 + i           the modulus is not", "1", "1", "0", "0"),
        ("-2              a real number is a complex number", "-2", "0", "0", "0"),
        ("3i              pure imaginary", "0", "3", "0", "0"),
        ("1/2 - (3/4)i    rational parts stay rational", "1/2", "-3/4", "0", "0"),
        ("i               the number the whole course is about", "0", "1", "0", "0"),
    ],
    "arith": [
        ("z = 3 + 2i,  w = 1 + 4i", "3", "2", "1", "4"),
        ("z = 2 + 3i,  w = 2 - 3i    conjugates", "2", "3", "2", "-3"),
        ("z = 1 + i,   w = 1 + i     squaring", "1", "1", "1", "1"),
        ("z = 5,       w = 2i        where dividing the parts is nonsense", "5", "0", "0", "2"),
        ("z = 1 + 2i,  w = 3 - i     the answer has denominators", "1", "2", "3", "-1"),
        ("z = 1 + i,   w = 0         division by zero", "1", "1", "0", "0"),
    ],
    "roots": [
        ("x^2 + 1              the definition of i, as a root", "1", "0", "1", "0"),
        ("x^2 - 2x + 5         whole-number parts", "1", "-2", "5", "0"),
        ("x^2 + x + 1          the parts are not whole numbers", "1", "1", "1", "0"),
        ("2x^2 - 4x + 3        a leading coefficient that is not 1", "2", "-4", "3", "0"),
        ("x^2 - 4x + 4         discriminant 0: no pair at all", "1", "-4", "4", "0"),
        ("x^2 - 5x + 6         discriminant positive: two real roots", "1", "-5", "6", "0"),
    ],
}

CX_TITLES = {
    "intro": ("The complex plane", "Parts, conjugate, modulus, and the powers of i found by multiplying"),
    "arith": ("Arithmetic with complex numbers", "Add, multiply, conjugate, and divide by the conjugate"),
    "roots": ("The roots a negative discriminant hides", "The conjugate pair, multiplied back into the quadratic it came from"),
}

CX_FIELDS = {
    "intro": [("cxA", "Real part  a"), ("cxB", "Imaginary part  b")],
    "arith": [("cxA", "Re z"), ("cxB", "Im z"), ("cxC", "Re w"), ("cxD", "Im w")],
    "roots": [("cxA", "a  (coefficient of x^2)"), ("cxB", "b  (coefficient of x)"), ("cxC", "c  (constant)")],
}

CX_LEGENDS = {
    "intro": '<span class="tone-amber"><i class="legend-swatch"></i>z</span>'
             '<span class="tone-cyan"><i class="legend-swatch"></i>conjugate</span>'
             '<span class="tone-purple"><i class="legend-swatch"></i>negative</span>',
    "arith": '<span class="tone-amber"><i class="legend-swatch"></i>z and w</span>'
             '<span class="tone-green"><i class="legend-swatch"></i>z + w</span>'
             '<span class="tone-purple"><i class="legend-swatch"></i>z &times; w and z &divide; w</span>',
    "roots": '<span class="tone-green"><i class="legend-swatch"></i>the roots</span>'
             '<span class="tone-muted"><i class="legend-swatch"></i>the real axis</span>',
}


CX_SCRIPT = r"""
  var MODE = '__MODE__', NFIELDS = __NFIELDS__;

  var preset = document.getElementById('cxPreset');
  var inputs = [document.getElementById('cxA'), document.getElementById('cxB')];
  if (NFIELDS > 2) inputs.push(document.getElementById('cxC'));
  if (NFIELDS > 3) inputs.push(document.getElementById('cxD'));
  var work = document.getElementById('cxWork');
  var status = document.getElementById('cxStatus');
  var titleOut = document.getElementById('cxTitle');
  var subOut = document.getElementById('cxSub');
  var svg = document.getElementById('cxPlot');
  var kval = [document.getElementById('cxK1'), document.getElementById('cxK2'), document.getElementById('cxK3')];
  var klab = [document.getElementById('cxK1Lab'), document.getElementById('cxK2Lab'), document.getElementById('cxK3Lab')];
  var LABELS = __LABELS__;

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function row(label, detail) {
    return '<tr><th class="rowhead">' + label + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function focusrow(label, detail) {
    return '<tr class="focus"><th class="rowhead">' + label + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function table(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption
      + '</caption><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  function chip(kind, text) { return '<span class="chip ' + kind + '">' + text + '</span>'; }
  function setkpi(list) {
    for (var i = 0; i < 3; i += 1) { klab[i].textContent = list[i][0]; kval[i].textContent = list[i][1]; }
  }
  /* " + 3i" or " - 6i", never " + -6i" and never "1i". */
  function addend(r, unit) {
    var mag = Rabs(r);
    var body = (Requ(mag, R1) ? '' : (Rint(mag) ? Rtext(mag) : '(' + Rtext(mag) + ')')) + unit;
    return (Rsign(r) < 0 ? ' - ' : ' + ') + body;
  }

  /* Rparse throws on 1/0 rather than returning null, so both outcomes are
     caught here and answered in words. */
  function readR(el, label) {
    var s = String(el.value === undefined || el.value === null ? '' : el.value).trim();
    if (!s) {
      return { ok: false, msg: '<strong>' + label + ' is empty.</strong> Every part here is an exact '
        + 'rational number: type a whole number such as <code>3</code>, a negative such as '
        + '<code>-2</code>, or a fraction such as <code>-3/4</code>.' };
    }
    var v = null;
    try { v = Rparse(s); } catch (err) { v = null; }
    if (v === null) {
      return { ok: false, msg: '<strong>' + label + ' is not a number this lab can hold exactly: &ldquo;'
        + esc(s) + '&rdquo;.</strong> Whole numbers, negatives, decimals and fractions such as '
        + '<code>-3/4</code> all work. A fraction with 0 underneath does not, and neither does a letter '
        + '&mdash; every value here has to be exact, because the whole point is that 1/3 stays 1/3.' };
    }
    return { ok: true, r: v };
  }

  /* One unit is the same number of pixels along both axes, so a right angle in
     the plane is a right angle on the screen. The drawing area is 600 x 370. */
  function argand(points) {
    var xs = [0], ys = [0];
    points.forEach(function (p) {
      if (isFinite(p.x) && isFinite(p.y)) { xs.push(p.x); ys.push(p.y); }
    });
    var xmin = Math.min.apply(null, xs), xmax = Math.max.apply(null, xs);
    var ymin = Math.min.apply(null, ys), ymax = Math.max.apply(null, ys);
    var ratio = 600 / 370;
    var halfY = Math.max((ymax - ymin) / 2, (xmax - xmin) / 2 / ratio, 1) * 1.45;
    var halfX = halfY * ratio;
    var cx = (xmin + xmax) / 2, cy = (ymin + ymax) / 2;
    var plot = Plot(svg, { xmin: cx - halfX, xmax: cx + halfX, ymin: cy - halfY, ymax: cy + halfY });
    plot.frame();
    return plot;
  }

  /* ================================================================= intro */
  function modeIntro(z) {
    var m2 = Cabs2(z), m = Cmod(z);
    var blocks = [];
    blocks.push(table('The number, and its two parts', [
      row('z', Ctext(z)),
      row('real part  Re(z)', Rtext(z.a)),
      row('imaginary part  Im(z)', Rtext(z.b) + (Rzero(z.b)
        ? ' &mdash; there is no imaginary part, which is what makes this a real number'
        : ' &mdash; the imaginary part is the real number ' + Rtext(z.b) + ', not ' + Cimtext(z.b)
          + '. That distinction is the one every later formula relies on.')),
      row('as a point', '(' + Rtext(z.a) + ', ' + Rtext(z.b) + ') on the Argand plane above'),
      row('is it real?', Rzero(z.b) ? chip('ok', 'yes') + ' a real number is the special case b = 0'
        : chip('no', 'no') + ' the imaginary part is ' + Rtext(z.b)),
      row('is it pure imaginary?', Rzero(z.a) && !Rzero(z.b) ? chip('ok', 'yes')
        : chip('no', 'no') + ' the real part is ' + Rtext(z.a))
    ]));

    var conj = Cconj(z), neg = Cneg(z);
    blocks.push(table('Conjugate and negative, and what each one is for', [
      row('conjugate  conj(z)', Ctext(conj) + ' &mdash; the reflection of z in the real axis'),
      row('negative  -z', Ctext(neg) + ' &mdash; the same point turned through half a revolution'),
      row('z + conj(z)', Ctext(Cadd(z, conj)) + ' &mdash; always real, and always 2 &times; Re(z)'),
      row('z - conj(z)', Ctext(Csub(z, conj)) + ' &mdash; always pure imaginary'),
      focusrow('z &times; conj(z)', Rtext(m2) + ' &mdash; always a real number, and equal to '
        + 'a^2 + b^2 = ' + Rtext(Rmul(z.a, z.a)) + ' + ' + Rtext(Rmul(z.b, z.b))
        + '. This is the fact that makes division possible at all.')
    ]));

    var modText = m.k === 1n
      ? surdtext(m) + ' &mdash; exact, because ' + Rtext(m2) + ' is a perfect square'
      : surdtext(m) + ' &mdash; irrational, so this is the answer. Rounded it is about '
        + Math.sqrt(Rnum(m2)).toFixed(6) + ', and that decimal is a rounding of the exact value, not the value.';
    blocks.push(table('Modulus', [
      row('|z|^2 = a^2 + b^2', Rtext(m2)),
      focusrow('|z|', modText),
      row('|conj(z)|', 'the same: reflecting in the real axis cannot change a distance from the origin')
    ]));

    /* The cycle is FOUND by multiplying, not quoted from a table. */
    var pw = C1, irows = [];
    for (var k = 0; k <= 7; k += 1) {
      irows.push(row('i^' + k, Ctext(pw) + (k > 0 ? '  &nbsp;(= i^' + (k - 1) + ' &times; i)' : '  &nbsp;(anything to the power 0)')));
      pw = Cmul(pw, CI);
    }
    blocks.push(table('The powers of i, each one computed from the one before it', irows));

    var zp = C1, zrows = [];
    for (k = 1; k <= 5; k += 1) {
      zp = Cmul(zp, z);
      zrows.push(row('z^' + k, Ctext(zp) + ' &nbsp;&nbsp;|z^' + k + '|^2 = ' + Rtext(Cabs2(zp))));
    }
    blocks.push(table('Powers of z, by repeated multiplication', zrows));

    var pts = [{ x: Cx(z), y: Cy(z) }, { x: Cx(conj), y: Cy(conj) }, { x: Cx(neg), y: Cy(neg) }];
    var plot = argand(pts);
    plot.segment(0, 0, Cx(z), Cy(z), 'plot-aux');
    plot.segment(0, 0, Cx(conj), Cy(conj), 'plot-aux');
    plot.point(Cx(z), Cy(z), 'plot-point', 'z = ' + Ctext(z));
    plot.point(Cx(conj), Cy(conj), 'plot-point root', 'conj(z)');
    plot.point(Cx(neg), Cy(neg), 'plot-point vertex', '-z');
    plot.describe('The Argand plane with z at (' + Rtext(z.a) + ', ' + Rtext(z.b)
      + '), its conjugate reflected in the real axis, and its negative opposite the origin.');

    var msg;
    if (Rzero(z.b)) {
      msg = '<strong>' + Ctext(z) + ' is a real number, and it is also a complex number.</strong> '
        + 'Its imaginary part is 0, it sits on the horizontal axis, and it is its own conjugate. '
        + 'The reals are not a separate system that complex numbers replaced &mdash; they are the '
        + 'horizontal line through the middle of this plane.';
    } else if (Rzero(z.a)) {
      msg = '<strong>' + Ctext(z) + ' is pure imaginary: it sits on the vertical axis.</strong> '
        + 'Squaring it gives ' + Ctext(Cmul(z, z)) + ', a real number, and a negative one. '
        + 'That is the property the reals could not supply and the reason this plane exists.';
    } else {
      msg = '<strong>' + Ctext(z) + ' is at (' + Rtext(z.a) + ', ' + Rtext(z.b) + ') with modulus '
        + surdtext(m) + '.</strong> Look at the powers table: ' + Ctext(z) + ' squared is '
        + Ctext(Cmul(z, z)) + ', and the modulus squared each time &mdash; |z^2|^2 = '
        + Rtext(Cabs2(Cmul(z, z))) + ' = ' + Rtext(m2) + '^2. Multiplying complex numbers multiplies '
        + 'their distances from the origin, which is why the powers march away from or towards 0 and '
        + 'never wander.';
    }
    return {
      title: 'z = ' + Ctext(z),
      sub: 'Re = ' + Rtext(z.a) + ',  Im = ' + Rtext(z.b) + ',  |z| = ' + surdtext(m),
      blocks: blocks,
      status: msg,
      kpi: [['|z|', surdtext(m)], ['z &times; conj(z)', Rtext(m2)], ['z + conj(z)', Ctext(Cadd(z, conj))]]
    };
  }

  /* ================================================================= arith */
  function modeArith(z, w) {
    var sum = Cadd(z, w), diff = Csub(z, w), prod = Cmul(z, w);
    var conj = Cconj(w), m2 = Cabs2(w);
    var quot = Cdiv(z, w);
    var blocks = [];

    blocks.push(table('Adding and subtracting: the parts never mix', [
      row('z + w', '(' + Rtext(z.a) + ' + ' + Rterm(w.a) + ') + (' + Rtext(z.b) + ' + ' + Rterm(w.b)
        + ')i = ' + Ctext(sum)),
      row('z - w', '(' + Rtext(z.a) + ' - ' + Rterm(w.a) + ') + (' + Rtext(z.b) + ' - ' + Rterm(w.b)
        + ')i = ' + Ctext(diff)),
      row('on the plane', 'z + w is the fourth corner of the parallelogram with corners 0, z and w &mdash; '
        + 'drawn above with dashed sides')
    ]));

    var ac = Rmul(z.a, w.a), ad = Rmul(z.a, w.b), bc = Rmul(z.b, w.a), bd = Rmul(z.b, w.b);
    blocks.push(table('Multiplying: ordinary expansion, and then i^2 = -1', [
      row('expand', '(' + Ctext(z) + ')(' + Ctext(w) + ')'),
      row('four products', Rtext(ac) + addend(ad, 'i') + addend(bc, 'i') + addend(bd, 'i^2')),
      focusrow('replace i^2 by -1', 'the i^2 term is ' + Rterm(bd) + ' &times; i^2 = ' + Rterm(bd)
        + ' &times; (-1) = ' + Rtext(Rneg(bd))
        + ', which is why the real part loses bd rather than gaining it'),
      row('collect', 'real: ' + Rtext(ac) + ' - ' + Rterm(bd) + ' = ' + Rtext(Rsub(ac, bd))
        + '&nbsp;&nbsp;&nbsp;imaginary: ' + Rtext(ad) + ' + ' + Rterm(bc) + ' = ' + Rtext(Radd(ad, bc))),
      focusrow('z &times; w', Ctext(prod))
    ]));

    var r3 = [
      row('conj(w)', Ctext(conj)),
      focusrow('w &times; conj(w)', Rtext(m2) + ' &mdash; a real number, computed as '
        + Rtext(Rmul(w.a, w.a)) + ' + ' + Rtext(Rmul(w.b, w.b)))
    ];
    if (quot === null) {
      r3.push(row('divide by it?', chip('no', 'not possible')
        + ' w is 0, so conj(w) is 0 and w &times; conj(w) is 0. The trick turns the bottom into a real '
        + 'number, and here that real number is 0 &mdash; which is exactly as forbidden in the complex '
        + 'numbers as it is in the reals. Adding i did not repeal division by zero.'));
    } else {
      var t = Cmul(z, conj);
      r3.push(row('multiply top and bottom by conj(w)', '(' + Ctext(z) + ')(' + Ctext(conj)
        + ') over (' + Ctext(w) + ')(' + Ctext(conj) + ')'));
      r3.push(row('numerator', Ctext(t)));
      r3.push(row('denominator', Rtext(m2) + ' &mdash; real, so the division is now two ordinary divisions'));
      r3.push(focusrow('z &divide; w', '(' + Ctext(t) + ') / ' + Rtext(m2)
        + ' &mdash; divide each part by ' + Rtext(m2) + ' &mdash; = ' + Ctext(quot)));
    }
    blocks.push(table('Dividing: turn the bottom into a real number', r3));

    if (quot !== null) {
      var back = Cmul(quot, w);
      blocks.push(table('Check the division by undoing it', [
        row('(z &divide; w) &times; w', '(' + Ctext(quot) + ')(' + Ctext(w) + ') = ' + Ctext(back)),
        row('z', Ctext(z)),
        focusrow('equal?', Cequ(back, z)
          ? chip('ok', 'yes') + ' the product was computed from the quotient without looking at z, so '
            + 'this is a check rather than a restatement'
          : chip('no', 'no') + ' this should never appear')
      ]));
    }

    var pts = [{ x: Cx(z), y: Cy(z) }, { x: Cx(w), y: Cy(w) }, { x: Cx(sum), y: Cy(sum) },
               { x: Cx(prod), y: Cy(prod) }];
    if (quot !== null) pts.push({ x: Cx(quot), y: Cy(quot) });
    var plot = argand(pts);
    plot.segment(0, 0, Cx(z), Cy(z), 'plot-aux');
    plot.segment(0, 0, Cx(w), Cy(w), 'plot-aux');
    plot.segment(Cx(z), Cy(z), Cx(sum), Cy(sum), 'plot-aux');
    plot.segment(Cx(w), Cy(w), Cx(sum), Cy(sum), 'plot-aux');
    plot.point(Cx(z), Cy(z), 'plot-point', 'z');
    plot.point(Cx(w), Cy(w), 'plot-point', 'w');
    plot.point(Cx(sum), Cy(sum), 'plot-point root', 'z + w');
    plot.point(Cx(prod), Cy(prod), 'plot-point vertex', 'z x w');
    if (quot !== null) plot.point(Cx(quot), Cy(quot), 'plot-point vertex', 'z / w');
    plot.describe('The Argand plane with z, w, their sum at the fourth corner of a parallelogram, '
      + 'their product and their quotient.');

    var msg;
    if (quot === null) {
      msg = '<strong>w = 0, so z &divide; w does not exist.</strong> Everything else on this page still '
        + 'works: the sum is ' + Ctext(sum) + ' and the product is ' + Ctext(prod) + ', which is 0 '
        + 'because a product is 0 exactly when one of its factors is. Division is the one operation '
        + 'complex numbers did not make more forgiving, and a lab that quietly printed a number here '
        + 'would be teaching the opposite of that.';
    } else if (Rzero(w.a) && !Rzero(w.b)) {
      msg = '<strong>Dividing by ' + Ctext(w) + ': the obvious wrong move is to divide the parts.</strong> '
        + 'Re(z)/Re(w) is ' + Rtext(z.a) + '/0, which is not a number, and yet z &divide; w = '
        + Ctext(quot) + ' is perfectly ordinary. Division is not done part by part; it is done by '
        + 'multiplying above and below by conj(w) = ' + Ctext(conj) + ', which turns the bottom into the '
        + 'real number ' + Rtext(m2) + '.';
    } else if (Cequ(z, Cconj(w)) || Requ(prod.b, R0)) {
      msg = '<strong>' + Ctext(z) + ' times ' + Ctext(w) + ' is ' + Ctext(prod)
        + ', a real number.</strong> Two numbers that are not real multiplied to one that is: the '
        + 'imaginary parts, ' + Rtext(ad) + ' and ' + Rtext(bc) + ', cancelled. That is not a '
        + 'coincidence when w is the conjugate of z, and it is the mechanism the division below uses.';
    } else {
      msg = '<strong>z &times; w = ' + Ctext(prod) + ' and z &divide; w = ' + Ctext(quot) + '.</strong> '
        + 'Both parts of the quotient are exact fractions over ' + Rtext(m2) + ', which is w &times; conj(w). '
        + 'The multiplication row above shows where the minus sign in the real part comes from: it is '
        + 'the single substitution i^2 = -1, applied once.';
    }
    return {
      title: 'z = ' + Ctext(z) + ',  w = ' + Ctext(w),
      sub: 'z + w = ' + Ctext(sum) + ',  z x w = ' + Ctext(prod),
      blocks: blocks,
      status: msg,
      kpi: [['z &times; w', Ctext(prod)], ['z &divide; w', quot === null ? 'undefined' : Ctext(quot)],
            ['Check', quot === null ? 'n/a' : (Cequ(Cmul(quot, w), z) ? 'passes' : 'FAILS')]]
    };
  }

  /* ================================================================= roots */
  function modeRoots(a, b, c) {
    if (Rzero(a)) {
      return { fail: '<strong>With a = 0 this is not a quadratic, so there is no pair of roots to find.</strong> '
        + Ptext([c, b]) + ' = 0 is linear and has one solution. Every formula below divides by a, which '
        + 'is precisely why the definition of a quadratic insists a is not 0.' };
    }
    var r = quadroots(a, b, c);
    var poly = [c, b, a];
    /* s^2, where each root is p +- s (times i when the discriminant is
       negative). It is rational whichever case we are in, which is what makes
       the sum and product of the pair rational as well. */
    var sq = Rmul(Rmul(r.s.q, r.s.q), R(BigInt(r.s.k)));
    var sum = Rmul(R(2n), r.p);
    var prod = r.kind === 'complex' ? Radd(Rmul(r.p, r.p), sq) : Rsub(Rmul(r.p, r.p), sq);
    var rootText = r.kind === 'complex' ? pmtext(r.p, r.s, true) : pmtext(r.p, r.s);
    var blocks = [];

    blocks.push(table('Step 1 &middot; the discriminant decides which world the roots live in', [
      row('the quadratic', Ptext(poly) + ' = 0'),
      row('b^2 - 4ac', Rtext(Rmul(b, b)) + ' - ' + Rtext(Rmul(R(4n), Rmul(a, c))) + ' = ' + Rtext(r.disc)),
      focusrow('verdict', r.kind === 'complex'
        ? chip('hi', 'negative') + ' no real root, and exactly two complex ones'
        : (r.kind === 'double'
            ? chip('no', 'zero') + ' one repeated REAL root, and no complex pair at all'
            : chip('no', 'positive') + ' two REAL roots, and again no complex pair'))
    ]));

    var r2 = [
      row('x = (-b +- sqrt(b^2 - 4ac)) / 2a', '(' + Rtext(Rneg(b)) + ' +- sqrt(' + Rtext(r.disc)
        + ')) / ' + Rtext(Rmul(R(2n), a)))
    ];
    if (r.kind === 'complex') {
      r2.push(row('sqrt of a negative', 'sqrt(' + Rtext(r.disc) + ') = sqrt(' + Rtext(Rneg(r.disc))
        + ') &middot; i = ' + surdtext(Rsurd(Rneg(r.disc))) + 'i &mdash; this is the step that needs i to exist'));
      r2.push(focusrow('the conjugate pair', 'x = ' + rootText));
      var imtxt = surdtext(r.s);
      var imwhole = imtxt === '1' ? 'i' : imtxt + 'i';
      r2.push(row('the two roots, separately',
        'r1 = ' + (Rzero(r.p) ? imwhole : Rtext(r.p) + ' + ' + imwhole)
        + '&nbsp;&nbsp;&nbsp;r2 = ' + (Rzero(r.p) ? '-' + imwhole : Rtext(r.p) + ' - ' + imwhole)));
      r2.push(row('why they come in pairs', 'a, b and c are real, so conjugating the whole equation '
        + 'changes nothing on the right and turns one root into the other. A real quadratic cannot have '
        + 'just one non-real root.'));
    } else if (r.kind === 'double') {
      r2.push(focusrow('one repeated root', 'x = ' + Rtext(r.p)));
    } else {
      r2.push(focusrow('two real roots', 'x = ' + rootText));
    }
    blocks.push(table('Step 2 &middot; the roots', r2));

    /* The proof: multiply the pair back together and see the quadratic
       reappear. Sum and product are computed from p and s alone. */
    var monic = [prod, Rneg(sum), R1];
    var rebuilt = Pscale(monic, a);
    var same = Pzero(Psub(rebuilt, Pnorm(poly)));
    var r3 = [
      row('(x - r1)(x - r2)', 'x^2 - (r1 + r2)x + r1&middot;r2'),
      row('r1 + r2', r.kind === 'complex'
        ? '(' + Rtext(r.p) + ' + ' + surdtext(r.s) + 'i) + (' + Rtext(r.p) + ' - ' + surdtext(r.s)
          + 'i) = ' + Rtext(sum) + ' &mdash; the imaginary parts cancel'
        : Rtext(sum)),
      row('r1 &middot; r2', r.kind === 'complex'
        ? '(' + Rtext(r.p) + ')^2 + (' + surdtext(r.s) + ')^2 = ' + Rtext(Rmul(r.p, r.p)) + ' + '
          + Rtext(sq) + ' = ' + Rtext(prod)
          + ' &mdash; a difference of squares with i^2 = -1 in it, so the two minus signs make a plus'
        : Rtext(Rmul(r.p, r.p)) + ' - ' + Rtext(sq) + ' = ' + Rtext(prod)),
      row('so the monic quadratic is', Ptext(monic) + ' = 0'),
      row('multiply by a = ' + Rtext(a), Ptext(rebuilt)),
      focusrow('is that the quadratic we started with?', same
        ? chip('ok', 'yes') + ' ' + Ptext(rebuilt) + ' is exactly ' + Ptext(poly)
          + '. The roots were built from a, b and c; multiplying them back reproduces a, b and c, and '
          + 'nothing in between was copied from anything else.'
        : chip('no', 'no') + ' this should never appear')
    ];
    blocks.push(table('Step 3 &middot; multiply the roots back together', r3));

    var vietaSum = Rdiv(Rneg(b), a), vietaProd = Rdiv(c, a);
    blocks.push(table('Step 4 &middot; the same two numbers, straight from the coefficients', [
      row('-b/a', Rtext(vietaSum)),
      row('r1 + r2 from step 3', Rtext(sum)),
      row('c/a', Rtext(vietaProd)),
      row('r1 &middot; r2 from step 3', Rtext(prod)),
      focusrow('agree?', (Requ(vietaSum, sum) && Requ(vietaProd, prod))
        ? chip('ok', 'both') + ' two independent routes to the sum and the product of the roots, '
          + 'and they land on the same rationals'
        : chip('no', 'no') + ' this should never appear')
    ]));

    var pts = [];
    var im = Rnum(r.s.q) * Math.sqrt(Number(r.s.k));
    if (r.kind === 'complex') {
      pts.push({ x: Rnum(r.p), y: im }, { x: Rnum(r.p), y: -im });
    } else if (r.kind === 'double') {
      pts.push({ x: Rnum(r.p), y: 0 });
    } else {
      pts.push({ x: Rnum(r.p) + im, y: 0 }, { x: Rnum(r.p) - im, y: 0 });
    }
    var plot = argand(pts);
    if (r.kind === 'complex') {
      plot.segment(0, 0, Rnum(r.p), im, 'plot-aux');
      plot.segment(0, 0, Rnum(r.p), -im, 'plot-aux');
      plot.segment(Rnum(r.p), im, Rnum(r.p), -im, 'plot-aux');
      plot.point(Rnum(r.p), im, 'plot-point root', rootText);
      plot.point(Rnum(r.p), -im, 'plot-point root', '');
    } else if (r.kind === 'double') {
      plot.point(Rnum(r.p), 0, 'plot-point root', 'x = ' + Rtext(r.p));
    } else if (r.kind === 'rational') {
      plot.point(Rnum(r.p) + im, 0, 'plot-point root', Rtext(Radd(r.p, r.s.q)));
      plot.point(Rnum(r.p) - im, 0, 'plot-point root', Rtext(Rsub(r.p, r.s.q)));
    } else {
      /* An irrational root has no finite decimal, so the point is labelled with
         a rounding and says so with the ~. The exact value is in step 2. */
      plot.point(Rnum(r.p) + im, 0, 'plot-point root', '~' + (Rnum(r.p) + im).toFixed(3));
      plot.point(Rnum(r.p) - im, 0, 'plot-point root', '~' + (Rnum(r.p) - im).toFixed(3));
    }
    plot.describe('The Argand plane with the roots of ' + Ptext(poly) + ' marked'
      + (r.kind === 'complex' ? ' as a conjugate pair either side of the real axis.' : ' on the real axis.')
      + (r.kind === 'irrational' ? ' The point labels are rounded to three places; the exact roots are '
          + rootText + '.' : ''));

    var msg;
    if (r.kind === 'complex') {
      msg = '<strong>The discriminant is ' + Rtext(r.disc) + ', so the roots are ' + rootText + '.</strong> '
        + 'They are a conjugate pair: same real part, opposite imaginary parts, mirror images in the '
        + 'real axis. Step 3 is the part worth dwelling on &mdash; multiplying them back together gives '
        + Ptext(rebuilt) + ', the quadratic you typed, with every trace of i gone. '
        + 'The pair sums to the real number ' + Rtext(sum) + ' and multiplies to the real number '
        + Rtext(prod) + ', which is how two non-real numbers can be the roots of an equation with '
        + 'nothing imaginary anywhere in it.';
    } else if (r.kind === 'double') {
      msg = '<strong>The discriminant is exactly 0, so there is no conjugate pair here at all.</strong> '
        + 'There is one repeated real root, x = ' + Rtext(r.p) + '. This preset is in the list to make '
        + 'the hypothesis visible: &ldquo;complex roots come in conjugate pairs&rdquo; is a statement '
        + 'about a NEGATIVE discriminant, and this one is not negative. Step 3 still works &mdash; the '
        + '&ldquo;pair&rdquo; is that root twice, and multiplying it back still rebuilds ' + Ptext(rebuilt) + '.';
    } else {
      msg = '<strong>The discriminant is ' + Rtext(r.disc) + ', which is positive: two real roots, '
        + rootText + ', and no complex pair.</strong> Nothing here needs i. That is worth seeing next '
        + 'to the presets that do: complex roots are not what happens when a quadratic is difficult, '
        + 'they are what happens when b^2 is smaller than 4ac. Step 3 rebuilds ' + Ptext(rebuilt)
        + ' from these two real roots by exactly the same arithmetic.';
    }
    return {
      title: Ptext(poly) + ' = 0',
      sub: 'x = ' + rootText,
      blocks: blocks,
      status: msg,
      kpi: [['Discriminant', Rtext(r.disc)], ['Roots', rootText],
            ['r1 &middot; r2', Rtext(prod)]]
    };
  }

  /* ================================================================ driver */
  function fail(msg) {
    status.innerHTML = msg;
    work.innerHTML = table('Nothing computed yet', [
      row('waiting for', 'exact rational values in every box above'),
      row('values that work', '<code>3</code>, <code>-2</code>, <code>1/2</code>, <code>-3/4</code>, <code>0.25</code>')
    ]);
    titleOut.textContent = 'Nothing to show';
    subOut.textContent = 'fix the values above';
    svg.textContent = '';
    setkpi([['Status', '--'], ['Status', '--'], ['Status', '--']]);
  }

  function redraw() {
    var vals = [];
    for (var i = 0; i < inputs.length; i += 1) {
      var got = readR(inputs[i], LABELS[i]);
      if (!got.ok) { fail(got.msg); return; }
      vals.push(got.r);
    }
    var out;
    try {
      if (MODE === 'intro') out = modeIntro(Cnew(vals[0], vals[1]));
      else if (MODE === 'arith') out = modeArith(Cnew(vals[0], vals[1]), Cnew(vals[2], vals[3]));
      else out = modeRoots(vals[0], vals[1], vals[2]);
    } catch (err) {
      fail('<strong>Those values are more than this lab can carry: ' + (err && err.message) + '.</strong> '
        + 'Everything here is exact rational arithmetic over BigInt, and a few inputs &mdash; enormous '
        + 'numerators, denominators of 0 &mdash; run past what it will do. Try a preset and edit it a '
        + 'little at a time.');
      return;
    }
    if (out.fail) { fail(out.fail); return; }
    titleOut.innerHTML = out.title;
    subOut.textContent = out.sub;
    work.innerHTML = out.blocks.join('');
    status.innerHTML = out.status;
    setkpi(out.kpi);
  }

  function loadPreset() {
    var parts = String(preset.value).split('|');
    for (var i = 0; i < inputs.length; i += 1) inputs[i].value = parts[i] === undefined ? '0' : parts[i];
  }
  preset.addEventListener('change', function () { loadPreset(); redraw(); });
  inputs.forEach(function (el) { el.addEventListener('input', redraw); });
  loadPreset();
  redraw();
  window.redrawLab = redraw;
"""


def complex_lab(cfg):
    """Complex numbers, with exact rational real and imaginary parts.

    The teaching decision: a + bi is carried as a PAIR of exact rationals and
    never as a float, because every claim this lab makes is an equality --
    z * conj(z) is real, the two roots multiply back to the quadratic, dividing
    and then multiplying by w returns z. Each of those is checked by comparing
    two numbers, and floating point would turn every check into "close enough",
    which is not a thing a reader can be taught to trust.

    In `roots`, the conjugate pair is p +- q*sqrt(k) i with p and q rational and
    k squarefree, so the sum (2p) and the product (p^2 + q^2 k) come out
    rational and can be compared, exactly, against -b/a and c/a formed straight
    from the coefficients. Two of the six presets have a discriminant that is
    not negative, because the rule only means something beside the case it
    does not cover.
    """
    mode = cfg.get("mode", "intro")
    if mode not in CX_PRESETS:
        mode = "intro"
    presets = cfg.get("presets") or CX_PRESETS[mode]
    title, subtitle = CX_TITLES[mode]
    fields = CX_FIELDS[mode]

    options = "".join(
        '<option value="' + a + "|" + b + "|" + c + "|" + d + '">' + label + "</option>"
        for label, a, b, c, d in presets
    )
    field_markup = "".join(
        '        <div class="field" id="' + fid + 'Field">\n'
        '          <label for="' + fid + '">' + flabel + "</label>\n"
        '          <input id="' + fid + '" type="text" value="0" inputmode="text" autocomplete="off">\n'
        "        </div>\n"
        for fid, flabel in fields
    )

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="cxTitle">Complex numbers</strong>'
        '<span id="cxSub"></span></div>\n'
        '        <div class="inline-legend">' + CX_LEGENDS[mode] + "</div>\n"
        "      </div>\n"
        '      <div class="lab-stage" id="cxStage"><svg id="cxPlot"></svg></div>\n'
        '      <div id="cxWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="cxStatus" style="margin-top:12px;"></div>'
    )

    controls = (
        '        <div class="field" id="cxFieldPreset">\n'
        '          <label for="cxPreset">Worked example</label>\n'
        '          <select id="cxPreset">' + options + "</select>\n"
        "        </div>\n"
        + field_markup
        + '        <div class="kpi-grid">\n'
        '          <div class="kpi"><span id="cxK1Lab">&mdash;</span><strong id="cxK1">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="cxK2Lab">&mdash;</span><strong id="cxK2">&mdash;</strong></div>\n'
        '          <div class="kpi"><span id="cxK3Lab">&mdash;</span><strong id="cxK3">&mdash;</strong></div>\n'
        "        </div>\n"
        '        <p class="small-copy" id="cxHint" style="margin:0;">Every box takes a whole number or an '
        "exact fraction such as <code>-3/4</code>. Nothing below is rounded except where it says so, "
        "and the Argand plane draws the numbers the tables computed.</p>"
    )

    labels_js = "[" + ", ".join(
        "'" + flabel.replace("'", "\\'") + "'" for _, flabel in fields
    ) + "]"

    script = (
        RATIONAL_JS + POLY_JS + SURD_JS + PLOT_JS + CX_JS
        + CX_SCRIPT
        .replace("__MODE__", mode)
        .replace("__NFIELDS__", str(len(fields)))
        .replace("__LABELS__", labels_js)
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a worked example, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "Real and imaginary parts are held as exact fractions, so every equality below "
            "is checked rather than approximated. The plane above draws the numbers the "
            "tables computed, from the same values.",
        ),
        script=script,
    )
