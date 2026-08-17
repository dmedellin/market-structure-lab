"""Lab for course 8: algorithms and complexity."""

from .common import Lab, cfg_literal


def algorithm_lab(cfg):
    """Counts from running the algorithm, not from quoting its complexity class.

    Every operation count in this lab is produced by executing the algorithm on
    an actual array and incrementing a counter. That is the difference between
    "merge sort is O(n log n)" as a fact to repeat and as a claim you have
    watched hold: the measured column and the predicted column sit beside each
    other, and where they diverge the lab says why.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong id="alTitle">Algorithms and growth</strong><span id="alSub"></span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>measured</span><span class="tone-purple"><i class="legend-swatch"></i>predicted</span><span class="tone-amber"><i class="legend-swatch"></i>crossover</span></div>
      </div>
      <div class="lab-stage"><svg id="alPlot" viewBox="0 0 520 230" role="img" aria-label="Operation counts plotted against input size."></svg></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="alTable"></table></div>
      <div class="status-banner" id="alStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="alMode">What to examine</label>
          <select id="alMode">
            <option value="growth">Growth rates side by side</option>
            <option value="witness">Is f(n) = O(g(n))? find C and k</option>
            <option value="search">Linear vs binary search (counted)</option>
            <option value="sort">Sorting algorithms (counted)</option>
            <option value="master">Master theorem cases</option>
            <option value="greedy">Greedy vs dynamic programming</option>
          </select>
        </div>
        <div class="field" id="alFWrap">
          <label for="alF">f(n)</label>
          <select id="alF"></select>
        </div>
        <div class="field" id="alGWrap">
          <label for="alG">g(n)</label>
          <select id="alG"></select>
        </div>
        <div id="alNWrap">
          <div class="range-row"><label class="small-copy" for="alN">n</label><span class="range-value" id="alNOut">16</span></div>
          <input id="alN" type="range" min="2" max="64" value="16" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span id="alK1L">measured</span><strong id="alK1">&mdash;</strong></div>
          <div class="kpi"><span id="alK2L">predicted</span><strong id="alK2">&mdash;</strong></div>
        </div>"""

    script = r"""
  var modeSel = document.getElementById('alMode'), fSel = document.getElementById('alF'), gSel = document.getElementById('alG');
  var nS = document.getElementById('alN');
  var plot = document.getElementById('alPlot'), table = document.getElementById('alTable');
  var status = document.getElementById('alStatus');
  var title = document.getElementById('alTitle'), sub = document.getElementById('alSub');
  var k1 = document.getElementById('alK1'), k2 = document.getElementById('alK2');
  var k1L = document.getElementById('alK1L'), k2L = document.getElementById('alK2L');

  var FUNCS = [
    ['1', function (n) { return 1; }],
    ['log₂ n', function (n) { return Math.log2(n); }],
    ['n', function (n) { return n; }],
    ['n log₂ n', function (n) { return n * Math.log2(n); }],
    ['n²', function (n) { return n * n; }],
    ['n³', function (n) { return n * n * n; }],
    ['2ⁿ', function (n) { return Math.pow(2, n); }],
    ['n!', function (n) { var f = 1; for (var i = 2; i <= n; i += 1) f *= i; return f; }],
    ['3n² + 5n + 100', function (n) { return 3 * n * n + 5 * n + 100; }],
    ['100n', function (n) { return 100 * n; }]
  ];
  FUNCS.forEach(function (f, i) {
    [fSel, gSel].forEach(function (sel) {
      var o = document.createElement('option');
      o.value = String(i); o.textContent = f[0];
      sel.appendChild(o);
    });
  });
  fSel.value = '8'; gSel.value = '4';

  function show(ids) {
    ['alFWrap', 'alGWrap', 'alNWrap'].forEach(function (id) {
      document.getElementById(id).hidden = ids.indexOf(id) === -1;
    });
  }

  function drawSeries(series, xs, logScale) {
    var maxY = 0;
    series.forEach(function (s) { s.values.forEach(function (v) { if (isFinite(v) && v > maxY) maxY = v; }); });
    if (maxY <= 0) maxY = 1;
    function y(v) {
      if (!isFinite(v)) return 6;
      if (logScale) {
        var lv = Math.log10(Math.max(v, 1)), lm = Math.log10(Math.max(maxY, 10));
        return 200 - (lv / lm) * 180;
      }
      return 200 - (v / maxY) * 180;
    }
    function x(i) { return 26 + (i / Math.max(1, xs.length - 1)) * 470; }
    var s = '<line x1="26" y1="200" x2="500" y2="200" stroke="var(--line-strong)" />'
      + '<line x1="26" y1="14" x2="26" y2="200" stroke="var(--line-strong)" />';
    series.forEach(function (ser) {
      var d = ser.values.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(' ');
      s += '<path d="' + d + '" fill="none" stroke="' + ser.colour + '" stroke-width="2.4" opacity="0.9" />';
      s += '<text x="' + (x(ser.values.length - 1) - 6) + '" y="' + Math.max(14, y(ser.values[ser.values.length - 1]) - 6)
        + '" text-anchor="end" font-size="11" font-weight="700" fill="' + ser.colour + '">' + ser.label + '</text>';
    });
    s += '<text x="26" y="216" font-size="10" fill="var(--muted)">n = ' + xs[0] + '</text>';
    s += '<text x="500" y="216" text-anchor="end" font-size="10" fill="var(--muted)">n = ' + xs[xs.length - 1] + '</text>';
    if (logScale) s += '<text x="30" y="24" font-size="10" fill="var(--muted)">log scale</text>';
    plot.innerHTML = s;
  }

  /* --- counted algorithms. Each RUNS and increments a counter. ----------- */
  function makeArray(n, kind) {
    var a = [];
    for (var i = 0; i < n; i += 1) a.push(i + 1);
    if (kind === 'reverse') a.reverse();
    else if (kind === 'shuffle') {
      /* A fixed permutation, generated by a deterministic step so two readers
         at the same n see the same array and the same counts. */
      var out = [];
      var idx = 0;
      while (a.length) { idx = (idx + 7) % a.length; out.push(a.splice(idx, 1)[0]); }
      a = out;
    }
    return a;
  }

  function linearSearch(a, target) {
    var c = 0;
    for (var i = 0; i < a.length; i += 1) { c += 1; if (a[i] === target) return c; }
    return c;
  }
  function binarySearch(a, target) {
    var lo = 0, hi = a.length - 1, c = 0;
    while (lo <= hi) {
      c += 1;
      var mid = (lo + hi) >> 1;
      if (a[mid] === target) return c;
      if (a[mid] < target) lo = mid + 1; else hi = mid - 1;
    }
    return c;
  }
  function bubbleSort(a) {
    var arr = a.slice(), c = 0;
    for (var i = 0; i < arr.length; i += 1)
      for (var j = 0; j + 1 < arr.length - i; j += 1) {
        c += 1;
        if (arr[j] > arr[j + 1]) { var t = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = t; }
      }
    return c;
  }
  function insertionSort(a) {
    var arr = a.slice(), c = 0;
    for (var i = 1; i < arr.length; i += 1) {
      var key = arr[i], j = i - 1;
      while (j >= 0) { c += 1; if (arr[j] <= key) break; arr[j + 1] = arr[j]; j -= 1; }
      arr[j + 1] = key;
    }
    return c;
  }
  function mergeSort(a) {
    var c = 0;
    function sort(arr) {
      if (arr.length <= 1) return arr;
      var mid = arr.length >> 1;
      var L = sort(arr.slice(0, mid)), R = sort(arr.slice(mid)), out = [], i = 0, j = 0;
      while (i < L.length && j < R.length) { c += 1; out.push(L[i] <= R[j] ? L[i++] : R[j++]); }
      while (i < L.length) out.push(L[i++]);
      while (j < R.length) out.push(R[j++]);
      return out;
    }
    sort(a.slice());
    return c;
  }

  /* Coin change: greedy and exact DP, run against each other. */
  function greedyCoins(coins, amount) {
    var left = amount, used = 0, picks = [];
    var sorted = coins.slice().sort(function (x, y) { return y - x; });
    sorted.forEach(function (c) {
      while (left >= c) { left -= c; used += 1; picks.push(c); }
    });
    return left === 0 ? { count: used, picks: picks } : { count: Infinity, picks: [] };
  }
  function dpCoins(coins, amount) {
    var best = new Array(amount + 1).fill(Infinity), from = new Array(amount + 1).fill(-1);
    best[0] = 0;
    for (var v = 1; v <= amount; v += 1) {
      coins.forEach(function (c) {
        if (c <= v && best[v - c] + 1 < best[v]) { best[v] = best[v - c] + 1; from[v] = c; }
      });
    }
    var picks = [], cur = amount;
    while (cur > 0 && from[cur] !== -1) { picks.push(from[cur]); cur -= from[cur]; }
    return { count: best[amount], picks: picks, table: best };
  }

  var MODES = {
    growth: function () {
      show(['alNWrap']);
      title.textContent = 'Growth rates';
      sub.textContent = 'the same axes, log scale';
      var N = +nS.value, xs = [], series = [];
      for (var n = 1; n <= N; n += 1) xs.push(n);
      var picks = [[1, 'var(--green)'], [2, 'var(--cyan)'], [3, 'var(--blue)'], [4, 'var(--purple)'], [6, 'var(--red)']];
      picks.forEach(function (p) {
        series.push({ label: FUNCS[p[0]][0], colour: p[1], values: xs.map(function (n) { return FUNCS[p[0]][1](n); }) });
      });
      drawSeries(series, xs, true);
      var rows = '';
      [4, 8, 16, 32, 64].filter(function (n) { return n <= N; }).forEach(function (n) {
        rows += '<tr><td>' + n + '</td>' + picks.map(function (p) {
          var v = FUNCS[p[0]][1](n);
          return '<td>' + (v > 1e15 ? v.toExponential(2) : Math.round(v).toLocaleString('en-US')) + '</td>';
        }).join('') + '</tr>';
      });
      table.innerHTML = '<thead><tr><th>n</th>' + picks.map(function (p) { return '<th>' + FUNCS[p[0]][0] + '</th>'; }).join('')
        + '</tr></thead><tbody>' + rows + '</tbody>';
      k1L.textContent = 'n'; k1.textContent = N;
      k2L.textContent = '2ⁿ at n'; k2.textContent = Math.pow(2, N) > 1e15 ? Math.pow(2, N).toExponential(2) : Math.pow(2, N).toLocaleString('en-US');
      status.innerHTML = 'The vertical axis is logarithmic, so a straight line is exponential growth. '
        + 'At n = 64, n² is ' + (64 * 64).toLocaleString('en-US') + ' and 2ⁿ is about 1.8 × 10¹⁹ — the gap between '
        + 'polynomial and exponential is not a matter of constants, and no faster machine closes it.';
    },
    witness: function () {
      show(['alFWrap', 'alGWrap', 'alNWrap']);
      title.textContent = 'Big-O by witness';
      sub.textContent = 'f(n) ≤ C·g(n) for all n ≥ k';
      var f = FUNCS[+fSel.value], g = FUNCS[+gSel.value], N = Math.max(8, +nS.value);
      /* Search a small grid of C and k for a pair that works on 1..4N. The
         search is honest: if no pair in the grid works, the lab says the
         relation looks false rather than inventing a constant. */
      var found = null;
      var Cs = [1, 2, 3, 4, 5, 10, 20, 50, 100, 1000];
      for (var ci = 0; ci < Cs.length && !found; ci += 1) {
        for (var k = 1; k <= 40 && !found; k += 1) {
          var ok = true;
          for (var n = k; n <= 4 * N; n += 1) {
            if (f[1](n) > Cs[ci] * g[1](n) + 1e-9) { ok = false; break; }
          }
          if (ok) found = { C: Cs[ci], k: k };
        }
      }
      var xs = [], series = [];
      for (var n2 = 1; n2 <= N; n2 += 1) xs.push(n2);
      series.push({ label: f[0], colour: 'var(--cyan)', values: xs.map(f[1]) });
      series.push({ label: (found ? found.C + '·' : '') + g[0], colour: 'var(--purple)', values: xs.map(function (n) { return (found ? found.C : 1) * g[1](n); }) });
      drawSeries(series, xs, true);
      var rows = '';
      xs.filter(function (n) { return n <= 12 || n % 4 === 0; }).forEach(function (n) {
        var fv = f[1](n), gv = (found ? found.C : 1) * g[1](n);
        rows += '<tr' + (fv <= gv ? '' : ' class="focus"') + '><td>' + n + '</td><td>' + fv.toFixed(2) + '</td><td>'
          + gv.toFixed(2) + '</td><td class="' + (fv <= gv ? 't' : 'f') + '">' + (fv <= gv ? '≤' : '>') + '</td></tr>';
      });
      table.innerHTML = '<thead><tr><th>n</th><th>' + f[0] + '</th><th>' + (found ? found.C + '·' : '') + g[0]
        + '</th><th></th></tr></thead><tbody>' + rows + '</tbody>';
      k1L.textContent = 'C'; k1.textContent = found ? found.C : '—';
      k2L.textContent = 'k'; k2.textContent = found ? found.k : '—';
      status.innerHTML = found
        ? '<strong>' + f[0] + ' = O(' + g[0] + ')</strong>, witnessed by C = ' + found.C + ' and k = ' + found.k
          + ': for every n ≥ ' + found.k + ', f(n) ≤ ' + found.C + '·g(n). Big-O is an existence claim about such a '
          + 'pair, and producing one is the whole proof. Note that the first few n may violate it — that is what k is for.'
        : '<strong>No constant works.</strong> The search tried C up to 1000 and k up to 40 and found no pair holding '
          + 'through n = ' + (4 * N) + '. That is strong evidence ' + f[0] + ' is NOT O(' + g[0] + ') — a bigger '
          + 'constant cannot rescue a faster-growing function, because the ratio itself diverges.';
    },
    search: function () {
      show(['alNWrap']);
      title.textContent = 'Linear versus binary search';
      sub.textContent = 'worst-case comparisons, counted by running both';
      var N = +nS.value, xs = [], lin = [], bin = [];
      for (var n = 2; n <= Math.max(8, N); n += 1) {
        var a = makeArray(n, 'sorted');
        xs.push(n);
        lin.push(linearSearch(a, n));
        var worst = 0;
        for (var t = 1; t <= n; t += 1) worst = Math.max(worst, binarySearch(a, t));
        bin.push(worst);
      }
      drawSeries([
        { label: 'linear', colour: 'var(--cyan)', values: lin },
        { label: 'binary', colour: 'var(--purple)', values: bin }
      ], xs, false);
      var rows = '';
      xs.filter(function (n) { return n % Math.max(1, Math.floor(xs.length / 10)) === 0; }).forEach(function (n, i) {
        var idx = xs.indexOf(n);
        rows += '<tr><td>' + n + '</td><td>' + lin[idx] + '</td><td>' + bin[idx] + '</td><td>'
          + (Math.floor(Math.log2(n)) + 1) + '</td></tr>';
      });
      table.innerHTML = '<thead><tr><th>n</th><th>linear (worst)</th><th>binary (worst)</th><th>⌊log₂n⌋+1</th></tr></thead><tbody>'
        + rows + '</tbody>';
      var last = xs.length - 1;
      k1L.textContent = 'linear'; k1.textContent = lin[last];
      k2L.textContent = 'binary'; k2.textContent = bin[last];
      status.innerHTML = 'At n = ' + xs[last] + ' the counted worst cases are <strong>' + lin[last]
        + '</strong> and <strong>' + bin[last] + '</strong>. The binary column matches ⌊log₂n⌋+1 exactly, because '
        + 'each comparison halves the remaining range — and that is only available because the array is SORTED. '
        + 'Sorting first costs O(n log n), so binary search pays for itself only across many searches.';
    },
    sort: function () {
      show(['alNWrap']);
      title.textContent = 'Sorting, comparisons counted';
      sub.textContent = 'the same input through three algorithms';
      var N = Math.max(4, +nS.value), xs = [], bub = [], ins = [], mer = [], nlogn = [];
      for (var n = 2; n <= N; n += 1) {
        var a = makeArray(n, 'shuffle');
        xs.push(n);
        bub.push(bubbleSort(a));
        ins.push(insertionSort(a));
        mer.push(mergeSort(a));
        nlogn.push(n * Math.log2(n));
      }
      drawSeries([
        { label: 'bubble', colour: 'var(--red)', values: bub },
        { label: 'insertion', colour: 'var(--amber)', values: ins },
        { label: 'merge', colour: 'var(--cyan)', values: mer },
        { label: 'n log n', colour: 'var(--purple)', values: nlogn }
      ], xs, false);
      var rows = '';
      xs.filter(function (n) { return n % Math.max(1, Math.floor(xs.length / 8)) === 0; }).forEach(function (n) {
        var i = xs.indexOf(n);
        rows += '<tr><td>' + n + '</td><td>' + bub[i] + '</td><td>' + ins[i] + '</td><td>' + mer[i]
          + '</td><td>' + Math.round(n * (n - 1) / 2) + '</td><td>' + Math.round(nlogn[i]) + '</td></tr>';
      });
      table.innerHTML = '<thead><tr><th>n</th><th>bubble</th><th>insertion</th><th>merge</th><th>n(n−1)/2</th><th>n log₂ n</th></tr></thead><tbody>'
        + rows + '</tbody>';
      var last = xs.length - 1;
      k1L.textContent = 'bubble'; k1.textContent = bub[last];
      k2L.textContent = 'merge'; k2.textContent = mer[last];
      status.innerHTML = 'At n = ' + xs[last] + ': bubble sort made <strong>' + bub[last] + '</strong> comparisons '
        + 'and merge sort <strong>' + mer[last] + '</strong>. Bubble sort matches n(n−1)/2 exactly, because its two '
        + 'loops do not depend on the data at all. Insertion sort does — it is the one whose count changes with the '
        + 'input, and on nearly-sorted data it beats merge sort, which is why real sort implementations switch to it '
        + 'for small subarrays.';
    },
    master: function () {
      show([]);
      title.textContent = 'The master theorem';
      sub.textContent = 'T(n) = a·T(n/b) + n^d';
      var cases = [
        [2, 2, 1, 'merge sort'],
        [2, 2, 0, 'binary-tree traversal'],
        [1, 2, 0, 'binary search'],
        [7, 2, 2, "Strassen's matrix multiplication"],
        [8, 2, 2, 'naive matrix multiplication'],
        [3, 2, 1, 'Karatsuba multiplication'],
        [4, 2, 2, 'balanced case'],
        [2, 4, 1, 'a < b^d']
      ];
      var rows = cases.map(function (c) {
        var a = c[0], b = c[1], d = c[2];
        var crit = Math.log(a) / Math.log(b);
        var which, result;
        if (Math.abs(crit - d) < 1e-9) { which = 'case 2 (a = b^d)'; result = 'Θ(n^' + d + ' log n)'; }
        else if (crit > d) { which = 'case 1 (a > b^d)'; result = 'Θ(n^log_' + b + ' ' + a + ') ≈ Θ(n^' + crit.toFixed(3) + ')'; }
        else { which = 'case 3 (a < b^d)'; result = 'Θ(n^' + d + ')'; }
        return '<tr><td>' + a + '</td><td>' + b + '</td><td>' + d + '</td><td>' + crit.toFixed(3) + '</td><td>'
          + which + '</td><td>' + result + '</td><td>' + c[3] + '</td></tr>';
      }).join('');
      table.innerHTML = '<thead><tr><th>a</th><th>b</th><th>d</th><th>log_b a</th><th>case</th><th>T(n)</th><th>example</th></tr></thead><tbody>'
        + rows + '</tbody>';
      var xs = [], series = [];
      for (var n = 2; n <= 64; n += 1) xs.push(n);
      series.push({ label: 'n log n', colour: 'var(--cyan)', values: xs.map(function (n) { return n * Math.log2(n); }) });
      series.push({ label: 'n^1.585', colour: 'var(--purple)', values: xs.map(function (n) { return Math.pow(n, Math.log2(3)); }) });
      series.push({ label: 'n²', colour: 'var(--red)', values: xs.map(function (n) { return n * n; }) });
      drawSeries(series, xs, true);
      k1L.textContent = 'compare'; k1.textContent = 'log_b a vs d';
      k2L.textContent = 'cases'; k2.textContent = '3';
      status.innerHTML = 'The whole theorem is one comparison: log_b a against d — whether the work at the leaves '
        + 'or the work at the root dominates. Karatsuba (a = 3, b = 2, d = 1) beats the naive n² only because '
        + 'log₂3 ≈ 1.585 &lt; 2; the improvement comes from doing three multiplications instead of four, and nothing else.';
    },
    greedy: function () {
      show(['alNWrap']);
      title.textContent = 'Greedy versus dynamic programming';
      sub.textContent = 'making change with coins 1, 3, 4';
      var amount = Math.max(2, +nS.value);
      var coinSets = [[1, 5, 10, 25], [1, 3, 4]];
      var rows = '';
      var mismatch = null;
      for (var a = 1; a <= amount; a += 1) {
        var g1 = greedyCoins(coinSets[0], a), d1 = dpCoins(coinSets[0], a);
        var g2 = greedyCoins(coinSets[1], a), d2 = dpCoins(coinSets[1], a);
        if (g2.count !== d2.count && mismatch === null) mismatch = { a: a, greedy: g2, dp: d2 };
        if (a > amount - 12) {
          rows += '<tr' + (g2.count !== d2.count ? ' class="focus"' : '') + '><td>' + a + '</td><td>' + g1.count
            + '</td><td>' + d1.count + '</td><td>' + g2.count + ' (' + g2.picks.join('+') + ')</td><td>'
            + d2.count + ' (' + d2.picks.join('+') + ')</td></tr>';
        }
      }
      table.innerHTML = '<thead><tr><th>amount</th><th>greedy {1,5,10,25}</th><th>optimal</th><th>greedy {1,3,4}</th><th>optimal</th></tr></thead><tbody>'
        + rows + '</tbody>';
      var xs = [], gv = [], dv = [];
      for (var v = 1; v <= amount; v += 1) {
        xs.push(v);
        gv.push(greedyCoins(coinSets[1], v).count);
        dv.push(dpCoins(coinSets[1], v).count);
      }
      drawSeries([
        { label: 'greedy', colour: 'var(--red)', values: gv },
        { label: 'optimal', colour: 'var(--cyan)', values: dv }
      ], xs, false);
      k1L.textContent = 'first failure'; k1.textContent = mismatch ? mismatch.a : 'none yet';
      k2L.textContent = 'gap'; k2.textContent = mismatch ? (mismatch.greedy.count - mismatch.dp.count) : 0;
      status.innerHTML = mismatch
        ? '<strong>Greedy is wrong at ' + mismatch.a + '.</strong> Taking the largest coin first gives '
          + mismatch.greedy.picks.join(' + ') + ' — ' + mismatch.greedy.count + ' coins — while the optimum is '
          + mismatch.dp.picks.join(' + ') + ', just ' + mismatch.dp.count + '. The same greedy rule is OPTIMAL for '
          + '{1, 5, 10, 25}, which is why "greedy works" is a property of the coin system, never of the strategy. '
          + 'Dynamic programming gets it right by solving every smaller amount once and reusing the answers.'
        : 'Raise n past 5 to find where greedy fails on the coin set {1, 3, 4}.';
    }
  };

  function redraw() {
    document.getElementById('alNOut').textContent = nS.value;
    MODES[modeSel.value]();
  }

  [nS, fSel, gSel].forEach(function (el) { el.addEventListener('input', redraw); });
  [modeSel, fSel, gSel].forEach(function (el) { el.addEventListener('change', redraw); });
  modeSel.value = """ + '"%s"' % cfg.get("mode", "growth") + r""";
  nS.value = """ + str(cfg.get("n", 16)) + r""";
  """ + (cfg.get("overrides_js") or "") + r"""
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Algorithms and growth",
        subtitle="Counts from running, not from quoting",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose what to measure"),
        panel_intro=cfg.get(
            "panel_intro",
            "The measured columns come from executing the algorithm with a counter. "
            "Where they diverge from the predicted growth, the reason is stated.",
        ),
        script=script,
    )
