"""Labs for course 2: sets, relations and functions."""

from .common import Lab, cfg_literal

SET_JS = r"""
  /* ---- finite sets as sorted integer arrays ---------------------------- */
  function uniq(a) { return a.filter(function (v, i) { return a.indexOf(v) === i; }).sort(function (x, y) { return x - y; }); }
  function union(a, b) { return uniq(a.concat(b)); }
  function inter(a, b) { return a.filter(function (v) { return b.indexOf(v) !== -1; }); }
  function diff(a, b) { return a.filter(function (v) { return b.indexOf(v) === -1; }); }
  function symdiff(a, b) { return union(diff(a, b), diff(b, a)); }
  function comp(a, u) { return diff(u, a); }
  function eq(a, b) { return a.length === b.length && a.every(function (v, i) { return v === b[i]; }); }
  function subset(a, b) { return a.every(function (v) { return b.indexOf(v) !== -1; }); }
  function setText(a) { return a.length ? '{' + a.join(', ') + '}' : '∅'; }
"""


def set_lab(cfg):
    """Set algebra over a visible universe, with both sides of an identity computed.

    A Venn diagram shows which REGIONS an expression selects; the element lists
    below it show which elements. Both are derived from the same membership
    toggles, so a reader who doubts the picture can check the list, and an
    identity is confirmed by the two sides selecting the same elements rather
    than by the diagram looking symmetric.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>Set expressions over U = {1, …, 12}</strong><span>Click an element to move it between the sets</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>selected by A</span><span class="tone-purple"><i class="legend-swatch"></i>selected by B</span></div>
      </div>
      <div class="lab-stage">
        <svg id="venn" viewBox="0 0 460 260" role="img" aria-label="Three overlapping sets drawn as circles; the regions an expression selects are filled."></svg>
        <div id="vennKey" class="small-copy" style="margin-top:8px;"></div>
      </div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="setRows"></table></div>"""
    controls = """        <div class="field">
          <label for="setExprA">Expression A</label>
          <select id="setExprA"></select>
        </div>
        <div class="field">
          <label for="setExprB">Expression B (compare)</label>
          <select id="setExprB"></select>
        </div>
        <div class="field">
          <label for="setMembers">Membership &mdash; click to toggle</label>
          <div id="setMembers"></div>
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>|A|</span><strong id="kA">&mdash;</strong></div>
          <div class="kpi"><span>|B|</span><strong id="kB">&mdash;</strong></div>
          <div class="kpi"><span>|C|</span><strong id="kC">&mdash;</strong></div>
          <div class="kpi"><span>Equal?</span><strong id="kEq">&mdash;</strong></div>
        </div>
        <div class="status-banner" id="setStatus">Pick two expressions and see whether anything separates them.</div>"""

    script = SET_JS + cfg_literal("SET_DEFAULT", cfg.get("default", ["A ∪ B", "B ∪ A"])) + r"""
  var U = [1,2,3,4,5,6,7,8,9,10,11,12];
  var S = { A: [1,2,3,4,5,6], B: [4,5,6,7,8,9], C: [2,3,6,7,10,11] };

  /* Each expression is a FUNCTION of the three sets, so the value shown is
     computed from the current membership every time -- never a stored answer. */
  var EXPR = [
    ['A', function (A) { return A; }],
    ['B', function (A, B) { return B; }],
    ['C', function (A, B, C) { return C; }],
    ['A ∪ B', function (A, B) { return union(A, B); }],
    ['B ∪ A', function (A, B) { return union(B, A); }],
    ['A ∩ B', function (A, B) { return inter(A, B); }],
    ['B ∩ A', function (A, B) { return inter(B, A); }],
    ['A \\ B', function (A, B) { return diff(A, B); }],
    ['B \\ A', function (A, B) { return diff(B, A); }],
    ['A △ B', function (A, B) { return symdiff(A, B); }],
    ['Ā', function (A) { return comp(A, U); }],
    ['A ∩ B̄', function (A, B) { return inter(A, comp(B, U)); }],
    ['A ∪ (B ∩ C)', function (A, B, C) { return union(A, inter(B, C)); }],
    ['(A ∪ B) ∩ (A ∪ C)', function (A, B, C) { return inter(union(A, B), union(A, C)); }],
    ['A ∩ (B ∪ C)', function (A, B, C) { return inter(A, union(B, C)); }],
    ['(A ∩ B) ∪ (A ∩ C)', function (A, B, C) { return union(inter(A, B), inter(A, C)); }],
    ['(A ∪ B)‾', function (A, B) { return comp(union(A, B), U); }],
    ['Ā ∩ B̄', function (A, B) { return inter(comp(A, U), comp(B, U)); }],
    ['(A ∩ B)‾', function (A, B) { return comp(inter(A, B), U); }],
    ['Ā ∪ B̄', function (A, B) { return union(comp(A, U), comp(B, U)); }],
    ['A ∪ (A ∩ B)', function (A, B) { return union(A, inter(A, B)); }],
    ['(A ∪ B) \\ (A ∩ B)', function (A, B) { return diff(union(A, B), inter(A, B)); }]
  ];

  var selA = document.getElementById('setExprA'), selB = document.getElementById('setExprB');
  EXPR.forEach(function (e, i) {
    [selA, selB].forEach(function (sel) {
      var o = document.createElement('option');
      o.value = String(i); o.textContent = e[0];
      sel.appendChild(o);
    });
  });
  function indexOfExpr(name) { for (var i = 0; i < EXPR.length; i += 1) if (EXPR[i][0] === name) return i; return 0; }
  selA.value = String(indexOfExpr(SET_DEFAULT[0]));
  selB.value = String(indexOfExpr(SET_DEFAULT[1]));

  var members = document.getElementById('setMembers');
  var rows = document.getElementById('setRows');
  var venn = document.getElementById('venn'), vennKey = document.getElementById('vennKey');
  var status = document.getElementById('setStatus');

  function inSet(name, v) { return S[name].indexOf(v) !== -1; }

  function paintMembers() {
    members.textContent = '';
    U.forEach(function (v) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'chip';
      var tags = ['A','B','C'].filter(function (n) { return inSet(n, v); });
      b.textContent = v + (tags.length ? ' · ' + tags.join('') : '');
      if (tags.length) b.classList.add('hi');
      b.title = 'Cycle element ' + v + ' through the sets';
      b.addEventListener('click', function () { cycle(v); });
      members.appendChild(b);
    });
  }

  /* Cycling through the eight membership patterns is what makes every REGION
     of the diagram reachable, including the ones a reader never draws. */
  function cycle(v) {
    var code = (inSet('A', v) ? 1 : 0) + (inSet('B', v) ? 2 : 0) + (inSet('C', v) ? 4 : 0);
    code = (code + 1) % 8;
    ['A','B','C'].forEach(function (n, i) {
      var want = (code >> i) & 1;
      var at = S[n].indexOf(v);
      if (want && at === -1) S[n] = uniq(S[n].concat([v]));
      if (!want && at !== -1) S[n].splice(at, 1);
    });
    redraw();
  }

  /* The seven bounded regions of a three-circle diagram plus the outside, each
     drawn where it belongs and filled when the expression selects it. A region
     is "selected" when every element in it is, which is well defined because an
     expression built from these operations cannot split a region. */
  var REGIONS = [
    { key: 'A',   cx: 118, cy: 108, label: 'A only' },
    { key: 'B',   cx: 232, cy: 108, label: 'B only' },
    { key: 'C',   cx: 175, cy: 186, label: 'C only' },
    { key: 'AB',  cx: 175, cy: 96,  label: 'A∩B' },
    { key: 'AC',  cx: 137, cy: 158, label: 'A∩C' },
    { key: 'BC',  cx: 213, cy: 158, label: 'B∩C' },
    { key: 'ABC', cx: 175, cy: 138, label: 'A∩B∩C' },
    { key: 'out', cx: 390, cy: 44,  label: 'outside' }
  ];
  function regionOf(v) {
    var a = inSet('A', v), b = inSet('B', v), c = inSet('C', v);
    if (!a && !b && !c) return 'out';
    return (a ? 'A' : '') + (b ? 'B' : '') + (c ? 'C' : '');
  }

  function paintVenn(sel) {
    var chosen = {};
    REGIONS.forEach(function (r) { chosen[r.key] = { on: false, off: false, items: [] }; });
    U.forEach(function (v) {
      var r = regionOf(v);
      if (!chosen[r]) return;
      chosen[r].items.push(v);
      if (sel.indexOf(v) !== -1) chosen[r].on = true; else chosen[r].off = true;
    });
    var circles = [
      ['A', 143, 122, 62, 'var(--cyan)'],
      ['B', 207, 122, 62, 'var(--purple)'],
      ['C', 175, 172, 62, 'var(--green)']
    ];
    var svg = '';
    circles.forEach(function (c) {
      svg += '<circle cx="' + c[1] + '" cy="' + c[2] + '" r="' + c[3]
        + '" fill="none" stroke="' + c[4] + '" stroke-width="2" opacity="0.85" />';
    });
    svg += '<text x="96" y="58" fill="var(--cyan)" font-size="15" font-weight="700">A</text>';
    svg += '<text x="252" y="58" fill="var(--purple)" font-size="15" font-weight="700">B</text>';
    svg += '<text x="169" y="248" fill="var(--green)" font-size="15" font-weight="700">C</text>';
    svg += '<text x="352" y="26" fill="var(--muted)" font-size="12">U</text>';
    REGIONS.forEach(function (r) {
      var st = chosen[r.key];
      if (!st.items.length) return;
      var on = st.on && !st.off;
      svg += '<circle cx="' + r.cx + '" cy="' + r.cy + '" r="15" fill="'
        + (on ? 'var(--cyan)' : 'var(--panel-3)') + '" opacity="' + (on ? '0.85' : '0.9') + '" />';
      svg += '<text x="' + r.cx + '" y="' + (r.cy + 4) + '" text-anchor="middle" font-size="10" font-weight="700" fill="'
        + (on ? 'var(--on-accent)' : 'var(--muted)') + '">' + st.items.length + '</text>';
    });
    venn.innerHTML = svg;
    vennKey.innerHTML = REGIONS.filter(function (r) { return chosen[r.key].items.length; })
      .map(function (r) {
        var st = chosen[r.key];
        return '<span class="chip' + (st.on && !st.off ? ' hi' : '') + '">' + r.label + ': ' + setText(st.items) + '</span>';
      }).join(' ');
  }

  function redraw() {
    var A = S.A.slice().sort(function (x, y) { return x - y; });
    var B = S.B.slice().sort(function (x, y) { return x - y; });
    var C = S.C.slice().sort(function (x, y) { return x - y; });
    var ea = EXPR[+selA.value], eb = EXPR[+selB.value];
    var va = ea[1](A, B, C), vb = eb[1](A, B, C);
    document.getElementById('kA').textContent = A.length;
    document.getElementById('kB').textContent = B.length;
    document.getElementById('kC').textContent = C.length;
    var same = eq(va, vb);
    document.getElementById('kEq').textContent = same ? 'yes' : 'no';
    rows.innerHTML = '<thead><tr><th>expression</th><th>value</th><th>size</th></tr></thead><tbody>'
      + '<tr><td>' + ea[0] + '</td><td>' + setText(va) + '</td><td>' + va.length + '</td></tr>'
      + '<tr><td>' + eb[0] + '</td><td>' + setText(vb) + '</td><td>' + vb.length + '</td></tr>'
      + '<tr class="focus"><td>difference</td><td>' + setText(symdiff(va, vb))
      + '</td><td>' + symdiff(va, vb).length + '</td></tr></tbody>';
    paintMembers();
    paintVenn(va);
    if (same) {
      status.innerHTML = '<strong>' + ea[0] + ' = ' + eb[0] + '</strong> on this membership. '
        + 'One membership is not a proof: it is a failed attempt at a counterexample. '
        + 'Click elements to try to separate them &mdash; if the identity is real you will not manage it.';
    } else {
      status.innerHTML = '<strong>' + ea[0] + ' ≠ ' + eb[0] + '.</strong> The elements in exactly one of '
        + 'them are ' + setText(symdiff(va, vb)) + ', and a single such element is a complete disproof.';
    }
  }

  selA.addEventListener('change', redraw);
  selB.addEventListener('change', redraw);
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Set algebra",
        subtitle="Two expressions, one membership",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Build the sets"),
        panel_intro=cfg.get(
            "panel_intro",
            "Both expressions are evaluated against the same twelve elements, so "
            "an identity either survives every membership you can build or it does not.",
        ),
        script=script,
    )


def relation_lab(cfg):
    """A relation you can edit, with every property decided by checking it.

    Reflexive, symmetric, antisymmetric and transitive are each defined by a
    quantified sentence, and each verdict below is produced by evaluating that
    sentence over the matrix -- reporting the offending pair when it fails.
    "Not transitive" without the (a, b), (b, c) that break it is the kind of
    feedback that teaches a reader to memorise names instead of checking.
    """
    n = cfg.get("size", 5)
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>A relation on S = {1, …, %d}</strong><span>Click a cell to add or remove the pair (a, b)</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>in R</span><span class="tone-amber"><i class="legend-swatch"></i>needed for closure</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="relGrid"></div></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="relProps"></table></div>""" % n
    controls = """        <div class="field">
          <label for="relPreset">Preset relation</label>
          <select id="relPreset">
            <option value="eq">a = b (equality)</option>
            <option value="le">a &le; b</option>
            <option value="lt">a &lt; b</option>
            <option value="div">a divides b</option>
            <option value="mod2">a &equiv; b (mod 2)</option>
            <option value="succ">b = a + 1</option>
            <option value="empty">empty relation</option>
            <option value="full">all pairs</option>
          </select>
        </div>
        <div class="field">
          <label for="relClosure">Show closure</label>
          <select id="relClosure">
            <option value="none">off</option>
            <option value="refl">reflexive closure</option>
            <option value="sym">symmetric closure</option>
            <option value="trans">transitive closure</option>
          </select>
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>Pairs</span><strong id="relCount">&mdash;</strong></div>
          <div class="kpi"><span>Kind</span><strong id="relKind">&mdash;</strong></div>
        </div>
        <div class="status-banner" id="relStatus">Toggle pairs and watch which properties survive.</div>"""

    script = cfg_literal("RN", n) + r"""
  var R = [];
  var grid = document.getElementById('relGrid'), props = document.getElementById('relProps');
  var status = document.getElementById('relStatus');
  var presetSel = document.getElementById('relPreset'), closureSel = document.getElementById('relClosure');

  var PRESETS = {
    eq: function (a, b) { return a === b; },
    le: function (a, b) { return a <= b; },
    lt: function (a, b) { return a < b; },
    div: function (a, b) { return b % a === 0; },
    mod2: function (a, b) { return (a - b) % 2 === 0; },
    succ: function (a, b) { return b === a + 1; },
    empty: function () { return false; },
    full: function () { return true; }
  };

  function fill(fn) {
    R = [];
    for (var a = 0; a < RN; a += 1) {
      var row = [];
      for (var b = 0; b < RN; b += 1) row.push(!!fn(a + 1, b + 1));
      R.push(row);
    }
  }

  function copy(M) { return M.map(function (r) { return r.slice(); }); }

  /* Each property is decided by evaluating its definition, and returns the
     witness that decides it. */
  function reflexive() {
    for (var a = 0; a < RN; a += 1) if (!R[a][a]) return { v: false, why: '(' + (a + 1) + ', ' + (a + 1) + ') ∉ R' };
    return { v: true, why: 'every (a, a) ∈ R' };
  }
  function irreflexive() {
    for (var a = 0; a < RN; a += 1) if (R[a][a]) return { v: false, why: '(' + (a + 1) + ', ' + (a + 1) + ') ∈ R' };
    return { v: true, why: 'no (a, a) ∈ R' };
  }
  function symmetric() {
    for (var a = 0; a < RN; a += 1) for (var b = 0; b < RN; b += 1)
      if (R[a][b] && !R[b][a]) return { v: false, why: '(' + (a + 1) + ', ' + (b + 1) + ') ∈ R but (' + (b + 1) + ', ' + (a + 1) + ') ∉ R' };
    return { v: true, why: 'every pair has its reverse' };
  }
  function antisymmetric() {
    for (var a = 0; a < RN; a += 1) for (var b = 0; b < RN; b += 1)
      if (a !== b && R[a][b] && R[b][a]) return { v: false, why: 'both (' + (a + 1) + ', ' + (b + 1) + ') and its reverse are in R' };
    return { v: true, why: 'no two distinct elements relate both ways' };
  }
  function transitive() {
    for (var a = 0; a < RN; a += 1) for (var b = 0; b < RN; b += 1) {
      if (!R[a][b]) continue;
      for (var c = 0; c < RN; c += 1) {
        if (R[b][c] && !R[a][c])
          return { v: false, why: '(' + (a + 1) + ', ' + (b + 1) + ') and (' + (b + 1) + ', ' + (c + 1) + ') ∈ R but (' + (a + 1) + ', ' + (c + 1) + ') ∉ R' };
      }
    }
    return { v: true, why: 'every two-step path is a one-step edge' };
  }

  function reflClosure() { var M = copy(R); for (var a = 0; a < RN; a += 1) M[a][a] = true; return M; }
  function symClosure() {
    var M = copy(R);
    for (var a = 0; a < RN; a += 1) for (var b = 0; b < RN; b += 1) if (R[a][b]) M[b][a] = true;
    return M;
  }
  /* Warshall: the transitive closure, computed rather than asserted. */
  function transClosure() {
    var M = copy(R);
    for (var k = 0; k < RN; k += 1)
      for (var a = 0; a < RN; a += 1)
        for (var b = 0; b < RN; b += 1)
          if (M[a][k] && M[k][b]) M[a][b] = true;
    return M;
  }

  /* Equivalence classes, by walking the relation -- only meaningful when R is
     an equivalence relation, which is why it is only reported then. */
  function classes() {
    var seen = [], out = [];
    for (var a = 0; a < RN; a += 1) {
      if (seen.indexOf(a) !== -1) continue;
      var cls = [];
      for (var b = 0; b < RN; b += 1) if (R[a][b]) { cls.push(b + 1); seen.push(b); }
      out.push(cls);
    }
    return out;
  }

  function paintGrid() {
    var mode = closureSel.value;
    var extra = mode === 'refl' ? reflClosure() : mode === 'sym' ? symClosure() : mode === 'trans' ? transClosure() : null;
    var h = '<table class="tt"><caption>rows are a, columns are b; a cell is the pair (a, b)</caption><thead><tr><th></th>';
    for (var b = 1; b <= RN; b += 1) h += '<th>' + b + '</th>';
    h += '</tr></thead><tbody>';
    for (var a = 0; a < RN; a += 1) {
      h += '<tr><th class="rowhead">' + (a + 1) + '</th>';
      for (var b2 = 0; b2 < RN; b2 += 1) {
        var here = R[a][b2], added = extra && extra[a][b2] && !here;
        h += '<td class="' + (here ? 'on' : '') + '" data-a="' + a + '" data-b="' + b2
          + '" role="button" tabindex="0" style="cursor:pointer;'
          + (added ? 'color:var(--amber);font-weight:800;' : '') + '">'
          + (here ? '1' : (added ? '+' : '·')) + '</td>';
      }
      h += '</tr>';
    }
    grid.innerHTML = h + '</tbody></table>';
  }

  function paintProps() {
    var rows = [
      ['reflexive', '∀a. (a, a) ∈ R', reflexive()],
      ['irreflexive', '∀a. (a, a) ∉ R', irreflexive()],
      ['symmetric', '∀a,b. aRb → bRa', symmetric()],
      ['antisymmetric', '∀a≠b. ¬(aRb ∧ bRa)', antisymmetric()],
      ['transitive', '∀a,b,c. aRb ∧ bRc → aRc', transitive()]
    ];
    var h = '<thead><tr><th>property</th><th>definition</th><th>holds</th><th>because</th></tr></thead><tbody>';
    rows.forEach(function (r) {
      h += '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td class="' + (r[2].v ? 't' : 'f') + '">'
        + (r[2].v ? 'yes' : 'no') + '</td><td>' + r[2].why + '</td></tr>';
    });
    props.innerHTML = h + '</tbody></table>';
  }

  function redraw() {
    paintGrid();
    paintProps();
    var count = 0;
    for (var a = 0; a < RN; a += 1) for (var b = 0; b < RN; b += 1) if (R[a][b]) count += 1;
    document.getElementById('relCount').textContent = count;
    var isEquiv = reflexive().v && symmetric().v && transitive().v;
    var isOrder = reflexive().v && antisymmetric().v && transitive().v;
    var kind = isEquiv ? 'equivalence' : isOrder ? 'partial order' : '—';
    document.getElementById('relKind').textContent = kind;
    if (isEquiv) {
      var cls = classes();
      status.innerHTML = '<strong>This is an equivalence relation</strong>, so it partitions S into '
        + cls.length + ' class' + (cls.length === 1 ? '' : 'es') + ': '
        + cls.map(function (c) { return '{' + c.join(', ') + '}'; }).join(', ')
        + '. Every element lands in exactly one &mdash; that is the theorem, and you can check it above.';
    } else if (isOrder) {
      status.innerHTML = '<strong>This is a partial order.</strong> Antisymmetry is what stops it '
        + 'being an equivalence: distinct elements never relate both ways, so the relation ranks '
        + 'rather than groups. Some pairs may be incomparable, which is what makes it partial.';
    } else {
      var fails = [];
      if (!reflexive().v) fails.push('reflexivity (' + reflexive().why + ')');
      if (!symmetric().v && !antisymmetric().v) fails.push('symmetry and antisymmetry both');
      if (!transitive().v) fails.push('transitivity (' + transitive().why + ')');
      status.innerHTML = 'Not an equivalence relation and not a partial order. Failing: ' + fails.join('; ') + '.';
    }
  }

  grid.addEventListener('click', function (e) {
    var td = e.target.closest('td[data-a]');
    if (!td) return;
    R[+td.dataset.a][+td.dataset.b] = !R[+td.dataset.a][+td.dataset.b];
    redraw();
  });
  grid.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var td = e.target.closest('td[data-a]');
    if (!td) return;
    e.preventDefault();
    R[+td.dataset.a][+td.dataset.b] = !R[+td.dataset.a][+td.dataset.b];
    redraw();
  });
  presetSel.addEventListener('change', function () { fill(PRESETS[presetSel.value]); redraw(); });
  closureSel.addEventListener('change', redraw);

  presetSel.value = """ + '"%s"' % cfg.get("preset", "div") + r""";
  fill(PRESETS[presetSel.value]);
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Relation properties",
        subtitle="Decided by checking, not by name",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose a relation"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every verdict names the pair that decides it, so a failure tells you "
            "where to look instead of only that you were wrong.",
        ),
        script=script,
    )


def function_lab(cfg):
    """f : A -> B, assigned by hand, classified by counting.

    Injective and surjective are properties of the whole assignment, not of a
    formula, so the lab lets the reader build any function at all and reports
    which of the two it has -- with the collision or the missed element named.
    The counts underneath are the pigeonhole principle in its bare form: with
    |A| > |B| the injective column can never be reached, and the lab says so
    before the reader tries.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>f : A &rarr; B</strong><span>Choose where each element of A is sent</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>hit once</span><span class="tone-amber"><i class="legend-swatch"></i>hit twice or more</span><span class="tone-muted"><i class="legend-swatch"></i>never hit</span></div>
      </div>
      <div class="lab-stage"><svg id="fnPlot" viewBox="0 0 460 300" role="img" aria-label="Two columns of dots with an arrow from each element of the domain to its image."></svg></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="fnProps"></table></div>"""
    controls = """        <div>
          <div class="range-row"><label class="small-copy" for="fnA">|A| (domain)</label><span class="range-value" id="fnAOut">4</span></div>
          <input id="fnA" type="range" min="1" max="6" value="4" />
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="fnB">|B| (codomain)</label><span class="range-value" id="fnBOut">4</span></div>
          <input id="fnB" type="range" min="1" max="6" value="4" />
        </div>
        <div class="field">
          <label>Assignment &mdash; click to advance each arrow</label>
          <div id="fnMap"></div>
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>Injective</span><strong id="fnInj">&mdash;</strong></div>
          <div class="kpi"><span>Surjective</span><strong id="fnSur">&mdash;</strong></div>
          <div class="kpi"><span>Image size</span><strong id="fnImg">&mdash;</strong></div>
        </div>
        <div class="status-banner" id="fnStatus">Change the sizes and try to build a bijection.</div>"""

    script = r"""
  var f = [0, 1, 2, 3], nA = 4, nB = 4;
  var plot = document.getElementById('fnPlot'), propsOut = document.getElementById('fnProps');
  var mapOut = document.getElementById('fnMap'), status = document.getElementById('fnStatus');
  var aSlider = document.getElementById('fnA'), bSlider = document.getElementById('fnB');

  function image() {
    var seen = [];
    for (var i = 0; i < nA; i += 1) if (seen.indexOf(f[i]) === -1) seen.push(f[i]);
    return seen.sort(function (x, y) { return x - y; });
  }
  function collision() {
    for (var i = 0; i < nA; i += 1) for (var j = i + 1; j < nA; j += 1)
      if (f[i] === f[j]) return [i, j];
    return null;
  }
  function missed() {
    var img = image();
    for (var b = 0; b < nB; b += 1) if (img.indexOf(b) === -1) return b;
    return -1;
  }

  function paintPlot() {
    var top = 34, gap = 40;
    var s = '';
    for (var i = 0; i < nA; i += 1) {
      var y = top + i * gap;
      s += '<circle cx="110" cy="' + y + '" r="13" fill="var(--panel-3)" stroke="var(--cyan)" stroke-width="2" />';
      s += '<text x="110" y="' + (y + 5) + '" text-anchor="middle" font-size="12" font-weight="700" fill="var(--text)">a' + (i + 1) + '</text>';
    }
    var counts = {};
    for (var k = 0; k < nA; k += 1) counts[f[k]] = (counts[f[k]] || 0) + 1;
    for (var j = 0; j < nB; j += 1) {
      var yb = top + j * gap;
      var c = counts[j] || 0;
      var stroke = c === 0 ? 'var(--muted)' : c === 1 ? 'var(--cyan)' : 'var(--amber)';
      s += '<circle cx="350" cy="' + yb + '" r="13" fill="var(--panel-3)" stroke="' + stroke + '" stroke-width="2" />';
      s += '<text x="350" y="' + (yb + 5) + '" text-anchor="middle" font-size="12" font-weight="700" fill="var(--text)">b' + (j + 1) + '</text>';
    }
    for (var i2 = 0; i2 < nA; i2 += 1) {
      var y1 = top + i2 * gap, y2 = top + f[i2] * gap;
      var dup = (counts[f[i2]] || 0) > 1;
      s += '<line x1="126" y1="' + y1 + '" x2="334" y2="' + y2 + '" stroke="'
        + (dup ? 'var(--amber)' : 'var(--cyan)') + '" stroke-width="2" opacity="0.8" />';
    }
    s += '<text x="110" y="18" text-anchor="middle" font-size="12" fill="var(--muted)">A</text>';
    s += '<text x="350" y="18" text-anchor="middle" font-size="12" fill="var(--muted)">B</text>';
    plot.setAttribute('viewBox', '0 0 460 ' + Math.max(300, top + Math.max(nA, nB) * gap + 10));
    plot.innerHTML = s;
  }

  function paintMap() {
    mapOut.textContent = '';
    for (var i = 0; i < nA; i += 1) {
      (function (i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'chip hi';
        b.textContent = 'a' + (i + 1) + ' ↦ b' + (f[i] + 1);
        b.addEventListener('click', function () { f[i] = (f[i] + 1) % nB; redraw(); });
        mapOut.appendChild(b);
      })(i);
    }
  }

  function redraw() {
    nA = +aSlider.value; nB = +bSlider.value;
    document.getElementById('fnAOut').textContent = nA;
    document.getElementById('fnBOut').textContent = nB;
    while (f.length < nA) f.push(0);
    for (var i = 0; i < nA; i += 1) if (f[i] >= nB) f[i] = nB - 1;
    var col = collision(), miss = missed(), img = image();
    var inj = col === null, sur = miss === -1;
    document.getElementById('fnInj').textContent = inj ? 'yes' : 'no';
    document.getElementById('fnSur').textContent = sur ? 'yes' : 'no';
    document.getElementById('fnImg').textContent = img.length + ' / ' + nB;
    propsOut.innerHTML = '<thead><tr><th>property</th><th>definition</th><th>holds</th><th>because</th></tr></thead><tbody>'
      + '<tr><td>injective</td><td>f(x) = f(y) → x = y</td><td class="' + (inj ? 't' : 'f') + '">'
      + (inj ? 'yes' : 'no') + '</td><td>'
      + (inj ? 'no two elements share an image' : 'a' + (col[0] + 1) + ' and a' + (col[1] + 1) + ' both map to b' + (f[col[0]] + 1)) + '</td></tr>'
      + '<tr><td>surjective</td><td>∀b ∃a. f(a) = b</td><td class="' + (sur ? 't' : 'f') + '">'
      + (sur ? 'yes' : 'no') + '</td><td>'
      + (sur ? 'every element of B is hit' : 'b' + (miss + 1) + ' is never hit') + '</td></tr>'
      + '<tr class="focus"><td>bijective</td><td>both</td><td class="' + (inj && sur ? 't' : 'f') + '">'
      + (inj && sur ? 'yes' : 'no') + '</td><td>'
      + (inj && sur ? 'f has a two-sided inverse' : 'no inverse function exists') + '</td></tr></tbody>';
    paintPlot(); paintMap();
    if (nA > nB) {
      status.innerHTML = '<strong>|A| = ' + nA + ' > ' + nB + ' = |B|, so no injection exists at all.</strong> '
        + 'That is the pigeonhole principle, and it is not a statement about this assignment: '
        + 'you cannot fix it by rearranging the arrows.';
    } else if (nB > nA) {
      status.innerHTML = '<strong>|B| = ' + nB + ' > ' + nA + ' = |A|, so no surjection exists.</strong> '
        + nA + ' arrows cannot cover ' + nB + ' targets, however they are arranged.';
    } else if (inj && sur) {
      status.innerHTML = '<strong>A bijection.</strong> With |A| = |B| finite, injective and surjective '
        + 'imply each other &mdash; which is exactly the property that fails for infinite sets, and is why '
        + 'ℕ can be put in bijection with a proper subset of itself.';
    } else {
      status.innerHTML = 'With |A| = |B| a bijection is possible; this assignment is not one yet. '
        + (inj ? '' : 'Two elements collide. ') + (sur ? '' : 'Something in B is unhit. ')
        + 'On equal finite sets those two failures always arrive together.';
    }
  }

  aSlider.addEventListener('input', redraw);
  bSlider.addEventListener('input', redraw);
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Injective, surjective, bijective",
        subtitle="Built by hand, classified by counting",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Build a function"),
        panel_intro=cfg.get(
            "panel_intro",
            "Change the two sizes first. Some combinations make one of the two "
            "properties unreachable, and the lab says so rather than letting you hunt.",
        ),
        script=script,
    )
