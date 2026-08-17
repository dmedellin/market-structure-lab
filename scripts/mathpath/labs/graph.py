"""Lab for course 7: graphs and trees."""

from .common import Lab, cfg_literal


def graph_lab(cfg):
    """One editable graph, and every algorithm in the course run against it.

    The graph is the reader's: they add and remove edges and the whole panel
    re-derives. That matters more here than anywhere else on the path, because
    almost every theorem in graph theory is a claim about ALL graphs, and the
    fastest way to understand one is to try to break it. The handshake theorem
    holds no matter what you draw; Euler's condition fails the moment you give a
    third vertex odd degree; a graph stops being bipartite exactly when you
    close an odd cycle. Each of those is checked here by running the definition.

    Edge weights are a function of the endpoints, w(i, j) = ((7i + 13j) mod 9) + 1,
    so they are deterministic and reproducible: two readers who build the same
    graph get the same minimum spanning tree.
    """
    markup = """      <div class="lab-toolbar">
        <div class="lab-title"><strong>Build a graph, run the algorithms</strong><span id="gCaption">Click a cell in the adjacency matrix to toggle an edge</span></div>
        <div class="inline-legend"><span class="tone-cyan"><i class="legend-swatch"></i>in the result</span><span class="tone-amber"><i class="legend-swatch"></i>visited / root</span><span class="tone-muted"><i class="legend-swatch"></i>not used</span></div>
      </div>
      <div class="lab-stage">
        <svg id="gPlot" viewBox="0 0 460 300" role="img" aria-label="A graph drawn with its vertices evenly spaced on a circle and its edges as straight lines."></svg>
      </div>
      <div class="grid-2" style="margin-top:12px;">
        <div class="table-wrap"><table class="tt" id="gMatrix"></table></div>
        <div class="table-wrap"><table class="tt" id="gFacts"></table></div>
      </div>
      <div class="status-banner" id="gStatus" style="margin-top:12px;"></div>"""
    controls = """        <div class="field">
          <label for="gAlgo">Algorithm</label>
          <select id="gAlgo">
            <option value="degree">Degrees and the handshake theorem</option>
            <option value="components">Connected components</option>
            <option value="bfs">Breadth-first search from vertex 1</option>
            <option value="dfs">Depth-first search from vertex 1</option>
            <option value="path">Shortest path 1 &rarr; last (unweighted)</option>
            <option value="dijkstra">Dijkstra 1 &rarr; last (weighted)</option>
            <option value="bipartite">Bipartite test / 2-colouring</option>
            <option value="euler">Euler path and circuit</option>
            <option value="hamilton">Hamilton path and circuit</option>
            <option value="tree">Is it a tree?</option>
            <option value="spanning">Spanning tree (BFS)</option>
            <option value="mst">Minimum spanning tree (Kruskal)</option>
            <option value="colour">Greedy colouring</option>
            <option value="walks">Walk counts from A<sup>k</sup></option>
          </select>
        </div>
        <div class="field">
          <label for="gPreset">Preset graph</label>
          <select id="gPreset">
            <option value="path">Path</option>
            <option value="cycle">Cycle</option>
            <option value="complete">Complete K&#8345;</option>
            <option value="star">Star</option>
            <option value="bipartite">Complete bipartite</option>
            <option value="tree">Tree</option>
            <option value="petersen">Two triangles joined</option>
            <option value="empty">No edges</option>
          </select>
        </div>
        <div>
          <div class="range-row"><label class="small-copy" for="gN">Vertices</label><span class="range-value" id="gNOut">6</span></div>
          <input id="gN" type="range" min="3" max="8" value="6" />
        </div>
        <div class="kpi-grid">
          <div class="kpi"><span>|V|</span><strong id="gV">&mdash;</strong></div>
          <div class="kpi"><span>|E|</span><strong id="gE">&mdash;</strong></div>
          <div class="kpi"><span>Σ deg</span><strong id="gSum">&mdash;</strong></div>
        </div>"""

    script = r"""
  var N = 6, A = [];
  var algoSel = document.getElementById('gAlgo'), presetSel = document.getElementById('gPreset');
  var nS = document.getElementById('gN');
  var plot = document.getElementById('gPlot'), matrix = document.getElementById('gMatrix');
  var facts = document.getElementById('gFacts'), status = document.getElementById('gStatus');

  function blank(n) {
    var M = [];
    for (var i = 0; i < n; i += 1) { var r = []; for (var j = 0; j < n; j += 1) r.push(0); M.push(r); }
    return M;
  }
  function link(M, i, j) { if (i !== j) { M[i][j] = 1; M[j][i] = 1; } }
  function weight(i, j) { var a = Math.min(i, j), b = Math.max(i, j); return ((7 * a + 13 * b) % 9) + 1; }

  var PRESETS = {
    path: function (n) { var M = blank(n); for (var i = 0; i + 1 < n; i += 1) link(M, i, i + 1); return M; },
    cycle: function (n) { var M = blank(n); for (var i = 0; i < n; i += 1) link(M, i, (i + 1) % n); return M; },
    complete: function (n) { var M = blank(n); for (var i = 0; i < n; i += 1) for (var j = i + 1; j < n; j += 1) link(M, i, j); return M; },
    star: function (n) { var M = blank(n); for (var i = 1; i < n; i += 1) link(M, 0, i); return M; },
    bipartite: function (n) {
      var M = blank(n), half = Math.floor(n / 2);
      for (var i = 0; i < half; i += 1) for (var j = half; j < n; j += 1) link(M, i, j);
      return M;
    },
    tree: function (n) { var M = blank(n); for (var i = 1; i < n; i += 1) link(M, i, Math.floor((i - 1) / 2)); return M; },
    petersen: function (n) {
      var M = blank(n);
      for (var i = 0; i + 2 < n && i < 3; i += 1) link(M, i, (i + 1) % 3);
      if (n >= 6) { link(M, 3, 4); link(M, 4, 5); link(M, 5, 3); link(M, 0, 3); }
      return M;
    },
    empty: function (n) { return blank(n); }
  };

  function edges() {
    var out = [];
    for (var i = 0; i < N; i += 1) for (var j = i + 1; j < N; j += 1) if (A[i][j]) out.push([i, j, weight(i, j)]);
    return out;
  }
  function degree(v) { var d = 0; for (var j = 0; j < N; j += 1) d += A[v][j]; return d; }
  function neighbours(v) { var out = []; for (var j = 0; j < N; j += 1) if (A[v][j]) out.push(j); return out; }

  function componentsOf() {
    var seen = new Array(N).fill(false), comps = [];
    for (var s = 0; s < N; s += 1) {
      if (seen[s]) continue;
      var stack = [s], comp = [];
      seen[s] = true;
      while (stack.length) {
        var v = stack.pop(); comp.push(v);
        neighbours(v).forEach(function (u) { if (!seen[u]) { seen[u] = true; stack.push(u); } });
      }
      comps.push(comp.sort(function (a, b) { return a - b; }));
    }
    return comps;
  }

  function bfs(start) {
    var dist = new Array(N).fill(-1), parent = new Array(N).fill(-1), order = [];
    dist[start] = 0;
    var queue = [start];
    while (queue.length) {
      var v = queue.shift();
      order.push(v);
      neighbours(v).forEach(function (u) {
        if (dist[u] === -1) { dist[u] = dist[v] + 1; parent[u] = v; queue.push(u); }
      });
    }
    return { dist: dist, parent: parent, order: order };
  }

  function dfs(start) {
    var seen = new Array(N).fill(false), order = [], parent = new Array(N).fill(-1);
    (function visit(v) {
      seen[v] = true; order.push(v);
      neighbours(v).forEach(function (u) { if (!seen[u]) { parent[u] = v; visit(u); } });
    })(start);
    return { order: order, parent: parent };
  }

  function dijkstra(start) {
    var dist = new Array(N).fill(Infinity), parent = new Array(N).fill(-1), done = new Array(N).fill(false);
    dist[start] = 0;
    for (var it = 0; it < N; it += 1) {
      var best = -1;
      for (var v = 0; v < N; v += 1) if (!done[v] && dist[v] < Infinity && (best === -1 || dist[v] < dist[best])) best = v;
      if (best === -1) break;
      done[best] = true;
      neighbours(best).forEach(function (u) {
        var alt = dist[best] + weight(best, u);
        if (alt < dist[u]) { dist[u] = alt; parent[u] = best; }
      });
    }
    return { dist: dist, parent: parent };
  }

  function twoColour() {
    var colour = new Array(N).fill(-1), conflict = null;
    for (var s = 0; s < N; s += 1) {
      if (colour[s] !== -1) continue;
      colour[s] = 0;
      var queue = [s];
      while (queue.length) {
        var v = queue.shift();
        var nb = neighbours(v);
        for (var k = 0; k < nb.length; k += 1) {
          var u = nb[k];
          if (colour[u] === -1) { colour[u] = 1 - colour[v]; queue.push(u); }
          else if (colour[u] === colour[v] && !conflict) conflict = [v, u];
        }
      }
    }
    return { colour: colour, conflict: conflict };
  }

  function greedyColour() {
    var colour = new Array(N).fill(-1);
    for (var v = 0; v < N; v += 1) {
      var used = {};
      neighbours(v).forEach(function (u) { if (colour[u] !== -1) used[colour[u]] = true; });
      var c = 0;
      while (used[c]) c += 1;
      colour[v] = c;
    }
    return colour;
  }

  function kruskal() {
    var es = edges().slice().sort(function (a, b) { return a[2] - b[2] || a[0] - b[0] || a[1] - b[1]; });
    var parent = [];
    for (var i = 0; i < N; i += 1) parent.push(i);
    function find(x) { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; }
    var chosen = [], total = 0, considered = [];
    es.forEach(function (e) {
      var a = find(e[0]), b = find(e[1]);
      if (a === b) { considered.push([e, false]); return; }
      parent[a] = b;
      chosen.push(e); total += e[2];
      considered.push([e, true]);
    });
    return { chosen: chosen, total: total, considered: considered };
  }

  /* Hamilton by exhaustive search. n is capped at 8, so 8! = 40320 permutations
     is instant -- and the cap is itself the lesson: this is the algorithm that
     does not scale, and course 8 comes back to why. */
  function hamilton() {
    var best = null, bestCircuit = null;
    var used = new Array(N).fill(false);
    function walk(path) {
      if (path.length === N) {
        if (!best) best = path.slice();
        if (A[path[path.length - 1]][path[0]] && !bestCircuit) bestCircuit = path.slice();
        return;
      }
      for (var v = 0; v < N; v += 1) {
        if (used[v]) continue;
        if (path.length && !A[path[path.length - 1]][v]) continue;
        used[v] = true; path.push(v);
        walk(path);
        path.pop(); used[v] = false;
        if (best && bestCircuit) return;
      }
    }
    walk([]);
    return { path: best, circuit: bestCircuit };
  }

  function matrixPower(k) {
    var M = A.map(function (r) { return r.slice(); });
    for (var step = 1; step < k; step += 1) {
      var out = blank(N);
      for (var i = 0; i < N; i += 1) for (var j = 0; j < N; j += 1) {
        var s = 0;
        for (var t = 0; t < N; t += 1) s += M[i][t] * A[t][j];
        out[i][j] = s;
      }
      M = out;
    }
    return M;
  }

  /* --- drawing ---------------------------------------------------------- */
  function positions() {
    var pts = [];
    for (var i = 0; i < N; i += 1) {
      var ang = -Math.PI / 2 + (2 * Math.PI * i) / N;
      pts.push([230 + 105 * Math.cos(ang), 150 + 105 * Math.sin(ang)]);
    }
    return pts;
  }

  function draw(highlightEdges, vertexColours, labels) {
    var pts = positions(), s = '';
    var hi = {};
    (highlightEdges || []).forEach(function (e) { hi[Math.min(e[0], e[1]) + '-' + Math.max(e[0], e[1])] = true; });
    var weighted = algoSel.value === 'dijkstra' || algoSel.value === 'mst';
    edges().forEach(function (e) {
      var on = hi[e[0] + '-' + e[1]];
      s += '<line x1="' + pts[e[0]][0] + '" y1="' + pts[e[0]][1] + '" x2="' + pts[e[1]][0] + '" y2="' + pts[e[1]][1]
        + '" stroke="' + (on ? 'var(--cyan)' : 'var(--line-strong)') + '" stroke-width="' + (on ? 3.4 : 1.8) + '" />';
      if (weighted) {
        var mx = (pts[e[0]][0] + pts[e[1]][0]) / 2, my = (pts[e[0]][1] + pts[e[1]][1]) / 2;
        s += '<circle cx="' + mx + '" cy="' + my + '" r="9" fill="var(--panel-solid)" stroke="var(--line)" />';
        s += '<text x="' + mx + '" y="' + (my + 4) + '" text-anchor="middle" font-size="10" fill="'
          + (on ? 'var(--cyan)' : 'var(--muted)') + '" font-weight="700">' + e[2] + '</text>';
      }
    });
    var PALETTE = ['var(--cyan)', 'var(--purple)', 'var(--amber)', 'var(--green)', 'var(--red)', 'var(--blue)'];
    for (var i = 0; i < N; i += 1) {
      var c = vertexColours && vertexColours[i] !== undefined && vertexColours[i] !== -1
        ? PALETTE[vertexColours[i] % PALETTE.length] : 'var(--panel-3)';
      s += '<circle cx="' + pts[i][0] + '" cy="' + pts[i][1] + '" r="17" fill="' + c
        + '" stroke="var(--line-strong)" stroke-width="2" />';
      var label = labels && labels[i] !== undefined ? labels[i] : (i + 1);
      s += '<text x="' + pts[i][0] + '" y="' + (pts[i][1] + 5) + '" text-anchor="middle" font-size="13" font-weight="800" fill="'
        + (vertexColours && vertexColours[i] !== undefined && vertexColours[i] !== -1 ? 'var(--on-accent)' : 'var(--text)')
        + '">' + label + '</text>';
    }
    plot.innerHTML = s;
  }

  function paintMatrix(power) {
    var M = power ? matrixPower(power) : A;
    var h = '<caption>' + (power ? 'A^' + power + ' — entry (i, j) counts walks of length ' + power : 'adjacency matrix A — click to toggle')
      + '</caption><thead><tr><th></th>';
    for (var j = 1; j <= N; j += 1) h += '<th>' + j + '</th>';
    h += '</tr></thead><tbody>';
    for (var i = 0; i < N; i += 1) {
      h += '<tr><th class="rowhead">' + (i + 1) + '</th>';
      for (var j2 = 0; j2 < N; j2 += 1) {
        h += '<td class="' + (M[i][j2] ? 'on' : '') + '" data-i="' + i + '" data-j="' + j2
          + '" role="button" tabindex="0" style="cursor:pointer;">' + M[i][j2] + '</td>';
      }
      h += '</tr>';
    }
    matrix.innerHTML = h + '</tbody>';
  }

  function factRows(rows) {
    facts.innerHTML = '<thead><tr><th>quantity</th><th>value</th></tr></thead><tbody>'
      + rows.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'; }).join('')
      + '</tbody>';
  }

  var ALGOS = {
    degree: function () {
      var degs = [], sum = 0, odd = [];
      for (var v = 0; v < N; v += 1) { var d = degree(v); degs.push(d); sum += d; if (d % 2) odd.push(v + 1); }
      draw([], null, degs);
      factRows([
        ['degree sequence', degs.slice().sort(function (a, b) { return b - a; }).join(', ')],
        ['Σ deg(v)', sum],
        ['2|E|', 2 * edges().length],
        ['vertices of odd degree', odd.length ? odd.join(', ') : 'none']
      ]);
      status.innerHTML = 'Each vertex is labelled with its degree. Σ deg(v) = <strong>' + sum
        + '</strong> and 2|E| = <strong>' + (2 * edges().length) + '</strong> — equal, as the handshake theorem '
        + 'requires, because every edge contributes exactly 2 to the total. There are <strong>' + odd.length
        + '</strong> vertices of odd degree, and that number is always even: it cannot be otherwise, since '
        + 'the total is even.';
    },
    components: function () {
      var comps = componentsOf(), colour = new Array(N).fill(0);
      comps.forEach(function (c, i) { c.forEach(function (v) { colour[v] = i; }); });
      draw(edges(), colour);
      factRows([
        ['components', comps.length],
        ['sizes', comps.map(function (c) { return c.length; }).join(', ')],
        ['connected', comps.length === 1 ? 'yes' : 'no']
      ]);
      status.innerHTML = comps.length === 1
        ? 'One component: every vertex reaches every other. A graph on ' + N + ' vertices needs at least '
          + (N - 1) + ' edges to be connected, and this one has ' + edges().length + '.'
        : '<strong>' + comps.length + ' components:</strong> ' + comps.map(function (c) {
            return '{' + c.map(function (v) { return v + 1; }).join(', ') + '}';
          }).join(', ') + '. No path crosses between them, so no walk, no matter how long, joins two of these sets.';
    },
    bfs: function () {
      var r = bfs(0), used = [];
      for (var v = 0; v < N; v += 1) if (r.parent[v] !== -1) used.push([r.parent[v], v]);
      draw(used, null, r.dist.map(function (d) { return d === -1 ? '∞' : d; }));
      factRows([
        ['visit order', r.order.map(function (v) { return v + 1; }).join(' → ')],
        ['unreachable', r.dist.filter(function (d) { return d === -1; }).length],
        ['eccentricity of 1', Math.max.apply(null, r.dist)]
      ]);
      status.innerHTML = 'Labels are distances from vertex 1 in EDGES, not in geometry. Breadth-first search '
        + 'settles every vertex at distance k before any at distance k+1, which is exactly why its tree gives '
        + 'shortest paths in an unweighted graph — and why the same argument fails once edges have weights.';
    },
    dfs: function () {
      var r = dfs(0), used = [];
      for (var v = 0; v < N; v += 1) if (r.parent[v] !== -1) used.push([r.parent[v], v]);
      var pos = new Array(N).fill('—');
      r.order.forEach(function (v, i) { pos[v] = i + 1; });
      draw(used, null, pos);
      factRows([
        ['visit order', r.order.map(function (v) { return v + 1; }).join(' → ')],
        ['visited', r.order.length + ' of ' + N],
        ['tree edges', used.length]
      ]);
      status.innerHTML = 'Labels are the ORDER of first visit. Depth-first search follows one branch as far as it '
        + 'goes before backtracking, so its tree is deep and narrow where breadth-first search is wide and shallow. '
        + 'Both visit every vertex of the component; neither is a shortest-path algorithm in a weighted graph.';
    },
    path: function () {
      var r = bfs(0), target = N - 1, used = [], route = [];
      if (r.dist[target] !== -1) {
        var v = target;
        while (v !== -1) { route.unshift(v); if (r.parent[v] !== -1) used.push([r.parent[v], v]); v = r.parent[v]; }
      }
      draw(used, null, null);
      factRows([
        ['from → to', '1 → ' + N],
        ['distance (edges)', r.dist[target] === -1 ? 'unreachable' : r.dist[target]],
        ['route', route.length ? route.map(function (v) { return v + 1; }).join(' → ') : '—']
      ]);
      status.innerHTML = r.dist[target] === -1
        ? 'Vertex ' + N + ' is unreachable from vertex 1: they lie in different components.'
        : 'Shortest route uses <strong>' + r.dist[target] + '</strong> edges. In an unweighted graph "shortest" '
          + 'means fewest edges, and breadth-first search finds it without looking at any other path.';
    },
    dijkstra: function () {
      var r = dijkstra(0), target = N - 1, used = [], route = [];
      if (r.dist[target] < Infinity) {
        var v = target;
        while (v !== -1) { route.unshift(v); if (r.parent[v] !== -1) used.push([r.parent[v], v]); v = r.parent[v]; }
      }
      var bfsr = bfs(0);
      draw(used, null, r.dist.map(function (d) { return d === Infinity ? '∞' : d; }));
      factRows([
        ['weighted distance', r.dist[target] === Infinity ? 'unreachable' : r.dist[target]],
        ['route', route.length ? route.map(function (v) { return v + 1; }).join(' → ') : '—'],
        ['edges used', route.length ? route.length - 1 : 0],
        ['fewest-edge distance', bfsr.dist[target] === -1 ? '—' : bfsr.dist[target]]
      ]);
      var differs = route.length > 1 && bfsr.dist[target] !== -1 && (route.length - 1) !== bfsr.dist[target];
      status.innerHTML = 'Labels are total WEIGHT from vertex 1. '
        + (differs
            ? '<strong>The cheapest route uses ' + (route.length - 1) + ' edges while the shortest uses '
              + bfsr.dist[target] + '.</strong> That gap is the whole reason Dijkstra exists: counting edges and '
              + 'adding weights are different questions.'
            : 'Here the cheapest route happens to use the fewest edges too. Toggle an edge to break that — '
              + 'the two answers coincide only by accident.');
    },
    bipartite: function () {
      var r = twoColour();
      draw(edges(), r.conflict ? null : r.colour);
      var sides = [[], []];
      if (!r.conflict) for (var v = 0; v < N; v += 1) sides[r.colour[v]].push(v + 1);
      factRows([
        ['bipartite', r.conflict ? 'no' : 'yes'],
        ['part X', r.conflict ? '—' : '{' + sides[0].join(', ') + '}'],
        ['part Y', r.conflict ? '—' : '{' + sides[1].join(', ') + '}'],
        ['conflict', r.conflict ? 'vertices ' + (r.conflict[0] + 1) + ' and ' + (r.conflict[1] + 1) : 'none']
      ]);
      status.innerHTML = r.conflict
        ? '<strong>Not bipartite.</strong> Vertices ' + (r.conflict[0] + 1) + ' and ' + (r.conflict[1] + 1)
          + ' are adjacent and the 2-colouring forced them the same colour, which means an ODD cycle passes '
          + 'through them. A graph is bipartite exactly when it has no odd cycle — nothing else can obstruct it.'
        : '<strong>Bipartite.</strong> The two colours are a partition into independent sets, and every edge '
          + 'crosses between them. Equivalently: every cycle in this graph has even length.';
    },
    euler: function () {
      var odd = [];
      for (var v = 0; v < N; v += 1) if (degree(v) % 2) odd.push(v + 1);
      var comps = componentsOf().filter(function (c) { return c.some(function (v) { return degree(v) > 0; }); });
      var connected = comps.length <= 1;
      var circuit = connected && odd.length === 0 && edges().length > 0;
      var pathOnly = connected && odd.length === 2;
      draw(edges(), null, null);
      factRows([
        ['odd-degree vertices', odd.length ? odd.join(', ') + ' (' + odd.length + ')' : 'none'],
        ['edges connected', connected ? 'yes' : 'no'],
        ['Euler circuit', circuit ? 'yes' : 'no'],
        ['Euler path', circuit || pathOnly ? 'yes' : 'no']
      ]);
      status.innerHTML = circuit
        ? '<strong>An Euler circuit exists.</strong> Every vertex has even degree and the edges form one connected '
          + 'piece — that is the complete criterion, and it is checkable in one pass over the degrees.'
        : pathOnly
          ? '<strong>An Euler path exists but no circuit.</strong> Exactly two vertices have odd degree (' + odd.join(' and ')
            + '), and any Euler path must start at one and end at the other.'
          : '<strong>Neither.</strong> ' + (connected
              ? 'There are ' + odd.length + ' odd-degree vertices; an Euler path allows 0 or 2 and nothing else, '
                + 'because every visit to a vertex uses two edge-ends.'
              : 'The edges are not all in one component, so no single walk can cover them.');
    },
    hamilton: function () {
      var r = hamilton();
      var used = [];
      var seq = r.circuit || r.path;
      if (seq) for (var i = 0; i + 1 < seq.length; i += 1) used.push([seq[i], seq[i + 1]]);
      if (r.circuit) used.push([seq[seq.length - 1], seq[0]]);
      draw(used, null, null);
      factRows([
        ['Hamilton path', r.path ? r.path.map(function (v) { return v + 1; }).join(' → ') : 'none'],
        ['Hamilton circuit', r.circuit ? r.circuit.map(function (v) { return v + 1; }).join(' → ') + ' → ' + (r.circuit[0] + 1) : 'none'],
        ['search space', N + '! = ' + (function () { var f = 1; for (var i = 2; i <= N; i += 1) f *= i; return f; })() + ' orderings']
      ]);
      status.innerHTML = (r.circuit
          ? '<strong>A Hamilton circuit exists.</strong> '
          : r.path ? '<strong>A Hamilton path exists, but no circuit.</strong> ' : '<strong>Neither exists.</strong> ')
        + 'Note how it was found: by trying orderings until one worked. Unlike the Euler condition, which is a '
        + 'one-pass check on degrees, no simple criterion decides this — deciding it in general is NP-complete, '
        + 'which is why the vertex count here stops at 8.';
    },
    tree: function () {
      var comps = componentsOf(), E = edges().length;
      var connected = comps.length === 1;
      var isTree = connected && E === N - 1;
      draw(edges(), null, null);
      var leaves = [];
      for (var v = 0; v < N; v += 1) if (degree(v) === 1) leaves.push(v + 1);
      factRows([
        ['|V|', N], ['|E|', E], ['|V| − 1', N - 1],
        ['connected', connected ? 'yes' : 'no'],
        ['acyclic', E <= N - comps.length ? 'yes' : 'no'],
        ['tree', isTree ? 'yes' : 'no'],
        ['leaves', leaves.length ? leaves.join(', ') : 'none']
      ]);
      status.innerHTML = isTree
        ? '<strong>A tree.</strong> Connected with exactly ' + (N - 1) + ' edges — and for a connected graph those '
          + 'two conditions force each other: one more edge creates a cycle, one fewer disconnects it. Every pair '
          + 'of vertices is joined by exactly one path.'
        : connected
          ? 'Connected but not a tree: ' + E + ' edges where a tree on ' + N + ' vertices has exactly ' + (N - 1)
            + '. The extra ' + (E - (N - 1)) + ' edge(s) close cycles.'
          : 'Not a tree: not connected. With ' + comps.length + ' components and ' + E + ' edges, it is a forest '
            + (E === N - comps.length ? '(acyclic)' : 'with at least one cycle') + '.';
    },
    spanning: function () {
      var r = bfs(0), used = [];
      for (var v = 0; v < N; v += 1) if (r.parent[v] !== -1) used.push([r.parent[v], v]);
      var reached = r.order.length;
      draw(used, null, null);
      factRows([
        ['tree edges', used.length],
        ['vertices spanned', reached + ' of ' + N],
        ['edges left out', edges().length - used.length]
      ]);
      status.innerHTML = reached === N
        ? 'A spanning tree: <strong>' + used.length + ' edges reaching all ' + N + ' vertices</strong>, which is '
          + N + ' − 1 exactly. Every connected graph has one, and the ' + (edges().length - used.length)
          + ' edges left out are precisely the ones that would close a cycle.'
        : 'No spanning tree exists: the graph is disconnected, so a search from vertex 1 reaches only '
          + reached + ' of ' + N + ' vertices. What you get is a spanning tree of one COMPONENT.';
    },
    mst: function () {
      var r = kruskal(), rows = [];
      r.considered.forEach(function (c) {
        rows.push([(c[0][0] + 1) + '–' + (c[0][1] + 1) + ' (w ' + c[0][2] + ')', c[1] ? 'taken' : 'rejected: closes a cycle']);
      });
      draw(r.chosen, null, null);
      factRows([['total weight', r.total], ['edges chosen', r.chosen.length + ' of ' + edges().length]].concat(rows.slice(0, 8)));
      status.innerHTML = r.chosen.length === N - 1
        ? 'Kruskal takes edges in increasing weight and skips any that would close a cycle. Total weight '
          + '<strong>' + r.total + '</strong>. The greedy choice is provably optimal here — which is unusual, '
          + 'and course 8 explains what makes this problem yield to greed when most do not.'
        : 'The graph is disconnected, so Kruskal produces a minimum spanning FOREST: '
          + r.chosen.length + ' edges, weight ' + r.total + '. No set of edges can span a disconnected graph.';
    },
    colour: function () {
      var colour = greedyColour();
      var used = Math.max.apply(null, colour) + 1;
      var maxDeg = 0;
      for (var v = 0; v < N; v += 1) maxDeg = Math.max(maxDeg, degree(v));
      var clique = twoColour().conflict ? 3 : 2;
      draw(edges(), colour);
      factRows([
        ['colours used (greedy)', used],
        ['max degree Δ', maxDeg],
        ['Brooks-style bound Δ + 1', maxDeg + 1],
        ['bipartite (2-colourable)', twoColour().conflict ? 'no' : 'yes']
      ]);
      status.innerHTML = 'Greedy colouring in vertex order used <strong>' + used + '</strong> colour'
        + (used === 1 ? '' : 's') + '. It never needs more than Δ + 1 = ' + (maxDeg + 1)
        + ', but it is not optimal in general: the order it visits vertices in can cost it colours, and finding '
        + 'the true chromatic number is NP-hard.';
    },
    walks: function () {
      draw(edges(), null, null);
      paintMatrix(2);
      var M2 = matrixPower(2), M3 = matrixPower(3);
      var closed3 = 0;
      for (var v = 0; v < N; v += 1) closed3 += M3[v][v];
      factRows([
        ['A²[1][1] = deg(1)', M2[0][0]],
        ['walks of length 2 from 1 to ' + N, M2[0][N - 1]],
        ['walks of length 3 from 1 to ' + N, M3[0][N - 1]],
        ['Σ A³[v][v]', closed3 + ' = 6 × (number of triangles) = ' + (closed3 / 6)]
      ]);
      status.innerHTML = 'The matrix above is A², whose (i, j) entry counts walks of length 2 from i to j — '
        + 'a fact that follows from how matrix multiplication sums over the middle vertex. The diagonal of A³ '
        + 'counts closed walks of length 3, and each triangle contributes 6 of them (3 starting points × 2 directions), '
        + 'so this graph has <strong>' + (closed3 / 6) + '</strong> triangle(s).';
    }
  };

  function redraw() {
    document.getElementById('gNOut').textContent = nS.value;
    document.getElementById('gV').textContent = N;
    document.getElementById('gE').textContent = edges().length;
    var sum = 0;
    for (var v = 0; v < N; v += 1) sum += degree(v);
    document.getElementById('gSum').textContent = sum;
    if (algoSel.value !== 'walks') paintMatrix(0);
    ALGOS[algoSel.value]();
  }

  function rebuild() {
    N = +nS.value;
    A = PRESETS[presetSel.value](N);
    redraw();
  }

  matrix.addEventListener('click', function (e) {
    var td = e.target.closest('td[data-i]');
    if (!td || algoSel.value === 'walks') return;
    var i = +td.dataset.i, j = +td.dataset.j;
    if (i === j) return;
    A[i][j] = A[i][j] ? 0 : 1;
    A[j][i] = A[i][j];
    redraw();
  });
  matrix.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var td = e.target.closest('td[data-i]');
    if (!td || algoSel.value === 'walks') return;
    e.preventDefault();
    var i = +td.dataset.i, j = +td.dataset.j;
    if (i === j) return;
    A[i][j] = A[i][j] ? 0 : 1;
    A[j][i] = A[i][j];
    redraw();
  });
  algoSel.addEventListener('change', redraw);
  presetSel.addEventListener('change', rebuild);
  nS.addEventListener('input', rebuild);

  algoSel.value = """ + '"%s"' % cfg.get("algo", "degree") + r""";
  presetSel.value = """ + '"%s"' % cfg.get("preset", "cycle") + r""";
  nS.value = """ + str(cfg.get("n", 6)) + r""";
  rebuild();
  window.redrawLab = redraw;
"""
    return Lab(
        title="Graph workbench",
        subtitle="Your graph, the course's algorithms",
        markup=markup,
        controls=controls,
        panel_title=cfg.get("panel_title", "Build and analyse"),
        panel_intro=cfg.get(
            "panel_intro",
            "Toggle any cell of the adjacency matrix and everything re-derives. "
            "Try to break the theorem the lesson just stated; that is the fastest "
            "way to see what it actually rules out.",
        ),
        script=script,
    )
