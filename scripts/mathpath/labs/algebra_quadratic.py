"""Course 6: the quadratic, solved four ways at once.

The design decision worth stating: this lab solves EVERY quadratic by all four
methods on every redraw, independently, and prints the four answers together.
They agree because they were computed separately, not because one was copied
into the others. A reader who has just been told that completing the square and
the formula are the same thing can watch them be the same thing on a quadratic
they chose.

The parabola is drawn by evaluating the function, and the roots, vertex and axis
marked on it are the exact values printed beside it -- so the picture cannot
flatter the algebra.
"""

from .algebra_core import PLOT_JS, POLY_JS, RATIONAL_JS, SURD_JS
from .common import Lab

# Each preset is (a, b, c) as strings, plus a label. Kept per mode so a lesson
# on the square root property is not handed a quadratic with a linear term.
PRESETS = {
    "zero": [("x^2 - 5x + 6", "1", "-5", "6"), ("x^2 - x - 12", "1", "-1", "-12"),
             ("2x^2 + 5x - 3", "2", "5", "-3"), ("x^2 - 9", "1", "0", "-9"),
             ("3x^2 - 12x", "3", "-12", "0")],
    "factor": [("x^2 + 7x + 12", "1", "7", "12"), ("x^2 - 5x + 6", "1", "-5", "6"),
               ("2x^2 - 7x + 3", "2", "-7", "3"), ("6x^2 + x - 2", "6", "1", "-2"),
               ("x^2 - 16", "1", "0", "-16")],
    "sqrt": [("x^2 - 9 = 0", "1", "0", "-9"), ("x^2 - 5 = 0", "1", "0", "-5"),
             ("4x^2 - 25 = 0", "4", "0", "-25"), ("x^2 + 4 = 0", "1", "0", "4"),
             ("2x^2 - 3 = 0", "2", "0", "-3")],
    "complete": [("x^2 + 6x + 5", "1", "6", "5"), ("x^2 - 4x - 1", "1", "-4", "-1"),
                 ("x^2 + 3x + 1", "1", "3", "1"), ("2x^2 - 8x + 3", "2", "-8", "3"),
                 ("x^2 - 2x - 4", "1", "-2", "-4")],
    "formula": [("x^2 - 2x - 4", "1", "-2", "-4"), ("3x^2 - 6x + 2", "3", "-6", "2"),
                ("x^2 + x - 1", "1", "1", "-1"), ("2x^2 + 3x - 4", "2", "3", "-4"),
                ("x^2 - 6x + 13", "1", "-6", "13")],
    "discriminant": [("x^2 - 4x + 3   (D > 0)", "1", "-4", "3"),
                     ("x^2 - 4x + 4   (D = 0)", "1", "-4", "4"),
                     ("x^2 - 4x + 5   (D < 0)", "1", "-4", "5"),
                     ("x^2 - 2x - 4   (D > 0, irrational)", "1", "-2", "-4"),
                     ("2x^2 + 3x + 5  (D < 0)", "2", "3", "5")],
    "graph": [("x^2 - 4", "1", "0", "-4"), ("-x^2 + 4x - 3", "-1", "4", "-3"),
              ("2x^2 - 4x + 5", "2", "-4", "5"), ("(1/2)x^2 - x - 4", "1/2", "-1", "-4"),
              ("x^2 + 2x + 1", "1", "2", "1")],
    "vertex": [("x^2 - 6x + 5", "1", "-6", "5"), ("x^2 + 4x + 7", "1", "4", "7"),
               ("-2x^2 + 8x - 5", "-2", "8", "-5"), ("3x^2 + 6x + 1", "3", "6", "1"),
               ("x^2 - 3x + 1", "1", "-3", "1")],
    "optimise": [("fence: A = x(40 - x)", "-1", "40", "0"),
                 ("profit: P = -2x^2 + 60x - 200", "-2", "60", "-200"),
                 ("height: h = -5t^2 + 20t + 1", "-5", "20", "1"),
                 ("revenue: R = x(100 - 2x)", "-2", "100", "0"),
                 ("area: A = x(24 - 2x)", "-2", "24", "0")],
    "reducible": [("x^4 - 5x^2 + 4", "1", "-5", "4"), ("x^4 - 13x^2 + 36", "1", "-13", "36"),
                  ("x^4 - 3x^2 - 4", "1", "-3", "-4"), ("2x^4 - 5x^2 + 2", "2", "-5", "2"),
                  ("x^4 + x^2 - 6", "1", "1", "-6")],
}

TITLES = {
    "zero": ("A product that is zero", "Every root comes from one factor being zero"),
    "factor": ("Solving by factoring", "The factored form, found by search"),
    "sqrt": ("The square root property", "Two roots, and the sign that is not optional"),
    "complete": ("Completing the square", "Every step, on the quadratic you chose"),
    "formula": ("The quadratic formula", "Substituted, and checked against the other methods"),
    "discriminant": ("The discriminant", "Counting the roots before finding them"),
    "graph": ("The parabola", "Direction, intercepts, vertex, axis"),
    "vertex": ("Vertex form", "a(x - h)^2 + k, derived by completing the square"),
    "optimise": ("Maximum and minimum", "The vertex is the optimum, with no calculus"),
    "reducible": ("Quadratic in disguise", "Substitute u = x^2, solve, substitute back"),
}


def quadratic_lab(cfg):
    mode = cfg.get("mode", "formula")
    presets = cfg.get("presets") or PRESETS.get(mode, PRESETS["formula"])
    title, subtitle = TITLES.get(mode, TITLES["formula"])
    quartic = "true" if mode == "reducible" else "false"

    options = "".join(
        '<option value="%s|%s|%s">%s</option>' % (a, b, c, label)
        for label, a, b, c in presets
    )

    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="qdTitle">Quadratic</strong><span id="qdSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>the curve</span><span class="tone-green"><i class="legend-swatch"></i>roots</span><span class="tone-purple"><i class="legend-swatch"></i>vertex</span></div>
      </div>
      <div class="lab-stage"><svg id="qdPlot"></svg></div>
      <div id="qdWork" style="margin-top:12px;"></div>
      <div class="status-banner" id="qdStatus" style="margin-top:12px;"></div>"""

    controls = """        <div class="field">
          <label for="qdPreset">Quadratic</label>
          <select id="qdPreset">%s</select>
        </div>
        <div class="field">
          <label for="qdA">a</label>
          <input id="qdA" type="text" value="1" inputmode="text" autocomplete="off">
        </div>
        <div class="field">
          <label for="qdB">b</label>
          <input id="qdB" type="text" value="0" inputmode="text" autocomplete="off">
        </div>
        <div class="field">
          <label for="qdC">c</label>
          <input id="qdC" type="text" value="0" inputmode="text" autocomplete="off">
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>Discriminant</span><strong id="qdDisc">&mdash;</strong></div>
          <div class="kpi"><span>Real roots</span><strong id="qdCount">&mdash;</strong></div>
          <div class="kpi"><span>Vertex</span><strong id="qdVertex">&mdash;</strong></div>
        </div>
        <p class="small-copy" id="qdHint" style="margin:0;">Whole numbers or fractions such as <code>-3/2</code>. Every step below is recomputed from these three.</p>""" % options

    script = RATIONAL_JS + POLY_JS + SURD_JS + PLOT_JS + r"""
  var MODE = '""" + mode + r"""', QUARTIC = """ + quartic + r""";
  var preset = document.getElementById('qdPreset');
  var inA = document.getElementById('qdA'), inB = document.getElementById('qdB'), inC = document.getElementById('qdC');
  var work = document.getElementById('qdWork'), status = document.getElementById('qdStatus');
  var titleOut = document.getElementById('qdTitle'), subOut = document.getElementById('qdSub');
  var svg = document.getElementById('qdPlot');

  function row(label, detail) {
    return '<tr><td style="text-align:left;">' + label + '</td><td style="text-align:left;">' + detail + '</td></tr>';
  }
  function table(caption, rows) {
    return '<div class="table-wrap"><table class="tt"><caption>' + caption + '</caption><tbody>'
      + rows.join('') + '</tbody></table></div>';
  }

  /* ---- the four methods, each computed on its own ---- */

  /* 1. Factoring. The factorisation is SEARCHED for by the rational root
     theorem, so a quadratic that does not factor over the rationals reports
     that rather than silently producing something else. */
  function byFactoring(a, b, c) {
    var poly = [c, b, a];
    var f = Pfactor(poly);
    var linear = f.factors.length;
    if (!linear) return { ok: false, text: 'no factorisation over the rationals: the rational root search returned nothing' };
    var text = Pfactortextfull(poly) + ' = 0';
    var roots = [];
    f.factors.forEach(function (item) { for (var i = 0; i < item.mult; i += 1) roots.push(item.root); });
    if (f.rest.length) return { ok: false, text: text + ' &mdash; the remaining factor has no rational root' };
    return { ok: true, text: text, roots: roots };
  }

  /* 2. The square root property, which applies only when b = 0. */
  function bySquareRoot(a, b, c) {
    if (!Rzero(b)) return { ok: false, text: 'only applies when there is no linear term; here b = ' + Rtext(b) };
    var rhs = Rdiv(Rneg(c), a);
    if (Rsign(rhs) < 0) {
      var im = Rsurd(Rneg(rhs));
      return { ok: true, text: 'x^2 = ' + Rtext(rhs) + ', and no real number squares to a negative: x = +-' + surdtext(im) + 'i' };
    }
    var s = Rsurd(rhs);
    return { ok: true, text: 'x^2 = ' + Rtext(rhs) + ', so x = +-' + surdtext(s) };
  }

  /* 3. Completing the square, printed step by step -- this is the lesson, not
     a means to the answer. */
  function byCompleting(a, b, c) {
    var lines = [];
    lines.push(row('start', Ptext([c, b, a]) + ' = 0'));
    var b1 = Rdiv(b, a), c1 = Rdiv(c, a);
    if (!Requ(a, R1)) lines.push(row('divide by a = ' + Rtext(a), Ptext([c1, b1, R1]) + ' = 0'));
    /* Every line here is written the way a reader is expected to write it, which
       means signs are folded into the term rather than bracketed onto it:
       "x^2 - 3x", not "x^2 + (-3)x". Ptext already applies that rule to a whole
       polynomial, so the trace is rendered through it instead of by gluing
       coefficients together with plus signs. */
    lines.push(row('move the constant', Ptext([R0, b1, R1]) + ' = ' + Rtext(Rneg(c1))));
    var half = Rdiv(b1, R(2n)), sq = Rmul(half, half);
    lines.push(row('half of ' + Rtext(b1) + ', squared',
                   '(' + Rterm(b1) + '/2)^2 = ' + Rtext(sq)));
    lines.push(row('add it to both sides',
                   Ptext([sq, b1, R1]) + ' = ' + Rtext(Radd(Rneg(c1), sq))));
    var rhs = Radd(Rneg(c1), sq);
    var square = Pfactortext([half, R1]) + '^2';
    lines.push(row('the left side is a square', square + ' = ' + Rtext(rhs)));
    var answer;
    if (Rsign(rhs) < 0) {
      var im = Rsurd(Rneg(rhs));
      answer = 'x = ' + pmtext(Rneg(half), im, true);
      lines.push(row('take the square root',
                     Ptext([half, R1]) + ' = +-' + surdtext(im) + 'i'));
    } else {
      var s = Rsurd(rhs);
      answer = 'x = ' + pmtext(Rneg(half), s);
      lines.push(row('take the square root', Ptext([half, R1]) + ' = +-' + surdtext(s)));
    }
    lines.push(row('solve for x', answer));
    return { lines: lines, answer: answer, vertexH: Rneg(half), vertexK: Rmul(a, Rneg(rhs)) };
  }

  /* 4. The formula, with the substitution shown before the arithmetic. */
  function byFormula(a, b, c) {
    var r = quadroots(a, b, c);
    var lines = [];
    lines.push(row('a, b, c', 'a = ' + Rtext(a) + ',  b = ' + Rtext(b) + ',  c = ' + Rtext(c)));
    lines.push(row('substitute', 'x = (-(' + Rtext(b) + ') +- sqrt((' + Rtext(b) + ')^2 - 4(' + Rtext(a) + ')(' + Rtext(c) + '))) / (2 * ' + Rtext(a) + ')'));
    lines.push(row('the discriminant', 'b^2 - 4ac = ' + Rtext(Rmul(b, b)) + ' - ' + Rtext(Rmul(R(4n), Rmul(a, c))) + ' = ' + Rtext(r.disc)));
    if (r.kind === 'complex') {
      lines.push(row('negative, so no real root', 'x = ' + pmtext(r.p, r.s, true)));
    } else if (r.kind === 'double') {
      lines.push(row('zero, so one repeated root', 'x = ' + Rtext(r.p)));
    } else {
      lines.push(row('simplify the radical', 'sqrt(' + Rtext(r.disc) + ') = ' + surdtext(Rsurd(r.disc))));
      lines.push(row('the two roots', 'x = ' + pmtext(r.p, r.s)));
    }
    return { lines: lines, result: r };
  }

  function redraw() {
    var a, b, c;
    try {
      a = Rparse(inA.value); b = Rparse(inB.value); c = Rparse(inC.value);
    } catch (err) { a = null; }
    if (a === null || b === null || c === null) {
      status.innerHTML = '<strong>Each of a, b and c must be a whole number or a fraction.</strong> '
        + 'Try 3, -2 or -3/2.';
      work.textContent = '';
      return;
    }
    if (Rzero(a)) {
      status.innerHTML = '<strong>With a = 0 this is not a quadratic.</strong> '
        + Ptext([c, b]) + ' = 0 is linear, and it has one solution rather than two. '
        + 'The whole method below divides by a, which is the reason the definition of a '
        + 'quadratic insists a is not zero.';
      work.textContent = '';
      svg.textContent = '';
      return;
    }

    var r = quadroots(a, b, c);
    var vh = Rdiv(Rneg(b), Rmul(R(2n), a));
    var vk = Peval([c, b, a], vh);
    document.getElementById('qdDisc').textContent = Rtext(r.disc);
    document.getElementById('qdCount').textContent =
      r.kind === 'complex' ? '0' : (r.kind === 'double' ? '1' : '2');
    document.getElementById('qdVertex').textContent = '(' + Rtext(vh) + ', ' + Rtext(vk) + ')';

    var expr = QUARTIC
      ? Ptext([c, R0, b, R0, a])
      : Ptext([c, b, a]);
    titleOut.textContent = QUARTIC ? expr + ' = 0' : expr + ' = 0';
    subOut.textContent = 'a = ' + Rtext(a) + ', b = ' + Rtext(b) + ', c = ' + Rtext(c);

    /* ---- the picture ---- */
    var av = Rnum(a), bv = Rnum(b), cv = Rnum(c);
    var hv = Rnum(vh), kv = Rnum(vk);
    var f = QUARTIC
      ? function (x) { return av * x * x * x * x + bv * x * x + cv; }
      : function (x) { return av * x * x + bv * x + cv; };
    var span = 6;
    if (r.kind !== 'complex' && r.roots.length) {
      var lo = Math.min.apply(null, r.roots.map(Rnum)), hi = Math.max.apply(null, r.roots.map(Rnum));
      span = Math.max(6, (hi - lo) * 2.2);
    }
    var cx = QUARTIC ? 0 : hv;
    var xmin = cx - span / 2, xmax = cx + span / 2;
    var samples = [];
    for (var i = 0; i <= 60; i += 1) samples.push(f(xmin + (xmax - xmin) * i / 60));
    var ylo = Math.min.apply(null, samples), yhi = Math.max.apply(null, samples);
    if (!QUARTIC) { ylo = Math.min(ylo, kv); yhi = Math.max(yhi, kv); }
    var pad = Math.max(1, (yhi - ylo) * 0.18);
    var plot = Plot(svg, { xmin: xmin, xmax: xmax, ymin: ylo - pad, ymax: yhi + pad });
    plot.frame();
    if (!QUARTIC) plot.segment(hv, ylo - pad, hv, yhi + pad, 'plot-aux');
    plot.curve(f);
    if (r.kind !== 'complex') {
      if (QUARTIC) {
        r.roots.forEach(function (u) {
          if (Rsign(u) < 0) return;
          var s = Math.sqrt(Rnum(u));
          plot.point(s, 0, 'plot-point root');
          if (s > 0) plot.point(-s, 0, 'plot-point root');
        });
      } else {
        r.roots.forEach(function (x) { plot.point(Rnum(x), 0, 'plot-point root', Rtext(x)); });
        if (r.kind === 'irrational') {
          var sv = Rnum(r.s.q) * Math.sqrt(Number(r.s.k));
          plot.point(Rnum(r.p) + sv, 0, 'plot-point root');
          plot.point(Rnum(r.p) - sv, 0, 'plot-point root');
        }
      }
    }
    if (!QUARTIC) plot.point(hv, kv, 'plot-point vertex', 'vertex');
    plot.describe(expr + ' drawn by evaluating it at 480 points, with its '
      + (r.kind === 'complex' ? 'vertex marked and no x-intercept, because the discriminant is negative'
                              : 'roots and vertex marked') + '.');

    /* ---- the work ---- */
    var blocks = [];
    var fac = byFactoring(a, b, c);
    var sqp = bySquareRoot(a, b, c);
    var comp = byCompleting(a, b, c);
    var form = byFormula(a, b, c);

    if (MODE === 'complete' || MODE === 'vertex') {
      blocks.push(table('Completing the square, step by step', comp.lines));
    } else if (MODE === 'formula' || MODE === 'reducible') {
      blocks.push(table('The quadratic formula, substituted', form.lines));
    } else if (MODE === 'factor' || MODE === 'zero') {
      blocks.push(table('Factoring', [
        row('factored form', fac.ok ? fac.text : fac.text),
        row('each factor set to zero', fac.ok
          ? fac.roots.map(function (x) { return 'x = ' + Rtext(x); }).join(',   ')
          : 'not available for this quadratic'),
      ]));
    } else if (MODE === 'sqrt') {
      blocks.push(table('The square root property', [row('applies here?', sqp.text)]));
    }

    /* Every mode ends with the four methods side by side. Agreement between
       independently computed answers is the evidence; a single answer is not. */
    blocks.push(table('The four methods, computed separately', [
      row('factoring', fac.ok ? fac.roots.map(function (x) { return 'x = ' + Rtext(x); }).join(',   ') : '<span class="tone-muted">' + fac.text + '</span>'),
      row('square root property', sqp.ok ? sqp.text : '<span class="tone-muted">' + sqp.text + '</span>'),
      row('completing the square', comp.answer),
      row('the formula', r.kind === 'complex' ? 'x = ' + pmtext(r.p, r.s, true)
          : (r.kind === 'double' ? 'x = ' + Rtext(r.p) : 'x = ' + pmtext(r.p, r.s))),
    ]));

    if (QUARTIC) {
      var back = [];
      back.push(row('substitute u = x^2', Ptext([c, b, a], 'u') + ' = 0'));
      if (r.kind === 'rational' || r.kind === 'double') {
        r.roots.forEach(function (u) {
          if (Rsign(u) > 0) {
            var s = Rsurd(u);
            back.push(row('u = ' + Rtext(u), 'x^2 = ' + Rtext(u) + ', so x = +-' + surdtext(s)));
          } else if (Rzero(u)) {
            back.push(row('u = 0', 'x = 0'));
          } else {
            back.push(row('u = ' + Rtext(u), 'x^2 cannot be negative, so this value of u gives no real x'));
          }
        });
      } else {
        back.push(row('u is not rational here', 'solve for u first, then take square roots'));
      }
      blocks.push(table('Back-substituting', back));
    }
    work.innerHTML = blocks.join('');

    /* ---- what the reader should take away ---- */
    var msg;
    if (r.kind === 'complex') {
      msg = '<strong>The discriminant is ' + Rtext(r.disc) + ', which is negative.</strong> '
        + 'The parabola above never meets the x-axis, and the two solutions are the conjugate '
        + 'pair x = ' + pmtext(r.p, r.s, true) + '. Those are not "no solutions" &mdash; they are '
        + 'two solutions that are not real numbers.';
    } else if (r.kind === 'double') {
      msg = '<strong>The discriminant is exactly 0.</strong> The formula gives one value, '
        + 'x = ' + Rtext(r.p) + ', and the parabola touches the axis there without crossing. '
        + 'The factored form has that bracket twice, which is what "repeated root" means.';
    } else if (r.kind === 'rational') {
      msg = '<strong>The discriminant is ' + Rtext(r.disc) + ', a perfect square.</strong> '
        + 'That is exactly the condition for this quadratic to factor over the rationals, which is '
        + 'why factoring works here and fails on the next preset. The roots are '
        + r.roots.map(Rtext).join(' and ') + '.';
    } else {
      msg = '<strong>The discriminant is ' + Rtext(r.disc) + ': positive, but not a perfect square.</strong> '
        + 'There are two real roots, x = ' + pmtext(r.p, r.s) + ', and no factorisation over the '
        + 'rationals &mdash; which is why the factoring row above is empty. An irrational root is '
        + 'still an exact answer; ' + Rdec(r.p, 4) + ' +- ' + Rdec(r.s.q, 4) + '*sqrt(' + r.s.k + ') is a rounding of it.';
    }
    if (!QUARTIC) {
      msg += ' The vertex is at (' + Rtext(vh) + ', ' + Rtext(vk) + '), on the axis x = ' + Rtext(vh)
        + ', and the parabola opens ' + (Rsign(a) > 0 ? 'upward' : 'downward')
        + ', so that point is a ' + (Rsign(a) > 0 ? 'minimum' : 'maximum') + '.';
    }
    status.innerHTML = msg;
  }

  preset.addEventListener('change', function () {
    var parts = preset.value.split('|');
    inA.value = parts[0]; inB.value = parts[1]; inC.value = parts[2];
    redraw();
  });
  [inA, inB, inC].forEach(function (el) { el.addEventListener('input', redraw); });
  var first = preset.value.split('|');
  inA.value = first[0]; inB.value = first[1]; inC.value = first[2];
  redraw();
  window.redrawLab = redraw;
"""

    return Lab(
        title=title,
        subtitle=subtitle,
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose or type a quadratic"),
        panel_intro=cfg.get(
            "panel_intro",
            "Change a, b or c and everything below is recomputed: the four methods, "
            "the discriminant, and the parabola drawn through the roots it found.",
        ),
        script=script,
    )
