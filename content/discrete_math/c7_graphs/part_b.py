"""Course 7, lessons 08-14 — search, paths, trees, colouring, planarity."""

LESSONS = [
    # ---------------------------------------------------------------- 08
    {
        "slug": "graph-traversal",
        "title": "Breadth-First and Depth-First Search",
        "module": "Traversal",
        "one_line": "Two ways to visit everything, with different shapes and different uses.",
        "summary": (
            "Breadth-first search settles vertices in order of distance and therefore "
            "finds shortest paths in an unweighted graph. Depth-first goes as deep as "
            "possible first and is what detects cycles and orders dependencies."
        ),
        "key": [
            "BFS  queue   visits by increasing distance   ⟹  shortest paths (unweighted)",
            "DFS  stack   follows one branch to the end   ⟹  cycles, components, ordering",
            "both cost Θ(n + |E|) with adjacency lists",
            "each produces a SPANNING TREE of its component",
        ],
        "key_label": "Queue or stack",
        "concepts_intro": (
            "The two searches differ in one data structure and produce completely "
            "different trees."
        ),
        "concepts": [
            ("BFS settles by distance",
             "Every vertex at distance `k` is visited before any at distance `k+1`, which "
             "is exactly why its tree gives shortest paths."),
            ("DFS follows one branch to exhaustion",
             "Then backtracks. Its tree is deep and narrow, and the order of backtracking "
             "is what topological sorting uses."),
            ("Both visit every vertex of the component",
             "They differ in order, not in coverage. Both cost `Θ(n + |E|)` with adjacency "
             "lists."),
        ],
        "read_title": "The two searches",
        "read_intro": "Both algorithms, what each guarantees, and where each is used.",
        "body": [
            ("math", [
                "BFS(G, s):",
                "    mark s visited; dist[s] = 0;  queue = [s]",
                "    while queue not empty:",
                "        v = queue.pop_front()",
                "        for each neighbour u of v:",
                "            if u unvisited:",
                "                mark u;  dist[u] = dist[v] + 1;  parent[u] = v",
                "                queue.push_back(u)",
            ]),
            ("thm", ("BFS finds shortest paths",
                     "In an unweighted graph, `dist[v]` after BFS from `s` is the minimum "
                     "number of edges on any `s`&ndash;`v` path.")),
            ("proof", [
                "By induction on the distance. Vertices at distance 0 and 1 are handled "
                "correctly by initialisation and the first round.",
                "Suppose every vertex at true distance `≤ k` is dequeued with the correct "
                "`dist`. A vertex `v` at true distance `k+1` has a neighbour `u` at "
                "distance `k`; when `u` is processed, `v` is either already marked with a "
                "value at most `k+1`, or is marked `k+1` then. It cannot be marked less, "
                "since that would give a shorter path.",
                "The queue therefore holds vertices in non-decreasing distance order "
                "throughout.",
            ]),
            ("p", "The queue is doing the work. Replacing it with a stack gives depth-first "
                  "search, and the distance guarantee vanishes immediately &mdash; DFS may "
                  "reach a neighbour of the start by a long detour and record that depth."),
            ("math", [
                "DFS(G, v):",
                "    mark v visited",
                "    for each neighbour u of v:",
                "        if u unvisited:  parent[u] = v;  DFS(G, u)",
            ]),
            ("h3", "What each is used for"),
            ("math", [
                "BFS                              DFS",
                "shortest paths (unweighted)      cycle detection",
                "level structure / distances      topological sort",
                "bipartiteness testing            strongly connected components",
                "web crawling by depth            maze generation and solving",
                "                                 articulation points and bridges",
            ]),
            ("p", "Both find the components and both produce a spanning tree, and either "
                  "serves for those. The distinctive uses come from the ORDER: BFS knows "
                  "distances, DFS knows the nesting of the recursion, and each of those is "
                  "the key to different problems."),
            ("h3", "Cycle detection with DFS"),
            ("thm", ("Back edges are cycles",
                     "During a depth-first search of an undirected graph, an edge to an "
                     "already-visited vertex that is not the current vertex's parent "
                     "closes a cycle. A graph is acyclic exactly when no such edge is "
                     "found.")),
            ("p", "This is what makes DFS the tool for cycle detection: the search tree "
                  "plus a single back edge exhibits the cycle explicitly. The parent "
                  "exclusion matters &mdash; without it every edge would look like a cycle "
                  "of length 2."),
            ("h3", "Cost"),
            ("p", "Each vertex is marked once and each edge examined twice (once from each "
                  "end), so both searches cost `Θ(n + |E|)` with adjacency lists and "
                  "`Θ(n²)` with a matrix. For a sparse graph that is the difference between "
                  "linear and quadratic, which is lesson 3's trade-off arriving in "
                  "practice."),
        ],
        "lab": ("graph", {
            "algo": "bfs", "preset": "tree", "n": 7,
            "panel_title": "Distances, then order",
            "panel_intro": "In BFS mode the labels are distances from vertex 1. Switch to "
                           "DFS and they become visit order &mdash; and the tree drawn "
                           "changes shape completely on the same graph.",
        }),
        "steps_title": "Running a search",
        "steps_intro": "Choose the structure from the question.",
        "steps": [
            ("Pick BFS for distances",
             "Shortest paths, level structure, bipartiteness. Anything where \"how far\" "
             "matters."),
            ("Pick DFS for structure",
             "Cycles, dependency order, articulation points. Anything where the nesting of "
             "the search matters."),
            ("Mark on discovery, not on processing",
             "Marking a vertex when it is added to the queue prevents it being added "
             "twice. Marking on removal is the classic bug."),
            ("Repeat from unvisited vertices",
             "One search covers one component. A full traversal loops over starting "
             "points."),
        ],
        "worked": {
            "title": "Both searches on one graph",
            "intro": ["Vertices 1–6; edges 1–2, 1–3, 2–4, 3–4, 4–5, 5–6."],
            "lines": [
                "BFS from 1 (queue):",
                "   visit 1        dist 0",
                "   visit 2, 3     dist 1",
                "   visit 4        dist 2      (reached from 2)",
                "   visit 5        dist 3",
                "   visit 6        dist 4",
                "   order: 1 2 3 4 5 6        tree edges: 1–2, 1–3, 2–4, 4–5, 5–6",
                "",
                "DFS from 1 (stack / recursion):",
                "   1 → 2 → 4 → 3   (3 is a dead end, backtrack)",
                "         4 → 5 → 6",
                "   order: 1 2 4 3 5 6        tree edges: 1–2, 2–4, 4–3, 4–5, 5–6",
                "",
                "Different trees, same six vertices.  Note DFS reached 3 at depth 3,",
                "although its true distance from 1 is 1.",
            ],
            "after": [
                "That last line is the reason DFS cannot be used for shortest paths. It "
                "found vertex 3 by the route `1→2→4→3`, and the depth it records is a fact "
                "about the search order rather than about the graph. The edge `3–4` is a "
                "back edge and closes the cycle `1–2–4–3–1`."
            ],
        },
        "quiz_title": "Traversal",
        "quiz": [
            {"q": "BFS uses a queue; DFS uses a:",
             "a": ["priority queue", "stack", "heap", "hash table"],
             "c": 1,
             "why": "Last in, first out &mdash; explicitly, or implicitly via recursion. "
                    "That single change produces a completely different tree."},
            {"q": "Which finds shortest paths in an unweighted graph?",
             "a": ["DFS", "BFS", "both", "neither"],
             "c": 1,
             "why": "BFS settles vertices in non-decreasing distance order. DFS may reach "
                    "a near vertex by a long detour."},
            {"q": "Both searches cost, with adjacency lists:",
             "a": ["`Θ(n²)`", "`Θ(n + |E|)`", "`Θ(|E|²)`", "exponential"],
             "c": 1,
             "why": "Each vertex is marked once and each edge examined from both ends."},
        ],
        "mistakes": [
            ("Using DFS for shortest paths",
             "The depth it records is an artefact of the search order. Only BFS guarantees "
             "distance."),
            ("Marking vertices on removal rather than on discovery",
             "A vertex can then be queued several times before it is processed, which "
             "breaks both the cost bound and the distance guarantee."),
            ("Forgetting to exclude the parent in cycle detection",
             "Otherwise every edge looks like a cycle back to where you came from."),
        ],
        "standard": ("Finish when you can predict both visit orders on a small graph.",
                     "Take a graph on seven vertices, write out the BFS and DFS orders by "
                     "hand, and mark the tree edges of each. The two trees should look "
                     "nothing alike."),
        "note": "Dijkstra's algorithm in the next lesson is BFS with a priority queue in "
                "place of the queue. The correspondence is exact, and it is why Dijkstra "
                "reduces to BFS when every weight is 1.",
    },
    # ---------------------------------------------------------------- 09
    {
        "slug": "shortest-paths",
        "title": "Shortest Paths and Dijkstra's Algorithm",
        "module": "Traversal",
        "one_line": "Fewest edges is not cheapest route.",
        "summary": (
            "With weights, breadth-first search no longer works. Dijkstra settles "
            "vertices in order of distance from the source, which is correct precisely "
            "because the weights are non-negative."
        ),
        "key": [
            "unweighted: BFS gives shortest paths",
            "weighted:   Dijkstra — settle the nearest unsettled vertex, relax its edges",
            "requires NON-NEGATIVE weights",
            "negative weights ⟹ Bellman–Ford instead",
        ],
        "key_label": "Weights change everything",
        "concepts_intro": (
            "Two different questions &mdash; fewest edges and least total weight &mdash; "
            "and the second needs a different algorithm."
        ),
        "concepts": [
            ("Fewest edges and least weight differ",
             "A two-edge route of weight 20 loses to a five-edge route of weight 8. BFS "
             "answers the wrong question once weights exist."),
            ("Dijkstra settles the nearest unsettled vertex",
             "Once settled, a vertex's distance is final, because any other route would "
             "have to pass through a vertex already known to be further away."),
            ("Non-negativity is essential",
             "A negative edge could make a longer detour cheaper, so a settled vertex "
             "might be improvable &mdash; and Dijkstra never revisits it."),
        ],
        "read_title": "Weighted shortest paths",
        "read_intro": "The algorithm, why it is correct, and where it fails.",
        "body": [
            ("def", ("Weighted graph and path weight",
                     "A <strong>weighted graph</strong> assigns each edge a number. The "
                     "<strong>weight</strong> of a path is the sum of its edge weights, and "
                     "a <strong>shortest path</strong> is one of minimum weight.")),
            ("math", [
                "DIJKSTRA(G, s):",
                "    dist[s] = 0;  dist[v] = ∞ for v ≠ s;  all vertices unsettled",
                "    while some unsettled vertex has finite dist:",
                "        u = unsettled vertex with smallest dist",
                "        settle u",
                "        for each neighbour v of u:",
                "            if dist[u] + w(u,v) < dist[v]:",
                "                dist[v] = dist[u] + w(u,v);  parent[v] = u",
            ]),
            ("thm", ("Correctness",
                     "With non-negative weights, when Dijkstra settles a vertex `u`, "
                     "`dist[u]` is the true shortest distance from `s` to `u`.")),
            ("proof", [
                "By induction on the order of settling. Suppose every previously settled "
                "vertex has its true distance, and consider the moment `u` is chosen.",
                "Take any path `P` from `s` to `u`, and let `x` be its first vertex that is "
                "not yet settled, with predecessor `y` (settled). Then the length of `P` is "
                "at least `dist[y] + w(y,x) ≥ dist[x] ≥ dist[u]`, the last step because `u` "
                "was chosen as the smallest.",
                "The first inequality uses that the remaining part of `P` has non-negative "
                "weight &mdash; which is exactly where the hypothesis enters. So no path "
                "beats `dist[u]`.",
            ]),
            ("p", "The proof names the place non-negativity is used, which is the useful "
                  "way to read it: the argument is fine until a negative edge lets the tail "
                  "of a path reduce its total."),
            ("example", ("Where a negative edge breaks it",
                         "Vertices `s, a, b` with `w(s,a) = 1`, `w(s,b) = 2`, "
                         "`w(b,a) = −2`. Dijkstra settles `a` at distance 1 and never "
                         "reconsiders, but `s → b → a` has weight 0. The answer is wrong "
                         "and the algorithm never notices.")),
            ("p", "Bellman&ndash;Ford handles negative weights by relaxing every edge `n−1` "
                  "times, at cost `Θ(n|E|)`, and detects negative cycles &mdash; for which "
                  "no shortest path exists at all, since going round the cycle again always "
                  "reduces the total."),
            ("h3", "Cost"),
            ("math", [
                "implementation of \"smallest unsettled\"     cost",
                "linear scan                                 Θ(n² + |E|)",
                "binary heap                                 Θ((n + |E|) log n)",
                "Fibonacci heap                              Θ(|E| + n log n)",
            ]),
            ("p", "For sparse graphs the heap version is much faster; for dense ones the "
                  "simple scan is competitive. The choice is exactly lesson 3's "
                  "representation trade-off appearing again."),
            ("p", "With all weights equal to 1, Dijkstra settles vertices in the order BFS "
                  "visits them, and the priority queue degenerates into a plain queue. BFS "
                  "is Dijkstra's special case, which is why lesson 8 came first."),
        ],
        "lab": ("graph", {
            "algo": "dijkstra", "preset": "complete", "n": 6,
            "panel_title": "Cheapest, not shortest",
            "panel_intro": "Edge weights are shown on the graph. The panel reports both "
                           "the weighted distance and the fewest-edge distance &mdash; and "
                           "on most graphs they disagree.",
        }),
        "steps_title": "Running Dijkstra",
        "steps_intro": "Settle the nearest, relax its edges, repeat.",
        "steps": [
            ("Initialise",
             "Source at 0, everything else at infinity, nothing settled."),
            ("Settle the unsettled vertex with the smallest distance",
             "Its distance is now final. This is the step the correctness proof justifies."),
            ("Relax its edges",
             "For each neighbour, if going through the settled vertex is cheaper, update "
             "the distance and the parent."),
            ("Repeat until everything reachable is settled",
             "Vertices still at infinity are unreachable. Follow the parent pointers "
             "backwards to recover a route."),
        ],
        "worked": {
            "title": "Cheapest and shortest disagree",
            "intro": ["`s → a` weight 10; `s → b` weight 3; `b → a` weight 2; `a → t` weight 1; `b → t` weight 9."],
            "lines": [
                "settle s     dist: s=0, a=10, b=3,  t=∞",
                "settle b (3) relax:  a = min(10, 3+2) = 5     t = min(∞, 3+9) = 12",
                "settle a (5) relax:  t = min(12, 5+1) = 6",
                "settle t (6)",
                "",
                "shortest by WEIGHT:   s → b → a → t   weight 6,  three edges",
                "shortest by EDGES:    s → b → t       two edges, weight 12",
                "",
                "BFS would have returned the two-edge route — twice the cost.",
            ],
            "after": [
                "The relaxation of `a` from 10 down to 5 is the step BFS cannot perform: it "
                "settles a vertex on first contact and never improves it. That is exactly "
                "right when every edge costs 1 and wrong otherwise."
            ],
        },
        "quiz_title": "Shortest paths",
        "quiz": [
            {"q": "Dijkstra requires:",
             "a": ["a connected graph", "non-negative edge weights",
                   "integer weights", "a tree"],
             "c": 1,
             "why": "A settled vertex is never revisited, which is only safe when no later "
                    "route can be cheaper &mdash; guaranteed by non-negativity."},
            {"q": "With all weights equal to 1, Dijkstra reduces to:",
             "a": ["DFS", "BFS", "Kruskal", "nothing"],
             "c": 1,
             "why": "The priority queue becomes an ordinary queue and vertices settle in "
                    "distance order. BFS is the special case."},
            {"q": "For negative edge weights you should use:",
             "a": ["Dijkstra with an offset added to every weight",
                   "Bellman&ndash;Ford",
                   "BFS",
                   "Kruskal"],
             "c": 1,
             "why": "Adding a constant to every weight changes which path is cheapest, "
                    "since paths have different lengths. Bellman&ndash;Ford handles "
                    "negatives directly."},
        ],
        "mistakes": [
            ("Using BFS on a weighted graph",
             "It answers \"fewest edges\", which is a different question and often a much "
             "more expensive route."),
            ("Applying Dijkstra with negative weights",
             "It returns a confident wrong answer. The failure is silent, which is the "
             "worst kind."),
            ("Adding a constant to make weights non-negative",
             "It penalises longer paths differently and changes the answer. It is a "
             "tempting fix and it does not work."),
        ],
        "standard": ("Finish when you can say where the correctness proof uses "
                     "non-negativity.",
                     "Build a small graph with one negative edge and run Dijkstra by hand. "
                     "Watch it settle a vertex whose distance later turns out to be "
                     "improvable, and locate the step of the proof that fails."),
        "note": "A* search is Dijkstra with a heuristic estimate added to each distance, "
                "guiding the search toward the target. It is correct when the heuristic "
                "never overestimates, and it is what route planners actually run.",
    },
    # ---------------------------------------------------------------- 10
    {
        "slug": "trees",
        "title": "Trees",
        "module": "Trees",
        "one_line": "Connected and acyclic — and five other equivalent descriptions.",
        "summary": (
            "A tree is a connected acyclic graph, and that single condition forces "
            "`|E| = |V| − 1`, unique paths between vertices, and every edge being a "
            "bridge. The characterisations are all equivalent."
        ),
        "key": [
            "tree = connected + acyclic",
            "⟺ |E| = |V| − 1 and connected",
            "⟺ exactly one path between every pair of vertices",
            "every tree with ≥ 2 vertices has at least 2 leaves",
        ],
        "key_label": "Six ways to say the same thing",
        "concepts_intro": (
            "Trees are the minimally connected graphs: connected, with nothing to spare."
        ),
        "concepts": [
            ("`n − 1` edges is exactly enough",
             "Fewer disconnects, more creates a cycle. Trees sit exactly at the boundary "
             "lesson 4's edge bound identified."),
            ("Paths are unique",
             "Two distinct paths between the same pair would form a cycle. Uniqueness is "
             "equivalent to acyclicity given connectivity."),
            ("Every edge is a bridge",
             "No edge lies on a cycle, so removing any one disconnects the tree. Trees "
             "have no redundancy at all."),
        ],
        "read_title": "Trees",
        "read_intro": "The definition, the equivalences, and the leaf lemma.",
        "body": [
            ("def", ("Tree and forest",
                     "A <strong>tree</strong> is a connected acyclic graph. A "
                     "<strong>forest</strong> is an acyclic graph, so its components are "
                     "trees. A vertex of degree 1 is a <strong>leaf</strong>.")),
            ("thm", ("Equivalent characterisations",
                     "For a graph `G` on `n` vertices, the following are equivalent: "
                     "(1) `G` is a tree; "
                     "(2) `G` is connected with `n − 1` edges; "
                     "(3) `G` is acyclic with `n − 1` edges; "
                     "(4) every pair of vertices is joined by exactly one path; "
                     "(5) `G` is connected and every edge is a bridge; "
                     "(6) `G` is acyclic and adding any edge creates exactly one cycle.")),
            ("proof", [
                "<strong>(1) ⟹ (4).</strong> Connectivity gives at least one path. If two "
                "distinct paths joined `u` and `v`, following one and returning by the "
                "other would produce a cycle.",
                "<strong>(4) ⟹ (5).</strong> Unique paths mean removing any edge `uv` "
                "leaves no `u`&ndash;`v` route, since that edge was the only path.",
                "<strong>(1) ⟹ (2),</strong> by induction on `n`. A tree on one vertex has "
                "0 edges. For `n ≥ 2`, the leaf lemma below gives a leaf; removing it "
                "leaves a tree on `n − 1` vertices, with `n − 2` edges by hypothesis, so "
                "`G` has `n − 1`.",
                "<strong>(2) ⟹ (1).</strong> A connected graph with a cycle can lose a "
                "cycle edge and stay connected; repeating until acyclic gives a tree, which "
                "has `n − 1` edges by the previous part. Since `G` already had `n − 1`, no "
                "edge was removed and `G` was acyclic.",
            ]),
            ("thm", ("Leaf lemma",
                     "Every tree with at least two vertices has at least two leaves.")),
            ("proof", [
                "Take a longest path `v₀ v₁ … v_k` in the tree; one exists because the "
                "graph is finite, and `k ≥ 1` since there are at least two vertices and the "
                "tree is connected.",
                "Every neighbour of `v₀` must lie on the path &mdash; otherwise the path "
                "could be extended, contradicting maximality &mdash; and it cannot be any "
                "`vᵢ` with `i ≥ 2`, since that would close a cycle. So `v₀`'s only "
                "neighbour is `v₁`, making it a leaf. The same argument applies at `v_k`.",
            ]),
            ("p", "The longest-path argument is a standard device and worth keeping: it "
                  "produces an object that cannot be extended, and maximality is then the "
                  "hypothesis that does the work."),
            ("h3", "Rooted trees"),
            ("def", ("Rooted tree",
                     "A tree with one vertex designated the <strong>root</strong>. Each "
                     "other vertex then has a unique <strong>parent</strong> (its "
                     "neighbour toward the root), and its other neighbours are its "
                     "<strong>children</strong>. The <strong>depth</strong> of a vertex is "
                     "its distance from the root, and the <strong>height</strong> of the "
                     "tree is the largest depth.")),
            ("p", "Rooting adds structure that the underlying tree does not have: the "
                  "parent relation is a partial order, and it is course 2 lesson 9's "
                  "material appearing as a data structure."),
            ("thm", ("Binary trees",
                     "A <strong>binary tree</strong> has at most two children per vertex. "
                     "One of height `h` has at most `2^{h+1} − 1` vertices, so a binary "
                     "tree on `n` vertices has height at least `log₂(n+1) − 1`.")),
            ("p", "That bound is why balanced search trees are the data structure they are: "
                  "`n` items can be arranged with depth about `log₂ n`, and search costs "
                  "one comparison per level. Course 8 lesson 6 makes the connection to "
                  "binary search explicit."),
            ("h3", "Counting trees"),
            ("thm", ("Cayley's formula",
                     "The number of distinct labelled trees on `n` vertices is `n^{n−2}`. "
                     "For `n = 4` that is 16; for `n = 10` it is a hundred million.")),
        ],
        "lab": ("graph", {
            "algo": "tree", "preset": "tree", "n": 7,
            "panel_title": "The characterisations, checked",
            "panel_intro": "The panel reports connectivity, the edge count and `|V| − 1` "
                           "side by side. Add one edge and a cycle appears; remove one and "
                           "the graph splits.",
        }),
        "steps_title": "Recognising a tree",
        "steps_intro": "Two of the three conditions imply the third.",
        "steps": [
            ("Count the edges",
             "A tree on `n` vertices has exactly `n − 1`. Any other count settles it "
             "immediately."),
            ("Check connectivity",
             "One search. Connected with `n − 1` edges is a tree."),
            ("Or check for cycles",
             "Acyclic with `n − 1` edges is also a tree. Any two of connected, acyclic and "
             "`n − 1` edges imply the third."),
            ("Find the leaves",
             "Degree-1 vertices. There are at least two, and induction on a tree usually "
             "proceeds by removing one."),
        ],
        "worked": {
            "title": "Is it a tree?",
            "intro": ["Three graphs on 6 vertices."],
            "lines": [
                "A:  edges 1–2, 2–3, 3–4, 4–5, 5–6                  |E| = 5 = n−1",
                "    connected?  yes.        ⟹ TREE (a path)",
                "    leaves: 1 and 6 — exactly two, the minimum",
                "",
                "B:  edges 1–2, 1–3, 1–4, 1–5, 1–6                  |E| = 5 = n−1",
                "    connected?  yes.        ⟹ TREE (a star)",
                "    leaves: 2,3,4,5,6 — five of them",
                "",
                "C:  edges 1–2, 2–3, 3–1, 4–5, 5–6                  |E| = 5 = n−1",
                "    connected?  NO — two components.",
                "    ⟹ NOT a tree.  It is a forest? No: 1–2–3–1 is a cycle.",
                "    Right edge count, and neither connected nor acyclic.",
            ],
            "after": [
                "Graph C is the warning: `n − 1` edges alone proves nothing. The count is "
                "necessary and must be paired with connectivity or acyclicity, and C has "
                "neither."
            ],
        },
        "quiz_title": "Trees",
        "quiz": [
            {"q": "A tree on 12 vertices has how many edges?",
             "a": ["12", "11", "13", "24"],
             "c": 1,
             "why": "`n − 1 = 11`, always. It follows from the definition by induction on "
                    "the leaf lemma."},
            {"q": "Which is NOT equivalent to being a tree?",
             "a": ["connected and acyclic",
                   "connected with `n − 1` edges",
                   "having `n − 1` edges",
                   "exactly one path between every pair"],
             "c": 2,
             "why": "A triangle plus a disjoint path has `n − 1` edges and is neither "
                    "connected nor acyclic. The count needs a companion condition."},
            {"q": "Every tree with at least two vertices has:",
             "a": ["a cycle", "at least two leaves",
                   "a vertex of degree 3", "an even number of edges"],
             "c": 1,
             "why": "Take a longest path; both its endpoints must be leaves, or the path "
                    "could be extended or a cycle would close."},
        ],
        "mistakes": [
            ("Using the edge count alone",
             "`n − 1` edges is necessary and not sufficient. It must be paired with "
             "connectivity or acyclicity."),
            ("Assuming a rooted tree is a different object",
             "Rooting adds a designated vertex and induces the parent relation; the "
             "underlying graph is unchanged."),
            ("Forgetting that a forest need not be a tree",
             "Acyclic and disconnected is a forest. Its component count is `n − |E|`."),
        ],
        "standard": ("Finish when you can prove one characterisation from another.",
                     "Prove that a connected graph with `n − 1` edges is acyclic, using the "
                     "leaf lemma and induction. It is the direction that needs an argument, "
                     "and it is four lines."),
        "note": "Trees are everywhere in computing because they combine two properties: "
                "unique paths, so navigation is unambiguous, and logarithmic depth when "
                "balanced, so navigation is fast. File systems, parse trees, search trees "
                "and decision trees are all this object.",
    },
    # ---------------------------------------------------------------- 11
    {
        "slug": "tree-traversals",
        "title": "Rooted Trees and Traversals",
        "module": "Trees",
        "one_line": "Preorder, inorder, postorder — three ways to visit every node.",
        "summary": (
            "A rooted tree is visited in one of three canonical orders, distinguished by "
            "when the root is handled. Each is a structural induction, and each is the "
            "right one for a different job."
        ),
        "key": [
            "PREORDER   root, then left subtree, then right    — copying, prefix notation",
            "INORDER    left, root, right                      — sorted order in a BST",
            "POSTORDER  left, right, then root                 — evaluation, deletion",
            "all three are structural induction (course 3 lesson 7)",
        ],
        "key_label": "Where the root goes",
        "concepts_intro": (
            "Three orders, differing only in when the root is visited, and each is right "
            "for a different task."
        ),
        "concepts": [
            ("The name says when the root is visited",
             "Pre: before the subtrees. In: between them. Post: after both. Everything "
             "else is the same recursion."),
            ("Each is a structural induction",
             "The recursive definition of a binary tree from course 3 lesson 6 gives the "
             "recursion directly."),
            ("Inorder on a search tree gives sorted order",
             "That is the defining property of a binary search tree, and it is why inorder "
             "matters."),
        ],
        "read_title": "Traversals",
        "read_intro": "The three orders, their uses, and the expression-tree example.",
        "body": [
            ("math", [
                "PREORDER(v):     visit v;  PREORDER(left);  PREORDER(right)",
                "INORDER(v):      INORDER(left);  visit v;  INORDER(right)",
                "POSTORDER(v):    POSTORDER(left);  POSTORDER(right);  visit v",
            ]),
            ("p", "Each is the recursive definition of a binary tree with the visit "
                  "inserted at a different point, so each is a structural induction in the "
                  "sense of course 3 lesson 7. Every node is visited exactly once and the "
                  "cost is `Θ(n)`."),
            ("h3", "Expression trees"),
            ("p", "An arithmetic expression is a binary tree: operators are internal nodes "
                  "and operands are leaves. The three traversals produce the three standard "
                  "notations."),
            ("math", [
                "          +",
                "         / \\",
                "        *   5",
                "       / \\",
                "      3   4",
                "",
                "PREORDER    + * 3 4 5        prefix (Polish)",
                "INORDER     3 * 4 + 5        infix — needs parentheses in general",
                "POSTORDER   3 4 * 5 +        postfix (reverse Polish)",
            ]),
            ("p", "Postfix is what stack-based evaluators consume: read left to right, push "
                  "operands, and on an operator pop two and push the result. No parentheses "
                  "and no precedence rules are needed, because the tree structure is "
                  "already encoded in the order."),
            ("p", "Infix is the notation people read and the only one of the three that is "
                  "ambiguous without parentheses or precedence conventions &mdash; which is "
                  "the whole reason course 1 lesson 2 had to state a precedence order."),
            ("h3", "Binary search trees"),
            ("def", ("Binary search tree",
                     "A binary tree in which every node's key exceeds all keys in its left "
                     "subtree and is less than all keys in its right subtree.")),
            ("thm", ("Inorder gives sorted order",
                     "An inorder traversal of a binary search tree visits the keys in "
                     "increasing order.")),
            ("proof", [
                "By structural induction. The empty tree is vacuous.",
                "For a node with subtrees `L` and `R`: by the hypothesis the traversal "
                "visits `L`'s keys in increasing order, all less than the root; then the "
                "root; then `R`'s keys in increasing order, all greater. The concatenation "
                "is increasing.",
            ]),
            ("p", "Searching a balanced binary search tree costs `Θ(log n)`, one comparison "
                  "per level, which is course 8 lesson 6's binary search reorganised as a "
                  "data structure. If the tree is unbalanced &mdash; a path &mdash; it "
                  "degenerates to `Θ(n)`, which is why balancing schemes exist."),
            ("h3", "Other traversals"),
            ("p", "<strong>Level order</strong> visits by depth and is exactly breadth-first "
                  "search from the root, using a queue rather than recursion. It is the "
                  "traversal that prints a tree row by row."),
            ("p", "For non-binary rooted trees, preorder and postorder generalise directly "
                  "&mdash; visit the children in order &mdash; while inorder does not, "
                  "since there is no single place for the root among three or more "
                  "children."),
        ],
        "lab": ("graph", {
            "algo": "dfs", "preset": "tree", "n": 7,
            "panel_title": "Depth-first order on a tree",
            "panel_intro": "The tree preset is a rooted binary tree, and DFS from vertex 1 "
                           "produces the preorder visit sequence. The labels are visit "
                           "order, not distance.",
        }),
        "steps_title": "Traversing a tree",
        "steps_intro": "Pick the order from the task.",
        "steps": [
            ("Preorder to copy or serialise",
             "The root is emitted before its subtrees, so the structure can be rebuilt as "
             "it is read."),
            ("Inorder for a search tree",
             "It produces the keys in sorted order, which is what the structure exists for."),
            ("Postorder to evaluate or delete",
             "Children are finished before the parent, which is what evaluation and safe "
             "deallocation both require."),
            ("Level order to see the shape",
             "Breadth-first from the root. It is the traversal that shows depth and "
             "balance."),
        ],
        "worked": {
            "title": "All three orders on one tree",
            "intro": ["A binary search tree containing 2, 3, 5, 6, 7, 8."],
            "lines": [
                "            6",
                "          /   \\",
                "         3     8",
                "        / \\   /",
                "       2   5 7",
                "",
                "PREORDER    6 3 2 5 8 7        root first — reconstructible",
                "INORDER     2 3 5 6 7 8        SORTED, as a BST must be",
                "POSTORDER   2 5 3 7 8 6        children before parents",
                "LEVEL       6 3 8 2 5 7        by depth",
                "",
                "Only inorder is sorted, and that is the property that makes the",
                "structure a search tree rather than an arbitrary binary tree.",
            ],
            "after": [
                "Preorder alone determines the tree when it is a binary search tree, "
                "because the ordering constraint says where each subsequent key belongs. "
                "For a general binary tree it does not: preorder plus inorder is needed to "
                "reconstruct the shape."
            ],
        },
        "quiz_title": "Traversals",
        "quiz": [
            {"q": "Which traversal of a binary search tree gives sorted order?",
             "a": ["preorder", "inorder", "postorder", "level order"],
             "c": 1,
             "why": "Left subtree, root, right subtree &mdash; and by the search-tree "
                    "property those are increasing, the root, then larger."},
            {"q": "Postfix notation comes from which traversal?",
             "a": ["preorder", "inorder", "postorder", "level order"],
             "c": 2,
             "why": "Operands before the operator, which is exactly what a stack-based "
                    "evaluator consumes."},
            {"q": "The names pre-, in- and post- refer to:",
             "a": ["the order of the children",
                   "when the root is visited relative to the subtrees",
                   "the depth", "the direction of recursion"],
             "c": 1,
             "why": "Before, between and after. The subtree recursion is identical in all "
                    "three."},
        ],
        "mistakes": [
            ("Expecting preorder to be sorted on a search tree",
             "Only inorder is. Preorder visits the root first, which is by definition not "
             "the smallest key."),
            ("Trying to define inorder for a general rooted tree",
             "With three or more children there is no single place for the root. Pre- and "
             "postorder generalise; inorder does not."),
            ("Assuming one traversal determines the tree",
             "For a general binary tree, preorder plus inorder is needed. One sequence is "
             "consistent with many shapes."),
        ],
        "standard": ("Finish when you can produce all three orders from a drawing.",
                     "Build a binary search tree by inserting 5, 3, 8, 1, 4, 7, 9 in that "
                     "order, then write all three traversals. The inorder must come out "
                     "sorted, which is a check on the insertion."),
        "note": "Postorder is why reverse Polish notation needs no parentheses: the "
                "traversal order already encodes the tree structure, so precedence never "
                "has to be inferred. Calculators and stack machines consume it directly.",
    },
    # ---------------------------------------------------------------- 12
    {
        "slug": "spanning-trees",
        "title": "Spanning Trees and Minimum Spanning Trees",
        "module": "Trees",
        "one_line": "Connect everything with as few — or as cheap — edges as possible.",
        "summary": (
            "A spanning tree reaches every vertex with `n − 1` edges. When the edges are "
            "weighted, Kruskal's greedy algorithm finds the cheapest one, and its "
            "optimality is genuinely surprising."
        ),
        "key": [
            "spanning tree: a subgraph that is a tree containing every vertex",
            "exists  ⟺  the graph is connected;  has n − 1 edges",
            "KRUSKAL  take edges in increasing weight, skip any that closes a cycle",
            "greedy is OPTIMAL here — unusually",
        ],
        "key_label": "Cheapest connection",
        "concepts_intro": (
            "The minimum spanning tree is the rare optimisation problem where the "
            "obvious greedy method is provably right."
        ),
        "concepts": [
            ("Every connected graph has a spanning tree",
             "Remove cycle edges until none remain; connectivity survives because a cycle "
             "edge is never a bridge."),
            ("Kruskal is greedy and correct",
             "Take the cheapest edge that does not close a cycle, repeatedly. The cut "
             "property is why this cannot go wrong."),
            ("Greedy is usually wrong",
             "Course 8 lesson 9 shows greedy failing on coin change and on the travelling "
             "salesman. Minimum spanning trees are the exception, and the reason is "
             "structural."),
        ],
        "read_title": "Spanning trees",
        "read_intro": "Existence, the minimum weight problem, and why greed works here.",
        "body": [
            ("def", ("Spanning tree",
                     "A <strong>spanning tree</strong> of a connected graph `G` is a "
                     "subgraph that is a tree and contains every vertex of `G`. It has "
                     "`n − 1` edges.")),
            ("thm", ("Existence",
                     "Every connected graph has a spanning tree.")),
            ("proof", [
                "If `G` is acyclic it is already a tree. Otherwise take any cycle and "
                "remove one of its edges; that edge is not a bridge (lesson 4), so the "
                "graph stays connected, and the number of edges has decreased.",
                "Repeating terminates, since the edge count strictly decreases, and it ends "
                "with a connected acyclic subgraph on all the vertices &mdash; a spanning "
                "tree.",
            ]),
            ("p", "Breadth-first and depth-first search each produce one directly: the tree "
                  "edges of a search from any vertex form a spanning tree of its component. "
                  "So the object is available for free from lesson 8."),
            ("h3", "Minimum spanning trees"),
            ("def", ("Minimum spanning tree",
                     "In a weighted connected graph, a <strong>minimum spanning tree</strong> "
                     "is a spanning tree of least total weight.")),
            ("math", [
                "KRUSKAL(G):",
                "    sort the edges by increasing weight",
                "    T = ∅",
                "    for each edge e in order:",
                "        if e does not close a cycle in T:  add e to T",
                "    return T",
            ]),
            ("thm", ("The cut property",
                     "Let `S` be any nonempty proper subset of the vertices. The lightest "
                     "edge with exactly one end in `S` belongs to some minimum spanning "
                     "tree. If it is strictly lightest, it belongs to every one.")),
            ("proof", [
                "Let `e` be that lightest crossing edge and let `T` be a minimum spanning "
                "tree not containing it. Adding `e` to `T` creates exactly one cycle "
                "(lesson 10), and that cycle must cross the cut a second time, at some edge "
                "`f ≠ e`.",
                "Swapping `f` for `e` keeps the graph spanning and acyclic, and since "
                "`w(e) ≤ w(f)` the total weight does not increase. So the result is also a "
                "minimum spanning tree, and it contains `e`.",
            ]),
            ("p", "Kruskal's correctness follows: whenever it adds an edge, that edge is "
                  "the lightest crossing the cut between the component it is joining and "
                  "the rest, so the cut property guarantees a minimum spanning tree "
                  "containing everything chosen so far."),
            ("p", "Prim's algorithm is the same theorem used differently: grow a single "
                  "tree from one vertex, always adding the lightest edge leaving it. It is "
                  "Dijkstra's shape with a different priority, and it is often faster on "
                  "dense graphs."),
            ("h3", "Why greed works here and usually does not"),
            ("p", "The cut property is a strong structural fact: a locally cheapest choice "
                  "is provably part of a global optimum. Most optimisation problems have no "
                  "such property, and greed then fails &mdash; sometimes badly. Coin change "
                  "with denominations `{1, 3, 4}` is greedy-wrong at 6, and the travelling "
                  "salesman is greedy-wrong routinely."),
            ("p", "The technical name for the structure that makes greed correct is a "
                  "<strong>matroid</strong>, and the forests of a graph form one. Course 8 "
                  "lesson 9 discusses greedy algorithms without the theory; what matters "
                  "here is that \"greedy works\" is a theorem about this problem, not a "
                  "general method."),
            ("h3", "Cost"),
            ("p", "Kruskal sorts the edges &mdash; `Θ(|E| log |E|)` &mdash; and then tests "
                  "each for a cycle using a union&ndash;find structure, at nearly constant "
                  "cost per test. So the sort dominates. Prim with a heap runs in "
                  "`Θ((n + |E|) log n)`."),
        ],
        "lab": ("graph", {
            "algo": "mst", "preset": "complete", "n": 6,
            "panel_title": "Kruskal, edge by edge",
            "panel_intro": "The panel lists the edges in weight order and marks each as "
                           "taken or rejected. A rejected edge is always one whose ends are "
                           "already connected.",
        }),
        "steps_title": "Building a minimum spanning tree",
        "steps_intro": "Sort, then add whatever does not close a cycle.",
        "steps": [
            ("Sort the edges by weight",
             "This is the dominant cost and the only global step in the algorithm."),
            ("Take each edge in order if it joins two components",
             "Skip it if both ends are already connected &mdash; that would close a cycle."),
            ("Stop at `n − 1` edges",
             "Or when the list is exhausted. Fewer than `n − 1` means the graph was "
             "disconnected and you have a minimum spanning forest."),
            ("Verify the count and the connectivity",
             "`n − 1` edges reaching every vertex. Both are cheap checks and either failing "
             "means the input was disconnected."),
        ],
        "worked": {
            "title": "Kruskal on five vertices",
            "intro": ["Edges: AB 1, BC 2, CD 3, DE 4, AE 5, AC 6, BD 7."],
            "lines": [
                "sorted:  AB(1) BC(2) CD(3) DE(4) AE(5) AC(6) BD(7)",
                "",
                "AB 1   components {A,B}                       TAKE",
                "BC 2   joins {A,B} and {C}                    TAKE",
                "CD 3   joins {A,B,C} and {D}                  TAKE",
                "DE 4   joins {A,B,C,D} and {E}                TAKE",
                "AE 5   A and E already connected              skip",
                "AC 6   already connected                      skip",
                "BD 7   already connected                      skip",
                "",
                "MST = {AB, BC, CD, DE},  4 = n − 1 edges,  total weight 10",
                "",
                "Note the algorithm never reconsidered a choice.",
            ],
            "after": [
                "Every edge was decided once and never revisited, which is what makes the "
                "algorithm greedy &mdash; and what makes its correctness surprising. The "
                "cut property is the theorem that licenses never looking back."
            ],
        },
        "quiz_title": "Spanning trees",
        "quiz": [
            {"q": "A spanning tree of a connected graph on 20 vertices has:",
             "a": ["20 edges", "19 edges", "as many edges as the graph", "1 edge"],
             "c": 1,
             "why": "It is a tree on all `n` vertices, so `n − 1 = 19` edges."},
            {"q": "Kruskal's algorithm rejects an edge when:",
             "a": ["it is too heavy",
                   "both its ends are already connected in the partial tree",
                   "it is a bridge",
                   "it has been seen before"],
             "c": 1,
             "why": "Adding it would close a cycle. Weight decides the order, not the "
                    "rejection."},
            {"q": "Greedy algorithms are optimal for minimum spanning trees because:",
             "a": ["greedy is always optimal",
                   "the cut property guarantees the locally cheapest crossing edge is in some optimum",
                   "the graph is a tree",
                   "the weights are positive"],
             "c": 1,
             "why": "It is a theorem about this problem. Greed fails on coin change and on "
                    "the travelling salesman."},
        ],
        "mistakes": [
            ("Assuming greedy works generally",
             "It works here because of the cut property. Course 8 lesson 9 shows greedy "
             "failing on a problem that looks no harder."),
            ("Stopping before `n − 1` edges",
             "Unless the graph is disconnected, in which case you have a minimum spanning "
             "forest and should say so."),
            ("Assuming the minimum spanning tree is unique",
             "It is unique when all edge weights are distinct. With ties there may be "
             "several, all of the same total weight."),
        ],
        "standard": ("Finish when you can run Kruskal and justify each rejection.",
                     "Take a weighted graph on six vertices and run the algorithm, saying "
                     "for each rejected edge which two vertices were already connected. "
                     "That justification is the correctness argument in miniature."),
        "note": "Minimum spanning trees are used for network design, clustering (cut the "
                "heaviest edges of the tree and the components are the clusters), and as a "
                "subroutine in approximation algorithms &mdash; including a "
                "2-approximation for the travelling salesman problem.",
    },
    # ---------------------------------------------------------------- 13
    {
        "slug": "graph-colouring",
        "title": "Graph Colouring",
        "module": "Colouring and planarity",
        "one_line": "Colour the vertices so no edge joins two of the same colour.",
        "summary": (
            "The chromatic number is the fewest colours needed. Two colours is a linear "
            "test, three is NP-complete, and the four-colour theorem says planar graphs "
            "never need more than four."
        ),
        "key": [
            "proper colouring: adjacent vertices get different colours",
            "χ(G) = chromatic number = fewest colours needed",
            "χ = 2  ⟺  bipartite       — linear-time test",
            "deciding χ ≤ 3 is NP-complete;  greedy uses at most Δ + 1",
        ],
        "key_label": "Easy at two, hard at three",
        "concepts_intro": (
            "Colouring models conflict: adjacent things cannot share a resource, and the "
            "chromatic number is how many resources are needed."
        ),
        "concepts": [
            ("It models conflict",
             "Exam scheduling, register allocation, frequency assignment. An edge means "
             "\"cannot share\", and a colour is a resource."),
            ("Greedy is fast and not optimal",
             "It never uses more than `Δ + 1` colours, and the visiting order can cost it "
             "colours it did not need."),
            ("Two is easy, three is hard",
             "`χ ≤ 2` is one search; `χ ≤ 3` is NP-complete. The boundary between easy and "
             "hard is exactly there."),
        ],
        "read_title": "Colouring",
        "read_intro": "The definition, bounds, the greedy algorithm, and the four-colour theorem.",
        "body": [
            ("def", ("Proper colouring, chromatic number",
                     "A <strong>proper colouring</strong> assigns a colour to each vertex "
                     "so that adjacent vertices differ. The <strong>chromatic number</strong> "
                     "`χ(G)` is the smallest number of colours admitting one.")),
            ("math", [
                "χ(Kₙ)      = n          every pair adjacent",
                "χ(Cₙ)      = 2 if n even, 3 if n odd",
                "χ(tree)    = 2          for any tree with an edge",
                "χ(bipartite) = 2        by definition, for a graph with an edge",
            ]),
            ("thm", ("Two colours",
                     "`χ(G) ≤ 2` if and only if `G` is bipartite, if and only if `G` has no "
                     "odd cycle. Testable in `Θ(n + |E|)` by lesson 6.")),
            ("thm", ("Greedy bound",
                     "Colouring the vertices in any order, giving each the smallest colour "
                     "unused by its already-coloured neighbours, uses at most `Δ + 1` "
                     "colours, where `Δ` is the maximum degree.")),
            ("proof", [
                "When a vertex is coloured, it has at most `Δ` neighbours, so at most `Δ` "
                "colours are forbidden. Among `Δ + 1` colours one is always available.",
            ]),
            ("p", "Brooks's theorem sharpens this: `χ(G) ≤ Δ` unless `G` is a complete "
                  "graph or an odd cycle, which are the two families needing `Δ + 1`."),
            ("p", "Greedy is not optimal, and the order is what costs it. On a bipartite "
                  "graph a bad order can use many colours where two suffice, which is why "
                  "the algorithm is a bound rather than a solution."),
            ("thm", ("Colouring is hard",
                     "Deciding whether `χ(G) ≤ 3` is NP-complete, and computing `χ(G)` "
                     "exactly is NP-hard. Even approximating it well is hard.")),
            ("p", "The jump from 2 to 3 is the sharpest example on this path of a problem "
                  "changing character with a parameter. Nothing in the statements suggests "
                  "it, and course 8 lesson 11 explains what NP-complete means."),
            ("h3", "The four-colour theorem"),
            ("thm", ("Four colours suffice",
                     "Every planar graph has `χ(G) ≤ 4`.")),
            ("p", "Conjectured in 1852 and proved by Appel and Haken in 1976, with a proof "
                  "that reduced the problem to 1936 configurations and checked them by "
                  "computer. It was the first major theorem whose proof could not be "
                  "verified by a human reading it, and the resulting argument about what "
                  "counts as a proof has not entirely settled."),
            ("p", "The five-colour theorem, by contrast, has a short human proof by "
                  "induction using Euler's formula from lesson 14. Four is genuinely "
                  "harder than five."),
            ("h3", "Applications"),
            ("ul", [
                "<strong>Exam scheduling.</strong> Vertices are exams, edges join exams "
                "sharing a student, colours are time slots. `χ` is the fewest slots needed.",
                "<strong>Register allocation.</strong> Vertices are variables, edges join "
                "variables live at the same time, colours are CPU registers. Compilers do "
                "this constantly &mdash; and use heuristics, since the problem is NP-hard.",
                "<strong>Frequency assignment.</strong> Vertices are transmitters, edges "
                "join those that would interfere, colours are frequencies.",
                "<strong>Sudoku.</strong> A 9-colouring problem on a graph with 81 vertices "
                "and an edge for every row, column and box constraint.",
            ]),
        ],
        "lab": ("graph", {
            "algo": "colour", "preset": "petersen", "n": 6,
            "panel_title": "Greedy, and its bound",
            "panel_intro": "The lab reports the colours greedy used and the `Δ + 1` bound. "
                           "Build a bipartite graph and check whether greedy finds the "
                           "two-colouring &mdash; it does not always.",
        }),
        "steps_title": "Colouring a graph",
        "steps_intro": "Bound first, then colour.",
        "steps": [
            ("Look for a large complete subgraph",
             "A `Kₖ` inside `G` forces `χ ≥ k`. This is the standard lower bound and it is "
             "often tight."),
            ("Check bipartiteness",
             "If the graph is bipartite, `χ = 2` and you are finished. One search."),
            ("Run greedy for an upper bound",
             "At most `Δ + 1` colours. Trying several vertex orders often reduces it."),
            ("Compare the bounds",
             "If the clique lower bound meets the greedy upper bound, that value is `χ`. "
             "Otherwise exact computation is expensive."),
        ],
        "worked": {
            "title": "Scheduling exams",
            "intro": ["Five exams; edges join exams with a student in common."],
            "lines": [
                "edges:  A–B, A–C, B–C, B–D, C–D, D–E",
                "",
                "A, B, C are mutually adjacent — a triangle — so χ ≥ 3.",
                "",
                "Greedy in order A, B, C, D, E:",
                "   A  colour 1",
                "   B  adjacent to A          colour 2",
                "   C  adjacent to A and B    colour 3",
                "   D  adjacent to B and C    colour 1",
                "   E  adjacent to D          colour 2",
                "",
                "3 colours used, and χ ≥ 3, so χ = 3.",
                "",
                "Three time slots:   {A, D}   {B, E}   {C}",
            ],
            "after": [
                "The triangle gave the lower bound and greedy gave the upper, and they met "
                "&mdash; which is the only cheap way to be certain. Without a matching "
                "lower bound, greedy's answer is an upper bound and nothing more."
            ],
        },
        "quiz_title": "Colouring",
        "quiz": [
            {"q": "`χ(C₅)` equals:",
             "a": ["2", "3", "5", "4"],
             "c": 1,
             "why": "An odd cycle is not bipartite so `χ &gt; 2`, and three colours suffice "
                    "by alternating with one repeat."},
            {"q": "Greedy colouring uses at most:",
             "a": ["`χ(G)`", "`Δ + 1` colours", "2 colours", "`n` colours"],
             "c": 1,
             "why": "Each vertex has at most `Δ` coloured neighbours, so one of `Δ + 1` "
                    "colours is free. It is a bound, not the optimum."},
            {"q": "Deciding whether three colours suffice is:",
             "a": ["linear time", "NP-complete", "impossible", "the same as bipartiteness"],
             "c": 1,
             "why": "Two colours is one search; three is NP-complete. The boundary between "
                    "easy and hard is exactly there."},
        ],
        "mistakes": [
            ("Treating greedy's answer as `χ`",
             "It is an upper bound. A different vertex order may use fewer colours, and "
             "`χ` may be lower than any order achieves quickly."),
            ("Assuming a planar graph needs four colours",
             "Four suffice; many planar graphs need two or three. The theorem is an upper "
             "bound."),
            ("Forgetting the clique lower bound",
             "A `Kₖ` inside the graph forces `χ ≥ k`, and it is usually the easiest lower "
             "bound to find."),
        ],
        "standard": ("Finish when you can bound `χ` from both sides.",
                     "For a graph of your own, find the largest complete subgraph you can "
                     "and run greedy. If the two numbers meet you have `χ` exactly; if not, "
                     "you have located the difficulty."),
        "note": "Register allocation in compilers is graph colouring on a graph with "
                "thousands of vertices, solved by heuristics because the exact problem is "
                "NP-hard. It is one of the most economically significant applications of "
                "anything on this path.",
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "planar-graphs",
        "title": "Planar Graphs and Euler's Formula",
        "module": "Colouring and planarity",
        "one_line": "Drawable without crossings, and the formula that constrains it.",
        "summary": (
            "A planar graph can be drawn with no edges crossing. Euler's formula "
            "`V − E + F = 2` bounds how many edges such a graph can have, and "
            "Kuratowski's theorem says exactly which graphs fail."
        ),
        "key": [
            "V − E + F = 2                    Euler's formula, connected planar",
            "E ≤ 3V − 6                       for V ≥ 3",
            "E ≤ 2V − 4                       if additionally triangle-free",
            "K₅ and K_{3,3} are the obstructions        (Kuratowski)",
        ],
        "key_label": "One formula, several consequences",
        "concepts_intro": (
            "Planarity is a property of the graph, not of a drawing, and Euler's formula "
            "is what makes it computable."
        ),
        "concepts": [
            ("Planar means a crossing-free drawing exists",
             "Not that a particular drawing has no crossings. `K₄` drawn with a crossing is "
             "still planar."),
            ("Euler's formula counts faces",
             "`V − E + F = 2` for any connected planar drawing, including the unbounded "
             "outer face."),
            ("Two graphs are the only obstructions",
             "Kuratowski: a graph is planar exactly when it contains no subdivision of "
             "`K₅` or `K_{3,3}`."),
        ],
        "read_title": "Planarity",
        "read_intro": "Euler's formula, the edge bounds it gives, and the two forbidden graphs.",
        "body": [
            ("def", ("Planar graph, face",
                     "A graph is <strong>planar</strong> if it can be drawn in the plane "
                     "with no two edges crossing. Such a drawing divides the plane into "
                     "<strong>faces</strong>, including one unbounded outer face.")),
            ("thm", ("Euler's formula",
                     "For a connected planar graph drawn without crossings, "
                     "`V − E + F = 2`, where `F` counts the faces including the outer one.")),
            ("proof", [
                "By induction on the number of edges. A connected graph with no cycle is a "
                "tree: `E = V − 1` and `F = 1`, so `V − (V−1) + 1 = 2`.",
                "If the graph has a cycle, remove one of its edges. The graph stays "
                "connected, and the two faces on either side of that edge merge into one, "
                "so `E` and `F` each drop by 1 and `V − E + F` is unchanged. Repeating "
                "reaches a tree.",
            ]),
            ("example", ("A cube",
                         "The graph of a cube has `V = 8`, `E = 12`, `F = 6`, and "
                         "`8 − 12 + 6 = 2`. The same holds for every convex polyhedron "
                         "&mdash; which is where Euler first stated it, in 1758.")),
            ("thm", ("The edge bound",
                     "A simple connected planar graph with `V ≥ 3` has `E ≤ 3V − 6`. If it "
                     "is also triangle-free, `E ≤ 2V − 4`.")),
            ("proof", [
                "Every face is bounded by at least 3 edges, and every edge borders at most "
                "2 faces. Counting edge&ndash;face incidences two ways gives `3F ≤ 2E`.",
                "Substituting `F = 2 − V + E` into `3F ≤ 2E` gives "
                "`3(2 − V + E) ≤ 2E`, hence `E ≤ 3V − 6`.",
                "If there are no triangles, every face has at least 4 edges, so `4F ≤ 2E` "
                "and the same substitution gives `E ≤ 2V − 4`.",
            ]),
            ("p", "The double count is the handshake theorem's argument applied to faces "
                  "instead of vertices, which is worth noticing: the same technique keeps "
                  "returning."),
            ("thm", ("`K₅` and `K_{3,3}` are not planar",
                     "Neither can be drawn without crossings.")),
            ("proof", [
                "`K₅` has `V = 5` and `E = 10`. The bound gives `E ≤ 3(5) − 6 = 9 &lt; 10`, "
                "so it is not planar.",
                "`K_{3,3}` has `V = 6` and `E = 9`, and satisfies `E ≤ 3V − 6 = 12`. But it "
                "is bipartite hence triangle-free, so the sharper bound applies: "
                "`E ≤ 2(6) − 4 = 8 &lt; 9`. Not planar.",
            ]),
            ("p", "Two graphs, two bounds, and the second needed the triangle-free version "
                  "&mdash; which is why both were derived. `K_{3,3}` is the classic \"three "
                  "utilities to three houses\" puzzle, and it has no solution."),
            ("thm", ("Kuratowski's theorem",
                     "A graph is planar if and only if it contains no subgraph that is a "
                     "subdivision of `K₅` or of `K_{3,3}`. A <strong>subdivision</strong> "
                     "replaces edges by paths through new degree-2 vertices.")),
            ("p", "This is a complete characterisation by two forbidden structures, which "
                  "is remarkable: infinitely many graphs are non-planar and all of them "
                  "fail for one of two reasons. Planarity can also be tested in linear "
                  "time, though the algorithms are intricate."),
            ("thm", ("Consequences for colouring",
                     "Every planar graph has a vertex of degree at most 5, since otherwise "
                     "`2E = Σ deg(v) ≥ 6V`, contradicting `E ≤ 3V − 6`. That fact is the "
                     "base of the induction proving the five-colour theorem, and the "
                     "starting point of the four-colour proof.")),
            ("p", "So this course ends where it began: with the handshake theorem. Counting "
                  "degrees gave Euler's criterion in lesson 7, the tree edge count in "
                  "lesson 10, and now the degree bound that makes planar graphs colourable."),
        ],
        "lab": ("graph", {
            "algo": "degree", "preset": "complete", "n": 5,
            "panel_title": "Check the bound yourself",
            "panel_intro": "`K₅` is loaded: five vertices and ten edges, against the planar "
                           "limit of `3V − 6 = 9`. Drop to four vertices and `K₄` fits the "
                           "bound &mdash; and is indeed planar.",
        }),
        "steps_title": "Testing planarity",
        "steps_intro": "Count first; the bound settles many cases.",
        "steps": [
            ("Check `E ≤ 3V − 6`",
             "If it fails, the graph is not planar and you are finished. Cheap and "
             "conclusive when it fires."),
            ("If triangle-free, check `E ≤ 2V − 4`",
             "The sharper bound, and the one that rules out `K_{3,3}`."),
            ("Look for `K₅` or `K_{3,3}` subdivisions",
             "By Kuratowski these are the only obstructions. Finding one is a complete "
             "proof of non-planarity."),
            ("Otherwise try to draw it",
             "The bounds are necessary and not sufficient, so passing them does not "
             "establish planarity. A crossing-free drawing does."),
        ],
        "worked": {
            "title": "Three graphs tested",
            "intro": ["The bound, the sharper bound, and a case it cannot settle."],
            "lines": [
                "K₅        V=5  E=10     3V−6 = 9   <  10     NOT PLANAR",
                "",
                "K_{3,3}   V=6  E=9      3V−6 = 12  ≥  9      inconclusive",
                "          bipartite ⟹ triangle-free",
                "          2V−4 = 8   <  9                    NOT PLANAR",
                "",
                "Petersen  V=10 E=15     3V−6 = 24  ≥  15     inconclusive",
                "          triangle-free: 2V−4 = 16 ≥ 15      still inconclusive",
                "          It contains a K_{3,3} subdivision  ⟹ NOT PLANAR",
                "                                              (Kuratowski)",
            ],
            "after": [
                "The Petersen graph passes both counting bounds and is still not planar, "
                "which shows the bounds are necessary and not sufficient. Only Kuratowski's "
                "characterisation settles it, and finding the subdivision is the work."
            ],
        },
        "quiz_title": "Planarity",
        "quiz": [
            {"q": "A connected planar graph has `V = 10` and `E = 15`. How many faces?",
             "a": ["5", "7", "25", "cannot be determined"],
             "c": 1,
             "why": "`V − E + F = 2` gives `F = 2 − 10 + 15 = 7`, counting the outer face."},
            {"q": "Why is `K₅` not planar?",
             "a": ["it has too many vertices",
                   "`E = 10 &gt; 9 = 3V − 6`",
                   "it is bipartite",
                   "it has a cycle"],
             "c": 1,
             "why": "The edge bound is violated, which is a complete proof for this graph."},
            {"q": "Kuratowski's theorem says a graph is planar exactly when it contains no subdivision of:",
             "a": ["`K₄`", "`K₅` or `K_{3,3}`", "any cycle", "`Kₙ` for large `n`"],
             "c": 1,
             "why": "Two forbidden structures characterise planarity completely, however "
                    "large the graph."},
        ],
        "mistakes": [
            ("Concluding planarity from the edge bound",
             "It is necessary and not sufficient. The Petersen graph satisfies both bounds "
             "and is not planar."),
            ("Forgetting the outer face",
             "Euler's formula counts it. Omitting it gives `V − E + F = 1` and every "
             "subsequent bound is wrong."),
            ("Applying the triangle-free bound to a graph with triangles",
             "`E ≤ 2V − 4` requires girth at least 4. Using it otherwise rules out planar "
             "graphs incorrectly."),
        ],
        "standard": ("Finish when you can rule out planarity by counting.",
                     "Take `K_{4,4}`: `V = 8`, `E = 16`, triangle-free. `2V − 4 = 12 &lt; "
                     "16`, so it is not planar &mdash; settled by arithmetic, with no "
                     "drawing attempted."),
        "note": "Euler's formula generalises to surfaces: on a torus `V − E + F = 0`, and "
                "graphs that cannot be drawn in the plane can often be drawn there. `K₅` "
                "and `K_{3,3}` both embed in a torus, and the genus of a graph measures how "
                "many handles it needs.",
    },
]
