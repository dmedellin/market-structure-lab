"""Labs for course 4: counting."""

from .common import Lab, cfg_literal

BIGINT_JS = r"""
  /* Counting is done in BigInt. 21! already exceeds what a double can hold
     exactly, so a lab that used ordinary numbers would start printing
     confidently wrong totals somewhere around n = 21 with nothing to mark the
     boundary. Every count below is exact for every n the controls allow. */
  function fact(n) { var r = 1n; for (var i = 2n; i <= BigInt(n); i += 1n) r *= i; return r; }
  function perm(n, r) {
    if (r > n || r < 0) return 0n;
    var out = 1n;
    for (var i = 0; i < r; i += 1) out *= BigInt(n - i);
    return out;
  }
  function comb(n, r) {
    if (r < 0 || r > n) return 0n;
    r = Math.min(r, n - r);
    var num = 1n, den = 1n;
    for (var i = 0; i < r; i += 1) { num *= BigInt(n - i); den *= BigInt(i + 1); }
    return num / den;
  }
  function group(x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
"""


def counting_lab(cfg):
    """The four counting rules on one screen, with the small cases enumerated.

    The reason the four are confusable is that the FORMULAS look alike. The
    reason they stop being confusable is seeing the actual selections listed:
    with n = 3 and r = 2 the four answers are 9, 6, 6 and 3, and the lists show
    why. So the lab enumerates whenever the total is small enough to read, and
    says plainly when it has stopped.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>Choosing r from n</strong><span>Order matters or not; repetition allowed or not</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>selected rule</span></div>
      </div>
      <div class="lab-stage">
        <div class="table-wrap"><table class="tt" id="cntTable"></table></div>
        <div id="cntList" class="small-copy" style="margin-top:10px;"></div>
      </div>"""
    controls = """        <div>
          <div class="range-row"><label class="small-copy" for="cntN">n (things to choose from)</label><span class="range-value" id="cntNOut">5</span></div>
          <input id="cntN" type="range" min="1" max="24" value="5" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="cntR">r (things chosen)</label><span class="range-value" id="cntROut">3</span></div>
          <input id="cntR" type="range" min="0" max="12" value="3" />
        </div>
        <div class="field">
          <label for="cntRule">Highlight and enumerate</label>
          <select id="cntRule">
            <option value="pr">Ordered, repetition allowed &mdash; n<sup>r</sup></option>
            <option value="p">Ordered, no repetition &mdash; P(n, r)</option>
            <option value="c" selected="selected">Unordered, no repetition &mdash; C(n, r)</option>
            <option value="cr">Unordered, repetition allowed &mdash; C(n+r-1, r)</option>
          </select>
        </div>
        <div class="status-banner" id="cntStatus">Every total is computed in exact integer arithmetic.</div>"""

    script = BIGINT_JS + r"""
  var nS = document.getElementById('cntN'), rS = document.getElementById('cntR');
  var ruleSel = document.getElementById('cntRule');
  var table = document.getElementById('cntTable'), list = document.getElementById('cntList');
  var status = document.getElementById('cntStatus');
  var LETTERS = 'abcdefghijklmnopqrstuvwx';

  function enumerate(kind, n, r) {
    var out = [];
    function ordered(prefix, repeat) {
      if (prefix.length === r) { out.push(prefix.join('')); return; }
      if (out.length > 400) return;
      for (var i = 0; i < n; i += 1) {
        if (!repeat && prefix.indexOf(LETTERS[i]) !== -1) continue;
        ordered(prefix.concat([LETTERS[i]]), repeat);
      }
    }
    function unordered(start, prefix, repeat) {
      if (prefix.length === r) { out.push(prefix.join('')); return; }
      if (out.length > 400) return;
      for (var i = start; i < n; i += 1) {
        unordered(repeat ? i : i + 1, prefix.concat([LETTERS[i]]), repeat);
      }
    }
    if (kind === 'pr') ordered([], true);
    else if (kind === 'p') ordered([], false);
    else if (kind === 'c') unordered(0, [], false);
    else unordered(0, [], true);
    return out;
  }

  function redraw() {
    var n = +nS.value, r = +rS.value;
    document.getElementById('cntNOut').textContent = n;
    document.getElementById('cntROut').textContent = r;
    var vals = {
      pr: BigInt(n) ** BigInt(r),
      p: perm(n, r),
      c: comb(n, r),
      cr: comb(n + r - 1, r)
    };
    var rows = [
      ['pr', 'ordered, repetition allowed', 'n<sup>r</sup> = ' + n + '<sup>' + r + '</sup>', vals.pr],
      ['p', 'ordered, no repetition', 'P(' + n + ', ' + r + ') = ' + n + '!/(' + n + '−' + r + ')!', vals.p],
      ['c', 'unordered, no repetition', 'C(' + n + ', ' + r + ')', vals.c],
      ['cr', 'unordered, repetition allowed', 'C(' + (n + r - 1) + ', ' + r + ')', vals.cr]
    ];
    var kind = ruleSel.value;
    var h = '<thead><tr><th>rule</th><th>counts</th><th>formula</th><th>value</th></tr></thead><tbody>';
    rows.forEach(function (row) {
      h += '<tr' + (row[0] === kind ? ' class="focus"' : '') + '><td>' + row[0].toUpperCase()
        + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + group(row[3]) + '</td></tr>';
    });
    table.innerHTML = h + '</tbody></table>';

    var total = vals[kind];
    if (total <= 400n && r <= 8 && n <= 20) {
      var items = enumerate(kind, n, r);
      list.innerHTML = '<strong>All ' + items.length + ':</strong> '
        + items.map(function (s) { return '<span class="chip">' + (s || '∅') + '</span>'; }).join('');
      if (BigInt(items.length) !== total) {
        list.innerHTML += '<br /><span class="tone-red">enumeration and formula disagree</span>';
      } else {
        status.innerHTML = 'The formula says <strong>' + group(total) + '</strong> and the enumeration '
          + 'produced <strong>' + items.length + '</strong> selections. They agree, which is the only '
          + 'reason to trust the formula on the values too large to list.';
      }
    } else {
      list.innerHTML = '<span class="tone-muted">Too many to list (' + group(total)
        + ' selections). The count is still exact &mdash; it is computed in big-integer arithmetic, '
        + 'not as a floating-point approximation.</span>';
      status.innerHTML = 'At n = ' + n + ', r = ' + r + ' the four rules differ by factors of '
        + 'thousands. Choosing the wrong one is not a small error.';
    }
  }

  [nS, rS, ruleSel].forEach(function (el) { el.addEventListener('input', redraw); });
  ruleSel.addEventListener('change', redraw);
  nS.value = """ + str(cfg.get("n", 5)) + r"""; rS.value = """ + str(cfg.get("r", 3)) + r""";
  ruleSel.value = """ + '"%s"' % cfg.get("rule", "c") + r""";
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="The four counting rules",
        subtitle="Enumerated while enumeration is possible",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Set n and r"),
        panel_intro=cfg.get(
            "panel_intro",
            "All four totals are shown at once, because the mistake is never "
            "arithmetic: it is picking the wrong one of the four.",
        ),
        script=script,
    )


def pascal_lab(cfg):
    """Pascal's triangle, with the identity you select highlighted in it.

    Every identity here is CHECKED as it is highlighted -- the lab sums the
    cells it has highlighted and compares that to the cell the identity claims
    they equal. An identity that failed would show a mismatch rather than a
    tidy picture.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>Pascal's triangle</strong><span>Row n, entry k is C(n, k)</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>the identity's terms</span><span class="tone-amber"><i class="legend-swatch"></i>the value they equal</span></div>
      </div>
      <div class="lab-stage"><div id="pasOut" style="text-align:center;font-family:var(--mono);font-size:0.8rem;line-height:2;"></div></div>
      <div class="status-banner" id="pasCheck" style="margin-top:12px;"></div>"""
    controls = """        <div>
          <div class="range-row"><label class="small-copy" for="pasRows">Rows shown</label><span class="range-value" id="pasRowsOut">10</span></div>
          <input id="pasRows" type="range" min="4" max="16" value="10" />
        </div>
        <div class="field">
          <label for="pasId">Identity to highlight</label>
          <select id="pasId">
            <option value="rule">Pascal's rule: C(n,k) = C(n−1,k−1) + C(n−1,k)</option>
            <option value="sym">Symmetry: C(n,k) = C(n,n−k)</option>
            <option value="row">Row sum: &Sigma;<sub>k</sub> C(n,k) = 2<sup>n</sup></option>
            <option value="alt">Alternating sum: &Sigma;<sub>k</sub> (−1)<sup>k</sup> C(n,k) = 0</option>
            <option value="hockey">Hockey stick: &Sigma;<sub>i≤n</sub> C(i,k) = C(n+1,k+1)</option>
          </select>
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="pasN">n</label><span class="range-value" id="pasNOut">6</span></div>
          <input id="pasN" type="range" min="1" max="16" value="6" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="pasK">k</label><span class="range-value" id="pasKOut">2</span></div>
          <input id="pasK" type="range" min="0" max="16" value="2" />
        </div>
        <div class="field">
          <label>Binomial expansion of (x + y)<sup>n</sup></label>
          <div id="pasExpand" class="mathblock" style="font-size:0.82rem;"></div>
        </div>"""

    script = BIGINT_JS + r"""
  var rowsS = document.getElementById('pasRows'), nS = document.getElementById('pasN'), kS = document.getElementById('pasK');
  var idSel = document.getElementById('pasId');
  var out = document.getElementById('pasOut'), check = document.getElementById('pasCheck');
  var expand = document.getElementById('pasExpand');

  function redraw() {
    var rows = +rowsS.value, n = Math.min(+nS.value, rows), k = +kS.value;
    document.getElementById('pasRowsOut').textContent = rows;
    document.getElementById('pasNOut').textContent = n;
    document.getElementById('pasKOut').textContent = k;
    var mode = idSel.value;

    /* Which cells the identity involves, and which cell it claims they equal.
       Both are derived from the identity, then CHECKED against the triangle. */
    var terms = [], target = null, claim = '', lhs = 0n, rhs = 0n;
    if (mode === 'rule') {
      if (k >= 1 && k <= n && n >= 1) {
        terms = [[n - 1, k - 1], [n - 1, k]];
        target = [n, k];
        lhs = comb(n - 1, k - 1) + comb(n - 1, k);
        rhs = comb(n, k);
        claim = 'C(' + (n - 1) + ',' + (k - 1) + ') + C(' + (n - 1) + ',' + k + ') = C(' + n + ',' + k + ')';
      } else { claim = 'Pascal\'s rule needs 1 ≤ k ≤ n.'; }
    } else if (mode === 'sym') {
      terms = [[n, k]]; target = [n, n - k];
      lhs = comb(n, k); rhs = comb(n, n - k);
      claim = 'C(' + n + ',' + k + ') = C(' + n + ',' + (n - k) + ')';
    } else if (mode === 'row') {
      for (var j = 0; j <= n; j += 1) { terms.push([n, j]); lhs += comb(n, j); }
      rhs = 2n ** BigInt(n);
      claim = 'the sum of row ' + n + ' = 2^' + n;
    } else if (mode === 'alt') {
      for (var j2 = 0; j2 <= n; j2 += 1) { terms.push([n, j2]); lhs += (j2 % 2 ? -1n : 1n) * comb(n, j2); }
      rhs = 0n;
      claim = 'the alternating sum of row ' + n + ' = 0' + (n === 0 ? ' (row 0 is the exception: it is 1)' : '');
      if (n === 0) rhs = 1n;
    } else {
      for (var i = k; i <= n; i += 1) { terms.push([i, k]); lhs += comb(i, k); }
      target = [n + 1, k + 1];
      rhs = comb(n + 1, k + 1);
      claim = 'C(' + k + ',' + k + ') + … + C(' + n + ',' + k + ') = C(' + (n + 1) + ',' + (k + 1) + ')';
    }

    function isTerm(r, c) { return terms.some(function (t) { return t[0] === r && t[1] === c; }); }
    function isTarget(r, c) { return target && target[0] === r && target[1] === c; }

    var html = '';
    for (var r2 = 0; r2 <= rows; r2 += 1) {
      var line = '';
      for (var c = 0; c <= r2; c += 1) {
        var v = comb(r2, c).toString();
        var cls = isTarget(r2, c) ? 'tone-amber' : isTerm(r2, c) ? 'tone-cyan' : 'tone-muted';
        var weight = (isTerm(r2, c) || isTarget(r2, c)) ? 'font-weight:800;' : '';
        line += '<span class="' + cls + '" style="display:inline-block;min-width:3.4em;' + weight + '">' + v + '</span>';
      }
      html += '<div>' + line + '</div>';
    }
    out.innerHTML = html;

    if (terms.length) {
      var ok = lhs === rhs;
      check.innerHTML = '<strong>' + claim + '</strong><br />'
        + 'highlighted terms sum to <strong>' + group(lhs) + '</strong>; the identity claims <strong>'
        + group(rhs) + '</strong> &mdash; ' + (ok
          ? 'they match, and they match at every n and k you can set here.'
          : '<span class="tone-red">they do not match.</span>');
    } else {
      check.innerHTML = claim;
    }

    var parts = [];
    for (var t = 0; t <= n; t += 1) {
      var coef = comb(n, t).toString();
      var xp = n - t, yp = t;
      var term = (coef === '1' ? '' : coef)
        + (xp ? 'x' + (xp > 1 ? '^' + xp : '') : '')
        + (yp ? 'y' + (yp > 1 ? '^' + yp : '') : '');
      parts.push(term || '1');
    }
    expand.textContent = '(x + y)^' + n + ' = ' + parts.join(' + ');
  }

  [rowsS, nS, kS].forEach(function (el) { el.addEventListener('input', redraw); });
  idSel.addEventListener('change', redraw);
  idSel.value = """ + '"%s"' % cfg.get("identity", "rule") + r""";
  nS.value = """ + str(cfg.get("n", 6)) + r"""; kS.value = """ + str(cfg.get("k", 2)) + r""";
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Pascal's triangle",
        subtitle="Identities highlighted and checked",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Pick an identity"),
        panel_intro=cfg.get(
            "panel_intro",
            "Each identity highlights the cells it involves and then adds them up, "
            "so the picture and the arithmetic are shown together.",
        ),
        script=script,
    )


def inclusion_exclusion(cfg):
    """Inclusion-exclusion built from the actual multiples, term by term.

    The classic "how many of 1..N are divisible by a, b or c" is the right
    vehicle because both sides are checkable: the lab counts by brute force AND
    by the formula, and shows the two agreeing. If a reader drops a term -- the
    universal mistake -- the running total on the left visibly misses.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>How many integers in 1 … N are divisible by a, b or c?</strong><span>Counted two ways</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>added</span><span class="tone-red"><i class="legend-swatch"></i>subtracted</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap"><table class="tt" id="ieTable"></table></div></div>
      <div class="status-banner" id="ieStatus" style="margin-top:12px;"></div>"""
    controls = """        <div>
          <div class="range-row"><label class="small-copy" for="ieN">N</label><span class="range-value" id="ieNOut">100</span></div>
          <input id="ieN" type="range" min="10" max="500" step="10" value="100" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="ieA">a</label><span class="range-value" id="ieAOut">2</span></div>
          <input id="ieA" type="range" min="2" max="12" value="2" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="ieB">b</label><span class="range-value" id="ieBOut">3</span></div>
          <input id="ieB" type="range" min="2" max="12" value="3" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="ieC">c</label><span class="range-value" id="ieCOut">5</span></div>
          <input id="ieC" type="range" min="2" max="12" value="5" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>By formula</span><strong id="ieFormula">&mdash;</strong></div>
          <div class="kpi"><span>By counting</span><strong id="ieBrute">&mdash;</strong></div>
        </div>"""

    script = r"""
  var nS = document.getElementById('ieN'), aS = document.getElementById('ieA');
  var bS = document.getElementById('ieB'), cS = document.getElementById('ieC');
  var table = document.getElementById('ieTable'), status = document.getElementById('ieStatus');

  function lcm(x, y) { var a = x, b = y; while (b) { var t = a % b; a = b; b = t; } return x / a * y; }

  function redraw() {
    var N = +nS.value, a = +aS.value, b = +bS.value, c = +cS.value;
    document.getElementById('ieNOut').textContent = N;
    document.getElementById('ieAOut').textContent = a;
    document.getElementById('ieBOut').textContent = b;
    document.getElementById('ieCOut').textContent = c;

    var terms = [
      ['|A| = ⌊N/' + a + '⌋', Math.floor(N / a), 1],
      ['|B| = ⌊N/' + b + '⌋', Math.floor(N / b), 1],
      ['|C| = ⌊N/' + c + '⌋', Math.floor(N / c), 1],
      ['|A∩B| = ⌊N/lcm(' + a + ',' + b + ')⌋', Math.floor(N / lcm(a, b)), -1],
      ['|A∩C| = ⌊N/lcm(' + a + ',' + c + ')⌋', Math.floor(N / lcm(a, c)), -1],
      ['|B∩C| = ⌊N/lcm(' + b + ',' + c + ')⌋', Math.floor(N / lcm(b, c)), -1],
      ['|A∩B∩C| = ⌊N/lcm(' + a + ',' + b + ',' + c + ')⌋', Math.floor(N / lcm(lcm(a, b), c)), 1]
    ];

    var running = 0;
    var h = '<thead><tr><th>term</th><th>sign</th><th>value</th><th>running total</th></tr></thead><tbody>';
    terms.forEach(function (t) {
      running += t[2] * t[1];
      h += '<tr><td>' + t[0] + '</td><td class="' + (t[2] > 0 ? 't' : 'f') + '">'
        + (t[2] > 0 ? '+' : '−') + '</td><td>' + t[1] + '</td><td>' + running + '</td></tr>';
    });
    table.innerHTML = h + '</tbody></table>';

    /* The same count by brute force. Two independent routes to one number is
       the whole reason to believe either of them. */
    var brute = 0;
    for (var i = 1; i <= N; i += 1) if (i % a === 0 || i % b === 0 || i % c === 0) brute += 1;

    document.getElementById('ieFormula').textContent = running;
    document.getElementById('ieBrute').textContent = brute;
    var naive = terms[0][1] + terms[1][1] + terms[2][1];
    if (running === brute) {
      status.innerHTML = 'Both routes give <strong>' + brute + '</strong>. Adding the three sizes alone gives '
        + '<strong>' + naive + '</strong> &mdash; too big by ' + (naive - brute) + ', because every number divisible '
        + 'by two of them was counted twice and every number divisible by all three was counted three times. '
        + 'That over-count is exactly what the alternating terms remove.';
    } else {
      status.innerHTML = '<span class="tone-red">The two routes disagree (' + running + ' vs ' + brute + ').</span>';
    }
  }

  [nS, aS, bS, cS].forEach(function (el) { el.addEventListener('input', redraw); });
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Inclusion and exclusion",
        subtitle="Formula and brute force, side by side",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Set the divisors"),
        panel_intro=cfg.get(
            "panel_intro",
            "The right-hand count walks 1 to N one integer at a time. It exists to "
            "check the formula, not to replace it.",
        ),
        script=script,
    )
