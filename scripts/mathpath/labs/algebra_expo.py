"""Course 8: exponentials and logarithms, with the arithmetic kept exact.

Two labs live here because they are one subject seen from two sides, and the
file is arranged so that neither can drift from the other: they share one set of
numeric helpers, and every logarithm on the page is answered by asking a
question about EXPONENTS.

--------------------------------------------------------------------------
expo_lab -- the exponential function

The teaching decision: an exponential is introduced as the function whose
successive values have a constant RATIO, not as a curve that "goes up fast", so
every table here prints the ratio and the difference side by side and lets the
reader watch which one stays put. Because the values at integer x are a * b^x
with a and b rational, they are exact fractions -- 3(1/2)^4 is 3/16 on the page,
not 0.1875 -- and the ratio column is exactly b, printed from the arithmetic
rather than asserted.

  intro     the definition, against a straight line through the same first two
            points, with the horizontal asymptote drawn and named
  growth     b > 1 against 0 < b < 1 as one picture, with the number of steps to
            double (or to halve) found by EXACT search over b^n, and the real
            doubling time given afterwards as the rounded irrational it is
  e         (1 + 1/n)^n computed exactly as a fraction for as long as exact
            arithmetic is affordable, beside the series sum 1/k!, so the reader
            sees where e comes from AND why nobody computes it that way. The two
            naive answers -- "the base tends to 1, so the limit is 1" and "the
            exponent cancels the fraction, so it is 2" -- are columns in the
            table, wrong on every row.
  interest  the same principal compounded at six frequencies plus continuously,
            each an exact rational as long as n*t is a whole number, with simple
            interest alongside as the method that quietly loses money.

--------------------------------------------------------------------------
logarithm_lab -- the logarithm

The teaching decision: a logarithm is never evaluated by calling a logarithm.
Every exact answer on this page is found by SEARCHING for a rational exponent
p/q with b^p = x^q -- exact rational arithmetic, no floating point anywhere near
it -- and when the search comes back empty the lab says so, brackets the answer
between two consecutive integer powers it can prove, and only then prints a
rounded decimal, labelled as rounded. That is the honest shape of the subject:
log_2(8) is 3 exactly, and log_2(10) is a number we can only pin down.

  define    the two forms of one fact, converted both ways
  graph     the exponential and the logarithm as reflections in y = x, drawn
            from the same base, each with the asymptote the other one's line
            became
  laws      each law checked on the reader's numbers, and the two invented laws
            log(M + N) = log M + log N and log(M/N) = log M / log N shown
            failing on a concrete example rather than merely warned against
  common    base 10 and base e: the characteristic is exact and the mantissa is
            not, which is the whole reason log tables had two columns
  base      change of base, derived, then checked through three different helper
            bases that must agree
  solveexp  b^(cx+d) = k by matching powers when that is possible and by logs
            when it is not, including the cases with no solution at all
  solvelog  the domain check as a first-class step: candidates that make an
            argument zero or negative are rejected, with the reason
  scale     decibels, pH and magnitude -- where a difference of one on the scale
            is a factor on the quantity, and where adding two equal sources adds
            about 3, not double
"""

from .algebra_core import PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# --------------------------------------------------------------------------
# Shared numerics. Both labs need three things the core kit does not have: a
# float that survives a fraction with thousands of digits (for pixels), an
# exactly rounded decimal (for every place a lesson says "rounded to"), and the
# exponent search that answers every logarithm on the page.

NUMERIC_JS = r"""
  /* ---- decimals, and the one honest way to leave the exact world ---- */

  /* A fraction whose numerator and denominator have both left the range of a
     double still has to land on a pixel. Dividing in integers first is the
     difference between a point on the curve and a NaN. */
  function Rfloat(a) {
    var quick = Number(a.n) / Number(a.d);
    if (isFinite(quick)) return quick;
    var neg = a.n < 0n, n = neg ? -a.n : a.n;
    var scaled = (n * 100000000000000000000n) / a.d;      /* 10^20 */
    var s = scaled.toString();
    if (s === '0') return 0;
    var head = s.slice(0, 17);
    var v = Number(head) * Math.pow(10, s.length - head.length - 20);
    return neg ? -v : v;
  }

  /* Rounding done in integers, so the decimal a lab prints is the correct
     rounding of the exact fraction and not of a double that already lost the
     digits. Half rounds up. Every caller states the number of places. */
  function Rdecimal(a, places) {
    if (places === undefined) places = 6;
    var neg = Rsign(a) < 0, m = Rabs(a);
    var scale = 10n ** BigInt(places);
    var q = (m.n * scale * 2n / m.d + 1n) / 2n;
    var s = q.toString();
    while (s.length <= places) s = '0' + s;
    var whole = s.slice(0, s.length - places);
    var frac = places > 0 ? '.' + s.slice(s.length - places) : '';
    return (neg ? '-' : '') + whole + frac;
  }
  /* The exact fraction when it fits on the page, and a rounding marked with an
     "approximately" sign when it does not. A 40,000-digit numerator is exact
     and unreadable; the reader is told which of the two they are looking at.
     The size test compares BigInts rather than building the string, because
     the string is the expensive part and is usually thrown away. */
  var SHOWMAX = 100000000000000000000n;
  function Rbig(a) { return (a.n < 0n ? -a.n : a.n) >= SHOWMAX || a.d >= SHOWMAX; }
  function Rshow(a, places) {
    if (!Rbig(a)) return Rtext(a);
    return '&asymp;&nbsp;' + Rdecimal(a, places === undefined ? 6 : places);
  }

  /* ---- exact powers that stay affordable ----

     Rpow reduces after every multiplication, and a gcd on two 40,000-digit
     integers costs seconds. It never needs to: p/q in lowest terms makes
     p^k/q^k in lowest terms already. Skipping the reduction is what lets this
     page compound daily for thirty years EXACTLY instead of approximately. */
  function Rpowfast(a, k) {
    if (k < 0) return Rinv(Rpowfast(a, -k));
    var e = BigInt(k);
    return { n: a.n ** e, d: a.d ** e };
  }
  /* The same bargain for a single product: correct, unreduced, and destined to
     be rounded to a decimal rather than printed as a fraction. */
  function Rmulraw(a, b) { return { n: a.n * b.n, d: a.d * b.d }; }
  function pct(a, places) { return Rdecimal(Rmul(a, R(100n)), places === undefined ? 4 : places) + '%'; }
  /* 37/5 is exact and 7.4 is the same number written the way a reader typed it.
     A fraction whose denominator is built only from 2s and 5s has a decimal
     that terminates, so this is exactness in a friendlier notation -- and every
     other fraction keeps its slash rather than being silently rounded. */
  function Rdectext(a) {
    if (Rint(a)) return Rtext(a);
    var d = a.d, twos = 0, fives = 0;
    while (d % 2n === 0n) { d /= 2n; twos += 1; }
    while (d % 5n === 0n) { d /= 5n; fives += 1; }
    if (d !== 1n) return Rtext(a);
    return Rdecimal(a, Math.max(twos, fives));
  }

  /* ---- the exponent search: every exact logarithm on this page ----

     log_b(x) = p/q  <=>  b^p = x^q, and that is a question about exact
     rationals. So this searches: it builds b^p for every p in range, raises x
     to each q, and compares. log_2(8) comes back 3, log_9(3) comes back 1/2,
     and log_2(10) comes back EMPTY -- which is not a failure of the search but
     the fact the lesson beside it is about. */
  var PMAX = 48, QMAX = 12;
  function ratpow(b, x) {
    if (Rsign(b) <= 0 || Rsign(x) <= 0 || Requ(b, R1)) return null;
    if (Rtext(b).length > 40 || Rtext(x).length > 40) return null;   /* lesson-sized */
    var powers = [], p;
    for (p = -PMAX; p <= PMAX; p += 1) powers.push(Rpow(b, p));
    for (var q = 1; q <= QMAX; q += 1) {
      var xq = Rpow(x, q);
      for (p = -PMAX; p <= PMAX; p += 1) {
        if (!Requ(powers[p + PMAX], xq)) continue;
        var g = bgcd(BigInt(p < 0 ? -p : p), BigInt(q)) || 1n;
        return R(BigInt(p) / g, BigInt(q) / g);
      }
    }
    return null;
  }

  /* The integer part of log_b(x), found by multiplying by b until x is passed.
     It returns the two powers that trap x, so a lab can show 2^3 < 10 < 2^4 as
     an exact statement before it shows any decimal at all. */
  function bracketexp(b, x) {
    if (Rsign(b) <= 0 || Requ(b, R1) || Rsign(x) <= 0) return null;
    var up = Rcmp(b, R1) > 0, k = 0, cur = R1, guard = 0;
    while (guard++ < 2000) {
      var next = Rmul(cur, b);
      if (!(up ? Rcmp(next, x) <= 0 : Rcmp(next, x) >= 0)) break;
      cur = next; k += 1;
    }
    if (guard >= 2000) return null;
    guard = 0;
    while (guard++ < 2000) {
      if (!(up ? Rcmp(cur, x) > 0 : Rcmp(cur, x) < 0)) break;
      cur = Rdiv(cur, b); k -= 1;
    }
    if (guard >= 2000) return null;
    return { k: k, low: cur, high: Rmul(cur, b) };
  }

  /* One logarithm, with its provenance attached. kind is 'exact' when the
     search found the exponent, 'searched' when it did not (and then br holds
     the powers that bracket x and v is a rounded double), and a named refusal
     when the base or the argument is outside the definition. */
  function logvalue(b, x) {
    if (Rsign(b) <= 0) return { kind: 'badbase' };
    if (Requ(b, R1)) return { kind: 'base1' };
    if (Rsign(x) <= 0) return { kind: 'domain' };
    var y = ratpow(b, x);
    if (y !== null) return { kind: 'exact', y: y, v: Rfloat(y) };
    var br = bracketexp(b, x);
    /* A whole-number exponent past the end of the search is still exact: if the
       lower power in the bracket IS x, the logarithm is that integer. b = 2 and
       x = 2^100 would otherwise be reported as "no exact answer", which is
       false, and a lab that says something false about its own search is worse
       than one that searches a smaller range. */
    if (br !== null && Requ(br.low, x)) return { kind: 'exact', y: R(BigInt(br.k)), v: br.k };
    return { kind: 'searched', br: br, v: Math.log(Rfloat(x)) / Math.log(Rfloat(b)) };
  }
  /* What to print for one logarithm, exact or not, in six characters or sixty. */
  function logtext(lv, places) {
    if (places === undefined) places = 6;
    if (lv.kind === 'exact') return Rtext(lv.y);
    if (lv.kind === 'searched') return '&asymp;&nbsp;' + lv.v.toFixed(places);
    if (lv.kind === 'domain') return 'undefined';
    if (lv.kind === 'base1') return 'undefined (base 1)';
    return 'undefined (base &le; 0)';
  }
  function logfloat(lv) { return lv.kind === 'exact' ? Rfloat(lv.y) : lv.v; }

  /* ---- small HTML the two labs share ---- */
  function cell(t, cls) { return '<td' + (cls ? ' class="' + cls + '"' : '') + '>' + t + '</td>'; }
  function rowhead(t) { return '<th class="rowhead">' + t + '</th>'; }
  function trow(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.join('') + '</tr>'; }
  function ttable(caption, heads, rows) {
    var head = heads.length
      ? '<thead><tr>' + heads.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead>'
      : '';
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption>'
      + head + '<tbody>' + rows.join('') + '</tbody></table></div>';
  }
  /* The two-column "step / what it says" table the exemplar uses. */
  function steps(caption, pairs) {
    return ttable(caption, [], pairs.map(function (p) {
      return trow([rowhead(p[0]), cell(p[1])]);
    }));
  }
  function chip(text, cls) { return '<span class="chip ' + cls + '">' + text + '</span>'; }
"""



# --------------------------------------------------------------------------
# Markup helpers. Every mode declares its own controls, because a lab may only
# read an element it actually put on the page -- reaching for an input that a
# different mode declares is the bug this file is arranged to make impossible.


def _text_field(field_id, label, value):
    return ('        <div class="field">\n'
            '          <label for="' + field_id + '">' + label + '</label>\n'
            '          <input id="' + field_id + '" type="text" value="' + value
            + '" inputmode="text" autocomplete="off">\n'
            '        </div>\n')


def _range_field(field_id, label, lo, hi, value):
    return ('        <div>\n'
            '          <div class="range-row"><label class="small-copy" for="' + field_id + '">'
            + label + '</label><span class="range-value" id="' + field_id + 'Out">' + value
            + '</span></div>\n'
            '          <input id="' + field_id + '" type="range" min="' + lo + '" max="' + hi
            + '" value="' + value + '" />\n'
            '        </div>\n')


def _kpi_grid(pairs):
    cells = "".join('<div class="kpi"><span>' + label + '</span><strong id="' + kid
                    + '">&mdash;</strong></div>' for label, kid in pairs)
    return '        <div class="kpi-grid">' + cells + "</div>\n"


def _select(field_id, label, presets):
    options = "".join('<option value="' + "|".join(parts) + '">' + text + "</option>"
                      for text, *parts in presets)
    return ('        <div class="field">\n'
            '          <label for="' + field_id + '">' + label + '</label>\n'
            '          <select id="' + field_id + '">' + options + "</select>\n"
            '        </div>\n')


def _legend(items):
    return '<div class="inline-legend">' + "".join(
        '<span class="' + tone + '"><i class="legend-swatch"></i>' + text + "</span>"
        for tone, text in items) + "</div>"


def _js_list(ids):
    return "[" + ", ".join("'" + i + "'" for i in ids) + "]"


# --------------------------------------------------------------------------
# expo_lab
#
# Presets are chosen so a lesson can walk them in order and meet the awkward
# case on purpose: base 1 (neither growth nor decay), a negative base (not a
# function on the reals at all), a rate large enough that the compounding
# frequency stops being a detail, and a table of n big enough that floating
# point answers the limit question with the wrong number.

EXPO_PRESETS = {
    "intro": [
        ("f(x) = 2^x", "1", "2", "0"),
        ("f(x) = 3(1/2)^x &mdash; halving", "3", "1/2", "0"),
        ("f(x) = 2^x + 3 &mdash; asymptote y = 3", "1", "2", "3"),
        ("f(x) = 100(4/5)^x - 20 &mdash; decay to y = -20", "100", "4/5", "-20"),
        ("f(x) = 5(1)^x &mdash; base 1: nothing happens", "5", "1", "0"),
        ("f(x) = (-2)^x &mdash; negative base: no curve to draw", "1", "-2", "0"),
    ],
    "growth": [
        ("doubling: b = 2", "1", "2"),
        ("+50% a step: b = 3/2", "1", "3/2"),
        ("halving: b = 1/2", "160", "1/2"),
        ("-10% a step: b = 9/10", "100", "9/10"),
        ("+1% a step: b = 101/100 &mdash; the rule of 70", "100", "101/100"),
        ("b = 1: no change, ever", "100", "1"),
    ],
    "e": [
        ("n = 1, 2, 3, 4, ... &mdash; counting", "count"),
        ("n = 1, 2, 4, 8, ... &mdash; doubling", "double"),
        ("n = 1, 10, 100, ... &mdash; powers of ten", "ten"),
        ("n = 10, 20, 30, ... &mdash; and it barely moves", "arith"),
        ("n = 10^9 upward &mdash; where a double gives up", "big"),
    ],
    "interest": [
        ("$1 at 100% for 1 year &mdash; where e comes from", "1", "100", "1"),
        ("$1000 at 5% for 10 years", "1000", "5", "10"),
        ("$2500 at 7% for 30 years", "2500", "7", "30"),
        ("$1000 at 12% for 1 year &mdash; monthly is not annual", "1000", "12", "1"),
        ("$1000 at 200% for 1 year &mdash; frequency stops being a detail", "1000", "200", "1"),
        ("$1000 at 5% for half a year &mdash; n*t is not always whole", "1000", "5", "1/2"),
    ],
}

EXPO_TITLES = {
    "intro": ("What makes a function exponential", "A constant ratio, where a line has a constant difference"),
    "growth": ("Growth and decay", "The base decides which, and exactly how fast"),
    "e": ("Where e comes from", "(1 + 1/n)^n, computed here rather than quoted"),
    "interest": ("Compounding", "Six frequencies against the continuous limit"),
}

EXPO_LEGEND = {
    "intro": [("tone-cyan", "f(x)"), ("tone-muted", "the line through f(0) and f(1)"),
              ("tone-red", "the asymptote")],
    "growth": [("tone-cyan", "b^x"), ("tone-purple", "(1/b)^x"), ("tone-red", "the asymptote y = 0")],
    "e": [("tone-amber", "(1 + 1/n)^n"), ("tone-green", "1 + 1/1! + 1/2! + ..."), ("tone-red", "e")],
    "interest": [("tone-cyan", "yearly"), ("tone-purple", "monthly"), ("tone-green", "continuous"),
                 ("tone-muted", "simple interest")],
}

EXPO_KPIS = {
    "intro": [("f(0)", "exKpi1"), ("Ratio each step", "exKpi2"), ("Asymptote", "exKpi3")],
    "growth": [("Change a step", "exKpi1"), ("Steps to double", "exKpi2"), ("Reached", "exKpi3")],
    "e": [("Last (1 + 1/n)^n", "exKpi1"), ("Last series sum", "exKpi2"), ("e, from the series", "exKpi3")],
    "interest": [("Yearly", "exKpi1"), ("Continuous", "exKpi2"), ("The gap", "exKpi3")],
}

EXPO_HINT = {
    "intro": "Whole numbers or fractions such as <code>4/5</code>. A base must be positive: the "
             "table still works for a negative base, and it is the curve that fails.",
    "growth": "The base is the whole story. Try <code>101/100</code> and count the steps to double.",
    "e": "Nothing here is a stored constant. The value of e in the last box is the series summed "
         "in this browser as an exact fraction, rounded once at the end.",
    "interest": "A rate is a percentage: <code>5</code> means 5% a year. Every balance is exact "
                "whenever n*t is a whole number, and says so when it is not.",
}

EXPO_FIELDS = {
    "intro": ["exA", "exB", "exShift"],
    "growth": ["exA", "exB"],
    "e": [],
    "interest": ["exP", "exR", "exT"],
}

EXPO_RANGES = {"intro": [], "growth": ["exSteps"], "e": ["exTerms"], "interest": []}


def expo_lab(cfg):
    """The exponential function: the definition, growth against decay, e, compounding.

    Every value in every table is a*b^x with a and b exact rationals, so the
    ratio column is the base itself rather than a rounding of it. The plot is
    the same function evaluated in floating point, because a pixel is a pixel.
    """
    mode = cfg.get("mode", "intro")
    if mode not in EXPO_PRESETS:
        mode = "intro"
    presets = cfg.get("presets") or EXPO_PRESETS[mode]
    title, subtitle = EXPO_TITLES[mode]

    markup = ('      <div class="lab-toolbar">\n'
              '        <div class="lab-title"><strong id="exTitle">Exponential</strong>'
              '<span id="exSub"></span></div>\n'
              "        " + _legend(EXPO_LEGEND[mode]) + "\n"
              "      </div>\n"
              '      <div class="lab-stage"><svg id="exPlot"></svg></div>\n'
              '      <div id="exWork" style="margin-top:12px;"></div>\n'
              '      <div class="status-banner" id="exStatus" style="margin-top:12px;"></div>')

    controls = _select("exPreset", "Example", presets)
    if mode in ("intro", "growth"):
        controls += _text_field("exA", "a (the value at x = 0)", "1")
        controls += _text_field("exB", "b (the base)", "2")
    if mode == "intro":
        controls += _text_field("exShift", "k (the asymptote it settles on)", "0")
    if mode == "growth":
        controls += _range_field("exSteps", "steps shown", "3", "24", "10")
    if mode == "e":
        controls += _range_field("exTerms", "rows", "3", "12", "8")
    if mode == "interest":
        controls += _text_field("exP", "P (principal)", "1000")
        controls += _text_field("exR", "r (annual rate, in percent)", "5")
        controls += _text_field("exT", "t (years)", "10")
    controls += _kpi_grid(EXPO_KPIS[mode])
    controls += '        <p class="small-copy" id="exHint" style="margin:0;">' + EXPO_HINT[mode] + "</p>\n"

    script = RATIONAL_JS + PLOT_JS + NUMERIC_JS + r"""
  var MODE = '""" + mode + r"""';
  var FIELDS = """ + _js_list(EXPO_FIELDS[mode]) + r""";
  var RANGES = """ + _js_list(EXPO_RANGES[mode]) + r""";
  var preset = document.getElementById('exPreset');
  var svg = document.getElementById('exPlot');
  var work = document.getElementById('exWork'), status = document.getElementById('exStatus');
  var titleOut = document.getElementById('exTitle'), subOut = document.getElementById('exSub');
  var kpi1 = document.getElementById('exKpi1');
  var kpi2 = document.getElementById('exKpi2');
  var kpi3 = document.getElementById('exKpi3');

  /* Reader input is a string until proved otherwise, and Rparse throws on
     "1/0" -- which is a thing a reader types -- so every read comes through
     here and a bad value becomes null rather than an exception. */
  function readnum(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return Rparse(el.value); } catch (err) { return null; }
  }
  function readint(id, fallback) {
    var el = document.getElementById(id);
    var v = el ? parseInt(el.value, 10) : NaN;
    return isFinite(v) ? v : fallback;
  }
  function setkpis(a, b, c) { kpi1.innerHTML = a; kpi2.innerHTML = b; kpi3.innerHTML = c; }
  /* A frame with nothing in it is still an answer: it says "there is no curve
     here", which is the honest picture for a base that is zero or negative. */
  function blankStage() {
    var p = Plot(svg, { xmin: -4, xmax: 4, ymin: -2, ymax: 8 });
    p.frame();
    p.describe('an empty frame: the values in the panel do not define a curve.');
    return p;
  }
  function fail(message) {
    status.innerHTML = message;
    work.innerHTML = '';
    setkpis('&mdash;', '&mdash;', '&mdash;');
    blankStage();
  }

  /* f(x) = a*b^x + k, exactly, at whole x. */
  function fexact(a, b, k, x) { return Radd(Rmul(a, Rpow(b, x)), k); }
  /* "3(1/2)^x", "-2^x", "5(1)^x + 3". The base is bracketed whenever a
     coefficient is written in front of it, because 5 and 1 side by side would
     read as fifty-one. */
  function ftext(a, b, k, v) {
    var coef = Requ(a, R1) ? '' : (Requ(a, R(-1n)) ? '-' : Rtext(a));
    var base = Rterm(b);
    if (coef !== '' && coef !== '-' && base.charAt(0) !== '(') base = '(' + base + ')';
    var s = coef + base + '^' + (v || 'x');
    if (!Rzero(k)) s += Rsign(k) > 0 ? ' + ' + Rtext(k) : ' - ' + Rtext(Rabs(k));
    return s;
  }

  /* ------------------------------------------------------------ intro ---- */
  function drawIntro() {
    var a = readnum('exA'), b = readnum('exB'), k = readnum('exShift');
    if (a === null || b === null || k === null) {
      fail('<strong>a, b and k each have to be a whole number or a fraction.</strong> '
        + 'Try 3, -2 or 4/5. Nothing below can be computed from a value that is not a number, and '
        + 'guessing what was meant would be worse than saying so.');
      return;
    }
    if (Rzero(b)) {
      fail('<strong>0 is not a base.</strong> 0^x is 0 for every positive x, is 1 at x = 0 by the '
        + 'empty-product convention, and is undefined for every negative x because it would ask for '
        + '1/0. Three rules on one function is not a function worth having, which is why the '
        + 'definition of an exponential requires b &gt; 0.');
      return;
    }
    titleOut.textContent = 'f(x) = ' + ftext(a, b, k);
    subOut.textContent = 'a = ' + Rtext(a) + ',  b = ' + Rtext(b) + ',  k = ' + Rtext(k);

    var lo = -3, hi = 4, rows = [], xs = [], x;
    var f0 = fexact(a, b, k, 0), f1 = fexact(a, b, k, 1), slope = Rsub(f1, f0);
    for (x = lo; x <= hi; x += 1) {
      var v = fexact(a, b, k, x);
      var gap = Rsub(v, k);
      var prev = x > lo ? fexact(a, b, k, x - 1) : null;
      var ratio = '&mdash;', constant = false;
      if (prev !== null) {
        var pgap = Rsub(prev, k);
        if (Rzero(pgap)) { ratio = '0 / 0, undefined'; }
        else { var q = Rdiv(gap, pgap); ratio = Rtext(q); constant = Requ(q, b); }
      }
      var line = Radd(f0, Rmul(slope, R(BigInt(x))));
      rows.push(trow([
        cell(String(x)), cell(Rshow(v)), cell(Rshow(gap)),
        cell(prev === null ? '&mdash;' : Rshow(Rsub(v, prev))),
        cell(ratio, constant ? 'on' : ''),
        cell(Rshow(line))
      ]));
      xs.push({ x: x, v: v });
    }
    work.innerHTML = ttable('f(x) = ' + ftext(a, b, k) + ', evaluated exactly at each whole x',
      ['x', 'f(x)', 'f(x) - k', 'change', 'ratio of the gaps', 'the line through f(0), f(1)'], rows);

    var av = Rfloat(a), bv = Rfloat(b), kv = Rfloat(k), sv = Rfloat(slope), f0v = Rfloat(f0);
    var vals = xs.map(function (p) { return Rfloat(p.v); }).concat([kv, f0v, f0v + sv * hi]);
    var ymin = Math.min.apply(null, vals), ymax = Math.max.apply(null, vals);
    var pad = Math.max(1, (ymax - ymin) * 0.15);
    var plot = Plot(svg, { xmin: lo - 0.4, xmax: hi + 0.4, ymin: ymin - pad, ymax: ymax + pad });
    plot.frame();
    plot.hline(kv, 'plot-asym', 'y = ' + Rtext(k));
    plot.curve(function (t) { return f0v + sv * t; }, 'plot-curve parent');
    if (Rsign(b) > 0) plot.curve(function (t) { return av * Math.pow(bv, t) + kv; });
    xs.forEach(function (p) { plot.point(p.x, Rfloat(p.v), 'plot-point'); });
    plot.describe('f(x) = ' + ftext(a, b, k) + ', its horizontal asymptote y = ' + Rtext(k)
      + ', and the straight line through the same first two points.');

    setkpis(Rshow(f0), Rtext(b), 'y = ' + Rtext(k));

    var msg;
    if (Rsign(b) < 0) {
      msg = '<strong>A negative base has no curve.</strong> The table is fine &mdash; b^x at whole x '
        + 'just alternates sign, and every entry above is exact. But halfway between two of those '
        + 'rows, at x = 1/2, the value would have to be a square root of ' + Rtext(b) + ', and no '
        + 'real number squares to a negative. There is nothing to draw between the dots, which is '
        + 'the reason the definition asks for b &gt; 0.';
    } else if (Rzero(a)) {
      msg = '<strong>With a = 0 there is no exponential left.</strong> f(x) = 0&middot;'
        + Rterm(b) + '^x + ' + Rtext(k) + ' is the constant ' + Rtext(k) + ', the ratio column is '
        + '0/0, and the curve lies along its own asymptote. An exponential needs a non-zero value '
        + 'at x = 0.';
    } else if (Requ(b, R1)) {
      msg = '<strong>Base 1 is the degenerate case.</strong> 1^x is 1 for every x, so f is the '
        + 'constant ' + Rshow(Radd(a, k)) + ': the ratio column is 1 and the change column is 0. '
        + 'It is not growth and it is not decay. It is also the reason the definition excludes '
        + 'b = 1 &mdash; a constant function has no inverse, so log base 1 could not exist.';
    } else {
      msg = '<strong>The ratio column is constant at ' + Rtext(b) + '. The change column is not.</strong> '
        + 'That is the entire difference between this and the straight line in the last column, '
        + 'which adds ' + Rshow(slope) + ' every step and never anything else. The distance from '
        + 'the asymptote, f(x) - k, is multiplied by ' + Rtext(b) + ' each step, so it '
        + (Rcmp(b, R1) > 0 ? 'grows without bound' : 'shrinks toward zero') + '. '
        + 'f(x) never equals y = ' + Rtext(k) + ': that would need a&middot;b^x = 0, and a product '
        + 'of non-zero numbers is never zero. That is what a horizontal asymptote is.';
    }
    status.innerHTML = msg;
  }

  /* ----------------------------------------------------------- growth ---- */

  /* The least n with b^n past a target, found by multiplying. A question about
     a whole number of steps is answered with whole numbers of steps -- no
     logarithm, no rounding, no "about 70". b^n stays in lowest terms on its
     own, so the reduction Rmul would do every round is skipped. */
  function stepsToFactor(b, target, cap) {
    var up = Rcmp(b, R1) > 0, cur = R1, n = 0;
    while (n < cap) {
      cur = { n: cur.n * b.n, d: cur.d * b.d };
      n += 1;
      if (up ? Rcmp(cur, target) >= 0 : Rcmp(cur, target) <= 0) return { n: n, value: cur };
    }
    return null;
  }

  function drawGrowth() {
    var a = readnum('exA'), b = readnum('exB');
    var n = readint('exSteps', 10);
    var out = document.getElementById('exStepsOut');
    if (out) out.textContent = String(n);
    if (a === null || b === null) {
      fail('<strong>a and b each have to be a whole number or a fraction.</strong> The base is the '
        + 'interesting one: try 2, 3/2, 9/10 or 101/100.');
      return;
    }
    if (Rsign(b) <= 0) {
      fail('<strong>Growth and decay need a positive base.</strong> With b = ' + Rtext(b)
        + ' the values alternate in sign or are undefined, so neither word describes anything. '
        + 'Every statement about a rate on this page assumes b &gt; 0.');
      return;
    }
    titleOut.textContent = 'f(n) = ' + ftext(a, b, R0, 'n') + ',  n = 0 to ' + n;
    subOut.textContent = 'every step multiplies by ' + Rtext(b);

    var rate = Rsub(b, R1), rows = [], cum = R1, val = a, i;
    for (i = 0; i <= n; i += 1) {
      rows.push(trow([
        cell(String(i)), cell(Rshow(val)), cell(Rshow(cum)),
        cell(i === 0 ? '&mdash;' : Rshow(Rmul(Rdiv(val, b), rate))),
        cell(i === 0 ? '&mdash;' : pct(rate, 4))
      ]));
      cum = Rmulraw(cum, b);
      val = Rmul(val, b);
    }

    var doubling = Rcmp(b, R1) > 0 ? stepsToFactor(b, R(2n), 400) : null;
    var halving = Rcmp(b, R1) < 0 ? stepsToFactor(b, R(1n, 2n), 400) : null;
    var hit = doubling || halving;
    var pairs = [];
    if (hit) {
      pairs.push([(doubling ? 'first n with b^n &ge; 2' : 'first n with b^n &le; 1/2'),
        'n = ' + hit.n + ', where b^' + hit.n + ' = ' + Rshow(hit.value, 8)
        + '. Found by multiplying by ' + Rtext(b) + ' until the target was passed, so it is the '
        + 'exact first step and not a rounded one.']);
      var real = Math.log(2) / Math.abs(Math.log(Rfloat(b)));
      pairs.push(['the continuous ' + (doubling ? 'doubling' : 'half') + ' time',
        'ln 2 / |ln ' + Rtext(b) + '| &asymp; ' + real.toFixed(4) + ' steps. This one is irrational '
        + 'and is rounded to 4 places; the whole number above is the first step at which the factor '
        + 'has really been reached.']);
      var pv = Math.abs(Rfloat(rate) * 100);
      if (pv > 0) {
        pairs.push(['the "rule of 70"',
          '70 / ' + Rdecimal(Rabs(Rmul(rate, R(100n))), 4) + ' &asymp; ' + (70 / pv).toFixed(2)
          + ' steps against the true ' + real.toFixed(4) + '. The rule rounds ln 2 &asymp; 0.6931 up '
          + 'to 0.70 and ignores that the step is discrete, so it drifts as the rate gets large.']);
      }
    } else if (Requ(b, R1)) {
      pairs.push(['first n with b^n &ge; 2',
        'there is none. b = 1 makes b^n = 1 for every n, so the sequence never moves and no number '
        + 'of steps doubles anything.']);
    } else {
      pairs.push(['first n with b^n past the target',
        'not within 400 steps at this rate. The search stops there rather than pretending; try a '
        + 'base further from 1.']);
    }
    work.innerHTML = ttable('every step, exactly &mdash; a value past 20 digits is shown '
      + 'rounded to 6 places and marked with an approximation sign',
      ['n', 'f(n)', 'b^n', 'change from the step before', 'change as a percent'], rows)
      + steps('how long a factor of two takes', pairs);

    var av = Rfloat(a), bv = Rfloat(b);
    var top = Math.max(Math.abs(av * Math.pow(bv, n)), Math.abs(av * Math.pow(1 / bv, n)), Math.abs(av), 1);
    if (!isFinite(top) || top > 1e9) top = Math.abs(av) * 100 || 1;
    var plot = Plot(svg, { xmin: -0.4, xmax: n + 0.4, ymin: -top * 0.12, ymax: top * 1.1 });
    plot.frame();
    plot.hline(0, 'plot-asym', 'y = 0');
    plot.curve(function (t) { return av * Math.pow(bv, t); });
    plot.curve(function (t) { return av * Math.pow(1 / bv, t); }, 'plot-curve alt');
    for (i = 0; i <= n; i += 1) plot.point(i, av * Math.pow(bv, i), 'plot-point');
    if (hit && hit.n <= n) plot.point(hit.n, av * Math.pow(bv, hit.n), 'plot-point root', 'n = ' + hit.n);
    plot.describe('a&middot;b^x with b = ' + Rtext(b) + ' drawn against its mirror a&middot;(1/b)^x, '
      + 'both sampled from the same definition, with the asymptote y = 0.');

    setkpis(pct(rate, 4), hit ? String(hit.n) : 'never', hit ? Rshow(hit.value, 6) : '1');

    var msg;
    if (Requ(b, R1)) {
      msg = '<strong>b = 1 is the border between growth and decay, and it is neither.</strong> '
        + 'The change column reads 0% on every row. Anything strictly greater than 1 grows without '
        + 'bound; anything strictly between 0 and 1 decays toward zero; 1 itself does nothing, '
        + 'forever.';
    } else if (Rcmp(b, R1) > 0) {
      msg = '<strong>b = ' + Rtext(b) + ' is greater than 1, so this grows by exactly '
        + pct(rate, 4) + ' every step.</strong> The percentage is the same on every row while the '
        + 'absolute change gets larger and larger &mdash; that is what people mean when they call '
        + 'growth "exponential", and it is a statement about the ratio, not about the speed. After '
        + n + ' steps the multiplier is b^' + n + ' = ' + Rshow(Rpowfast(b, n), 6)
        + '. The purple curve is base 1/b = ' + Rtext(Rinv(b))
        + ': decay is this same function reflected in the vertical axis, not a different species.';
    } else {
      msg = '<strong>b = ' + Rtext(b) + ' lies between 0 and 1, so this decays by '
        + pct(Rneg(rate), 4) + ' every step.</strong> It never reaches zero: b^n is a positive '
        + 'fraction however large n gets, which is why the axis is an asymptote and not a '
        + 'destination. After ' + n + ' steps the multiplier is ' + Rshow(Rpowfast(b, n), 8)
        + '. The purple curve, base 1/b = ' + Rtext(Rinv(b)) + ', is the same decay run backwards.';
    }
    status.innerHTML = msg;
  }

  /* ---------------------------------------------------------------- e ---- */

  /* Exact arithmetic on ((n+1)/n)^n stops being affordable somewhere, and the
     honest move is to name where rather than to quietly switch. Past this n a
     row is computed with doubles and is labelled as such -- and the last preset
     is chosen so the reader watches the doubles fail. */
  var EXACT_MAX = 100000;

  function esequence(kind, terms) {
    var out = [], i;
    for (i = 0; i < terms; i += 1) {
      if (kind === 'count') out.push(i + 1);
      else if (kind === 'double') out.push(Math.pow(2, i));
      else if (kind === 'ten') out.push(Math.pow(10, i));
      else if (kind === 'arith') out.push(10 * (i + 1));
      else out.push(Math.pow(10, 9 + i));
    }
    return out;
  }
  /* The partial sums of 1 + 1/1! + 1/2! + ..., exactly. */
  function eseries(terms) {
    var sums = [], fact = R1, acc = R0, k;
    for (k = 0; k < terms; k += 1) {
      if (k > 0) fact = Rmul(fact, R(BigInt(k)));
      acc = Radd(acc, Rinv(fact));
      sums.push({ k: k, term: Rinv(fact), sum: acc });
    }
    return sums;
  }
  function convergent(n) {
    return n <= EXACT_MAX
      ? { dec: Rdecimal(Rpowfast(R(BigInt(n) + 1n, BigInt(n)), n), 12), exact: true }
      : { dec: Math.pow(1 + 1 / n, n).toFixed(12), exact: false };
  }
  /* How many leading digits two decimal strings share. */
  function agreedigits(a, b) {
    var n = 0;
    for (var i = 0; i < Math.min(a.length, b.length); i += 1) {
      if (a[i] !== b[i]) break;
      if (a[i] !== '.') n += 1;
    }
    return n;
  }

  function drawE() {
    var terms = readint('exTerms', 8);
    if (!(terms >= 3)) terms = 3;
    if (terms > 12) terms = 12;
    var out = document.getElementById('exTermsOut');
    if (out) out.textContent = String(terms);
    var kind = (preset.value || 'count').split('|')[0];

    /* e, summed here from 30 terms of the series. Everything past the 30th
       term is smaller than 1/30!, which is below 1e-32, so the 18 places
       printed are right -- and they were computed on this page, not pasted in
       from somewhere the reader cannot check. */
    var ref = eseries(30), eexact = ref[ref.length - 1].sum, eref = Rdecimal(eexact, 18);

    titleOut.textContent = '(1 + 1/n)^n  as n grows';
    subOut.textContent = 'against 1 + 1/1! + 1/2! + ... , and against the two shortcuts';

    var ns = esequence(kind, terms), rows = [], last = null, seen = [];
    ns.forEach(function (n) {
      var c = convergent(n);
      last = { dec: c.dec, exact: c.exact, digits: agreedigits(c.dec, eref) };
      seen.push({ n: n, dec: c.dec, v: parseFloat(c.dec), digits: last.digits });
      rows.push(trow([
        cell(String(n)), cell(c.dec), cell(String(last.digits)),
        cell(c.exact ? chip('exact', 'ok') : chip('double', 'no')),
        cell('1.000000000000'), cell('2.000000000000')
      ]));
    });
    var series = eseries(terms);
    var srows = series.map(function (item) {
      var dec = Rdecimal(item.sum, 18);
      return trow([cell(String(item.k)), cell(Rshow(item.term)), cell(dec),
                   cell(String(agreedigits(dec, eref)))]);
    });
    var lastSum = series[series.length - 1].sum;

    work.innerHTML = ttable(
      'the limit definition, beside the two readings of it that look reasonable and are wrong',
      ['n', '(1 + 1/n)^n to 12 places', 'digits of e it has right', 'arithmetic',
       'base rounded to 1 first', 'exponent cancelled first'], rows)
      + ttable('the series 1 + 1/1! + 1/2! + ..., summed exactly',
        ['k', '1/k!', 'partial sum to 18 places', 'digits of e it has right'], srows)
      + steps('what the two tables are for', [
        ['the definition is rational', '(1 + 1/n)^n = ((n+1)/n)^n is a fraction for every whole n. '
          + 'The rows marked exact are that fraction, rounded once at the end and never before.'],
        ['and it is a bad way to compute e', 'the error falls like 1/n, so each further digit '
          + 'costs a factor of ten in n. Over the same ' + terms + ' rows the series reaches '
          + agreedigits(Rdecimal(lastSum, 18), eref) + ' correct digits and the limit reaches '
          + last.digits + ', because 1/k! falls faster than anything of the form 1/n.'],
        ['the two shortcuts', '1 + 1/n does tend to 1, and 1 raised to any power is 1. n&middot;(1/n) '
          + 'does equal 1, so the binomial\'s first two terms do give 2. Both readings are '
          + 'arithmetic applied to a limit in the wrong order, and the columns show them stuck at '
          + '1 and at 2 while the real value climbs past both.'],
        ['the reference', 'e above is the series to 30 terms &mdash; an exact fraction, rounded to '
          + '18 places at the very end: ' + eref + '. e is irrational, so every decimal on this '
          + 'page is a rounding of it and none of them is it.']
      ]);

    var plot = Plot(svg, { xmin: 0.4, xmax: terms + 0.6, ymin: 0.7, ymax: 3.2 });
    plot.frame();
    plot.hline(Rfloat(eexact), 'plot-asym', 'e');
    ns.forEach(function (n, i) { plot.point(i + 1, parseFloat(convergent(n).dec), 'plot-point'); });
    series.forEach(function (item, i) { plot.point(i + 1, Rfloat(item.sum), 'plot-point root'); });
    plot.describe('the sequence (1 + 1/n)^n rising toward e from below, with the partial sums of '
      + 'the series arriving far sooner, both against the row number.');

    setkpis(last.dec + (last.exact ? '' : ' (double)'), Rdecimal(lastSum, 12), eref);

    /* The closing paragraph is written from the rows that were just computed:
       which one first collapses to 1, which one overshoots, how many digits
       the series got. Nothing here is a claim about a number the reader cannot
       see in the table above. */
    var collapsed = null, over = null, best = 0, i;
    for (i = 0; i < seen.length; i += 1) {
      if (collapsed === null && seen[i].v === 1) collapsed = seen[i];
      if (seen[i].v > 2.72 && (over === null || seen[i].v > over.v)) over = seen[i];
      if (seen[i].digits > best) best = seen[i].digits;
    }
    var seriesDigits = agreedigits(Rdecimal(lastSum, 18), eref);
    var msg;
    if (kind === 'big') {
      msg = '<strong>This is where floating point gives up.</strong> Past n = ' + EXACT_MAX
        + ' the rows above are doubles rather than fractions. The best any of them manages is '
        + best + ' correct digits';
      if (over) {
        msg += ', and at n = ' + over.n + ' the answer is ' + over.dec
          + ' &mdash; past e, which the true sequence never is, because it increases toward e from '
          + 'below';
      }
      if (collapsed) {
        msg += '. At n = ' + collapsed.n + ' it reads exactly ' + collapsed.dec
          + ': 1 + 1/n has rounded to 1 in a double, and 1 to any power is 1';
      }
      msg += '. That is a fact about doubles, not about e. The exact rows and the series both say '
        + '2.718..., and they are the ones to believe.';
    } else {
      msg = '<strong>After ' + terms + ' rows the limit definition has '
        + last.digits + (last.digits === 1 ? ' correct digit' : ' correct digits')
        + ' and the series has ' + seriesDigits + '.</strong> Both climb to the same number and '
        + 'neither arrives: e is irrational, so no (1 + 1/n)^n and no partial sum of the series is '
        + 'ever equal to it. The last two columns are the two shortcuts, wrong on every row '
        + '&mdash; and worth taking seriously, because each is a correct piece of arithmetic done '
        + 'before the limit instead of after it. e &asymp; ' + eref + ', computed here.';
    }
    status.innerHTML = msg;
  }

  /* --------------------------------------------------------- interest ---- */

  var FREQS = [[1, 'once a year'], [2, 'twice a year'], [4, 'quarterly'], [12, 'monthly'],
               [52, 'weekly'], [365, 'daily']];

  function drawInterest() {
    var P = readnum('exP'), rpc = readnum('exR'), t = readnum('exT');
    if (P === null || rpc === null || t === null) {
      fail('<strong>P, r and t each have to be a number.</strong> The rate is a percentage, so '
        + '<code>5</code> means 5% a year, and t may be a fraction such as <code>1/2</code>.');
      return;
    }
    if (Rsign(t) < 0) {
      fail('<strong>t is a number of years, and this lab will not take a negative one.</strong> '
        + 'The formula would answer &mdash; it would tell you the balance before the deposit '
        + 'existed &mdash; but that answer is not about this account.');
      return;
    }
    if (Rcmp(Rdiv(rpc, R(100n)), R(-1n)) <= 0) {
      fail('<strong>A rate of ' + Rtext(rpc) + '% wipes out the balance within a single period.</strong> '
        + '1 + r/n has to stay positive for the powers below to mean anything, so this needs '
        + 'r &gt; -100%.');
      return;
    }
    var r = Rdiv(rpc, R(100n));
    titleOut.textContent = 'A = P(1 + r/n)^(nt)';
    subOut.textContent = 'P = ' + Rtext(P) + ',  r = ' + Rtext(rpc) + '%,  t = ' + Rtext(t)
      + ', against A = Pe^(rt)';

    var contv = Rfloat(P) * Math.exp(Rfloat(r) * Rfloat(t));
    var years = Rtext(t) + (Requ(t, R1) ? ' year' : ' years');
    var rows = [], annual = null, daily = null;
    FREQS.forEach(function (item) {
      var n = item[0], name = item[1];
      var per = Radd(R1, Rdiv(r, R(BigInt(n))));        /* 1 + r/n, exact */
      var apy = Rsub(Rpowfast(per, n), R1);             /* the effective annual rate, exact */
      var expo = Rmul(R(BigInt(n)), t);                 /* n*t */
      var exact = Rint(expo) && expo.n >= 0n && expo.n <= 50000n && per.n < 1000000000000n;
      /* The balance is exact whenever the exponent is a whole number. It is
         rounded to the cent for the column and kept at full width for the gap,
         so the last row of the table is not compared against a rounding. */
      var amount = exact ? Rmulraw(P, Rpowfast(per, Number(expo.n))) : null;
      var shown = exact ? Rdecimal(amount, 2)
                        : (Rfloat(P) * Math.pow(Rfloat(per), Rfloat(expo))).toFixed(2);
      var value = exact ? Rfloat(amount) : parseFloat(shown);
      if (n === 1) annual = { shown: shown, value: value };
      if (n === 365) daily = { shown: shown, value: value };
      rows.push(trow([
        cell(name), cell(String(n)), cell(Rtext(expo)), cell(shown),
        cell(exact ? chip('exact', 'ok') : chip('rounded', 'no')),
        cell(pct(apy, 4)), cell((contv - value).toFixed(6))
      ]));
    });
    var simple = Rmul(P, Radd(R1, Rmul(r, t)));         /* simple interest, exact */
    rows.push(trow([
      cell('continuously'), cell('&rarr; unbounded'), cell('&mdash;'), cell(contv.toFixed(2)),
      cell(chip('irrational', 'hi')),
      cell(((Math.exp(Rfloat(r)) - 1) * 100).toFixed(4) + '% (rounded)'), cell('0.000000')
    ], 'focus'));
    rows.push(trow([
      cell('not at all: simple interest'), cell('&mdash;'), cell('&mdash;'), cell(Rdecimal(simple, 2)),
      cell(chip('exact', 'ok')), cell(pct(r, 4)), cell((contv - Rfloat(simple)).toFixed(6))
    ]));

    work.innerHTML = ttable('the same money, compounded seven different ways',
      ['compounded', 'n', 'n&middot;t', 'balance after ' + years + ', to the cent', 'arithmetic',
       'effective annual rate', 'gap to continuous'], rows)
      + steps('why the last two rows are different in kind', [
        ['the exact rows', 'A = P(1 + r/n)^(nt) is a product of fractions whenever n&middot;t is a '
          + 'whole number, so those balances are exact and are rounded to the cent once, at the '
          + 'end. Where n&middot;t is not whole &mdash; half a year compounded once a year &mdash; '
          + 'the power is a root and is generally irrational, and the row says so instead of '
          + 'pretending.'],
        ['the continuous row', 'A = Pe^(rt), and e is irrational: that balance is a rounding no '
          + 'matter how it is computed. It is the limit of the column above it rather than a '
          + 'seventh frequency you could ask a bank for.'],
        ['simple interest', 'P(1 + rt) = ' + Rshow(simple, 2) + ', exactly: the rate applied once '
          + 'to the original principal, with the interest never earning anything itself. The gap '
          + 'between that row and the first one is the whole subject.']
      ]);

    var Pv = Rfloat(P), rv = Rfloat(r), tv = Rfloat(t);
    var hi = Math.max(Pv, contv, Pv * (1 + rv * tv)), lowv = Math.min(Pv, contv, Pv * (1 + rv * tv));
    var plot = Plot(svg, { xmin: 0, xmax: Math.max(tv, 0.0001),
                           ymin: Math.min(0, lowv * 0.9), ymax: hi * 1.08 + 0.001 });
    plot.frame();
    plot.curve(function (s) { return Pv * Math.pow(1 + rv, s); });
    plot.curve(function (s) { return Pv * Math.pow(1 + rv / 12, 12 * s); }, 'plot-curve alt');
    plot.curve(function (s) { return Pv * Math.exp(rv * s); }, 'plot-curve good');
    plot.curve(function (s) { return Pv * (1 + rv * s); }, 'plot-curve parent');
    plot.describe('the balance over ' + years + ' compounded yearly, monthly and '
      + 'continuously, with simple interest as the straight line below them.');

    setkpis(annual.shown, contv.toFixed(2), (contv - annual.value).toFixed(6));

    var apy12 = Rsub(Rpowfast(Radd(R1, Rdiv(r, R(12n))), 12), R1);
    status.innerHTML = '<strong>' + Rtext(rpc) + '% a year compounded monthly is not '
      + Rtext(rpc) + '% a year.</strong> Twelve payments of ' + pct(Rdiv(r, R(12n)), 6)
      + ' compound to an effective ' + pct(apy12, 4) + ' &mdash; exactly, from the fraction '
      + '(1 + r/12)^12 - 1 &mdash; and the difference is interest earning interest. Raising the '
      + 'frequency raises the balance every time, but never past a ceiling: the daily row reaches '
      + daily.shown + ' against the continuous ' + contv.toFixed(2) + ', and the gap between them '
      + 'is ' + (contv - daily.value).toFixed(6) + ' on a principal of ' + Rtext(P)
      + '. That ceiling is Pe^(rt), and the e in it is the number (1 + 1/n)^n was climbing toward.';
  }

  function redraw() {
    if (MODE === 'intro') drawIntro();
    else if (MODE === 'growth') drawGrowth();
    else if (MODE === 'e') drawE();
    else drawInterest();
  }

  function applyPreset() {
    var parts = (preset.value || '').split('|');
    FIELDS.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (el && parts[i] !== undefined) el.value = parts[i];
    });
    redraw();
  }

  preset.addEventListener('change', applyPreset);
  FIELDS.concat(RANGES).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', redraw);
  });
  applyPreset();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an example, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every value in the tables is an exact fraction, recomputed from the definition "
            "when you change these. Only the drawing and the genuinely irrational quantities "
            "are decimals, and those say so where they appear.",
        ),
        script=script,
    )


# --------------------------------------------------------------------------
# logarithm_lab
#
# The presets carry the lesson. Each mode includes the case that refuses to
# work: an argument of zero, a base of 1, an equation whose only candidate is
# outside the domain, a pH difference that is not a whole number of decades.
# A reader who only ever sees log_2(8) learns that logs are lookup; a reader who
# watches the exponent search come back empty on log_2(10) learns what they are.

LOG_PRESETS = {
    "define": [
        ("log_2(8)", "2", "8"),
        ("log_10(1/1000)", "10", "1/1000"),
        ("log_9(3) &mdash; the exponent is a fraction", "9", "3"),
        ("log_2(10) &mdash; the search comes back empty", "2", "10"),
        ("log_2(0) &mdash; no power of 2 is ever 0", "2", "0"),
        ("log_1(5) &mdash; base 1 cannot be undone", "1", "5"),
    ],
    "graph": [
        ("base 2", "2", "3"),
        ("base 10", "10", "2"),
        ("base 1/2 &mdash; both curves fall", "1/2", "2"),
        ("base 3/2 &mdash; a gentle base", "3/2", "2"),
        ("base e &mdash; irrational, so these are decimals", "e", "1"),
        ("base 1 &mdash; constant, so it has no inverse", "1", "2"),
    ],
    "laws": [
        ("base 2, M = 8, N = 4", "2", "8", "4", "3"),
        ("base 10, M = 1000, N = 100", "10", "1000", "100", "2"),
        ("base 2, M = N = 8 &mdash; the invented laws at their worst", "2", "8", "8", "2"),
        ("base 3, M = 1/9, N = 27", "3", "1/9", "27", "-2"),
        ("base 4, M = 8, N = 2 &mdash; fractional exponents", "4", "8", "2", "2"),
        ("base 2, M = 5, N = 6 &mdash; no exact logs, so the check is numerical", "2", "5", "6", "3"),
    ],
    "common": [
        ("x = 5000", "5000"),
        ("x = 1/500, which is 0.002", "1/500"),
        ("x = 1 &mdash; the log is exactly 0", "1"),
        ("x = 10000000 &mdash; exact, all characteristic", "10000000"),
        ("x = 7 &mdash; the mantissa is irrational", "7"),
        ("x = 0 &mdash; there is no answer to give", "0"),
    ],
    "base": [
        ("log_7(343)", "7", "343"),
        ("log_9(27) &mdash; exact, through base 3", "9", "27"),
        ("log_2(10) &mdash; three helper bases must agree", "2", "10"),
        ("log_5(1/125)", "5", "1/125"),
        ("log_4(2)", "4", "2"),
        ("log_6(0) &mdash; outside the domain", "6", "0"),
    ],
    "solveexp": [
        ("2^x = 32", "1", "2", "1", "0", "32"),
        ("3^(2x - 1) = 27", "1", "3", "2", "-1", "27"),
        ("4^x = 8 &mdash; one base underneath both", "1", "4", "1", "0", "8"),
        ("5 &middot; 2^x = 160", "5", "2", "1", "0", "160"),
        ("2^x = 10 &mdash; only logs will do it", "1", "2", "1", "0", "10"),
        ("3 &middot; 2^x = -12 &mdash; no solution at all", "3", "2", "1", "0", "-12"),
    ],
    "solvelog": [
        ("log_2(x) + log_2(x - 2) = 3", "sum", "2", "0", "2", "3"),
        ("log_10(x) + log_10(x + 3) = 1", "sum", "10", "0", "-3", "1"),
        ("log_2(x) - log_2(x + 3) = 1 &mdash; no solution", "diff", "2", "0", "-3", "1"),
        ("log_5(x - 1) - log_5(x - 4) = 0 &mdash; no solution", "diff", "5", "1", "4", "0"),
        ("log_3(x^2 - 7) = 2 &mdash; both answers survive", "square", "3", "7", "0", "2"),
        ("log_2(x^2 + 20) = 2 &mdash; no real solution", "square", "2", "-20", "0", "2"),
    ],
    "scale": [
        ("a 120 dB jet against a 60 dB office", "db", "120", "60"),
        ("60 dB, and a second 60 dB source", "db", "60", "60"),
        ("pH 3 lemon against pH 7 water", "ph", "3", "7"),
        ("pH 7.4 blood against pH 7 water", "ph", "7.4", "7"),
        ("magnitude 8 against magnitude 5", "rich", "8", "5"),
        ("magnitude 6 against magnitude 5.5", "rich", "6", "5.5"),
    ],
}

LOG_TITLES = {
    "define": ("Two ways to say one thing", "log_b(x) = y and b^y = x are the same sentence"),
    "graph": ("The graph, and its reflection", "y = b^x and y = log_b(x) across the line y = x"),
    "laws": ("The laws, checked", "Three that hold, two that people invent"),
    "common": ("Base 10 and base e", "The characteristic is exact; the mantissa is not"),
    "base": ("Change of base", "Derived, then checked through three different bases"),
    "solveexp": ("Solving b^(cx+d) = k", "Match the powers when you can; take logs when you cannot"),
    "solvelog": ("Solving a logarithmic equation", "The domain check is a step, not a formality"),
    "scale": ("Scales that are logarithms", "Decibels, pH and magnitude"),
}

LOG_LEGEND = {
    "define": [("tone-cyan", "y = b^t"), ("tone-red", "the value x"), ("tone-amber", "the exponent")],
    "graph": [("tone-cyan", "y = b^x"), ("tone-purple", "y = log_b(x)"), ("tone-muted", "y = x"),
              ("tone-red", "asymptotes")],
    "laws": [("tone-cyan", "y = log_b(x)"), ("tone-amber", "M, N and MN"),
             ("tone-muted", "the heights that add")],
    "common": [("tone-cyan", "y = log_10(x)"), ("tone-purple", "y = ln(x)"), ("tone-amber", "your x")],
    "base": [("tone-cyan", "y = log_b(x)"), ("tone-purple", "the helper bases"), ("tone-amber", "your x")],
    "solveexp": [("tone-cyan", "the left side"), ("tone-red", "y = k"), ("tone-green", "the solution")],
    "solvelog": [("tone-cyan", "the left side, on its domain"), ("tone-red", "y = k"),
                 ("tone-green", "accepted"), ("tone-muted", "rejected")],
    "scale": [("tone-cyan", "the span between them"), ("tone-amber", "the two readings")],
}

LOG_KPIS = {
    "define": [("log_b(x)", "lgKpi1"), ("Written as a power", "lgKpi2"), ("Exact?", "lgKpi3")],
    "graph": [("b^x at your x", "lgKpi1"), ("The mirrored point", "lgKpi2"), ("Direction", "lgKpi3")],
    "laws": [("Laws that held", "lgKpi1"), ("Invented laws that held", "lgKpi2"), ("Checked", "lgKpi3")],
    "common": [("Characteristic", "lgKpi1"), ("log_10(x)", "lgKpi2"), ("ln(x)", "lgKpi3")],
    "base": [("log_b(x)", "lgKpi1"), ("Through base 10", "lgKpi2"), ("Helper bases agree?", "lgKpi3")],
    "solveexp": [("x", "lgKpi1"), ("Method", "lgKpi2"), ("Check", "lgKpi3")],
    "solvelog": [("Candidates", "lgKpi1"), ("Accepted", "lgKpi2"), ("Rejected", "lgKpi3")],
    "scale": [("Difference", "lgKpi1"), ("Factor", "lgKpi2"), ("Exact?", "lgKpi3")],
}

LOG_FIELDS = {
    "define": ["lgBase", "lgX"],
    "graph": ["lgBase", "lgX"],
    "laws": ["lgBase", "lgM", "lgN", "lgP"],
    "common": ["lgX"],
    "base": ["lgBase", "lgX"],
    "solveexp": ["lgA", "lgBase", "lgC", "lgD", "lgK"],
    "solvelog": ["lgShape", "lgBase", "lgP", "lgQ", "lgK"],
    "scale": ["lgScale", "lgV1", "lgV2"],
}

LOG_HINT = {
    "define": "Whole numbers or fractions. The lab searches for an exact exponent first and only "
              "reaches for a decimal when the search fails.",
    "graph": "Type <code>e</code> as the base to see the natural logarithm; every number for that "
             "base is a decimal, and the panel says so.",
    "laws": "p has to be a whole number, so that M^p is exact and the check can be exact too.",
    "common": "Any positive number. The characteristic comes from comparing x with powers of ten, "
              "which is exact arithmetic; only the mantissa is rounded.",
    "base": "The helper bases are 10, e and 2. They are not special &mdash; they are the ones a "
            "calculator happens to carry.",
    "solveexp": "The equation is a&middot;b^(cx + d) = k. Set a = 1 and d = 0 for the plain case.",
    "solvelog": "k has to be a whole number so that b^k is exact. The shape picker changes the "
                "equation; p and q are the numbers subtracted inside the logarithms.",
    "scale": "Two readings on the same scale. A difference of 1 is a factor on the quantity, and "
             "the lab shows which factor.",
}


def logarithm_lab(cfg):
    """The logarithm: definition, graph, laws, common bases, equations, scales.

    Nothing here calls a logarithm to answer a question about a logarithm. An
    exact value is found by searching for a rational exponent p/q with
    b^p = x^q, which is exact rational arithmetic; a value the search cannot
    find is bracketed between two integer powers, also exactly, and only then
    printed as a rounded decimal that says it is one.
    """
    mode = cfg.get("mode", "define")
    if mode not in LOG_PRESETS:
        mode = "define"
    presets = cfg.get("presets") or LOG_PRESETS[mode]
    title, subtitle = LOG_TITLES[mode]

    markup = ('      <div class="lab-toolbar">\n'
              '        <div class="lab-title"><strong id="lgTitle">Logarithm</strong>'
              '<span id="lgSub"></span></div>\n'
              "        " + _legend(LOG_LEGEND[mode]) + "\n"
              "      </div>\n"
              '      <div class="lab-stage"><svg id="lgPlot"></svg></div>\n'
              '      <div id="lgWork" style="margin-top:12px;"></div>\n'
              '      <div class="status-banner" id="lgStatus" style="margin-top:12px;"></div>')

    controls = _select("lgPreset", "Example", presets)
    if mode == "solvelog":
        controls += _select("lgShape", "Shape of the equation", [
            ("log_b(x - p) + log_b(x - q) = k", "sum"),
            ("log_b(x - p) - log_b(x - q) = k", "diff"),
            ("log_b(x^2 - p) = k", "square"),
            ("log_b(x - p) = k", "single"),
        ])
    if mode == "scale":
        controls += _select("lgScale", "Scale", [
            ("decibels: L = 10 log_10(I / I0)", "db"),
            ("pH = -log_10(concentration)", "ph"),
            ("magnitude: M = log_10(A / A0)", "rich"),
        ])
    if mode in ("define", "graph", "laws", "base", "solveexp", "solvelog"):
        controls += _text_field("lgBase", "b (the base)", "2")
    if mode in ("define", "graph", "common", "base"):
        controls += _text_field("lgX", "x (the argument)" if mode != "graph" else "x (the point to trace)", "8")
    if mode == "laws":
        controls += _text_field("lgM", "M", "8")
        controls += _text_field("lgN", "N", "4")
        controls += _text_field("lgP", "p (a whole number)", "3")
    if mode == "solveexp":
        controls += _text_field("lgA", "a (the coefficient)", "1")
        controls += _text_field("lgC", "c (the coefficient of x)", "1")
        controls += _text_field("lgD", "d (added to the exponent)", "0")
        controls += _text_field("lgK", "k (the right-hand side)", "32")
    if mode == "solvelog":
        controls += _text_field("lgP", "p", "0")
        controls += _text_field("lgQ", "q", "2")
        controls += _text_field("lgK", "k (a whole number)", "3")
    if mode == "scale":
        controls += _text_field("lgV1", "first reading", "60")
        controls += _text_field("lgV2", "second reading", "120")
    controls += _kpi_grid(LOG_KPIS[mode])
    controls += '        <p class="small-copy" id="lgHint" style="margin:0;">' + LOG_HINT[mode] + "</p>\n"

    script = RATIONAL_JS + POLY_JS + SURD_JS + PLOT_JS + NUMERIC_JS + r"""
  var MODE = '""" + mode + r"""';
  var FIELDS = """ + _js_list(LOG_FIELDS[mode]) + r""";
  var preset = document.getElementById('lgPreset');
  var svg = document.getElementById('lgPlot');
  var work = document.getElementById('lgWork'), status = document.getElementById('lgStatus');
  var titleOut = document.getElementById('lgTitle'), subOut = document.getElementById('lgSub');
  var kpi1 = document.getElementById('lgKpi1');
  var kpi2 = document.getElementById('lgKpi2');
  var kpi3 = document.getElementById('lgKpi3');

  function readnum(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return Rparse(el.value); } catch (err) { return null; }
  }
  function readtext(id) {
    var el = document.getElementById(id);
    return el ? String(el.value).trim() : '';
  }
  /* The base, which is the one input that may be the irrational e. Modes that
     need exact arithmetic refuse it by name rather than by silently rounding. */
  function readbase(id) {
    var raw = readtext(id);
    if (raw.toLowerCase() === 'e') return { kind: 'e', v: Math.E, text: 'e' };
    var r = readnum(id);
    return r === null ? null : { kind: 'q', r: r, v: Rfloat(r), text: Rterm(r) };
  }
  function setkpis(a, b, c) { kpi1.innerHTML = a; kpi2.innerHTML = b; kpi3.innerHTML = c; }
  function blankStage() {
    var p = Plot(svg, { xmin: -1, xmax: 9, ymin: -4, ymax: 4 });
    p.frame();
    p.describe('an empty frame: the values in the panel do not describe a logarithm.');
    return p;
  }
  function fail(message) {
    status.innerHTML = message;
    work.innerHTML = '';
    setkpis('&mdash;', '&mdash;', '&mdash;');
    blankStage();
  }
  /* "x", "x - 2", "x + 3" -- the argument of a logarithm, written the way it
     would be written by hand. */
  function argtext(p) {
    if (Rzero(p)) return 'x';
    return Rsign(p) > 0 ? 'x - ' + Rtext(p) : 'x + ' + Rtext(Rneg(p));
  }
  function logname(b, arg) { return 'log_' + b + '(' + arg + ')'; }

  /* Every mode that needs one uses the same sentence for a refusal, so the
     reader meets the same three conditions on a base everywhere. */
  function baseProblem(bb, allowOne) {
    if (bb === null) return '<strong>The base has to be a whole number or a fraction.</strong> '
      + 'Try 2, 10 or 3/2.';
    if (bb.kind === 'e') return null;
    if (allowOne && Requ(bb.r, R1) && Rsign(bb.r) > 0) return null;   /* the graph draws it */
    if (Rsign(bb.r) <= 0) {
      return '<strong>A base has to be positive.</strong> With b = ' + Rtext(bb.r)
        + ', b^(1/2) is not a real number, so b^y is not defined for every y and the exponent '
        + 'cannot be undone. That is the whole reason the definition insists on b &gt; 0.';
    }
    if (Requ(bb.r, R1)) {
      return '<strong>Base 1 has no logarithm.</strong> 1^y = 1 for every y, so 1^y = x has no '
        + 'solution at all when x is not 1, and every y at once when x is 1. A function that is '
        + 'constant cannot be inverted, which is exactly what a logarithm is: an inverse.';
    }
    return null;
  }

  /* ----------------------------------------------------------- define ---- */

  function drawDefine() {
    var bb = readbase('lgBase'), x = readnum('lgX');
    var problem = baseProblem(bb);
    if (problem) { fail(problem); return; }
    if (bb.kind === 'e') {
      fail('<strong>This mode needs an exact base.</strong> e is irrational, so there is no '
        + 'fraction p/q with e^p = x^q to search for and nothing here could be exact. Try 2, 10 or '
        + '9; the graph mode will draw base e.');
      return;
    }
    if (x === null) {
      fail('<strong>x has to be a whole number or a fraction.</strong> Try 8, 1/1000 or 10.');
      return;
    }
    var b = bb.r;
    titleOut.textContent = 'log_' + Rterm(b) + '(' + Rtext(x) + ') = y   means   '
      + Rterm(b) + '^y = ' + Rtext(x);
    subOut.textContent = 'one fact, written two ways';

    /* The table is the definition, read in both directions. */
    var rows = [], k;
    for (k = -3; k <= 3; k += 1) {
      var v = Rpow(b, k);
      rows.push(trow([
        cell(Rterm(b) + '^' + k + ' = ' + Rshow(v)),
        cell('log_' + Rterm(b) + '(' + Rshow(v) + ') = ' + k),
        cell(Requ(v, x) ? chip('this is your x', 'ok') : '')
      ], Requ(v, x) ? 'focus' : ''));
    }
    var blocks = [ttable('the same seven facts, each written both ways',
      ['as a power', 'as a logarithm', ''], rows)];

    var lv = logvalue(b, x);
    var pairs = [];
    if (lv.kind === 'domain') {
      pairs.push(['the question', 'log_' + Rterm(b) + '(' + Rtext(x) + ') asks for a y with '
        + Rterm(b) + '^y = ' + Rtext(x) + '.']);
      pairs.push(['why there is no answer', 'every entry in the middle column above is positive, '
        + 'and that is not an accident of the range shown: a positive base raised to any real '
        + 'power is positive. So no y gives ' + Rtext(x)
        + ', and log_' + Rterm(b) + '(' + Rtext(x) + ') is undefined. The domain of a logarithm is '
        + 'x &gt; 0, and it is the range of the exponential turned on its side.']);
    } else if (lv.kind === 'exact') {
      var y = lv.y;
      pairs.push(['the search', 'looking for an exponent p/q with ' + Rterm(b) + '^p = '
        + Rtext(x) + '^q, over every p from -48 to 48 and every q up to 12.']);
      pairs.push(['it found one', 'p/q = ' + Rtext(y) + ', so log_' + Rterm(b) + '('
        + Rtext(x) + ') = ' + Rtext(y) + ' exactly.']);
      var lhs = Rpow(b, Number(y.n)), rhs = Rpow(x, Number(y.d));
      pairs.push(['the check, in exact arithmetic', Rterm(b) + '^' + String(y.n) + ' = ' + Rshow(lhs)
        + ' and ' + Rterm(x) + '^' + String(y.d) + ' = ' + Rshow(rhs) + '. '
        + (Requ(lhs, rhs) ? 'They are equal, so the exponent is right.' : 'They differ.')]);
    } else {
      pairs.push(['the search', 'no p/q with |p| &le; 48 and q &le; 12 satisfies ' + Rterm(b)
        + '^p = ' + Rtext(x) + '^q, and x is not a whole power of ' + Rterm(b)
        + ' either. So the answer is not a fraction of that size; where no fraction works at all, '
        + 'the logarithm is irrational and no decimal will ever be equal to it.']);
      if (lv.br) {
        pairs.push(['what is still exact', Rterm(b) + '^' + lv.br.k + ' = ' + Rshow(lv.br.low)
          + ' and ' + Rterm(b) + '^' + (lv.br.k + 1) + ' = ' + Rshow(lv.br.high) + ', and '
          + Rshow(lv.br.low) + ' &lt; ' + Rtext(x) + ' &lt; ' + Rshow(lv.br.high)
          + '. So ' + lv.br.k + ' &lt; log_' + Rterm(b) + '(' + Rtext(x) + ') &lt; ' + (lv.br.k + 1)
          + ', proved by multiplication alone.']);
      }
      pairs.push(['only now, a decimal', 'log_' + Rterm(b) + '(' + Rtext(x) + ') &asymp; '
        + lv.v.toFixed(8) + ', rounded to 8 places. It is a rounding of an irrational number and '
        + 'not the number itself.']);
    }
    blocks.push(steps('your x', pairs));
    work.innerHTML = blocks.join('');

    /* The picture is the definition too: the height of b^t reaching x. */
    var bv = Rfloat(b), xv = Rfloat(x);
    var yv = lv.kind === 'exact' ? Rfloat(lv.y) : (lv.kind === 'searched' ? lv.v : null);
    var lo = -3, hi = 3;
    if (yv !== null && isFinite(yv)) { lo = Math.min(lo, yv - 1); hi = Math.max(hi, yv + 1); }
    var top = Math.max(Math.abs(xv) * 1.4, Math.pow(bv, hi), 2);
    if (!isFinite(top) || top > 1e6) top = Math.max(Math.abs(xv) * 1.4, 2);
    var plot = Plot(svg, { xmin: lo, xmax: hi, ymin: -top * 0.12, ymax: top });
    plot.frame();
    plot.curve(function (t) { return Math.pow(bv, t); });
    if (Rsign(x) > 0) plot.hline(xv, 'plot-asym', 'y = ' + Rtext(x));
    if (yv !== null && isFinite(yv)) {
      plot.segment(yv, 0, yv, xv, 'plot-aux');
      plot.point(yv, xv, 'plot-point', 'y = ' + (lv.kind === 'exact' ? Rtext(lv.y) : lv.v.toFixed(4)));
    }
    plot.describe('the curve y = ' + Rterm(b) + '^t with the horizontal line y = ' + Rtext(x)
      + ', meeting where t is the logarithm.');

    if (lv.kind === 'exact') {
      setkpis(Rtext(lv.y), Rterm(b) + '^' + Rterm(lv.y) + ' = ' + Rtext(x), chip('exact', 'ok'));
      status.innerHTML = '<strong>log_' + Rterm(b) + '(' + Rtext(x) + ') = ' + Rtext(lv.y)
        + ', and that is a statement about an exponent.</strong> The logarithm asks one question '
        + 'and only one: what power of ' + Rterm(b) + ' gives ' + Rtext(x)
        + '? Every row of the table above is the same question answered in advance, read left to '
        + 'right as a power and right to left as a logarithm. Nothing was looked up &mdash; the '
        + 'exponent was searched for in exact arithmetic and then checked by raising ' + Rterm(b)
        + ' to it.';
    } else if (lv.kind === 'domain') {
      setkpis('undefined', 'no y at all', chip('outside the domain', 'no'));
      status.innerHTML = '<strong>There is no such exponent.</strong> log_' + Rterm(b) + '('
        + Rtext(x) + ') would be a y with ' + Rterm(b) + '^y = ' + Rtext(x)
        + ', and a positive base raised to a real power is always positive &mdash; large for big y, '
        + 'small for very negative y, and never zero or below. The curve above has the horizontal '
        + 'axis as an asymptote for exactly this reason, which is why the domain of every '
        + 'logarithm is x &gt; 0.';
    } else {
      setkpis('&asymp; ' + lv.v.toFixed(6),
        lv.br ? (lv.br.k + ' &lt; y &lt; ' + (lv.br.k + 1)) : 'between two powers',
        chip('no exact power', 'hi'));
      status.innerHTML = '<strong>The exact search came back empty, and that is the answer.</strong> '
        + 'No fraction p/q in the search range has ' + Rterm(b) + '^p = ' + Rtext(x) + '^q, so '
        + 'log_' + Rterm(b) + '(' + Rtext(x) + ') is not a fraction of that size &mdash; and for a '
        + 'pair like this one no fraction works at all, which is what "irrational" means. What is '
        + 'still exact is the bracket: '
        + (lv.br ? (Rshow(lv.br.low) + ' &lt; ' + Rtext(x) + ' &lt; ' + Rshow(lv.br.high) + ', so '
                    + lv.br.k + ' &lt; log_' + Rterm(b) + '(' + Rtext(x) + ') &lt; ' + (lv.br.k + 1) + '. ')
                 : '')
        + 'The decimal ' + lv.v.toFixed(8) + ' comes last, and it is a rounding.';
    }
  }

  /* ------------------------------------------------------------ graph ---- */

  function drawGraph() {
    var bb = readbase('lgBase'), x = readnum('lgX');
    /* Base 1 is allowed IN here, on purpose: the reader is meant to watch a
       constant function fail to have an inverse rather than be told it does. */
    var problem = baseProblem(bb, true);
    if (problem) { fail(problem); return; }
    if (x === null) {
      fail('<strong>The point to trace has to be a number.</strong> It is the x at which the two '
        + 'curves are sampled; try 1, 2 or 3.');
      return;
    }
    var exact = bb.kind === 'q';
    var bv = bb.v, btext = bb.text;
    var constant = exact && Requ(bb.r, R1);
    titleOut.textContent = 'y = ' + btext + '^x   and   y = log_' + btext + '(x)';
    subOut.textContent = constant ? 'a constant function has no inverse'
                                  : 'each is the other reflected in y = x';

    var rows = [], t;
    for (t = -2; t <= 3; t += 1) {
      var v = exact ? Rpow(bb.r, t) : Math.pow(bv, t);
      var vtext = exact ? Rshow(v) : v.toFixed(6);
      rows.push(trow([
        cell(String(t)), cell(vtext),
        cell('(' + t + ', ' + vtext + ')'),
        cell('(' + vtext + ', ' + t + ')'),
        cell(exact ? chip('exact', 'ok') : chip('rounded', 'no'))
      ]));
    }
    var pairs = [
      ['the exponential', constant
        ? 'domain: every real x. Range: the single value 1. A constant function is still a '
          + 'function, and that is the only good thing to say about this one.'
        : 'domain: every real x. Range: y &gt; 0. It has the horizontal line y = 0 as an asymptote '
          + 'and never touches it.'],
      ['the logarithm', constant
        ? 'there is none. Undoing 1^x would mean answering "which x gave this 1?", and every x did.'
        : 'domain: x &gt; 0. Range: every real y. It has the vertical line x = 0 as an asymptote '
          + '&mdash; the same asymptote, reflected.'],
      ['the reflection', constant
        ? 'the fourth column is still the third column with its coordinates swapped, and look at '
          + 'what it produces: (1, -2), (1, -1), (1, 0), ... one x with every y at once. That is a '
          + 'vertical line, and a vertical line is not the graph of a function. There is no log '
          + 'base 1 to draw, which is why the picture above has only one curve.'
        : 'swapping the coordinates of a point is exactly what reflecting in y = x does, and the '
          + 'fourth column above is the third column with its pair swapped. That is the whole '
          + 'relationship: log_' + btext + ' undoes ' + btext + '^x, so its graph is that graph '
          + 'seen from the other axis.']
    ];
    if (!constant && !exact) {
      pairs.push(['base e', 'e is irrational, so every value in the table is a decimal rounded to '
        + '6 places rather than a fraction. The shape of the picture is unaffected; the exactness '
        + 'is what is lost, and it is worth noticing where.']);
    }
    work.innerHTML = ttable('points on one curve, and the same points on the other',
      ['t', btext + '^t', 'on y = ' + btext + '^x',
       constant ? 'reflected in y = x' : 'on y = log_' + btext + '(x)', 'arithmetic'], rows)
      + steps('what the reflection means', pairs);

    var span = Math.max(4, Math.abs(Rfloat(x)) + 2);
    var lim = Math.min(span, 12);
    var plot = Plot(svg, { xmin: -lim, xmax: lim, ymin: -lim, ymax: lim });
    plot.frame();
    plot.curve(function (t) { return t; }, 'plot-curve parent');
    plot.hline(0, 'plot-asym', 'y = 0');
    plot.vline(0, 'plot-asym', 'x = 0');
    plot.curve(function (t) { return Math.pow(bv, t); });
    if (!constant) {
      plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.log(bv) : NaN; }, 'plot-curve alt');
    }
    var xv = Rfloat(x), yv = Math.pow(bv, xv);
    if (isFinite(yv) && Math.abs(yv) < 1e6) {
      plot.point(xv, yv, 'plot-point', '(' + Rtext(x) + ', ' + yv.toFixed(3) + ')');
      if (!constant) plot.point(yv, xv, 'plot-point vertex', '(' + yv.toFixed(3) + ', ' + Rtext(x) + ')');
      plot.segment(xv, yv, yv, xv, 'plot-aux');
    }
    plot.describe('y = ' + btext + '^x and y = log_' + btext + '(x) drawn together with the line '
      + 'y = x, and one point shown on both curves with its coordinates swapped.');

    setkpis(isFinite(yv) ? (exact ? Rshow(Rpow(bb.r, Math.round(xv))) : yv.toFixed(6)) : 'too large',
      '(' + (isFinite(yv) ? yv.toFixed(3) : '?') + ', ' + Rtext(x) + ')',
      constant ? 'flat' : (bv > 1 ? 'both rise' : 'both fall'));

    if (constant) {
      status.innerHTML = '<strong>Base 1 is where the picture stops working.</strong> y = 1^x is a '
        + 'horizontal line, and every horizontal line fails the test an inverse needs: two '
        + 'different x values share one y, so undoing it has no single answer. Reflected in y = x '
        + 'the line becomes vertical, which is not the graph of a function at all. That is why '
        + 'b = 1 is excluded from the definition, and it is the same exclusion that kept it out '
        + 'of the exponential.';
    } else {
      status.innerHTML = '<strong>The two curves are one curve, looked at from the other axis.</strong> '
        + (bv > 1 ? 'With b = ' + btext + ' &gt; 1 both rise: the exponential steeply and the '
                    + 'logarithm ever more slowly. '
                  : 'With 0 &lt; b = ' + btext + ' &lt; 1 both fall, which is the case people '
                    + 'forget: a logarithm is not automatically an increasing function. ')
        + 'The traced point is at ' + Rtext(x) + ' on the exponential, and the same pair of numbers '
        + 'in the other order sits on the logarithm, on the far side of the dashed line y = x. '
        + 'The exponential\'s horizontal asymptote y = 0 reflects to the logarithm\'s vertical '
        + 'asymptote x = 0, which is the graph saying what the domain already said: the argument '
        + 'of a logarithm is positive, and as it approaches zero the log falls without bound.';
    }
  }

  /* ------------------------------------------------------------- laws ---- */

  /* A quantity that may or may not be exact, so that a law can be CHECKED
     exactly when both sides are exact and numerically when they are not --
     and can say which of the two just happened. */
  function Q(lv) {
    return lv.kind === 'exact' ? { exact: true, r: lv.y, v: Rfloat(lv.y) }
                               : { exact: false, r: null, v: lv.v };
  }
  function Qnum(r) { return { exact: true, r: r, v: Rfloat(r) }; }
  function Qadd(a, b) {
    return (a.exact && b.exact) ? Qnum(Radd(a.r, b.r)) : { exact: false, r: null, v: a.v + b.v };
  }
  function Qsub(a, b) {
    return (a.exact && b.exact) ? Qnum(Rsub(a.r, b.r)) : { exact: false, r: null, v: a.v - b.v };
  }
  function Qmul(a, b) {
    return (a.exact && b.exact) ? Qnum(Rmul(a.r, b.r)) : { exact: false, r: null, v: a.v * b.v };
  }
  function Qdiv(a, b) {
    if (a.exact && b.exact && !Rzero(b.r)) return Qnum(Rdiv(a.r, b.r));
    return { exact: false, r: null, v: a.v / b.v };
  }
  function Qtext(q, places) {
    if (q.exact) return Rtext(q.r);
    if (!isFinite(q.v)) return 'undefined';
    return '&asymp;&nbsp;' + q.v.toFixed(places === undefined ? 8 : places);
  }
  /* Equal exactly, or equal as far as a double can see. The distinction is
     reported rather than smoothed over. */
  function Qeq(a, b) {
    if (a.exact && b.exact) return { same: Requ(a.r, b.r), how: 'exact' };
    if (!isFinite(a.v) || !isFinite(b.v)) return { same: false, how: 'undefined' };
    return { same: Math.abs(a.v - b.v) < 1e-9, how: 'numerical' };
  }

  function drawLaws() {
    var bb = readbase('lgBase'), M = readnum('lgM'), N = readnum('lgN'), p = readnum('lgP');
    var problem = baseProblem(bb);
    if (problem) { fail(problem); return; }
    if (bb.kind === 'e') {
      fail('<strong>This mode needs an exact base.</strong> With e the checks below could only be '
        + 'numerical, and a law that is only ever checked to twelve decimal places is a law the '
        + 'reader has to take on trust. Try 2, 10, 3 or 4.');
      return;
    }
    if (M === null || N === null || p === null) {
      fail('<strong>M, N and p all have to be numbers.</strong> M and N are the arguments of the '
        + 'logarithms and p is the exponent in the power law.');
      return;
    }
    if (Rsign(M) <= 0 || Rsign(N) <= 0) {
      fail('<strong>Every law here is about log_b(M) and log_b(N), so M and N must be positive.</strong> '
        + 'With M = ' + Rtext(M) + ' and N = ' + Rtext(N) + ', at least one of those logarithms does '
        + 'not exist, and a law cannot be checked on a quantity that is undefined. That is not a '
        + 'technicality: it is why log(MN) = log M + log N needs both arguments positive even '
        + 'though the product of two negatives would be positive.');
      return;
    }
    if (!Rint(p) || p.n > 40n || p.n < -40n) {
      fail('<strong>p has to be a whole number between -40 and 40.</strong> M^p is then an exact '
        + 'fraction and the power law can be checked in fractions rather than to eight decimal '
        + 'places. A fractional p would make both sides approximate, which proves less; a huge one '
        + 'would make M^p a number with more digits than the page.');
      return;
    }
    var b = bb.r, pn = Number(p.n);
    titleOut.textContent = 'base ' + Rterm(b) + ',  M = ' + Rtext(M) + ',  N = ' + Rtext(N)
      + ',  p = ' + Rtext(p);
    subOut.textContent = 'every row below is computed twice, from each side';

    var lM = Q(logvalue(b, M)), lN = Q(logvalue(b, N)), lb = Q(logvalue(b, b));
    /* Each law is stated in general and then computed on these numbers, so the
       reader can see which statement the two value columns belong to. */
    function lg(v) { return 'log_' + Rterm(b) + '(' + Rshow(v) + ')'; }
    var laws = [
      ['the product law<br>log_b(MN) = log_b(M) + log_b(N)',
        lg(Rmul(M, N)), Q(logvalue(b, Rmul(M, N))), lg(M) + ' + ' + lg(N), Qadd(lM, lN)],
      ['the quotient law<br>log_b(M/N) = log_b(M) - log_b(N)',
        lg(Rdiv(M, N)), Q(logvalue(b, Rdiv(M, N))), lg(M) + ' - ' + lg(N), Qsub(lM, lN)],
      ['the power law<br>log_b(M^p) = p log_b(M)',
        lg(Rpow(M, pn)), Q(logvalue(b, Rpow(M, pn))), Rterm(p) + ' ' + lg(M), Qmul(Qnum(p), lM)],
      ['the log of 1<br>log_b(1) = 0', lg(R1), Q(logvalue(b, R1)), '0', Qnum(R0)],
      ['the log of the base<br>log_b(b) = 1', lg(b), lb, '1', Qnum(R1)],
      ['the reciprocal<br>log_b(1/N) = -log_b(N)',
        lg(Rinv(N)), Q(logvalue(b, Rinv(N))), '-' + lg(N), Qsub(Qnum(R0), lN)]
    ];
    var held = 0, anyNumeric = false;
    var rows = laws.map(function (law) {
      var verdict = Qeq(law[2], law[4]);
      if (verdict.same) held += 1;
      if (verdict.how === 'numerical') anyNumeric = true;
      return trow([
        rowhead(law[0]), cell(law[1]), cell(Qtext(law[2])), cell(law[3]), cell(Qtext(law[4])),
        cell(verdict.same ? 'holds' : 'FAILS', verdict.same ? 't' : 'f'),
        cell(verdict.how === 'exact' ? chip('exact', 'ok') : chip(verdict.how, 'hi'))
      ]);
    });

    /* The two laws nobody was taught and everybody writes down anyway. */
    var invented = [
      ['"the log of a sum is the sum of the logs"<br>log_b(M + N) = log_b(M) + log_b(N)',
        lg(Radd(M, N)), Q(logvalue(b, Radd(M, N))), lg(M) + ' + ' + lg(N), Qadd(lM, lN)],
      ['"dividing the arguments divides the logs"<br>log_b(M/N) = log_b(M) / log_b(N)',
        lg(Rdiv(M, N)), Q(logvalue(b, Rdiv(M, N))), lg(M) + ' / ' + lg(N), Qdiv(lM, lN)]
    ];
    var inventedHeld = 0;
    var irows = invented.map(function (law) {
      var verdict = Qeq(law[2], law[4]);
      if (verdict.same) inventedHeld += 1;
      return trow([
        rowhead(law[0]), cell(law[1]), cell(Qtext(law[2])), cell(law[3]), cell(Qtext(law[4])),
        cell(verdict.same ? 'holds here' : 'FAILS', verdict.same ? 't' : 'f'),
        cell(verdict.how === 'exact' ? chip('exact', 'ok') : chip(verdict.how, 'hi'))
      ]);
    });

    work.innerHTML = ttable('the laws, each side computed on its own',
      ['law', 'left side', 'value', 'right side', 'value', 'verdict', 'checked'], rows)
      + ttable('the two laws that do not exist, on the same numbers',
        ['the claim', 'left side', 'value', 'right side', 'value', 'verdict', 'checked'], irows)
      + steps('why the first six hold and the last two cannot', [
        ['where the laws come from', 'b^u &middot; b^v = b^(u+v). Write M = b^u and N = b^v and '
          + 'that line says log_b(MN) = u + v = log_b(M) + log_b(N). Every law in the first table '
          + 'is one exponent rule read backwards, which is why they need no separate proof.'],
        ['why the sum has no law', 'there is no rule turning b^u + b^v into a single power of b, '
          + 'so there is nothing for log_b(M + N) to be. The first row of the second table shows '
          + 'the gap on real numbers: ' + Qtext(Q(logvalue(b, Radd(M, N))), 6) + ' against '
          + Qtext(Qadd(lM, lN), 6) + '.'],
        ['why the quotient of logs is not the log of the quotient', 'log_b(M) / log_b(N) is a real '
          + 'thing &mdash; it is log_N(M), the change of base formula &mdash; and it answers a '
          + 'different question. The second row shows the two side by side: '
          + Qtext(Q(logvalue(b, Rdiv(M, N))), 6) + ' against ' + Qtext(Qdiv(lM, lN), 6) + '.'],
        ['what "checked exactly" means here', 'a row marked exact was decided by comparing two '
          + 'fractions, not two decimals. A row marked numerical had at least one irrational '
          + 'logarithm in it and was compared to within 1e-9, which is evidence rather than proof.']
      ]);

    /* The product law as a picture: three heights on one curve, two of them
       adding to the third. */
    var bv = Rfloat(b), Mv = Rfloat(M), Nv = Rfloat(N), MNv = Mv * Nv;
    var xmax = Math.max(MNv * 1.15, 2);
    if (!isFinite(xmax) || xmax > 1e6) xmax = Math.max(Mv, Nv) * 2 + 2;
    var lows = [Math.log(Mv), Math.log(Nv), Math.log(MNv)].map(function (v) { return v / Math.log(bv); });
    var ylo = Math.min.apply(null, lows.concat([0])), yhi = Math.max.apply(null, lows.concat([0]));
    var ypad = Math.max(0.6, (yhi - ylo) * 0.2);
    var plot = Plot(svg, { xmin: -xmax * 0.05, xmax: xmax, ymin: ylo - ypad, ymax: yhi + ypad });
    plot.frame();
    plot.vline(0, 'plot-asym', 'x = 0');
    plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.log(bv) : NaN; });
    [[Mv, 'M'], [Nv, 'N'], [MNv, 'MN']].forEach(function (item) {
      if (!isFinite(item[0]) || item[0] <= 0 || item[0] > xmax) return;
      var h = Math.log(item[0]) / Math.log(bv);
      plot.segment(item[0], 0, item[0], h, 'plot-aux');
      plot.point(item[0], h, 'plot-point', item[1]);
    });
    plot.describe('y = log_' + Rterm(b) + '(x) with M, N and MN marked, the height at MN being the '
      + 'sum of the heights at M and at N.');

    setkpis(held + ' of ' + laws.length, inventedHeld + ' of 2',
      anyNumeric ? chip('some numerically', 'hi') : chip('all exactly', 'ok'));

    var sameMN = Requ(M, N);
    status.innerHTML = '<strong>' + held + ' of the ' + laws.length + ' laws held on these numbers, '
      + 'and ' + (inventedHeld === 0 ? 'neither invented one did' : inventedHeld + ' of the invented ones did')
      + '.</strong> '
      + (sameMN
        ? 'With M = N the second table is at its clearest: log_b(M + N) is log_b of double M, one '
          + 'step further along the curve, while log_b(M) + log_b(N) is double the height &mdash; '
          + 'two completely different operations that happen to be spelled similarly. '
        : 'The gap is not small and it is not a rounding: the two columns in the second table are '
          + 'answers to different questions. ')
      + 'A law is a statement about every M and N, so one honest counterexample settles it, while '
      + 'no number of agreeing examples would prove it. The first table is a check, not a proof; '
      + 'the proof is the exponent rule quoted underneath it.';
  }

  /* ----------------------------------------------------------- common ---- */

  function drawCommon() {
    var x = readnum('lgX');
    if (x === null) {
      fail('<strong>x has to be a whole number or a fraction.</strong> Try 5000, 1/500 or 7.');
      return;
    }
    titleOut.textContent = 'log_10(' + Rtext(x) + ')   and   ln(' + Rtext(x) + ')';
    subOut.textContent = 'the two bases a calculator carries';
    if (Rsign(x) <= 0) {
      var plot0 = Plot(svg, { xmin: -1, xmax: 12, ymin: -3, ymax: 2 });
      plot0.frame();
      plot0.vline(0, 'plot-asym', 'x = 0');
      plot0.curve(function (t) { return t > 0 ? Math.log(t) / Math.LN10 : NaN; });
      plot0.curve(function (t) { return t > 0 ? Math.log(t) : NaN; }, 'plot-curve alt');
      plot0.describe('y = log_10(x) and y = ln(x), both stopping at x = 0, which is where the '
        + 'requested value lies.');
      work.innerHTML = steps('what happens at x = ' + Rtext(x), [
        ['the characteristic', 'there is none. The characteristic is the k with 10^k &le; x, and '
          + 'no power of ten is zero or negative, so the search has nothing to return.'],
        ['what a calculator does', 'it prints an error, or -Infinity for zero. -Infinity is not a '
          + 'number and not an answer: it is the machine reporting that log_10(x) falls without '
          + 'bound as x approaches 0 from above, which the curve above shows.'],
        ['the domain', 'x &gt; 0, for every base. The curve on the left of the picture simply does '
          + 'not exist.']
      ]);
      setkpis('none', 'undefined', 'undefined');
      status.innerHTML = '<strong>log_10(' + Rtext(x) + ') has no value.</strong> A logarithm asks '
        + 'for the exponent that produces x, and 10 raised to any real power is positive. As x '
        + 'falls toward 0 the logarithm falls without bound &mdash; which is a description of the '
        + 'asymptote, not a value at 0. Everything else in this mode needs x &gt; 0.';
      return;
    }

    /* The characteristic is found by comparing x with powers of ten. That part
       is exact; the mantissa is the part that is not. */
    var br = bracketexp(R(10n), x);
    if (br === null) {
      fail('<strong>That number is too far from 1 for this lab to bracket.</strong> The search '
        + 'multiplies by ten until it passes x, and it gives up after 2000 steps rather than '
        + 'pretending. Try something between 10^-100 and 10^100.');
      return;
    }
    var k = br.k, mant = Rdiv(x, Rpow(R(10n), k));
    var xv = Rfloat(x);
    var log10 = Math.log(xv) / Math.LN10, ln = Math.log(xv), log2 = Math.log(xv) / Math.LN2;
    var mantlog = Math.log(Rfloat(mant)) / Math.LN10;
    var exactly = Requ(mant, R1);

    work.innerHTML = ttable('the two parts of a common logarithm',
      ['part', 'value', 'where it comes from', 'arithmetic'], [
        trow([rowhead('x in scientific notation'), cell(Rshow(mant) + ' &times; 10^' + k),
          cell('10^' + k + ' = ' + Rshow(br.low) + ' &le; ' + Rtext(x) + ' &lt; '
            + Rshow(br.high) + ' = 10^' + (k + 1)), cell(chip('exact', 'ok'))]),
        trow([rowhead('characteristic'), cell(String(k)),
          cell('the whole number part: how many powers of ten fit inside x'), cell(chip('exact', 'ok'))]),
        trow([rowhead('mantissa'), cell(exactly ? '0' : '&asymp;&nbsp;' + mantlog.toFixed(8)),
          cell('log_10(' + Rshow(mant) + '), a number in [0, 1)'),
          cell(exactly ? chip('exact', 'ok') : chip('irrational', 'hi'))]),
        trow([rowhead('log_10(x)'), cell(exactly ? String(k) : '&asymp;&nbsp;' + log10.toFixed(8)),
          cell('characteristic + mantissa = ' + k + (exactly ? '' : ' + ' + mantlog.toFixed(8))),
          cell(exactly ? chip('exact', 'ok') : chip('rounded', 'no'))]),
        trow([rowhead('ln(x)'), cell('&asymp;&nbsp;' + ln.toFixed(8)),
          cell('log_10(x) &times; ln(10) = ' + log10.toFixed(8) + ' &times; ' + Math.LN10.toFixed(8)
            + ' &asymp; ' + (log10 * Math.LN10).toFixed(8) + ', which agrees'),
          cell(chip('rounded', 'no'))]),
        trow([rowhead('log_2(x)'), cell('&asymp;&nbsp;' + log2.toFixed(8)),
          cell('log_10(x) / log_10(2) &asymp; ' + (log10 / (Math.LN2 / Math.LN10)).toFixed(8)),
          cell(chip('rounded', 'no'))])
      ])
      + steps('why this split is the whole history of the subject', [
        ['ten times x has the same mantissa', 'x = ' + Rtext(x) + ' and 10x = ' + Rtext(Rmul(x, R(10n)))
          + ' differ by exactly 1 in the characteristic and not at all in the mantissa, because '
          + 'log_10(10x) = log_10(10) + log_10(x) = 1 + log_10(x). A table of logarithms therefore '
          + 'only ever had to list mantissas for numbers between 1 and 10; the reader supplied the '
          + 'characteristic by looking at the number.'],
        ['what is exact here', 'the characteristic ' + k + ' and the scientific-notation form '
          + Rshow(mant) + ' &times; 10^' + k + '. Both came from comparing fractions with powers of '
          + 'ten, which is multiplication and nothing else.'],
        ['what is not', exactly
          ? 'nothing, on this x: the mantissa is 0 because x is exactly a power of ten, so '
            + 'log_10(x) = ' + k + ' with no rounding anywhere.'
          : 'the mantissa. log_10(' + Rshow(mant) + ') is irrational, and every decimal in the '
            + 'last four rows is a rounding of it to 8 places.'],
        ['ln against log', 'the two differ by the constant factor ln(10) &asymp; '
          + Math.LN10.toFixed(8) + '. Which one a formula uses is a matter of convention, and the '
          + 'row above checks the conversion by computing ln(x) twice, once directly and once '
          + 'through log_10.']
      ]);

    var top = Math.max(xv * 1.3, 12);
    var plot = Plot(svg, { xmin: -top * 0.04, xmax: top,
                           ymin: Math.min(-2, ln - 2), ymax: Math.max(2, ln + 2) });
    plot.frame();
    plot.vline(0, 'plot-asym', 'x = 0');
    plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.LN10 : NaN; });
    plot.curve(function (t) { return t > 0 ? Math.log(t) : NaN; }, 'plot-curve alt');
    plot.point(xv, log10, 'plot-point', 'log_10 &asymp; ' + log10.toFixed(4));
    plot.point(xv, ln, 'plot-point vertex');
    plot.describe('y = log_10(x) and y = ln(x) with x = ' + Rtext(x) + ' marked on both.');

    setkpis(String(k), exactly ? String(k) : '&asymp; ' + log10.toFixed(6), '&asymp; ' + ln.toFixed(6));

    status.innerHTML = exactly
      ? '<strong>log_10(' + Rtext(x) + ') = ' + k + ' exactly.</strong> x is a whole power of ten, '
        + 'so the mantissa is zero and there is nothing to round. These are the only arguments for '
        + 'which a common logarithm is exact, which is worth remembering when a page prints '
        + 'log_10(2) = 0.3010 without a word about where the rest of the digits went.'
      : '<strong>The characteristic is ' + k + ' and it is exact; the mantissa is not.</strong> '
        + 'Writing x as ' + Rshow(mant) + ' &times; 10^' + k + ' splits log_10(x) into a whole '
        + 'number anybody can read off and an irrational remainder in [0, 1) that has to be '
        + 'computed. log_10(' + Rtext(x) + ') &asymp; ' + log10.toFixed(8) + ' is that sum, rounded '
        + 'to 8 places, and ln(' + Rtext(x) + ') &asymp; ' + ln.toFixed(8) + ' is the same number '
        + 'scaled by ln(10).';
  }

  /* ------------------------------------------------------------- base ---- */

  function drawBase() {
    var bb = readbase('lgBase'), x = readnum('lgX');
    var problem = baseProblem(bb);
    if (problem) { fail(problem); return; }
    if (bb.kind === 'e') {
      fail('<strong>Put a rational base here.</strong> This mode changes FROM base b TO the three '
        + 'bases a calculator carries, and one of those three is e already.');
      return;
    }
    if (x === null) {
      fail('<strong>x has to be a whole number or a fraction.</strong> Try 343, 27 or 10.');
      return;
    }
    var b = bb.r, bv = Rfloat(b);
    titleOut.textContent = 'log_' + Rterm(b) + '(' + Rtext(x) + ')';
    subOut.textContent = 'computed directly, and again through three other bases';

    if (Rsign(x) <= 0) {
      var pl = Plot(svg, { xmin: -1, xmax: 12, ymin: -4, ymax: 4 });
      pl.frame();
      pl.vline(0, 'plot-asym', 'x = 0');
      pl.curve(function (t) { return t > 0 ? Math.log(t) / Math.log(bv) : NaN; });
      pl.describe('y = log_' + Rterm(b) + '(x), which stops at x = 0.');
      work.innerHTML = steps('change of base cannot rescue this', [
        ['the formula', 'log_b(x) = log_c(x) / log_c(b). Changing base changes the tool, not the '
          + 'question, and the question is still which power of ' + Rterm(b) + ' gives ' + Rtext(x) + '.'],
        ['what happens to the numerator', 'log_c(' + Rtext(x) + ') is undefined for every base c, '
          + 'because no positive base raised to a real power is zero or negative. A fraction with '
          + 'an undefined numerator is not a number.'],
        ['the honest answer', 'log_' + Rterm(b) + '(' + Rtext(x) + ') does not exist. x &gt; 0 is a '
          + 'condition on the argument, not on the base.']
      ]);
      setkpis('undefined', 'undefined', chip('outside the domain', 'no'));
      status.innerHTML = '<strong>An argument of ' + Rtext(x) + ' has no logarithm in any base.</strong> '
        + 'Change of base multiplies a logarithm by a constant; it cannot create one where none '
        + 'exists. The domain x &gt; 0 survives every change of base, which is one way of seeing '
        + 'that the formula is a rescaling of the same curve rather than a different function.';
      return;
    }

    var lv = logvalue(b, x);
    /* An exact change of base: a base c that BOTH b and x are exact powers of.
       When it exists the whole formula runs in fractions -- log_9(27) = 3/2 the
       hard way, with nothing rounded anywhere. */
    var shared = null, c;
    for (c = 2; c <= 30 && shared === null; c += 1) {
      var cr = R(BigInt(c)), eb = ratpow(cr, b), ex = ratpow(cr, x);
      if (eb !== null && ex !== null && !Rzero(eb)) shared = { c: c, lb: eb, lx: ex };
    }
    var xv = Rfloat(x);
    var helpers = [['10', Math.LN10], ['e', 1], ['2', Math.LN2]];
    var rows = helpers.map(function (h) {
      var lx = Math.log(xv) / h[1], lb2 = Math.log(bv) / h[1];
      return trow([
        cell('c = ' + h[0]), cell(lx.toFixed(8)), cell(lb2.toFixed(8)),
        cell((lx / lb2).toFixed(8)), cell(chip('rounded', 'no'))
      ]);
    });
    if (shared) {
      rows.push(trow([
        cell('c = ' + shared.c + ' (exact)'), cell(Rtext(shared.lx)), cell(Rtext(shared.lb)),
        cell(Rtext(Rdiv(shared.lx, shared.lb))), cell(chip('exact', 'ok'))
      ], 'focus'));
    }

    var pairs = [
      ['the derivation', 'let y = log_b(x), so b^y = x. Take log_c of both sides: '
        + 'log_c(b^y) = log_c(x). The power law makes the left side y&middot;log_c(b), so '
        + 'y = log_c(x) / log_c(b). Nothing about c was used, which is why any c will do.'],
      ['why a calculator only needs two buttons', 'log and ln are enough for every base, because '
        + 'the formula turns log_' + Rterm(b) + ' into a division of two of them. The rows above '
        + 'are three different c values landing on the same number.']
    ];
    if (shared) {
      pairs.push(['the exact route', 'both ' + Rterm(b) + ' and ' + Rtext(x) + ' are powers of '
        + shared.c + ': ' + shared.c + '^' + Rtext(shared.lb) + ' = ' + Rterm(b) + ' and '
        + shared.c + '^' + Rtext(shared.lx) + ' = ' + Rtext(x) + '. So log_' + Rterm(b) + '('
        + Rtext(x) + ') = ' + Rtext(shared.lx) + ' / ' + Rtext(shared.lb) + ' = '
        + Rtext(Rdiv(shared.lx, shared.lb)) + ', in fractions, with nothing rounded.']);
    } else {
      pairs.push(['no exact route here', 'no whole number c up to 30 has both ' + Rterm(b)
        + ' and ' + Rtext(x) + ' as exact powers, so every row above is a rounded decimal. They '
        + 'agree to eight places, which is evidence that the formula is right and not a proof of '
        + 'it &mdash; the proof is the derivation above.']);
    }
    work.innerHTML = ttable('log_' + Rterm(b) + '(' + Rtext(x) + ') = log_c(' + Rtext(x)
      + ') / log_c(' + Rterm(b) + '), through four helper bases',
      ['helper base c', 'log_c(x)', 'log_c(b)', 'the ratio', 'arithmetic'], rows)
      + steps('where the formula comes from', pairs);

    var xmax = Math.max(xv * 1.25, 12);
    var ys = [Math.log(xv) / Math.log(bv), Math.log(xv) / Math.LN10, Math.log(xv), Math.log(xv) / Math.LN2];
    var ylo = Math.min.apply(null, ys.concat([0])), yhi = Math.max.apply(null, ys.concat([0]));
    var pad = Math.max(1, (yhi - ylo) * 0.2);
    var plot = Plot(svg, { xmin: -xmax * 0.04, xmax: xmax, ymin: ylo - pad, ymax: yhi + pad });
    plot.frame();
    plot.vline(0, 'plot-asym', 'x = 0');
    plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.log(bv) : NaN; });
    plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.LN10 : NaN; }, 'plot-curve alt');
    plot.curve(function (t) { return t > 0 ? Math.log(t) : NaN; }, 'plot-curve alt');
    plot.curve(function (t) { return t > 0 ? Math.log(t) / Math.LN2 : NaN; }, 'plot-curve alt');
    plot.point(xv, Math.log(xv) / Math.log(bv), 'plot-point', 'log_' + Rterm(b));
    plot.describe('y = log_' + Rterm(b) + '(x) with log_10, ln and log_2 drawn beside it: the same '
      + 'curve at four different vertical scales.');

    var direct = Math.log(xv) / Math.log(bv);
    var spread = Math.max.apply(null, helpers.map(function (h) {
      return Math.abs((Math.log(xv) / h[1]) / (Math.log(bv) / h[1]) - direct);
    }));
    setkpis(lv.kind === 'exact' ? Rtext(lv.y) : '&asymp; ' + direct.toFixed(6),
      '&asymp; ' + ((Math.log(xv) / Math.LN10) / (Math.log(bv) / Math.LN10)).toFixed(6),
      spread < 1e-9 ? chip('agree to 1e-9', 'ok') : chip('differ', 'no'));

    status.innerHTML = lv.kind === 'exact'
      ? '<strong>log_' + Rterm(b) + '(' + Rtext(x) + ') = ' + Rtext(lv.y) + ', exactly.</strong> '
        + 'The exponent search settled it without any change of base at all'
        + (shared ? ', and the exact row above reaches the same fraction through base ' + shared.c
                    + ' &mdash; two independent routes to ' + Rtext(lv.y) + '. ' : '. ')
        + 'The three decimal rows agree with it to eight places, which is what the formula '
        + 'promises: changing base rescales the whole curve by a constant and cannot move a value '
        + 'that was already right.'
      : '<strong>No exact exponent exists here, so the change of base formula is how the number is '
        + 'reached at all.</strong> log_' + Rterm(b) + '(' + Rtext(x) + ') &asymp; '
        + direct.toFixed(8) + ', and the three helper bases above land within 1e-9 of each other. '
        + 'They must: log_c(x)/log_c(b) has the constant ln(c) in both parts, and it cancels. That '
        + 'is the same reason all four curves in the picture have the same shape and differ only '
        + 'in vertical scale.';
  }

  /* --------------------------------------------------------- solveexp ---- */

  function drawSolveExp() {
    var a = readnum('lgA'), bb = readbase('lgBase'), c = readnum('lgC');
    var d = readnum('lgD'), k = readnum('lgK');
    var problem = baseProblem(bb);
    if (problem) { fail(problem); return; }
    if (bb.kind === 'e') {
      fail('<strong>Use a rational base here.</strong> The first method below asks whether the '
        + 'right-hand side is an exact power of the base, and that question only has an exact '
        + 'answer for a rational base. Try 2, 3, 4 or 10.');
      return;
    }
    if (a === null || c === null || d === null || k === null) {
      fail('<strong>a, c, d and k all have to be numbers.</strong> The equation is '
        + 'a&middot;b^(cx + d) = k.');
      return;
    }
    var b = bb.r, bv = Rfloat(b);
    /* The equation, written the way it would be written by hand: no coefficient
       glued to a base (5 and 2 side by side would read as fifty-two), and no
       brackets round an exponent that is a single letter. */
    var coef = Requ(a, R1) ? '' : (Requ(a, R(-1n)) ? '-' : Rtext(a));
    var basetext = Rterm(b);
    if (coef !== '' && coef !== '-' && basetext.charAt(0) !== '(') basetext = '(' + basetext + ')';
    var expText = (Requ(c, R1) ? 'x' : (Requ(c, R(-1n)) ? '-x' : Rterm(c) + 'x'))
      + (Rzero(d) ? '' : (Rsign(d) > 0 ? ' + ' + Rtext(d) : ' - ' + Rtext(Rabs(d))));
    var expDisp = (expText === 'x' || expText === '-x') ? expText : '(' + expText + ')';
    var expr = coef + basetext + '^' + expDisp;
    titleOut.textContent = expr + ' = ' + Rtext(k);
    subOut.textContent = 'matched powers first, logarithms second';

    if (Rzero(a)) {
      fail('<strong>With a = 0 the left side is 0 whatever x does.</strong> The equation is then '
        + '0 = ' + Rtext(k) + ', which is either false for every x or true for every x &mdash; and '
        + 'neither is what "solve for x" means. Set a to something non-zero.');
      return;
    }
    var rhs = Rdiv(k, a);
    var pairs = [['isolate the power', Requ(a, R1)
      ? 'there is nothing to divide by: the power already stands alone, equal to ' + Rtext(rhs) + '.'
      : 'divide both sides by ' + Rtext(a) + ': ' + Rterm(b) + '^' + expDisp + ' = ' + Rtext(rhs)
        + '.']];

    var solved = null, method = '', exactY = null;
    if (Rsign(rhs) <= 0) {
      pairs.push(['stop here', Rterm(b) + ' raised to any real power is positive &mdash; large '
        + 'for big exponents, small for very negative ones, never zero and never negative. The '
        + 'right-hand side is ' + Rtext(rhs) + ', so there is no exponent that could produce it, '
        + 'and the equation has no solution. Taking logarithms of both sides at this point would '
        + 'produce a number, and that number would be wrong.']);
    } else {
      exactY = ratpow(b, rhs);
      if (exactY !== null) {
        pairs.push(['both sides as powers of ' + Rterm(b), Rtext(rhs) + ' = ' + Rterm(b) + '^'
          + Rterm(exactY) + ', found by searching exponents p/q with ' + Rterm(b) + '^p = '
          + Rterm(rhs) + '^q. An exponential is one-to-one, so equal values force equal exponents: '
          + expText + ' = ' + Rtext(exactY) + '.']);
        if (Rzero(c)) {
          var holds = Requ(d, exactY);
          pairs.push(['c is 0, so x has vanished', holds
            ? 'the equation reduces to a true statement, so every real x is a solution. That is an '
              + 'identity rather than an equation to solve.'
            : 'the equation reduces to ' + Rtext(d) + ' = ' + Rtext(exactY)
              + ', which is false, so no x satisfies it.']);
        } else {
          solved = Rdiv(Rsub(exactY, d), c);
          method = 'matched powers';
          pairs.push(['solve the linear equation', 'x = (' + Rtext(exactY) + ' - ' + Rterm(d)
            + ') / ' + Rterm(c) + ' = ' + Rtext(solved) + ', exactly.']);
          var back = Radd(Rmul(c, solved), d);
          /* The check stays exact even when the exponent is a fraction: b^(p/q)
             is rhs precisely when b^p = rhs^q, and those are two whole numbers
             to compare. */
          pairs.push(['check by substitution', Rint(back)
            ? Rterm(b) + '^' + Rterm(back) + ' = ' + Rshow(Rpow(b, Number(back.n))) + ', and '
              + Rtext(k) + ' / ' + Rtext(a) + ' = ' + Rtext(rhs) + '. The two agree, in fractions.'
            : Rterm(b) + '^' + String(back.n) + ' = ' + Rshow(Rpow(b, Number(back.n))) + ' and '
              + Rterm(rhs) + '^' + String(back.d) + ' = ' + Rshow(Rpow(rhs, Number(back.d)))
              + ', and those two are equal &mdash; which is exactly what ' + Rterm(b) + '^'
              + Rterm(back) + ' = ' + Rtext(rhs) + ' means. No decimal was involved.']);
        }
      } else {
        pairs.push(['no exact match', 'the search found no p/q with ' + Rterm(b) + '^p = '
          + Rtext(rhs) + '^q, so the two sides cannot be written as powers of one base and the '
          + 'first method has nothing to offer. This is the ordinary case, not the exceptional '
          + 'one.']);
      }
      if (!Rzero(c)) {
        var logv = Math.log(Rfloat(rhs)) / Math.log(bv);
        var xnum = (logv - Rfloat(d)) / Rfloat(c);
        var logExpr = 'log_' + Rterm(b) + '(' + Rtext(rhs) + ')';
        if (!Rzero(d)) logExpr = '(' + logExpr + ' - ' + Rterm(d) + ')';
        if (!Requ(c, R1)) logExpr = logExpr + ' / ' + Rterm(c);
        pairs.push(['take logarithms of both sides', 'log_' + Rterm(b) + '(' + Rterm(b) + '^'
          + expDisp + ') = ' + expText + ' by the power law, so ' + expText + ' = log_' + Rterm(b)
          + '(' + Rtext(rhs) + ') &asymp; ' + logv.toFixed(8) + ', which gives x &asymp; '
          + xnum.toFixed(8) + '.']);
        pairs.push(['which of the two to trust', exactY !== null
          ? 'they agree: ' + Rtext(solved === null ? exactY : solved) + ' against '
            + xnum.toFixed(8) + '. The first is exact and the second is a rounding of it, so the '
            + 'exact one is the answer to write down.'
          : 'only the logarithm method applies, and its answer is irrational. '
            + xnum.toFixed(8) + ' is a rounding to 8 places; the exact answer is the expression x = '
            + logExpr + ', and leaving it in that form is not laziness.']);
      }
    }
    work.innerHTML = steps('solving ' + expr + ' = ' + Rtext(k), pairs);

    var av = Rfloat(a), cv = Rfloat(c), dv = Rfloat(d), kv = Rfloat(k);
    var f = function (t) { return av * Math.pow(bv, cv * t + dv); };
    var centre = 0;
    if (solved !== null) centre = Rfloat(solved);
    else if (Rsign(rhs) > 0 && !Rzero(c)) centre = (Math.log(Rfloat(rhs)) / Math.log(bv) - dv) / cv;
    if (!isFinite(centre)) centre = 0;
    var xmin = centre - 4, xmax = centre + 4;
    var ys = [kv, f(xmin), f(xmax), 0];
    var ylo = Math.min.apply(null, ys), yhi = Math.max.apply(null, ys);
    if (!isFinite(ylo) || !isFinite(yhi) || yhi - ylo > 1e6) { ylo = Math.min(0, kv * 1.5); yhi = Math.max(1, kv * 1.5, 4); }
    var span = Math.max(yhi - ylo, 1);
    var plot = Plot(svg, { xmin: xmin, xmax: xmax, ymin: ylo - span * 0.12, ymax: yhi + span * 0.12 });
    plot.frame();
    plot.hline(kv, 'plot-asym', 'y = ' + Rtext(k));
    plot.curve(f);
    if (solved !== null) plot.point(Rfloat(solved), kv, 'plot-point root', 'x = ' + Rtext(solved));
    else if (Rsign(rhs) > 0 && !Rzero(c) && isFinite(centre)) {
      plot.point(centre, kv, 'plot-point root', 'x &asymp; ' + centre.toFixed(4));
    }
    plot.describe('y = ' + expr + ' and the horizontal line y = ' + Rtext(k)
      + (Rsign(rhs) <= 0 ? ', which the curve never reaches.' : ', meeting at the solution.'));

    if (Rsign(rhs) <= 0) {
      setkpis('no solution', 'positivity', chip('nothing to check', 'no'));
      status.innerHTML = '<strong>No solution, and the reason is worth more than the answer.</strong> '
        + 'After dividing by ' + Rtext(a) + ' the equation asks for a power of ' + Rterm(b)
        + ' equal to ' + Rtext(rhs) + '. The curve above has y = 0 as an asymptote and lives '
        + 'entirely on one side of it, so the line y = ' + Rtext(k) + ' never meets it. A reader '
        + 'who takes logarithms of both sides here gets log of a non-positive number, which most '
        + 'calculators return as an error and some return as a complex number &mdash; neither is a '
        + 'solution to this equation.';
    } else if (solved !== null) {
      setkpis(Rtext(solved), method, chip('substituted back', 'ok'));
      status.innerHTML = '<strong>x = ' + Rtext(solved) + ', exactly.</strong> Both sides were '
        + 'written as powers of ' + Rterm(b) + ' and the exponents matched, which is legitimate '
        + 'precisely because ' + Rterm(b) + '^t is one-to-one: it takes each value once, so equal '
        + 'values force equal exponents. The logarithm method gives the same number as a decimal; '
        + 'it is the method to reach for when the matching fails, which is most of the time.';
    } else if (Rzero(c)) {
      setkpis('x has vanished', 'not an equation in x', chip('degenerate', 'no'));
      status.innerHTML = '<strong>With c = 0 there is no x in the equation.</strong> The exponent is '
        + 'the constant ' + Rtext(d) + ', so the left side is a fixed number and the statement is '
        + 'either true for every x or for none. It is worth meeting once: "solve for x" assumes x '
        + 'is still there after the algebra.';
    } else {
      var approx = (Math.log(Rfloat(rhs)) / Math.log(bv) - Rfloat(d)) / Rfloat(c);
      setkpis('&asymp; ' + approx.toFixed(6), 'logarithms', chip('irrational', 'hi'));
      var logExpr2 = 'log_' + Rterm(b) + '(' + Rtext(rhs) + ')';
      if (!Rzero(d)) logExpr2 = '(' + logExpr2 + ' - ' + Rterm(d) + ')';
      if (!Requ(c, R1)) logExpr2 = logExpr2 + ' / ' + Rterm(c);
      status.innerHTML = '<strong>This one has no exact power to match, so logarithms are the '
        + 'method rather than a shortcut.</strong> x = ' + logExpr2
        + ' &asymp; ' + approx.toFixed(8) + ', rounded to 8 '
        + 'places. The exact answer is that expression, not the decimal: writing '
        + approx.toFixed(4) + ' and calling it x throws away everything after the fourth place '
        + 'without saying so.';
    }
  }

  /* --------------------------------------------------------- solvelog ---- */

  /* The sign of c + s*sqrt(kk), decided exactly. A domain check on an
     irrational candidate is exactly where a float comparison would quietly
     accept a root that is a hair outside the domain. */
  function surdsign(d, s, kk) {
    var sd = Rsign(d), ss = Rsign(s);
    if (ss === 0 || kk === 1n) return Rsign(Radd(d, Rmul(s, R1)));
    if (sd >= 0 && ss > 0) return (sd === 0 && ss === 0) ? 0 : 1;
    if (sd <= 0 && ss < 0) return -1;
    var cmp = Rcmp(Rmul(d, d), Rmul(Rmul(s, s), R(kk)));
    if (sd > 0) return cmp > 0 ? 1 : (cmp === 0 ? 0 : -1);
    return cmp < 0 ? 1 : (cmp === 0 ? 0 : -1);
  }
  function candrational(cd) {
    return (Rzero(cd.s) || cd.k === 1n) ? Radd(cd.c, Rmul(cd.s, R1)) : null;
  }
  function candtext(cd) {
    var r = candrational(cd);
    if (r !== null) return Rtext(r);
    var mag = surdtext({ q: Rabs(cd.s), k: cd.k });
    if (Rzero(cd.c)) return (Rsign(cd.s) < 0 ? '-' : '') + mag;
    return Rtext(cd.c) + (Rsign(cd.s) < 0 ? ' - ' : ' + ') + mag;
  }
  function candfloat(cd) {
    return Rfloat(cd.c) + Rfloat(cd.s) * Math.sqrt(Number(cd.k));
  }

  function drawSolveLog() {
    var shape = readtext('lgShape') || 'sum';
    var bb = readbase('lgBase'), p = readnum('lgP'), q = readnum('lgQ'), k = readnum('lgK');
    var problem = baseProblem(bb);
    if (problem) { fail(problem); return; }
    if (bb.kind === 'e') {
      fail('<strong>Use a rational base here.</strong> The right-hand side becomes b^k, and that '
        + 'has to be an exact number for the domain check below to be exact too.');
      return;
    }
    if (p === null || q === null || k === null) {
      fail('<strong>p, q and k all have to be numbers.</strong> p and q are subtracted inside the '
        + 'logarithms; k is the right-hand side.');
      return;
    }
    if (!Rint(k) || k.n > 40n || k.n < -40n) {
      fail('<strong>k has to be a whole number between -40 and 40.</strong> b^k is then an exact '
        + 'fraction, and the whole solution &mdash; including the domain check that decides which '
        + 'candidate survives &mdash; stays exact.');
      return;
    }
    var b = bb.r, bv = Rfloat(b), bk = Rpow(b, Number(k.n));
    var lhs, args, quad = null;
    if (shape === 'sum') {
      lhs = logname(Rterm(b), argtext(p)) + ' + ' + logname(Rterm(b), argtext(q));
      args = [argtext(p), argtext(q)];
    } else if (shape === 'diff') {
      lhs = logname(Rterm(b), argtext(p)) + ' - ' + logname(Rterm(b), argtext(q));
      args = [argtext(p), argtext(q)];
    } else if (shape === 'square') {
      lhs = logname(Rterm(b), 'x^2' + (Rzero(p) ? '' : (Rsign(p) > 0 ? ' - ' + Rtext(p) : ' + ' + Rtext(Rneg(p)))));
      args = [(Rzero(p) ? 'x^2' : 'x^2' + (Rsign(p) > 0 ? ' - ' + Rtext(p) : ' + ' + Rtext(Rneg(p))))];
    } else {
      lhs = logname(Rterm(b), argtext(p));
      args = [argtext(p)];
    }
    titleOut.textContent = lhs + ' = ' + Rtext(k);
    subOut.textContent = 'candidates first, then the domain';

    var pairs = [], cands = [], note = null;
    if (shape === 'sum') {
      pairs.push(['combine the logarithms', 'the product law turns the left side into '
        + logname(Rterm(b), '(' + argtext(p) + ')(' + argtext(q) + ')') + ' = ' + Rtext(k) + '.']);
      pairs.push(['undo the logarithm', '(' + argtext(p) + ')(' + argtext(q) + ') = '
        + Rterm(b) + '^' + Rtext(k) + ' = ' + Rshow(bk) + '.']);
      var poly = [Rsub(Rmul(p, q), bk), Rneg(Radd(p, q)), R1];
      pairs.push(['a quadratic', Ptext(poly) + ' = 0.']);
      quad = quadroots(R1, poly[1], poly[0]);
      if (quad.kind === 'complex') {
        note = 'The quadratic ' + Ptext(poly) + ' = 0 has discriminant ' + Rtext(quad.disc)
          + ', which is negative, so it has no real root. The equation fails in the algebra, '
          + 'before the domain is ever consulted &mdash; a different kind of "no solution" from '
          + 'the one where a candidate appears and is then rejected.';
        pairs.push(['no real candidates', note]);
      } else if (quad.kind === 'double') {
        cands.push({ c: quad.p, s: R0, k: 1n });
      } else {
        cands.push({ c: quad.p, s: quad.s.q, k: quad.s.k });
        cands.push({ c: quad.p, s: Rneg(quad.s.q), k: quad.s.k });
      }
    } else if (shape === 'diff') {
      pairs.push(['combine the logarithms', 'the quotient law turns the left side into '
        + logname(Rterm(b), '(' + argtext(p) + ') / (' + argtext(q) + ')') + ' = ' + Rtext(k) + '.']);
      pairs.push(['undo the logarithm', '(' + argtext(p) + ') / (' + argtext(q) + ') = '
        + Rterm(b) + '^' + Rtext(k) + ' = ' + Rshow(bk) + '.']);
      var denom = Rsub(R1, bk);
      if (Rzero(denom)) {
        note = Requ(p, q)
          ? 'With b^k = 1 the equation says the two arguments are equal, and they are the same '
            + 'expression, so every x in the domain is a solution. That is an identity, not an '
            + 'equation with an answer.'
          : 'With k = 0, b^k = 1, so the equation says ' + argtext(p) + ' = ' + argtext(q)
            + ' &mdash; that is, ' + Rtext(Rneg(p)) + ' = ' + Rtext(Rneg(q))
            + ', which is false. There is no x at all, and no candidate to test.';
        pairs.push(['the x terms cancel', note]);
      } else {
        var xv2 = Rdiv(Rsub(p, Rmul(bk, q)), denom);
        pairs.push(['solve the linear equation', argtext(p) + ' = ' + Rshow(bk) + '('
          + argtext(q) + ') gives x = ' + Rtext(xv2) + '.']);
        cands.push({ c: xv2, s: R0, k: 1n });
      }
    } else if (shape === 'square') {
      pairs.push(['undo the logarithm', 'x^2' + (Rzero(p) ? '' : (Rsign(p) > 0 ? ' - ' + Rtext(p) : ' + ' + Rtext(Rneg(p))))
        + ' = ' + Rterm(b) + '^' + Rtext(k) + ' = ' + Rshow(bk) + ', so x^2 = ' + Rshow(Radd(bk, p)) + '.']);
      var sq = Radd(bk, p);
      if (Rsign(sq) < 0) {
        note = 'x^2 = ' + Rshow(sq) + ' has no real solution, because a square is never negative. '
          + 'The equation fails in the algebra, before the domain is ever consulted &mdash; and '
          + 'notice that the argument x^2 ' + (Rsign(p) > 0 ? '- ' + Rtext(p) : '+ ' + Rtext(Rneg(p)))
          + ' is at least ' + Rshow(Rneg(p)) + ' for every real x, while b^k = ' + Rshow(bk)
          + ' is smaller than that. No x could have worked.';
        pairs.push(['no real candidates', note]);
      } else {
        var sr = Rsurd(sq);
        pairs.push(['two square roots', 'x = +-' + surdtext(sr) + '. Both are candidates; the '
          + 'domain decides, not the sign.']);
        cands.push({ c: R0, s: sr.q, k: sr.k });
        if (!Rzero(sr.q)) cands.push({ c: R0, s: Rneg(sr.q), k: sr.k });
      }
    } else {
      pairs.push(['undo the logarithm', Rzero(p)
        ? 'x = ' + Rterm(b) + '^' + Rtext(k) + ' = ' + Rshow(bk) + '.'
        : argtext(p) + ' = ' + Rterm(b) + '^' + Rtext(k) + ' = ' + Rshow(bk) + ', so x = '
          + Rtext(p) + ' + ' + Rshow(bk) + ' = ' + Rshow(Radd(p, bk)) + '.']);
      cands.push({ c: Radd(p, bk), s: R0, k: 1n });
    }

    /* ---- the domain check, exactly, on every candidate ---- */
    function argvalue(cd, which) {
      /* the value of one argument at a candidate, as (c + s*sqrt(k)) */
      if (shape === 'square') {
        var cc = Radd(Rmul(cd.c, cd.c), Rmul(Rmul(cd.s, cd.s), R(cd.k)));
        return { c: Rsub(cc, p), s: Rmul(R(2n), Rmul(cd.c, cd.s)), k: cd.k };
      }
      var t = which === 0 ? p : q;
      return { c: Rsub(cd.c, t), s: cd.s, k: cd.k };
    }
    var accepted = [], rejected = [], crows = [];
    cands.forEach(function (cd) {
      var details = [], ok = true;
      for (var i = 0; i < args.length; i += 1) {
        var av = argvalue(cd, i);
        var sgn = surdsign(av.c, av.s, av.k);
        var shown = candtext(av);
        details.push(args[i] + ' = ' + shown + ' ' + (sgn > 0 ? chip('positive', 'ok')
          : chip(sgn === 0 ? 'zero' : 'negative', 'no')));
        if (sgn <= 0) ok = false;
      }
      (ok ? accepted : rejected).push(cd);
      crows.push(trow([
        cell('x = ' + candtext(cd)), cell(candfloat(cd).toFixed(6)),
        cell(details.join('<br>')),
        cell(ok ? 'accepted' : 'rejected', ok ? 't' : 'f')
      ], ok ? 'focus' : ''));
    });

    var blocks = [steps('the algebra', pairs)];
    if (crows.length) {
      blocks.push(ttable('every candidate, tested against the domain of each logarithm',
        ['candidate', 'as a decimal', 'the arguments at that x', 'verdict'], crows));
    }
    /* Substituting the survivors back, exactly where the arguments are exact
       powers of the base and numerically where they are not. */
    var checks = [];
    accepted.forEach(function (cd) {
      var r = candrational(cd), line;
      if (r !== null) {
        var parts = [], total = { exact: true, r: R0, v: 0 };
        for (var i = 0; i < args.length; i += 1) {
          var av = argvalue(cd, i), rv = candrational(av);
          var lvv = rv === null ? { kind: 'searched', v: NaN } : logvalue(b, rv);
          var qv = Q(lvv);
          parts.push(logname(Rterm(b), Rtext(rv)) + ' = ' + Qtext(qv, 6));
          total = (shape === 'diff' && i === 1) ? Qsub(total, qv) : Qadd(total, qv);
        }
        var match = Qeq(total, Qnum(k));
        line = parts.join(',  ') + ' &rarr; ' + Qtext(total, 6) + ' against k = ' + Rtext(k)
          + '. ' + (match.same ? 'They agree, ' + match.how + 'ly.' : 'They do not agree.');
      } else {
        var f = logFor(shape, b, p, q, bv);
        line = 'x is irrational here, so the check is numerical: the left side comes to '
          + f(candfloat(cd)).toFixed(8) + ' against k = ' + Rtext(k) + '.';
      }
      checks.push(['x = ' + candtext(cd), line]);
    });
    if (checks.length) blocks.push(steps('substituting the survivors back', checks));
    work.innerHTML = blocks.join('');

    /* The picture draws the left side only where it is defined, so the domain
       is visible rather than asserted. */
    var f = logFor(shape, b, p, q, bv);
    var marks = cands.map(candfloat).filter(function (v) { return isFinite(v); });
    var lowm = marks.length ? Math.min.apply(null, marks) : 0;
    var highm = marks.length ? Math.max.apply(null, marks) : 1;
    var edge = shape === 'square' ? 0 : Math.max(Rfloat(p), shape === 'single' ? Rfloat(p) : Rfloat(q));
    var xmin = Math.min(lowm, edge) - 3, xmax = Math.max(highm, edge) + 3;
    var kv = Rfloat(k);
    var plot = Plot(svg, { xmin: xmin, xmax: xmax, ymin: kv - 5, ymax: kv + 5 });
    plot.frame();
    plot.hline(kv, 'plot-asym', 'y = ' + Rtext(k));
    plot.curve(f);
    accepted.forEach(function (cd) { plot.point(candfloat(cd), kv, 'plot-point root', 'x = ' + candtext(cd)); });
    rejected.forEach(function (cd) { plot.hole(candfloat(cd), kv); });
    plot.describe('y = ' + lhs + ' drawn only where every argument is positive, with the line y = '
      + Rtext(k) + '; accepted solutions are filled and rejected candidates are hollow.');

    setkpis(String(cands.length), String(accepted.length), String(rejected.length));

    var msg;
    if (!cands.length) {
      msg = '<strong>There is no candidate to test.</strong> ' + (note || 'The algebra ran out '
        + 'before any x appeared.')
        + ' An equation with no solution is a legitimate answer, and it is not the same thing as a '
        + 'candidate that appears and is then rejected by the domain &mdash; the two presets '
        + 'either side of this one show both.';
    } else if (!accepted.length) {
      msg = '<strong>Every candidate was rejected, so the equation has no solution.</strong> '
        + 'The algebra produced x = ' + cands.map(candtext).join(' and x = ')
        + ', and at that value at least one argument above is zero or negative &mdash; a logarithm '
        + 'of it does not exist, so the original equation was never satisfied. This is why the '
        + 'domain check is a step and not a formality: the arithmetic that produced the candidate '
        + 'was correct, and the candidate is still not a solution.';
    } else if (rejected.length) {
      msg = '<strong>' + accepted.length + ' of the ' + cands.length + ' candidates survived.</strong> '
        + 'x = ' + accepted.map(candtext).join(', ') + ' keeps every argument positive; x = '
        + rejected.map(candtext).join(', ') + ' does not, and gets thrown away. Combining two '
        + 'logarithms into one widened the domain &mdash; log(A) + log(B) needs A and B positive '
        + 'while log(AB) only needs the product positive &mdash; so the combined equation has '
        + 'solutions the original does not. Every one of them shows up here.';
    } else if (accepted.length === 1) {
      msg = '<strong>The one candidate survived the domain check.</strong> x = '
        + candtext(accepted[0]) + ' keeps every argument positive, so it is a solution of the '
        + 'original equation and not only of the combined one. The check still had to be made: '
        + 'the presets either side of this one produce candidates that fail it.';
    } else {
      msg = '<strong>All ' + accepted.length + ' candidates survived the domain check.</strong> '
        + 'Rejection is not automatic: x = ' + accepted.map(candtext).join(' and x = ')
        + ' each keep every argument positive, so each is a genuine solution. A reader who has '
        + 'learned to discard the negative root by reflex gets this one wrong.';
    }
    status.innerHTML = msg;
  }

  /* The left-hand side as a function of x, defined only on its domain: Math.log
     of a non-positive number is NaN, and the grapher breaks the curve there. */
  function logFor(shape, b, p, q, bv) {
    var pv = Rfloat(p), qv = Rfloat(q), lb = Math.log(bv);
    if (shape === 'sum') return function (t) { return (Math.log(t - pv) + Math.log(t - qv)) / lb; };
    if (shape === 'diff') return function (t) { return (Math.log(t - pv) - Math.log(t - qv)) / lb; };
    if (shape === 'square') return function (t) { return Math.log(t * t - pv) / lb; };
    return function (t) { return Math.log(t - pv) / lb; };
  }

  /* ------------------------------------------------------------ scale ---- */

  /* 10^e, exactly when e is a whole number and honestly rounded when it is not.
     A decibel difference of 30 is a factor of exactly 1000; a difference of 3
     is a factor of about 1.995, and the lab must not print the second as though
     it were the first. */
  function powten(e) {
    if (Rint(e) && e.n >= -60n && e.n <= 60n) {
      var val = Rpow(R(10n), Number(e.n));
      return { exact: true, r: val, v: Rfloat(val) };
    }
    return { exact: false, r: null, v: Math.pow(10, Rfloat(e)) };
  }
  /* An exact power of ten that is very large or very small is exact and
     unreadable at the same time, so the scientific form is offered beside it
     rather than instead of it. */
  function showpow(t) {
    if (!t.exact) {
      if (!isFinite(t.v)) return 'past anything a double can hold';
      return '&asymp;&nbsp;' + t.v.toPrecision(8);
    }
    var text = Rshow(t.r, 6);
    if (t.v !== 0 && (Math.abs(t.v) < 0.001 || Math.abs(t.v) >= 1e7)) {
      text += ' = ' + t.v.toExponential(0);
    }
    return text;
  }

  var SCALES = {
    db: { unit: 'dB', name: 'sound level', formula: 'L = 10 log_10(I / I0)',
          quantity: 'intensity I / I0', per: '10' },
    ph: { unit: '', name: 'pH', formula: 'pH = -log_10(H+ concentration)',
          quantity: 'concentration in mol/L', per: '1' },
    rich: { unit: '', name: 'magnitude', formula: 'M = log_10(A / A0)',
            quantity: 'amplitude A / A0', per: '1' }
  };

  function drawScale() {
    var kind = readtext('lgScale') || 'db';
    if (!SCALES[kind]) kind = 'db';
    var v1 = readnum('lgV1'), v2 = readnum('lgV2');
    if (v1 === null || v2 === null) {
      fail('<strong>Both readings have to be numbers.</strong> They are two measurements on the '
        + 'same scale, such as 60 and 120 decibels, or 3 and 7 on the pH scale.');
      return;
    }
    var sc = SCALES[kind];
    titleOut.textContent = sc.formula;
    subOut.textContent = 'two readings: ' + Rtext(v1) + ' and ' + Rtext(v2);

    /* The exponent that turns a reading into the quantity behind it. */
    function quantityExp(v) {
      if (kind === 'db') return Rdiv(v, R(10n));
      if (kind === 'ph') return Rneg(v);
      return v;
    }
    var e1 = quantityExp(v1), e2 = quantityExp(v2);
    var t1 = powten(e1), t2 = powten(e2);
    var diff = Rsub(v1, v2);
    var factorExp = Rsub(e1, e2);
    var factor = powten(factorExp);
    var rows = [
      trow([rowhead('first reading'), cell(Rdectext(v1) + ' ' + sc.unit),
        cell('10^(' + Rdectext(e1) + ') = ' + showpow(t1)),
        cell(t1.exact ? chip('exact', 'ok') : chip('irrational', 'hi'))]),
      trow([rowhead('second reading'), cell(Rdectext(v2) + ' ' + sc.unit),
        cell('10^(' + Rdectext(e2) + ') = ' + showpow(t2)),
        cell(t2.exact ? chip('exact', 'ok') : chip('irrational', 'hi'))]),
      trow([rowhead('difference, first minus second'), cell(Rdectext(diff) + ' ' + sc.unit),
        cell('a difference on the scale, which is not a ratio of anything'),
        cell(chip('exact', 'ok'))]),
      trow([rowhead('the first ' + sc.quantity + ', divided by the second'), cell(showpow(factor)),
        cell('10^(' + Rdectext(factorExp) + '), because subtracting logarithms divides the '
          + 'quantities' + (kind === 'ph' ? ' &mdash; and the minus sign in the pH formula turns '
            + 'the difference round, so the lower reading is the larger concentration' : '')),
        cell(factor.exact ? chip('exact', 'ok') : chip('irrational', 'hi'))], 'focus')
    ];

    var extra = [];
    if (kind === 'db') {
      var sum = 10 * Math.log(Math.pow(10, Rfloat(v1) / 10) + Math.pow(10, Rfloat(v2) / 10)) / Math.LN10;
      rows.push(trow([rowhead('the two sources together'), cell('&asymp;&nbsp;' + sum.toFixed(4) + ' dB'),
        cell('10 log_10(10^(' + Rdectext(v1) + '/10) + 10^(' + Rdectext(v2) + '/10)): the intensities add, '
          + 'and the level is the logarithm of the total'), cell(chip('rounded', 'no'))]));
      extra.push(['adding decibels does not add decibels', 'two equal sources are 10 log_10(2) '
        + '&asymp; 3.0103 dB louder than one, not twice as many decibels. Here the pair comes to '
        + '&asymp; ' + sum.toFixed(4) + ' dB, against the ' + Rdectext(Radd(v1, v2))
        + ' dB that adding the numbers would suggest.']);
      extra.push(['what the reference is', 'I0 = 10^-12 W/m^2, roughly the quietest audible sound. '
        + 'A level is always a ratio to something, which is why a decibel on its own is not a '
        + 'quantity of anything.']);
    } else if (kind === 'ph') {
      extra.push(['lower pH means more acid', 'the minus sign in pH = -log_10(concentration) '
        + 'reverses the order: pH ' + Rdectext(v1) + ' has ' + showpow(t1) + ' mol/L and pH '
        + Rdectext(v2) + ' has ' + showpow(t2) + ' mol/L, so the '
        + (Rcmp(v1, v2) < 0 ? 'first' : 'second') + ' is the more acidic of the two.']);
      extra.push(['each step is a factor of ten', 'a pH difference of ' + Rdectext(diff)
        + ' means the first concentration is ' + showpow(powten(Rneg(diff))) + ' times the '
        + 'second, or equivalently the second is ' + showpow(powten(diff)) + ' times the first. '
        + 'Reading a pH gap as a small difference is the error the scale invites and the reason '
        + 'it is worth converting back to concentration before saying anything about it.']);
    } else {
      var energyExp = Rmul(R(3n, 2n), diff);
      var energy = powten(energyExp);
      rows.push(trow([rowhead('factor on the energy released'), cell(showpow(energy)),
        cell('10^(1.5 &times; ' + Rdectext(diff) + '), from the empirical law log_10(E) = 1.5M + constant'),
        cell(energy.exact ? chip('exact', 'ok') : chip('irrational', 'hi'))]));
      extra.push(['a magnitude 8 is not twice a magnitude 4', 'it is 10^4 = 10000 times the ground '
        + 'amplitude and about 10^6 times the energy. On these two readings the amplitude factor '
        + 'is ' + showpow(factor) + ' and the energy factor is ' + showpow(energy) + '.']);
      extra.push(['why the energy exponent is 1.5', 'it is measured, not derived: energy rises '
        + 'faster than amplitude, and the constant 1.5 comes from seismology rather than from '
        + 'algebra. When the difference is odd the exponent 1.5 &times; difference is not a whole '
        + 'number, and the factor is irrational.']);
    }
    /* "a factor of 1/1000000" is the same fact as "a factor of 1000000" and
       reads like a different one, so the span is always stated as the larger
       of the two. */
    var spanUp = Math.abs(factor.v) >= 1 ? factor
      : (factor.exact ? { exact: true, r: Rinv(factor.r), v: 1 / factor.v }
                      : { exact: false, r: null, v: 1 / factor.v });
    extra.push(['why a scale like this exists at all', 'the two quantities behind these readings '
      + 'differ by a factor of ' + showpow(spanUp) + '. A logarithm turns that into the difference '
      + Rdectext(diff) + ', which fits on an axis and in a sentence &mdash; and the price is that '
      + 'the difference no longer looks like the gap it stands for.']);

    work.innerHTML = ttable(sc.formula + ' &mdash; reading by reading',
      ['', 'on the scale', 'behind the scale', 'arithmetic'], rows)
      + steps('what the scale hides', extra);

    var lo = Math.min(Rfloat(v1), Rfloat(v2)), hi = Math.max(Rfloat(v1), Rfloat(v2));
    var pad = Math.max((hi - lo) * 0.35, 1);
    var line = NumberLine(svg, lo - pad, hi + pad);
    if (hi > lo) line.interval(lo, hi, true, true); else line.point(lo, true);
    line.point(Rfloat(v1), true);
    line.point(Rfloat(v2), true);
    line.describe('the two readings ' + Rtext(v1) + ' and ' + Rtext(v2) + ' on the ' + sc.name
      + ' scale, with the span between them marked.');

    setkpis(Rdectext(diff) + ' ' + sc.unit, showpow(factor),
      factor.exact ? chip('exact', 'ok') : chip('rounded', 'no'));

    status.innerHTML = '<strong>A difference of ' + Rdectext(diff) + ' on this scale means the '
      + 'first reading\'s ' + sc.quantity + ' is ' + showpow(factor) + ' times the second\'s.</strong> '
      + 'That is the whole content of a logarithmic scale: the readings are exponents, so '
      + 'subtracting them divides the quantities. '
      + (factor.exact
        ? 'Here the exponent came out a whole number, so the factor is exact &mdash; no decimal '
          + 'is involved anywhere in that claim.'
        : 'Here the exponent is ' + Rdectext(factorExp) + ', which is not a whole number, so '
          + 'the factor is irrational and every digit shown is a rounding.')
      + ' The readings themselves are small and comparable; the things they describe are not, and '
      + 'that is exactly the trade the scale was invented to make.';
  }

  /* ---------------------------------------------------------- wiring ---- */

  function redraw() {
    if (MODE === 'define') drawDefine();
    else if (MODE === 'graph') drawGraph();
    else if (MODE === 'laws') drawLaws();
    else if (MODE === 'common') drawCommon();
    else if (MODE === 'base') drawBase();
    else if (MODE === 'solveexp') drawSolveExp();
    else if (MODE === 'solvelog') drawSolveLog();
    else drawScale();
  }

  function applyPreset() {
    var parts = (preset.value || '').split('|');
    FIELDS.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (el && parts[i] !== undefined) el.value = parts[i];
    });
    redraw();
  }

  preset.addEventListener('change', applyPreset);
  FIELDS.forEach(function (id) {
    var el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', redraw);
      el.addEventListener('change', redraw);
    }
  });
  applyPreset();
  window.redrawLab = redraw;
"""
    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an example, or type your own"),
        panel_intro=cfg.get(
            "panel_intro",
            "An exact answer here is found by searching for an exponent, not by calling a "
            "logarithm. Where no exact exponent exists the lab brackets the answer between two "
            "powers it can prove, and labels the decimal it prints as a rounding.",
        ),
        script=script,
    )
