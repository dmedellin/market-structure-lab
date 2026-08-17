"""Labs for course 5: discrete probability."""

from .common import Lab, cfg_literal

FRACTION_JS = r"""
  /* Probabilities are kept as exact fractions. A finite equally-likely sample
     space makes every probability a ratio of counts, so there is no reason to
     ever show 0.1666666666666666 -- and every reason not to, because 1/6 is
     the answer and the decimal is a lossy rendering of it. */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function frac(n, d) {
    if (d === 0) return { n: 0, d: 0, text: 'undefined', dec: NaN };
    var g = gcd(n, d), sn = n / g, sd = d / g;
    return { n: sn, d: sd, text: sn === 0 ? '0' : (sd === 1 ? String(sn) : sn + '/' + sd), dec: n / d };
  }
  function pct(f) { return isNaN(f.dec) ? '—' : (100 * f.dec).toFixed(2) + '%'; }
"""


def probability_lab(cfg):
    """Every outcome listed, every probability a ratio of counts.

    Conditional probability is where intuition fails hardest, and it fails less
    when the sample space is on the screen: P(A | B) is not a new axiom, it is
    the same counting restricted to the rows that satisfy B. The lab shows the
    restriction happening.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="prExp">Sample space</strong><span id="prCount"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>in A</span><span class="tone-purple"><i class="legend-swatch"></i>in B</span><span class="tone-green"><i class="legend-swatch"></i>in both</span></div>
      </div>
      <div class="lab-stage"><div id="prSpace"></div></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="prTable"></table></div>
      <div class="status-banner" id="prStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="prExperiment">Experiment</label>
          <select id="prExperiment">
            <option value="dice2">Roll two fair dice</option>
            <option value="coins4">Flip four fair coins</option>
            <option value="urn">Draw 2 of 6 balls without replacement</option>
            <option value="cards">Deal 2 from a 12-card deck</option>
          </select>
        </div>
        <div class="field">
          <label for="prA">Event A</label>
          <select id="prA"></select>
        </div>
        <div class="field">
          <label for="prB">Event B (the condition)</label>
          <select id="prB"></select>
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>P(A)</span><strong id="prPA">&mdash;</strong></div>
          <div class="kpi"><span>P(B)</span><strong id="prPB">&mdash;</strong></div>
          <div class="kpi"><span>P(A|B)</span><strong id="prPAB">&mdash;</strong></div>
        </div>"""

    script = FRACTION_JS + r"""
  var expSel = document.getElementById('prExperiment');
  var aSel = document.getElementById('prA'), bSel = document.getElementById('prB');
  var space = document.getElementById('prSpace'), table = document.getElementById('prTable');
  var status = document.getElementById('prStatus');
  var expName = document.getElementById('prExp'), countOut = document.getElementById('prCount');

  function product(sets) {
    return sets.reduce(function (acc, s) {
      var out = [];
      acc.forEach(function (a) { s.forEach(function (v) { out.push(a.concat([v])); }); });
      return out;
    }, [[]]);
  }
  function pairs(items) {
    var out = [];
    for (var i = 0; i < items.length; i += 1) for (var j = i + 1; j < items.length; j += 1) out.push([items[i], items[j]]);
    return out;
  }

  var EXPERIMENTS = {
    dice2: {
      name: 'Two fair dice',
      outcomes: function () { return product([[1,2,3,4,5,6], [1,2,3,4,5,6]]); },
      label: function (o) { return o[0] + ',' + o[1]; },
      events: [
        ['sum is 7', function (o) { return o[0] + o[1] === 7; }],
        ['sum is at least 9', function (o) { return o[0] + o[1] >= 9; }],
        ['the first die is 4', function (o) { return o[0] === 4; }],
        ['a double', function (o) { return o[0] === o[1]; }],
        ['at least one 6', function (o) { return o[0] === 6 || o[1] === 6; }],
        ['both dice even', function (o) { return o[0] % 2 === 0 && o[1] % 2 === 0; }],
        ['sum is even', function (o) { return (o[0] + o[1]) % 2 === 0; }]
      ]
    },
    coins4: {
      name: 'Four fair coins',
      outcomes: function () { return product([['H','T'], ['H','T'], ['H','T'], ['H','T']]); },
      label: function (o) { return o.join(''); },
      events: [
        ['exactly two heads', function (o) { return o.filter(function (c) { return c === 'H'; }).length === 2; }],
        ['at least three heads', function (o) { return o.filter(function (c) { return c === 'H'; }).length >= 3; }],
        ['the first flip is heads', function (o) { return o[0] === 'H'; }],
        ['all four the same', function (o) { return o.every(function (c) { return c === o[0]; }); }],
        ['more heads than tails', function (o) { return o.filter(function (c) { return c === 'H'; }).length > 2; }],
        ['the last flip is heads', function (o) { return o[3] === 'H'; }]
      ]
    },
    urn: {
      name: '6 balls: 3 red (r1–r3), 2 blue (b1–b2), 1 green (g1)',
      outcomes: function () { return pairs(['r1','r2','r3','b1','b2','g1']); },
      label: function (o) { return o.join('+'); },
      events: [
        ['both red', function (o) { return o.every(function (x) { return x[0] === 'r'; }); }],
        ['at least one red', function (o) { return o.some(function (x) { return x[0] === 'r'; }); }],
        ['no blue', function (o) { return !o.some(function (x) { return x[0] === 'b'; }); }],
        ['the green ball is drawn', function (o) { return o.indexOf('g1') !== -1; }],
        ['two different colours', function (o) { return o[0][0] !== o[1][0]; }]
      ]
    },
    cards: {
      name: '12 cards: A–F in two suits (♠, ♥)',
      outcomes: function () {
        var deck = [];
        ['A','B','C','D','E','F'].forEach(function (r) { ['♠','♥'].forEach(function (s) { deck.push(r + s); }); });
        return pairs(deck);
      },
      label: function (o) { return o.join(' '); },
      events: [
        ['a pair (same rank)', function (o) { return o[0][0] === o[1][0]; }],
        ['both spades', function (o) { return o[0][1] === '♠' && o[1][1] === '♠'; }],
        ['at least one A', function (o) { return o[0][0] === 'A' || o[1][0] === 'A'; }],
        ['same suit', function (o) { return o[0][1] === o[1][1]; }],
        ['contains A♠', function (o) { return o.indexOf('A♠') !== -1; }]
      ]
    }
  };

  function fillEvents() {
    var exp = EXPERIMENTS[expSel.value];
    [aSel, bSel].forEach(function (sel) { sel.textContent = ''; });
    exp.events.forEach(function (e, i) {
      [aSel, bSel].forEach(function (sel) {
        var o = document.createElement('option');
        o.value = String(i); o.textContent = e[0];
        sel.appendChild(o);
      });
    });
    aSel.value = '0';
    bSel.value = String(Math.min(2, exp.events.length - 1));
  }

  function redraw() {
    var exp = EXPERIMENTS[expSel.value];
    var outcomes = exp.outcomes();
    var A = exp.events[+aSel.value], B = exp.events[+bSel.value];
    var nA = 0, nB = 0, nAB = 0;
    var cells = outcomes.map(function (o) {
      var a = A[1](o), b = B[1](o);
      if (a) nA += 1;
      if (b) nB += 1;
      if (a && b) nAB += 1;
      var cls = a && b ? 'ok' : a ? 'hi' : b ? '' : '';
      var style = a && b ? 'border-color:var(--green);color:var(--green);'
        : a ? 'border-color:var(--cyan);color:var(--cyan);'
        : b ? 'border-color:var(--purple);color:var(--purple);' : 'opacity:0.5;';
      return '<span class="chip" style="' + style + '">' + exp.label(o) + '</span>';
    });
    space.innerHTML = cells.join('');
    var total = outcomes.length;
    expName.textContent = exp.name;
    countOut.textContent = total + ' equally likely outcomes';

    var pA = frac(nA, total), pB = frac(nB, total), pAB = frac(nAB, total);
    var cond = frac(nAB, nB), condBA = frac(nAB, nA);
    var pAtimesB = frac(nA * nB, total * total);
    var independent = nB > 0 && nA * nB === nAB * total;

    document.getElementById('prPA').textContent = pA.text;
    document.getElementById('prPB').textContent = pB.text;
    document.getElementById('prPAB').textContent = cond.text;

    table.innerHTML = '<thead><tr><th>quantity</th><th>count</th><th>exact</th><th>decimal</th></tr></thead><tbody>'
      + '<tr><td>P(A)</td><td>' + nA + ' / ' + total + '</td><td>' + pA.text + '</td><td>' + pct(pA) + '</td></tr>'
      + '<tr><td>P(B)</td><td>' + nB + ' / ' + total + '</td><td>' + pB.text + '</td><td>' + pct(pB) + '</td></tr>'
      + '<tr><td>P(A ∩ B)</td><td>' + nAB + ' / ' + total + '</td><td>' + pAB.text + '</td><td>' + pct(pAB) + '</td></tr>'
      + '<tr class="focus"><td>P(A | B) = P(A∩B)/P(B)</td><td>' + nAB + ' / ' + nB + '</td><td>' + cond.text + '</td><td>' + pct(cond) + '</td></tr>'
      + '<tr><td>P(B | A) = P(A∩B)/P(A)</td><td>' + nAB + ' / ' + nA + '</td><td>' + condBA.text + '</td><td>' + pct(condBA) + '</td></tr>'
      + '<tr><td>P(A)·P(B)</td><td>—</td><td>' + pAtimesB.text + '</td><td>' + pct(pAtimesB) + '</td></tr>'
      + '</tbody>';

    var bayesOk = nA > 0 && nB > 0
      && Math.abs(cond.dec - (condBA.dec * pA.dec) / pB.dec) < 1e-12;
    status.innerHTML = '<strong>Conditioning is not a new rule, it is a smaller sample space.</strong> '
      + 'B holds in ' + nB + ' of the ' + total + ' outcomes; among those, A holds in ' + nAB
      + '. So P(A | B) = ' + nAB + '/' + nB + ' = ' + cond.text + ', while P(A) = ' + pA.text + '. '
      + (independent
          ? 'Here P(A∩B) = P(A)·P(B) exactly, so A and B are <strong>independent</strong>: learning B happened '
            + 'tells you nothing about A. Independence is this equation, not a story about causes.'
          : 'P(A∩B) = ' + pAB.text + ' but P(A)·P(B) = ' + pAtimesB.text + ', so A and B are <strong>dependent</strong>.')
      + (bayesOk ? ' Bayes checks out too: P(A|B)·P(B) = P(B|A)·P(A), both equal P(A∩B).' : '');
  }

  expSel.addEventListener('change', function () { fillEvents(); redraw(); });
  aSel.addEventListener('change', redraw);
  bSel.addEventListener('change', redraw);
  expSel.value = """ + '"%s"' % cfg.get("experiment", "dice2") + r""";
  fillEvents();
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Sample space, event, condition",
        subtitle="Exact fractions, every outcome listed",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose an experiment and two events"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every outcome of the experiment is drawn above, so each probability "
            "below is a count you can verify by eye.",
        ),
        script=script,
    )


def distribution_lab(cfg):
    """A distribution, its expectation and its variance, from the definition.

    E[X] is computed here as the sum over outcomes of x·P(X = x), not by
    applying np -- and then the closed form is printed beside it. Seeing the two
    agree is what makes the closed form usable; being handed it is not.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="dsTitle">Distribution</strong><span id="dsSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>P(X = k)</span><span class="tone-amber"><i class="legend-swatch"></i>E[X]</span></div>
      </div>
      <div class="lab-stage"><svg id="dsPlot" viewBox="0 0 520 220" role="img" aria-label="Probability mass function drawn as bars, with the expected value marked."></svg></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="dsTable"></table></div>
      <div class="status-banner" id="dsStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="dsKind">Distribution</label>
          <select id="dsKind">
            <option value="binomial">Binomial: successes in n trials</option>
            <option value="geometric">Geometric: trials until the first success</option>
            <option value="uniform">Uniform on 1 … n</option>
            <option value="dice">Sum of two fair dice</option>
          </select>
        </div>
        <div id="dsNWrap">
          <div class="range-row"><label class="small-copy" for="dsN">n</label><span class="range-value" id="dsNOut">10</span></div>
          <input id="dsN" type="range" min="1" max="20" value="10" />
        </div>
        <div id="dsPWrap">
          <div class="range-row"><label class="small-copy" for="dsP">p (in twelfths)</label><span class="range-value" id="dsPOut">6/12</span></div>
          <input id="dsP" type="range" min="1" max="11" value="6" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>E[X] summed</span><strong id="dsE">&mdash;</strong></div>
          <div class="kpi"><span>E[X] formula</span><strong id="dsEF">&mdash;</strong></div>
          <div class="kpi"><span>Var(X)</span><strong id="dsV">&mdash;</strong></div>
        </div>"""

    script = FRACTION_JS + r"""
  var kindSel = document.getElementById('dsKind'), nS = document.getElementById('dsN'), pS = document.getElementById('dsP');
  var plot = document.getElementById('dsPlot'), table = document.getElementById('dsTable');
  var status = document.getElementById('dsStatus');
  var title = document.getElementById('dsTitle'), sub = document.getElementById('dsSub');

  function comb(n, r) {
    if (r < 0 || r > n) return 0;
    var out = 1;
    for (var i = 0; i < r; i += 1) out = out * (n - i) / (i + 1);
    return Math.round(out);
  }

  function redraw() {
    var kind = kindSel.value, n = +nS.value, pn = +pS.value, p = pn / 12;
    document.getElementById('dsNOut').textContent = n;
    document.getElementById('dsPOut').textContent = pn + '/12';
    /* Hide the controls a distribution does not use, addressing the WRAPPERS by
       id rather than by walking to a parent node. Reaching for parentElement
       couples the script to the markup's nesting: it works until someone adds a
       wrapping div, and then it hides the wrong element or throws. */
    document.getElementById('dsNWrap').hidden = kind === 'dice';
    document.getElementById('dsPWrap').hidden = kind === 'uniform' || kind === 'dice';

    var ks = [], probs = [], formulaE = '', formulaV = '', name = '', note = '';
    if (kind === 'binomial') {
      name = 'Binomial(n = ' + n + ', p = ' + pn + '/12)';
      for (var k = 0; k <= n; k += 1) {
        ks.push(k);
        probs.push(comb(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k));
      }
      formulaE = 'np = ' + n + '·' + pn + '/12 = ' + frac(n * pn, 12).text;
      formulaV = 'np(1−p) = ' + (n * p * (1 - p)).toFixed(4);
      note = 'The binomial counts SUCCESSES in a fixed number of independent trials. Its expectation is n·p '
        + 'for a reason worth more than the formula: X is a sum of n indicator variables, each with expectation p, '
        + 'and expectation adds even when the indicators are not independent.';
    } else if (kind === 'geometric') {
      name = 'Geometric(p = ' + pn + '/12)';
      var tail = 1;
      for (var k2 = 1; k2 <= 30; k2 += 1) {
        ks.push(k2);
        probs.push(Math.pow(1 - p, k2 - 1) * p);
      }
      formulaE = '1/p = 12/' + pn + ' = ' + frac(12, pn).text + ' ≈ ' + (1 / p).toFixed(4);
      formulaV = '(1−p)/p² = ' + ((1 - p) / (p * p)).toFixed(4);
      note = 'The geometric counts TRIALS UNTIL the first success. Its expectation 1/p is the memorable one: '
        + 'a 1-in-6 event takes 6 trials on average — but the distribution is heavily skewed, so "on average 6" '
        + 'is not "usually about 6". The table below is truncated at 30; the true support is infinite.';
    } else if (kind === 'uniform') {
      name = 'Uniform on 1 … ' + n;
      for (var k3 = 1; k3 <= n; k3 += 1) { ks.push(k3); probs.push(1 / n); }
      formulaE = '(n+1)/2 = ' + frac(n + 1, 2).text;
      formulaV = '(n²−1)/12 = ' + ((n * n - 1) / 12).toFixed(4);
      note = 'Every value equally likely. The expectation is the midpoint, which is the one case where '
        + '"average" and "typical" coincide.';
    } else {
      name = 'Sum of two fair dice';
      for (var s = 2; s <= 12; s += 1) {
        ks.push(s);
        probs.push((6 - Math.abs(7 - s)) / 36);
      }
      formulaE = '7 (by symmetry, or 3.5 + 3.5 by linearity)';
      formulaV = '35/6 ≈ 5.8333';
      note = 'Not uniform, even though each die is: there are six ways to make 7 and one to make 2. '
        + 'The expectation 7 follows from linearity — E[X+Y] = E[X] + E[Y] — without touching this distribution at all.';
    }

    /* E and Var from the DEFINITION, summed term by term. */
    var E = 0, E2 = 0, total = 0;
    for (var i = 0; i < ks.length; i += 1) { E += ks[i] * probs[i]; E2 += ks[i] * ks[i] * probs[i]; total += probs[i]; }
    var V = E2 - E * E;

    document.getElementById('dsE').textContent = E.toFixed(4);
    document.getElementById('dsEF').textContent = formulaE;
    document.getElementById('dsV').textContent = V.toFixed(4);

    var maxP = Math.max.apply(null, probs) || 1;
    var w = 520 / ks.length, s2 = '';
    for (var j = 0; j < ks.length; j += 1) {
      var h = (probs[j] / maxP) * 165;
      s2 += '<rect x="' + (j * w + 2) + '" y="' + (185 - h) + '" width="' + Math.max(2, w - 4) + '" height="' + h
        + '" rx="2" fill="var(--cyan)" opacity="0.82" />';
      if (ks.length <= 21) {
        s2 += '<text x="' + (j * w + w / 2) + '" y="203" text-anchor="middle" font-size="9" fill="var(--muted)">' + ks[j] + '</text>';
      }
    }
    var ex = ((E - ks[0]) / (ks[ks.length - 1] - ks[0] || 1)) * (520 - w) + w / 2;
    s2 += '<line x1="' + ex + '" y1="8" x2="' + ex + '" y2="185" stroke="var(--amber)" stroke-width="2" stroke-dasharray="5 4" />';
    s2 += '<text x="' + Math.min(ex + 6, 470) + '" y="18" font-size="10" fill="var(--amber)" font-weight="700">E[X] = ' + E.toFixed(3) + '</text>';
    s2 += '<line x1="0" y1="185" x2="520" y2="185" stroke="var(--line-strong)" stroke-width="1" />';
    plot.innerHTML = s2;

    var rows = '';
    for (var t = 0; t < Math.min(ks.length, 14); t += 1) {
      rows += '<tr><td>' + ks[t] + '</td><td>' + probs[t].toFixed(6) + '</td><td>' + (100 * probs[t]).toFixed(3) + '%</td><td>'
        + (ks[t] * probs[t]).toFixed(6) + '</td></tr>';
    }
    table.innerHTML = '<thead><tr><th>k</th><th>P(X = k)</th><th>%</th><th>k·P(X = k)</th></tr></thead><tbody>'
      + rows + '<tr class="focus"><td>Σ</td><td>' + total.toFixed(6) + '</td><td>' + (100 * total).toFixed(2)
      + '%</td><td>' + E.toFixed(6) + '</td></tr></tbody>';

    title.textContent = name;
    sub.textContent = 'E[X] and Var(X) summed from the definition';
    status.innerHTML = '<strong>Summed from the definition: E[X] = ' + E.toFixed(4) + '.</strong> '
      + 'The closed form says ' + formulaE + ', and Var(X) = E[X²] − E[X]² = ' + V.toFixed(4)
      + ' against ' + formulaV + '. ' + note
      + (total < 0.999 ? ' The probabilities shown sum to ' + total.toFixed(4) + ' because the table is truncated.' : '');
  }

  [kindSel, nS, pS].forEach(function (el) { el.addEventListener('input', redraw); });
  kindSel.addEventListener('change', redraw);
  kindSel.value = """ + '"%s"' % cfg.get("kind", "binomial") + r""";
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Distribution, expectation, variance",
        subtitle="Definition first, formula second",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a distribution"),
        panel_intro=cfg.get(
            "panel_intro",
            "The expectation is summed term by term and then compared with the "
            "closed form, so the formula arrives as a result rather than a rule.",
        ),
        script=script,
    )
