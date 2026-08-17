"""Course 2: the moves that keep a statement true, made visible.

Two labs live here because they are one lesson twice. `equation_lab` and
`inequality_lab` share a single routine, `traceLinear`, that applies one
operation to BOTH sides and names it -- and the only difference between solving
3x - 4 = 11 and solving 3x - 4 < 11 is what that routine does in the divide step
when the coefficient is negative. Sharing the code is the argument: a reader can
see that the step list is identical and that exactly one line in it changes.

The teaching decision behind `equation_lab` is that a step trace is only half a
lesson. A trace can be followed and still be wrong, so every mode that produces
an answer then SUBSTITUTES that answer back into the equation as the reader
typed it -- the original tree, not the simplified one -- and evaluates both
sides in exact rationals. When the two sides come out equal the check is a
proof, not a plausibility argument, which is the whole reason the arithmetic is
rational rather than floating point. The substitution is also what makes the
absolute-value and proportion modes honest: both can produce a candidate that
survives the algebra and fails the check, and a lab that never checked would
report those extraneous values as answers.

The teaching decision behind `inequality_lab` is that an inequality's answer is
a SET, so the lab computes sets rather than describing them. Intervals with
exact endpoints are intersected and unioned by code, drawn on a number line from
those same endpoints, and printed in interval and set-builder notation from the
same structure -- so the four representations on screen cannot disagree with one
another. The sign reversal gets its own row in the trace, with its reason, and
every mode ends by testing exact sample values against the ORIGINAL statement:
a reversed sign is invisible in the algebra and obvious in the test.

Nothing here is precomputed. Every coefficient is parsed from what the controls
hold, every step is derived, and the presets are equations rather than answers.
Floating point appears only in the plotting windows and in choosing WHERE to
look for a test point in the quadratic sign analysis -- the sign itself is then
established exactly, at an exact rational, and irrational endpoints are carried
as p +- q*sqrt(k) throughout.
"""

import re

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# --------------------------------------------------------------------------
# Shared JavaScript. Both labs read algebra the reader typed, print it back,
# evaluate it exactly, and show one operation being applied to both sides.
# --------------------------------------------------------------------------

FORM_JS = r"""
  /* ---------------------------------------------------------- presentation */
  function trow(label, detail, cls) {
    return '<tr' + (cls ? ' class="' + cls + '"' : '') + '><th class="rowhead">' + label
      + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function ttable(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption
      + '</caption><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  function chip(text, kind) { return '<span class="chip ' + kind + '">' + text + '</span>'; }
  /* Wider tables -- a sign row, a set of test values -- need real columns. */
  function tcells(items, cls) {
    return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>'
      + items.map(function (t) { return '<td style="text-align:left;">' + t + '</td>'; }).join('') + '</tr>';
  }
  function tgrid(caption, head, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption><thead><tr>'
      + head.map(function (t) { return '<th>' + t + '</th>'; }).join('')
      + '</tr></thead><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  var YES = chip('true', 'ok'), NO = chip('false', 'no');

  /* Rparse throws on a zero denominator, and "1/0" is four keystrokes. Every
     reader-facing parse goes through this instead. */
  function parseR(text) {
    try { return Rparse(text); } catch (err) { return null; }
  }

  /* ------------------------------------------------- what the reader typed */
  /* A side is kept BOTH ways: as a polynomial, which is what gets solved, and
     as the tree it was typed as, which is what a substitution has to be shown
     in. Normalising first and substituting into the normalised form would show
     the reader a check on an equation they did not write. */
  function sideOf(text, v, what) {
    var s = String(text === null || text === undefined ? '' : text).trim();
    if (!s) {
      return { ok: false, msg: 'the ' + what + ' is empty. Type an expression such as <code>2x + 1</code>.' };
    }
    var node;
    try { node = Eparse(s); } catch (err) {
      return { ok: false, msg: 'the ' + what + ', <code>' + s + '</code>, could not be read: ' + err.message + '.' };
    }
    var poly;
    try { poly = Epoly(node, v); } catch (err) {
      return { ok: false, msg: 'the ' + what + ', <code>' + s + '</code>, divides by zero somewhere.' };
    }
    if (poly === null) {
      return { ok: false, msg: 'the ' + what + ', <code>' + s + '</code>, is not a polynomial in ' + v
        + '. It may use another letter, or put ' + v + ' under a root or in a denominator, and this lab '
        + 'solves for one letter at a time.' };
    }
    return { ok: true, node: node, poly: poly, src: s };
  }

  /* ------------------------------------------- exact value of a typed tree */
  /* Rational wherever the value is rational, and null wherever it is not --
     an irrational root, a logarithm, a zero denominator. Every caller says so
     rather than printing a number it does not actually have. This is what
     turns "substitute and check" into a proof. */
  function Reval(node, env) {
    var a, b;
    switch (node.k) {
      case 'num': return Rparse(node.v);
      case 'var': return (env && Object.prototype.hasOwnProperty.call(env, node.v)) ? env[node.v] : null;
      case 'neg': a = Reval(node.a, env); return a === null ? null : Rneg(a);
      case 'add': case 'sub': case 'mul':
        a = Reval(node.a, env); b = Reval(node.b, env);
        if (a === null || b === null) return null;
        return node.k === 'add' ? Radd(a, b) : (node.k === 'sub' ? Rsub(a, b) : Rmul(a, b));
      case 'div':
        a = Reval(node.a, env); b = Reval(node.b, env);
        if (a === null || b === null || Rzero(b)) return null;
        return Rdiv(a, b);
      case 'pow':
        a = Reval(node.a, env); b = Reval(node.b, env);
        if (a === null || b === null || !Rint(b)) return null;
        if (b.n > 40n || b.n < -40n) return null;
        if (Rzero(a) && b.n <= 0n) return null;
        return Rpow(a, Number(b.n));
      case 'fn':
        a = Reval(node.a, env);
        if (a === null) return null;
        if (node.v === 'abs') return Rabs(a);
        if (node.v === 'sqrt') return Rsqrt(a);   /* null unless it comes out exact */
        return null;
    }
    return null;
  }
  function varsOf(node, out) {
    out = out || {};
    if (node.k === 'var') out[node.v] = 1;
    if (node.a) varsOf(node.a, out);
    if (node.b) varsOf(node.b, out);
    return out;
  }

  /* ------------------------------------------------- printing a tree back */
  /* `env` may map a letter to the text that stands in for it, which is how a
     substitution is SHOWN before it is worked out: 3(5/2) - 4 is the line a
     reader would write, and it is produced from the tree rather than by string
     surgery on the source, so a variable named t cannot corrupt sqrt(). */
  function atomtext(s) { return /^[A-Za-z0-9.]+$/.test(s) || /^\([^()]*\)$/.test(s); }
  function etext(n, env, need) {
    var s, lvl = 4;
    switch (n.k) {
      case 'num': s = n.v; lvl = atomtext(s) ? 4 : 1; break;
      case 'var': s = (env[n.v] !== undefined) ? env[n.v] : n.v; lvl = atomtext(s) ? 4 : 1; break;
      case 'neg': s = '-' + etext(n.a, env, 2); lvl = 1; break;
      case 'add': s = etext(n.a, env, 1) + ' + ' + etext(n.b, env, 1); lvl = 1; break;
      case 'sub': s = etext(n.a, env, 1) + ' - ' + etext(n.b, env, 2); lvl = 1; break;
      case 'mul': {
        /* a quotient inside a product is always bracketed: 3/4(1) can be read
           as (3/4)*1 or as 3/(4*1), and only one of them is what was typed */
        var l = etext(n.a, env, n.a.k === 'div' ? 3 : 2),
            r = etext(n.b, env, n.b.k === 'div' ? 3 : 2);
        /* juxtaposition where it reads as a product, an explicit * where
           2 followed by 3 would read as twenty-three */
        s = l + (/^[0-9.]/.test(r) ? '*' : '') + r; lvl = 2; break;
      }
      case 'div': s = etext(n.a, env, 2) + '/' + etext(n.b, env, 3); lvl = 2; break;
      case 'pow': s = etext(n.a, env, 3) + '^' + etext(n.b, env, 4); lvl = 3; break;
      case 'fn': s = n.v + '(' + etext(n.a, env, 0) + ')'; lvl = 4; break;
      default: s = '?';
    }
    return lvl < need ? '(' + s + ')' : s;
  }
  function Etext(node, env) { return etext(node, env || {}, 0); }
  /* The tree with one letter replaced by a value, bracketed so -3/2 cannot
     glue onto whatever precedes it. */
  function Esub(node, v, value) {
    var env = {};
    env[v] = '(' + Rtext(value) + ')';
    return etext(node, env, 0);
  }

  /* --------------------------------------- one operation, applied to both */
  var RELTEXT = { '=': '=', '<': '&lt;', '<=': '&le;', '>': '&gt;', '>=': '&ge;' };
  function relText(rel) { return RELTEXT[rel] || rel; }
  /* Reading a statement from the other end. 6 &lt; x and x &gt; 6 are the same
     statement; this is NOT the reversal that multiplying by a negative causes,
     and the trace says which is which wherever it uses this. */
  function relSwap(rel) {
    return rel === '<' ? '>' : (rel === '<=' ? '>=' : (rel === '>' ? '<' : (rel === '>=' ? '<=' : '=')));
  }
  function relHolds(a, b, rel) {
    var c = Rcmp(a, b);
    if (rel === '=') return c === 0;
    if (rel === '<') return c < 0;
    if (rel === '<=') return c <= 0;
    if (rel === '>') return c > 0;
    if (rel === '>=') return c >= 0;
    return false;
  }
  function relName(rel) {
    if (rel === '=') return 'equation';
    return 'inequality';
  }
  function lcmden(poly) {
    var d = 1n;
    Pnorm(poly).forEach(function (c) { d = d * c.d / bgcd(d, c.d); });
    return d;
  }
  function lcdOf(a, b) {
    var x = lcmden(a), y = lcmden(b);
    return x * y / bgcd(x, y);
  }

  /* The trace. Each entry is one operation applied to BOTH sides, named, with
     the statement as it stands afterwards. The reversal in the divide step is
     the only line that differs between an equation and an inequality, and it
     carries its own reason so it cannot be read as a typing slip.

     `collectLeft` decides which side the variable is gathered on. It is a
     parameter rather than a convention because the choice is itself a lesson:
     both work, and one of them avoids a negative coefficient. */
  function traceLinear(L0, R0p, v, rel, collectLeft) {
    var L = Pnorm(L0), Rr = Pnorm(R0p), steps = [], rl = rel;
    function push(op, note) {
      steps.push({
        op: op, note: note || '',
        text: Ptext(L, v) + ' ' + relText(rl) + ' ' + Ptext(Rr, v)
      });
    }
    push('expand and collect each side');

    var den = lcdOf(L, Rr);
    if (den > 1n) {
      L = Pscale(L, R(den)); Rr = Pscale(Rr, R(den));
      push('multiply both sides by ' + den,
           'the least common denominator of every coefficient, which clears all of them at once');
    }

    var from = collectLeft ? Rr : L;
    var k = from.length > 1 ? from[1] : R0;
    if (!Rzero(k)) {
      var term = [R0, k];
      L = Psub(L, term); Rr = Psub(Rr, term);
      push(Rsign(k) > 0
        ? 'subtract ' + Ptext(term, v) + ' from both sides'
        : 'add ' + Ptext(Pscale(term, R(-1n)), v) + ' to both sides');
    }

    var keepOn = collectLeft ? L : Rr;
    var c0 = keepOn.length ? keepOn[0] : R0;
    if (!Rzero(c0)) {
      var cterm = [c0];
      L = Psub(L, cterm); Rr = Psub(Rr, cterm);
      push(Rsign(c0) > 0
        ? 'subtract ' + Rtext(c0) + ' from both sides'
        : 'add ' + Rtext(Rneg(c0)) + ' to both sides');
    }

    var side = collectLeft ? L : Rr, other = collectLeft ? Rr : L;
    var a = side.length > 1 ? side[1] : R0;
    if (Rzero(a)) {
      /* Every v cancelled. What is left is a statement about two numbers, and
         it is either true for every v or for none -- never "v = 0". */
      var lc = L.length ? L[0] : R0, rc = Rr.length ? Rr[0] : R0;
      var holds = relHolds(lc, rc, rl);
      return {
        steps: steps, kind: holds ? 'all' : 'none', rel: rl,
        constText: Rtext(lc) + ' ' + relText(rl) + ' ' + Rtext(rc)
      };
    }

    var value = Rdiv(other.length ? other[0] : R0, a);
    var flipped = Rsign(a) < 0 && rel !== '=';
    var before = rl;
    if (flipped) rl = relSwap(rl);
    var wasOne = Requ(a, R1);
    if (collectLeft) { L = [R0, R1]; Rr = [value]; } else { L = [value]; Rr = [R0, R1]; }
    /* Dividing by 1 is not a step. Printing it as one teaches a reader to
       write a line down whether or not anything happened on it. */
    if (!wasOne) push('divide both sides by ' + Rtext(a),
      (flipped ? '<strong>' + Rtext(a) + ' is negative, so the statement reverses: '
                 + relText(before) + ' becomes ' + relText(rl) + '.</strong> '
               : '')
      + (Rint(a) ? '' : 'the same move as multiplying both sides by ' + Rtext(Rinv(a)) + '.'));

    if (!collectLeft) {
      var readAs = relSwap(rl);
      rl = readAs;
      L = [R0, R1]; Rr = [value];
      push('read it from the other end',
           'the same statement written the usual way round, with ' + v + ' on the left. '
           + 'Nothing was multiplied here, so this is not the reversal rule.');
    }
    return { steps: steps, kind: 'unique', value: value, rel: rl, coef: a, flipped: flipped };
  }

  /* `typed` is the statement as the reader wrote it. When the first step
     produces exactly that, no expanding or collecting happened and the row is
     dropped rather than shown as a step that did nothing. */
  function traceRows(trace, typed) {
    var steps = trace.steps;
    if (typed && steps.length && steps[0].text === typed) steps = steps.slice(1);
    return steps.map(function (s) {
      return trow(s.op, '<code>' + s.text + '</code>' + (s.note ? '<br><span class="small-copy">' + s.note + '</span>' : ''));
    });
  }

  /* A polynomial as a function of a float, for drawing only. */
  function polyFn(p) {
    var cs = Pnorm(p).map(Rnum);
    return function (x) {
      var acc = 0;
      for (var i = cs.length - 1; i >= 0; i -= 1) acc = acc * x + cs[i];
      return acc;
    };
  }
  function niceWindow(xs, minSpan) {
    var pts = xs.filter(function (x) { return isFinite(x); });
    var lo = pts.length ? Math.min.apply(null, pts) : 0;
    var hi = pts.length ? Math.max.apply(null, pts) : 0;
    var c = (lo + hi) / 2, span = Math.max(minSpan || 8, (hi - lo) * 2.4);
    return { xmin: c - span / 2, xmax: c + span / 2 };
  }
"""


# --------------------------------------------------------------------------
# Symbolic machinery, used only by the literal-equation mode. A formula solved
# for one of its letters has an ANSWER that is an expression, so the lab needs
# to do algebra on trees rather than on polynomials.
# --------------------------------------------------------------------------

SYMBOL_JS = r"""
  var ZEROND = { k: 'num', v: '0' }, ONEND = { k: 'num', v: '1' };
  function Enum(r) { return { k: 'num', v: Rtext(r) }; }
  function Econst(node) { return Reval(node, {}); }
  function isZeroND(n) { var c = Econst(n); return c !== null && Rzero(c); }
  function isOneND(n) { var c = Econst(n); return c !== null && Requ(c, R1); }

  /* Tidy a tree without changing what it means. A constant subtree is folded
     to a single rational -- that is exact arithmetic doing the simplifying --
     and the identities that only add noise (times one, plus zero, minus a
     minus) are removed. Nothing here cancels a factor that could be zero. */
  function Esimp(node) {
    var c = Econst(node);
    if (c !== null) return Enum(c);
    var a, b;
    switch (node.k) {
      case 'add':
        a = Esimp(node.a); b = Esimp(node.b);
        if (isZeroND(a)) return b;
        if (isZeroND(b)) return a;
        if (b.k === 'neg') return { k: 'sub', a: a, b: b.a };
        return { k: 'add', a: a, b: b };
      case 'sub':
        a = Esimp(node.a); b = Esimp(node.b);
        if (isZeroND(b)) return a;
        if (isZeroND(a)) return Esimp({ k: 'neg', a: b });
        return { k: 'sub', a: a, b: b };
      case 'mul':
        a = Esimp(node.a); b = Esimp(node.b);
        if (isZeroND(a) || isZeroND(b)) return ZEROND;
        if (isOneND(a)) return b;
        if (isOneND(b)) return a;
        return { k: 'mul', a: a, b: b };
      case 'div':
        a = Esimp(node.a); b = Esimp(node.b);
        if (isOneND(b)) return a;
        return { k: 'div', a: a, b: b };
      case 'neg':
        a = Esimp(node.a);
        if (a.k === 'neg') return a.a;
        if (a.k === 'sub') return { k: 'sub', a: a.b, b: a.a };
        return { k: 'neg', a: a };
      case 'pow':
        a = Esimp(node.a); b = Esimp(node.b);
        if (isOneND(b)) return a;
        return { k: 'pow', a: a, b: b };
      default:
        return node;
    }
  }
  function mkAdd(a, b) { return Esimp({ k: 'add', a: a, b: b }); }
  function mkSub(a, b) { return Esimp({ k: 'sub', a: a, b: b }); }
  function mkMul(a, b) { return Esimp({ k: 'mul', a: a, b: b }); }
  function mkDiv(a, b) { return Esimp({ k: 'div', a: a, b: b }); }
  function mkNeg(a) { return Esimp({ k: 'neg', a: a }); }

  /* Write the tree as  a*v + b  with a and b free of v, or return null when it
     cannot be written that way -- which is exactly the case a reader has to
     recognise, because then this method does not apply. v inside a function,
     under a power, in a denominator, or multiplied by itself all end here. */
  function Elin(node, v) {
    var l, r, e;
    switch (node.k) {
      case 'num': return { a: ZEROND, b: node };
      case 'var': return node.v === v ? { a: ONEND, b: ZEROND } : { a: ZEROND, b: node };
      case 'neg':
        l = Elin(node.a, v);
        return l === null ? null : { a: mkNeg(l.a), b: mkNeg(l.b) };
      case 'add': case 'sub':
        l = Elin(node.a, v); r = Elin(node.b, v);
        if (l === null || r === null) return null;
        return node.k === 'add'
          ? { a: mkAdd(l.a, r.a), b: mkAdd(l.b, r.b) }
          : { a: mkSub(l.a, r.a), b: mkSub(l.b, r.b) };
      case 'mul':
        l = Elin(node.a, v); r = Elin(node.b, v);
        if (l === null || r === null) return null;
        if (!isZeroND(l.a) && !isZeroND(r.a)) return null;   /* a v^2 term */
        return { a: mkAdd(mkMul(l.a, r.b), mkMul(r.a, l.b)), b: mkMul(l.b, r.b) };
      case 'div':
        l = Elin(node.a, v); r = Elin(node.b, v);
        if (l === null || r === null || !isZeroND(r.a)) return null;   /* v downstairs */
        return { a: mkDiv(l.a, r.b), b: mkDiv(l.b, r.b) };
      case 'pow':
        l = Elin(node.a, v); e = Elin(node.b, v);
        if (l === null || e === null || !isZeroND(e.a)) return null;
        if (isZeroND(l.a)) return { a: ZEROND, b: node };   /* v is not in there at all */
        return isOneND(node.b) ? l : null;                  /* v^2 and up are not linear */
      case 'fn':
        l = Elin(node.a, v);
        if (l === null || !isZeroND(l.a)) return null;      /* v inside sqrt, abs, ln */
        return { a: ZEROND, b: node };
    }
    return null;
  }
  /* The coefficient written against the letter, bracketed only when it needs it. */
  function coefText(a, letter) {
    var s = Etext(a);
    if (s === '1') return letter;
    if (s === '-1') return '-' + letter;
    return atomtext(s) ? s + letter : '(' + s + ')' + letter;
  }
  /* " + b" or " - |b|", so a trace never prints "x + -3". */
  function tailText(b) {
    if (isZeroND(b)) return '';
    if (b.k === 'neg') return ' - ' + Etext(b.a);
    var c = Econst(b);
    if (c !== null && Rsign(c) < 0) return ' - ' + Rtext(Rneg(c));
    return ' + ' + Etext(b);
  }
"""


# --------------------------------------------------------------------------
# The equation lab.
# --------------------------------------------------------------------------

# Presets are STATEMENTS, never answers: each tuple is a label and the text the
# controls are filled with. They are chosen so that a lesson walking the list
# meets the awkward case on purpose -- the near miss, the rounding that fails,
# the identity, the contradiction, the candidate the algebra produces and the
# check throws out.
EQ_PRESETS = {
    "check": [
        ("3x - 4 = 11,  try x = 5", "3x - 4", "11", "5"),
        ("3x - 4 = 11,  try x = 4", "3x - 4", "11", "4"),
        ("3x = 1,  try x = 0.333", "3x", "1", "0.333"),
        ("3x = 1,  try x = 1/3", "3x", "1", "1/3"),
        ("2(x + 3) = 2x + 6,  try x = 7", "2(x + 3)", "2x + 6", "7"),
        ("x + 1 = x + 2,  try x = 0", "x + 1", "x + 2", "0"),
    ],
    "solve": [
        ("3x - 4 = 11", "3x - 4", "11"),
        ("5x + 2 = 3x - 8", "5x + 2", "3x - 8"),
        ("2(x - 3) + 4 = 3(x + 1) - 5", "2(x - 3) + 4", "3(x + 1) - 5"),
        ("(3/4)x + 1/2 = 5/4", "(3/4)x + 1/2", "5/4"),
        ("7 - 2x = 19", "7 - 2x", "19"),
        ("4(x + 1) = 4x + 4", "4(x + 1)", "4x + 4"),
    ],
    "sides": [
        ("5x + 2 = 3x - 8", "5x + 2", "3x - 8"),
        ("3x - 7 = 8x + 3", "3x - 7", "8x + 3"),
        ("2 - x = 4 - 3x", "2 - x", "4 - 3x"),
        ("(1/2)x + 3 = (3/2)x - 1", "(1/2)x + 3", "(3/2)x - 1"),
        ("6x + 1 = 6x + 1", "6x + 1", "6x + 1"),
        ("6x + 1 = 6x - 4", "6x + 1", "6x - 4"),
    ],
    "fractions": [
        ("x/2 + x/3 = 5", "x/2 + x/3", "5"),
        ("(x + 1)/3 - (x - 2)/4 = 1", "(x + 1)/3 - (x - 2)/4", "1"),
        ("0.2x + 1.5 = 3.1", "0.2x + 1.5", "3.1"),
        ("x/2 + 1/3 = x/3 + 1/2", "x/2 + 1/3", "x/3 + 1/2"),
        ("2x/5 - 1 = 2x/5 + 3", "2x/5 - 1", "2x/5 + 3"),
        ("x/6 + x/3 = x/2", "x/6 + x/3", "x/2"),
    ],
    "literal": [
        ("A = P(1 + rt),  for r", "A", "P(1 + rt)", "r"),
        ("F = (9/5)C + 32,  for C", "F", "(9/5)C + 32", "C"),
        ("S = C + rC,  for C", "S", "C + rC", "C"),
        ("ax + b = c,  for x", "ax + b", "c", "x"),
        ("A = (1/2)bh,  for h", "A", "(1/2)bh", "h"),
        ("A = s^2,  for s", "A", "s^2", "s"),
    ],
    "type": [
        ("2(x + 3) = 2x + 6", "2(x + 3)", "2x + 6"),
        ("2(x + 3) = 2x + 5", "2(x + 3)", "2x + 5"),
        ("2(x + 3) = x + 5", "2(x + 3)", "x + 5"),
        ("3x - (x - 4) = 2(x + 2)", "3x - (x - 4)", "2(x + 2)"),
        ("x/2 + x/3 = (5/6)x", "x/2 + x/3", "(5/6)x"),
        ("3x + 5 = 3x + 5 + x", "3x + 5", "3x + 5 + x"),
    ],
    "proportion": [
        ("x/4 = 3/8", "x", "4", "3", "8"),
        ("5/x = 15/9", "5", "x", "15", "9"),
        ("(x + 1)/3 = (x - 2)/5", "x + 1", "3", "x - 2", "5"),
        ("2/3 = 8/x", "2", "3", "8", "x"),
        ("2/(x + 1) = 3/(x - 1)", "2", "x + 1", "3", "x - 1"),
        ("x/(x - 2) = 2/(x - 2)", "x", "x - 2", "2", "x - 2"),
    ],
    "model": [
        ("Plans: 20 + 0.15m against 35 + 0.10m", "plans", "20", "0.15", "35", "0.10"),
        ("Plans with the same rate: 20 + 0.15m against 35 + 0.15m", "plans", "20", "0.15", "35", "0.15"),
        ("Three consecutive whole numbers adding to 48", "consec", "3", "1", "48", "0"),
        ("Three consecutive whole numbers adding to 50", "consec", "3", "1", "50", "0"),
        ("Add 50% solution to 20 L of 10%, aiming at 25%", "mix", "50", "10", "20", "25"),
        ("Add 50% solution to 20 L of 10%, aiming at 60%", "mix", "50", "10", "20", "60"),
    ],
    "absolute": [
        ("|x - 3| = 5", "x - 3", "5"),
        ("|3x - 6| = 9", "3x - 6", "9"),
        ("|2x + 1| = 0", "2x + 1", "0"),
        ("|x + 4| = -2", "x + 4", "-2"),
        ("|2x - 1| = x + 3", "2x - 1", "x + 3"),
        ("|2x - 1| = x - 5", "2x - 1", "x - 5"),
    ],
}

EQ_TITLES = {
    "check": ("What a solution is", "A value is tested, not guessed"),
    "solve": ("Solving, one operation at a time", "Every step named, and the answer put back"),
    "sides": ("The variable on both sides", "Collect it left or right &mdash; both work"),
    "fractions": ("Clearing the denominators", "One multiplication, every term"),
    "literal": ("Solving for a named letter", "The same steps, with letters for numbers"),
    "type": ("Identity, contradiction, conditional", "The three things an equation can be"),
    "proportion": ("Proportions", "Cross-multiplying, and what it assumes"),
    "model": ("From words to an equation", "Built from the numbers, solved, then judged"),
    "absolute": ("Absolute value equations", "Two cases, and a check that throws one out"),
}

# Which control ids the preset value fills, in order, and where in the packed
# value the first of them sits (the model presets lead with a scenario key).
EQ_FIELDS = {
    "check": (["eqLhs", "eqRhs", "eqCand"], 0),
    "solve": (["eqLhs", "eqRhs"], 0),
    "sides": (["eqLhs", "eqRhs"], 0),
    "fractions": (["eqLhs", "eqRhs"], 0),
    "literal": (["eqLhs", "eqRhs", "eqFor"], 0),
    "type": (["eqLhs", "eqRhs"], 0),
    "proportion": (["eqN1", "eqD1", "eqN2", "eqD2"], 0),
    "model": (["eqP1", "eqP2", "eqP3", "eqP4"], 1),
    "absolute": (["eqIns", "eqRhs"], 0),
}

EQ_PLOT_MODES = ("check", "solve", "sides", "type", "model", "absolute")


def _field(input_id, label, value, label_id=""):
    return (
        '        <div class="field">\n'
        '          <label%s for="%s">%s</label>\n'
        '          <input id="%s" type="text" value="%s" inputmode="text" autocomplete="off">\n'
        "        </div>\n"
        % ((' id="%s"' % label_id) if label_id else "", input_id, label, input_id, value)
    )


def _preset_field(select_id, label, options):
    return (
        '        <div class="field">\n'
        '          <label for="%s">%s</label>\n'
        '          <select id="%s">%s</select>\n'
        "        </div>\n" % (select_id, label, select_id, options)
    )


def _own_ids(*chunks):
    """`var OWN = {...}`: every id the assembled markup declares.

    Read out of the markup the lab is about to ship rather than written down
    twice, so the two cannot disagree -- and so a mode that does not build a
    plot cannot ask for one.
    """
    ids = sorted(set(re.findall(r'id="([^"]+)"', "".join(chunks))))
    return "\n  var OWN = {%s};\n" % ", ".join("'%s': 1" % i for i in ids)


def _kpis(items):
    cells = "".join(
        '<div class="kpi"><span>%s</span><strong id="%s">&mdash;</strong></div>' % (label, kid)
        for label, kid in items
    )
    return '        <div class="kpi-grid">%s</div>\n' % cells


EQ_JS = r"""
  /* --------------------------------------------------------- the controls */
  /* OWN is the set of ids this mode's own markup and controls declare, and it
     is generated from that markup rather than typed out beside it. A lab that
     asks the document for an element it never put there gets null, throws on
     the next line, and ships a blank panel that looks like a styling problem.
     Nine modes share this script and they do not share their controls, so the
     question "is this box mine?" has to be answered before it is asked. */
  function el(id) { return OWN[id] ? document.getElementById(id) : null; }
  function val(id) { var e = el(id); return e ? String(e.value) : ''; }
  function kpi(id, text) { var e = el(id); if (e) e.textContent = text; }
  var titleEl = el('eqTitle'), subEl = el('eqSub'),
      workEl = el('eqWork'), statusEl = el('eqStatus');
  function say(html) { statusEl.innerHTML = html; }
  var V = 'x';

  /* An unreadable box explains itself and clears the panel. A stale picture
     beside a new message is worse than no picture. */
  function trouble(msg) {
    workEl.innerHTML = '';
    var svg = el('eqPlot');
    if (svg) svg.textContent = '';
    kpi('eqKA', '--'); kpi('eqKB', '--'); kpi('eqKC', '--');
    if (titleEl) titleEl.textContent = 'waiting for a statement';
    if (subEl) subEl.textContent = '';
    say('<strong>Nothing to work with yet.</strong> ' + msg);
  }
  function degMsg(a, b) {
    return 'the highest power here is ' + V + '^' + Math.max(Pdeg(a), Pdeg(b))
      + ', and this lab solves LINEAR statements &mdash; one operation undone at a time. '
      + 'A quadratic needs the four-method lab in course 6, not this one.';
  }

  /* --------------------------------------------------------- the picture */
  /* Both sides drawn as functions of x. Where the two graphs cross is
     where the two sides are equal, which is the definition of a solution
     rather than an illustration of it: parallel graphs mean no solution, and
     one graph mean every value is a solution. */
  function drawSides(fL, fR, marks, note) {
    var svg = el('eqPlot');
    if (!svg) return;
    var win = niceWindow(marks.map(function (m) { return m.x; }), 8);
    var lo = Infinity, hi = -Infinity, i, x;
    for (i = 0; i <= 80; i += 1) {
      x = win.xmin + (win.xmax - win.xmin) * i / 80;
      [fL(x), fR(x)].forEach(function (y) {
        if (isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); }
      });
    }
    marks.forEach(function (m) { if (isFinite(m.y)) { lo = Math.min(lo, m.y); hi = Math.max(hi, m.y); } });
    if (!isFinite(lo) || !isFinite(hi)) { lo = -5; hi = 5; }
    if (hi - lo < 1e-9) { lo -= 5; hi += 5; }
    var pad = Math.max(1, (hi - lo) * 0.18);
    var plot = Plot(svg, { xmin: win.xmin, xmax: win.xmax, ymin: lo - pad, ymax: hi + pad });
    plot.frame();
    plot.curve(fL, 'plot-curve');
    plot.curve(fR, 'plot-curve alt');
    marks.forEach(function (m) { plot.point(m.x, m.y, m.cls || 'plot-point', m.label || ''); });
    plot.describe(note);
  }

  /* ------------------------------------------------------------ the check */
  /* Substitution into the equation AS TYPED, in exact rationals. If the two
     sides come out the same number then the answer is right whatever happened
     in the middle, and if they do not then the trace above has a mistake in it
     that the reader can go and find. */
  function checkRows(L, Rs, x, v) {
    var env = {}; env[v] = x;
    var lv = Reval(L.node, env), rv = Reval(Rs.node, env);
    var rows = [
      trow('the equation as typed', '<code>' + L.src + ' = ' + Rs.src + '</code>'),
      trow('put ' + v + ' = ' + Rtext(x) + ' into it',
           '<code>' + Esub(L.node, v, x) + ' = ' + Esub(Rs.node, v, x) + '</code>')
    ];
    if (lv === null || rv === null) {
      rows.push(trow('work each side out',
        'one side has no exact value at ' + v + ' = ' + Rtext(x)
        + ' &mdash; a zero denominator, or a root that is not exact'));
      return { rows: rows, ok: false };
    }
    var ok = Requ(lv, rv);
    rows.push(trow('work each side out',
      '<code>' + Rtext(lv) + (ok ? '  =  ' : '  is not  ') + Rtext(rv) + '</code>'));
    rows.push(trow('verdict', ok
      ? chip('checks out', 'ok') + ' both sides are exactly ' + Rtext(lv)
      : chip('does not check', 'no') + ' the two sides differ by ' + Rtext(Rabs(Rsub(lv, rv)))));
    return { rows: rows, ok: ok, lv: lv, rv: rv };
  }

  /* A handful of values tried against the original statement. This is the only
     way to SEE the difference between "true for one value", "true for every
     value" and "true for none". */
  function sampleGrid(caption, L, Rs, xs, v) {
    var seen = {}, rows = [];
    xs.forEach(function (x) {
      var key = Rtext(x);
      if (seen[key]) return;
      seen[key] = 1;
      var env = {}; env[v] = x;
      var lv = Reval(L.node, env), rv = Reval(Rs.node, env);
      var ok = lv !== null && rv !== null && Requ(lv, rv);
      rows.push(tcells([
        '<code>' + v + ' = ' + key + '</code>',
        lv === null ? 'undefined' : Rtext(lv),
        rv === null ? 'undefined' : Rtext(rv),
        ok ? YES : NO
      ], ok ? 'focus' : ''));
    });
    return tgrid(caption, [v, 'left side', 'right side', 'equal?'], rows);
  }

  function outcomeText(tr, v) {
    if (tr.kind === 'unique') return v + ' = ' + Rtext(tr.value);
    if (tr.kind === 'all') return 'every value of ' + v;
    return 'no value of ' + v;
  }
  /* The two ways an equation ends without a single answer, said in the words
     the reader will be marked on. */
  function endnote(tr, v) {
    if (tr.kind === 'all') {
      return '<strong>Every ' + v + ' cancelled and left ' + tr.constText + ', which is true.</strong> '
        + 'The two sides were the same expression written differently, so every number is a solution. '
        + 'This is an IDENTITY. Note what it is not: it is not "' + v + ' = 0".';
    }
    return '<strong>Every ' + v + ' cancelled and left ' + tr.constText + ', which is false.</strong> '
      + 'No number can make it true, so the equation has NO solution &mdash; the graphs below are parallel. '
      + 'This is a CONTRADICTION, and again it is not "' + v + ' = 0".';
  }

  var MODES = {};

  /* ============================================================== check ==
     A solution is a number that makes the statement true. This mode never
     solves anything: it substitutes and reports, which is the definition
     being exercised rather than described. */
  MODES.check = function () {
    var L = sideOf(val('eqLhs'), V, 'left side'), Rs = sideOf(val('eqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    titleEl.textContent = L.src + ' = ' + Rs.src;

    var solved = (Pdeg(L.poly) <= 1 && Pdeg(Rs.poly) <= 1)
      ? traceLinear(L.poly, Rs.poly, V, '=', true) : null;
    var cand = parseR(val('eqCand'));
    var fL = polyFn(L.poly), fR = polyFn(Rs.poly);

    if (cand === null) {
      subEl.textContent = 'the value to test is not a number';
      workEl.innerHTML = ttable('Waiting for a value to test', [
        trow('left side', '<code>' + Etext(L.node) + '</code>'),
        trow('right side', '<code>' + Etext(Rs.node) + '</code>')
      ]);
      kpi('eqKA', '--'); kpi('eqKB', '--'); kpi('eqKC', '--');
      drawSides(fL, fR, [], 'the two sides of ' + L.src + ' = ' + Rs.src + ', drawn as graphs');
      return say('<strong>The value to test has to be a number.</strong> Whole numbers, fractions such as '
        + '<code>-3/2</code> and decimals such as <code>0.333</code> all work. The decimal is read exactly, '
        + 'as 333/1000, which is the point of one of the presets.');
    }

    var res = checkRows(L, Rs, cand, V);
    subEl.textContent = 'testing ' + V + ' = ' + Rtext(cand);
    kpi('eqKA', res.lv === undefined ? '--' : Rtext(res.lv));
    kpi('eqKB', res.rv === undefined ? '--' : Rtext(res.rv));
    kpi('eqKC', res.ok ? 'yes' : 'no');

    var neighbours = [Rsub(cand, R1), cand, Radd(cand, R1), R0];
    if (solved && solved.kind === 'unique') neighbours.push(solved.value);
    var blocks = [
      ttable('Substituting the value into the equation', res.rows),
      sampleGrid('The same test on other values', L, Rs, neighbours, V)
    ];
    workEl.innerHTML = blocks.join('');

    var marks = [{ x: Rnum(cand), y: res.lv === undefined ? 0 : Rnum(res.lv), label: 'left at ' + Rtext(cand) }];
    if (res.rv !== undefined) marks.push({ x: Rnum(cand), y: Rnum(res.rv), label: 'right at ' + Rtext(cand), cls: 'plot-point vertex' });
    if (solved && solved.kind === 'unique') {
      var yv = Rnum(Peval(L.poly, solved.value));
      marks.push({ x: Rnum(solved.value), y: yv, label: 'they meet', cls: 'plot-point root' });
    }
    drawSides(fL, fR, marks, 'the two sides drawn as graphs, with the tested value marked on each');

    var msg;
    if (res.ok) {
      msg = '<strong>' + Rtext(cand) + ' is a solution.</strong> Both sides come out as ' + Rtext(res.lv)
        + ', so the statement is true at this value. That is all "solution" means, and checking is not '
        + 'the same skill as solving: this panel never solved anything.';
    } else {
      msg = '<strong>' + Rtext(cand) + ' is not a solution.</strong> The left side is ' + Rtext(res.lv)
        + ' and the right is ' + Rtext(res.rv) + ', a gap of ' + Rtext(Rabs(Rsub(res.lv, res.rv)))
        + ' &mdash; visible above as the distance between the two graphs at ' + V + ' = ' + Rdec(cand, 4) + '.';
    }
    if (solved && solved.kind === 'unique') {
      msg += ' Exactly one value balances this equation, and it is ' + V + ' = ' + Rtext(solved.value) + '.';
    } else if (solved && solved.kind === 'all') {
      msg += ' Every value balances this one: the two sides are the same expression written two ways.';
    } else if (solved) {
      msg += ' No value balances this one, so no candidate you try can ever pass.';
    }
    say(msg);
  };

  /* ============================================================== solve ==
     The trace, then the check. Naming the operation is the lesson: "do the
     same thing to both sides" is a rule about what you are allowed to do, and
     a step list that does not say what was done cannot be checked. */
  MODES.solve = function () {
    var L = sideOf(val('eqLhs'), V, 'left side'), Rs = sideOf(val('eqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    if (Pdeg(L.poly) > 1 || Pdeg(Rs.poly) > 1) return trouble(degMsg(L.poly, Rs.poly));
    titleEl.textContent = L.src + ' = ' + Rs.src;

    var tr = traceLinear(L.poly, Rs.poly, V, '=', true);
    var typed = L.src + ' = ' + Rs.src;
    var blocks = [ttable('Each step, and what it did to both sides',
      [trow('the equation as typed', '<code>' + typed + '</code>')].concat(traceRows(tr, typed)))];

    var fL = polyFn(L.poly), fR = polyFn(Rs.poly), marks = [];
    if (tr.kind === 'unique') {
      var res = checkRows(L, Rs, tr.value, V);
      blocks.push(ttable('The check: the answer put back into the original', res.rows));
      kpi('eqKA', V + ' = ' + Rtext(tr.value));
      kpi('eqKB', 'one solution');
      kpi('eqKC', res.ok ? 'passes' : 'FAILS');
      subEl.textContent = tr.steps.length + ' steps, answer ' + V + ' = ' + Rtext(tr.value);
      marks.push({ x: Rnum(tr.value), y: Rnum(Peval(L.poly, tr.value)), label: V + ' = ' + Rtext(tr.value), cls: 'plot-point root' });
      say('<strong>' + V + ' = ' + Rtext(tr.value) + '.</strong> '
        + (res.ok
          ? 'Substituted back into the equation as it was typed, both sides come out as ' + Rtext(res.lv)
            + '. Every step above was an operation applied to BOTH sides, which is the only reason the '
            + 'last line has the same solutions as the first.'
          : 'The substitution does not balance, which means a step above is wrong &mdash; report this.')
        + (Rint(tr.value) ? '' : ' The answer is a fraction and is written as one: ' + Rdec(tr.value, 6)
            + ' is a rounding of ' + Rtext(tr.value) + ', not the answer.'));
    } else {
      blocks.push(sampleGrid('Trying values against the original', L, Rs,
        [R(-2n), R0, R1, R(3n)], V));
      kpi('eqKA', tr.kind === 'all' ? 'every number' : 'none');
      kpi('eqKB', tr.kind === 'all' ? 'identity' : 'contradiction');
      kpi('eqKC', '--');
      subEl.textContent = tr.kind === 'all' ? 'an identity' : 'a contradiction';
      say(endnote(tr, V));
    }
    workEl.innerHTML = blocks.join('');
    drawSides(fL, fR, marks, 'each side drawn as a graph; they cross where the equation is true');
  };

  /* ============================================================== sides ==
     Both choices, side by side. Collecting the variable on the left and on the
     right are different arithmetic and the same answer, and a reader who has
     seen the two traces end in the same place stops believing that one of them
     is "the" method. */
  MODES.sides = function () {
    var L = sideOf(val('eqLhs'), V, 'left side'), Rs = sideOf(val('eqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    if (Pdeg(L.poly) > 1 || Pdeg(Rs.poly) > 1) return trouble(degMsg(L.poly, Rs.poly));
    titleEl.textContent = L.src + ' = ' + Rs.src;

    var typedS = L.src + ' = ' + Rs.src;
    var left = traceLinear(L.poly, Rs.poly, V, '=', true);
    var right = traceLinear(L.poly, Rs.poly, V, '=', false);
    var blocks = [
      ttable('Collecting ' + V + ' on the LEFT',
        [trow('as typed', '<code>' + typedS + '</code>')].concat(traceRows(left, typedS))),
      ttable('Collecting ' + V + ' on the RIGHT',
        [trow('as typed', '<code>' + typedS + '</code>')].concat(traceRows(right, typedS)))
    ];
    var agree = left.kind === right.kind
      && (left.kind !== 'unique' || Requ(left.value, right.value));
    kpi('eqKA', outcomeText(left, V));
    kpi('eqKB', outcomeText(right, V));
    kpi('eqKC', agree ? 'same answer' : 'DISAGREE');

    var marks = [];
    if (left.kind === 'unique') {
      var res = checkRows(L, Rs, left.value, V);
      blocks.push(ttable('The check, done once &mdash; there is only one answer to check', res.rows));
      marks.push({ x: Rnum(left.value), y: Rnum(Peval(L.poly, left.value)), label: V + ' = ' + Rtext(left.value), cls: 'plot-point root' });
      var lc = left.coef;
      subEl.textContent = 'both routes give ' + V + ' = ' + Rtext(left.value);
      say('<strong>Both traces end at ' + V + ' = ' + Rtext(left.value) + '.</strong> '
        + 'Collecting on the left leaves a coefficient of ' + Rtext(lc) + '; collecting on the right leaves '
        + Rtext(right.coef) + '. ' + (Rsign(lc) < 0
          ? 'Here the RIGHT-hand route is the tidier one: it never divides by a negative number, and that '
            + 'is the one step where sign errors happen.'
          : 'Here the LEFT-hand route is the tidier one, because its coefficient is already positive.')
        + ' The last step of the right-hand trace only rewrites ' + Rtext(left.value) + ' = ' + V
        + ' as ' + V + ' = ' + Rtext(left.value) + '; nothing was multiplied, so nothing reversed.');
    } else {
      blocks.push(sampleGrid('Trying values against the original', L, Rs, [R(-1n), R0, R1, R(2n)], V));
      subEl.textContent = left.kind === 'all' ? 'an identity' : 'a contradiction';
      say(endnote(left, V) + ' Both routes reach it: the variable cancels whichever side you gather it on.');
    }
    workEl.innerHTML = blocks.join('');
    drawSides(polyFn(L.poly), polyFn(Rs.poly), marks,
      'each side as a graph; the crossing point is the answer both routes found');
  };

  /* The additive terms of a side, in the order they were typed, with the sign
     each one carries. Flattening + and - rather than evaluating is the point:
     these are the terms a reader can see on the page and has to remember to
     multiply. */
  function termsOf(node, sign, out) {
    out = out || [];
    sign = sign === undefined ? 1 : sign;
    if (node.k === 'add') { termsOf(node.a, sign, out); termsOf(node.b, sign, out); return out; }
    if (node.k === 'sub') { termsOf(node.a, sign, out); termsOf(node.b, -sign, out); return out; }
    if (node.k === 'neg') { termsOf(node.a, -sign, out); return out; }
    out.push({ node: node, sign: sign });
    return out;
  }

  /* ========================================================== fractions ==
     One multiplication, applied to EVERY term. The term-by-term table exists
     because the standard mistake is not the LCD, it is multiplying four of the
     five terms and leaving the fifth alone. */
  MODES.fractions = function () {
    var L = sideOf(val('eqLhs'), V, 'left side'), Rs = sideOf(val('eqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    if (Pdeg(L.poly) > 1 || Pdeg(Rs.poly) > 1) return trouble(degMsg(L.poly, Rs.poly));
    titleEl.textContent = L.src + ' = ' + Rs.src;

    /* The terms as the reader WROTE them. Reading them off the collected
       polynomial instead would merge x/2 and x/3 into (5/6)x before the table
       is drawn, and the whole point of the table is that each written term is
       multiplied -- the error this mode exists for is multiplying four terms
       out of five, which cannot be seen once they have been merged. */
    var written = [];
    termsOf(L.node).forEach(function (t) { written.push({ t: t, side: 'left' }); });
    termsOf(Rs.node).forEach(function (t) { written.push({ t: t, side: 'right' }); });

    var dens = [], lcd = 1n;
    written.forEach(function (item) {
      var p = null;
      try { p = Epoly(item.t.node, V); } catch (err) { p = null; }
      item.poly = p;
      if (p === null) return;
      Pnorm(p).forEach(function (c) {
        if (c.d !== 1n && dens.indexOf(String(c.d)) < 0) dens.push(String(c.d));
      });
      var d = lcmden(p);
      lcd = lcd * d / bgcd(lcd, d);
    });
    dens.sort(function (x, y) { return Number(x) - Number(y); });

    var termRows = written.map(function (item) {
      var sgn = item.t.sign < 0 ? '-' : '';
      var shown = sgn + etext(item.t.node, {}, 2);
      var after = item.poly === null ? '?'
        : Ptext(Pscale(Pscale(item.poly, R(BigInt(item.t.sign))), R(lcd)), V);
      return tcells([item.side, '<code>' + shown + '</code>',
        '<code>' + lcd + ' &times; ' + shown + '</code>', '<code>' + after + '</code>']);
    });

    var collectedLcd = lcdOf(L.poly, Rs.poly);
    var typedF = L.src + ' = ' + Rs.src;
    var tr = traceLinear(L.poly, Rs.poly, V, '=', true);
    var multiplierRows = [
      trow('the denominators written down', dens.length ? dens.join(', ')
        : 'none &mdash; every term is already whole'),
      trow('their least common multiple', String(lcd)),
      trow('what to do with it', lcd === 1n
        ? 'nothing: there is nothing to clear'
        : 'multiply BOTH sides by ' + lcd + ', which means every term on both sides, '
          + 'including the ones that are already whole numbers')
    ];
    if (collectedLcd !== lcd) {
      multiplierRows.push(trow('after collecting like terms',
        'the collected equation only needs ' + collectedLcd + ', because collecting cancelled some of '
        + 'the denominators. Multiplying by ' + lcd + ' is still correct &mdash; it is a multiple of it.'));
    }
    var blocks = [
      ttable('Finding the multiplier', multiplierRows),
      tgrid('Every term, multiplied by ' + lcd, ['side', 'term as written', 'multiplied', 'becomes'], termRows),
      ttable('Then solve as usual',
        [trow('the equation as typed', '<code>' + typedF + '</code>')].concat(traceRows(tr, typedF)))
    ];

    kpi('eqKA', String(lcd));
    kpi('eqKB', outcomeText(tr, V));
    if (tr.kind === 'unique') {
      var res = checkRows(L, Rs, tr.value, V);
      blocks.push(ttable('The check, in the ORIGINAL fractional form', res.rows));
      kpi('eqKC', res.ok ? 'passes' : 'FAILS');
      subEl.textContent = 'LCD ' + lcd + ', answer ' + V + ' = ' + Rtext(tr.value);
      say('<strong>' + V + ' = ' + Rtext(tr.value) + '.</strong> The check above is done in the fractions '
        + 'the equation was written in, not in the cleared version &mdash; a slip while clearing would show '
        + 'up there and nowhere else. Multiplying by ' + lcd + ' is legal because ' + lcd + ' is not zero, '
        + 'and it is worth doing because ' + (dens.length ? Ptext(L.poly, V) : 'the cleared form')
        + ' is easier to work with than any equation containing a fraction.');
    } else {
      kpi('eqKC', '--');
      blocks.push(sampleGrid('Trying values against the original', L, Rs, [R0, R1, R(6n)], V));
      subEl.textContent = tr.kind === 'all' ? 'an identity' : 'a contradiction';
      say(endnote(tr, V) + ' Clearing the denominators did not create that outcome, it revealed it: '
        + 'the fractions were hiding two sides that are the same expression, or two that can never meet.');
    }
    workEl.innerHTML = blocks.join('');
  };

  /* ============================================================ literal ==
     The same three steps, with letters where the numbers were. The lab does
     the algebra on the TREE, so the answer is an expression; and because it
     cannot then substitute a number, it checks the answer by giving the other
     letters exact values and testing the original equation there. */
  MODES.literal = function () {
    var target = val('eqFor').trim();
    if (!/^[A-Za-z]$/.test(target)) {
      return trouble('name the letter to solve for as a single letter, such as <code>r</code>.');
    }
    var lsrc = val('eqLhs').trim(), rsrc = val('eqRhs').trim();
    if (!lsrc || !rsrc) return trouble('both sides of the formula are needed.');
    var lnode, rnode;
    try { lnode = Eparse(lsrc); rnode = Eparse(rsrc); }
    catch (err) { return trouble('that formula could not be read: ' + err.message + '.'); }

    titleEl.textContent = lsrc + ' = ' + rsrc + ',  for ' + target;
    var all = { k: 'sub', a: lnode, b: rnode };
    var lin = Elin(all, target);
    if (lin === null) {
      kpi('eqKA', target); kpi('eqKB', 'not linear'); kpi('eqKC', '--');
      subEl.textContent = 'this method does not apply';
      workEl.innerHTML = ttable('Why the method stops here', [
        trow('the formula', '<code>' + lsrc + ' = ' + rsrc + '</code>'),
        trow('solving for', target),
        trow('what is needed', 'the formula must be able to be written as (something) &times; ' + target
          + ' + (something), with neither part containing ' + target),
        trow('what is there instead', target + ' appears squared, or under a root, or inside a denominator, '
          + 'or multiplied by itself')
      ]);
      return say('<strong>' + target + ' cannot be isolated by these steps.</strong> Adding, subtracting, '
        + 'multiplying and dividing both sides undo a linear relationship, and this one is not linear in '
        + target + '. A squared letter needs a square root &mdash; and then BOTH signs, which is a course 6 '
        + 'lesson, not a rearrangement.');
    }

    var a = lin.a, b = lin.b;
    var ac = Econst(a);
    if (isZeroND(a)) {
      kpi('eqKA', target); kpi('eqKB', 'does not appear'); kpi('eqKC', '--');
      subEl.textContent = target + ' is not in this formula';
      workEl.innerHTML = ttable('Nothing to solve for', [
        trow('the formula', '<code>' + lsrc + ' = ' + rsrc + '</code>'),
        trow('the coefficient of ' + target, '0')
      ]);
      return say('<strong>' + target + ' does not appear in this formula</strong> (or it cancels out '
        + 'completely), so there is nothing to solve for. Every other letter is free and the statement is '
        + 'either always true or never true.');
    }

    var rows = [
      trow('the formula', '<code>' + lsrc + ' = ' + rsrc + '</code>'),
      trow('everything on one side', '<code>' + Etext(lnode) + ' - '
        + (atomtext(Etext(rnode)) ? Etext(rnode) : '(' + Etext(rnode) + ')') + ' = 0</code>')
    ];
    var negated = false;
    if ((ac !== null && Rsign(ac) < 0) || (ac === null && a.k === 'neg')) {
      a = mkNeg(a); b = mkNeg(b); negated = true;
      ac = Econst(a);     /* the coefficient CHANGED; everything below uses it */
    }
    rows.push(trow('collect the ' + target + ' terms',
      '<code>' + coefText(a, target) + tailText(b) + ' = 0</code>'
      + (negated ? '<br><span class="small-copy">both sides multiplied by -1 first, so the coefficient of '
        + target + ' is positive</span>' : '')));
    if (!isZeroND(b)) {
      rows.push(trow(tailText(b).indexOf(' - ') === 0
        ? 'add ' + Etext(mkNeg(b)) + ' to both sides'
        : 'subtract ' + Etext(b) + ' from both sides',
        '<code>' + coefText(a, target) + ' = ' + Etext(mkNeg(b)) + '</code>'));
    }
    var answer = (ac !== null && !Rzero(ac))
      ? mkMul(Enum(Rinv(ac)), mkNeg(b))    /* dividing by a number: use its reciprocal */
      : mkDiv(mkNeg(b), a);
    rows.push(trow('divide both sides by ' + Etext(a),
      '<code>' + target + ' = ' + Etext(answer) + '</code>'
      + (ac !== null ? '<br><span class="small-copy">the same move as multiplying by '
          + Rtext(Rinv(ac)) + '</span>' : '')));
    rows.push(trow('valid provided', ac !== null
      ? Etext(a) + ' is not zero, which it is not &mdash; it is a number'
      : '<code>' + Etext(a) + '</code> is not zero. Dividing by it is the last step, and dividing by zero '
        + 'is the one operation that does not preserve an equation'));

    /* The check: give every other letter an exact value, work out what the
       answer says, and test the ORIGINAL formula there. Rational throughout,
       so agreement is exact rather than close. */
    var names = Object.keys(varsOf(all)).filter(function (n) { return n !== target; }).sort();
    var probeSets = [[2n, 3n, 5n, 7n, 11n], [3n, 5n, 7n, 2n, 13n], [5n, 7n, 2n, 3n, 17n]];
    var probeRows = [], good = 0;
    probeSets.forEach(function (vals) {
      var env = {}, shown = [];
      names.forEach(function (n, i) {
        env[n] = R(vals[i % vals.length]);
        shown.push(n + ' = ' + Rtext(env[n]));
      });
      var xv = Reval(answer, env);
      if (xv === null) {
        probeRows.push(tcells([shown.join(', ') || 'no other letters', 'undefined here', '--', '--', NO]));
        return;
      }
      var env2 = {}, key;
      for (key in env) if (Object.prototype.hasOwnProperty.call(env, key)) env2[key] = env[key];
      env2[target] = xv;
      var lv = Reval(lnode, env2), rv = Reval(rnode, env2);
      var ok = lv !== null && rv !== null && Requ(lv, rv);
      if (ok) good += 1;
      probeRows.push(tcells([
        shown.join(', ') || 'no other letters',
        Rtext(xv),
        lv === null ? 'undefined' : Rtext(lv),
        rv === null ? 'undefined' : Rtext(rv),
        ok ? YES : NO
      ], ok ? 'focus' : ''));
    });

    workEl.innerHTML = [
      ttable('Solving for ' + target, rows),
      tgrid('The check: exact values for the other letters',
        ['the other letters', target + ' from the answer', 'left side', 'right side', 'equal?'], probeRows)
    ].join('');
    kpi('eqKA', target);
    kpi('eqKB', Etext(answer));
    kpi('eqKC', ac !== null ? 'always' : Etext(a) + ' = 0');
    subEl.textContent = target + ' = ' + Etext(answer);
    say('<strong>' + target + ' = ' + Etext(answer) + '.</strong> '
      + (good ? 'Checked at ' + good + ' exact assignment' + (good === 1 ? '' : 's')
          + ' of the other letters: the formula balances at every one of them, in rational arithmetic. '
        : 'No probe assignment produced an exact value here, so read the check table for the reason. ')
      + (ac !== null
        ? 'The divisor was a number, so the rearrangement is valid for all values of the other letters.'
        : 'The last step divided by <code>' + Etext(a) + '</code>. That is the whole catch in literal '
          + 'equations: the answer is valid exactly when that expression is not zero, and a formula that '
          + 'does not say so is hiding a case.'));
  };

  /* =============================================================== type ==
     Three outcomes, told apart by doing the subtraction. What survives after
     the sides are subtracted is either nothing (identity), a false statement
     about numbers (contradiction), or a term in x (conditional). */
  MODES.type = function () {
    var L = sideOf(val('eqLhs'), V, 'left side'), Rs = sideOf(val('eqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    if (Pdeg(L.poly) > 1 || Pdeg(Rs.poly) > 1) return trouble(degMsg(L.poly, Rs.poly));
    titleEl.textContent = L.src + ' = ' + Rs.src;

    var D = Psub(L.poly, Rs.poly);
    var tr = traceLinear(L.poly, Rs.poly, V, '=', true);
    var kind = tr.kind === 'unique' ? 'conditional' : (tr.kind === 'all' ? 'identity' : 'contradiction');
    var rows = [
      trow('as typed', '<code>' + L.src + ' = ' + Rs.src + '</code>'),
      trow('expand the left side', '<code>' + Ptext(L.poly, V) + '</code>'),
      trow('expand the right side', '<code>' + Ptext(Rs.poly, V) + '</code>'),
      trow('subtract the right side from both', '<code>' + Ptext(D, V) + ' = 0</code>'),
      trow('what is left', Pzero(D)
        ? '<code>0 = 0</code> &mdash; nothing at all, and 0 = 0 is true'
        : (Pdeg(D) === 0
          ? '<code>' + Ptext(D, V) + ' = 0</code> &mdash; a statement about numbers, and it is false'
          : '<code>' + Ptext(D, V) + ' = 0</code> &mdash; still contains ' + V)),
      trow('so this equation is', kind === 'identity' ? chip('an identity', 'ok')
        : (kind === 'contradiction' ? chip('a contradiction', 'no') : chip('conditional', 'hi'))),
      trow('its solutions', kind === 'identity' ? 'every real number'
        : (kind === 'contradiction' ? 'none at all' : 'exactly one: ' + V + ' = ' + Rtext(tr.value)))
    ];
    var samples = [R(-1n), R0, R1, R(5n)];
    if (tr.kind === 'unique') samples.push(tr.value);
    var blocks = [
      ttable('Deciding which of the three it is', rows),
      sampleGrid('The same equation tested at several values', L, Rs, samples, V)
    ];
    if (tr.kind === 'unique') {
      blocks.push(ttable('The check', checkRows(L, Rs, tr.value, V).rows));
    }
    workEl.innerHTML = blocks.join('');
    kpi('eqKA', kind);
    kpi('eqKB', Pzero(D) ? '0 = 0' : Ptext(D, V) + ' = 0');
    kpi('eqKC', kind === 'identity' ? 'all reals' : (kind === 'contradiction' ? 'none' : '1'));
    subEl.textContent = kind;

    var marks = [];
    if (tr.kind === 'unique') marks.push({ x: Rnum(tr.value), y: Rnum(Peval(L.poly, tr.value)), label: V + ' = ' + Rtext(tr.value), cls: 'plot-point root' });
    drawSides(polyFn(L.poly), polyFn(Rs.poly), marks,
      kind === 'identity' ? 'both sides are the same graph, drawn twice'
        : (kind === 'contradiction' ? 'two parallel graphs, which never meet'
          : 'two graphs crossing once'));

    if (kind === 'identity') {
      say('<strong>An identity.</strong> The two sides are the same expression written differently, so the '
        + 'graphs above lie on top of each other and every value in the table balances. Written as an '
        + 'equation to solve, it collapses to 0 = 0 &mdash; which is a true statement containing no '
        + V + ', and therefore says nothing about ' + V + '. The answer is "every real number", not "' + V + ' = 0".');
    } else if (kind === 'contradiction') {
      say('<strong>A contradiction.</strong> The sides differ by the constant ' + Ptext(D, V)
        + ' no matter what ' + V + ' is, so the graphs are parallel and nothing in the table balances. '
        + 'It collapses to a false statement about numbers. The answer is "no solution" &mdash; and note '
        + 'that "no solution" and "the solution is 0" are as different as an empty box and a box with a '
        + 'zero written in it.');
    } else {
      say('<strong>Conditional: true for ' + V + ' = ' + Rtext(tr.value) + ' and false for everything else.</strong> '
        + 'This is what most equations are, and it is the only one of the three where "solving" produces a '
        + 'number. ' + (Rzero(tr.value)
          ? 'Here that number happens to be 0, which is a genuine solution and not the same thing as no '
            + 'solution: the table shows the equation balancing at ' + V + ' = 0.'
          : 'The table shows it balancing at ' + Rtext(tr.value) + ' and failing everywhere else.'));
    }
  };
"""


EQ_JS += r"""
  /* ========================================================= proportion ==
     Cross-multiplying is not a rule of its own: it is multiplying both sides
     by both denominators. That is only legal where neither denominator is
     zero, which is why this mode finds the excluded values BEFORE it solves
     and tests every candidate against them afterwards. */
  /* Brackets only where they change the reading: x/4, but (x + 1)/3. */
  function ratioText(num, den) {
    return (atomtext(num) ? num : '(' + num + ')') + '/' + (atomtext(den) ? den : '(' + den + ')');
  }

  MODES.proportion = function () {
    var n1 = sideOf(val('eqN1'), V, 'left numerator'),
        d1 = sideOf(val('eqD1'), V, 'left denominator'),
        n2 = sideOf(val('eqN2'), V, 'right numerator'),
        d2 = sideOf(val('eqD2'), V, 'right denominator');
    var parts = [n1, d1, n2, d2], i;
    for (i = 0; i < parts.length; i += 1) if (!parts[i].ok) return trouble(parts[i].msg);
    if (Pzero(d1.poly) || Pzero(d2.poly)) return trouble('a denominator is 0, and nothing is divided by zero.');
    var lhsText = ratioText(n1.src, d1.src), rhsText = ratioText(n2.src, d2.src);
    titleEl.textContent = lhsText + ' = ' + rhsText;

    var excluded = [];
    [d1, d2].forEach(function (d) {
      if (Pdeg(d.poly) < 1) return;
      Prationalroots(d.poly).forEach(function (r) {
        if (!excluded.some(function (e) { return Requ(e, r); })) excluded.push(r);
      });
    });
    excluded.sort(Rcmp);

    var left = Pmul(n1.poly, d2.poly), right = Pmul(n2.poly, d1.poly);
    var cross = Psub(left, right);
    var rows = [
      trow('the proportion', '<code>' + lhsText + ' = ' + rhsText + '</code>'),
      trow('multiply both sides by (' + d1.src + ')(' + d2.src + ')',
        '<code>' + Ptext(left, V) + ' = ' + Ptext(right, V) + '</code>'
        + '<br><span class="small-copy">this is all "cross-multiply" means: one multiplication '
        + 'applied to both sides, after which each denominator has cancelled</span>'),
      trow('legal only when', excluded.length
        ? 'neither denominator is zero, so ' + V + ' cannot be ' + excluded.map(Rtext).join(' or ')
        : 'neither denominator is zero &mdash; both are constants here, so nothing is excluded'),
      trow('everything on one side', '<code>' + Ptext(cross, V) + ' = 0</code>')
    ];

    var candidates = [], verdict = '', deg = Pdeg(cross);
    if (Pzero(cross)) {
      verdict = 'every value except the excluded ones';
    } else if (deg <= 0) {
      verdict = 'no value at all: what is left is ' + Ptext(cross, V) + ' = 0, which is false';
    } else if (deg === 1) {
      candidates = [Rdiv(Rneg(cross[0]), cross[1])];
    } else if (deg === 2) {
      var q = quadroots(cross[2], cross[1], cross[0]);
      rows.push(trow('this came out quadratic',
        'both denominators contain ' + V + ', so the cross product has an ' + V + '^2 term. '
        + 'Discriminant ' + Rtext(q.disc) + '.'));
      if (q.kind === 'complex') verdict = 'no real value';
      else if (q.kind === 'double') candidates = [q.p];
      else if (q.kind === 'rational') candidates = q.roots.slice();
      else verdict = 'two irrational values, ' + V + ' = ' + pmtext(q.p, q.s)
        + ', neither of which can equal an excluded rational';
    } else {
      verdict = 'a polynomial of degree ' + deg + ', which is past what this lab solves';
    }

    var kept = [], checkRowsOut = [];
    candidates.forEach(function (x) {
      var isOut = excluded.some(function (e) { return Requ(e, x); });
      var lv = null, rv = null, ok = false;
      if (!isOut) {
        var dl = Peval(d1.poly, x), dr = Peval(d2.poly, x);
        if (!Rzero(dl) && !Rzero(dr)) {
          lv = Rdiv(Peval(n1.poly, x), dl);
          rv = Rdiv(Peval(n2.poly, x), dr);
          ok = Requ(lv, rv);
        }
      }
      if (ok) kept.push(x);
      checkRowsOut.push(tcells([
        '<code>' + V + ' = ' + Rtext(x) + '</code>',
        isOut ? 'a denominator is 0 here' : Rtext(lv),
        isOut ? '&mdash;' : Rtext(rv),
        ok ? chip('a solution', 'ok') : chip(isOut ? 'extraneous' : 'fails', 'no')
      ], ok ? 'focus' : ''));
    });

    var blocks = [ttable('What cross-multiplying actually does', rows)];
    if (checkRowsOut.length) {
      blocks.push(tgrid('Every candidate, put back into the ORIGINAL fractions',
        [V, 'left ratio', 'right ratio', 'verdict'], checkRowsOut));
    }
    workEl.innerHTML = blocks.join('');
    kpi('eqKA', Ptext(left, V) + ' = ' + Ptext(right, V));
    kpi('eqKB', kept.length ? kept.map(Rtext).join(', ') : 'none');
    kpi('eqKC', excluded.length ? excluded.map(Rtext).join(', ') : 'none');
    subEl.textContent = excluded.length
      ? V + ' cannot be ' + excluded.map(Rtext).join(' or ') : 'no excluded values';

    if (kept.length) {
      say('<strong>' + kept.map(function (x) { return V + ' = ' + Rtext(x); }).join(' and ')
        + '.</strong> Each one was put back into the two ratios as they were written, and both ratios came '
        + 'out as the same exact fraction. '
        + (excluded.length
          ? 'The excluded value' + (excluded.length === 1 ? ' ' : 's ') + excluded.map(Rtext).join(', ')
            + ' had to be checked because multiplying by a denominator that is zero is not one of the '
            + 'operations that preserves an equation.'
          : 'With constant denominators there is nothing to exclude, which is why the plain '
            + 'cross-multiplication rule works so reliably on the simplest proportions &mdash; and why it '
            + 'is trusted too far on the harder ones.'));
    } else if (candidates.length) {
      say('<strong>No solution.</strong> The algebra produced '
        + candidates.map(function (x) { return V + ' = ' + Rtext(x); }).join(' and ')
        + (candidates.length === 1 ? ', and it is thrown out by the check.'
                                   : ', and every one of them is thrown out by the check.')
        + ' This is what an EXTRANEOUS solution is: '
        + 'cross-multiplying multiplied both sides by an expression that is zero at exactly that value, '
        + 'which is not a legal move there. The step created a solution the original statement never had, '
        + 'and only substituting back finds it.');
    } else {
      say('<strong>' + verdict.charAt(0).toUpperCase() + verdict.slice(1) + '.</strong> '
        + 'The cross product is ' + Ptext(cross, V) + ' = 0, and that is what the proportion reduces to '
        + 'once both denominators are cleared.');
    }
  };

  /* ============================================================== model ==
     The words come first, the equation is BUILT from the numbers in the
     controls, and only then is it solved by the same trace every other mode
     uses. The last row is the one that matters: an equation can have a
     perfectly good solution that the situation it describes rejects. */
  function termTail(r, letter) {
    if (Rzero(r)) return '';
    var neg = Rsign(r) < 0, mag = Rabs(r);
    return (neg ? ' - ' : ' + ') + (Requ(mag, R1) ? '' : Rterm(mag)) + letter;
  }
  function signedNum(r) { return Rsign(r) < 0 ? ' - ' + Rtext(Rneg(r)) : ' + ' + Rtext(r); }
  function headTerm(r, letter) {
    if (Rzero(r)) return '0';
    if (Requ(r, R1)) return letter;
    if (Requ(r, R(-1n))) return '-' + letter;
    return Rterm(r) + letter;
  }

  var SCENARIOS = {
    plans: {
      v: 'm', arity: 4,
      labels: ['plan A: fixed charge', 'plan A: cost per unit', 'plan B: fixed charge', 'plan B: cost per unit'],
      build: function (p) {
        return {
          lhs: Rtext(p[0]) + termTail(p[1], 'm'),
          rhs: Rtext(p[2]) + termTail(p[3], 'm'),
          words: 'Plan A charges ' + Rtext(p[0]) + ' up front and ' + Rtext(p[1]) + ' for each unit. '
            + 'Plan B charges ' + Rtext(p[2]) + ' up front and ' + Rtext(p[3]) + ' for each unit.',
          ask: 'At how many units do the two plans cost the same?',
          unknown: 'm, the number of units'
        };
      },
      judge: function (x, p, common) {
        if (Rsign(x) < 0) {
          return { ok: false, why: 'the equation is solved by m = ' + Rtext(x)
            + ', and nobody buys a negative number of units. In the situation the words describe there is '
            + 'no answer at all: plan ' + (Rcmp(p[0], p[2]) < 0 ? 'A' : 'B') + ' is cheaper at m = 0 and the '
            + 'gap only widens from there.' };
        }
        return { ok: true, why: 'at m = ' + Rtext(x) + ' units both plans cost ' + Rtext(common)
          + '. Below that the smaller fixed charge wins; above it the smaller rate does.' };
      }
    },
    consec: {
      v: 'n', arity: 3,
      labels: ['how many numbers', 'the step between them', 'what they add up to'],
      valid: function (p) {
        if (!Rint(p[0]) || p[0].n < 1n || p[0].n > 60n) return 'the count must be a whole number from 1 to 60.';
        if (!Rint(p[1])) return 'the step must be a whole number: 1 for consecutive, 2 for consecutive evens.';
        return '';
      },
      build: function (p) {
        var k = p[0], s = p[1], count = Number(k.n), list = [], i;
        for (i = 0; i < Math.min(count, 8); i += 1) {
          list.push(i === 0 ? 'n' : 'n' + signedNum(Rmul(s, R(BigInt(i)))));
        }
        if (count > 8) list.push('...');
        /* n + (n+s) + ... + (n+(k-1)s)  =  k*n + s*k(k-1)/2, derived here */
        var cst = Rmul(s, Rdiv(Rmul(k, Rsub(k, R1)), R(2n)));
        return {
          lhs: headTerm(k, 'n') + (Rzero(cst) ? '' : signedNum(cst)),
          rhs: Rtext(p[2]),
          words: 'Call the first number n. The ' + Rtext(k) + ' numbers are then ' + list.join(', ')
            + ', because each is ' + Rtext(s) + ' more than the one before. Adding them gives '
            + Rtext(k) + ' copies of n plus ' + Rtext(cst) + '.',
          ask: 'What is the first of the ' + Rtext(k) + ' numbers?',
          unknown: 'n, the first number'
        };
      },
      judge: function (x, p) {
        if (!Rint(x)) {
          return { ok: false, why: 'the equation is solved exactly by n = ' + Rtext(x)
            + ', and that is not a whole number. There is no run of ' + Rtext(p[0]) + ' whole numbers with '
            + 'this total: the equation has a solution and the model does not. Change the total by 1 or 2 '
            + 'and it will.' };
        }
        var count = Number(p[0].n), out = [], i;
        for (i = 0; i < Math.min(count, 12); i += 1) out.push(Rtext(Radd(x, Rmul(p[1], R(BigInt(i))))));
        if (count > 12) out.push('...');
        return { ok: true, why: 'the numbers are ' + out.join(', ') + ', and they add to ' + Rtext(p[2]) + '.' };
      }
    },
    mix: {
      v: 'x', arity: 4,
      labels: ['strength of what you add (%)', 'strength of what you have (%)',
               'litres you have', 'strength you want (%)'],
      build: function (p) {
        var a = Rdiv(p[0], R(100n)), b = Rdiv(p[1], R(100n)), lit = p[2], c = Rdiv(p[3], R(100n));
        return {
          lhs: headTerm(a, 'x') + (Rzero(Rmul(b, lit)) ? '' : signedNum(Rmul(b, lit))),
          rhs: Rterm(c) + '(x' + signedNum(lit) + ')',
          words: 'You have ' + Rtext(lit) + ' litres at ' + Rtext(p[1]) + '% and you add x litres at '
            + Rtext(p[0]) + '%. The pure substance you end with is what you started with plus what you '
            + 'added, and the mixture must come out at ' + Rtext(p[3]) + '% of its new volume.',
          ask: 'How many litres of the ' + Rtext(p[0]) + '% must be added?',
          unknown: 'x, the litres added'
        };
      },
      judge: function (x, p) {
        if (Rsign(x) < 0) {
          return { ok: false, why: 'the equation is solved by x = ' + Rtext(x)
            + ' litres, which you cannot pour. Mixing two strengths always lands BETWEEN them, and '
            + Rtext(p[3]) + '% is not between ' + Rtext(p[1]) + '% and ' + Rtext(p[0])
            + '%. The negative answer is the algebra reporting an impossible request rather than failing.' };
        }
        return { ok: true, why: 'adding ' + Rtext(x) + ' litres gives '
          + Rtext(Radd(x, p[2])) + ' litres at ' + Rtext(p[3]) + '%.' };
      }
    }
  };

  function applyScenario(sc) {
    for (var i = 1; i <= 4; i += 1) {
      var lab = el('eqL' + i), inp = el('eqP' + i);
      if (!lab || !inp) continue;
      if (i <= sc.arity) { lab.textContent = sc.labels[i - 1]; inp.disabled = false; }
      else { lab.textContent = 'not used by this model'; inp.disabled = true; }
    }
  }

  MODES.model = function () {
    var preset = el('eqPreset');
    var key = preset ? String(preset.value).split('|')[0] : 'plans';
    var sc = SCENARIOS[key] || SCENARIOS.plans;
    applyScenario(sc);

    var p = [], i, r;
    for (i = 0; i < sc.arity; i += 1) {
      r = parseR(val('eqP' + (i + 1)));
      if (r === null) {
        return trouble('"' + sc.labels[i] + '" has to be a number &mdash; a whole number, a fraction such '
          + 'as <code>3/20</code>, or a decimal such as <code>0.15</code>, which is read exactly as 15/100.');
      }
      p.push(r);
    }
    var why = sc.valid ? sc.valid(p) : '';
    if (why) return trouble(why);

    var built = sc.build(p), v = sc.v;
    var L = sideOf(built.lhs, v, 'left side'), Rs = sideOf(built.rhs, v, 'right side');
    if (!L.ok || !Rs.ok) return trouble('the model built an expression this lab could not read back: '
      + (L.ok ? Rs.msg : L.msg));
    titleEl.textContent = built.lhs + ' = ' + built.rhs;

    var tr = traceLinear(L.poly, Rs.poly, v, '=', true);
    var blocks = [
      ttable('From the words to an equation', [
        trow('the situation', built.words),
        trow('what is unknown', built.unknown),
        trow('the question', built.ask),
        trow('the equation it becomes', '<code>' + built.lhs + ' = ' + built.rhs + '</code>')
      ]),
      ttable('Solving it', traceRows(tr))
    ];

    var marks = [];
    if (tr.kind === 'unique') {
      var common = Peval(L.poly, tr.value);
      var res = checkRows(L, Rs, tr.value, v);
      var verdictObj = sc.judge(tr.value, p, common);
      blocks.push(ttable('The check', res.rows));
      blocks.push(ttable('Does the situation accept that answer?', [
        trow('the equation says', v + ' = ' + Rtext(tr.value)),
        trow('the situation says', (verdictObj.ok ? chip('usable', 'ok') : chip('rejected', 'no'))
          + ' ' + verdictObj.why)
      ]));
      kpi('eqKA', v + ' = ' + Rtext(tr.value));
      kpi('eqKB', Rtext(common));
      kpi('eqKC', verdictObj.ok ? 'yes' : 'no');
      subEl.textContent = v + ' = ' + Rtext(tr.value) + (verdictObj.ok ? '' : ' (rejected by the model)');
      say('<strong>' + v + ' = ' + Rtext(tr.value) + ', and the model '
        + (verdictObj.ok ? 'accepts it' : 'does NOT accept it') + '.</strong> ' + verdictObj.why
        + ' Solving is only the middle of the job: the equation was built from the words, and the answer '
        + 'has to be handed back to the words before it counts.');
      marks.push({ x: Rnum(tr.value), y: Rnum(common), label: v + ' = ' + Rtext(tr.value), cls: 'plot-point root' });
    } else {
      kpi('eqKA', tr.kind === 'all' ? 'every value' : 'none');
      kpi('eqKB', '--');
      kpi('eqKC', 'no');
      subEl.textContent = tr.kind === 'all' ? 'an identity' : 'no solution';
      blocks.push(sampleGrid('Trying values in the model', L, Rs, [R0, R(10n), R(100n)], v));
      say(endnote(tr, v) + ' In this model that is a fact about the situation, not a failure of the '
        + 'arithmetic: two plans with the same rate keep the same gap for ever, so there is no number of '
        + 'units at which they agree.');
    }
    workEl.innerHTML = blocks.join('');
    drawSides(polyFn(L.poly), polyFn(Rs.poly), marks,
      'the two sides of the model drawn against ' + v + '; they cross at the answer');
  };

  /* =========================================================== absolute ==
     |A| = B is two equations because |A| is A or -A, and it is TWO equations
     rather than one answer with a plus-or-minus stuck on it. Every candidate
     is then put back into the original, which is the only step that catches
     the case where B itself is negative at that value. */
  MODES.absolute = function () {
    var ins = sideOf(val('eqIns'), V, 'expression inside the bars'),
        rhs = sideOf(val('eqRhs'), V, 'right side');
    if (!ins.ok) return trouble(ins.msg);
    if (!rhs.ok) return trouble(rhs.msg);
    if (Pdeg(ins.poly) > 1 || Pdeg(rhs.poly) > 1) return trouble(degMsg(ins.poly, rhs.poly));
    var eqText = '|' + ins.src + '| = ' + rhs.src;
    titleEl.textContent = eqText;

    var negRhs = Pscale(rhs.poly, R(-1n));
    var caseA = traceLinear(ins.poly, rhs.poly, V, '=', true);
    var caseB = traceLinear(ins.poly, negRhs, V, '=', true);
    var rows = [
      trow('the equation', '<code>' + eqText + '</code>'),
      trow('what the bars mean', '|' + ins.src + '| is ' + ins.src + ' when that is not negative, and -('
        + ins.src + ') when it is. So the equation is two equations.'),
      trow('case 1', '<code>' + Ptext(ins.poly, V) + ' = ' + Ptext(rhs.poly, V) + '</code> &nbsp; gives &nbsp;'
        + outcomeText(caseA, V)),
      trow('case 2', '<code>' + Ptext(ins.poly, V) + ' = ' + Ptext(negRhs, V) + '</code> &nbsp; gives &nbsp;'
        + outcomeText(caseB, V))
    ];

    var cands = [];
    [caseA, caseB].forEach(function (t) {
      if (t.kind === 'unique' && !cands.some(function (x) { return Requ(x, t.value); })) cands.push(t.value);
    });
    cands.sort(Rcmp);

    var kept = [], testRows = [];
    cands.forEach(function (x) {
      var insv = Peval(ins.poly, x), rv = Peval(rhs.poly, x), lv = Rabs(insv);
      var ok = Requ(lv, rv);
      if (ok) kept.push(x);
      testRows.push(tcells([
        '<code>' + V + ' = ' + Rtext(x) + '</code>',
        Rtext(insv),
        Rtext(lv),
        Rtext(rv),
        ok ? chip('a solution', 'ok') : chip('extraneous', 'no')
      ], ok ? 'focus' : ''));
    });

    var blocks = [ttable('Splitting the bars into two equations', rows)];
    if (testRows.length) {
      blocks.push(tgrid('Every candidate, put back into |' + ins.src + '| = ' + rhs.src,
        [V, ins.src, '|' + ins.src + '|', rhs.src, 'verdict'], testRows));
    }
    if (caseA.kind !== 'unique' || caseB.kind !== 'unique') {
      blocks.push(ttable('One of the cases did not give a single value', [
        trow('case 1', caseA.kind === 'unique' ? 'one value, ' + Rtext(caseA.value)
          : (caseA.kind === 'all' ? 'true for every ' + V + ' &mdash; the two sides are the same expression'
            : 'true for no ' + V + ' at all')),
        trow('case 2', caseB.kind === 'unique' ? 'one value, ' + Rtext(caseB.value)
          : (caseB.kind === 'all' ? 'true for every ' + V + ' &mdash; the two sides are the same expression'
            : 'true for no ' + V + ' at all')),
        trow('what that means', 'a case with no value contributes nothing; a case true for every ' + V
          + ' contributes every ' + V + ' at which the right side is not negative, because the left side '
          + 'is a distance and a distance is never negative')
      ]));
    }
    workEl.innerHTML = blocks.join('');
    kpi('eqKA', outcomeText(caseA, V));
    kpi('eqKB', outcomeText(caseB, V));
    kpi('eqKC', kept.length ? kept.map(Rtext).join(', ') : 'none');
    subEl.textContent = kept.length === 1 ? 'one solution'
      : (kept.length ? kept.length + ' solutions' : 'no solution');

    var fIns = polyFn(ins.poly), fRhs = polyFn(rhs.poly);
    var marks = kept.map(function (x) {
      return { x: Rnum(x), y: Rnum(Peval(rhs.poly, x)), label: V + ' = ' + Rtext(x), cls: 'plot-point root' };
    });
    drawSides(function (x) { return Math.abs(fIns(x)); }, fRhs, marks,
      'the V-shaped graph of |' + ins.src + '| against the graph of ' + rhs.src
      + '; a solution is a crossing point');

    var rhsConst = Pdeg(rhs.poly) === 0 || Pzero(rhs.poly);
    var rhsVal = rhsConst ? (rhs.poly.length ? rhs.poly[0] : R0) : null;
    if (rhsConst && Rsign(rhsVal) < 0) {
      say('<strong>No solution, and it can be seen before any algebra is done.</strong> The left side is a '
        + 'distance from zero, so it is never negative, and the right side is ' + Rtext(rhsVal)
        + '. The two cases were still worked through above, and both candidates fail the check &mdash; '
        + 'which is what "no solution" looks like from inside the method.');
    } else if (rhsConst && Rzero(rhsVal)) {
      say('<strong>One solution.</strong> Zero is the only value with a single point at that distance from '
        + 'it, so the two cases collapse into the same equation and give the same answer, ' + V + ' = '
        + kept.map(Rtext).join('') + '. This is the one absolute value equation that does not have two '
        + 'answers, and the reason is worth more than the answer.');
    } else if (kept.length === cands.length && kept.length) {
      say('<strong>' + kept.map(function (x) { return V + ' = ' + Rtext(x); }).join(' and ')
        + '.</strong> Both cases survived the check: at each one the inside came out as a number whose '
        + 'distance from zero is exactly the right side. The graphs above cross twice, once on each arm '
        + 'of the V, and neither crossing is the "same" answer with a sign changed &mdash; they came from '
        + 'two different equations.');
    } else if (kept.length) {
      say('<strong>' + kept.map(function (x) { return V + ' = ' + Rtext(x); }).join(' and ')
        + ', and the other candidate is extraneous.</strong> Splitting the bars is not a reversible step: '
        + 'it produces values that solve one of the two cases without solving the original. Only '
        + 'substituting back into |' + ins.src + '| = ' + rhs.src + ' tells them apart, which is why that '
        + 'table is not optional.');
    } else {
      say('<strong>No solution: every candidate is extraneous.</strong> The algebra produced '
        + cands.map(function (x) { return V + ' = ' + Rtext(x); }).join(' and ')
        + ', and at each one the right side is negative while the left side, being a distance, is not. '
        + 'A reader who stopped at the two cases would write down two answers here and both would be wrong.');
    }
  };

  /* ----------------------------------------------------------- wiring up */
  function redraw() {
    var fn = MODES[MODE];
    if (!fn) return trouble('this lab has no mode named ' + MODE + '.');
    try {
      fn();
    } catch (err) {
      /* Backstop. Every mode above explains its own bad input; this catches
         anything they did not anticipate and still leaves the reader a
         sentence rather than an empty panel. */
      trouble('that combination could not be worked out (' + (err && err.message ? err.message : err)
        + '). Try one of the presets and change it a little at a time.');
    }
  }

  var presetEl = el('eqPreset');
  function applyPreset() {
    if (!presetEl) return;
    var parts = String(presetEl.value).split('|');
    FIELDS.forEach(function (id, i) {
      var e = el(id);
      if (e && parts[i + FIELD_AT] !== undefined) e.value = parts[i + FIELD_AT];
    });
  }
  if (presetEl) presetEl.addEventListener('change', function () { applyPreset(); redraw(); });
  var wired = {};
  FIELDS.concat(['eqLhs', 'eqRhs', 'eqCand', 'eqFor', 'eqIns']).forEach(function (id) {
    if (wired[id]) return;
    wired[id] = 1;
    var e = el(id);
    if (e) e.addEventListener('input', redraw);
  });
  applyPreset();
  redraw();
  window.redrawLab = redraw;
"""


EQ_KPIS = {
    "check": [("left side", "eqKA"), ("right side", "eqKB"), ("balances?", "eqKC")],
    "solve": [("solution", "eqKA"), ("kind", "eqKB"), ("check", "eqKC")],
    "sides": [("collect left", "eqKA"), ("collect right", "eqKB"), ("agree?", "eqKC")],
    "fractions": [("LCD", "eqKA"), ("solution", "eqKB"), ("check", "eqKC")],
    "literal": [("solving for", "eqKA"), ("answer", "eqKB"), ("invalid when", "eqKC")],
    "type": [("kind", "eqKA"), ("what is left", "eqKB"), ("solutions", "eqKC")],
    "proportion": [("cross product", "eqKA"), ("solutions", "eqKB"), ("excluded", "eqKC")],
    "model": [("answer", "eqKA"), ("both sides", "eqKB"), ("model accepts?", "eqKC")],
    "absolute": [("case 1", "eqKA"), ("case 2", "eqKB"), ("survives", "eqKC")],
}

EQ_HINTS = {
    "check": "Fractions such as <code>1/3</code> and decimals such as <code>0.333</code> are both read "
             "exactly &mdash; and they are not the same number, which is what the third preset is for.",
    "solve": "Type any linear equation. Every row below is one operation applied to both sides, and the "
             "last table puts the answer back into what you typed.",
    "sides": "The same equation is solved twice. Watch the coefficient in the divide step: one route "
             "divides by a negative and the other does not.",
    "fractions": "Decimals count as fractions here: <code>0.2</code> is 1/5, so the multiplier the lab "
                 "finds clears decimals and fractions in one move.",
    "literal": "Any letters work. Name the one to solve for on its own line; the answer is an expression "
               "in the others, and the condition under it is part of the answer.",
    "type": "Change one number on the right and watch an identity become a contradiction: the difference "
            "between them is one constant.",
    "proportion": "The two denominators may contain <code>x</code>. When they do, the values that make "
                  "them zero are excluded before any solving happens.",
    "model": "Change the numbers and the equation is rebuilt from them, then solved, then handed back "
             "to the situation to be accepted or rejected. A decimal you type is read exactly: "
             "<code>0.15</code> becomes 3/20 and the whole model is solved in fractions.",
    "absolute": "The right side may contain <code>x</code>. When it does, the check at the bottom is the "
                "only thing standing between you and two wrong answers.",
}

EQ_LEGEND_PLOT = (
    '<div class="inline-legend">'
    '<span class="tone-cyan"><i class="legend-swatch"></i>left side</span>'
    '<span class="tone-purple"><i class="legend-swatch"></i>right side</span>'
    '<span class="tone-green"><i class="legend-swatch"></i>where they agree</span></div>'
)
EQ_LEGEND_PLAIN = (
    '<div class="inline-legend">'
    '<span class="tone-green"><i class="legend-swatch"></i>survives the check</span>'
    '<span class="tone-red"><i class="legend-swatch"></i>thrown out</span></div>'
)


def _eq_controls(mode, options, first):
    """The control panel for one mode. Only the boxes that mode reads exist in
    it, which is the rule that keeps a lab from reading an id it never
    declared -- the failure that ships a blank panel."""
    out = [_preset_field("eqPreset", "Worked example" if mode == "model" else "Statement", options)]
    if mode == "check":
        out.append(_field("eqLhs", "Left side", first[0]))
        out.append(_field("eqRhs", "Right side", first[1]))
        out.append(_field("eqCand", "Value to test", first[2]))
    elif mode == "literal":
        out.append(_field("eqLhs", "Left side", first[0]))
        out.append(_field("eqRhs", "Right side", first[1]))
        out.append(_field("eqFor", "Solve for which letter", first[2]))
    elif mode == "proportion":
        out.append(_field("eqN1", "Left numerator", first[0]))
        out.append(_field("eqD1", "Left denominator", first[1]))
        out.append(_field("eqN2", "Right numerator", first[2]))
        out.append(_field("eqD2", "Right denominator", first[3]))
    elif mode == "model":
        for i in range(4):
            out.append(_field("eqP%d" % (i + 1), "parameter %d" % (i + 1), first[i + 1],
                              label_id="eqL%d" % (i + 1)))
    elif mode == "absolute":
        out.append(_field("eqIns", "Inside the bars", first[0]))
        out.append(_field("eqRhs", "Right side", first[1]))
    else:
        out.append(_field("eqLhs", "Left side", first[0]))
        out.append(_field("eqRhs", "Right side", first[1]))
    out.append(_kpis(EQ_KPIS[mode]))
    out.append('        <p class="small-copy" style="margin:0;">%s</p>\n' % EQ_HINTS[mode])
    return "".join(out)


def equation_lab(cfg):
    """A linear equation, solved by named operations and then CHECKED.

    The teaching decision: the trace and the check are one widget, never two.
    A step list is a claim about what is allowed, and the substitution at the
    bottom is the evidence that the claim held -- computed in exact rationals
    against the equation as the reader typed it, so it can genuinely fail. Three
    of the nine modes exist because it does fail there: `proportion` and
    `absolute` both manufacture candidates that the original statement rejects,
    and `check` exists to make the definition of a solution the reader's first
    tool rather than their last.

    The mode also decides the controls. A mode that reads a box builds that box;
    nothing is hidden, disabled or shared between modes it does not belong to.
    """
    mode = cfg.get("mode", "solve")
    if mode not in EQ_PRESETS:
        mode = "solve"
    presets = cfg.get("presets") or EQ_PRESETS[mode]
    fields, field_at = EQ_FIELDS[mode]
    title, subtitle = EQ_TITLES[mode]

    options = "".join(
        '<option value="%s">%s</option>' % ("|".join(rest), label)
        for label, *rest in presets
    )
    first = list(presets[0][1:])

    markup = (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="eqTitle">a statement to solve</strong>'
        '<span id="eqSub"></span></div>\n'
        "        %s\n"
        "      </div>\n"
        "%s"
        '      <div id="eqWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="eqStatus" style="margin-top:12px;"></div>'
        % (
            EQ_LEGEND_PLOT if mode in EQ_PLOT_MODES else EQ_LEGEND_PLAIN,
            '      <div class="lab-stage"><svg id="eqPlot"></svg></div>\n'
            if mode in EQ_PLOT_MODES else "",
        )
    )

    controls = _eq_controls(mode, options, first)
    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + SURD_JS + PLOT_JS + FORM_JS + SYMBOL_JS
        + _own_ids(markup, controls)
        + "\n  var MODE = '%s';\n" % mode
        + "  var FIELDS = [%s];\n" % ", ".join("'%s'" % f for f in fields)
        + "  var FIELD_AT = %d;\n" % field_at
        + EQ_JS
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a statement, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every number below is worked out here, in exact fractions, from what these boxes hold. "
            "Change one and the trace, the check and the picture are all recomputed together.",
        ),
        script=script,
    )


# --------------------------------------------------------------------------
# The inequality lab. An inequality's answer is a SET, so the lab computes
# sets: intervals with exact endpoints, intersected and unioned by code, then
# drawn, and printed in two notations, from the same structure.
# --------------------------------------------------------------------------

SET_JS = r"""
  /* An interval. A null endpoint is unbounded on that side, and the two flags
     say whether the ends belong to it -- the distinction the whole notation
     lesson turns on. */
  function iv(lo, loC, hi, hiC) { return { lo: lo, loC: !!loC, hi: hi, hiC: !!hiC }; }
  var ALLR = [iv(null, false, null, false)];

  function ivEmpty(i) {
    if (i.lo === null || i.hi === null) return false;
    var c = Rcmp(i.lo, i.hi);
    return c > 0 || (c === 0 && !(i.loC && i.hiC));
  }
  function ivPoint(i) {
    return i.lo !== null && i.hi !== null && Rcmp(i.lo, i.hi) === 0 && i.loC && i.hiC;
  }
  function ivHas(i, x) {
    if (i.lo !== null) { var c = Rcmp(x, i.lo); if (c < 0 || (c === 0 && !i.loC)) return false; }
    if (i.hi !== null) { var d = Rcmp(x, i.hi); if (d > 0 || (d === 0 && !i.hiC)) return false; }
    return true;
  }
  function setHas(s, x) {
    for (var i = 0; i < s.length; i += 1) if (ivHas(s[i], x)) return true;
    return false;
  }
  /* Order by lower endpoint, -inf first, and a closed end before an open one at
     the same number so that [1,2] and (1,3) merge in the right direction. */
  function loCmp(a, b) {
    if (a.lo === null && b.lo === null) return 0;
    if (a.lo === null) return -1;
    if (b.lo === null) return 1;
    var c = Rcmp(a.lo, b.lo);
    if (c !== 0) return c;
    return (a.loC === b.loC) ? 0 : (a.loC ? -1 : 1);
  }
  /* Sorted, non-empty, non-overlapping. Two pieces that touch at a point are
     merged only when at least one of them CONTAINS that point: [1,2) and (2,3)
     leave a hole at 2 and stay apart, which is exactly the answer a quadratic
     with a repeated root produces. */
  function setNorm(list) {
    var xs = list.filter(function (i) { return !ivEmpty(i); }).sort(loCmp), out = [];
    xs.forEach(function (i) {
      var last = out[out.length - 1];
      if (!last) { out.push(iv(i.lo, i.loC, i.hi, i.hiC)); return; }
      var joins;
      if (last.hi === null) joins = true;
      else if (i.lo === null) joins = true;
      else {
        var c = Rcmp(i.lo, last.hi);
        joins = c < 0 || (c === 0 && (last.hiC || i.loC));
      }
      if (!joins) { out.push(iv(i.lo, i.loC, i.hi, i.hiC)); return; }
      if (last.hi === null) return;
      if (i.hi === null) { last.hi = null; last.hiC = false; return; }
      var d = Rcmp(i.hi, last.hi);
      if (d > 0) { last.hi = i.hi; last.hiC = i.hiC; }
      else if (d === 0) { last.hiC = last.hiC || i.hiC; }
    });
    return out;
  }
  function setUnion(a, b) { return setNorm(a.concat(b)); }
  function ivMeet(x, y) {
    var lo, loC, hi, hiC, c;
    if (x.lo === null) { lo = y.lo; loC = y.loC; }
    else if (y.lo === null) { lo = x.lo; loC = x.loC; }
    else {
      c = Rcmp(x.lo, y.lo);
      lo = c >= 0 ? x.lo : y.lo;
      loC = c > 0 ? x.loC : (c < 0 ? y.loC : (x.loC && y.loC));
    }
    if (x.hi === null) { hi = y.hi; hiC = y.hiC; }
    else if (y.hi === null) { hi = x.hi; hiC = x.hiC; }
    else {
      c = Rcmp(x.hi, y.hi);
      hi = c <= 0 ? x.hi : y.hi;
      hiC = c < 0 ? x.hiC : (c > 0 ? y.hiC : (x.hiC && y.hiC));
    }
    return iv(lo, loC, hi, hiC);
  }
  function setMeet(a, b) {
    var out = [];
    a.forEach(function (x) {
      b.forEach(function (y) {
        var m = ivMeet(x, y);
        if (!ivEmpty(m)) out.push(m);
      });
    });
    return setNorm(out);
  }

  /* ---- the same set, said four ways ---- */
  function ivText(i) {
    return (i.loC ? '[' : '(') + (i.lo === null ? '-inf' : Rtext(i.lo)) + ', '
      + (i.hi === null ? 'inf' : Rtext(i.hi)) + (i.hiC ? ']' : ')');
  }
  function setText(s) {
    if (!s.length) return '{ }';
    if (s.length === 1 && s[0].lo === null && s[0].hi === null) return '(-inf, inf)';
    return s.map(ivText).join(' U ');
  }
  function ivIneq(i, v) {
    if (i.lo === null && i.hi === null) return 'every real ' + v;
    if (ivPoint(i)) return v + ' = ' + Rtext(i.lo);
    if (i.lo === null) return v + ' ' + relText(i.hiC ? '<=' : '<') + ' ' + Rtext(i.hi);
    if (i.hi === null) return v + ' ' + relText(i.loC ? '>=' : '>') + ' ' + Rtext(i.lo);
    return Rtext(i.lo) + ' ' + relText(i.loC ? '<=' : '<') + ' ' + v + ' '
      + relText(i.hiC ? '<=' : '<') + ' ' + Rtext(i.hi);
  }
  function setIneq(s, v) {
    if (!s.length) return 'no ' + v + ' at all';
    return s.map(function (i) { return ivIneq(i, v); }).join('  or  ');
  }
  function setBuilder(s, v) {
    if (!s.length) return '{ }';
    if (s.length === 1 && s[0].lo === null && s[0].hi === null) return '{ ' + v + ' in R }';
    return '{ ' + v + ' in R : ' + setIneq(s, v) + ' }';
  }
  function setWords(s, v) {
    if (!s.length) return 'no number satisfies it';
    if (s.length === 1 && s[0].lo === null && s[0].hi === null) return 'every real number satisfies it';
    if (s.length === 1 && ivPoint(s[0])) return 'exactly one number satisfies it';
    return s.length === 1 ? 'one stretch of the line' : s.length + ' separate stretches of the line';
  }

  /* A window wide enough to show every endpoint with room around it. */
  function lineWindow(set, extra) {
    var xs = (extra || []).slice();
    set.forEach(function (i) {
      if (i.lo !== null) xs.push(Rnum(i.lo));
      if (i.hi !== null) xs.push(Rnum(i.hi));
    });
    xs = xs.filter(function (x) { return isFinite(x); });
    if (!xs.length) return { lo: -5, hi: 5 };
    var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs);
    var pad = Math.max(2, (hi - lo) * 0.6);
    return { lo: lo - pad, hi: hi + pad };
  }
  /* The set on a number line, drawn from the same endpoints that were printed.
     Filled ends are the ones that belong to the set. */
  function drawSet(svg, set, win, note) {
    if (!svg) return;
    var line = NumberLine(svg, win.lo, win.hi), span = win.hi - win.lo;
    set.forEach(function (i) {
      if (ivPoint(i)) { line.point(Rnum(i.lo), true); return; }
      var a = i.lo === null ? win.lo - span : Rnum(i.lo);
      var b = i.hi === null ? win.hi + span : Rnum(i.hi);
      line.interval(a, b, i.loC, i.hiC);
    });
    line.describe(note);
  }
"""


# Ops travel through the option values as two letters so that the markup never
# has to carry a bare < inside an attribute.
INEQ_OPS = [("lt", "&lt;"), ("le", "&le;"), ("gt", "&gt;"), ("ge", "&ge;")]

INEQ_PRESETS = {
    "linear": [
        ("3x - 4 < 11", "3x - 4", "lt", "11"),
        ("-2x > 6", "-2x", "gt", "6"),
        ("5 - 3x >= 2x + 15", "5 - 3x", "ge", "2x + 15"),
        ("(1/2)x + 1 <= (1/3)x", "(1/2)x + 1", "le", "(1/3)x"),
        ("2x + 1 > 2x", "2x + 1", "gt", "2x"),
        ("2x + 1 < 2x", "2x + 1", "lt", "2x"),
    ],
    "compound": [
        ("3 < 2x + 1  and  2x + 1 <= 9", "3", "lt", "2x + 1", "and", "2x + 1", "le", "9"),
        ("2x + 1 >= 5  and  x - 4 < 0", "2x + 1", "ge", "5", "and", "x - 4", "lt", "0"),
        ("x > 5  and  x < 2", "x", "gt", "5", "and", "x", "lt", "2"),
        ("x >= 3  and  x <= 3", "x", "ge", "3", "and", "x", "le", "3"),
        ("x < -2  or  x >= 3", "x", "lt", "-2", "or", "x", "ge", "3"),
        ("x < 4  or  x > 1", "x", "lt", "4", "or", "x", "gt", "1"),
    ],
    "absolute": [
        ("|x - 2| < 5", "x - 2", "lt", "5"),
        ("|x - 2| > 5", "x - 2", "gt", "5"),
        ("|3 - 2x| >= 7", "3 - 2x", "ge", "7"),
        ("|2x + 1| <= 0", "2x + 1", "le", "0"),
        ("|x + 3| < -1", "x + 3", "lt", "-1"),
        ("|x + 3| > -1", "x + 3", "gt", "-1"),
    ],
    "notation": [
        ("[2, 5)", "2", "c", "5", "o", "5"),
        ("(-inf, 3]", "-inf", "o", "3", "c", "3"),
        ("(-2, inf)", "-2", "o", "inf", "o", "-2"),
        ("[4, 4]  a single point", "4", "c", "4", "c", "4"),
        ("(4, 4)  nothing at all", "4", "o", "4", "o", "4"),
        ("[5, 2]  written backwards", "5", "c", "2", "c", "3"),
    ],
    "quadratic": [
        ("x^2 - 5x + 6 > 0", "x^2 - 5x + 6", "gt", "0"),
        ("x^2 - 5x + 6 <= 0", "x^2 - 5x + 6", "le", "0"),
        ("x^2 > 4", "x^2", "gt", "4"),
        ("x^2 - 4x + 4 > 0", "x^2 - 4x + 4", "gt", "0"),
        ("x^2 - 2x - 4 < 0", "x^2 - 2x - 4", "lt", "0"),
        ("x^2 + 1 <= 0", "x^2 + 1", "le", "0"),
    ],
}

INEQ_TITLES = {
    "linear": ("Solving an inequality", "The same steps, and the one that reverses"),
    "compound": ("And, or, and the line", "Two statements at once: overlap or gather"),
    "absolute": ("Absolute value inequalities", "Less than gives a band, greater than gives two rays"),
    "notation": ("Writing a solution set down", "Four notations for one set of numbers"),
    "quadratic": ("Quadratic inequalities", "Sign analysis on the factored form"),
}

INEQ_FIELDS = {
    "linear": ["iqLhs", "iqOp", "iqRhs"],
    "compound": ["iqLhs", "iqOp", "iqRhs", "iqConn", "iqLhs2", "iqOp2", "iqRhs2"],
    "absolute": ["iqIns", "iqOp", "iqRhs"],
    "notation": ["iqLo", "iqLoB", "iqHi", "iqHiB", "iqTest"],
    "quadratic": ["iqLhs", "iqOp", "iqRhs"],
}

INEQ_KPIS = {
    "linear": [("solution", "iqKA"), ("interval", "iqKB"), ("sign reversed?", "iqKC")],
    "compound": [("first", "iqKA"), ("second", "iqKB"), ("combined", "iqKC")],
    "absolute": [("case 1", "iqKA"), ("case 2", "iqKB"), ("combined", "iqKC")],
    "notation": [("interval", "iqKA"), ("what it is", "iqKB"), ("test value", "iqKC")],
    "quadratic": [("factored", "iqKA"), ("critical points", "iqKB"), ("solution", "iqKC")],
}

INEQ_HINTS = {
    "linear": "Multiply or divide by a negative and the statement reverses. The trace names that step "
              "and says why; the table under it tests the answer against what you typed.",
    "compound": "<code>and</code> keeps the numbers in both sets, <code>or</code> keeps the numbers in "
                "either. Two of the presets show what that does when the sets miss each other entirely.",
    "absolute": "The right side may be negative. Both of those presets are worth doing before you trust "
                "the two-case rule.",
    "notation": "Type <code>-inf</code> or <code>inf</code> for an unbounded end. Infinity is not a number, "
                "so it can never be included &mdash; try to close that bracket and see what happens.",
    "quadratic": "The sign of each factor is worked out at an exact test value inside each interval, so "
                 "the table is evidence rather than a rule of thumb.",
}

INEQ_LEGEND = (
    '<div class="inline-legend">'
    '<span class="tone-cyan"><i class="legend-swatch"></i>the solution set</span>'
    '<span class="tone-green"><i class="legend-swatch"></i>satisfies the statement</span>'
    '<span class="tone-red"><i class="legend-swatch"></i>fails it</span></div>'
)


INEQ_JS = r"""
  /* --------------------------------------------------------- the controls */
  /* As in the equation lab: five modes share this script and do not share
     their controls, so an id is asked for only when this mode declared it. */
  function el(id) { return OWN[id] ? document.getElementById(id) : null; }
  function val(id) { var e = el(id); return e ? String(e.value) : ''; }
  function kpi(id, text) { var e = el(id); if (e) e.innerHTML = text; }
  var titleEl = el('iqTitle'), subEl = el('iqSub'),
      workEl = el('iqWork'), statusEl = el('iqStatus');
  function say(html) { statusEl.innerHTML = html; }
  var V = 'x';
  var OPS = { lt: '<', le: '<=', gt: '>', ge: '>=' };
  function readOp(id) { return OPS[val(id)] || '<'; }

  function trouble(msg) {
    workEl.innerHTML = '';
    ['iqLine', 'iqLineA', 'iqLineB', 'iqPlot'].forEach(function (id) {
      var svg = el(id);
      if (svg) svg.textContent = '';
    });
    kpi('iqKA', '--'); kpi('iqKB', '--'); kpi('iqKC', '--');
    if (titleEl) titleEl.textContent = 'waiting for a statement';
    if (subEl) subEl.textContent = '';
    say('<strong>Nothing to work with yet.</strong> ' + msg);
  }

  /* One linear inequality, solved, with its answer as a SET. Everything that
     follows -- the drawing, both notations, the tests -- is generated from
     that one structure, so they cannot contradict each other. */
  function solveIneq(L, Rr, v, rel) {
    var tr = traceLinear(L, Rr, v, rel, true);
    if (tr.kind === 'all') return { tr: tr, set: ALLR };
    if (tr.kind === 'none') return { tr: tr, set: [] };
    var x = tr.value, r = tr.rel;
    if (r === '<') return { tr: tr, set: [iv(null, false, x, false)] };
    if (r === '<=') return { tr: tr, set: [iv(null, false, x, true)] };
    if (r === '>') return { tr: tr, set: [iv(x, false, null, false)] };
    return { tr: tr, set: [iv(x, true, null, false)] };
  }

  function notationRows(set, v) {
    return [
      trow('as an inequality', '<code>' + setIneq(set, v) + '</code>'),
      trow('in interval notation', '<code>' + setText(set) + '</code>'),
      trow('in set-builder notation', '<code>' + setBuilder(set, v) + '</code>'),
      trow('in words', setWords(set, v))
    ];
  }

  /* The test that catches a reversed sign. Each value is put into the statement
     the reader typed AND looked up in the computed set; the two columns have to
     agree, and the lab says so loudly if they ever do not. */
  function agreeGrid(caption, xs, holdsFn, set, v) {
    var mismatch = false;
    var rows = xs.map(function (x) {
      var holds = holdsFn(x), inSet = setHas(set, x);
      if (holds !== inSet) mismatch = true;
      return tcells([
        '<code>' + v + ' = ' + Rtext(x) + '</code>',
        holds ? YES : NO,
        inSet ? 'in it' : 'not in it',
        holds === inSet ? chip('agree', 'ok') : chip('DISAGREE', 'no')
      ], holds ? 'focus' : '');
    });
    return {
      html: tgrid(caption, [v, 'the statement you typed', 'the answer set', ''], rows),
      mismatch: mismatch
    };
  }
  /* Values worth testing: on each boundary and one step either side of it. */
  function probesAround(points) {
    var out = [], seen = {};
    function add(r) {
      var k = Rtext(r);
      if (!seen[k]) { seen[k] = 1; out.push(r); }
    }
    add(R0);
    points.forEach(function (p) { add(Rsub(p, R1)); add(p); add(Radd(p, R1)); });
    out.sort(Rcmp);
    return out.slice(0, 9);
  }
  function boundsOf(set) {
    var out = [];
    set.forEach(function (i) {
      if (i.lo !== null) out.push(i.lo);
      if (i.hi !== null) out.push(i.hi);
    });
    return out;
  }
  function degTrouble(a, b) {
    return 'the highest power here is ' + V + '^' + Math.max(Pdeg(a), Pdeg(b))
      + '. Adding to and dividing both sides only solves LINEAR inequalities; a squared term '
      + 'changes sign twice and needs the sign analysis in the quadratic mode of this lab.';
  }

  var MODES = {};

  /* ============================================================= linear ==
     One operation at a time, exactly as in the equation lab, with one
     difference: multiplying or dividing by a negative reverses the statement.
     That step is bold in the trace because it is the only rule in this course
     that a reader will otherwise apply from memory and get backwards. */
  MODES.linear = function () {
    var L = sideOf(val('iqLhs'), V, 'left side'), Rs = sideOf(val('iqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    if (Pdeg(L.poly) > 1 || Pdeg(Rs.poly) > 1) return trouble(degTrouble(L.poly, Rs.poly));
    var op = readOp('iqOp');
    var typed = L.src + ' ' + relText(op) + ' ' + Rs.src;
    titleEl.innerHTML = typed;

    var res = solveIneq(L.poly, Rs.poly, V, op);
    var set = res.set, tr = res.tr;
    var holds = function (x) { return relHolds(Peval(L.poly, x), Peval(Rs.poly, x), op); };
    var probes = probesAround(tr.kind === 'unique' ? [tr.value] : [R0, R1]);
    var test = agreeGrid('Testing values against the statement you typed', probes, holds, set, V);

    workEl.innerHTML = [
      ttable('Each step, and what it did to both sides',
        [trow('as typed', '<code>' + typed + '</code>')].concat(traceRows(tr, typed))),
      ttable('The answer, written four ways', notationRows(set, V)),
      test.html
    ].join('');
    kpi('iqKA', tr.kind === 'unique' ? V + ' ' + relText(tr.rel) + ' ' + Rtext(tr.value)
      : (tr.kind === 'all' ? 'every ' + V : 'no ' + V));
    kpi('iqKB', setText(set));
    kpi('iqKC', tr.flipped ? 'yes' : 'no');
    subEl.innerHTML = setText(set);

    var win = lineWindow(set, [0]);
    drawSet(el('iqLine'), set, win, 'the solution set on the number line: ' + setText(set));

    var msg;
    if (tr.kind === 'all') {
      msg = '<strong>Every real number works.</strong> The ' + V + ' terms cancelled and left '
        + tr.constText + ', which is true whatever ' + V + ' is. The solution set is the whole line, '
        + 'written (-inf, inf).';
    } else if (tr.kind === 'none') {
      msg = '<strong>No number works.</strong> The ' + V + ' terms cancelled and left ' + tr.constText
        + ', which is false whatever ' + V + ' is. The solution set is empty, and an empty set is an '
        + 'answer rather than a failure to find one.';
    } else if (tr.flipped) {
      msg = '<strong>' + V + ' ' + relText(tr.rel) + ' ' + Rtext(tr.value)
        + ', and the statement reversed on the way.</strong> Dividing by ' + Rtext(tr.coef)
        + ' turned ' + relText(op) + ' into ' + relText(tr.rel) + '. The reason is not a convention: '
        + 'multiplying by a negative number reverses the order of every pair of numbers on the line, so '
        + 'a statement about which of two things is bigger has to turn round with it. The test table '
        + 'above is the check &mdash; a reader who forgets the rule gets a set whose every row disagrees '
        + 'with the original statement.';
    } else {
      msg = '<strong>' + V + ' ' + relText(tr.rel) + ' ' + Rtext(tr.value) + '.</strong> '
        + 'Nothing reversed here: every step added to or subtracted from both sides'
        + (Requ(tr.coef, R1)
          ? ', and the coefficient of ' + V + ' was already 1, so there was no division to do.'
          : ', or divided by ' + Rtext(tr.coef) + ', which is positive.')
        + ' Adding a number to both sides slides the whole line and does not reorder it, and neither '
        + 'does multiplying by a positive one.';
    }
    if (test.mismatch) {
      msg += ' <strong>Warning: a test value disagrees with the computed set.</strong> That is a fault '
        + 'in this lab, not in the arithmetic above, and it should be reported.';
    }
    say(msg);
  };

  /* =========================================================== compound ==
     Two statements and one line. `and` is the overlap, `or` is everything
     either one covers, and both are computed as set operations on intervals
     rather than reasoned about in words. */
  MODES.compound = function () {
    var L1 = sideOf(val('iqLhs'), V, 'first left side'), R1s = sideOf(val('iqRhs'), V, 'first right side'),
        L2 = sideOf(val('iqLhs2'), V, 'second left side'), R2s = sideOf(val('iqRhs2'), V, 'second right side');
    var bad = [L1, R1s, L2, R2s].filter(function (x) { return !x.ok; });
    if (bad.length) return trouble(bad[0].msg);
    if (Pdeg(L1.poly) > 1 || Pdeg(R1s.poly) > 1) return trouble(degTrouble(L1.poly, R1s.poly));
    if (Pdeg(L2.poly) > 1 || Pdeg(R2s.poly) > 1) return trouble(degTrouble(L2.poly, R2s.poly));

    var op1 = readOp('iqOp'), op2 = readOp('iqOp2');
    var conn = val('iqConn') === 'or' ? 'or' : 'and';
    var t1 = L1.src + ' ' + relText(op1) + ' ' + R1s.src;
    var t2 = L2.src + ' ' + relText(op2) + ' ' + R2s.src;
    titleEl.innerHTML = t1 + '  <strong>' + conn + '</strong>  ' + t2;

    var a = solveIneq(L1.poly, R1s.poly, V, op1), b = solveIneq(L2.poly, R2s.poly, V, op2);
    var result = conn === 'and' ? setMeet(a.set, b.set) : setUnion(a.set, b.set);

    var holds = function (x) {
      var h1 = relHolds(Peval(L1.poly, x), Peval(R1s.poly, x), op1);
      var h2 = relHolds(Peval(L2.poly, x), Peval(R2s.poly, x), op2);
      return conn === 'and' ? (h1 && h2) : (h1 || h2);
    };
    var probes = probesAround(boundsOf(a.set).concat(boundsOf(b.set)));
    var test = agreeGrid('Testing values against both statements', probes, holds, result, V);

    workEl.innerHTML = [
      ttable('The first statement, solved',
        [trow('as typed', '<code>' + t1 + '</code>')].concat(traceRows(a.tr, t1))),
      ttable('The second statement, solved',
        [trow('as typed', '<code>' + t2 + '</code>')].concat(traceRows(b.tr, t2))),
      ttable('Putting them together', [
        trow('the first set', '<code>' + setText(a.set) + '</code>'),
        trow('the second set', '<code>' + setText(b.set) + '</code>'),
        trow(conn === 'and' ? 'and: the numbers in BOTH' : 'or: the numbers in EITHER',
          '<code>' + setText(result) + '</code>'),
        trow('in set-builder notation', '<code>' + setBuilder(result, V) + '</code>')
      ]),
      test.html
    ].join('');
    kpi('iqKA', setText(a.set));
    kpi('iqKB', setText(b.set));
    kpi('iqKC', setText(result));
    subEl.innerHTML = setText(result);

    var win = lineWindow(setUnion(a.set, b.set), [0]);
    drawSet(el('iqLineA'), a.set, win, 'the first statement: ' + setText(a.set));
    drawSet(el('iqLineB'), b.set, win, 'the second statement: ' + setText(b.set));
    drawSet(el('iqLine'), result, win, 'the combined set: ' + setText(result));

    var msg;
    if (!result.length) {
      msg = '<strong>Nothing satisfies both.</strong> The two sets do not overlap anywhere, so the '
        + 'intersection is empty and the third line above is blank. The tempting move is to write the '
        + 'pair as one chain &mdash; and a chain such as <code>5 &lt; ' + V + ' &lt; 2</code> claims a '
        + 'number is above 5 and below 2 at the same time. Writing it down does not make such a number '
        + 'exist; it only hides that the answer is the empty set.';
    } else if (result.length === 1 && result[0].lo === null && result[0].hi === null) {
      msg = '<strong>Every real number satisfies it.</strong> The two sets between them cover the whole '
        + 'line, and with <code>or</code> a number only has to be in one of them. This is the case that '
        + 'looks wrong on the page and is obvious on the three lines above.';
    } else if (result.length === 1 && ivPoint(result[0])) {
      msg = '<strong>Exactly one number satisfies both:</strong> ' + V + ' = ' + Rtext(result[0].lo)
        + '. Each statement allows a half-line, and the two half-lines meet at a single point. '
        + '"' + V + ' &ge; 3 and ' + V + ' &le; 3" is how ' + V + ' = 3 is written when it arrives as '
        + 'two inequalities.';
    } else {
      msg = '<strong>' + setText(result) + '</strong> is the answer, and the three number lines above '
        + 'show how it was built: the first statement, the second, and '
        + (conn === 'and' ? 'the part they have in common.' : 'everything either one covers.')
        + ' With <code>' + conn + '</code>, a number belongs to the answer when it is in '
        + (conn === 'and' ? 'both' : 'at least one') + ' of the first two.';
    }
    if (test.mismatch) {
      msg += ' <strong>Warning: a test value disagrees with the computed set.</strong>';
    }
    say(msg);
  };
"""


INEQ_JS += r"""
  /* =========================================================== absolute ==
     |A| < c is ONE band and |A| > c is TWO rays, and the reason is the same
     sentence in both cases: |A| is the distance from A to zero. Both cases are
     solved by the linear trace and then combined as sets -- an intersection
     for less-than, a union for greater-than. */
  MODES.absolute = function () {
    var ins = sideOf(val('iqIns'), V, 'expression inside the bars'),
        rhs = sideOf(val('iqRhs'), V, 'right side');
    if (!ins.ok) return trouble(ins.msg);
    if (!rhs.ok) return trouble(rhs.msg);
    if (Pdeg(ins.poly) > 1 || Pdeg(rhs.poly) > 1) return trouble(degTrouble(ins.poly, rhs.poly));
    var op = readOp('iqOp');
    var less = op === '<' || op === '<=';
    var typed = '|' + ins.src + '| ' + relText(op) + ' ' + rhs.src;
    titleEl.innerHTML = typed;

    var negRhs = Pscale(rhs.poly, R(-1n));
    var a = solveIneq(ins.poly, rhs.poly, V, op);              /* A  op  B   */
    var b = solveIneq(ins.poly, negRhs, V, relSwap(op));       /* A  op' -B  */
    var set = less ? setMeet(a.set, b.set) : setUnion(a.set, b.set);

    var holds = function (x) {
      return relHolds(Rabs(Peval(ins.poly, x)), Peval(rhs.poly, x), op);
    };
    var probes = probesAround(boundsOf(a.set).concat(boundsOf(b.set)));
    var test = agreeGrid('Testing values against |' + ins.src + '| ' + relText(op) + ' ' + rhs.src,
      probes, holds, set, V);

    var meaning = less
      ? '|' + ins.src + '| ' + relText(op) + ' ' + rhs.src + ' says the distance from '
        + ins.src + ' to 0 is ' + (op === '<' ? 'less than ' : 'at most ') + rhs.src
        + ', which pins ' + ins.src + ' between -(' + rhs.src + ') and ' + rhs.src + ' &mdash; BOTH at once.'
      : '|' + ins.src + '| ' + relText(op) + ' ' + rhs.src + ' says the distance from '
        + ins.src + ' to 0 is ' + (op === '>' ? 'more than ' : 'at least ') + rhs.src
        + ', which happens when ' + ins.src + ' is far out on EITHER side.';

    workEl.innerHTML = [
      ttable('What the bars say', [
        trow('the statement', '<code>' + typed + '</code>'),
        trow('what it means', meaning),
        trow('so it becomes', less
          ? '<code>' + Ptext(negRhs, V) + ' ' + relText(op) + ' ' + Ptext(ins.poly, V) + ' '
            + relText(op) + ' ' + Ptext(rhs.poly, V) + '</code> &mdash; a chain, because both halves '
            + 'have to hold at once'
          : '<code>' + Ptext(ins.poly, V) + ' ' + relText(op) + ' ' + Ptext(rhs.poly, V)
            + '</code> or <code>' + Ptext(ins.poly, V) + ' ' + relText(relSwap(op)) + ' '
            + Ptext(negRhs, V) + '</code>')
      ]),
      ttable('Case 1: ' + Ptext(ins.poly, V) + ' ' + relText(op) + ' ' + Ptext(rhs.poly, V),
        traceRows(a.tr).concat([trow('as a set', '<code>' + setText(a.set) + '</code>')])),
      ttable('Case 2: ' + Ptext(ins.poly, V) + ' ' + relText(relSwap(op)) + ' ' + Ptext(negRhs, V),
        traceRows(b.tr).concat([trow('as a set', '<code>' + setText(b.set) + '</code>')])),
      ttable(less ? 'The two cases, intersected' : 'The two cases, unioned',
        [trow(less ? 'both at once' : 'either one', '<code>' + setText(set) + '</code>')]
          .concat(notationRows(set, V))),
      test.html
    ].join('');
    kpi('iqKA', setText(a.set));
    kpi('iqKB', setText(b.set));
    kpi('iqKC', setText(set));
    subEl.innerHTML = setText(set);

    var win = lineWindow(set.length ? set : setUnion(a.set, b.set), [0]);
    drawSet(el('iqLine'), set, win, 'the solution set: ' + setText(set));

    /* The V and the level it is compared with, drawn from the same polynomials. */
    var svg = el('iqPlot');
    if (svg) {
      var fIns = polyFn(ins.poly), fRhs = polyFn(rhs.poly);
      var fAbs = function (x) { return Math.abs(fIns(x)); };
      var lo = Infinity, hi = -Infinity, i, x;
      for (i = 0; i <= 80; i += 1) {
        x = win.lo + (win.hi - win.lo) * i / 80;
        [fAbs(x), fRhs(x)].forEach(function (y) {
          if (isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); }
        });
      }
      if (!isFinite(lo) || !isFinite(hi)) { lo = -2; hi = 5; }
      if (hi - lo < 1e-9) { lo -= 3; hi += 3; }
      var pad = Math.max(1, (hi - lo) * 0.2);
      var plot = Plot(svg, { xmin: win.lo, xmax: win.hi, ymin: lo - pad, ymax: hi + pad });
      plot.frame();
      plot.curve(fAbs, 'plot-curve');
      plot.curve(fRhs, 'plot-curve alt');
      boundsOf(set).forEach(function (r) { plot.point(Rnum(r), Rnum(Peval(rhs.poly, r)), 'plot-point root'); });
      plot.describe('the V-shaped graph of |' + ins.src + '| against ' + rhs.src
        + '; the solution set is where the V is '
        + (less ? 'below' : 'above') + ' the other graph');
    }

    var rhsConst = Pdeg(rhs.poly) <= 0;
    var c = rhsConst ? (rhs.poly.length ? rhs.poly[0] : R0) : null;
    var msg;
    if (rhsConst && Rsign(c) < 0 && less) {
      msg = '<strong>Nothing satisfies it, and no algebra is needed to see why.</strong> The left side is '
        + 'a distance, so it is never negative, and it cannot be below ' + Rtext(c) + '. The two cases '
        + 'were still solved above, and their overlap came out empty &mdash; which is what an impossible '
        + 'statement looks like from inside the method.';
    } else if (rhsConst && Rsign(c) < 0 && !less) {
      msg = '<strong>Every real number satisfies it.</strong> A distance is never negative, so it is '
        + 'always above ' + Rtext(c) + '. The two rays above overlap and cover the whole line.';
    } else if (!set.length) {
      msg = '<strong>The solution set is empty.</strong> The two cases have no number in common.';
    } else if (set.length === 1 && ivPoint(set[0])) {
      msg = '<strong>Exactly one number: ' + V + ' = ' + Rtext(set[0].lo) + '.</strong> '
        + 'Only zero is at distance zero from zero, so a statement of the form |A| &le; 0 collapses to '
        + 'A = 0. The band has closed up to a point.';
    } else if (less) {
      msg = '<strong>' + setText(set) + ': one band.</strong> Less-than gives a single interval because '
        + 'the two conditions have to hold together, and the answer is their overlap. The common mistake '
        + 'is to write it as two separate pieces joined by "or", which would claim every number outside '
        + 'the band as well.';
    } else {
      var chain = (set.length === 2 && set[0].hi !== null && set[1].lo !== null)
        ? Rtext(set[1].lo) + ' &lt; ' + V + ' &lt; ' + Rtext(set[0].hi) : null;
      msg = '<strong>' + setText(set) + ': two rays.</strong> Greater-than gives two pieces because a '
        + 'number can be far from zero in either direction, and it only has to manage one of them. '
        + (chain
          ? 'Squeezing the answer into a chain would give <code>' + chain + '</code>, which no number '
            + 'satisfies &mdash; the two pieces point away from each other and cannot be joined. '
          : '')
        + 'The answer has to stay two pieces joined by "or".';
    }
    if (test.mismatch) msg += ' <strong>Warning: a test value disagrees with the computed set.</strong>';
    say(msg);
  };

  /* =========================================================== notation ==
     Four ways of writing one set, generated from one structure so they cannot
     drift apart, plus the two errors that the notation itself invites: closing
     a bracket on infinity, and writing the endpoints the wrong way round. */
  function readEndpoint(text) {
    var s = String(text).trim().toLowerCase();
    if (s === 'inf' || s === '+inf' || s === 'infinity' || s === '+infinity') return { inf: 1 };
    if (s === '-inf' || s === '-infinity') return { inf: -1 };
    var r = parseR(text);
    return r === null ? null : { r: r };
  }

  MODES.notation = function () {
    var lo = readEndpoint(val('iqLo')), hi = readEndpoint(val('iqHi'));
    if (lo === null) return trouble('the left endpoint must be a number or <code>-inf</code>.');
    if (hi === null) return trouble('the right endpoint must be a number or <code>inf</code>.');
    if (lo.inf === 1) return trouble('the left endpoint cannot be +infinity: an interval runs upward.');
    if (hi.inf === -1) return trouble('the right endpoint cannot be -infinity: an interval runs upward.');

    var loClosed = val('iqLoB') === 'c', hiClosed = val('iqHiB') === 'c';
    var notes = [];
    if (lo.inf && loClosed) {
      loClosed = false;
      notes.push('Infinity is not a number, so it is never in the set and the bracket beside it is '
        + 'always round. The left bracket has been corrected to <code>(</code>.');
    }
    if (hi.inf && hiClosed) {
      hiClosed = false;
      notes.push('Same on the right: <code>inf]</code> would claim that infinity is one of the numbers '
        + 'in the set. The right bracket has been corrected to <code>)</code>.');
    }
    var interval = iv(lo.inf ? null : lo.r, loClosed, hi.inf ? null : hi.r, hiClosed);
    var empty = ivEmpty(interval);
    var set = empty ? [] : [interval];
    var written = (loClosed ? '[' : '(') + (lo.inf ? '-inf' : Rtext(lo.r)) + ', '
      + (hi.inf ? 'inf' : Rtext(hi.r)) + (hiClosed ? ']' : ')');
    titleEl.textContent = written;

    var kind;
    if (empty) {
      kind = (interval.lo !== null && interval.hi !== null && Rcmp(interval.lo, interval.hi) > 0)
        ? 'endpoints the wrong way round' : 'empty';
    } else if (interval.lo === null && interval.hi === null) kind = 'the whole line';
    else if (ivPoint(interval)) kind = 'a single point';
    else if (interval.lo === null || interval.hi === null) kind = 'a half-line';
    else kind = 'a bounded interval';

    var testR = parseR(val('iqTest'));
    var rows = notationRows(set, V);
    rows.push(trow('is it bounded?', interval.lo !== null && interval.hi !== null && !empty
      ? 'yes, at both ends' : (empty ? 'there is nothing to bound' : 'no &mdash; it runs for ever in at least one direction')));
    if (testR !== null) {
      rows.push(trow('is ' + Rtext(testR) + ' in it?', setHas(set, testR)
        ? chip('yes', 'ok') + ' every condition in the set-builder form holds at ' + Rtext(testR)
        : chip('no', 'no') + ' at least one condition fails at ' + Rtext(testR)));
    } else {
      rows.push(trow('the test value', 'not a number &mdash; type a whole number, a fraction such as '
        + '<code>7/2</code>, or a decimal'));
    }

    workEl.innerHTML = [
      ttable('What you wrote, said four ways', rows),
      ttable('The two things the notation invites you to get wrong', [
        trow('a square bracket on infinity',
          'always wrong. <code>[3, inf]</code> claims infinity is a number in the set; it is not a number '
          + 'at all. The correct form is <code>[3, inf)</code>.'),
        trow('endpoints the wrong way round',
          'an interval is written low end first. <code>[5, 2]</code> describes the numbers that are at '
          + 'once at least 5 and at most 2, of which there are none.'),
        trow('a round bracket and a square one', 'perfectly normal. <code>[2, 5)</code> contains 2 and '
          + 'not 5, and that is exactly what "at least 2 and less than 5" says.')
      ])
    ].join('');
    kpi('iqKA', setText(set));
    kpi('iqKB', kind);
    kpi('iqKC', testR === null ? '--' : (setHas(set, testR) ? 'in' : 'out'));
    subEl.textContent = kind;

    var win = lineWindow(set, set.length ? [] : [interval.lo === null ? 0 : Rnum(interval.lo),
                                                interval.hi === null ? 0 : Rnum(interval.hi)]);
    drawSet(el('iqLine'), set, win, 'the set ' + setText(set) + ' on the number line');

    var msg;
    if (kind === 'endpoints the wrong way round') {
      msg = '<strong>' + written + ' contains no numbers.</strong> Read it as a sentence: "at least '
        + Rtext(interval.lo) + ' and at most ' + Rtext(interval.hi) + '". Nothing is both. Interval '
        + 'notation always names the smaller end first, and swapping them does not describe the numbers '
        + 'in between &mdash; it describes nothing.';
    } else if (empty) {
      msg = '<strong>' + written + ' is the empty set.</strong> The two ends are the same number and at '
        + 'least one of them is excluded, so there is no room left. Compare it with <code>['
        + Rtext(interval.lo) + ', ' + Rtext(interval.lo) + ']</code>, which contains exactly one number.';
    } else if (kind === 'a single point') {
      msg = '<strong>' + written + ' contains exactly one number.</strong> Both ends are closed and they '
        + 'are the same, so the set is { ' + Rtext(interval.lo) + ' }. Open either bracket and it becomes '
        + 'empty, which is the sharpest illustration of what those brackets do.';
    } else {
      msg = '<strong>' + written + ' is ' + kind + '.</strong> The same set is written <code>'
        + setIneq(set, V) + '</code> as an inequality and <code>' + setBuilder(set, V) + '</code> in '
        + 'set-builder notation. The filled and hollow ends on the line are the brackets: a filled end is '
        + 'a square bracket, a hollow one is round.';
    }
    if (notes.length) msg += ' ' + notes.join(' ');
    say(msg);
  };
"""


INEQ_JS += r"""
  /* ========================================================== quadratic ==
     A quadratic changes sign only where it is zero, so its roots cut the line
     into pieces and the whole expression keeps one sign on each piece. The lab
     therefore FINDS a sign for each piece by evaluating at a point inside it,
     rather than quoting a rule about parabolas.

     The roots may be irrational. An endpoint is carried as its exact text plus
     an exact comparison, so a rational test point can be PROVED to lie inside
     its interval; the float beside it decides where to look and where to draw,
     and never what the answer is. */
  function cmpToSurd(t, p, q, k) {
    /* compare the rational t with p + q*sqrt(k), exactly */
    if (k === 1n) return Rcmp(t, Radd(p, q));
    var L = Rsub(t, p), sL = Rsign(L), sq = Rsign(q);
    if (sq === 0) return sL;
    if (sq > 0) {
      if (sL <= 0) return -1;                     /* q*sqrt(k) > 0 >= L */
      return Rcmp(Rmul(L, L), Rmul(Rmul(q, q), R(k)));
    }
    if (sL >= 0) return 1;                        /* q*sqrt(k) < 0 <= L */
    return -Rcmp(Rmul(L, L), Rmul(Rmul(q, q), R(k)));
  }
  function critRational(r) {
    return {
      text: Rtext(r), num: Rnum(r), rational: r,
      cmp: function (t) { return Rcmp(t, r); }
    };
  }
  function surdText(p, q, k) {
    if (k === 1n) return Rtext(Radd(p, q));
    var mag = Requ(Rabs(q), R1) ? 'sqrt(' + k + ')' : Rterm(Rabs(q)) + 'sqrt(' + k + ')';
    if (Rzero(p)) return (Rsign(q) < 0 ? '-' : '') + mag;
    return Rtext(p) + (Rsign(q) < 0 ? ' - ' : ' + ') + mag;
  }
  function critSurd(p, q, k) {
    return {
      text: surdText(p, q, k), num: Rnum(p) + Rnum(q) * Math.sqrt(Number(k)), rational: null,
      cmp: function (t) { return cmpToSurd(t, p, q, k); }
    };
  }
  /* A rational strictly inside (lo, hi). The float midpoint says where to look;
     the candidate is then CHECKED against both endpoints exactly, and only a
     candidate that passes is used. */
  function testPointIn(lo, hi) {
    var cands = [], i;
    if (!lo && !hi) cands.push(R0);
    else if (!lo) cands.push(R(BigInt(Math.floor(hi.num) - 1)));
    else if (!hi) cands.push(R(BigInt(Math.ceil(lo.num) + 1)));
    else {
      var m = (lo.num + hi.num) / 2;
      [1n, 2n, 4n, 12n, 120n, 12000n].forEach(function (den) {
        cands.push(R(BigInt(Math.round(m * Number(den))), den));
      });
    }
    for (i = 0; i < cands.length; i += 1) {
      var t = cands[i];
      if ((!lo || lo.cmp(t) > 0) && (!hi || hi.cmp(t) < 0)) return t;
    }
    return null;
  }

  MODES.quadratic = function () {
    var L = sideOf(val('iqLhs'), V, 'left side'), Rs = sideOf(val('iqRhs'), V, 'right side');
    if (!L.ok) return trouble(L.msg);
    if (!Rs.ok) return trouble(Rs.msg);
    var op = readOp('iqOp');
    var typed = L.src + ' ' + relText(op) + ' ' + Rs.src;
    titleEl.innerHTML = typed;
    var D = Psub(L.poly, Rs.poly);
    if (Pdeg(D) > 2) {
      return trouble('after moving everything to one side this is degree ' + Pdeg(D)
        + '. The sign analysis below works at any degree, but finding the roots of a cubic needs the '
        + 'rational root theorem from course 4, so this mode stops at the quadratic.');
    }

    var svgLine = el('iqLine'), svgPlot = el('iqPlot');

    /* Not actually quadratic: say so and finish the job anyway. */
    if (Pdeg(D) <= 1) {
      var res = solveIneq(L.poly, Rs.poly, V, op);
      var holdsL = function (x) { return relHolds(Peval(L.poly, x), Peval(Rs.poly, x), op); };
      var probesL = probesAround(res.tr.kind === 'unique' ? [res.tr.value] : [R0]);
      var testL = agreeGrid('Testing values against the statement you typed', probesL, holdsL, res.set, V);
      workEl.innerHTML = [
        ttable('There is no ' + V + '^2 term here', [
          trow('moving everything to one side', '<code>' + Ptext(D, V) + ' ' + relText(op) + ' 0</code>'),
          trow('what that leaves', Pdeg(D) === 1
            ? 'a linear inequality, which has one boundary rather than two and cannot change sign twice'
            : 'a statement about numbers with no ' + V + ' in it at all')
        ]),
        ttable('Solved as a linear inequality',
          [trow('as typed', '<code>' + typed + '</code>')].concat(traceRows(res.tr, typed))),
        ttable('The answer', notationRows(res.set, V)),
        testL.html
      ].join('');
      kpi('iqKA', Ptext(D, V));
      kpi('iqKB', 'none &mdash; not quadratic');
      kpi('iqKC', setText(res.set));
      subEl.innerHTML = setText(res.set);
      drawSet(svgLine, res.set, lineWindow(res.set, [0]), 'the solution set: ' + setText(res.set));
      if (svgPlot) svgPlot.textContent = '';
      return say('<strong>This one is linear.</strong> The ' + V + '^2 terms cancelled when the sides '
        + 'were subtracted, so there is a single boundary and no sign table to build. The answer is '
        + setText(res.set) + '.');
    }

    var q = quadroots(D[2], D.length > 1 ? D[1] : R0, D.length > 0 ? D[0] : R0);
    var crits = [];
    if (q.kind === 'double') crits = [critRational(q.p)];
    else if (q.kind === 'rational') crits = q.roots.map(critRational);
    else if (q.kind === 'irrational') {
      crits = [critSurd(q.p, Rneg(q.s.q), q.s.k), critSurd(q.p, q.s.q, q.s.k)];
    }

    /* the pieces of the line: interval, root, interval, root, interval */
    var pieces = [], i;
    if (!crits.length) pieces.push({ kind: 'iv', lo: null, hi: null });
    else {
      pieces.push({ kind: 'iv', lo: null, hi: crits[0] });
      for (i = 0; i < crits.length; i += 1) {
        pieces.push({ kind: 'pt', crit: crits[i] });
        pieces.push({ kind: 'iv', lo: crits[i], hi: crits[i + 1] || null });
      }
    }
    pieces.forEach(function (pc) {
      if (pc.kind === 'iv') pc.t = testPointIn(pc.lo, pc.hi);
    });

    function signAt(poly, pc) {
      if (pc.kind === 'pt') {
        return pc.crit.rational !== null ? Rsign(Peval(poly, pc.crit.rational)) : 0;
      }
      return pc.t === null ? 0 : Rsign(Peval(poly, pc.t));
    }
    pieces.forEach(function (pc) {
      pc.sign = signAt(D, pc);
      pc.selected = relHolds(R(BigInt(pc.sign)), R0, op);
    });

    /* the factored form, searched for rather than looked up */
    var fac = Pfactor(D);
    var factorRows = [];
    fac.factors.forEach(function (item) {
      for (var m = 0; m < item.mult; m += 1) factorRows.push({ label: Pfactortext(item.poly, V), poly: item.poly });
    });
    if (fac.rest.length && fac.factors.length) {
      factorRows.push({ label: Pfactortext(fac.rest, V), poly: fac.rest });
    }
    if (!Requ(fac.content, R1) && factorRows.length) {
      factorRows.push({ label: 'the constant ' + Rtext(fac.content), poly: [fac.content] });
    }

    function headCell(pc) {
      return pc.kind === 'pt' ? V + ' = ' + pc.crit.text
        : '(' + (pc.lo ? pc.lo.text : '-inf') + ', ' + (pc.hi ? pc.hi.text : 'inf') + ')';
    }
    function signRow(label, values) {
      return '<tr><th class="rowhead">' + label + '</th>' + values.map(function (s) {
        return '<td class="' + (s > 0 ? 't' : (s < 0 ? 'f' : '')) + '">'
          + (s > 0 ? '+' : (s < 0 ? '-' : '0')) + '</td>';
      }).join('') + '</tr>';
    }
    function plainRow(label, values) {
      return '<tr><th class="rowhead">' + label + '</th>'
        + values.map(function (t) { return '<td style="text-align:left;">' + t + '</td>'; }).join('') + '</tr>';
    }

    var signRows = [
      plainRow('value tested there', pieces.map(function (pc) {
        return pc.kind === 'pt' ? 'the root itself'
          : (pc.t === null ? 'no rational point found' : '<code>' + V + ' = ' + Rtext(pc.t) + '</code>');
      }))
    ];
    factorRows.forEach(function (fr) {
      signRows.push(signRow(fr.label, pieces.map(function (pc) { return signAt(fr.poly, pc); })));
    });
    signRows.push(signRow('<strong>' + Ptext(D, V) + '</strong>', pieces.map(function (pc) { return pc.sign; })));
    signRows.push(plainRow('is it ' + relText(op) + ' 0?', pieces.map(function (pc) {
      return pc.selected ? YES : NO;
    })));

    /* merge the selected pieces back into intervals */
    var merged = [], cur = null;
    pieces.forEach(function (pc) {
      if (!pc.selected) { if (cur) { merged.push(cur); cur = null; } return; }
      if (!cur) {
        cur = pc.kind === 'pt'
          ? { lo: pc.crit, loC: true, hi: pc.crit, hiC: true }
          : { lo: pc.lo, loC: false, hi: pc.hi, hiC: false };
      } else if (pc.kind === 'pt') { cur.hi = pc.crit; cur.hiC = true; }
      else { cur.hi = pc.hi; cur.hiC = false; }
    });
    if (cur) merged.push(cur);

    function pieceText(i2) {
      if (i2.lo && i2.hi && i2.lo === i2.hi) return '{' + i2.lo.text + '}';
      return (i2.loC ? '[' : '(') + (i2.lo ? i2.lo.text : '-inf') + ', '
        + (i2.hi ? i2.hi.text : 'inf') + (i2.hiC ? ']' : ')');
    }
    function solutionText() {
      if (!merged.length) return '{ }';
      if (merged.length === 1 && !merged[0].lo && !merged[0].hi) return '(-inf, inf)';
      return merged.map(pieceText).join(' U ');
    }
    function solutionIneq() {
      if (!merged.length) return 'no ' + V + ' at all';
      return merged.map(function (i2) {
        if (i2.lo && i2.hi && i2.lo === i2.hi) return V + ' = ' + i2.lo.text;
        if (!i2.lo && !i2.hi) return 'every real ' + V;
        if (!i2.lo) return V + ' ' + relText(i2.hiC ? '<=' : '<') + ' ' + i2.hi.text;
        if (!i2.hi) return V + ' ' + relText(i2.loC ? '>=' : '>') + ' ' + i2.lo.text;
        return i2.lo.text + ' ' + relText(i2.loC ? '<=' : '<') + ' ' + V + ' '
          + relText(i2.hiC ? '<=' : '<') + ' ' + i2.hi.text;
      }).join('  or  ');
    }

    /* An independent check: every test point, put back into the statement as
       typed, must agree with the piece it sits in. */
    var checkRows = [];
    var disagree = false;
    pieces.forEach(function (pc) {
      if (pc.kind !== 'iv' || pc.t === null) return;
      var holdsHere = relHolds(Peval(L.poly, pc.t), Peval(Rs.poly, pc.t), op);
      if (holdsHere !== pc.selected) disagree = true;
      checkRows.push(tcells([
        '<code>' + V + ' = ' + Rtext(pc.t) + '</code>',
        Rtext(Peval(L.poly, pc.t)),
        Rtext(Peval(Rs.poly, pc.t)),
        holdsHere ? YES : NO,
        holdsHere === pc.selected ? chip('agree', 'ok') : chip('DISAGREE', 'no')
      ], holdsHere ? 'focus' : ''));
    });

    workEl.innerHTML = [
      ttable('Getting it into the form (expression) ' + relText(op) + ' 0', [
        trow('as typed', '<code>' + typed + '</code>'),
        trow('subtract the right side from both', '<code>' + Ptext(D, V) + ' ' + relText(op) + ' 0</code>'),
        trow('factored over the rationals', '<code>' + Pfactortextfull(D, V) + '</code>'
          + (fac.factors.length ? '' : '<br><span class="small-copy">the rational root search came back '
            + 'empty, so the roots are irrational and the sign table uses the quadratic itself</span>')),
        trow('where it is zero', crits.length
          ? crits.map(function (c) { return '<code>' + V + ' = ' + c.text + '</code>'; }).join(' and ')
          : 'nowhere: the discriminant is ' + Rtext(q.disc) + ', which is negative')
      ]),
      tgrid('The sign on each piece of the line', [''].concat(pieces.map(headCell)), signRows),
      ttable('The answer', [
        trow('as an inequality', '<code>' + solutionIneq() + '</code>'),
        trow('in interval notation', '<code>' + solutionText() + '</code>'),
        trow('how many pieces', merged.length === 0 ? 'none' : String(merged.length))
      ]),
      checkRows.length
        ? tgrid('Each test value, put back into the statement you typed',
            [V, 'left side', 'right side', 'holds?', ''], checkRows)
        : ''
    ].join('');

    kpi('iqKA', Pfactortextfull(D, V));
    kpi('iqKB', crits.length ? crits.map(function (c) { return c.text; }).join(', ') : 'none');
    kpi('iqKC', solutionText());
    subEl.innerHTML = solutionText();

    var nums = crits.map(function (c) { return c.num; });
    var lo = nums.length ? Math.min.apply(null, nums) : -3, hi = nums.length ? Math.max.apply(null, nums) : 3;
    var pad = Math.max(2, (hi - lo) * 0.8);
    var win = { lo: lo - pad, hi: hi + pad }, span = win.hi - win.lo;
    if (svgLine) {
      var line = NumberLine(svgLine, win.lo, win.hi);
      merged.forEach(function (i2) {
        if (i2.lo && i2.hi && i2.lo === i2.hi) { line.point(i2.lo.num, true); return; }
        line.interval(i2.lo ? i2.lo.num : win.lo - span, i2.hi ? i2.hi.num : win.hi + span, i2.loC, i2.hiC);
      });
      line.describe('the solution set ' + solutionText() + ' on the number line');
    }
    if (svgPlot) {
      var fD = polyFn(D), ylo = Infinity, yhi = -Infinity, j, xx;
      for (j = 0; j <= 80; j += 1) {
        xx = win.lo + span * j / 80;
        var yy = fD(xx);
        if (isFinite(yy)) { ylo = Math.min(ylo, yy); yhi = Math.max(yhi, yy); }
      }
      if (!isFinite(ylo)) { ylo = -5; yhi = 5; }
      var ypad = Math.max(1, (yhi - ylo) * 0.15);
      var plot = Plot(svgPlot, { xmin: win.lo, xmax: win.hi, ymin: ylo - ypad, ymax: yhi + ypad });
      plot.frame();
      plot.curve(fD, 'plot-curve');
      merged.forEach(function (i2) {
        plot.segment(i2.lo ? i2.lo.num : win.lo - span, 0,
                     i2.hi ? i2.hi.num : win.hi + span, 0, 'plot-interval');
      });
      crits.forEach(function (c) { plot.point(c.num, 0, 'plot-point root', c.text); });
      plot.describe('the graph of ' + Ptext(D, V) + ', with the solution set marked along the x-axis');
    }

    var above = op === '>' || op === '>=';
    var msg;
    if (!crits.length) {
      msg = '<strong>' + (merged.length ? 'Every real number satisfies it.' : 'No number satisfies it.')
        + '</strong> The discriminant is ' + Rtext(q.disc) + ', so ' + Ptext(D, V) + ' is never zero and '
        + 'never changes sign: it is ' + (Rsign(D[2]) > 0 ? 'positive' : 'negative') + ' everywhere, as '
        + 'the graph shows. A quadratic that misses the axis makes an inequality that is either always '
        + 'true or always false, and there is nothing in between to find.';
    } else if (q.kind === 'double') {
      msg = '<strong>' + solutionText() + '.</strong> There is one root, ' + crits[0].text
        + ', where the parabola touches the axis without crossing, so the expression has the SAME sign on '
        + 'both sides of it. That is what makes this case catch people: '
        + (merged.length === 2
          ? 'the answer is the whole line with a single point cut out of it, and it has to be written as '
            + 'two pieces even though the graph looks like one.'
          : (merged.length === 1 && ivPointLike(merged[0])
            ? 'the only value that qualifies is the root itself.'
            : 'the sign never changes, so the answer is everything or nothing except at the root.'));
    } else {
      msg = '<strong>' + solutionText() + '.</strong> The two roots cut the line into three pieces and '
        + 'the sign table above was filled in by evaluating at one exact value inside each. '
        + (above
          ? 'Greater-than picks out the two OUTER pieces, and they have to be joined with "or" &mdash; '
            + 'they are not one interval and cannot be written as a chain.'
          : 'Less-than picks out the single piece BETWEEN the roots, which is why this case is one '
            + 'interval and can be written as a chain.')
        + (q.kind === 'irrational'
          ? ' The roots here are irrational: ' + crits[0].text + ' and ' + crits[1].text
            + ' are the exact endpoints, and ' + crits[0].num.toFixed(4) + ' and ' + crits[1].num.toFixed(4)
            + ' are roundings of them used only to place the marks on the picture.'
          : '');
    }
    if (crits.length === 2 && above) {
      msg += ' This is the shape the usual shortcut gets wrong: taking a square root and keeping one '
        + 'sign turns ' + V + '^2 &gt; 4 into ' + V + ' &gt; 2 and quietly loses half the answer, and '
        + 'dividing both sides by ' + V + ' is worse, because ' + V + ' may be negative and the division '
        + 'would then have to reverse the statement. The sign table needs neither move.';
    }
    if (disagree) {
      msg += ' <strong>Warning: a test value disagrees with the sign table.</strong>';
    }
    say(msg);
  };
  function ivPointLike(i2) { return i2.lo && i2.hi && i2.lo === i2.hi; }

  /* ----------------------------------------------------------- wiring up */
  function redraw() {
    var fn = MODES[MODE];
    if (!fn) return trouble('this lab has no mode named ' + MODE + '.');
    try {
      fn();
    } catch (err) {
      trouble('that combination could not be worked out (' + (err && err.message ? err.message : err)
        + '). Try one of the presets and change it a little at a time.');
    }
  }
  var presetEl = el('iqPreset');
  function applyPreset() {
    if (!presetEl) return;
    var parts = String(presetEl.value).split('|');
    FIELDS.forEach(function (id, i) {
      var e = el(id);
      if (e && parts[i] !== undefined) e.value = parts[i];
    });
  }
  if (presetEl) presetEl.addEventListener('change', function () { applyPreset(); redraw(); });
  FIELDS.forEach(function (id) {
    var e = el(id);
    if (!e) return;
    e.addEventListener('input', redraw);
    e.addEventListener('change', redraw);
  });
  applyPreset();
  redraw();
  window.redrawLab = redraw;
"""


def _op_options(selected):
    return "".join(
        '<option value="%s"%s>%s</option>' % (v, " selected" if v == selected else "", label)
        for v, label in INEQ_OPS
    )


def _choice_field(select_id, label, options):
    return (
        '        <div class="field">\n'
        '          <label for="%s">%s</label>\n'
        '          <select id="%s">%s</select>\n'
        "        </div>\n" % (select_id, label, select_id, options)
    )


def _ineq_controls(mode, options, first):
    out = [_preset_field("iqPreset", "Statement", options)]
    if mode == "linear" or mode == "quadratic":
        out.append(_field("iqLhs", "Left side", first[0]))
        out.append(_choice_field("iqOp", "Relation", _op_options(first[1])))
        out.append(_field("iqRhs", "Right side", first[2]))
    elif mode == "compound":
        out.append(_field("iqLhs", "First: left side", first[0]))
        out.append(_choice_field("iqOp", "First: relation", _op_options(first[1])))
        out.append(_field("iqRhs", "First: right side", first[2]))
        out.append(_choice_field(
            "iqConn", "Joined by",
            '<option value="and"%s>and</option><option value="or"%s>or</option>'
            % (" selected" if first[3] == "and" else "", " selected" if first[3] == "or" else "")))
        out.append(_field("iqLhs2", "Second: left side", first[4]))
        out.append(_choice_field("iqOp2", "Second: relation", _op_options(first[5])))
        out.append(_field("iqRhs2", "Second: right side", first[6]))
    elif mode == "absolute":
        out.append(_field("iqIns", "Inside the bars", first[0]))
        out.append(_choice_field("iqOp", "Relation", _op_options(first[1])))
        out.append(_field("iqRhs", "Right side", first[2]))
    elif mode == "notation":
        out.append(_field("iqLo", "Left endpoint (or -inf)", first[0]))
        out.append(_choice_field(
            "iqLoB", "Left bracket",
            '<option value="c"%s>[  included</option><option value="o"%s>(  excluded</option>'
            % (" selected" if first[1] == "c" else "", " selected" if first[1] == "o" else "")))
        out.append(_field("iqHi", "Right endpoint (or inf)", first[2]))
        out.append(_choice_field(
            "iqHiB", "Right bracket",
            '<option value="c"%s>]  included</option><option value="o"%s>)  excluded</option>'
            % (" selected" if first[3] == "c" else "", " selected" if first[3] == "o" else "")))
        out.append(_field("iqTest", "Is this number in it?", first[4]))
    out.append(_kpis(INEQ_KPIS[mode]))
    out.append('        <p class="small-copy" style="margin:0;">%s</p>\n' % INEQ_HINTS[mode])
    return "".join(out)


def _ineq_markup(mode):
    stages = []
    if mode == "compound":
        stages.append('      <p class="small-copy" style="margin:10px 0 4px;">the first statement</p>\n'
                      '      <div class="lab-stage"><svg id="iqLineA"></svg></div>\n')
        stages.append('      <p class="small-copy" style="margin:10px 0 4px;">the second statement</p>\n'
                      '      <div class="lab-stage"><svg id="iqLineB"></svg></div>\n')
        stages.append('      <p class="small-copy" style="margin:10px 0 4px;">the two of them together</p>\n'
                      '      <div class="lab-stage"><svg id="iqLine"></svg></div>\n')
    else:
        if mode in ("absolute", "quadratic"):
            stages.append('      <div class="lab-stage"><svg id="iqPlot"></svg></div>\n')
        stages.append('      <div class="lab-stage"><svg id="iqLine"></svg></div>\n')
    return (
        '      <div class="lab-toolbar">\n'
        '        <div class="lab-title"><strong id="iqTitle">a statement to solve</strong>'
        '<span id="iqSub"></span></div>\n'
        "        %s\n"
        "      </div>\n"
        "%s"
        '      <div id="iqWork" style="margin-top:12px;"></div>\n'
        '      <div class="status-banner" id="iqStatus" style="margin-top:12px;"></div>'
        % (INEQ_LEGEND, "".join(stages))
    )


def inequality_lab(cfg):
    """An inequality, solved and DRAWN, with the answer treated as a set.

    The teaching decision: the four representations of a solution -- the
    inequality, the interval, the set-builder form and the number line -- are
    all generated from one interval structure with exact endpoints, so they
    cannot disagree with one another on the page. Intersection and union are
    computed, which is what lets `and` and `or` be shown rather than asserted,
    and what makes the empty set and the whole line ordinary answers instead of
    special cases.

    The reversal on multiplying by a negative is a row in the trace with its
    reason attached, because it is the one rule on this course a reader will
    otherwise recall backwards. Every mode then tests exact sample values
    against the statement as typed and compares the verdict with membership of
    the computed set: a reversed sign makes every row disagree, which is the
    only symptom that is impossible to miss.
    """
    mode = cfg.get("mode", "linear")
    if mode not in INEQ_PRESETS:
        mode = "linear"
    presets = cfg.get("presets") or INEQ_PRESETS[mode]
    fields = INEQ_FIELDS[mode]
    title, subtitle = INEQ_TITLES[mode]

    options = "".join(
        '<option value="%s">%s</option>' % ("|".join(rest), label)
        for label, *rest in presets
    )
    first = list(presets[0][1:])

    markup = _ineq_markup(mode)
    controls = _ineq_controls(mode, options, first)
    script = (
        RATIONAL_JS + POLY_JS + EXPR_JS + SURD_JS + PLOT_JS + FORM_JS + SET_JS
        + _own_ids(markup, controls)
        + "\n  var MODE = '%s';\n" % mode
        + "  var FIELDS = [%s];\n" % ", ".join("'%s'" % f for f in fields)
        + INEQ_JS
    )

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a statement, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "The solution set is computed from what these boxes hold, then drawn on the line and "
            "written out in both notations. Every endpoint on the picture is the exact number printed "
            "beside it.",
        ),
        script=script,
    )
