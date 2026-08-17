"""Labs for course 3: induction and recursion."""

from .common import Lab, cfg_literal


def induction_lab(cfg):
    """Check P(n) for as many n as you like -- and watch that not be enough.

    This is the one lab on the path with a deliberately adversarial design. Two
    of its statements are FALSE and survive every check a reasonable person
    would run: n^2 + n + 41 is prime for n = 0 through 39, and the chord-region
    count matches 2^(n-1) for n = 1 through 5. A reader who has just been told
    "verify the base case, then the step" needs to meet the failure mode of
    verifying instead of proving, in a lab that let them believe it first.

    Everything is computed with exact integers, so the failures are real
    failures and not floating-point noise.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>P(n), checked one n at a time</strong><span id="indCaption"></span></div>
        <div class="inline-legend"><span class="tone-green"><i class="legend-swatch"></i>holds</span><span class="tone-red"><i class="legend-swatch"></i>fails</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="indTable"></div></div>
      <div class="status-banner" id="indStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="indStmt">Statement</label>
          <select id="indStmt"></select>
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="indN">Check up to n =</label><span class="range-value" id="indNOut">10</span></div>
          <input id="indN" type="range" min="1" max="60" value="10" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>Checked</span><strong id="indChecked">&mdash;</strong></div>
          <div class="kpi"><span>Held</span><strong id="indHeld">&mdash;</strong></div>
          <div class="kpi"><span>First failure</span><strong id="indFirst">&mdash;</strong></div>
        </div>
        <div class="note" id="indStep"></div>"""

    script = cfg_literal("IND_DEFAULT", cfg.get("statement", "sum")) + r"""
  /* Exact integer arithmetic throughout: these statements are about integers,
     and a check that rounded would report failures that are not there and miss
     failures that are. */
  function isPrime(n) {
    if (n < 2n) return false;
    for (var d = 2n; d * d <= n; d += 1n) if (n % d === 0n) return false;
    return true;
  }
  function comb(n, r) {
    if (r < 0 || r > n) return 0n;
    var num = 1n, den = 1n;
    for (var i = 0; i < r; i += 1) { num *= BigInt(n - i); den *= BigInt(i + 1); }
    return num / den;
  }

  var STATEMENTS = [
    {
      id: 'sum', label: '1 + 2 + … + n = n(n+1)/2', from: 1, truth: true,
      lhsName: 'Σ i', rhsName: 'n(n+1)/2',
      lhs: function (n) { var s = 0n; for (var i = 1n; i <= BigInt(n); i += 1n) s += i; return s; },
      rhs: function (n) { var N = BigInt(n); return N * (N + 1n) / 2n; },
      step: 'Assume Σ_{i≤k} i = k(k+1)/2. Then Σ_{i≤k+1} i = k(k+1)/2 + (k+1) = (k+1)(k+2)/2, which is the claim at k+1.'
    },
    {
      id: 'odd', label: '1 + 3 + 5 + … + (2n−1) = n²', from: 1, truth: true,
      lhsName: 'Σ (2i−1)', rhsName: 'n²',
      lhs: function (n) { var s = 0n; for (var i = 1n; i <= BigInt(n); i += 1n) s += 2n * i - 1n; return s; },
      rhs: function (n) { return BigInt(n) * BigInt(n); },
      step: 'Assume the sum of the first k odd numbers is k². Adding the next odd number gives k² + (2k+1) = (k+1)².'
    },
    {
      id: 'cubes', label: '1³ + 2³ + … + n³ = (n(n+1)/2)²', from: 1, truth: true,
      lhsName: 'Σ i³', rhsName: '(n(n+1)/2)²',
      lhs: function (n) { var s = 0n; for (var i = 1n; i <= BigInt(n); i += 1n) s += i * i * i; return s; },
      rhs: function (n) { var N = BigInt(n), t = N * (N + 1n) / 2n; return t * t; },
      step: 'Assume Σ_{i≤k} i³ = (k(k+1)/2)². Adding (k+1)³ gives ((k+1)(k+2)/2)² after factoring — the sum of cubes is always a perfect square, and it is the square of the sum.'
    },
    {
      id: 'pow', label: '2ⁿ > n²  (for n ≥ 5)', from: 1, truth: true, holdsFrom: 5,
      lhsName: '2ⁿ', rhsName: 'n²',
      lhs: function (n) { return 2n ** BigInt(n); },
      rhs: function (n) { return BigInt(n) * BigInt(n); },
      compare: 'gt',
      step: 'The base case is n = 5 (32 > 25), NOT n = 1: the statement is false at n = 2, 3 and 4. The step uses 2^{k+1} = 2·2^k > 2k² ≥ (k+1)² for k ≥ 3.'
    },
    {
      id: 'div6', label: 'n³ − n is divisible by 6', from: 1, truth: true,
      lhsName: '(n³−n) mod 6', rhsName: '0',
      lhs: function (n) { var N = BigInt(n); return (N * N * N - N) % 6n; },
      rhs: function () { return 0n; },
      step: 'n³ − n = (n−1)n(n+1), three consecutive integers: one is divisible by 2 and one by 3. Induction works too — the step adds 3k(k+1), and k(k+1) is even.'
    },
    {
      id: 'prime41', label: 'n² + n + 41 is prime', from: 0, truth: false,
      lhsName: 'n² + n + 41', rhsName: 'prime?',
      lhs: function (n) { var N = BigInt(n); return N * N + N + 41n; },
      rhs: function () { return null; },
      predicate: function (n) { var N = BigInt(n); return isPrime(N * N + N + 41n); },
      step: 'There is no inductive step here, and that is the point: the statement is FALSE. It holds for n = 0 through 39 and fails at n = 40, where the value is 40² + 40 + 41 = 1681 = 41². Push the slider past 39.'
    },
    {
      id: 'chords', label: 'n points on a circle, all chords drawn, give 2ⁿ⁻¹ regions', from: 1, truth: false,
      lhsName: 'regions', rhsName: '2ⁿ⁻¹',
      lhs: function (n) { return 1n + comb(n, 2) + comb(n, 4); },
      rhs: function (n) { return 2n ** BigInt(n - 1); },
      step: 'False again, and it survives longer than anyone expects: 1, 2, 4, 8, 16 for n = 1…5, then 31 rather than 32 at n = 6. The true count is 1 + C(n,2) + C(n,4). Five confirmations in a row is not a proof.'
    },
    {
      id: 'harm', label: '1/(1·2) + 1/(2·3) + … + 1/(n(n+1)) = n/(n+1)', from: 1, truth: true,
      lhsName: 'Σ 1/(i(i+1))  (as a fraction)', rhsName: 'n/(n+1)',
      rational: true,
      step: 'Telescoping: 1/(i(i+1)) = 1/i − 1/(i+1), so all the middle terms cancel and 1 − 1/(n+1) = n/(n+1) is left. The sum is computed below in exact fractions so the equality is not a rounding artefact.'
    }
  ];

  var stmtSel = document.getElementById('indStmt');
  STATEMENTS.forEach(function (s) {
    var o = document.createElement('option');
    o.value = s.id; o.innerHTML = s.label;
    stmtSel.appendChild(o);
  });

  var nS = document.getElementById('indN'), table = document.getElementById('indTable');
  var status = document.getElementById('indStatus'), stepOut = document.getElementById('indStep');
  var caption = document.getElementById('indCaption');

  function gcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { var t = a % b; a = b; b = t; } return a; }

  function rationalSum(n) {
    var num = 0n, den = 1n;
    for (var i = 1n; i <= BigInt(n); i += 1n) {
      var d = i * (i + 1n);
      num = num * d + den; den = den * d;
      var g = gcd(num, den); num /= g; den /= g;
    }
    return [num, den];
  }

  function redraw() {
    var s = STATEMENTS.filter(function (x) { return x.id === stmtSel.value; })[0];
    var N = +nS.value;
    document.getElementById('indNOut').textContent = N;
    var rows = '', checked = 0, held = 0, first = null;
    var start = s.holdsFrom || s.from;
    for (var n = s.from; n <= N; n += 1) {
      var ok, left, right;
      if (s.rational) {
        var r = rationalSum(n);
        left = r[0] + '/' + r[1];
        right = n + '/' + (n + 1);
        var g = gcd(BigInt(n), BigInt(n + 1));
        ok = r[0] === BigInt(n) / g && r[1] === BigInt(n + 1) / g;
      } else if (s.predicate) {
        left = s.lhs(n).toString();
        ok = s.predicate(n);
        right = ok ? 'prime' : 'composite';
      } else {
        var lv = s.lhs(n), rv = s.rhs(n);
        left = lv.toString(); right = rv.toString();
        ok = s.compare === 'gt' ? lv > rv : lv === rv;
      }
      var counts = n >= start;
      if (counts) { checked += 1; if (ok) held += 1; else if (first === null) first = n; }
      rows += '<tr' + (!ok && counts ? ' class="focus"' : '') + '><td>' + n + '</td><td>' + left + '</td><td>'
        + right + '</td><td class="' + (ok ? 't' : 'f') + '">' + (ok ? 'holds' : 'FAILS') + '</td></tr>';
    }
    table.innerHTML = '<table class="tt"><thead><tr><th>n</th><th>' + (s.lhsName || 'left')
      + '</th><th>' + (s.rhsName || 'right') + '</th><th>P(n)</th></tr></thead><tbody>' + rows + '</tbody></table>';
    document.getElementById('indChecked').textContent = checked;
    document.getElementById('indHeld').textContent = held;
    document.getElementById('indFirst').textContent = first === null ? 'none yet' : 'n = ' + first;
    caption.textContent = 'n = ' + s.from + ' to ' + N;
    stepOut.innerHTML = '<strong>Inductive step:</strong> ' + s.step;

    if (first !== null) {
      status.innerHTML = '<strong>Found a counterexample at n = ' + first + '.</strong> '
        + 'Every earlier n held, and none of that mattered: one failure ends the claim. '
        + 'This is why induction proves the STEP rather than checking cases &mdash; a step that works '
        + 'carries the claim past every n you could ever check by hand.';
    } else if (!s.truth) {
      status.innerHTML = '<strong>All ' + checked + ' checks passed &mdash; and the statement is still false.</strong> '
        + 'Push the slider further. A run of confirmations is evidence about the numbers you looked at '
        + 'and about nothing else.';
    } else {
      status.innerHTML = 'All ' + checked + ' checks passed. <strong>That is not a proof</strong>, and this lab '
        + 'contains two statements that pass dozens of checks and are false. What makes this one true is the '
        + 'step above: it turns P(k) into P(k+1) for EVERY k, which no amount of checking can do.';
    }
  }

  stmtSel.addEventListener('change', function () {
    var s = STATEMENTS.filter(function (x) { return x.id === stmtSel.value; })[0];
    if (s.id === 'prime41') nS.value = Math.max(+nS.value, 20);
    redraw();
  });
  nS.addEventListener('input', redraw);
  stmtSel.value = IND_DEFAULT;
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Check P(n), then notice checking is not proving",
        subtitle="Two of these statements are false",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a statement"),
        panel_intro=cfg.get(
            "panel_intro",
            "Two entries in this list are false and survive every check a careful "
            "person would run. Find them before reading on.",
        ),
        script=script,
    )


def recurrence_lab(cfg):
    """A recurrence iterated, and its closed form derived and checked.

    The characteristic equation is solved exactly where its roots are rational,
    so the closed form printed is the closed form, not a fit. Then every term
    is compared against the iteration: agreement across the whole range is what
    makes the algebra trustworthy, and the lab shows the comparison instead of
    asserting it.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>a<sub>n</sub> = c₁·a<sub>n−1</sub> + c₂·a<sub>n−2</sub> + f(n)</strong><span id="recCaption"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>iterated</span><span class="tone-purple"><i class="legend-swatch"></i>closed form</span></div>
      </div>
      <div class="lab-stage">
        <svg id="recPlot" viewBox="0 0 520 200" role="img" aria-label="The first terms of the sequence, drawn as bars."></svg>
        <div class="table-wrap" style="margin-top:10px;"><table class="tt" id="recTable"></table></div>
      </div>
      <div class="status-banner" id="recStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="recPreset">Recurrence</label>
          <select id="recPreset">
            <option value="fib">Fibonacci: aₙ = aₙ₋₁ + aₙ₋₂, a₀=0, a₁=1</option>
            <option value="hanoi">Tower of Hanoi: aₙ = 2aₙ₋₁ + 1, a₀=0</option>
            <option value="geo">Doubling: aₙ = 2aₙ₋₁, a₀=1</option>
            <option value="two">aₙ = 5aₙ₋₁ − 6aₙ₋₂, a₀=1, a₁=5</option>
            <option value="rep">Repeated root: aₙ = 4aₙ₋₁ − 4aₙ₋₂, a₀=1, a₁=4</option>
            <option value="lin">aₙ = aₙ₋₁ + n, a₀=0 (triangular)</option>
            <option value="merge">Merge sort: T(n) = 2T(n/2) + n</option>
          </select>
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="recTerms">Terms shown</label><span class="range-value" id="recTermsOut">12</span></div>
          <input id="recTerms" type="range" min="4" max="24" value="12" />
        </div>
        <div class="field">
          <label>Closed form</label>
          <div class="mathblock" id="recClosed" style="font-size:0.84rem;"></div>
        </div>"""

    script = r"""
  var presetSel = document.getElementById('recPreset'), termsS = document.getElementById('recTerms');
  var plot = document.getElementById('recPlot'), table = document.getElementById('recTable');
  var closedOut = document.getElementById('recClosed'), status = document.getElementById('recStatus');
  var caption = document.getElementById('recCaption');

  /* Each entry supplies the ITERATION and, separately, the closed form. They
     are computed independently and then compared, which is the only way the
     comparison means anything. */
  var RECS = {
    fib: {
      label: 'aₙ = aₙ₋₁ + aₙ₋₂', init: [0n, 1n],
      next: function (a, n) { return a[n - 1] + a[n - 2]; },
      closed: 'aₙ = (φⁿ − ψⁿ)/√5,  φ = (1+√5)/2,  ψ = (1−√5)/2',
      closedAt: function (n) { var s = Math.sqrt(5); return Math.round((Math.pow((1 + s) / 2, n) - Math.pow((1 - s) / 2, n)) / s); },
      note: 'The characteristic equation r² = r + 1 has irrational roots, so the closed form contains √5 — yet every term it produces is an integer. Rounding is used here only because the roots are irrational; the iteration on the left is exact.'
    },
    hanoi: {
      label: 'aₙ = 2aₙ₋₁ + 1', init: [0n],
      next: function (a, n) { return 2n * a[n - 1] + 1n; },
      closed: 'aₙ = 2ⁿ − 1',
      closedAt: function (n) { return Number(2n ** BigInt(n) - 1n); },
      exact: function (n) { return 2n ** BigInt(n) - 1n; },
      note: 'Nonhomogeneous: the +1 forces a particular solution. Guess a constant A, substitute, get A = 2A + 1 so A = −1; add the homogeneous C·2ⁿ and fit a₀ = 0.'
    },
    geo: {
      label: 'aₙ = 2aₙ₋₁', init: [1n],
      next: function (a, n) { return 2n * a[n - 1]; },
      closed: 'aₙ = 2ⁿ',
      closedAt: function (n) { return Number(2n ** BigInt(n)); },
      exact: function (n) { return 2n ** BigInt(n); },
      note: 'One root, r = 2. Every first-order homogeneous recurrence is a geometric sequence, which is why exponential growth is the default shape in this subject.'
    },
    two: {
      label: 'aₙ = 5aₙ₋₁ − 6aₙ₋₂', init: [1n, 5n],
      next: function (a, n) { return 5n * a[n - 1] - 6n * a[n - 2]; },
      closed: 'r² − 5r + 6 = 0 → r = 2, 3;  aₙ = A·2ⁿ + B·3ⁿ with A = −2, B = 3',
      closedAt: function (n) { return Number(-2n * 2n ** BigInt(n) + 3n * 3n ** BigInt(n)); },
      exact: function (n) { return -2n * (2n ** BigInt(n)) + 3n * (3n ** BigInt(n)); },
      note: 'Distinct real roots: the general solution is a combination of the two geometric sequences, and the initial conditions pick out which combination.'
    },
    rep: {
      label: 'aₙ = 4aₙ₋₁ − 4aₙ₋₂', init: [1n, 4n],
      next: function (a, n) { return 4n * a[n - 1] - 4n * a[n - 2]; },
      closed: 'r² − 4r + 4 = 0 → r = 2 twice;  aₙ = (A + Bn)·2ⁿ with A = 1, B = 1',
      closedAt: function (n) { return Number((1n + BigInt(n)) * 2n ** BigInt(n)); },
      exact: function (n) { return (1n + BigInt(n)) * (2n ** BigInt(n)); },
      note: 'A repeated root needs the extra n factor. Without it there is only one free constant and two initial conditions to satisfy, which is generally impossible.'
    },
    lin: {
      label: 'aₙ = aₙ₋₁ + n', init: [0n],
      next: function (a, n) { return a[n - 1] + BigInt(n); },
      closed: 'aₙ = n(n+1)/2',
      closedAt: function (n) { return n * (n + 1) / 2; },
      exact: function (n) { return BigInt(n) * BigInt(n + 1) / 2n; },
      note: 'Nonhomogeneous with a linear f(n) = n, so the particular solution is quadratic. Unrolling gives the triangular numbers, which course 3 also proves by induction.'
    },
    merge: {
      label: 'T(n) = 2T(n/2) + n, T(1) = 0, at n = 2ᵏ', init: [0n],
      next: function (a, n) { return 2n * a[n - 1] + 2n ** BigInt(n); },
      closed: 'T(2ᵏ) = k·2ᵏ, i.e. T(n) = n log₂ n',
      closedAt: function (n) { return n * Math.pow(2, n); },
      exact: function (n) { return BigInt(n) * (2n ** BigInt(n)); },
      indexLabel: 'k',
      note: 'Indexed by k with n = 2ᵏ, the divide-and-conquer recurrence becomes an ordinary linear one. That substitution is the whole trick behind the master theorem.'
    }
  };

  function redraw() {
    var rec = RECS[presetSel.value], count = +termsS.value;
    document.getElementById('recTermsOut').textContent = count;
    var a = rec.init.slice();
    for (var n = a.length; n <= count; n += 1) a.push(rec.next(a, n));

    var rows = '', mismatch = null;
    for (var i = 0; i <= count; i += 1) {
      var closed = rec.exact ? rec.exact(i) : BigInt(rec.closedAt(i));
      var same = closed === a[i];
      if (!same && mismatch === null) mismatch = i;
      rows += '<tr' + (same ? '' : ' class="focus"') + '><td>' + i + '</td><td>' + a[i].toString()
        + '</td><td>' + closed.toString() + '</td><td class="' + (same ? 't' : 'f') + '">'
        + (same ? '=' : '≠') + '</td></tr>';
    }
    table.innerHTML = '<thead><tr><th>' + (rec.indexLabel || 'n') + '</th><th>iterated</th><th>closed form</th><th></th></tr></thead><tbody>'
      + rows + '</tbody>';
    closedOut.textContent = rec.closed;

    /* Bars, scaled to the largest term so the shape of the growth is visible
       even when the values span several orders of magnitude. */
    var maxV = a.reduce(function (m, v) { return v > m ? v : m; }, 1n);
    var w = 520 / (count + 1), s = '';
    for (var j = 0; j <= count; j += 1) {
      var h = Number(a[j] * 160n / (maxV || 1n));
      if (h < 0) h = 0;
      s += '<rect x="' + (j * w + 2) + '" y="' + (180 - h) + '" width="' + (w - 4) + '" height="' + h
        + '" rx="2" fill="var(--cyan)" opacity="0.8" />';
    }
    s += '<line x1="0" y1="180" x2="520" y2="180" stroke="var(--line-strong)" stroke-width="1" />';
    plot.innerHTML = s;
    caption.textContent = rec.label;

    if (mismatch === null) {
      status.innerHTML = '<strong>The iteration and the closed form agree on all ' + (count + 1)
        + ' terms.</strong> ' + rec.note;
    } else {
      status.innerHTML = '<span class="tone-red">They disagree first at ' + (rec.indexLabel || 'n')
        + ' = ' + mismatch + '.</span> ' + rec.note;
    }
  }

  presetSel.addEventListener('change', redraw);
  termsS.addEventListener('input', redraw);
  presetSel.value = """ + '"%s"' % cfg.get("preset", "fib") + r""";
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Recurrence and closed form",
        subtitle="Iterated and solved, then compared",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a recurrence"),
        panel_intro=cfg.get(
            "panel_intro",
            "The left column unrolls the recurrence; the right evaluates the closed "
            "form. They are computed separately so their agreement is evidence.",
        ),
        script=script,
    )
