"""Course 7: polynomial arithmetic, and factoring as a search.

Two labs live here, and both were built around the same complaint about how
this material is usually taught: the reader is shown a finished manipulation
and asked to believe it. "Multiply these out" arrives as an answer with the
work erased, "factor this" arrives as a pair of brackets that someone already
knew, and the method that produced them is never visible. So:

  polynomial_lab  every product is shown TERM BY TERM in a grid before it is
                  collected, every long division prints the remainder before
                  and after each subtraction, and the synthetic-division mode
                  computes f(c) a second and independent way so the remainder
                  theorem is CHECKED on the reader's own polynomial rather than
                  quoted at them. Where two routes to the same number exist --
                  the identity and the honest expansion, the trace and the
                  library's own divmod -- the lab runs both and prints whether
                  they agreed. Agreement between separate computations is the
                  evidence; one number on its own is an assertion.

  factoring_lab   factoring is a SEARCH, and the search is the lesson. The ac
                  mode lists every pair of integers it tried, with the product
                  and the sum, and marks the one that worked -- or comes back
                  with nothing, which is what happens on a trinomial that does
                  not factor. The rational-root mode GENERATES its candidate
                  list from the divisors of the constant and leading
                  coefficients and then TESTS every candidate, so a reader who
                  runs it on x^3 - 2 watches four candidates fail and the list
                  run out. Every mode ends by multiplying its own factored form
                  back out and comparing it with what it started from.

Both obey the two rules the footer of every page on this path states. Nothing
is precomputed: no answer appears in this file as a literal, and every number
on the page comes out of the reader's own input in the browser. Everything is
exact: coefficients, steps, products, quotients, remainders and roots are
rationals over BigInt from first keystroke to final bracket. Floating point
appears only in the pictures, where a pixel is a pixel, and in the one place a
lesson explicitly asks for a decimal -- and it says so there.
"""

from .algebra_core import EXPR_JS, PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# --------------------------------------------------------------- shared JS

# Presentation and small algebra shared by the two labs below. It is a Python
# string rather than a function in algebra_core.py because algebra_core.py is
# the toolkit every algebra lab shares and this is only what these two need.
SHARED_JS = r"""
  /* ---- markup helpers ---- */
  /* Reader input is echoed back on every one of these panels, so it is escaped
     on the way in. A lesson about x^2 must survive a reader typing "<". */
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function cell(text, cls) { return '<td' + (cls ? ' class="' + cls + '"' : '') + '>' + text + '</td>'; }
  function rowOf(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.join('') + '</tr>'; }
  /* The "label: detail" row that carries most of what these labs say. */
  function say(label, detail, cls) {
    return '<tr' + (cls ? ' class="' + cls + '"' : '') + '><th class="rowhead">' + label
      + '</th><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function table(caption, heads, rows) {
    var thead = (heads && heads.length)
      ? '<thead>' + rowOf(heads.map(function (h) { return '<th>' + h + '</th>'; })) + '</thead>'
      : '';
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption>'
      + thead + '<tbody>' + rows.join('') + '</tbody></table></div>';
  }
  function chip(ok, text) { return '<span class="chip ' + (ok ? 'ok' : 'no') + '">' + text + '</span>'; }
  function chipHi(text) { return '<span class="chip hi">' + text + '</span>'; }
  function muted(text) { return '<span class="tone-muted">' + text + '</span>'; }
  /* What is in a box, echoed back safely -- and named as empty when it is. */
  function shownInput(el) {
    var v = el ? String(el.value || '').trim() : '';
    return v ? '<code>' + esc(v) + '</code>' : muted('nothing yet');
  }

  /* ---- polynomials, presented ---- */
  /* The single term c*x^e as a reader writes it. Ptext does the deciding, so
     "1x^2" and "+ -3x" cannot be produced here either. */
  function Pmono(c, e) {
    var arr = [];
    for (var i = 0; i < e; i += 1) arr.push(R0);
    arr.push(c);
    return Ptext(arr);
  }
  /* Non-zero terms, highest power first -- the order the reader writes in. */
  function Pterms(p) {
    var out = [];
    for (var i = p.length - 1; i >= 0; i -= 1) if (!Rzero(p[i])) out.push({ c: p[i], e: i });
    return out;
  }
  function Psame(a, b) { return Pzero(Psub(a, b)); }
  /* A list of {c, e} terms written as one expression, with the signs joined the
     way a reader writes them rather than as "+ -3x". Splitting a middle term
     into "+ -4x" on a page that is teaching sign discipline is not acceptable. */
  function joinTerms(list) {
    var out = '';
    list.forEach(function (t) {
      var neg = Rsign(t.c) < 0, mag = Pmono(Rabs(t.c), t.e);
      out += (out === '') ? (neg ? '-' + mag : mag) : (neg ? ' - ' + mag : ' + ' + mag);
    });
    return out === '' ? '0' : out;
  }
  /* A whole number inside a product or a sum: negatives get brackets, so the
     line reads (-6) * (-1) = 6 rather than -6 * -1 = 6. */
  function intTerm(v) { return v < 0n ? '(' + v + ')' : String(v); }
  /* The zero polynomial has no degree. Saying "degree 0" for it would make the
     next lesson -- deg(fg) = deg f + deg g -- false. */
  function Pdegtext(p) { return Pzero(p) ? 'none (the zero polynomial has no degree)' : String(Pdeg(p)); }
  function degName(d) {
    var names = ['constant', 'linear', 'quadratic', 'cubic', 'quartic', 'quintic'];
    return d >= 0 && d < names.length ? names[d] : 'degree ' + d;
  }
  function termName(n) {
    return n === 1 ? 'monomial' : (n === 2 ? 'binomial' : (n === 3 ? 'trinomial' : n + ' terms'));
  }
  /* The monomial common factor of a polynomial: the rational content (with the
     sign that makes the leading coefficient positive, which is where "factor
     out the minus" comes from) times the lowest power of x that appears. */
  function monoGcf(p) {
    var prim = Pprimitive(p);
    var q = prim.poly, e = 0;
    while (e < q.length && Rzero(q[e])) e += 1;
    return { c: prim.content, e: e, rest: q.slice(e) };
  }
  function gcfText(g) {
    if (g.e === 0) return Rtext(g.c);
    return Requ(g.c, R1) ? Pmono(R1, g.e) : Pmono(g.c, g.e);
  }

  /* Integer cube root, for the sum and difference of cubes. Newton on BigInt,
     then a neighbourhood check, because integer Newton can land one short and
     "8 is not a perfect cube" would be a lie told confidently. */
  function bicbrt(n) {
    if (n < 0n) { var neg = bicbrt(-n); return neg === null ? null : -neg; }
    if (n < 2n) return n;
    var x = n, y = (2n * x + n / (x * x)) / 3n;
    while (y < x) { x = y; y = (2n * x + n / (x * x)) / 3n; }
    for (var t = (x > 1n ? x - 1n : 0n); t <= x + 1n; t += 1n) if (t * t * t === n) return t;
    return null;
  }
  function Rcbrt(a) {
    var p = bicbrt(a.n), q = bicbrt(a.d);
    return (p === null || q === null) ? null : R(p, q);
  }

  /* ---- reading what the reader typed ---- */
  /* Three outcomes, and the middle one is lesson material rather than an
     error: it parsed, it is a perfectly good function, it is not a POLYNOMIAL.
     This walk finds the reason, which is the thing worth telling a reader. */
  function whyNotPoly(node) {
    switch (node.k) {
      case 'num': return null;
      case 'var':
        return node.v === 'x' ? null
          : 'the letter "' + esc(node.v) + '" is a second variable, and these labs work in x alone';
      case 'neg': return whyNotPoly(node.a);
      case 'add': case 'sub': case 'mul':
        return whyNotPoly(node.a) || whyNotPoly(node.b);
      case 'div': {
        var den = Epoly(node.b, 'x');
        if (den === null) return whyNotPoly(node.b) || 'the denominator is not a polynomial';
        if (Pzero(den)) return 'it divides by zero';
        if (Pdeg(den) > 0)
          return 'it divides by ' + Ptext(den) + ', and a variable in a denominator is a negative '
            + 'power of x -- a polynomial has whole-number powers only';
        return whyNotPoly(node.a);
      }
      case 'pow': {
        var ex = Epoly(node.b, 'x');
        if (ex === null || Pdeg(ex) > 0) return 'the exponent contains x, and a polynomial has constant exponents';
        var e = ex.length ? ex[0] : R0;
        if (!Rint(e)) return 'the exponent ' + Rtext(e) + ' is not a whole number, so that term is a root rather than a power';
        if (e.n < 0n) return 'the exponent ' + Rtext(e) + ' is negative, which puts x in a denominator';
        if (e.n > 64n) return 'the exponent ' + Rtext(e) + ' is larger than this lab will work with';
        return whyNotPoly(node.a);
      }
      case 'fn':
        return esc(node.v) + '(...) is not a polynomial operation: a polynomial is built from +, -, '
          + 'x and whole-number powers, and nothing else';
    }
    return 'it is not built from +, -, x and whole-number powers';
  }
  /* { ok, poly } on success; { ok:false, why, tree } otherwise, where `why` is
     a sentence the status banner can print as it stands. */
  function readPoly(el, name) {
    if (!el) return { ok: false, why: name + ' has no input box in this mode', tree: null };
    var src = String(el.value || '').trim();
    if (!src) return { ok: false, src: src, tree: null, why: name + ' is empty. Type something like <code>2x^2 - 3x + 1</code>.' };
    var tree;
    try {
      tree = Eparse(src);
    } catch (err) {
      return { ok: false, src: src, tree: null,
               why: name + ' does not parse: ' + esc(err && err.message ? err.message : String(err))
                    + '. Powers are written <code>x^2</code>, and multiplication may be left out: '
                    + '<code>2x</code>, <code>3(x + 1)</code>.' };
    }
    var poly = Epoly(tree, 'x');
    if (poly === null) {
      return { ok: false, src: src, tree: tree, notPoly: true,
               why: name + ' parses, but it is not a polynomial in x: ' + whyNotPoly(tree) + '.' };
    }
    return { ok: true, src: src, tree: tree, poly: poly };
  }
  function readNumber(el, name) {
    if (!el) return { ok: false, why: name + ' has no input box in this mode' };
    var src = String(el.value || '').trim();
    if (!src) return { ok: false, why: name + ' is empty. Type a whole number or a fraction such as <code>-3/2</code>.' };
    var v;
    try {
      v = Rparse(src);
    } catch (err) {
      /* "1/0" parses as a fraction and then fails to BE one. */
      return { ok: false, src: src,
               why: '<code>' + esc(src) + '</code> is not a number: ' + esc(err && err.message ? err.message : String(err))
                 + '. A fraction needs a denominator that is not zero.' };
    }
    if (v === null) return { ok: false, src: src,
      why: '<code>' + esc(src) + '</code> is not a whole number or a fraction. Try <code>3</code>, '
        + '<code>-2</code> or <code>1/2</code>.' };
    return { ok: true, value: v, src: src };
  }

  /* ---- pictures ---- */
  /* A polynomial as a plain JavaScript function, for drawing only. This is the
     one place these labs leave the exact world, and it changes no number the
     page reports: the curve is scenery for the arithmetic above it. */
  function Pfn(p) {
    var cs = p.map(Rnum);
    return function (x) {
      var acc = 0;
      for (var i = cs.length - 1; i >= 0; i -= 1) acc = acc * x + cs[i];
      return acc;
    };
  }
  /* A viewing window wide enough for the x values worth seeing and tall enough
     for the middle of what the curves actually do. The 5th/95th percentile
     clamp is a DRAWING decision -- a quartic leaves the panel in three pixels
     otherwise -- and it is why the axis labels, not the shape, are what a
     reader should measure against. */
  function viewFor(fns, xs) {
    var lo = -4, hi = 4, i;
    var pts = xs.filter(function (v) { return isFinite(v) && Math.abs(v) < 1e6; });
    if (pts.length) {
      lo = Math.min.apply(null, pts); hi = Math.max.apply(null, pts);
      var pad = Math.max(1.2, (hi - lo) * 0.35);
      lo -= pad; hi += pad;
    }
    if (!(hi - lo > 0.8)) { lo -= 2; hi += 2; }
    var vals = [];
    for (i = 0; i <= 160; i += 1) {
      var x = lo + (hi - lo) * i / 160;
      fns.forEach(function (f) { var y = f(x); if (typeof y === 'number' && isFinite(y)) vals.push(y); });
    }
    if (!vals.length) return { xmin: lo, xmax: hi, ymin: -5, ymax: 5 };
    vals.sort(function (a, b) { return a - b; });
    var ylo = vals[Math.floor((vals.length - 1) * 0.05)], yhi = vals[Math.floor((vals.length - 1) * 0.95)];
    if (!(yhi - ylo > 1e-9)) { ylo -= 2; yhi += 2; }
    var vpad = (yhi - ylo) * 0.2 + 0.5;
    ylo -= vpad; yhi += vpad;
    if (ylo > 0) ylo = -vpad;            /* the x-axis carries the roots: keep it */
    if (yhi < 0) yhi = vpad;
    return { xmin: lo, xmax: hi, ymin: ylo, ymax: yhi };
  }
"""


# ================================================================ lab one:
#                                                       polynomial arithmetic

# Each preset is (label, main, second, pattern). `second` is the second
# polynomial in the modes that take two, the number c in the modes that take a
# number, and the empty string where the mode has no second field; `pattern`
# is only read by the special-products mode. Presets are per mode because a
# lesson on long division must not be handed a quadratic with no linear term,
# and because the case that BREAKS the method is the one worth clicking.
POLY_PRESETS = {
    "form": [
        ("3x^2 - 5x + 2", "3x^2 - 5x + 2", "2", ""),
        ("x^4 - 3x^2 + x   (missing powers)", "x^4 - 3x^2 + x", "-1", ""),
        ("(1/2)x^3 - x + 3/4   (exact fractions)", "(1/2)x^3 - x + 3/4", "1/2", ""),
        ("2x^2 - 3x^2 + x + 4   (like terms collapse)", "2x^2 - 3x^2 + x + 4", "3", ""),
        ("5/x + 2   (not a polynomial)", "5/x + 2", "2", ""),
        ("x^2 + sqrt(x)   (not a polynomial)", "x^2 + sqrt(x)", "4", ""),
    ],
    "arith": [
        ("(3x^2 + 2x - 5) and (x^2 - 4x + 1)", "3x^2 + 2x - 5", "x^2 - 4x + 1", ""),
        ("different degrees", "x^3 - 2x + 7", "2x^2 + 5", ""),
        ("the leading terms cancel", "x^2 + 3x", "-x^2 + 2", ""),
        ("exact fractions", "(1/2)x^2 - (1/3)x", "(1/4)x^2 + (2/3)x", ""),
        ("P - Q is the zero polynomial", "4x^2 - x + 6", "4x^2 - x + 6", ""),
        ("the subtraction sign trap", "x^3 + x^2", "x^3 - x^2", ""),
    ],
    "multiply": [
        ("(x + 3)(x - 5)", "x + 3", "x - 5", ""),
        ("(2x - 1)(3x^2 + x - 4)", "2x - 1", "3x^2 + x - 4", ""),
        ("(x - 1)(x^2 + x + 1)   (terms cancel)", "x - 1", "x^2 + x + 1", ""),
        ("(x + 2)(x + 2)   (a square)", "x + 2", "x + 2", ""),
        ("fractions", "(1/2)x + 3", "4x - 2/3", ""),
        ("(x^2 + 1)(x^2 - 1)", "x^2 + 1", "x^2 - 1", ""),
    ],
    "special": [
        ("(x + 3)^2", "x", "3", "sqsum"),
        ("(2x + 5)^2   (the middle term)", "2x", "5", "sqsum"),
        ("(3x - 1)^2", "3x", "1", "sqdiff"),
        ("(x + 4)(x - 4)", "x", "4", "conj"),
        ("(2x + 3/2)(2x - 3/2)", "2x", "3/2", "conj"),
        ("(x + 2)^3", "x", "2", "cubesum"),
    ],
    "divide": [
        ("(x^2 + 5x + 6) / (x + 2)   (exact)", "x^2 + 5x + 6", "x + 2", ""),
        ("(2x^3 - 3x^2 + 4x - 5) / (x - 2)", "2x^3 - 3x^2 + 4x - 5", "x - 2", ""),
        ("(x^3 - 1) / (x - 1)   (missing powers)", "x^3 - 1", "x - 1", ""),
        ("(x^4 + 2x^2 - 3) / (x^2 - 1)", "x^4 + 2x^2 - 3", "x^2 - 1", ""),
        ("(3x^2 + 2) / (x^3 - 1)   (degree too low)", "3x^2 + 2", "x^3 - 1", ""),
        ("(2x^2 - x + 4) / (2x - 1)   (non-monic divisor)", "2x^2 - x + 4", "2x - 1", ""),
    ],
    "synthetic": [
        ("x^3 - 4x^2 + x + 6, c = 3", "x^3 - 4x^2 + x + 6", "3", ""),
        ("2x^3 + x^2 - 5, c = 2", "2x^3 + x^2 - 5", "2", ""),
        ("x^4 - 16, c = -2   (divisor x + 2)", "x^4 - 16", "-2", ""),
        ("2x^2 - 3x + 1, c = 1/2   (a fraction)", "2x^2 - 3x + 1", "1/2", ""),
        ("x^3 + 2x^2 - 5x - 6, c = 4", "x^3 + 2x^2 - 5x - 6", "4", ""),
        ("x^5 - 1, c = 1", "x^5 - 1", "1", ""),
    ],
}

POLY_TITLES = {
    "form": ("What a polynomial is", "Degree, terms, and the two things that disqualify an expression"),
    "arith": ("Adding and subtracting", "Like terms, lined up by power"),
    "multiply": ("Multiplying", "Every term against every term, then collected"),
    "special": ("The special products", "An identity and an honest expansion, computed separately"),
    "divide": ("Long division", "The remainder before and after every subtraction"),
    "synthetic": ("Synthetic division", "The short table, and the remainder theorem checked"),
}

# The KPI strip is four cells wide in every mode; only the labels change, so
# the ids a mode reads always exist.
POLY_KPIS = {
    "form": ["Degree", "Leading coefficient", "Constant term", "Value at your x"],
    "arith": ["deg P", "deg Q", "deg (P + Q)", "deg (P - Q)"],
    "multiply": ["deg P", "deg Q", "deg PQ", "Products in the grid"],
    "special": ["Pattern", "Expanded", "Wrong by", "Identity checks out"],
    "divide": ["Quotient", "Remainder", "deg r &lt; deg d", "Divides exactly"],
    "synthetic": ["c", "Remainder", "f(c)", "Remainder = f(c)"],
}

POLY_LEGENDS = {
    "form": '<span class="tone-cyan"><i class="legend-swatch"></i>the function you typed</span>',
    "arith": '<span class="tone-purple"><i class="legend-swatch"></i>P</span>'
             '<span class="tone-muted"><i class="legend-swatch"></i>Q</span>'
             '<span class="tone-cyan"><i class="legend-swatch"></i>P + Q</span>',
    "multiply": '<span class="tone-purple"><i class="legend-swatch"></i>P</span>'
                '<span class="tone-muted"><i class="legend-swatch"></i>Q</span>'
                '<span class="tone-cyan"><i class="legend-swatch"></i>PQ</span>'
                '<span class="tone-green"><i class="legend-swatch"></i>roots of the product</span>',
    "special": '<span class="tone-cyan"><i class="legend-swatch"></i>the expansion</span>'
               '<span class="tone-red"><i class="legend-swatch"></i>the common wrong answer</span>',
    "divide": '<span class="tone-cyan"><i class="legend-swatch"></i>f</span>'
              '<span class="tone-purple"><i class="legend-swatch"></i>d &middot; q</span>'
              '<span class="tone-muted"><i class="legend-swatch"></i>r</span>',
    "synthetic": '<span class="tone-cyan"><i class="legend-swatch"></i>f</span>'
                 '<span class="tone-green"><i class="legend-swatch"></i>(c, f(c)) &mdash; the remainder</span>',
}

# label for the main box, label for the second box ('' = the mode has none)
POLY_FIELDS = {
    "form": ("The expression", "Evaluate at x ="),
    "arith": ("P", "Q"),
    "multiply": ("P", "Q"),
    "special": ("A", "B"),
    "divide": ("f, the dividend", "d, the divisor"),
    "synthetic": ("f", "c   (dividing by x - c)"),
}

# Which second field a mode declares: a polynomial box, a number box, or none.
POLY_SECOND_KIND = {
    "form": "number", "arith": "poly", "multiply": "poly",
    "special": "poly", "divide": "poly", "synthetic": "number",
}


# The side panel's opening line, per mode. It says what the reader is meant to
# do with the controls, which is a different job from the lab's subtitle.
POLY_PANEL_INTRO = {
    "form": "Type any expression. The lab decides whether it is a polynomial, says which rule it "
            "breaks when it is not, and draws it either way &mdash; a function that fails the "
            "definition is still a function.",
    "arith": "Two polynomials, added and subtracted with the like terms lined up in columns. Watch "
             "the third preset: the degree of a sum can be lower than the degree of either part.",
    "multiply": "Every term of P is multiplied by every term of Q and the products are shown before "
                "they are collected. The collected answer is then checked against a separate "
                "multiplication routine.",
    "special": "Choose a pattern and the two pieces A and B. The lab computes the answer twice &mdash; "
               "once from the identity, once by multiplying the brackets out &mdash; and prints the "
               "common wrong answer with the exact amount it is wrong by.",
    "divide": "The trace shows what is left to divide at every step, the quotient term it produced, "
              "and what remains after subtracting. The fifth preset stops before it starts.",
    "synthetic": "The short table, plus f(c) evaluated separately so the remainder theorem is checked "
                 "on your polynomial. A remainder of zero is a factor, and the graph shows why.",
}

POLY_PATTERN_OPTIONS = [
    ("sqsum", "(A + B)^2"),
    ("sqdiff", "(A - B)^2"),
    ("conj", "(A + B)(A - B)"),
    ("cubesum", "(A + B)^3"),
    ("cubediff", "(A - B)^3"),
]


def polynomial_lab(cfg):
    """Polynomial arithmetic, with the work left in.

    The teaching decision: every one of these six modes shows the STEP that the
    printed answer came out of, and then checks that step against a second,
    independent computation.

      form       decides whether what the reader typed is a polynomial at all,
                 and when it is not, says which rule it broke -- then draws it
                 anyway, because 5/x + 2 is a perfectly good function and the
                 disqualifying feature is visible in the picture.
      arith      lines the two polynomials up by power in a grid of columns,
                 because "combine like terms" is a statement about columns.
      multiply   prints every term-by-term product in a grid BEFORE collecting
                 them, and then compares the collected result against the
                 library's own multiplication routine.
      special    computes each identity twice: once as the identity claims, and
                 once by honestly multiplying the brackets out. It also prints
                 the common wrong answer and the exact amount it is wrong by.
      divide     prints the remainder before and after every subtraction, and
                 then checks d*q + r = f on the reader's own polynomials.
      synthetic  runs the short table and evaluates f(c) SEPARATELY, so the
                 remainder theorem is verified on this polynomial rather than
                 asserted at the reader.

    Nothing below is stored: change a character in either box and every number
    on the panel is recomputed from the definition, exactly.
    """
    mode = cfg.get("mode", "form")
    if mode not in POLY_PRESETS:
        mode = "form"
    presets = cfg.get("presets") or POLY_PRESETS[mode]
    title, subtitle = POLY_TITLES[mode]
    main_label, second_label = POLY_FIELDS[mode]
    second_kind = POLY_SECOND_KIND[mode]
    first = presets[0]

    options = "".join(
        '<option value="%s|%s|%s">%s</option>' % (main, second, pattern, label)
        for label, main, second, pattern in presets
    )
    kpi_cells = "".join(
        '<div class="kpi"><span>%s</span><strong id="pnK%d">&mdash;</strong></div>' % (label, i + 1)
        for i, label in enumerate(POLY_KPIS[mode])
    )
    pattern_field = ""
    if mode == "special":
        pattern_field = (
            '        <div class="field">\n'
            '          <label for="pnPattern">Pattern</label>\n'
            '          <select id="pnPattern">%s</select>\n'
            "        </div>\n"
            % "".join('<option value="%s"%s>%s</option>'
                      % (key, ' selected' if key == first[3] else "", label)
                      for key, label in POLY_PATTERN_OPTIONS)
        )
    second_field = ""
    if second_kind != "none":
        second_field = (
            '        <div class="field">\n'
            '          <label for="pnSecond">%s</label>\n'
            '          <input id="pnSecond" type="text" value="%s" inputmode="text" autocomplete="off">\n'
            "        </div>\n" % (second_label, first[2])
        )

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="pnTitle">%s</strong><span id="pnSub"></span></div>
        <div class="inline-legend">%s</div>
      </div>
      <div class="lab-stage"><svg id="pnPlot"></svg></div>
      <div id="pnWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="pnStatus" style="margin-top:12px;"></div>""" % (
        title, POLY_LEGENDS[mode],
    )

    controls = """        <div class="field">
          <label for="pnPreset">Example</label>
          <select id="pnPreset">%s</select>
        </div>
%s        <div class="field">
          <label for="pnMain">%s</label>
          <input id="pnMain" type="text" value="%s" inputmode="text" autocomplete="off">
        </div>
%s        <div class="kpi-grid">%s</div>
        <p class="small-copy" style="margin:0;">Type as you would write it: <code>2x</code>, <code>3(x + 1)</code>,
        <code>x^2</code>, <code>(1/2)x - 3/4</code>. Every coefficient stays an exact fraction, and every
        number below is recomputed in your browser from what is in these boxes.</p>""" % (
        options, pattern_field, main_label, first[1], second_field, kpi_cells,
    )

    second_lookup = ("document.getElementById('pnSecond')"
                     if second_kind != "none" else "null")
    pattern_lookup = ("document.getElementById('pnPattern')"
                      if mode == "special" else "null")

    script = RATIONAL_JS + POLY_JS + EXPR_JS + SURD_JS + PLOT_JS + SHARED_JS + r"""
  var MODE = '""" + mode + r"""';
  var preset = document.getElementById('pnPreset');
  var inMain = document.getElementById('pnMain');
  /* These two are looked up only in the modes whose controls declare them. An
     id that is not on the page is not asked for: getElementById on a missing id
     is how a lab ends up with a null it forgot to guard. */
  var inSecond = """ + second_lookup + r""";
  var patternSel = """ + pattern_lookup + r""";
  var work = document.getElementById('pnWork'), status = document.getElementById('pnStatus');
  var titleOut = document.getElementById('pnTitle'), subOut = document.getElementById('pnSub');
  var svg = document.getElementById('pnPlot');
  var kpis = [document.getElementById('pnK1'), document.getElementById('pnK2'),
              document.getElementById('pnK3'), document.getElementById('pnK4')];

  function setKpis(values) {
    for (var i = 0; i < kpis.length; i += 1) {
      var v = values[i];
      kpis[i].innerHTML = (v === null || v === void 0 || v === '') ? '&mdash;' : v;
    }
  }
  function clearPlot() {
    svg.textContent = '';
    svg.setAttribute('aria-label', 'no picture yet: the input is incomplete');
  }
  /* Bad or empty input gets a sentence and whatever the lab did manage to work
     out. A blank panel would leave the reader guessing whether the lab is
     broken or their expression is. */
  function explain(msg, rows) {
    work.innerHTML = (rows && rows.length) ? table('Where it stopped', [], rows) : '';
    clearPlot();
    setKpis([]);
    status.innerHTML = msg;
  }
  function powerName(e) { return e === 0 ? 'constant' : (e === 1 ? 'x' : 'x^' + e); }
  /* "5 + 3" and "5 - 3", never "5 + -3": the second is what a reader is being
     taught not to write. */
  function sumText(a, b) {
    return Rsign(b) < 0 ? Rtext(a) + ' - ' + Rtext(Rabs(b)) : Rtext(a) + ' + ' + Rtext(b);
  }
  function polyDefinitionRows() {
    return [
      say('the form', 'a_n x^n + ... + a_1 x + a_0, with n a whole number'),
      say('allowed', 'adding, subtracting, multiplying, and whole-number powers of x'),
      say('not allowed', 'x in a denominator, x under a root, x in an exponent'),
      say('why it matters', 'every method in this course -- long division, the factor theorem, the '
        + 'rational root theorem -- is stated for polynomials and is simply false without that restriction')
    ];
  }

  /* ---- the term-by-term product grid, used by two modes ---- */
  /* Every term of P against every term of Q, printed BEFORE anything is
     collected. The collected result is then compared with Pmul, which is a
     different routine: agreement is the evidence that the grid is the product. */
  function productGrid(p, q) {
    var tp = Pterms(p), tq = Pterms(q), acc = [], contrib = {}, rows = [];
    tp.forEach(function (a) {
      var cells = ['<th class="rowhead">' + Pmono(a.c, a.e) + '</th>'];
      tq.forEach(function (b) {
        var c = Rmul(a.c, b.c), e = a.e + b.e;
        while (acc.length <= e) acc.push(R0);
        acc[e] = Radd(acc[e], c);
        (contrib[e] = contrib[e] || []).push({ c: c, e: e });
        cells.push(cell(Pmono(c, e)));
      });
      rows.push(rowOf(cells));
    });
    return {
      heads: ['&times;'].concat(tq.map(function (t) { return Pmono(t.c, t.e); })),
      rows: rows, acc: Pnorm(acc), contrib: contrib, count: tp.length * tq.length
    };
  }
  function collectRows(grid) {
    var powers = Object.keys(grid.contrib).map(Number).sort(function (a, b) { return b - a; });
    return powers.map(function (e) {
      var list = grid.contrib[e], total = grid.acc[e] || R0;
      var cancels = Rzero(total) && list.length > 1;
      return rowOf([
        '<th class="rowhead">' + powerName(e) + '</th>',
        cell(joinTerms(list)),
        cell(Rzero(total) ? '0' : Pmono(total, e), cancels ? 'f' : (list.length > 1 ? 't' : '')),
        cell(list.length < 2 ? muted('nothing to combine')
             : (cancels ? '<span class="tone-red">these cancel</span>' : 'combined'))
      ], cancels ? 'focus' : '');
    });
  }

  /* ---------------------------------------------------------- mode: form */
  function countTypedTerms(node) {
    return (node.k === 'add' || node.k === 'sub')
      ? countTypedTerms(node.a) + countTypedTerms(node.b) : 1;
  }
  function modeForm() {
    var read = readPoly(inMain, 'The expression');
    titleOut.textContent = read.src ? read.src : 'type an expression';
    subOut.textContent = 'is it a polynomial, and if so what shape is it?';

    if (!read.ok && !read.notPoly) {
      explain('<strong>Nothing to describe yet.</strong> ' + read.why
        + ' The definition is in the table; the parser is only asking for something it can read.',
        [say('you typed', read.src ? '<code>' + esc(read.src) + '</code>' : muted('nothing yet'))]
          .concat(polyDefinitionRows()));
      return;
    }

    if (read.notPoly) {
      /* It parsed. It is a function. It is not a POLYNOMIAL, and that is the
         lesson rather than an error, so it gets drawn: the reason it fails the
         definition is the same reason the picture looks like that. */
      var tree = read.tree;
      var fn = function (x) {
        var v = Eeval(tree, { x: x });
        return (typeof v === 'number' && isFinite(v)) ? v : NaN;
      };
      /* Can it be drawn at all? An expression in two variables has no curve in
         x, and claiming one is above would be the lab lying about its own
         picture, so the samples decide what the sentence says. */
      var tried = 0, live = 0;
      for (var si = 0; si <= 240; si += 1) {
        var sx = (si - 120) / 20;      /* exact, so x = 0 really is sampled */
        tried += 1;
        if (!isNaN(fn(sx))) live += 1;
      }
      var drawable = live > 1, gaps = live < tried;
      if (drawable) {
        Plot(svg, viewFor([fn], [-4, 4])).frame().curve(fn).describe(esc(read.src)
          + ' sampled at 480 points. It is a function, but not a polynomial.');
      } else {
        clearPlot();
      }
      setKpis(['not a polynomial', '&mdash;', '&mdash;', '&mdash;']);
      work.innerHTML =
        table('The test', [], [
          say('you typed', '<code>' + esc(read.src) + '</code>'),
          say('does it parse?', chip(true, 'yes') + (drawable
            ? ' it is a function of x, and it is drawn above'
            : ' but it does not define a single curve in x, so there is nothing to draw')),
          say('is it a polynomial?', chip(false, 'no')),
          say('which rule it breaks', whyNotPoly(tree) + '.'),
          say('where it is defined', drawable
            ? (gaps ? 'it has no value at ' + (tried - live) + ' of the ' + tried + ' x values '
                + 'sampled between -6 and 6, and those gaps are the breaks in the curve above'
              : 'at every one of the ' + tried + ' x values sampled between -6 and 6')
            : 'nowhere this lab can draw: a curve needs one variable')
        ])
        + table('What a polynomial is', [], polyDefinitionRows());
      status.innerHTML = '<strong>That is not a polynomial.</strong> The rule it breaks: '
        + whyNotPoly(tree) + '. The distinction is not pedantry: '
        + (drawable
          ? (gaps ? 'the curve above stops where the expression has no value, and a polynomial has a '
                    + 'value at every real number without exception. '
                  : 'a polynomial is a finite sum of whole-number powers, and no such sum bends the way '
                    + 'that curve does. ')
          : 'an expression in two variables is not a curve at all. ')
        + 'Every theorem in this course &mdash; long division, the factor theorem, the rational root '
        + 'theorem &mdash; is stated for polynomials, and each is false without that restriction.';
      return;
    }

    var p = read.poly, terms = Pterms(p), deg = Pdeg(p);
    var atRead = readNumber(inSecond, 'The value of x');

    /* the anatomy, one row per power INCLUDING the missing ones: a zero
       coefficient is not an absent term, and long division depends on it. */
    var anatomy = [];
    for (var i = deg; i >= 0; i -= 1) {
      var c = p[i] || R0, zero = Rzero(c);
      anatomy.push(rowOf([
        '<th class="rowhead">' + powerName(i) + '</th>',
        cell(zero ? muted('0') : Rtext(c)),
        cell(zero ? muted('no term at this power') : Pmono(c, i)),
        cell(zero ? muted('placeholder') : (i === deg ? 'leading term' : (i === 0 ? 'constant term' : '')))
      ]));
    }
    if (!terms.length) {
      anatomy.push(rowOf(['<th class="rowhead">' + powerName(0) + '</th>', cell('0'), cell('0'), cell('the zero polynomial')]));
    }

    var lead = terms.length ? terms[0].c : R0;
    var typed = countTypedTerms(read.tree);
    var shape = [
      say('standard form', Ptext(p)),
      say('degree', Pdegtext(p) + (terms.length ? ' &mdash; a ' + degName(deg) + ' polynomial' : '')),
      say('terms', terms.length + ' &mdash; a ' + termName(terms.length)),
      say('leading coefficient', terms.length ? Rtext(lead) : '0'),
      say('constant term', Rtext(p[0] || R0))
    ];
    if (typed > terms.length) {
      shape.push(say('like terms', 'you typed ' + typed + ' terms and the polynomial has ' + terms.length
        + ': terms with the same power of x were added together, which is all "collecting like terms" means'));
    }
    if (terms.length && deg >= 1) {
      var evenDeg = deg % 2 === 0, up = Rsign(lead) > 0;
      shape.push(say('as x grows large', 'x &rarr; +infinity: ' + (up ? 'f &rarr; +infinity' : 'f &rarr; -infinity')
        + ' &nbsp;&middot;&nbsp; x &rarr; -infinity: '
        + ((evenDeg ? up : !up) ? 'f &rarr; +infinity' : 'f &rarr; -infinity')
        + ' &mdash; decided by the leading term ' + Pmono(lead, deg) + ' alone'));
    }

    var blocks = [table('Every power, including the missing ones',
      ['power', 'coefficient', 'term', ''], anatomy),
      table('What that makes it', [], shape)];

    /* Evaluation, term by term, checked against Horner's rule. */
    var valueText = '';
    if (atRead.ok) {
      var x0 = atRead.value, rows = [], running = R0;
      terms.forEach(function (t) {
        var v = Rmul(t.c, Rpow(x0, t.e));
        running = Radd(running, v);
        rows.push(rowOf([
          '<th class="rowhead">' + Pmono(t.c, t.e) + '</th>',
          cell(Rtext(t.c) + ' * (' + Rtext(x0) + ')^' + t.e),
          cell(Rtext(v))
        ]));
      });
      var horner = Peval(p, x0);
      rows.push(rowOf(['<th class="rowhead">total</th>', cell('f(' + Rtext(x0) + ')'), cell(Rtext(running), 't')], 'focus'));
      rows.push(rowOf(['<th class="rowhead">check</th>',
        cell("Horner's rule, computed separately"),
        cell(Rtext(horner) + ' ' + chip(Requ(running, horner), Requ(running, horner) ? 'agrees' : 'disagrees'))]));
      blocks.push(table('f(' + Rtext(x0) + '), term by term', ['term', 'substituted', 'value'], rows));
      valueText = Rtext(horner);
    } else {
      blocks.push(table('Evaluating', [], [say('cannot evaluate yet', atRead.why)]));
    }
    work.innerHTML = blocks.join('');
    setKpis([Pdegtext(p), terms.length ? Rtext(lead) : '0', Rtext(p[0] || R0), valueText]);

    var fn = Pfn(p);
    var marks = [-3, 3];
    if (atRead.ok) marks.push(Rnum(atRead.value));
    Prationalroots(p).forEach(function (r) { marks.push(Rnum(r)); });
    var plot = Plot(svg, viewFor([fn], marks));
    plot.frame().curve(fn);
    if (atRead.ok) plot.point(Rnum(atRead.value), Rnum(Peval(p, atRead.value)), 'plot-point', 'f(' + Rtext(atRead.value) + ') = ' + Rtext(Peval(p, atRead.value)));
    plot.describe(Ptext(p) + ' sampled at 480 points.');

    status.innerHTML = terms.length
      ? '<strong>' + Ptext(p) + ' is a polynomial of degree ' + Pdegtext(p) + '.</strong> '
        + 'It is a ' + degName(deg) + ' ' + termName(terms.length) + ', and the leading term '
        + Pmono(lead, deg) + ' is the part that decides the two ends of the curve above: every other '
        + 'term is eventually too small to matter. The coefficients are held as exact fractions, so '
        + (Rint(lead) ? 'a coefficient like 1/3 would stay 1/3 here rather than becoming 0.3333.'
                      : 'the fractions you typed are the fractions the lab is using.')
      : '<strong>That is the zero polynomial.</strong> Every coefficient is zero, and it is the one '
        + 'polynomial with no degree at all: calling it degree 0 would break deg(fg) = deg f + deg g, '
        + 'which is why the definition leaves it out.';
  }
"""

    script += r"""
  /* --------------------------------------------------------- mode: arith */
  function modeArith() {
    var A = readPoly(inMain, 'P'), B = readPoly(inSecond, 'Q');
    if (!A.ok || !B.ok) {
      var bad = A.ok ? B : A;
      explain('<strong>There is nothing to add yet.</strong> ' + bad.why,
        [say('P', shownInput(inMain)), say('Q', shownInput(inSecond))]);
      return;
    }
    var p = A.poly, q = B.poly;
    var sum = Padd(p, q), diff = Psub(p, q), negQ = Pscale(q, R(-1n));
    var n = Math.max(Pdeg(p), Pdeg(q), 0);

    titleOut.textContent = '(' + Ptext(p) + ')  and  (' + Ptext(q) + ')';
    subOut.textContent = 'like terms are the ones in the same column';

    /* The columns ARE the method: "combine like terms" is a statement about
       what may be added down a column and nothing else. */
    var heads = ['&nbsp;'];
    for (var i = n; i >= 0; i -= 1) heads.push(powerName(i));
    function coefRow(label, poly, cls) {
      var cells = ['<th class="rowhead">' + label + '</th>'];
      for (var k = n; k >= 0; k -= 1) {
        var c = poly[k] || R0;
        cells.push(cell(Rzero(c) ? muted('0') : Rtext(c)));
      }
      return rowOf(cells, cls);
    }
    var columns = [coefRow('P', p), coefRow('Q', q),
                   coefRow('P + Q', sum, 'focus'), coefRow('P - Q', diff, 'focus')];

    var perPower = [];
    for (i = n; i >= 0; i -= 1) {
      var a = p[i] || R0, b = q[i] || R0;
      perPower.push(rowOf([
        '<th class="rowhead">' + powerName(i) + '</th>',
        cell(Rtext(a) + (Rsign(b) < 0 ? ' - ' + Rtext(Rabs(b)) : ' + ' + Rtext(b)) + ' = ' + Rtext(Radd(a, b))),
        cell(Rtext(a) + (Rsign(b) < 0 ? ' + ' + Rtext(Rabs(b)) : ' - ' + Rtext(b)) + ' = ' + Rtext(Rsub(a, b)))
      ]));
    }

    var checkAdd = Psame(Psub(sum, q), p), checkSub = Psame(Padd(diff, q), p);
    var results = [
      say('P + Q', Ptext(sum)),
      say('P - Q', Ptext(diff)),
      say('the subtraction, written out', 'P - Q = P + (-1)Q = (' + Ptext(p) + ') + (' + Ptext(negQ) + ')'
        + ' &mdash; the minus reaches every term of Q, which is where most sign errors come from'),
      say('degrees', 'deg P = ' + Pdegtext(p) + ', deg Q = ' + Pdegtext(q)
        + ', deg (P + Q) = ' + Pdegtext(sum)),
      say('checked', chip(checkAdd, '(P + Q) - Q = P') + ' ' + chip(checkSub, '(P - Q) + Q = P')
        + ' &mdash; both recomputed from the results above, not copied from P')
    ];

    work.innerHTML =
      table('Lined up by power', heads, columns)
      + table('One column at a time', ['power', 'added', 'subtracted'], perPower)
      + table('The results', [], results);
    setKpis([Pdegtext(p), Pdegtext(q), Pdegtext(sum), Pdegtext(diff)]);

    var fp = Pfn(p), fq = Pfn(q), fs = Pfn(sum);
    var win = viewFor([fp, fq, fs], [-3, 3]);
    var plot = Plot(svg, win);
    plot.frame().curve(fq, 'plot-curve parent').curve(fp, 'plot-curve alt').curve(fs);
    var x0 = (win.xmin + win.xmax) / 2 + (win.xmax - win.xmin) * 0.18;
    plot.point(x0, fp(x0), 'plot-point vertex').point(x0, fq(x0), 'plot-point')
        .point(x0, fs(x0), 'plot-point root', 'P + Q here is the two heights added');
    plot.describe('P, Q and P + Q sampled at 480 points each; at every x the third height is the '
      + 'sum of the first two.');

    var dropped = !Pzero(sum) && Pdeg(sum) < Math.max(Pdeg(p), Pdeg(q));
    status.innerHTML = Pzero(diff)
      ? '<strong>P - Q is the zero polynomial.</strong> Subtracting a polynomial from itself leaves '
        + 'nothing, and the zero polynomial is the one polynomial with no degree: there is no leading '
        + 'term to take a degree from. P + Q = ' + Ptext(sum) + ' is the interesting half here.'
      : (dropped
        ? '<strong>The degree dropped.</strong> deg P = ' + Pdegtext(p) + ' and deg Q = ' + Pdegtext(q)
          + ', but deg (P + Q) = ' + Pdegtext(sum) + ', because the leading coefficients '
          + Rtext(p[Math.max(Pdeg(p), Pdeg(q))] || R0) + ' and ' + Rtext(q[Math.max(Pdeg(p), Pdeg(q))] || R0)
          + ' add to zero. This is why the rule for sums is deg(P + Q) &lt;= max(deg P, deg Q) rather '
          + 'than an equality &mdash; the rule for products has no such escape.'
        : '<strong>Addition happens down the columns and nowhere else.</strong> Terms in different '
          + 'columns are different powers of x, and adding them would be like adding 3 to 3x. '
          + 'P + Q = ' + Ptext(sum) + ' and P - Q = ' + Ptext(diff) + ', '
          + (p.concat(q).some(function (c) { return !Rint(c); })
             ? 'and the fractions were added as fractions rather than as rounded decimals.'
             : 'each coefficient the sum of the two above it.'));
  }

  /* ------------------------------------------------------ mode: multiply */
  function modeMultiply() {
    var A = readPoly(inMain, 'P'), B = readPoly(inSecond, 'Q');
    if (!A.ok || !B.ok) {
      var bad = A.ok ? B : A;
      explain('<strong>There is nothing to multiply yet.</strong> ' + bad.why,
        [say('P', shownInput(inMain)), say('Q', shownInput(inSecond))]);
      return;
    }
    var p = A.poly, q = B.poly;
    titleOut.textContent = '(' + Ptext(p) + ')(' + Ptext(q) + ')';
    subOut.textContent = 'every term against every term';

    if (Pzero(p) || Pzero(q)) {
      setKpis([Pdegtext(p), Pdegtext(q), Pdegtext([]), '0']);
      clearPlot();
      work.innerHTML = table('A factor is zero', [], [
        say('P', Ptext(p)), say('Q', Ptext(q)),
        say('the product', '0 &mdash; every term of the grid is a product with a zero factor, so the '
          + 'grid is empty and the product is the zero polynomial')
      ]);
      status.innerHTML = '<strong>One factor is the zero polynomial, so the product is zero.</strong> '
        + 'It is the one case where the degree rule deg(PQ) = deg P + deg Q has nothing to say, because '
        + 'the zero polynomial has no degree.';
      return;
    }

    var grid = productGrid(p, q);
    var product = Pmul(p, q);
    var gridAgrees = Psame(grid.acc, product);
    var degreeAdds = Pdeg(product) === Pdeg(p) + Pdeg(q);
    var cancelled = [];
    Object.keys(grid.contrib).forEach(function (k) {
      if (grid.contrib[k].length > 1 && Rzero(grid.acc[Number(k)] || R0)) cancelled.push(powerName(Number(k)));
    });

    work.innerHTML =
      table('Every term against every term', grid.heads, grid.rows)
      + table('Collecting the like terms', ['power', 'products landing there', 'total', ''], collectRows(grid))
      + table('The result', [], [
        say('product', Ptext(product)),
        say('products multiplied', grid.count + ' = ' + Pterms(p).length + ' terms times ' + Pterms(q).length + ' terms'),
        say('degrees', 'deg P + deg Q = ' + Pdeg(p) + ' + ' + Pdeg(q) + ' = ' + (Pdeg(p) + Pdeg(q))
          + ', and deg PQ = ' + Pdegtext(product) + ' ' + chip(degreeAdds, degreeAdds ? 'as it must' : 'impossible over a field')),
        say('checked', chip(gridAgrees, gridAgrees ? 'the grid and the multiplication routine agree'
          : 'the grid and the multiplication routine disagree')
          + ' &mdash; the grid above was summed cell by cell, and compared with a separately written '
          + 'polynomial multiply')
      ]);
    setKpis([Pdegtext(p), Pdegtext(q), Pdegtext(product), String(grid.count)]);

    var fp = Pfn(p), fq = Pfn(q), fprod = Pfn(product);
    var roots = Prationalroots(product);
    var marks = roots.map(Rnum);
    marks.push(-2); marks.push(2);
    var plot = Plot(svg, viewFor([fprod], marks));
    plot.frame().curve(fq, 'plot-curve parent').curve(fp, 'plot-curve alt').curve(fprod);
    roots.forEach(function (r) { plot.point(Rnum(r), 0, 'plot-point root', Rtext(r)); });
    plot.describe('P, Q and their product sampled at 480 points; the product meets the axis exactly '
      + 'where one of the factors does.');

    status.innerHTML = '<strong>' + grid.count + ' products, then one collection step.</strong> '
      + (cancelled.length
        ? 'The ' + cancelled.join(' and ') + ' column' + (cancelled.length > 1 ? 's' : '') + ' cancelled '
          + 'to nothing, which is why (' + Ptext(p) + ')(' + Ptext(q) + ') = ' + Ptext(product)
          + ' has fewer terms than the ' + grid.count + ' products it came from. Cancellation is the '
          + 'reason the number of terms in a product is unpredictable &mdash; the DEGREE is not: '
        : 'Nothing cancelled here, so the product carries the powers the grid produced. The degree is '
          + 'the part that is never in doubt: ')
      + 'deg PQ = deg P + deg Q = ' + Pdeg(product) + ', because the two leading terms '
      + Pmono(Plead(p), Pdeg(p)) + ' and ' + Pmono(Plead(q), Pdeg(q)) + ' can only multiply to '
      + Pmono(Rmul(Plead(p), Plead(q)), Pdeg(product)) + ', and nothing else in the grid reaches that power.';
  }
"""

    script += r"""
  /* ------------------------------------------------------- mode: special */
  /* Each pattern carries BOTH routes to the same polynomial: the pieces the
     identity claims, and the brackets multiplied out honestly. The lab runs
     both and prints whether they agreed, which is the only reason a reader
     should believe the identity. `naive` is the wrong answer this identity is
     famous for, kept so the lab can print the exact amount it is wrong by. */
  var PATTERNS = {
    sqsum: {
      title: 'the square of a sum',
      identity: '(A + B)^2 = A^2 + 2AB + B^2',
      shown: function (a, b) { return '(' + Ptext(Padd(a, b)) + ')^2'; },
      substituted: function (A, B) {
        return '(' + A + ' + ' + B + ')^2 = (' + A + ')^2 + 2(' + A + ')(' + B + ') + (' + B + ')^2';
      },
      factors: function (a, b) { return [Padd(a, b), Padd(a, b)]; },
      pieces: function (a, b) {
        return [['A^2', Pmul(a, a)], ['2AB', Pscale(Pmul(a, b), R(2n))], ['B^2', Pmul(b, b)]];
      },
      naive: function (a, b) { return Padd(Pmul(a, a), Pmul(b, b)); },
      naiveName: 'A^2 + B^2',
      lesson: 'The middle term 2AB is the entire content of this identity, and it is exactly the term '
        + 'that gets dropped. Squaring does not distribute over addition.'
    },
    sqdiff: {
      title: 'the square of a difference',
      identity: '(A - B)^2 = A^2 - 2AB + B^2',
      shown: function (a, b) { return '(' + Ptext(Psub(a, b)) + ')^2'; },
      substituted: function (A, B) {
        return '(' + A + ' - ' + B + ')^2 = (' + A + ')^2 - 2(' + A + ')(' + B + ') + (' + B + ')^2';
      },
      factors: function (a, b) { return [Psub(a, b), Psub(a, b)]; },
      pieces: function (a, b) {
        return [['A^2', Pmul(a, a)], ['-2AB', Pscale(Pmul(a, b), R(-2n))], ['B^2', Pmul(b, b)]];
      },
      naive: function (a, b) { return Psub(Pmul(a, a), Pmul(b, b)); },
      naiveName: 'A^2 - B^2',
      lesson: 'The last term is +B^2 even though the bracket had a minus: a negative squared is '
        + 'positive. The minus survives only in the middle term.'
    },
    conj: {
      title: 'a difference of squares',
      identity: '(A + B)(A - B) = A^2 - B^2',
      shown: function (a, b) { return '(' + Ptext(Padd(a, b)) + ')(' + Ptext(Psub(a, b)) + ')'; },
      substituted: function (A, B) {
        return '(' + A + ' + ' + B + ')(' + A + ' - ' + B + ') = (' + A + ')^2 - (' + B + ')^2';
      },
      factors: function (a, b) { return [Padd(a, b), Psub(a, b)]; },
      pieces: function (a, b) { return [['A^2', Pmul(a, a)], ['-B^2', Pscale(Pmul(b, b), R(-1n))]]; },
      naive: function (a, b) { return Padd(Pmul(a, a), Pmul(b, b)); },
      naiveName: 'A^2 + B^2',
      lesson: 'Four products go into the grid and two of them, -AB and +AB, cancel. That cancellation '
        + 'is the identity; read backwards it is the difference-of-squares factorisation.'
    },
    cubesum: {
      title: 'the cube of a sum',
      identity: '(A + B)^3 = A^3 + 3A^2B + 3AB^2 + B^3',
      shown: function (a, b) { return '(' + Ptext(Padd(a, b)) + ')^3'; },
      substituted: function (A, B) {
        return '(' + A + ' + ' + B + ')^3 = (' + A + ')^3 + 3(' + A + ')^2(' + B + ') + 3('
          + A + ')(' + B + ')^2 + (' + B + ')^3';
      },
      factors: function (a, b) { return [Padd(a, b), Padd(a, b), Padd(a, b)]; },
      pieces: function (a, b) {
        return [['A^3', Ppow(a, 3)], ['3A^2B', Pscale(Pmul(Pmul(a, a), b), R(3n))],
                ['3AB^2', Pscale(Pmul(a, Pmul(b, b)), R(3n))], ['B^3', Ppow(b, 3)]];
      },
      naive: function (a, b) { return Padd(Ppow(a, 3), Ppow(b, 3)); },
      naiveName: 'A^3 + B^3',
      lesson: 'The coefficients 1, 3, 3, 1 are the fourth row of Pascal\'s triangle, and they are not '
        + 'optional: A^3 + B^3 is a different polynomial, and it is the FACTORISATION of a sum of '
        + 'cubes that has the familiar bracket, not the expansion of a cube.'
    },
    cubediff: {
      title: 'the cube of a difference',
      identity: '(A - B)^3 = A^3 - 3A^2B + 3AB^2 - B^3',
      shown: function (a, b) { return '(' + Ptext(Psub(a, b)) + ')^3'; },
      substituted: function (A, B) {
        return '(' + A + ' - ' + B + ')^3 = (' + A + ')^3 - 3(' + A + ')^2(' + B + ') + 3('
          + A + ')(' + B + ')^2 - (' + B + ')^3';
      },
      factors: function (a, b) { return [Psub(a, b), Psub(a, b), Psub(a, b)]; },
      pieces: function (a, b) {
        return [['A^3', Ppow(a, 3)], ['-3A^2B', Pscale(Pmul(Pmul(a, a), b), R(-3n))],
                ['3AB^2', Pscale(Pmul(a, Pmul(b, b)), R(3n))], ['-B^3', Pscale(Ppow(b, 3), R(-1n))]];
      },
      naive: function (a, b) { return Psub(Ppow(a, 3), Ppow(b, 3)); },
      naiveName: 'A^3 - B^3',
      lesson: 'The signs alternate because every B carries a minus: an odd number of them leaves a '
        + 'minus, an even number cancels it.'
    }
  };

  function modeSpecial() {
    var A = readPoly(inMain, 'A'), B = readPoly(inSecond, 'B');
    if (!A.ok || !B.ok) {
      var bad = A.ok ? B : A;
      explain('<strong>The pattern needs both pieces.</strong> ' + bad.why
        + ' A and B may be any polynomials at all &mdash; <code>2x</code>, <code>3</code>, '
        + '<code>x^2</code>, <code>3/2</code>.',
        [say('A', shownInput(inMain)), say('B', shownInput(inSecond))]);
      return;
    }
    var key = patternSel ? String(patternSel.value) : 'sqsum';
    var pat = PATTERNS[key] || PATTERNS.sqsum;
    var a = A.poly, b = B.poly;
    var Atext = Pfactortext(a), Btext = Pfactortext(b);

    titleOut.textContent = pat.shown(a, b);
    subOut.textContent = pat.identity;

    /* route 1: the identity, piece by piece */
    var pieces = pat.pieces(a, b), fromIdentity = [];
    var pieceRows = pieces.map(function (item) {
      fromIdentity = Padd(fromIdentity, item[1]);
      return rowOf(['<th class="rowhead">' + item[0] + '</th>', cell(Ptext(item[1]))]);
    });
    pieceRows.push(rowOf(['<th class="rowhead">sum</th>', cell(Ptext(fromIdentity), 't')], 'focus'));

    /* route 2: multiply the brackets out, with no identity involved */
    var factors = pat.factors(a, b), expanded = [R1], stageRows = [];
    factors.forEach(function (f, i) {
      expanded = Pmul(expanded, f);
      stageRows.push(rowOf([
        '<th class="rowhead">' + (i === 0 ? 'first bracket' : 'times bracket ' + (i + 1)) + '</th>',
        cell(Pfactortext(f)), cell(Ptext(expanded))
      ]));
    });

    var agree = Psame(fromIdentity, expanded);
    var naive = pat.naive(a, b), miss = Psub(expanded, naive);

    var blocks = [
      table('The pattern', [], [
        say('identity', pat.identity),
        say('A', Atext), say('B', Btext),
        say('substituted', pat.substituted(Atext, Btext))
      ]),
      table('Route 1: the identity, piece by piece', ['piece', 'polynomial'], pieceRows)
    ];
    if (factors.length === 2) {
      var grid = productGrid(factors[0], factors[1]);
      blocks.push(table('Route 2: multiply the brackets out, term by term', grid.heads, grid.rows));
      blocks.push(table('Collecting those products', ['power', 'products landing there', 'total', ''], collectRows(grid)));
    } else {
      blocks.push(table('Route 2: multiply the brackets out, one at a time', ['stage', 'bracket', 'so far'], stageRows));
    }
    blocks.push(table('Do the two routes agree?', [], [
      say('from the identity', Ptext(fromIdentity)),
      say('from the multiplication', Ptext(expanded)),
      say('verdict', chip(agree, agree ? 'the same polynomial' : 'they disagree')
        + ' &mdash; computed by two different routes on your A and B, not copied from one another')
    ]));
    blocks.push(table('The wrong answer this identity is famous for', [], [
      say('what gets written', pat.naiveName + ' = ' + Ptext(naive)),
      say('what it actually is', Ptext(expanded)),
      say('wrong by', Pzero(miss) ? 'nothing, for this A and B &mdash; see the note below' : Ptext(miss)),
      say('why', pat.lesson)
    ]));
    work.innerHTML = blocks.join('');
    setKpis([pat.title, Ptext(expanded), Pzero(miss) ? 'nothing' : Ptext(miss),
             chip(agree, agree ? 'yes' : 'no')]);

    var fe = Pfn(expanded), fn2 = Pfn(naive);
    var marks = Prationalroots(miss).map(Rnum);
    marks.push(-2); marks.push(2);
    Plot(svg, viewFor([fe, fn2], marks)).frame()
      .curve(fn2, 'plot-curve warn').curve(fe)
      .describe('The expansion and the common wrong answer, both sampled at 480 points. They are '
        + 'different curves wherever ' + Ptext(miss) + ' is not zero.');

    status.innerHTML = Pzero(miss)
      ? '<strong>For this A and B the wrong answer happens to be right.</strong> ' + Ptext(miss)
        + ' is the difference, and it is zero here &mdash; usually because A or B is zero. '
        + 'That is a coincidence of these two pieces, not a rule: change B and the two curves '
        + 'above separate immediately.'
      : '<strong>' + pat.shown(a, b) + ' = ' + Ptext(expanded) + '.</strong> '
        + 'Writing ' + pat.naiveName + ' instead gives ' + Ptext(naive) + ', which is wrong by exactly '
        + Ptext(miss) + ' &mdash; the red curve above. ' + pat.lesson
        + ' Both routes to the answer were computed here from your A and B, and they '
        + (agree ? 'agreed' : 'did not agree') + '.';
  }

  /* -------------------------------------------------------- mode: divide */
  /* This is Pdivmod's loop, written out again so the remainder can be shown
     BEFORE and AFTER each subtraction. Its quotient and remainder are compared
     with Pdivmod's below: the same algorithm implemented twice, and a
     disagreement would mean one of the two is wrong. */
  function longDivision(a, b) {
    var q = [], r = Pnorm(a), rows = [], guard = 0;
    var db = Pdeg(b), lb = Plead(b);
    while (!Pzero(r) && Pdeg(r) >= db && guard < 64) {
      guard += 1;
      var dr = Pdeg(r), coef = Rdiv(Plead(r), lb), shift = dr - db, term = [];
      for (var i = 0; i < shift; i += 1) term.push(R0);
      term.push(coef);
      var product = Pmul(term, b), after = Psub(r, product);
      rows.push({ before: r, term: term, product: product, after: after });
      r = after;
      q = Padd(q, term);
    }
    return { q: Pnorm(q), r: r, rows: rows };
  }

  function modeDivide() {
    var A = readPoly(inMain, 'The dividend f'), B = readPoly(inSecond, 'The divisor d');
    if (!A.ok || !B.ok) {
      var bad = A.ok ? B : A;
      explain('<strong>There is nothing to divide yet.</strong> ' + bad.why,
        [say('f', shownInput(inMain)), say('d', shownInput(inSecond))]);
      return;
    }
    var f = A.poly, d = B.poly;
    titleOut.textContent = '(' + Ptext(f) + ') / (' + Ptext(d) + ')';
    subOut.textContent = 'f = d * q + r, with deg r < deg d';

    if (Pzero(d)) {
      explain('<strong>The divisor is the zero polynomial.</strong> Division by zero is undefined for '
        + 'polynomials for the same reason it is for numbers: there is no q with 0 * q = f unless f is '
        + 'zero too, and then every q works. Put something non-zero in the divisor box.',
        [say('f', Ptext(f)), say('d', '0')]);
      return;
    }

    var run = longDivision(f, d), lib = Pdivmod(f, d);
    var agrees = Psame(run.q, lib.q) && Psame(run.r, lib.r);
    var rebuilt = Padd(Pmul(d, run.q), run.r);
    var identityHolds = Psame(rebuilt, f);
    var degreeOk = Pzero(run.r) || Pdeg(run.r) < Pdeg(d);
    var exact = Pzero(run.r);

    var traceRows = run.rows.map(function (st, i) {
      return rowOf([
        '<th class="rowhead">' + (i + 1) + '</th>',
        cell(Ptext(st.before)),
        cell(Pmono(Plead(st.term), Pdeg(st.term))),
        cell(Ptext(st.product)),
        cell(Ptext(st.after), i === run.rows.length - 1 ? 'on' : '')
      ]);
    });
    if (!traceRows.length) {
      traceRows.push(rowOf([
        '<th class="rowhead">&mdash;</th>',
        cell(Ptext(f)), cell('none'), cell('none'), cell(Ptext(f), 'on')
      ]));
    }

    var blocks = [
      table('The long division, one subtraction at a time',
        ['step', 'what is left to divide', 'quotient term', 'that term times d', 'after subtracting'],
        traceRows),
      table('The result', [], [
        say('quotient q', Ptext(run.q)),
        say('remainder r', Ptext(run.r)),
        say('as a single expression', exact
          ? '(' + Ptext(f) + ') / (' + Ptext(d) + ') = ' + Ptext(run.q)
          : '(' + Ptext(f) + ') / (' + Ptext(d) + ') = ' + Ptext(run.q) + ' + (' + Ptext(run.r) + ')/(' + Ptext(d) + ')'),
        say('the division algorithm', 'd * q + r = (' + Ptext(d) + ')(' + Ptext(run.q) + ')'
          + (Pzero(run.r) ? '' : ' + (' + Ptext(run.r) + ')') + ' = ' + Ptext(rebuilt) + ' '
          + chip(identityHolds, identityHolds ? 'equals f' : 'does not equal f')),
        say('the stopping rule', 'deg r = ' + Pdegtext(run.r) + ', deg d = ' + Pdegtext(d) + ' '
          + chip(degreeOk, degreeOk ? 'deg r &lt; deg d, so the division is finished' : 'the loop stopped too early')),
        say('checked against the library', chip(agrees, agrees ? 'the trace agrees with the divmod routine'
          : 'the trace and the divmod routine disagree'))
      ])
    ];
    if (!run.rows.length) {
      blocks.push(table('Why the trace is empty', [], [
        say('the first step never happens', 'deg f = ' + Pdegtext(f) + ' is already less than deg d = '
          + Pdegtext(d) + ', so there is no term of q to write down'),
        say('the answer', 'q = 0 and r = f. That is a complete, correct division: ' + Ptext(f)
          + ' = (' + Ptext(d) + ') * 0 + ' + Ptext(f) + ', and the remainder already satisfies deg r &lt; deg d.')
      ]));
    }
    if (exact) {
      blocks.push(table('An exact division is a factorisation', [], [
        say('r = 0', Ptext(f) + ' = (' + Ptext(d) + ')(' + Ptext(run.q) + ')'),
        say('so', 'd is a factor of f, and every root of d is a root of f')
      ]));
    }
    work.innerHTML = blocks.join('');
    setKpis([Ptext(run.q), Ptext(run.r), chip(degreeOk, degreeOk ? 'yes' : 'no'),
             chip(exact, exact ? 'yes, r = 0' : 'no')]);

    var ff = Pfn(f), fdq = Pfn(Pmul(d, run.q)), fr = Pfn(run.r);
    var marks = Prationalroots(f).map(Rnum);
    Prationalroots(d).forEach(function (r) { marks.push(Rnum(r)); });
    marks.push(-2); marks.push(2);
    Plot(svg, viewFor([ff, fdq], marks)).frame()
      .curve(fr, 'plot-curve parent').curve(fdq, 'plot-curve alt').curve(ff)
      .describe('f, the product d*q, and the remainder r, each sampled at 480 points. f and d*q are '
        + (exact ? 'the same curve, because the remainder is zero' : 'the same curve shifted by r'));

    status.innerHTML = exact
      ? '<strong>The remainder is zero, so this is a factorisation.</strong> '
        + Ptext(f) + ' = (' + Ptext(d) + ')(' + Ptext(run.q) + '), and the two curves above lie on top '
        + 'of each other because d*q IS f. Every root of ' + Ptext(d) + ' is therefore a root of f.'
      : '<strong>' + Ptext(f) + ' = (' + Ptext(d) + ')(' + Ptext(run.q) + ') + (' + Ptext(run.r) + ').</strong> '
        + 'The division stops when the remainder has lower degree than the divisor: deg r = '
        + Pdegtext(run.r) + ' and deg d = ' + Pdegtext(d) + '. Carrying on would mean writing a quotient '
        + 'term with a negative power of x, which is not a polynomial. '
        + (run.rows.length ? 'Each row above is one subtraction, and the last "after subtracting" column '
            + 'is the remainder.' : 'The trace is empty because the very first step was already impossible.');
  }
"""

    script += r"""
  /* ----------------------------------------------------- mode: synthetic */
  /* The short table for division by x - c. Every number in it is produced
     here; the remainder is then compared with f(c) computed a completely
     different way, which is how the remainder theorem gets CHECKED on the
     reader's polynomial instead of being quoted at them. */
  function syntheticRun(p, c) {
    var n = Pdeg(p), coefs = [], i;
    for (i = n; i >= 0; i -= 1) coefs.push(p[i] || R0);
    var carried = [null], totals = [coefs[0]];
    for (i = 1; i < coefs.length; i += 1) {
      var mult = Rmul(totals[i - 1], c);
      carried.push(mult);
      totals.push(Radd(coefs[i], mult));
    }
    return {
      coefs: coefs, carried: carried, totals: totals,
      quotient: Pnorm(totals.slice(0, totals.length - 1).slice().reverse()),
      remainder: totals[totals.length - 1]
    };
  }

  function modeSynthetic() {
    var A = readPoly(inMain, 'f'), C = readNumber(inSecond, 'c');
    if (!A.ok || !C.ok) {
      explain('<strong>Synthetic division needs both boxes.</strong> ' + (A.ok ? C.why : A.why),
        [say('f', shownInput(inMain)), say('c', shownInput(inSecond))]);
      return;
    }
    var f = A.poly, c = C.value, divisor = [Rneg(c), R1];
    /* x - c with the sign resolved: for c = -2 the divisor a reader writes is
       x + 2, and "x - (-2)" on the page would be the lab showing its working
       rather than the mathematics. */
    var divisorText = Rzero(c) ? 'x'
      : 'x ' + (Rsign(c) < 0 ? '+ ' + Rtext(Rabs(c)) : '- ' + Rtext(c));
    titleOut.textContent = '(' + Ptext(f) + ') / (' + divisorText + ')';
    subOut.textContent = 'the remainder should turn out to be f(' + Rtext(c) + ')';

    if (Pdeg(f) < 1) {
      explain('<strong>Synthetic division needs a polynomial of degree at least 1.</strong> '
        + 'You have ' + Ptext(f) + ', which has nothing to divide: dividing it by x - ' + Rtext(c)
        + ' gives the quotient 0 and the remainder ' + Ptext(f) + ' itself, and the table would have '
        + 'one column. Try ' + esc('x^3 - 4x^2 + x + 6') + '.',
        [say('f', Ptext(f)), say('deg f', Pdegtext(f)), say('c', Rtext(c))]);
      return;
    }

    var run = syntheticRun(f, c);
    var n = Pdeg(f);
    var heads = ['&nbsp;'];
    for (var i = n; i >= 0; i -= 1) heads.push(powerName(i));

    var coefCells = ['<th class="rowhead">coefficients of f</th>'];
    var carryCells = ['<th class="rowhead">multiply by c = ' + Rtext(c) + '</th>'];
    var totalCells = ['<th class="rowhead">add down</th>'];
    var placeholders = [];
    run.coefs.forEach(function (co, k) {
      var power = n - k;
      if (Rzero(co)) placeholders.push(powerName(power));
      coefCells.push(cell(Rzero(co) ? muted('0') : Rtext(co)));
      carryCells.push(cell(run.carried[k] === null ? muted('&mdash;') : Rtext(run.carried[k])));
      totalCells.push(cell(Rtext(run.totals[k]), k === run.coefs.length - 1 ? 'on' : ''));
    });

    var narration = [];
    narration.push(rowOf(['<th class="rowhead">1</th>',
      cell('bring the leading coefficient down'), cell(Rtext(run.totals[0]))]));
    for (i = 1; i < run.coefs.length; i += 1) {
      narration.push(rowOf(['<th class="rowhead">' + (i + 1) + '</th>',
        cell(Rtext(run.totals[i - 1]) + ' * ' + Rtext(c) + ' = ' + Rtext(run.carried[i])
          + ', and ' + sumText(run.coefs[i], run.carried[i]) + ' ='),
        cell(Rtext(run.totals[i]), i === run.coefs.length - 1 ? 'on' : '')]));
    }

    /* three independent checks of the same table */
    var fc = Peval(f, c);
    var remainderIsFc = Requ(run.remainder, fc);
    var lib = Pdivmod(f, divisor);
    var matchesLong = Psame(run.quotient, lib.q) && Requ(run.remainder, lib.r.length ? lib.r[0] : R0);
    var rebuilt = Padd(Pmul(divisor, run.quotient), [run.remainder]);
    var rebuildOk = Psame(rebuilt, f);

    var blocks = [
      table('The synthetic table', heads, [rowOf(coefCells), rowOf(carryCells), rowOf(totalCells, 'focus')]),
      table('What each column did', ['step', 'arithmetic', 'total'], narration),
      table('Reading the table', [], [
        say('quotient', Ptext(run.quotient) + ' &mdash; the totals except the last, one degree lower than f'),
        say('remainder', Rtext(run.remainder) + ' &mdash; the last total')
      ]),
      table('The remainder theorem, checked rather than asserted', [], [
        say('the theorem', 'dividing f by x - c leaves the remainder f(c)'),
        say('the table says', 'remainder = ' + Rtext(run.remainder)),
        say('f(' + Rtext(c) + '), evaluated separately', Ptext(f) + ' at x = ' + Rtext(c) + ' is ' + Rtext(fc)
          + ' &mdash; computed by evaluating the polynomial, with no reference to the table above'),
        say('verdict', chip(remainderIsFc, remainderIsFc ? 'the two agree' : 'the two disagree')),
        say('long division agrees too', chip(matchesLong, matchesLong ? 'same quotient and remainder' : 'different')
          + ' ' + chip(rebuildOk, rebuildOk ? '(x - c) * q + r = f' : 'reconstruction failed'))
      ])
    ];
    if (placeholders.length) {
      blocks.push(table('The zeros are not optional', [], [
        say('missing powers', placeholders.join(', ') + ' &mdash; ' + Ptext(f) + ' has no term there'),
        say('what happens if you leave them out', 'every later column shifts one place left and the '
          + 'quotient comes out with the wrong degree. A zero is what holds the column open.')
      ]));
    }
    if (Rzero(run.remainder)) {
      var factorRows = [
        say('remainder = 0', 'so ' + divisorText + ' divides f exactly'),
        say('the factor theorem', Ptext(f) + ' = (' + divisorText + ')(' + Ptext(run.quotient) + ')'),
        say('and so', 'x = ' + Rtext(c) + ' is a root of f: the curve below crosses the axis there')
      ];
      if (!Rint(c)) {
        var scaled = Pscale(run.quotient, R(c.d));
        factorRows.push(say('with whole coefficients', 'c = ' + Rtext(c) + ' is a fraction, so the usual '
          + 'integer factor is ' + Ptext([Rneg(R(c.n)), R(c.d)]) + ': multiply the bracket by ' + c.d
          + ' and divide the quotient by it, giving ' + Ptext(f) + ' = ('
          + Ptext([Rneg(R(c.n)), R(c.d)]) + ')(' + Ptext(Pscale(run.quotient, R(1n, c.d))) + ')'
          + ' ' + chip(Psame(Pmul([Rneg(R(c.n)), R(c.d)], Pscale(run.quotient, R(1n, c.d))), f), 'multiplied back out')));
      }
      blocks.push(table('A zero remainder is a factorisation', [], factorRows));
    }
    work.innerHTML = blocks.join('');
    setKpis([Rtext(c), Rtext(run.remainder), Rtext(fc),
             chip(remainderIsFc, remainderIsFc ? 'yes' : 'no')]);

    var ff = Pfn(f);
    var marks = [Rnum(c) - 1, Rnum(c) + 1];
    Prationalroots(f).forEach(function (r) { marks.push(Rnum(r)); });
    var plot = Plot(svg, viewFor([ff], marks));
    plot.frame().curve(ff).vline(Rnum(c), 'plot-aux', 'x = ' + Rtext(c))
        .point(Rnum(c), Rnum(fc), 'plot-point root', 'f(' + Rtext(c) + ') = ' + Rtext(fc));
    plot.describe(Ptext(f) + ' sampled at 480 points, with the height at x = ' + Rtext(c)
      + ' marked: that height is the remainder.');

    status.innerHTML = Rzero(run.remainder)
      ? '<strong>The remainder is 0, so ' + divisorText + ' is a factor.</strong> '
        + Ptext(f) + ' = (' + divisorText + ')(' + Ptext(run.quotient) + '), '
        + 'and the curve crosses the axis at x = ' + Rtext(c)
        + ' exactly because f(' + Rtext(c) + ') = 0. Remainder zero, root, factor: three names for one fact.'
      : '<strong>The remainder is ' + Rtext(run.remainder) + ', and f(' + Rtext(c) + ') is '
        + Rtext(fc) + '.</strong> Those two numbers were computed independently &mdash; one by running '
        + 'the table, one by evaluating the polynomial &mdash; and they '
        + (remainderIsFc ? 'agree, which is the remainder theorem on your polynomial rather than on a '
            + 'textbook example. ' : 'disagree, which would be a bug in this lab. ')
        + 'The marked height on the curve is that same number, so x = ' + Rtext(c) + ' is not a root: '
        + 'the graph misses the axis there by ' + Rtext(fc) + '.';
  }

  /* ------------------------------------------------------------- wiring */
  function redraw() {
    try {
      if (MODE === 'form') modeForm();
      else if (MODE === 'arith') modeArith();
      else if (MODE === 'multiply') modeMultiply();
      else if (MODE === 'special') modeSpecial();
      else if (MODE === 'divide') modeDivide();
      else modeSynthetic();
    } catch (err) {
      /* Nothing above should throw. If a reader finds the input that does, they
         get a sentence rather than a panel that has silently stopped. */
      explain('<strong>That input stopped the lab.</strong> ' + esc(err && err.message ? err.message : String(err))
        + '. Pick one of the examples to get moving again, and change it a little at a time to find '
        + 'what this lab could not read.', []);
    }
  }

  function applyPreset() {
    var parts = String(preset.value).split('|');
    inMain.value = parts[0] || '';
    if (inSecond) inSecond.value = parts[1] || '';
    if (patternSel && parts[2]) patternSel.value = parts[2];
    redraw();
  }
  preset.addEventListener('change', applyPreset);
  if (patternSel) patternSel.addEventListener('change', redraw);
  [inMain, inSecond].forEach(function (el) { if (el) el.addEventListener('input', redraw); });
  applyPreset();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an example, or type your own"),
        panel_intro=cfg.get("panel_intro", POLY_PANEL_INTRO[mode]),
        script=script,
    )


# ================================================================ lab two:
#                                                    factoring, as a search

FACTOR_PRESETS = {
    "gcf": [
        ("6x^3 + 9x^2 - 15x", "6x^3 + 9x^2 - 15x"),
        ("4x^2 + 6x + 9   (nothing to take out)", "4x^2 + 6x + 9"),
        ("-2x^3 + 8x^2 - 6x   (take out the minus)", "-2x^3 + 8x^2 - 6x"),
        ("(1/2)x^2 + (3/4)x   (fractions)", "(1/2)x^2 + (3/4)x"),
        ("12x^4 - 18x^3 + 30x^2", "12x^4 - 18x^3 + 30x^2"),
        ("5x^2 + 10   (no x in the GCF)", "5x^2 + 10"),
    ],
    "grouping": [
        ("x^3 + 3x^2 + 2x + 6", "x^3 + 3x^2 + 2x + 6"),
        ("2x^3 - 6x^2 + 5x - 15", "2x^3 - 6x^2 + 5x - 15"),
        ("x^3 + 2x^2 - 3x - 6   (the sign trap)", "x^3 + 2x^2 - 3x - 6"),
        ("x^3 + 2x^2 + 2x + 1   (grouping fails, it still factors)", "x^3 + 2x^2 + 2x + 1"),
        ("x^3 + x^2 + 2x + 6   (grouping fails, nothing factors)", "x^3 + x^2 + 2x + 6"),
        ("6x^3 + 4x^2 + 9x + 6", "6x^3 + 4x^2 + 9x + 6"),
    ],
    "trinomial": [
        ("x^2 + 7x + 12", "x^2 + 7x + 12"),
        ("x^2 - 5x + 6", "x^2 - 5x + 6"),
        ("x^2 + 2x - 15", "x^2 + 2x - 15"),
        ("x^2 + x + 1   (no pair works)", "x^2 + x + 1"),
        ("x^2 + 6x + 9   (a repeated factor)", "x^2 + 6x + 9"),
        ("2x^2 + 7x + 3   (a is not 1: wrong method)", "2x^2 + 7x + 3"),
    ],
    "ac": [
        ("6x^2 + 11x + 3", "6x^2 + 11x + 3"),
        ("2x^2 - 7x + 3", "2x^2 - 7x + 3"),
        ("4x^2 - 4x - 15", "4x^2 - 4x - 15"),
        ("3x^2 + 2x + 5   (no pair works)", "3x^2 + 2x + 5"),
        ("12x^2 + 10x - 12   (take the GCF out first)", "12x^2 + 10x - 12"),
        ("6x^2 - x - 2", "6x^2 - x - 2"),
    ],
    "special": [
        ("x^2 - 16   (difference of squares)", "x^2 - 16"),
        ("4x^2 - 9", "4x^2 - 9"),
        ("x^2 + 16   (a sum of squares)", "x^2 + 16"),
        ("x^2 + 10x + 25   (a perfect square)", "x^2 + 10x + 25"),
        ("x^3 - 8   (a difference of cubes)", "x^3 - 8"),
        ("x^4 - 16   (two passes)", "x^4 - 16"),
    ],
    "roots": [
        ("x^3 - 6x^2 + 11x - 6", "x^3 - 6x^2 + 11x - 6"),
        ("2x^3 - 3x^2 - 3x + 2   (a root with a denominator)", "2x^3 - 3x^2 - 3x + 2"),
        ("x^3 - 2   (the search comes back empty)", "x^3 - 2"),
        ("x^4 - 5x^2 + 4", "x^4 - 5x^2 + 4"),
        ("x^3 - x^2 - 8x + 12   (a repeated root)", "x^3 - x^2 - 8x + 12"),
        ("3x^3 + 2x^2 - 7x + 2   (eight candidates)", "3x^3 + 2x^2 - 7x + 2"),
    ],
}

FACTOR_TITLES = {
    "gcf": ("The common factor", "Divisor lists, intersected"),
    "grouping": ("Factoring by grouping", "All three pairings tried, not just the obvious one"),
    "trinomial": ("x^2 + bx + c", "Every pair that multiplies to c, with its sum"),
    "ac": ("ax^2 + bx + c", "The ac search, with every pair it tried"),
    "special": ("The special forms", "Four patterns tested against what you typed"),
    "roots": ("The rational root theorem", "Candidates generated from the divisors, then tested"),
}

FACTOR_KPIS = {
    "gcf": ["Common factor", "What is left", "Terms", "Multiplies back"],
    "grouping": ["Terms", "Pairings tried", "Pairing that worked", "Multiplies back"],
    "trinomial": ["b", "c", "The pair", "Multiplies back"],
    "ac": ["a &times; c", "Pairs tried", "The pair", "Multiplies back"],
    "special": ["Pattern", "Passes", "Factored form", "Multiplies back"],
    "roots": ["Candidates", "Roots found", "Factored form", "Multiplies back"],
}

FACTOR_PANEL_INTRO = {
    "gcf": "The lab lists the divisors of every coefficient and intersects them, so the greatest "
           "common factor is found rather than spotted. The second preset has nothing to take out.",
    "grouping": "All three ways of pairing four terms are tried and shown, including the ones that "
                "fail. Two of the presets cannot be factored by grouping at all &mdash; one of them "
                "still factors, which is the point.",
    "trinomial": "Every pair of integers multiplying to c is listed with its sum, and the one whose "
                 "sum is b is marked. When no pair works, the table is the proof.",
    "ac": "The ac method, with the search left in: every pair multiplying to a&middot;c, its sum, and "
          "whether that sum is b. Then the middle term is split and the four terms grouped.",
    "special": "Four patterns are tested against what you typed and each reports why it does or does "
               "not apply. A sum of squares fails all four, and the last preset needs two passes.",
    "roots": "The candidate list is built from the divisors of the constant and leading coefficients "
             "and then every candidate is evaluated. On the third preset the list runs out with "
             "nothing found, which is a result rather than a failure.",
}

FACTOR_LEGEND = ('<span class="tone-cyan"><i class="legend-swatch"></i>the polynomial</span>'
                 '<span class="tone-green"><i class="legend-swatch"></i>rational roots</span>'
                 '<span class="tone-muted"><i class="legend-swatch"></i>candidates that failed</span>')


def factoring_lab(cfg):
    """Factoring, with the search left in.

    The teaching decision: a factorisation is the END of a search, and this lab
    shows the search. Textbook factoring reads like magic because the pair of
    numbers that works appears without the twenty that did not; every mode here
    prints what it tried.

      gcf        intersects the divisor lists of the coefficients instead of
                 asserting a greatest common factor.
      grouping   tries all THREE ways of pairing four terms, shows the brackets
                 each pairing produces, and reports when none of them match --
                 including one preset that fails grouping and factors anyway.
      trinomial  lists every integer pair multiplying to c beside its sum.
      ac         does the same for a*c, then splits the middle term and groups,
                 so the reader sees why the ac trick is grouping in disguise.
      special    tests four named patterns against the reader's polynomial and
                 says why each does or does not apply. A sum of squares fails
                 all four, which is the lesson that pattern-matching has limits.
      roots      GENERATES the rational root candidates from the divisors of the
                 constant and leading coefficients, then TESTS each one, and on
                 x^3 - 2 the list runs out with nothing found.

    Every mode ends the same way: the factored form is multiplied back out and
    compared with what the reader typed. A factorisation that does not
    reproduce its own polynomial is not a factorisation, and the lab says so
    rather than hoping.
    """
    mode = cfg.get("mode", "gcf")
    if mode not in FACTOR_PRESETS:
        mode = "gcf"
    presets = cfg.get("presets") or FACTOR_PRESETS[mode]
    title, subtitle = FACTOR_TITLES[mode]
    first = presets[0]

    options = "".join('<option value="%s">%s</option>' % (value, label) for label, value in presets)
    kpi_cells = "".join(
        '<div class="kpi"><span>%s</span><strong id="fcK%d">&mdash;</strong></div>' % (label, i + 1)
        for i, label in enumerate(FACTOR_KPIS[mode])
    )

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="fcTitle">%s</strong><span id="fcSub"></span></div>
        <div class="inline-legend">%s</div>
      </div>
      <div class="lab-stage"><svg id="fcPlot"></svg></div>
      <div id="fcWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="fcStatus" style="margin-top:12px;"></div>""" % (
        title, FACTOR_LEGEND,
    )

    controls = """        <div class="field">
          <label for="fcPreset">Example</label>
          <select id="fcPreset">%s</select>
        </div>
        <div class="field">
          <label for="fcPoly">The polynomial</label>
          <input id="fcPoly" type="text" value="%s" inputmode="text" autocomplete="off">
        </div>
        <div class="kpi-grid">%s</div>
        <p class="small-copy" style="margin:0;">Type as you would write it: <code>6x^3 + 9x^2 - 15x</code>,
        <code>(1/2)x^2 + 3/4</code>. Every divisor list, every pair tried and every test below is
        computed in your browser from what is in this box.</p>""" % (options, first[1], kpi_cells)

    script = RATIONAL_JS + POLY_JS + EXPR_JS + SURD_JS + PLOT_JS + SHARED_JS + r"""
  var MODE = '""" + mode + r"""';
  var preset = document.getElementById('fcPreset');
  var inPoly = document.getElementById('fcPoly');
  var work = document.getElementById('fcWork'), status = document.getElementById('fcStatus');
  var titleOut = document.getElementById('fcTitle'), subOut = document.getElementById('fcSub');
  var svg = document.getElementById('fcPlot');
  var kpis = [document.getElementById('fcK1'), document.getElementById('fcK2'),
              document.getElementById('fcK3'), document.getElementById('fcK4')];

  function setKpis(values) {
    for (var i = 0; i < kpis.length; i += 1) {
      var v = values[i];
      kpis[i].innerHTML = (v === null || v === void 0 || v === '') ? '&mdash;' : v;
    }
  }
  function clearPlot() {
    svg.textContent = '';
    svg.setAttribute('aria-label', 'no picture yet: the input is incomplete');
  }
  function explain(msg, rows) {
    work.innerHTML = (rows && rows.length) ? table('Where it stopped', [], rows) : '';
    clearPlot();
    setKpis([]);
    status.innerHTML = msg;
  }
  function powerName(e) { return e === 0 ? 'constant' : (e === 1 ? 'x' : 'x^' + e); }

  /* ---- the check every mode ends with ---- */
  /* A factorisation is a claim that a product equals the original. The claim is
     tested here by making the product and subtracting, every time, on whatever
     the reader typed -- not on the examples this file was written against. */
  function expandBack(pieces) {
    var acc = [R1];
    pieces.forEach(function (f) { acc = Pmul(acc, f); });
    return acc;
  }
  function factoredText(pieces) {
    var real = pieces.filter(function (f) { return !(Pdeg(f) === 0 && Requ(Plead(f), R1)); });
    if (!real.length) return '1';
    /* A content of -1 is a minus sign, not a factor called "-1". */
    if (real.length > 1 && Pdeg(real[0]) === 0 && Requ(Plead(real[0]), R(-1n))) {
      var tail = '';
      real.slice(1).forEach(function (f) { tail += Pfactortext(f); });
      return '-' + tail;
    }
    /* A polynomial that did not factor is written as itself. Bracketing a lone
       factor says something was multiplied by something, which is the opposite
       of what that result means. */
    if (real.length === 1) return Ptext(real[0]);
    var out = '';
    real.forEach(function (f) { out += Pfactortext(f); });
    return out;
  }
  function verifyRows(pieces, original) {
    var back = expandBack(pieces), ok = Psame(back, original);
    return [
      say('the factored form', factoredText(pieces)),
      say('multiplied back out', Ptext(back)),
      say('compared with what you typed', Ptext(original) + ' '
        + chip(ok, ok ? 'the same polynomial' : 'NOT the same polynomial &mdash; the factorisation is wrong'))
    ];
  }
  function verified(pieces, original) { return Psame(expandBack(pieces), original); }

  /* ---- the picture: the curve, its rational roots, and (in the rational
     root mode) every candidate that was tested and failed ---- */
  function paintPlot(p, candidates) {
    var fn = Pfn(p), roots = Prationalroots(p), marks = [];
    roots.forEach(function (r) { if (Math.abs(Rnum(r)) <= 8) marks.push(Rnum(r)); });
    (candidates || []).forEach(function (c) { if (Math.abs(Rnum(c)) <= 6) marks.push(Rnum(c)); });
    if (!marks.length) { marks = [-3, 3]; }
    var plot = Plot(svg, viewFor([fn], marks));
    plot.frame().curve(fn);
    (candidates || []).forEach(function (c) {
      var isRoot = roots.some(function (r) { return Requ(r, c); });
      if (!isRoot) plot.hole(Rnum(c), 0);
    });
    roots.forEach(function (r) { plot.point(Rnum(r), 0, 'plot-point root', Rtext(r)); });
    plot.describe(Ptext(p) + ' sampled at 480 points'
      + (roots.length ? ', with its rational roots marked on the axis where the curve crosses'
                      : ': it has no rational root, and any crossing you can see is at an irrational x')
      + ((candidates && candidates.length) ? '. The hollow circles are candidates that were tested and failed.' : '.'));
  }

  /* ---- the divisor list a reader would write out ---- */
  function divisorList(n) {
    var d = bdivisors(n < 0n ? -n : n);
    return d.map(function (v) { return String(v); });
  }
  /* Every unordered pair of integers whose product is `target`, in the order a
     reader would try them: smallest magnitude first, both signs. */
  function factorPairs(target) {
    var out = [], divs = bdivisors(target < 0n ? -target : target);
    divs.forEach(function (d) {
      [d, -d].forEach(function (m) {
        var n = target / m;
        if (m * n !== target) return;
        if (m > n) return;                     /* (m, n) and (n, m) are one pair */
        out.push({ m: m, n: n });
      });
    });
    out.sort(function (a, b) { return a.m < b.m ? -1 : (a.m > b.m ? 1 : 0); });
    return out;
  }
"""

    script += r"""
  /* ----------------------------------------------------------- mode: gcf */
  function modeGcf() {
    var read = readPoly(inPoly, 'The polynomial');
    if (!read.ok) {
      explain('<strong>Nothing to factor yet.</strong> ' + read.why,
        [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly, terms = Pterms(p);
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'what divides every term?';
    if (!terms.length) {
      explain('<strong>That is the zero polynomial.</strong> Every polynomial divides it, so there is '
        + 'no greatest common factor to find: 0 = 5x(0) = x^7(0) and so on forever. Type something '
        + 'with a term in it.', [say('you typed', shownInput(inPoly)), say('as a polynomial', '0')]);
      return;
    }

    /* Denominators first: divisors are a statement about integers, so a
       polynomial with fractional coefficients is scaled up, the search is run,
       and the scaling is put back into the common factor at the end. */
    var den = 1n;
    terms.forEach(function (t) { den = den * t.c.d / bgcd(den, t.c.d); });
    var ints = terms.map(function (t) { return t.c.n * (den / t.c.d); });
    var lists = ints.map(function (v) { return divisorList(v); });
    var common = lists[0].filter(function (v) {
      return lists.every(function (L) { return L.indexOf(v) >= 0; });
    });
    var gInt = 0n;
    ints.forEach(function (v) { gInt = bgcd(gInt, v); });

    var g = monoGcf(p);
    var gcfPoly = [];
    for (var i = 0; i < g.e; i += 1) gcfPoly.push(R0);
    gcfPoly.push(g.c);
    var searchAgrees = Requ(Rabs(g.c), R(gInt, den));

    var divisorRows = terms.map(function (t, k) {
      return rowOf([
        '<th class="rowhead">' + Pmono(t.c, t.e) + '</th>',
        cell(Rtext(t.c) + (den === 1n ? '' : ' &rarr; ' + ints[k])),
        cell(lists[k].join(', ')),
        cell(String(t.e))
      ]);
    });
    var lowest = terms[terms.length - 1].e;

    var searchRows = [
      say('divisors of every coefficient', common.join(', ') + ' &mdash; the numbers in all '
        + terms.length + ' lists above'),
      say('the greatest of them', String(gInt) + (den === 1n ? ''
        : ', over the common denominator ' + den + ', so the numerical factor is ' + Rtext(R(gInt, den)))),
      say('lowest power of x present', lowest === 0
        ? 'x^0 &mdash; one term has no x at all, so no power of x is common'
        : powerName(lowest) + ' &mdash; every term has at least that many factors of x'),
      say('sign', Rsign(g.c) < 0
        ? 'the leading coefficient is negative, so the minus comes out too: it leaves the bracket '
          + 'starting with a positive term, which is the form every later method expects'
        : 'the leading coefficient is positive, so the common factor is taken positive'),
      say('the common factor', gcfText(g) + ' ' + chip(searchAgrees,
        searchAgrees ? 'the divisor search and the content routine agree' : 'the two disagree'))
    ];

    var trivial = Requ(Rabs(g.c), R1) && g.e === 0;
    var blocks = [
      table('Every term, and what divides it', ['term', 'coefficient', 'its divisors', 'power of x'], divisorRows),
      table('Intersecting the lists', [], searchRows),
      table('The factorisation', [], verifyRows([gcfPoly, g.rest], p))
    ];
    work.innerHTML = blocks.join('');
    setKpis([gcfText(g), Ptext(g.rest), String(terms.length),
             chip(verified([gcfPoly, g.rest], p), verified([gcfPoly, g.rest], p) ? 'yes' : 'no')]);
    paintPlot(p, []);

    status.innerHTML = trivial
      ? '<strong>There is nothing to take out.</strong> The divisor lists above have only 1 in common '
        + 'and ' + (lowest === 0 ? 'the constant term has no x' : 'not every term has an x')
        + ', so the greatest common factor of ' + Ptext(p) + ' is 1. That is a result, not a dead end: '
        + 'it says this polynomial is already primitive, and any factorisation of it has to come from '
        + 'one of the other methods.'
      : '<strong>' + Ptext(p) + ' = ' + gcfText(g) + '(' + Ptext(g.rest) + ').</strong> '
        + 'The common factor was found by listing the divisors of each coefficient and intersecting '
        + 'the lists &mdash; ' + common.join(', ') + ' survived, and ' + gInt + ' is the largest '
        + '&mdash; then taking the lowest power of x that appears in every term. '
        + (Rsign(g.c) < 0 ? 'The minus came out with it, which is why the bracket starts positive. '
                          : '')
        + 'Taking the common factor out first is not politeness: every method after this one assumes '
        + 'it has been done.';
  }

  /* ------------------------------------------------------ mode: grouping */
  function modeGrouping() {
    var read = readPoly(inPoly, 'The polynomial');
    if (!read.ok) {
      explain('<strong>Nothing to group yet.</strong> ' + read.why,
        [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly, terms = Pterms(p);
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'four terms, three ways to pair them';

    if (terms.length !== 4) {
      var full = Pfactortextfull(p);
      explain('<strong>Grouping is the method for four terms; this has ' + terms.length + '.</strong> '
        + (terms.length < 4
            ? 'With two terms try the special forms, and with three the trinomial or ac method. '
            : 'With more than four terms, take out a common factor first and see what is left. ')
        + 'For the record, the full factorisation over the rationals of ' + Ptext(p) + ' is '
        + full + ', found by the rational root search rather than by grouping.',
        [say('you typed', shownInput(inPoly)), say('as a polynomial', Ptext(p)),
         say('terms', String(terms.length)), say('factored over the rationals', full)]);
      return;
    }

    function monoPoly(t) {
      var arr = [];
      for (var i = 0; i < t.e; i += 1) arr.push(R0);
      arr.push(t.c);
      return arr;
    }
    var pairings = [[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]];
    var attempts = pairings.map(function (pair) {
      var first = Padd(monoPoly(terms[pair[0][0]]), monoPoly(terms[pair[0][1]]));
      var second = Padd(monoPoly(terms[pair[1][0]]), monoPoly(terms[pair[1][1]]));
      var g1 = monoGcf(first), g2 = monoGcf(second);
      return { first: first, second: second, g1: g1, g2: g2, match: Psame(g1.rest, g2.rest) };
    });
    var winner = null;
    attempts.forEach(function (att) { if (!winner && att.match) winner = att; });

    var attemptRows = attempts.map(function (att, i) {
      return rowOf([
        '<th class="rowhead">' + ['terms 1,2 and 3,4', 'terms 1,3 and 2,4', 'terms 1,4 and 2,3'][i] + '</th>',
        cell(Ptext(att.first) + ' = ' + gcfText(att.g1) + '(' + Ptext(att.g1.rest) + ')'),
        cell(Ptext(att.second) + ' = ' + gcfText(att.g2) + '(' + Ptext(att.g2.rest) + ')'),
        cell(att.match ? chip(true, 'both brackets are (' + Ptext(att.g1.rest) + ')')
                       : chip(false, '(' + Ptext(att.g1.rest) + ') is not (' + Ptext(att.g2.rest) + ')'),
             att.match ? 't' : 'f')
      ], att.match ? 'focus' : '');
    });

    var blocks = [table('The three pairings, all of them tried',
      ['pairing', 'first pair', 'second pair', 'do the brackets match?'], attemptRows)];

    if (winner) {
      var gcf1 = [], gcf2 = [], i;
      for (i = 0; i < winner.g1.e; i += 1) gcf1.push(R0);
      gcf1.push(winner.g1.c);
      for (i = 0; i < winner.g2.e; i += 1) gcf2.push(R0);
      gcf2.push(winner.g2.c);
      var outer = Padd(gcf1, gcf2), pieces = [winner.g1.rest, outer];
      /* The second common factor is often negative, and "+ -3(x + 2)" is the
         notation this whole lab exists to discourage. */
      var negSecond = Rsign(winner.g2.c) < 0;
      var joiner = negSecond ? ' - ' : ' + ';
      var mag2 = gcfText({ c: Rabs(winner.g2.c), e: winner.g2.e });
      blocks.push(table('Finishing the grouping', [], [
        say('the two pieces', gcfText(winner.g1) + '(' + Ptext(winner.g1.rest) + ')' + joiner
          + mag2 + '(' + Ptext(winner.g2.rest) + ')'),
        say('the common bracket', '(' + Ptext(winner.g1.rest) + ') appears in both, so it comes out'),
        say('what is left', gcfText(winner.g1) + joiner + mag2 + ' = ' + Ptext(outer))
      ]));
      blocks.push(table('The factorisation', [], verifyRows(pieces, p)));
      work.innerHTML = blocks.join('');
      setKpis([String(terms.length), '3', Ptext(winner.g1.rest),
               chip(verified(pieces, p), verified(pieces, p) ? 'yes' : 'no')]);
      paintPlot(p, []);
      status.innerHTML = '<strong>' + Ptext(p) + ' = ' + factoredText(pieces) + '.</strong> '
        + 'Grouping worked because one pairing left the same bracket on both sides: '
        + gcfText(winner.g1) + '(' + Ptext(winner.g1.rest) + ') and ' + gcfText(winner.g2)
        + '(' + Ptext(winner.g1.rest) + ') share (' + Ptext(winner.g1.rest) + '), and a factor shared '
        + 'by both halves is a factor of the whole. '
        + (Rsign(winner.g2.c) < 0
            ? 'Notice the second common factor came out NEGATIVE: taking out ' + Rtext(winner.g2.c)
              + ' rather than ' + Rtext(Rabs(winner.g2.c)) + ' is what made the brackets match, and '
              + 'forgetting that sign is the commonest way this method fails in a reader\'s hands.'
            : 'The pairing that works is not always the first one, which is why all three are shown.');
      return;
    }

    /* No pairing works. Whether the polynomial factors AT ALL is a different
       question, and the rational root search answers it. */
    var f = Pfactor(p), full = Pfactortextfull(p);
    var factorsAnyway = f.factors.length > 0;
    blocks.push(table('No pairing works. Does it factor at all?', [], [
      say('what grouping needs', 'two pairs whose leftover brackets are identical. None of the three '
        + 'pairings above produced that.'),
      say('the rational root search says', factorsAnyway
        ? Ptext(p) + ' = ' + full + ' &mdash; so it DOES factor; grouping is simply not the method that finds it'
        : Ptext(p) + ' has no rational root, so it has no factor of the form (qx - p) over the rationals at all'),
      say('the lesson', factorsAnyway
        ? 'Grouping is a pattern that works when the polynomial happens to have that shape. It is not '
          + 'a test for factorability, and a failed grouping proves nothing.'
        : 'Here grouping failed for the honest reason: there is nothing to find.')
    ]));
    work.innerHTML = blocks.join('');
    setKpis([String(terms.length), '3', 'none', factorsAnyway ? 'not by grouping' : 'nothing to check']);
    paintPlot(p, []);
    var settled = Pdeg(f.rest) <= 3;
    status.innerHTML = factorsAnyway
      ? '<strong>Grouping fails here, and the polynomial still factors.</strong> All three pairings '
        + 'left mismatched brackets, but ' + Ptext(p) + ' = ' + full + '. That combination is worth '
        + 'meeting early: a method that comes back empty has told you about the METHOD, not about the '
        + 'polynomial. The rational root search is what settles it.'
      : '<strong>Grouping fails, and nothing else would have worked either.</strong> All three '
        + 'pairings left mismatched brackets, and the rational root search finds no root. '
        + (settled
          ? 'At degree ' + Pdegtext(p) + ' that settles it: a polynomial of this degree that factors '
            + 'at all must have a linear factor, and there is none, so ' + Ptext(p) + ' does not '
            + 'factor over the rationals.'
          : 'That rules out every linear factor, though at degree ' + Pdegtext(p) + ' it does not rule '
            + 'out a split into two factors of degree 2 or more.')
        + ' The curve above still crosses the axis, so there IS a real root &mdash; an irrational one, '
        + 'and irrational roots are exactly the ones no amount of grouping will reveal.';
  }
"""

    script += r"""
  /* A monomial as a polynomial, used by the pattern tests below. */
  function monoPoly(c, e) {
    var arr = [];
    for (var i = 0; i < e; i += 1) arr.push(R0);
    arr.push(c);
    return arr;
  }
  /* What the rational root search can and cannot settle. It finds LINEAR
     factors over Q. A leftover of degree 2 or 3 with no rational root really is
     irreducible over Q -- any factorisation would have to include a linear
     factor -- but a leftover of degree 4 or more may still split into two
     quadratics, and saying otherwise would be a lie the reader cannot check. */
  function searchVerdict(p) {
    var f = Pfactor(p);
    return {
      text: Pfactortextfull(p),
      rest: f.rest,
      settled: Pdeg(f.rest) <= 3,
      linear: f.factors.length
    };
  }

  /* What the roots of a quadratic actually are, in the four cases the
     discriminant distinguishes. Calling a rational root irrational because the
     search that was run happened to miss it is the error this exists to stop. */
  function rootsSentence(r) {
    if (r.kind === 'complex') return 'x = ' + pmtext(r.p, r.s, true)
      + ' &mdash; not real at all, so the curve below never meets the axis';
    if (r.kind === 'double') return 'x = ' + Rtext(r.p)
      + ', twice &mdash; a repeated rational root, and the curve touches the axis without crossing';
    if (r.kind === 'rational') return 'x = ' + r.roots.map(Rtext).join(' and ')
      + ' &mdash; both rational, so this quadratic does factor over the rationals';
    return 'x = ' + pmtext(r.p, r.s) + ' &mdash; real and irrational, and no bracket with whole '
      + 'numbers in it can produce an irrational root';
  }

  /* --------------------------------------------------- mode: x^2 + bx + c */
  function modeTrinomial() {
    var read = readPoly(inPoly, 'The trinomial');
    if (!read.ok) {
      explain('<strong>Nothing to factor yet.</strong> ' + read.why, [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly;
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'two numbers multiplying to c, adding to b';

    if (Pdeg(p) !== 2) {
      var v = searchVerdict(p);
      explain('<strong>This method is for a quadratic; ' + Ptext(p) + ' has degree ' + Pdegtext(p)
        + '.</strong> The pair search below only makes sense for x^2 + bx + c, because it comes from '
        + 'multiplying (x + m)(x + n) out. For what you typed, the rational root search gives '
        + v.text + '.',
        [say('you typed', shownInput(inPoly)), say('degree', Pdegtext(p)),
         say('what the root search finds', v.text)]);
      return;
    }
    var a = p[2], b = p[1] || R0, c = p[0] || R0;
    if (!Rint(b) || !Rint(c) || !Rint(a)) {
      explain('<strong>The pair search is a search over whole numbers.</strong> Here b = ' + Rtext(b)
        + ' and c = ' + Rtext(c) + ', so multiply through by the common denominator first, factor the '
        + 'whole-number trinomial that leaves, and put the fraction back at the front.',
        [say('a', Rtext(a)), say('b', Rtext(b)), say('c', Rtext(c))]);
      return;
    }
    var monic = Requ(a, R1);

    if (Rzero(c)) {
      var pieces0 = [[R0, R1], [b, R1]];
      work.innerHTML = table('c is zero, so x itself is a factor', [], [
        say('what you typed', Ptext(p)),
        say('every term has an x', Ptext(p) + ' = x(' + Ptext([b, a]) + ')'),
        say('no pair search needed', 'the pair search looks for m*n = c, and with c = 0 one of them '
          + 'would have to be 0: that is the factor x, and it is quicker to take it out first')
      ]) + table('The factorisation', [], verifyRows([[R0, R1], [b, a]], p));
      setKpis([Rtext(b), '0', 'x and ' + Ptext([b, a]),
               chip(verified([[R0, R1], [b, a]], p), 'yes')]);
      paintPlot(p, []);
      status.innerHTML = '<strong>With c = 0 the factorisation is immediate: ' + Ptext(p) + ' = x('
        + Ptext([b, a]) + ').</strong> A trinomial with no constant term is really a binomial with a '
        + 'common factor, and taking x out is the first move on every polynomial before any pattern '
        + 'is tried.';
      return;
    }

    var pairs = factorPairs(c.n), hit = null;
    var pairRows = pairs.map(function (pr) {
      var sum = pr.m + pr.n, works = sum === b.n;
      if (works && !hit) hit = pr;
      return rowOf([
        cell(String(pr.m)), cell(String(pr.n)),
        cell(String(pr.m * pr.n)),
        cell(String(sum), works ? 't' : ''),
        cell(works ? chip(true, 'this is b') : muted('not b = ' + Rtext(b)))
      ], works ? 'focus' : '');
    });
    if (!pairRows.length) {
      pairRows.push(rowOf([cell('&mdash;'), cell('&mdash;'), cell('&mdash;'), cell('&mdash;'),
                           cell('there are no integer pairs to try')]));
    }

    var blocks = [];
    if (!monic) {
      blocks.push(table('This method assumes a = 1, and here a = ' + Rtext(a), [], [
        say('why it matters', '(x + m)(x + n) always has a leading coefficient of 1. With a = '
          + Rtext(a) + ' the pair search below is being run on the wrong equation &mdash; watch it '
          + 'either come back empty or produce brackets that do not multiply back to what you typed.'),
        say('the method that does apply', 'the ac method: search for m*n = a*c = '
          + Rtext(Rmul(a, c)) + ' instead of m*n = c = ' + Rtext(c))
      ]));
    }
    blocks.push(table('Every pair of whole numbers multiplying to c = ' + Rtext(c),
      ['m', 'n', 'm &times; n', 'm + n', 'is the sum b = ' + Rtext(b) + '?'], pairRows));

    var pieces = null;
    if (hit) {
      pieces = [[R(hit.m), R1], [R(hit.n), R1]];
      blocks.push(table('The pair that worked', [], [
        say('m and n', hit.m + ' and ' + hit.n),
        say('why those two', intTerm(hit.m) + ' * ' + intTerm(hit.n) + ' = ' + Rtext(c) + ' and '
          + intTerm(hit.m) + ' + ' + intTerm(hit.n) + ' = ' + Rtext(b) + ', which is exactly what '
          + 'multiplying (x + m)(x + n) out produces: x^2 + (m + n)x + mn'),
        say('so', Pfactortext([R(hit.m), R1]) + Pfactortext([R(hit.n), R1]))
      ]));
      blocks.push(table('The check', [], verifyRows(pieces, p)));
    } else {
      var r = quadroots(a, b, c);
      var perfect = Rsign(r.disc) >= 0 && Rsurd(r.disc).k === 1n;
      blocks.push(table('The search came back empty', [], [
        say('pairs tried', String(pairs.length)),
        say('why that settles it', monic
          ? 'for a monic trinomial with whole-number coefficients, any rational root is a whole number '
            + 'dividing c. Every one of those was tried above, so there is no factorisation over the '
            + 'rationals at all.'
          : 'nothing at all &mdash; this search was the wrong one to run for a = ' + Rtext(a) + '. It '
            + 'looked for the middle coefficient of a MONIC trinomial, and this one is not monic.'),
        say('the discriminant', 'b^2 - 4ac = ' + Rtext(r.disc) + ', '
          + (perfect ? 'a perfect square' : 'not a perfect square') + ' &mdash; '
          + (monic
            ? chip(perfect === false, 'and for a = 1 that is the same statement as "no integer pair works"')
            : 'and a perfect square here means ' + Ptext(p) + ' DOES factor over the rationals, as '
              + Pfactortextfull(p) + '. The pair search missed it because it was searching for the '
              + 'wrong product.')),
        say('the exact roots', rootsSentence(r))
      ]));
    }
    work.innerHTML = blocks.join('');
    setKpis([Rtext(b), Rtext(c), hit ? hit.m + ' and ' + hit.n : 'none',
             pieces ? chip(verified(pieces, p), verified(pieces, p) ? 'yes' : 'no') : '&mdash;']);
    paintPlot(p, []);

    status.innerHTML = hit
      ? (verified(pieces, p)
        ? '<strong>' + Ptext(p) + ' = ' + factoredText(pieces) + '.</strong> '
          + 'The search tried ' + pairs.length + ' pair' + (pairs.length === 1 ? '' : 's')
          + ' and kept the one where the product was c = ' + Rtext(c) + ' and the sum was b = '
          + Rtext(b) + '. Both conditions matter: the product alone leaves several candidates, and '
          + 'the sum is what picks between them.'
        : '<strong>The pair search found ' + hit.m + ' and ' + hit.n + ', and the brackets it built '
          + 'are wrong.</strong> ' + factoredText(pieces) + ' = '
          + Ptext(expandBack(pieces)) + ', which is not ' + Ptext(p) + '. That is what a = ' + Rtext(a)
          + ' does to this method: the search is looking for the middle coefficient of a MONIC '
          + 'trinomial. Use the ac method.')
      : '<strong>No pair of whole numbers multiplies to ' + Rtext(c) + ' and adds to ' + Rtext(b)
        + '.</strong> ' + pairs.length + ' pair' + (pairs.length === 1 ? ' was' : 's were')
        + ' tried and every sum missed. '
        + (monic ? 'For a monic trinomial that is conclusive: it does not factor over the rationals, '
                 + 'and the exact roots are irrational or complex rather than nonexistent.'
                 : 'With a = ' + Rtext(a) + ' this search was the wrong one to run: the ac method '
                 + 'searches for a product of a*c = ' + Rtext(Rmul(a, c)) + ' instead, and it finds '
                 + Ptext(p) + ' = ' + Pfactortextfull(p) + '.');
  }

  /* -------------------------------------------------- mode: ax^2 + bx + c */
  function modeAc() {
    var read = readPoly(inPoly, 'The trinomial');
    if (!read.ok) {
      explain('<strong>Nothing to factor yet.</strong> ' + read.why, [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly;
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'two numbers multiplying to a*c, adding to b';

    if (Pdeg(p) !== 2) {
      var v = searchVerdict(p);
      explain('<strong>The ac method is for a quadratic; ' + Ptext(p) + ' has degree ' + Pdegtext(p)
        + '.</strong> It comes from splitting the middle term of ax^2 + bx + c, and a polynomial with '
        + 'no single middle term has nothing to split. The rational root search gives ' + v.text + '.',
        [say('you typed', shownInput(inPoly)), say('degree', Pdegtext(p)),
         say('what the root search finds', v.text)]);
      return;
    }

    /* The common factor comes out first, always. Skipping it is what turns a
       six-pair search into a thirty-pair search. */
    var g = monoGcf(p), core = g.rest;
    var gcfPoly = [];
    for (var i = 0; i < g.e; i += 1) gcfPoly.push(R0);
    gcfPoly.push(g.c);
    var pulled = !(Requ(g.c, R1) && g.e === 0);
    var a = core[2], b = core[1] || R0, c = core[0] || R0;
    var ac = a.n * c.n;

    var blocks = [table('First: is there a common factor?', [], [
      say('the polynomial', Ptext(p)),
      say('common factor', pulled ? gcfText(g) + ', so ' + Ptext(p) + ' = ' + gcfText(g) + '('
            + Ptext(core) + ') and the search below runs on the bracket'
          : '1 &mdash; nothing to take out, so the search runs on ' + Ptext(core)),
      say('a, b, c', 'a = ' + Rtext(a) + ', b = ' + Rtext(b) + ', c = ' + Rtext(c)),
      say('a times c', Rtext(a) + ' * ' + Rterm(c) + ' = ' + ac)
    ])];

    if (Rzero(c) || Rzero(a)) {
      blocks.push(table('Nothing left to search for', [], [
        say('why', 'after the common factor came out there is no constant term, so the factorisation '
          + 'is already finished')
      ]));
      blocks.push(table('The factorisation', [], verifyRows([gcfPoly, core], p)));
      work.innerHTML = blocks.join('');
      setKpis([String(ac), '0', 'not needed', chip(verified([gcfPoly, core], p), 'yes')]);
      paintPlot(p, []);
      status.innerHTML = '<strong>The common factor finished the job.</strong> ' + Ptext(p) + ' = '
        + factoredText([gcfPoly, core]) + ', and no pair search was needed.';
      return;
    }

    var pairs = factorPairs(ac), hit = null;
    var pairRows = pairs.map(function (pr) {
      var sum = pr.m + pr.n, works = sum === b.n;
      if (works && !hit) hit = pr;
      return rowOf([
        cell(String(pr.m)), cell(String(pr.n)), cell(String(pr.m * pr.n)),
        cell(String(sum), works ? 't' : ''),
        cell(works ? chip(true, 'this is b') : muted('not b = ' + Rtext(b)))
      ], works ? 'focus' : '');
    });
    blocks.push(table('Every pair multiplying to a*c = ' + ac,
      ['m', 'n', 'm &times; n', 'm + n', 'is the sum b = ' + Rtext(b) + '?'], pairRows));

    /* The discriminant answers the same question a completely different way. */
    var r = quadroots(a, b, c);
    var perfect = Rsign(r.disc) >= 0 && Rsurd(r.disc).k === 1n;
    var pieces = null;

    if (hit) {
      var m = R(hit.m), n = R(hit.n);
      var first = Padd(monoPoly(a, 2), monoPoly(m, 1));      /* ax^2 + mx */
      var second = Padd(monoPoly(n, 1), monoPoly(c, 0));     /* nx + c    */
      var g1 = monoGcf(first), g2 = monoGcf(second);
      var gp1 = [], gp2 = [], k;
      for (k = 0; k < g1.e; k += 1) gp1.push(R0);
      gp1.push(g1.c);
      for (k = 0; k < g2.e; k += 1) gp2.push(R0);
      gp2.push(g2.c);
      var matched = Psame(g1.rest, g2.rest);
      pieces = matched ? [gcfPoly, g1.rest, Padd(gp1, gp2)] : null;
      blocks.push(table('Split the middle term, then group', [], [
        say('the pair', hit.m + ' and ' + hit.n + ': ' + intTerm(hit.m) + ' * ' + intTerm(hit.n)
          + ' = ' + ac + ' and ' + intTerm(hit.m) + ' + ' + intTerm(hit.n) + ' = ' + Rtext(b)),
        say('rewrite bx', Ptext(core) + ' = '
          + joinTerms([{ c: a, e: 2 }, { c: m, e: 1 }, { c: n, e: 1 }, { c: c, e: 0 }])
          + ' &mdash; the same polynomial, four terms instead of three'),
        say('group in pairs', '(' + Ptext(first) + ') + (' + Ptext(second) + ')'),
        say('take the common factor out of each', gcfText(g1) + '(' + Ptext(g1.rest) + ')'
          + (Rsign(g2.c) < 0 ? ' - ' : ' + ') + gcfText({ c: Rabs(g2.c), e: g2.e })
          + '(' + Ptext(g2.rest) + ')'),
        say('do the brackets match?', chip(matched, matched ? 'yes, both are (' + Ptext(g1.rest) + ')'
          : 'no &mdash; which would mean the split was wrong')),
        say('so', matched ? '(' + Ptext(g1.rest) + ')(' + Ptext(Padd(gp1, gp2)) + ')'
          : 'the grouping did not close')
      ]));
      if (pieces) blocks.push(table('The check', [], verifyRows(pieces, p)));
    } else {
      blocks.push(table('The search came back empty', [], [
        say('pairs tried', String(pairs.length) + ', every pair of whole numbers whose product is ' + ac),
        say('the discriminant', 'b^2 - 4ac = ' + Rtext(r.disc) + ', which is '
          + (perfect ? 'a perfect square' : 'not a perfect square')),
        say('the two tests agree', chip(!perfect, !perfect
          ? 'no pair, and no perfect square: both say the same thing'
          : 'a pair should exist &mdash; that would be a bug')
          + ' &mdash; a pair (m, n) with m + n = b and mn = ac exists exactly when b^2 - 4ac is a '
          + 'perfect square, because m and n are the roots of t^2 - bt + ac'),
        say('the exact roots', rootsSentence(r))
      ]));
    }
    work.innerHTML = blocks.join('');
    setKpis([String(ac), String(pairs.length), hit ? hit.m + ' and ' + hit.n : 'none',
             pieces ? chip(verified(pieces, p), verified(pieces, p) ? 'yes' : 'no') : '&mdash;']);
    paintPlot(p, []);

    status.innerHTML = pieces
      ? '<strong>' + Ptext(p) + ' = ' + factoredText(pieces) + '.</strong> '
        + 'The ac method is factoring by grouping in disguise: ' + pairs.length + ' pair'
        + (pairs.length === 1 ? ' was' : 's were') + ' tried against a*c = ' + ac + ', the pair '
        + hit.m + ' and ' + hit.n + ' split the middle term into two, and the four terms that left '
        + 'grouped into a common bracket. '
        + (pulled ? 'Taking the common factor ' + gcfText(g) + ' out first is what kept the search '
                  + 'this short.' : '')
      : '<strong>No pair of whole numbers multiplies to ' + ac + ' and adds to ' + Rtext(b) + '.</strong> '
        + 'All ' + pairs.length + ' were tried above. The discriminant says the same thing from the '
        + 'other side: b^2 - 4ac = ' + Rtext(r.disc) + ' is not a perfect square, and those two '
        + 'statements are equivalent. ' + Ptext(core) + ' does not factor over the rationals; its '
        + 'roots are ' + (r.kind === 'complex' ? 'not real at all' : 'real but irrational')
        + ', and no arrangement of whole numbers in brackets can produce them.';
  }
"""

    script += r"""
  /* ------------------------------------------------- mode: special forms */
  /* Each of these is a TEST, not a lookup: it either produces the two brackets
     and a reason, or it produces the reason it does not apply. The reason is
     the part worth reading -- "the middle term would have to be 12x and it is
     10x" is what tells a reader why the pattern nearly fitted. */
  function testDiffSquares(p) {
    var name = 'difference of squares', form = 'A^2 - B^2 = (A - B)(A + B)';
    var t = Pterms(p);
    if (t.length !== 2) return { name: name, form: form, ok: false,
      why: 'it needs exactly two terms, and this has ' + t.length };
    var hi = t[0], lo = t[1];
    if (!(Rsign(hi.c) > 0 && Rsign(lo.c) < 0)) return { name: name, form: form, ok: false,
      why: 'it needs a square MINUS a square; here the two coefficients are ' + Rtext(hi.c)
        + ' and ' + Rtext(lo.c) };
    if (hi.e % 2 !== 0 || lo.e % 2 !== 0) return { name: name, form: form, ok: false,
      why: 'the powers ' + powerName(hi.e) + ' and ' + powerName(lo.e) + ' are not both even, so the '
        + 'terms are not squares of monomials' };
    var A = Rsqrt(hi.c), B = Rsqrt(Rneg(lo.c));
    if (A === null || B === null) return { name: name, form: form, ok: false,
      why: Rtext(hi.c) + ' and ' + Rtext(Rneg(lo.c)) + ' are not both perfect squares' };
    var Ap = monoPoly(A, hi.e / 2), Bp = monoPoly(B, lo.e / 2);
    return { name: name, form: form, ok: true, pieces: [Psub(Ap, Bp), Padd(Ap, Bp)],
      why: 'A = ' + Ptext(Ap) + ' and B = ' + Ptext(Bp) + ', since A^2 = ' + Ptext(Pmul(Ap, Ap))
        + ' and B^2 = ' + Ptext(Pmul(Bp, Bp)) };
  }
  function testSumSquares(p) {
    var name = 'sum of squares', form = 'A^2 + B^2 = no (A - B)(A + B) factorisation';
    var t = Pterms(p);
    if (t.length !== 2 || Rsign(t[0].c) <= 0 || Rsign(t[1].c) <= 0
        || t[0].e % 2 !== 0 || t[1].e % 2 !== 0
        || Rsqrt(t[0].c) === null || Rsqrt(t[1].c) === null) {
      return { name: name, form: form, ok: false, why: 'this is not a sum of two squares' };
    }
    return { name: name, form: form, ok: false, recognised: true,
      why: 'this IS a sum of two squares, ' + Ptext(monoPoly(Rsqrt(t[0].c), t[0].e / 2)) + ' squared plus '
        + Ptext(monoPoly(Rsqrt(t[1].c), t[1].e / 2)) + ' squared, and there is no difference-of-squares '
        + 'factorisation of it. The minus sign in A^2 - B^2 is the whole pattern.' };
  }
  function testPerfectSquare(p) {
    var name = 'perfect square trinomial', form = 'A^2 +- 2AB + B^2 = (A +- B)^2';
    var t = Pterms(p);
    if (t.length !== 3) return { name: name, form: form, ok: false,
      why: 'it needs exactly three terms, and this has ' + t.length };
    var hi = t[0], mid = t[1], lo = t[2];
    if (Rsign(hi.c) < 0 || Rsign(lo.c) < 0) return { name: name, form: form, ok: false,
      why: 'the first and last terms are squares, so both must be positive; here they are '
        + Rtext(hi.c) + ' and ' + Rtext(lo.c) };
    if (hi.e % 2 !== 0 || lo.e % 2 !== 0) return { name: name, form: form, ok: false,
      why: 'the outer powers ' + powerName(hi.e) + ' and ' + powerName(lo.e) + ' are not both even' };
    var A = Rsqrt(hi.c), B = Rsqrt(lo.c);
    if (A === null || B === null) return { name: name, form: form, ok: false,
      why: Rtext(hi.c) + ' and ' + Rtext(lo.c) + ' are not both perfect squares' };
    var Ap = monoPoly(A, hi.e / 2), Bp = monoPoly(B, lo.e / 2);
    var plus = Padd(Ap, Bp), minus = Psub(Ap, Bp);
    if (Psame(Pmul(plus, plus), p)) return { name: name, form: form, ok: true, pieces: [plus, plus],
      why: 'A = ' + Ptext(Ap) + ', B = ' + Ptext(Bp) + ', and the middle term 2AB = '
        + Ptext(Pscale(Pmul(Ap, Bp), R(2n))) + ' is exactly what you typed' };
    if (Psame(Pmul(minus, minus), p)) return { name: name, form: form, ok: true, pieces: [minus, minus],
      why: 'A = ' + Ptext(Ap) + ', B = ' + Ptext(Bp) + ', and the middle term -2AB = '
        + Ptext(Pscale(Pmul(Ap, Bp), R(-2n))) + ' is exactly what you typed' };
    return { name: name, form: form, ok: false,
      why: 'the outer terms would give A = ' + Ptext(Ap) + ' and B = ' + Ptext(Bp)
        + ', so the middle term would have to be ' + Ptext(Pscale(Pmul(Ap, Bp), R(2n))) + ' or '
        + Ptext(Pscale(Pmul(Ap, Bp), R(-2n))) + '. It is ' + Pmono(mid.c, mid.e) + '.' };
  }
  function testCubes(p) {
    var form = 'A^3 + B^3 = (A + B)(A^2 - AB + B^2)';
    var t = Pterms(p);
    if (t.length !== 2) return { name: 'sum or difference of cubes', form: form, ok: false,
      why: 'it needs exactly two terms, and this has ' + t.length };
    var hi = t[0], lo = t[1];
    if (hi.e % 3 !== 0 || lo.e % 3 !== 0) return { name: 'sum or difference of cubes', form: form, ok: false,
      why: 'the powers ' + powerName(hi.e) + ' and ' + powerName(lo.e) + ' are not both multiples of 3' };
    var A = Rcbrt(hi.c), B = Rcbrt(lo.c);
    if (A === null || B === null) return { name: 'sum or difference of cubes', form: form, ok: false,
      why: Rtext(hi.c) + ' and ' + Rtext(lo.c) + ' are not both perfect cubes' };
    /* A difference of cubes is computed here as a sum with a negative B --
       the same arithmetic -- but it is REPORTED as the identity the reader was
       taught, with B positive and the signs where they expect them. */
    var negative = Rsign(B) < 0;
    var name = negative ? 'difference of cubes' : 'sum of cubes';
    var Ap = monoPoly(A, hi.e / 3), Bp = monoPoly(B, lo.e / 3);
    var Bshown = monoPoly(Rabs(B), lo.e / 3);
    var quad = Psub(Padd(Pmul(Ap, Ap), Pmul(Bp, Bp)), Pmul(Ap, Bp));
    return {
      name: name,
      form: negative ? 'A^3 - B^3 = (A - B)(A^2 + AB + B^2)' : form,
      ok: true, pieces: [Padd(Ap, Bp), quad],
      why: 'A = ' + Ptext(Ap) + ' and B = ' + Ptext(Bshown) + ', since A^3 = ' + Ptext(Ppow(Ap, 3))
        + ' and B^3 = ' + Ptext(Ppow(Bshown, 3)) };
  }
  function runTests(p) { return [testDiffSquares(p), testSumSquares(p), testPerfectSquare(p), testCubes(p)]; }
  function firstMatch(p) {
    var tests = runTests(p), hit = null;
    tests.forEach(function (t) { if (!hit && t.ok) hit = t; });
    return { tests: tests, hit: hit };
  }

  function modeSpecial() {
    var read = readPoly(inPoly, 'The polynomial');
    if (!read.ok) {
      explain('<strong>Nothing to test yet.</strong> ' + read.why, [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly;
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'four patterns, each tested against what you typed';
    if (Pzero(p)) {
      explain('<strong>That is the zero polynomial.</strong> None of the special forms applies to it: '
        + '0 = 0 * anything, so it has every polynomial as a factor and no useful factorisation at all.',
        [say('you typed', shownInput(inPoly))]);
      return;
    }

    var pass1 = firstMatch(p);
    var testRows = pass1.tests.map(function (t) {
      return rowOf([
        '<th class="rowhead">' + t.name + '</th>',
        cell(t.form),
        cell(t.ok ? chip(true, 'applies') : (t.recognised ? chipHi('recognised, but no factorisation') : chip(false, 'no')), t.ok ? 't' : ''),
        cell(t.why)
      ], t.ok ? 'focus' : '');
    });
    var blocks = [table('Testing all four patterns', ['pattern', 'the identity', 'does it apply?', 'why'], testRows)];

    if (!pass1.hit) {
      var v = searchVerdict(p);
      var sumSq = pass1.tests[1].recognised;
      blocks.push(table('No pattern applies. What now?', [], [
        say('the patterns are shortcuts', 'they recognise polynomials of a particular SHAPE. Failing '
          + 'every one of them says nothing about whether this polynomial factors.'),
        say('what the rational root search finds', v.linear
          ? Ptext(p) + ' = ' + v.text
          : 'no rational root, so no linear factor over the rationals'
            + (v.settled ? ' &mdash; and for degree ' + Pdegtext(p) + ' that settles it: it does not '
                 + 'factor over the rationals at all'
               : '. At degree ' + Pdegtext(p) + ' that is not the whole story: a polynomial with no '
                 + 'rational root can still split into two quadratics, and this search does not test for that')),
        say('the honest summary', sumSq
          ? 'a sum of squares of this shape has no difference-of-squares factorisation, which is what '
            + 'the second row above says. That is the useful conclusion; "it never factors" would be '
            + 'a stronger claim than the test made.'
          : 'the special forms are a small set of shapes, and most polynomials are not one of them')
      ]));
      work.innerHTML = blocks.join('');
      setKpis(['none', '0 of 4', v.linear ? v.text : Ptext(p), '&mdash;']);
      paintPlot(p, []);
      status.innerHTML = '<strong>None of the four patterns fits ' + Ptext(p) + '.</strong> '
        + (sumSq
          ? 'It is a sum of squares, and the difference-of-squares identity needs a minus: '
            + '(A - B)(A + B) multiplied out has -B^2 in it and there is no arrangement of brackets '
            + 'with rational coefficients that gives +B^2 for a quadratic. '
            + (Pdeg(p) === 2 ? 'For this quadratic the curve above shows the same thing: it never '
                 + 'reaches the axis, so there is no real root and no real factorisation either.' : '')
          : 'That is the ordinary case. The patterns are worth knowing because they are fast when they '
            + 'fit, not because they are complete; ' + (v.linear ? 'the rational root search factors '
            + 'this one as ' + v.text + '.' : 'here even the rational root search comes back empty.'));
      return;
    }

    /* A pattern applied. Apply the patterns again to each factor it produced --
       one pass is not enough for x^4 - 16, and stopping early is the commonest
       way this method is got wrong. */
    var refined = [], secondRows = [];
    pass1.hit.pieces.forEach(function (piece) {
      var again = firstMatch(piece);
      if (again.hit) {
        refined = refined.concat(again.hit.pieces);
        secondRows.push(rowOf(['<th class="rowhead">' + Pfactortext(piece) + '</th>',
          cell(chip(true, again.hit.name)),
          cell(factoredText(again.hit.pieces))], 'focus'));
      } else {
        refined.push(piece);
        secondRows.push(rowOf(['<th class="rowhead">' + Pfactortext(piece) + '</th>',
          cell(chip(false, 'no pattern applies')),
          cell(again.tests[1].recognised ? 'a sum of squares: it stays as it is' : 'it stays as it is')]));
      }
    });

    blocks.push(table('The pattern that fitted', [], [
      say('pattern', pass1.hit.name + ': ' + pass1.hit.form),
      say('the pieces', pass1.hit.why),
      say('first pass', factoredText(pass1.hit.pieces))
    ]));
    blocks.push(table('Second pass: can either factor be factored again?',
      ['factor', 'pattern', 'result'], secondRows));
    blocks.push(table('The check', [], verifyRows(refined, p)));

    var vv = searchVerdict(p);
    blocks.push(table('A second opinion', [], [
      say('the rational root search says', vv.text),
      say('these are the same factorisation', chip(Psame(expandBack(refined), p),
        'the pattern route multiplies back to what you typed')
        + ' &mdash; the two routes are independent: one recognises shapes, the other searches for roots')
    ]));
    work.innerHTML = blocks.join('');
    setKpis([pass1.hit.name, '1 of 4', factoredText(refined),
             chip(verified(refined, p), verified(refined, p) ? 'yes' : 'no')]);
    paintPlot(p, []);

    var deeper = refined.length > pass1.hit.pieces.length;
    status.innerHTML = '<strong>' + Ptext(p) + ' = ' + factoredText(refined) + '.</strong> '
      + 'The ' + pass1.hit.name + ' pattern fitted: ' + pass1.hit.why + '. '
      + (deeper
        ? 'One pass was not enough &mdash; a factor from the first pass matched a pattern again, and '
          + 'stopping after the first bracket would have left the answer half-finished. That is the '
          + 'commonest error with these identities.'
        : 'Neither factor matches a pattern again, so this is finished.')
      + ' Every bracket above was multiplied back out and compared with what you typed.';
  }

  /* ------------------------------------------- mode: the rational root theorem */
  function modeRoots() {
    var read = readPoly(inPoly, 'The polynomial');
    if (!read.ok) {
      explain('<strong>Nothing to search yet.</strong> ' + read.why, [say('you typed', shownInput(inPoly))]);
      return;
    }
    var p = read.poly;
    titleOut.textContent = Ptext(p);
    subOut.textContent = 'candidates from the divisors, then every one tested';
    if (Pdeg(p) < 1) {
      explain('<strong>A constant has no roots to look for.</strong> ' + Ptext(p) + ' is never zero '
        + (Pzero(p) ? 'except that it is always zero: the zero polynomial has every number as a root'
                    : 'for any x, so there is nothing for the search to find') + '. Type something of '
        + 'degree 1 or more.', [say('you typed', shownInput(inPoly)), say('degree', Pdegtext(p))]);
      return;
    }

    /* Clear denominators and take out x: the theorem is about a polynomial with
       whole-number coefficients and a non-zero constant term. */
    var g = monoGcf(p), core = g.rest;
    var gcfPoly = [];
    for (var i = 0; i < g.e; i += 1) gcfPoly.push(R0);
    gcfPoly.push(g.c);

    var prepRows = [
      say('what you typed', Ptext(p)),
      say('common factor out', (Requ(g.c, R1) && g.e === 0)
        ? 'nothing to take out'
        : Ptext(p) + ' = ' + gcfText(g) + '(' + Ptext(core) + ')'
          + (g.e > 0 ? ' &mdash; and x^' + g.e + ' being a factor means x = 0 is a root, found before the search starts' : '')),
      say('whole-number coefficients', Ptext(core) + ' &mdash; the theorem is stated for these, which '
        + 'is why the denominators were cleared first')
    ];

    if (Pdeg(core) < 1) {
      work.innerHTML = table('Preparing the polynomial', [], prepRows)
        + table('The factorisation', [], verifyRows([gcfPoly, core], p));
      setKpis(['0', g.e > 0 ? 'x = 0' : 'none', factoredText([gcfPoly, core]),
               chip(verified([gcfPoly, core], p), 'yes')]);
      paintPlot(p, []);
      status.innerHTML = '<strong>' + Ptext(p) + ' is a single term, and it is already factored.</strong> '
        + 'Taking the common factor out left ' + Ptext(core) + ', so there is no polynomial for the '
        + 'candidate search to run on. Its only root is x = 0'
        + (g.e > 1 ? ', repeated ' + g.e + ' times &mdash; the multiplicity is the power of x' : '')
        + ', and the rational root theorem is not needed to see it.';
      return;
    }

    var deg = Pdeg(core);
    var a0 = core[0].n, an = core[deg].n;
    var pdivs = bdivisors(a0), qdivs = bdivisors(an);
    var seen = {}, candidates = [];
    pdivs.forEach(function (pd) {
      qdivs.forEach(function (qd) {
        [pd, -pd].forEach(function (num) {
          var cand = R(num, qd), key = Rtext(cand);
          if (seen[key]) return;
          seen[key] = 1;
          candidates.push(cand);
        });
      });
    });
    candidates.sort(Rcmp);

    var genRows = [
      say('constant term', Rtext(core[0]) + ', whose divisors are ' + pdivs.join(', ')),
      say('leading coefficient', Rtext(core[deg]) + ', whose divisors are ' + qdivs.join(', ')),
      say('the theorem', 'if p/q in lowest terms is a root, then p divides the constant term and q '
        + 'divides the leading coefficient. So every rational root is one of the +-p/q built from '
        + 'those two lists &mdash; and nothing else can be.'),
      say('candidates', candidates.length + ' of them: ' + candidates.map(Rtext).join(', '))
    ];

    var roots = [], testRows = [];
    var shown = candidates.slice(0, 60);
    shown.forEach(function (cand) {
      var value = Peval(core, cand), zero = Rzero(value);
      if (zero) roots.push(cand);
      testRows.push(rowOf([
        '<th class="rowhead">x = ' + Rtext(cand) + '</th>',
        cell(Rtext(value), zero ? 't' : 'f'),
        cell(zero ? chip(true, 'a root, so ' + Pfactortext([Rneg(cand), R1]) + ' is a factor')
                  : muted('not a root'))
      ], zero ? 'focus' : ''));
    });
    if (candidates.length > shown.length) {
      testRows.push(rowOf(['<th class="rowhead">&mdash;</th>',
        cell(muted((candidates.length - shown.length) + ' further candidates were tested but are not listed')),
        cell(muted('the table would be longer than the lesson'))]));
      candidates.slice(60).forEach(function (cand) { if (Rzero(Peval(core, cand))) roots.push(cand); });
    }
    var libRoots = Prationalroots(core);
    var agree = libRoots.length === roots.length && libRoots.every(function (r, k) { return Requ(r, roots[k]); });

    /* Divide each root out, with its multiplicity, and see what is left. */
    var work2 = core, pieces = [], divRows = [];
    roots.forEach(function (r) {
      var factor = [Rneg(R(r.n)), R(r.d)], mult = 0;
      while (Pdeg(work2) > 0) {
        var dm = Pdivmod(work2, factor);
        if (!Pzero(dm.r)) break;
        work2 = dm.q;
        mult += 1;
        pieces.push(factor);
        divRows.push(rowOf([
          '<th class="rowhead">divide by ' + Pfactortext(factor) + '</th>',
          cell(Ptext(work2)),
          cell(mult > 1 ? 'x = ' + Rtext(r) + ' again: a repeated root' : 'remainder 0, so it is a factor')
        ]));
      }
    });
    var leftover = work2;
    var allPieces = [];
    if (!Requ(g.c, R1)) allPieces.push([g.c]);
    if (g.e > 0) allPieces.push(monoPoly(R1, g.e));
    pieces.forEach(function (f) { allPieces.push(f); });
    if (!(Pdeg(leftover) === 0 && Requ(Plead(leftover), R1))) allPieces.push(leftover);

    var blocks = [
      table('Preparing the polynomial', [], prepRows),
      table('Generating the candidates', [], genRows),
      table('Testing every candidate', ['candidate', 'f(candidate)', 'verdict'], testRows),
      table('What the search found', [], [
        say('roots', roots.length ? roots.map(Rtext).join(', ') : 'none &mdash; every candidate gave a non-zero value'),
        say('checked against the library search', chip(agree, agree
          ? (roots.length ? 'the same roots, found by a separately written routine'
                          : 'a separately written search also came back empty')
          : 'the two searches disagree'))
      ])
    ];
    if (divRows.length) blocks.push(table('Dividing each factor out', ['step', 'what is left', 'note'], divRows));
    if (Pdeg(leftover) > 0) {
      var leftRows = [say('what is left', Ptext(leftover)),
        say('why the search stopped', 'none of the remaining candidates is a root of it, so it has no '
          + 'linear factor with rational coefficients')];
      if (Pdeg(leftover) === 2) {
        var qr = quadroots(leftover[2], leftover[1] || R0, leftover[0] || R0);
        leftRows.push(say('its exact roots', qr.kind === 'complex'
          ? 'x = ' + pmtext(qr.p, qr.s, true) + ' &mdash; not real'
          : 'x = ' + pmtext(qr.p, qr.s) + ' &mdash; real, and irrational, which is exactly why no '
            + 'rational candidate could have found them'));
      } else if (Pdeg(leftover) === 3) {
        leftRows.push(say('is that final?', 'for a cubic, yes: a cubic that factors at all has a linear '
          + 'factor, and the search just ruled every one of them out'));
      } else {
        leftRows.push(say('is that final?', 'not necessarily: a polynomial of degree ' + Pdeg(leftover)
          + ' with no rational root can still split into two factors of degree 2 or more, and this '
          + 'search does not test for that'));
      }
      blocks.push(table('The leftover', [], leftRows));
    }
    blocks.push(table('The factorisation', [], verifyRows(allPieces, p)));
    work.innerHTML = blocks.join('');
    setKpis([String(candidates.length), String(roots.length), factoredText(allPieces),
             chip(verified(allPieces, p), verified(allPieces, p) ? 'yes' : 'no')]);
    paintPlot(p, candidates);

    status.innerHTML = roots.length
      ? '<strong>' + candidates.length + ' candidates, ' + roots.length + ' root'
        + (roots.length === 1 ? '' : 's') + ': ' + Ptext(p) + ' = ' + factoredText(allPieces) + '.</strong> '
        + 'The candidate list was built from the divisors of the constant term and of the leading '
        + 'coefficient &mdash; that is the whole content of the rational root theorem, and it is what '
        + 'turns "guess a root" into a finite search. Each candidate was substituted; the ones that '
        + 'gave zero are marked on the axis above, and the hollow circles are the ones that failed.'
      : '<strong>' + candidates.length + ' candidates, and not one of them is a root.</strong> '
        + 'The search is exhaustive: any rational root p/q must have p dividing ' + Rtext(core[0])
        + ' and q dividing ' + Rtext(core[deg]) + ', and every such number was substituted above. So '
        + Ptext(core) + ' has NO rational root. '
        + (Pdeg(core) <= 3
          ? 'For degree ' + Pdeg(core) + ' that also settles factorisation: it does not factor over '
            + 'the rationals at all. The curve above still crosses the axis, so it does have a real '
            + 'root &mdash; an irrational one, which no list of fractions was ever going to contain.'
          : 'At degree ' + Pdeg(core) + ' that rules out linear factors but not a split into two '
            + 'quadratics, which this search does not test for.');
  }

  /* ------------------------------------------------------------- wiring */
  function redraw() {
    try {
      if (MODE === 'gcf') modeGcf();
      else if (MODE === 'grouping') modeGrouping();
      else if (MODE === 'trinomial') modeTrinomial();
      else if (MODE === 'ac') modeAc();
      else if (MODE === 'special') modeSpecial();
      else modeRoots();
    } catch (err) {
      explain('<strong>That input stopped the lab.</strong> ' + esc(err && err.message ? err.message : String(err))
        + '. Pick one of the examples to get moving again, and change it a little at a time to find '
        + 'what this lab could not read.', []);
    }
  }
  preset.addEventListener('change', function () { inPoly.value = preset.value; redraw(); });
  inPoly.addEventListener('input', redraw);
  inPoly.value = preset.value;
  redraw();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an example, or type your own"),
        panel_intro=cfg.get("panel_intro", FACTOR_PANEL_INTRO[mode]),
        script=script,
    )
