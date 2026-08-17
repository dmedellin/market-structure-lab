"""Labs for course 1: propositional and predicate logic."""

from .common import Lab, cfg_literal

# --------------------------------------------------------------------------
# A recursive-descent parser and evaluator for propositional logic.
#
# It is shared by every logic lab and it is the reason those labs can be
# HONEST: the table is produced by evaluating the formula the reader chose over
# every assignment, so a column is right because the evaluator is right, not
# because someone typed a column of Ts and Fs correctly.
#
# Precedence, tightest first:  NOT  >  AND  >  OR, XOR  >  IMPLIES  >  IFF
# IMPLIES is right-associative (p->q->r parses as p->(q->r)); the rest are left.
# --------------------------------------------------------------------------
PARSER_JS = r"""
  /* ---- propositional logic: tokenizer, parser, evaluator ---------------- */
  var OPS = {
    '¬': 'not', '~': 'not', '!': 'not',
    '∧': 'and', '&': 'and',
    '∨': 'or', '|': 'or',
    '⊕': 'xor', '^': 'xor',
    '→': 'imp', '⇒': 'imp',
    '↔': 'iff', '⇔': 'iff'
  };
  var GLYPH = { not: '¬', and: '∧', or: '∨', xor: '⊕', imp: '→', iff: '↔' };

  function tokenize(src) {
    var out = [], i = 0;
    while (i < src.length) {
      var ch = src[i];
      if (ch === ' ') { i += 1; continue; }
      if (src.substr(i, 3) === '<->') { out.push({ t: 'op', v: 'iff' }); i += 3; continue; }
      if (src.substr(i, 2) === '->') { out.push({ t: 'op', v: 'imp' }); i += 2; continue; }
      if (ch === '(' || ch === ')') { out.push({ t: ch }); i += 1; continue; }
      if (OPS[ch]) { out.push({ t: 'op', v: OPS[ch] }); i += 1; continue; }
      if (/[A-Za-z]/.test(ch)) { out.push({ t: 'var', v: ch }); i += 1; continue; }
      if (ch === '⊤') { out.push({ t: 'const', v: true }); i += 1; continue; }
      if (ch === '⊥') { out.push({ t: 'const', v: false }); i += 1; continue; }
      throw new Error('unexpected character ' + ch);
    }
    return out;
  }

  function parse(src) {
    var ts = tokenize(src), pos = 0;
    function peek() { return ts[pos]; }
    function eat(kind, value) {
      var t = ts[pos];
      if (!t || t.t !== kind || (value !== undefined && t.v !== value)) return null;
      pos += 1;
      return t;
    }
    function primary() {
      if (eat('(')) {
        var inner = iff();
        if (!eat(')')) throw new Error('missing )');
        return inner;
      }
      var n = eat('op', 'not');
      if (n) return { op: 'not', a: primary() };
      var c = eat('const');
      if (c) return { op: 'const', v: c.v };
      var v = eat('var');
      if (!v) throw new Error('expected a variable');
      return { op: 'var', name: v.v };
    }
    function binaryLeft(next, names) {
      var node = next();
      for (;;) {
        var t = peek();
        if (t && t.t === 'op' && names.indexOf(t.v) !== -1) { pos += 1; node = { op: t.v, a: node, b: next() }; }
        else return node;
      }
    }
    function and() { return binaryLeft(primary, ['and']); }
    function or() { return binaryLeft(and, ['or', 'xor']); }
    function imp() {
      var left = or(), t = peek();
      if (t && t.t === 'op' && t.v === 'imp') { pos += 1; return { op: 'imp', a: left, b: imp() }; }
      return left;
    }
    function iff() { return binaryLeft(imp, ['iff']); }
    var tree = iff();
    if (pos !== ts.length) throw new Error('trailing input');
    return tree;
  }

  function evalNode(node, env) {
    switch (node.op) {
      case 'var': return !!env[node.name];
      case 'const': return node.v;
      case 'not': return !evalNode(node.a, env);
      case 'and': return evalNode(node.a, env) && evalNode(node.b, env);
      case 'or': return evalNode(node.a, env) || evalNode(node.b, env);
      case 'xor': return evalNode(node.a, env) !== evalNode(node.b, env);
      case 'imp': return !evalNode(node.a, env) || evalNode(node.b, env);
      case 'iff': return evalNode(node.a, env) === evalNode(node.b, env);
    }
    throw new Error('unknown node');
  }

  function show(node, outer) {
    switch (node.op) {
      case 'var': return node.name;
      case 'const': return node.v ? '⊤' : '⊥';
      case 'not': return GLYPH.not + show(node.a, false);
      default: {
        var s = show(node.a, false) + ' ' + GLYPH[node.op] + ' ' + show(node.b, false);
        return outer ? s : '(' + s + ')';
      }
    }
  }

  function variablesOf(node, seen) {
    seen = seen || [];
    if (node.op === 'var') { if (seen.indexOf(node.name) === -1) seen.push(node.name); }
    else { if (node.a) variablesOf(node.a, seen); if (node.b) variablesOf(node.b, seen); }
    return seen;
  }

  /* Every subexpression, in the order a reader would evaluate them: operands
     before the operator that combines them. Duplicates collapse, so p appears
     once however often it is written. */
  function subexpressions(node, out, seen) {
    out = out || []; seen = seen || {};
    if (node.a) subexpressions(node.a, out, seen);
    if (node.b) subexpressions(node.b, out, seen);
    if (node.op === 'var' || node.op === 'const') return out;
    var key = show(node, false);
    if (!seen[key]) { seen[key] = true; out.push(node); }
    return out;
  }

  /* Rows in the conventional order: T before F, leftmost variable slowest. */
  function assignments(vars) {
    var rows = [], total = 1 << vars.length;
    for (var i = 0; i < total; i += 1) {
      var env = {};
      for (var j = 0; j < vars.length; j += 1) {
        env[vars[j]] = ((i >> (vars.length - 1 - j)) & 1) === 0;
      }
      rows.push(env);
    }
    return rows;
  }
"""


def truth_table(cfg):
    """Build the truth table of a formula, column by column.

    Two modes on one control: ONE formula (classify it) or TWO (are they
    equivalent, and if not, at which assignment do they differ). The second is
    the whole of logical equivalence -- two formulas are equivalent exactly
    when no row separates them -- so the lab shows the separating row rather
    than announcing a verdict.
    """
    formulas = cfg["formulas"]
    default_b = cfg.get("compare_with")
    options = "".join(
        '<option value="%s">%s</option>' % (f, f) for f in formulas
    )
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>Truth table</strong><span id="ttCaption">Every assignment, every subexpression</span></div>
        <div class="inline-legend"><span class="tone-green"><i class="legend-swatch"></i>T</span><span class="tone-red"><i class="legend-swatch"></i>F</span><span class="tone-cyan"><i class="legend-swatch"></i>Whole formula</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="ttOut"></div></div>"""
    controls = """        <div class="field">
          <label for="ttMode">What to do</label>
          <select id="ttMode">
            <option value="one">Classify one formula</option>
            <option value="two"%s>Compare two formulas</option>
          </select>
        </div>
        <div class="field">
          <label for="ttA">Formula A</label>
          <select id="ttA">%s</select>
        </div>
        <div class="field" id="ttBWrap" hidden>
          <label for="ttB">Formula B</label>
          <select id="ttB">%s</select>
        </div>
        <div class="field">
          <label for="ttCustom">Or type your own (variables p q r s; operators ~ &amp; | -&gt; &lt;-&gt; ^)</label>
          <input id="ttCustom" type="text" placeholder="p -&gt; (q | r)" autocomplete="off" spellcheck="false" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>Rows</span><strong id="ttRows">&mdash;</strong></div>
          <div class="kpi"><span>True in</span><strong id="ttTrue">&mdash;</strong></div>
          <div class="kpi"><span>Verdict</span><strong id="ttVerdict">&mdash;</strong></div>
        </div>
        <div class="status-banner" id="ttStatus">Pick a formula.</div>""" % (
        ' selected="selected"' if cfg.get("mode") == "two" else "",
        options,
        "".join(
            '<option value="%s"%s>%s</option>'
            % (f, ' selected="selected"' if f == default_b else "", f)
            for f in formulas
        ),
    )

    script = PARSER_JS + """
  var modeSel = document.getElementById('ttMode');
  var selA = document.getElementById('ttA'), selB = document.getElementById('ttB');
  var bWrap = document.getElementById('ttBWrap');
  var custom = document.getElementById('ttCustom');
  var out = document.getElementById('ttOut');
  var rowsOut = document.getElementById('ttRows'), trueOut = document.getElementById('ttTrue');
  var verdictOut = document.getElementById('ttVerdict'), status = document.getElementById('ttStatus');
  var caption = document.getElementById('ttCaption');

  function cell(v) { return '<td class="' + (v ? 't' : 'f') + '">' + (v ? 'T' : 'F') + '</td>'; }

  function classify(count, total) {
    if (count === total) return ['Tautology', 'true under every assignment'];
    if (count === 0) return ['Contradiction', 'false under every assignment'];
    return ['Contingent', 'true under some assignments and false under others'];
  }

  function renderOne(tree) {
    var vars = variablesOf(tree).sort();
    if (!vars.length) vars = ['p'];
    var subs = subexpressions(tree);
    var whole = subs.length ? subs[subs.length - 1] : tree;
    var rows = assignments(vars);
    var head = '<tr>' + vars.map(function (v) { return '<th>' + v + '</th>'; }).join('')
      + subs.map(function (n, i) {
          var label = show(n, n === whole);
          return '<th' + (i === subs.length - 1 ? ' class="rowhead"' : '') + '>' + label + '</th>';
        }).join('') + '</tr>';
    var body = '', trueCount = 0;
    rows.forEach(function (env) {
      var final = evalNode(tree, env);
      if (final) trueCount += 1;
      body += '<tr>' + vars.map(function (v) { return cell(env[v]); }).join('')
        + subs.map(function (n) { return cell(evalNode(n, env)); }).join('') + '</tr>';
    });
    if (!subs.length) {
      body = '';
      rows.forEach(function (env) {
        var final = evalNode(tree, env);
        if (final) trueCount += 1;
        body += '<tr>' + vars.map(function (v) { return cell(env[v]); }).join('') + '</tr>';
      });
    }
    out.innerHTML = '<table class="tt"><caption>' + rows.length + ' assignments of '
      + vars.length + ' variable' + (vars.length === 1 ? '' : 's') + '</caption><thead>'
      + head + '</thead><tbody>' + body + '</tbody></table>';
    var verdict = classify(trueCount, rows.length);
    rowsOut.textContent = rows.length;
    trueOut.textContent = trueCount + ' / ' + rows.length;
    verdictOut.textContent = verdict[0];
    status.innerHTML = '<strong>' + show(tree, true) + '</strong> is <strong>' + verdict[0].toLowerCase()
      + '</strong>: ' + verdict[1] + '. It is satisfiable' + (trueCount ? '' : ' by no assignment')
      + (trueCount ? ' &mdash; ' + trueCount + ' row' + (trueCount === 1 ? '' : 's') + ' satisfy it' : '') + '.';
    caption.textContent = 'One formula, ' + subs.length + ' subexpression column' + (subs.length === 1 ? '' : 's');
  }

  function renderTwo(a, b) {
    var vars = variablesOf(a, variablesOf(b)).sort();
    if (!vars.length) vars = ['p'];
    var rows = assignments(vars);
    var head = '<tr>' + vars.map(function (v) { return '<th>' + v + '</th>'; }).join('')
      + '<th>' + show(a, true) + '</th><th>' + show(b, true) + '</th><th class="rowhead">same?</th></tr>';
    var body = '', differ = null, agree = 0;
    rows.forEach(function (env) {
      var va = evalNode(a, env), vb = evalNode(b, env), same = va === vb;
      if (same) agree += 1; else if (!differ) differ = env;
      body += '<tr' + (same ? '' : ' class="focus"') + '>'
        + vars.map(function (v) { return cell(env[v]); }).join('')
        + cell(va) + cell(vb)
        + '<td class="' + (same ? 't' : 'f') + '">' + (same ? '=' : '≠') + '</td></tr>';
    });
    out.innerHTML = '<table class="tt"><caption>' + rows.length
      + ' assignments; a highlighted row is one that separates the two formulas</caption><thead>'
      + head + '</thead><tbody>' + body + '</tbody></table>';
    rowsOut.textContent = rows.length;
    trueOut.textContent = agree + ' / ' + rows.length;
    verdictOut.textContent = differ ? 'Not equivalent' : 'Equivalent';
    if (differ) {
      var witness = vars.map(function (v) { return v + ' = ' + (differ[v] ? 'T' : 'F'); }).join(', ');
      status.innerHTML = 'These are <strong>not equivalent</strong>. One row is enough to prove it: at '
        + '<strong>' + witness + '</strong> the two formulas take different truth values, so no argument '
        + 'about the other rows can rescue the claim.';
    } else {
      status.innerHTML = 'These are <strong>logically equivalent</strong>: they agree in all '
        + rows.length + ' rows, which is exactly what equivalence means &mdash; not that they look alike, '
        + 'but that no assignment separates them.';
    }
    caption.textContent = 'Two formulas, compared row by row';
  }

  /* The try/catch covers PARSING and nothing else. A reader can type an
     ill-formed formula and must get a helpful message rather than a broken
     page; a bug in the table renderer must NOT be swallowed by the same
     handler, because a lab that silently degrades into an error banner looks
     like bad input and hides a real defect. So the parse is guarded and the
     render is not. */
  function redraw() {
    var two = modeSel.value === 'two';
    bWrap.hidden = !two;
    var typed = custom.value.trim();
    var treeA, treeB;
    try {
      treeA = parse(typed || selA.value);
      if (two) treeB = parse(selB.value);
    } catch (e) {
      custom.style.borderColor = 'var(--red)';
      status.innerHTML = '<strong>That is not a well-formed formula.</strong> '
        + 'Use variables p q r s and the operators ~ &amp; | -&gt; &lt;-&gt; ^, with balanced parentheses.';
      return;
    }
    custom.style.borderColor = '';
    if (two) renderTwo(treeA, treeB); else renderOne(treeA);
  }

  [modeSel, selA, selB].forEach(function (el) { el.addEventListener('change', redraw); });
  custom.addEventListener('input', redraw);
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Truth table",
        subtitle="Every assignment, evaluated",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Choose what to evaluate"),
        panel_intro=cfg.get(
            "panel_intro",
            "The table is produced by evaluating the formula under every assignment, "
            "so the columns are a computation rather than a claim.",
        ),
        script=script,
    )


def quantifier(cfg):
    """Nested quantifiers over a small, visible universe.

    The order of two quantifiers is the single most common misreading in
    predicate logic, and prose cannot settle it. A grid can: the reader toggles
    the truth of P(x, y) cell by cell, and the four orderings are re-evaluated
    against the grid they can see. The lab reports the witness or the
    counterexample, because "false" without the x that kills it teaches nothing.
    """
    n = cfg.get("size", 4)
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>P(x, y) over a finite universe</strong><span>Click a cell to make that pair true or false</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>P(x, y) holds</span><span class="tone-muted"><i class="legend-swatch"></i>fails</span></div>
      </div>
      <div class="lab-stage"><div class="table-wrap" id="qGrid"></div></div>
      <div class="table-wrap" style="margin-top:12px;"><table class="tt" id="qVerdicts"></table></div>"""
    controls = """        <div class="field">
          <label for="qPreset">Preset</label>
          <select id="qPreset">
            <option value="diag">Identity: P(x, y) iff x = y</option>
            <option value="le">Order: P(x, y) iff x &le; y</option>
            <option value="succ">Successor: P(x, y) iff y = x + 1</option>
            <option value="all">Everything true</option>
            <option value="none">Everything false</option>
          </select>
        </div>
        <div class="btn-row">
          <button class="btn small" id="qClear" type="button">Clear</button>
          <button class="btn small" id="qFlip" type="button">Complement</button>
        </div>
        <div class="status-banner" id="qStatus">Toggle cells and watch the four orderings move independently.</div>"""

    script = cfg_literal("QN", n) + r"""
  var grid = document.getElementById('qGrid');
  var verdicts = document.getElementById('qVerdicts');
  var status = document.getElementById('qStatus');
  var preset = document.getElementById('qPreset');
  var P = [];

  function fill(fn) {
    P = [];
    for (var x = 0; x < QN; x += 1) {
      var row = [];
      for (var y = 0; y < QN; y += 1) row.push(!!fn(x + 1, y + 1));
      P.push(row);
    }
  }

  var PRESETS = {
    diag: function (x, y) { return x === y; },
    le: function (x, y) { return x <= y; },
    succ: function (x, y) { return y === x + 1; },
    all: function () { return true; },
    none: function () { return false; }
  };

  /* The four orderings, evaluated by actually walking the grid. Each returns a
     verdict AND the element that decides it, because "false" on its own is the
     half of the answer that teaches nothing. */
  function forallForall() {
    for (var x = 0; x < QN; x += 1) for (var y = 0; y < QN; y += 1)
      if (!P[x][y]) return { v: false, why: 'x = ' + (x + 1) + ', y = ' + (y + 1) + ' fails' };
    return { v: true, why: 'no pair fails' };
  }
  function forallExists() {
    for (var x = 0; x < QN; x += 1) {
      var found = -1;
      for (var y = 0; y < QN; y += 1) if (P[x][y]) { found = y + 1; break; }
      if (found === -1) return { v: false, why: 'x = ' + (x + 1) + ' has no y at all' };
    }
    return { v: true, why: 'every x has some y (the y may differ per x)' };
  }
  function existsForall() {
    for (var x = 0; x < QN; x += 1) {
      var ok = true;
      for (var y = 0; y < QN; y += 1) if (!P[x][y]) { ok = false; break; }
      if (ok) return { v: true, why: 'x = ' + (x + 1) + ' works for every y' };
    }
    return { v: false, why: 'no single x works for all y' };
  }
  function existsExists() {
    for (var x = 0; x < QN; x += 1) for (var y = 0; y < QN; y += 1)
      if (P[x][y]) return { v: true, why: 'x = ' + (x + 1) + ', y = ' + (y + 1) + ' works' };
    return { v: false, why: 'no pair holds' };
  }

  function paintGrid() {
    var h = '<table class="tt"><caption>rows are x, columns are y, over U = {1, …, ' + QN + '}</caption><thead><tr><th></th>';
    for (var y = 1; y <= QN; y += 1) h += '<th>y=' + y + '</th>';
    h += '</tr></thead><tbody>';
    for (var x = 0; x < QN; x += 1) {
      h += '<tr><th class="rowhead">x=' + (x + 1) + '</th>';
      for (var y2 = 0; y2 < QN; y2 += 1) {
        h += '<td class="' + (P[x][y2] ? 'on' : '') + '" data-x="' + x + '" data-y="' + y2
          + '" role="button" tabindex="0" style="cursor:pointer;">' + (P[x][y2] ? 'T' : 'F') + '</td>';
      }
      h += '</tr>';
    }
    grid.innerHTML = h + '</tbody></table>';
  }

  function paintVerdicts() {
    var rows = [
      ['∀x ∀y P(x, y)', forallForall(), 'every pair'],
      ['∀x ∃y P(x, y)', forallExists(), 'each x gets its own y'],
      ['∃x ∀y P(x, y)', existsForall(), 'one x works for all y'],
      ['∃x ∃y P(x, y)', existsExists(), 'some pair']
    ];
    var h = '<thead><tr><th>statement</th><th>value</th><th>reads as</th><th>decided by</th></tr></thead><tbody>';
    rows.forEach(function (r) {
      h += '<tr><td>' + r[0] + '</td><td class="' + (r[1].v ? 't' : 'f') + '">' + (r[1].v ? 'T' : 'F')
        + '</td><td>' + r[2] + '</td><td>' + r[1].why + '</td></tr>';
    });
    verdicts.innerHTML = h + '</tbody></table>';
    var fe = forallExists(), ef = existsForall();
    if (fe.v && !ef.v) {
      status.innerHTML = '<strong>This is the case that settles the order question.</strong> '
        + '∀x∃y is true and ∃x∀y is false: every x has a partner, but there is no '
        + 'single y that serves them all. Swapping two quantifiers changes what is claimed.';
    } else if (fe.v && ef.v) {
      status.innerHTML = 'Both ∀x∃y and ∃x∀y hold here. That is allowed &mdash; ∃x∀y '
        + 'implies ∀x∃y always &mdash; so this grid does not separate them. Try the successor preset.';
    } else if (!fe.v) {
      status.innerHTML = '∀x∃y already fails (' + fe.why + '), so ∃x∀y cannot hold either: '
        + 'the stronger statement implies the weaker one, never the other way round.';
    }
  }

  function redraw() { paintGrid(); paintVerdicts(); }

  grid.addEventListener('click', function (e) {
    var td = e.target.closest('td[data-x]');
    if (!td) return;
    var x = +td.dataset.x, y = +td.dataset.y;
    P[x][y] = !P[x][y];
    redraw();
  });
  grid.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var td = e.target.closest('td[data-x]');
    if (!td) return;
    e.preventDefault();
    P[+td.dataset.x][+td.dataset.y] = !P[+td.dataset.x][+td.dataset.y];
    redraw();
  });
  preset.addEventListener('change', function () { fill(PRESETS[preset.value]); redraw(); });
  document.getElementById('qClear').addEventListener('click', function () { fill(PRESETS.none); redraw(); });
  document.getElementById('qFlip').addEventListener('click', function () {
    for (var x = 0; x < QN; x += 1) for (var y = 0; y < QN; y += 1) P[x][y] = !P[x][y];
    redraw();
  });

  fill(PRESETS[""" + '"%s"' % cfg.get("preset", "succ") + r"""]);
  preset.value = """ + '"%s"' % cfg.get("preset", "succ") + r""";
  redraw();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Quantifier order",
        subtitle="A finite universe you can edit",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Edit the predicate"),
        panel_intro=cfg.get(
            "panel_intro",
            "Every verdict below is recomputed by walking the grid you can see, "
            "so nothing here depends on trusting the wording of a rule.",
        ),
        script=script,
    )
