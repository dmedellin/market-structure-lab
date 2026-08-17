"""Course 7, lessons 01-07 — graphs, connectivity and traversal."""

LESSONS = [
    # ---------------------------------------------------------------- 01
    {
        "slug": "graphs-and-graph-models",
        "title": "Graphs and Graph Models",
        "module": "Basics",
        "one_line": "Vertices, edges, and the things they model.",
        "summary": (
            "A graph is a set of vertices and a set of edges joining them. The "
            "definition is deliberately spare, which is why the same object models "
            "networks, dependencies, molecules and schedules."
        ),
        "key": [
            "G = (V, E)      V vertices,  E edges (pairs of vertices)",
            "simple graph: no loops, no repeated edges, undirected",
            "adjacent: joined by an edge      incident: vertex meets edge",
            "a GRAPH is not a plot",
        ],
        "key_label": "The definition",
        "concepts_intro": (
            "The definition is short and the variants matter: what counts as an edge "
            "decides which theorems apply."
        ),
        "concepts": [
            ("A graph is a relation, drawn",
             "Course 2's symmetric irreflexive relation on `V` is exactly a simple graph. "
             "The picture adds nothing mathematically and a great deal practically."),
            ("The drawing is not the graph",
             "Position and edge shape carry no information. Two very different pictures "
             "can be the same graph, which is lesson 5's subject."),
            ("The variants are not interchangeable",
             "Loops, multiple edges and directions each change which theorems hold. "
             "\"Simple graph\" is the default here and is stated where it matters."),
        ],
        "read_title": "What a graph is",
        "read_intro": "The definition, the variants, and four models.",
        "body": [
            ("def", ("Simple graph",
                     "A <strong>simple graph</strong> `G = (V, E)` is a finite set `V` of "
                     "<strong>vertices</strong> together with a set `E` of "
                     "<strong>edges</strong>, each an unordered pair of distinct vertices. "
                     "No loops and no repeated edges.")),
            ("p", "Two vertices joined by an edge are <strong>adjacent</strong> or "
                  "<strong>neighbours</strong>; a vertex and an edge meeting are "
                  "<strong>incident</strong>. `|V|` is the <strong>order</strong> and "
                  "`|E|` the <strong>size</strong>."),
            ("math", [
                "variant           edges may…                  example use",
                "simple graph      neither loop nor repeat     friendship",
                "multigraph        repeat                      road networks with",
                "                                              parallel routes",
                "pseudograph       loop and repeat             state machines",
                "directed graph    have a direction            dependencies, the web",
                "weighted graph    carry a number              distances, costs",
            ]),
            ("p", "Unless stated otherwise, \"graph\" on this course means a simple "
                  "undirected graph. Lessons 8 and 10 attach weights; directions appear "
                  "only in remarks."),
            ("h3", "Standard families"),
            ("math", [
                "Kₙ        complete graph        every pair joined      C(n,2) edges",
                "Cₙ        cycle                 a single closed ring   n edges",
                "Pₙ        path                  a single open chain    n−1 edges",
                "K_{m,n}   complete bipartite    every left–right pair  mn edges",
                "Qₙ        hypercube             bit strings differing  n·2^{n−1} edges",
                "                                in one position",
            ]),
            ("p", "`K₅` and `K_{3,3}` matter later: lesson 14 shows they are precisely the "
                  "obstructions to drawing a graph in the plane without crossings."),
            ("h3", "Four models"),
            ("ul", [
                "<strong>Social networks.</strong> Vertices are people, edges are "
                "acquaintance. Course 2's pigeonhole result &mdash; two people share a "
                "degree &mdash; is a statement about this graph.",
                "<strong>Road networks.</strong> Vertices are junctions, edges are roads, "
                "weights are distances. Shortest paths are lesson 10.",
                "<strong>Dependencies.</strong> Vertices are tasks, directed edges are "
                "\"must precede\". A valid schedule exists exactly when there is no cycle, "
                "which is course 2's partial order again.",
                "<strong>Molecules.</strong> Vertices are atoms, edges are bonds. Two "
                "molecules with the same formula and different structures are non-isomorphic "
                "graphs, which is lesson 5.",
            ]),
            ("p", "The common thread: whenever the data is \"a set of things and which "
                  "pairs are related\", it is a graph, and every theorem in this course "
                  "applies to it at once. That generality is the reason graph theory is "
                  "worth a course."),
            ("thm", ("Maximum edges",
                     "A simple graph on `n` vertices has at most `C(n,2) = n(n−1)/2` edges, "
                     "with equality exactly for `Kₙ`.")),
            ("proof", [
                "Each edge is an unordered pair of distinct vertices, and no pair may "
                "repeat, so the edges form a subset of the `C(n,2)` pairs. Course 4 lesson "
                "4 counts them.",
            ]),
        ],
        "lab": ("graph", {
            "algo": "degree", "preset": "complete", "n": 5,
            "panel_title": "Build any graph",
            "panel_intro": "Toggle any cell of the adjacency matrix. The presets are the "
                           "standard families; everything else is yours, and every "
                           "algorithm re-derives from what you build.",
        }),
        "steps_title": "Modelling with a graph",
        "steps_intro": "Vertices first, then decide what an edge means.",
        "steps": [
            ("Say what a vertex is",
             "One per entity: person, junction, task, atom. If the answer is unclear the "
             "model is not ready."),
            ("Say exactly what an edge means",
             "\"Have met\", \"a road exists\", \"must precede\". The relation must be "
             "checkable for every pair."),
            ("Decide the variant",
             "Symmetric relation: undirected. Asymmetric: directed. Repeated connections: "
             "multigraph. Costs: weighted."),
            ("Restate the question in graph terms",
             "\"Can everyone be reached\" is connectivity; \"is there a route using every "
             "road once\" is an Euler circuit. The translation is where the theorems "
             "become available."),
        ],
        "worked": {
            "title": "Counting edges in the standard families",
            "intro": ["Each count is a small application of course 4."],
            "lines": [
                "Kₙ        every pair joined            C(n,2) = n(n−1)/2",
                "          K₅ has 10 edges,  K₁₀ has 45",
                "",
                "Cₙ        a closed ring                n edges, every degree 2",
                "",
                "Pₙ        an open chain of n vertices  n−1 edges",
                "",
                "K_{m,n}   every left vertex joined to every right one     m·n edges",
                "          K_{3,3} has 9 edges",
                "",
                "Qₙ        vertices = bit strings of length n  (2ⁿ of them)",
                "          edges join strings differing in one bit",
                "          each vertex has degree n, so |E| = n·2ⁿ/2 = n·2^{n−1}",
            ],
            "after": [
                "The hypercube count used the handshake theorem of lesson 2 before it was "
                "stated: `2|E| = Σ deg(v) = n · 2ⁿ`. Counting edges through degrees is the "
                "standard move and it is worth having early."
            ],
        },
        "quiz_title": "Graphs",
        "quiz": [
            {"q": "How many edges does `K₆` have?",
             "a": ["6", "12", "15", "30"],
             "c": 2,
             "why": "`C(6,2) = 15`: every pair of the six vertices is joined exactly once."},
            {"q": "A simple graph may not have:",
             "a": ["isolated vertices", "loops or repeated edges",
                   "more than `n` edges", "cycles"],
             "c": 1,
             "why": "Those are exactly the two exclusions. Isolated vertices and cycles "
                    "are both perfectly ordinary."},
            {"q": "Task dependencies are best modelled as:",
             "a": ["an undirected graph", "a directed graph",
                   "a complete graph", "a tree"],
             "c": 1,
             "why": "\"Must precede\" is asymmetric, so the edges need direction. A valid "
                    "schedule exists exactly when the digraph has no cycle."},
        ],
        "mistakes": [
            ("Reading a graph as a plot",
             "The word means two different things. A graph here is vertices and edges; "
             "nothing is being plotted."),
            ("Treating the drawing as the object",
             "Position and edge curvature carry no information. Two unrecognisably "
             "different pictures can be the same graph."),
            ("Using an undirected graph for an asymmetric relation",
             "\"Follows\" and \"must precede\" both need direction. Dropping it discards "
             "the information the model existed to carry."),
        ],
        "standard": ("Finish when you can state what a vertex and an edge are before "
                     "anything else.",
                     "Model \"which pairs of countries share a land border\" as a graph. "
                     "Say what the vertices are, what an edge means, and whether the graph "
                     "is simple &mdash; then ask what the degree of a vertex tells you."),
        "note": "Graph theory begins with Euler's 1736 paper on the bridges of Königsberg, "
                "which lesson 7 revisits. He solved it by discarding the map entirely and "
                "keeping only which land masses were connected &mdash; the first abstraction "
                "of this kind.",
    },
    # ---------------------------------------------------------------- 02
    {
        "slug": "degree-and-the-handshake-theorem",
        "title": "Degree and the Handshake Theorem",
        "module": "Basics",
        "one_line": "The degrees sum to twice the edges — always.",
        "summary": (
            "Each edge contributes 2 to the total degree, so `Σ deg(v) = 2|E|`. The "
            "immediate corollary &mdash; the number of odd-degree vertices is even "
            "&mdash; is used throughout the course."
        ),
        "key": [
            "deg(v) = number of edges at v",
            "Σ_{v} deg(v) = 2|E|                    the handshake theorem",
            "the number of ODD-degree vertices is EVEN",
            "degree sequence: the degrees, sorted",
        ],
        "key_label": "One identity, one corollary",
        "concepts_intro": (
            "The theorem is a double count and its corollary rules out whole families of "
            "graphs at a glance."
        ),
        "concepts": [
            ("Every edge has two ends",
             "So counting (vertex, incident edge) pairs by vertex gives the degree sum, "
             "and by edge gives `2|E|`. That is the whole proof."),
            ("Odd degrees come in pairs",
             "The total is even, so an odd number of odd degrees is impossible. This one "
             "line settles many existence questions."),
            ("The degree sequence is an invariant",
             "Isomorphic graphs have the same sorted degrees, so different sequences prove "
             "non-isomorphism. Equal sequences prove nothing."),
        ],
        "read_title": "Degrees",
        "read_intro": "The definition, the theorem, and what it rules out.",
        "body": [
            ("def", ("Degree",
                     "The <strong>degree</strong> `deg(v)` of a vertex is the number of "
                     "edges incident to it. A vertex of degree 0 is "
                     "<strong>isolated</strong>; one of degree 1 is a "
                     "<strong>leaf</strong> or pendant vertex.")),
            ("thm", ("Handshake theorem",
                     "For any graph, `Σ_{v ∈ V} deg(v) = 2|E|`.")),
            ("proof", [
                "Count the <strong>incidences</strong> &mdash; pairs consisting of a vertex "
                "and an edge meeting it &mdash; in two ways.",
                "By vertex: each `v` contributes `deg(v)` incidences, giving `Σ deg(v)`.",
                "By edge: each edge has exactly two ends, giving `2|E|`.",
                "One set counted twice, so the two expressions are equal.",
            ]),
            ("p", "This is a combinatorial proof in the sense of course 4 lesson 13, and "
                  "it is the cleanest example on the path: name the objects, count them "
                  "two ways, conclude."),
            ("thm", ("The handshake corollary",
                     "In any graph, the number of vertices of odd degree is even.")),
            ("proof", [
                "Split the degree sum into even-degree and odd-degree vertices. The total "
                "is `2|E|`, which is even, and the even-degree part is even, so the "
                "odd-degree part is even too.",
                "A sum of odd numbers is even exactly when there are an even number of "
                "them.",
            ]),
            ("example", ("What the corollary rules out",
                         "There is no graph on 5 vertices in which every vertex has degree "
                         "3: that would be five odd degrees, an odd count. There is no "
                         "party of 5 people where everyone shakes exactly 3 hands. The "
                         "argument is one line and does not depend on the structure at all.")),
            ("def", ("Degree sequence, regular graphs",
                     "The <strong>degree sequence</strong> is the list of degrees, usually "
                     "sorted descending. A graph is <strong>`k`-regular</strong> if every "
                     "vertex has degree `k`.")),
            ("thm", ("Regular graphs",
                     "A `k`-regular graph on `n` vertices has `nk/2` edges. It exists only "
                     "if `nk` is even &mdash; so `k`-regular graphs on an odd number of "
                     "vertices require `k` even.")),
            ("h3", "Which sequences are realisable"),
            ("p", "Not every list of numbers is a degree sequence. `(4, 3, 3, 2, 2)` sums "
                  "to 14, so `|E| = 7`, and it turns out to be realisable. "
                  "`(4, 4, 4, 4, 4)` sums to 20 but requires each of five vertices to be "
                  "adjacent to four others &mdash; that is `K₅`, which is fine. "
                  "`(5, 3, 3, 2, 1)` is impossible in a simple graph on five vertices: a "
                  "vertex cannot have degree 5 when only 4 others exist."),
            ("p", "The Erdős&ndash;Gallai theorem gives a complete criterion, and the "
                  "Havel&ndash;Hakimi algorithm constructs a graph when one exists. Both "
                  "are beyond this course; the two necessary conditions above &mdash; even "
                  "sum, and no degree exceeding `n − 1` &mdash; catch most cases."),
        ],
        "lab": ("graph", {
            "algo": "degree", "preset": "cycle", "n": 6,
            "panel_title": "Degrees, and the identity",
            "panel_intro": "Each vertex is labelled with its degree. `Σ deg(v)` and `2|E|` "
                           "are printed together &mdash; toggle any edge and watch both "
                           "move by exactly 2.",
        }),
        "steps_title": "Using degrees",
        "steps_intro": "Sum first; it is often the whole argument.",
        "steps": [
            ("Compute the degree sum",
             "It must be even, and it equals `2|E|`. That is one edge count for free."),
            ("Count the odd degrees",
             "If the count is odd, no such graph exists. This settles many existence "
             "questions before anything is drawn."),
            ("Check no degree exceeds `n − 1`",
             "A vertex in a simple graph on `n` vertices has at most `n − 1` neighbours."),
            ("Use the sequence as an invariant",
             "Different sorted sequences prove two graphs non-isomorphic. Equal sequences "
             "prove nothing, as lesson 5 shows."),
        ],
        "worked": {
            "title": "Three existence questions",
            "intro": ["All three are settled by counting degrees."],
            "lines": [
                "1.  A graph on 7 vertices, every degree 3?",
                "    seven odd degrees — an ODD count.        IMPOSSIBLE",
                "",
                "2.  A graph on 8 vertices, every degree 3?",
                "    eight odd degrees — even.  Σ deg = 24, so |E| = 12.",
                "    The cube graph Q₃ is one.                 POSSIBLE",
                "",
                "3.  A graph on 6 vertices with degrees 5,5,5,5,5,5?",
                "    Σ = 30, |E| = 15 = C(6,2).  That is K₆.   POSSIBLE",
                "",
                "4.  Degrees 5,3,3,2,1 on 5 vertices?",
                "    Σ = 14 is even, but degree 5 needs 5 neighbours",
                "    and only 4 other vertices exist.          IMPOSSIBLE",
            ],
            "after": [
                "Case 4 shows the parity test alone is not sufficient. Two necessary "
                "conditions &mdash; even sum and no degree above `n − 1` &mdash; catch "
                "most impossible sequences, and the full criterion is the "
                "Erdős&ndash;Gallai theorem."
            ],
        },
        "quiz_title": "Degrees",
        "quiz": [
            {"q": "A graph has 10 edges. What is the sum of its degrees?",
             "a": ["10", "20", "5", "cannot be determined"],
             "c": 1,
             "why": "`Σ deg(v) = 2|E| = 20`, regardless of how the edges are arranged."},
            {"q": "Can a graph have exactly three vertices of odd degree?",
             "a": ["Yes", "No — the number of odd-degree vertices is always even",
                   "Only if it is disconnected", "Only if it has loops"],
             "c": 1,
             "why": "The degree sum is even, so the odd degrees must pair up. Three is "
                    "impossible in any graph."},
            {"q": "A 3-regular graph on `n` vertices exists only if:",
             "a": ["`n` is prime", "`n` is even", "`n ≥ 6`", "`n` is odd"],
             "c": 1,
             "why": "`3n` must be even, so `n` must be. `|E| = 3n/2` has to be an integer."},
        ],
        "mistakes": [
            ("Forgetting that `Σ deg = 2|E|`, not `|E|`",
             "Every edge is counted at both ends. Halving is the step that is skipped."),
            ("Assuming any sequence with an even sum is realisable",
             "`(5,3,3,2,1)` has an even sum and is impossible on five vertices. The "
             "maximum-degree condition is separate."),
            ("Using equal degree sequences as proof of isomorphism",
             "They are necessary and not sufficient. Lesson 5 gives two non-isomorphic "
             "graphs with identical sequences."),
        ],
        "standard": ("Finish when you check parity before attempting a construction.",
                     "Decide whether a graph exists with degree sequence "
                     "`(4,4,3,3,2,2)`, and say which test settles it. The sum is 18, so "
                     "`|E| = 9`, and no degree exceeds 5 &mdash; so try to build one."),
        "note": "The handshake theorem is the most reused fact in this course. It supplies "
                "the edge count in lesson 11's tree characterisation, the parity condition "
                "in lesson 7's Euler criterion, and the counting argument in lesson 14's "
                "planarity bound.",
    },
    # ---------------------------------------------------------------- 03
    {
        "slug": "graph-representations",
        "title": "Graph Representations",
        "module": "Basics",
        "one_line": "Adjacency matrix, adjacency list, and what each makes cheap.",
        "summary": (
            "The same graph stored two ways. The matrix answers \"are these adjacent\" "
            "instantly and costs `n²` space; the list is compact and iterates "
            "neighbours quickly. And `Aᵏ` counts walks."
        ),
        "key": [
            "adjacency matrix   n × n,  A[i][j] = 1 if i ~ j",
            "adjacency list     one neighbour list per vertex",
            "matrix: O(1) adjacency test, O(n²) space",
            "Aᵏ[i][j] = number of walks of length k from i to j",
        ],
        "key_label": "Two structures, one graph",
        "concepts_intro": (
            "The choice is a trade between space and which operation is fast, and for "
            "sparse graphs it is not close."
        ),
        "concepts": [
            ("The matrix is symmetric with a zero diagonal",
             "For a simple undirected graph. Symmetry is the relation being symmetric; "
             "the zero diagonal is the absence of loops."),
            ("Lists win for sparse graphs",
             "Most real graphs have `|E|` far below `n²`. A road network with a million "
             "junctions has a few million edges and a matrix would need `10¹²` entries."),
            ("Matrix powers count walks",
             "`Aᵏ[i][j]` is the number of walks of length exactly `k`, because matrix "
             "multiplication sums over the intermediate vertex."),
        ],
        "read_title": "Storing a graph",
        "read_intro": "Both structures, their costs, and the one theorem about powers.",
        "body": [
            ("def", ("Adjacency matrix",
                     "The `n × n` matrix `A` with `A[i][j] = 1` when vertices `i` and `j` "
                     "are adjacent and 0 otherwise. For a simple undirected graph it is "
                     "symmetric with zero diagonal.")),
            ("def", ("Adjacency list",
                     "For each vertex, the list of its neighbours. Total space "
                     "`Θ(n + |E|)`, since each edge appears in two lists.")),
            ("math", [
                "operation                        matrix        list",
                "is u adjacent to v?              O(1)          O(deg u)",
                "iterate the neighbours of v      O(n)          O(deg v)",
                "space                            Θ(n²)         Θ(n + |E|)",
                "add an edge                      O(1)          O(1)",
                "iterate all edges                O(n²)         Θ(n + |E|)",
            ]),
            ("p", "The traversals of lesson 9 iterate neighbours constantly, so an "
                  "adjacency list gives breadth-first search a running time of "
                  "`Θ(n + |E|)` while a matrix gives `Θ(n²)`. On a sparse graph that is "
                  "the difference between linear and quadratic."),
            ("p", "The matrix wins when the graph is dense, when adjacency tests dominate, "
                  "or when the linear algebra of the next theorem is wanted."),
            ("thm", ("Matrix powers count walks",
                     "For a graph with adjacency matrix `A`, the entry `Aᵏ[i][j]` is the "
                     "number of walks of length exactly `k` from vertex `i` to vertex `j`. "
                     "A <strong>walk</strong> may repeat vertices and edges.")),
            ("proof", [
                "By induction on `k`. For `k = 1` the claim is the definition of `A`.",
                "Assume it for `k`. A walk of length `k+1` from `i` to `j` is a walk of "
                "length `k` from `i` to some `t`, followed by an edge from `t` to `j`. "
                "Summing over `t` gives `Σ_t A^k[i][t] · A[t][j]`, which is exactly "
                "`A^{k+1}[i][j]` by the definition of matrix multiplication.",
            ]),
            ("p", "The proof is the definition of matrix multiplication read as a "
                  "combinatorial statement: the sum over the middle index is the sum over "
                  "the intermediate vertex."),
            ("example", ("Counting triangles",
                         "`A³[v][v]` counts closed walks of length 3 from `v` back to "
                         "itself, and each such walk is a triangle traversed from `v`. Each "
                         "triangle gives 6 closed walks &mdash; three starting vertices, two "
                         "directions &mdash; so the number of triangles is "
                         "`(Σ_v A³[v][v]) / 6`, one sixth of the trace of `A³`.")),
            ("p", "That is a genuine algorithm: matrix multiplication counts triangles in "
                  "`O(n^ω)` where `ω &lt; 2.4` is the matrix multiplication exponent, which "
                  "beats the obvious `O(n³)` enumeration. It is one of the standard "
                  "examples of algebra outperforming combinatorics."),
            ("h3", "Other representations"),
            ("ul", [
                "<strong>Edge list.</strong> Just the pairs. Minimal space, and every "
                "query is a scan. Kruskal's algorithm in lesson 13 sorts exactly this.",
                "<strong>Incidence matrix.</strong> Rows are vertices, columns edges, with "
                "a 1 where they meet. Useful in flow problems and rarely elsewhere here.",
            ]),
        ],
        "lab": ("graph", {
            "algo": "walks", "preset": "petersen", "n": 6,
            "panel_title": "`A²`, and what it counts",
            "panel_intro": "The matrix shown is `A²`, whose entries count walks of length "
                           "2. The diagonal of `A²` is the degree sequence, and one sixth "
                           "of the trace of `A³` is the triangle count.",
        }),
        "steps_title": "Choosing a representation",
        "steps_intro": "Ask which operation dominates.",
        "steps": [
            ("Estimate the density",
             "`|E|` near `n²` is dense and favours the matrix; `|E|` near `n` is sparse "
             "and favours lists, usually decisively."),
            ("Ask which query dominates",
             "Repeated adjacency tests favour the matrix; repeated neighbour iteration "
             "favours lists."),
            ("Check the space budget",
             "`n²` entries is impossible past a few tens of thousands of vertices. Real "
             "large graphs are always stored as lists."),
            ("Use powers when counting walks",
             "`Aᵏ` answers walk-counting questions directly, and nothing else does so "
             "cleanly."),
        ],
        "worked": {
            "title": "Walks in a 4-cycle",
            "intro": ["`C₄` with vertices 1–2–3–4–1."],
            "lines": [
                "        0 1 0 1                    2 0 2 0",
                "  A  =  1 0 1 0            A²  =   0 2 0 2",
                "        0 1 0 1                    2 0 2 0",
                "        1 0 1 0                    0 2 0 2",
                "",
                "A²[1][1] = 2:  the walks 1→2→1 and 1→4→1 — which is deg(1).",
                "A²[1][3] = 2:  the walks 1→2→3 and 1→4→3.",
                "A²[1][2] = 0:  no walk of length 2 joins adjacent vertices here,",
                "               because C₄ is bipartite — lesson 6.",
                "",
                "trace(A³) = 0, so C₄ contains no triangle.        ✓",
            ],
            "after": [
                "The zeros in `A²` at adjacent positions are the bipartiteness of "
                "lesson 6 showing up in the algebra: in a bipartite graph every walk of "
                "even length ends on the same side it started, so it can never end at a "
                "neighbour."
            ],
        },
        "quiz_title": "Representations",
        "quiz": [
            {"q": "`A²[i][j]` counts:",
             "a": ["edges between `i` and `j`",
                   "walks of length 2 from `i` to `j`",
                   "paths from `i` to `j`",
                   "the distance from `i` to `j`"],
             "c": 1,
             "why": "Walks, which may repeat vertices. `A²[i][i] = deg(i)`, and those are "
                    "not paths."},
            {"q": "For a sparse graph with a million vertices, you should use:",
             "a": ["an adjacency matrix", "an adjacency list",
                   "either", "an incidence matrix"],
             "c": 1,
             "why": "A matrix would need `10¹²` entries. Lists need `Θ(n + |E|)`, which is "
                    "a few million."},
            {"q": "The adjacency matrix of a simple undirected graph is:",
             "a": ["symmetric with zero diagonal", "upper triangular",
                   "always invertible", "never symmetric"],
             "c": 0,
             "why": "Symmetric because the relation is; zero diagonal because there are no "
                    "loops."},
        ],
        "mistakes": [
            ("Confusing walks with paths",
             "`Aᵏ` counts walks, which may revisit vertices. Counting paths is a much "
             "harder problem with no matrix formula."),
            ("Using a matrix for a large sparse graph",
             "The space is quadratic and almost all of it is zeros. Lists are the default "
             "for anything real."),
            ("Forgetting each edge appears twice in the lists",
             "So the total list length is `2|E|`, not `|E|`. It matters for the space "
             "estimate and for iterating edges without duplication."),
        ],
        "standard": ("Finish when you can predict which structure suits a problem.",
                     "For a road network of a million junctions with an average of three "
                     "roads each, state the space each representation needs and which "
                     "queries each makes cheap. The gap is a factor of about 300 000."),
        "note": "Sparse matrix formats used in practice &mdash; compressed sparse row and "
                "its relatives &mdash; are adjacency lists with the indices packed into "
                "flat arrays. The trade-off in the table is the one every graph library "
                "is designed around.",
    },
    # ---------------------------------------------------------------- 04
    {
        "slug": "paths-and-connectivity",
        "title": "Paths and Connectivity",
        "module": "Structure",
        "one_line": "Walks, paths, cycles, components — and what disconnects a graph.",
        "summary": (
            "Reachability partitions the vertices into components. Cut vertices and "
            "bridges are the single points of failure, and the number of edges needed "
            "for connectivity is exactly `n − 1`."
        ),
        "key": [
            "walk    any sequence of edges;  may repeat",
            "path    a walk with no repeated VERTEX",
            "cycle   a closed path of length ≥ 3",
            "connected: every pair joined by a path",
        ],
        "key_label": "The vocabulary, precisely",
        "concepts_intro": (
            "The three words are used loosely in conversation and precisely here, and "
            "several theorems depend on the distinction."
        ),
        "concepts": [
            ("Walk, path and cycle differ by repetition",
             "A walk may repeat anything; a path repeats no vertex; a cycle is a path "
             "that returns to its start."),
            ("Reachability is an equivalence relation",
             "Reflexive, symmetric and transitive, so by course 2 lesson 8 it partitions "
             "the vertices &mdash; and the blocks are the components."),
            ("Connectivity needs at least `n − 1` edges",
             "Each edge can reduce the component count by at most one, and you start with "
             "`n` components."),
        ],
        "read_title": "Connectivity",
        "read_intro": "The vocabulary, components as classes, and the two kinds of weak point.",
        "body": [
            ("def", ("Walk, path, cycle",
                     "A <strong>walk</strong> is a sequence of vertices with consecutive "
                     "ones adjacent. A <strong>path</strong> is a walk with no repeated "
                     "vertex. A <strong>cycle</strong> is a walk of length at least 3 that "
                     "starts and ends at the same vertex and repeats no other. A graph "
                     "with no cycle is <strong>acyclic</strong>.")),
            ("thm", ("Walks contain paths",
                     "If there is a walk from `u` to `v`, there is a path from `u` to `v`.")),
            ("proof", [
                "Take a shortest walk from `u` to `v`. If it repeated a vertex `w`, the "
                "section between the two visits to `w` could be deleted, giving a shorter "
                "walk &mdash; contradicting minimality. So it repeats no vertex and is a "
                "path.",
            ]),
            ("p", "This small theorem is used constantly: it means questions about "
                  "reachability may be answered with walks, which are easier to build, and "
                  "the answer transfers to paths."),
            ("def", ("Connected, components",
                     "A graph is <strong>connected</strong> if every pair of vertices is "
                     "joined by a path. A <strong>component</strong> is a maximal connected "
                     "subgraph.")),
            ("thm", ("Components partition the vertices",
                     "\"Is joined by a path to\" is an equivalence relation on `V`, and its "
                     "classes are exactly the components.")),
            ("proof", [
                "Reflexive: the length-0 walk joins `v` to itself. Symmetric: reverse the "
                "path. Transitive: concatenate two walks and extract a path by the theorem "
                "above.",
                "By course 2 lesson 8 the classes partition `V`, and each class induces a "
                "maximal connected subgraph.",
            ]),
            ("thm", ("The edge bound",
                     "A connected graph on `n` vertices has at least `n − 1` edges.")),
            ("proof", [
                "Start with `n` vertices and no edges: `n` components. Adding one edge "
                "reduces the number of components by at most 1, since it can merge at most "
                "two.",
                "To reach one component from `n`, at least `n − 1` edges are required.",
            ]),
            ("p", "Lesson 11 shows that `n − 1` edges suffice exactly when the graph is a "
                  "tree, so trees are the minimally connected graphs &mdash; connected, "
                  "and no edge to spare."),
            ("h3", "Weak points"),
            ("def", ("Cut vertex and bridge",
                     "A <strong>cut vertex</strong> is a vertex whose removal increases the "
                     "number of components. A <strong>bridge</strong> is an edge whose "
                     "removal does so.")),
            ("thm", ("Bridges and cycles",
                     "An edge is a bridge if and only if it lies on no cycle.")),
            ("proof", [
                "If `e = uv` lies on a cycle, removing it leaves the rest of that cycle as "
                "a `u`–`v` path, so nothing is disconnected.",
                "If `e` is on no cycle and removing it left `u` and `v` connected, that "
                "path together with `e` would form a cycle &mdash; a contradiction.",
            ]),
            ("p", "So bridges are exactly the edges with no alternative route, which is why "
                  "network designers avoid them: a bridge is a single point of failure with "
                  "no redundancy. In a tree, every edge is a bridge."),
        ],
        "lab": ("graph", {
            "algo": "components", "preset": "tree", "n": 7,
            "panel_title": "Components, coloured",
            "panel_intro": "Each component gets its own colour. Delete an edge of the tree "
                           "preset and the graph splits immediately &mdash; in a tree every "
                           "edge is a bridge.",
        }),
        "steps_title": "Analysing connectivity",
        "steps_intro": "Search from one vertex; repeat for what is left.",
        "steps": [
            ("Search from any vertex",
             "Breadth-first or depth-first (lesson 9). What you reach is its component."),
            ("Repeat from an unvisited vertex",
             "Until every vertex is assigned. The number of searches is the number of "
             "components."),
            ("Find bridges by removal",
             "Remove an edge and re-count components. An edge on no cycle is a bridge, "
             "which is the faster test once cycles are visible."),
            ("Check the edge count",
             "Fewer than `n − 1` edges guarantees disconnection. More does not guarantee "
             "connection."),
        ],
        "worked": {
            "title": "Reading a graph's structure",
            "intro": ["Seven vertices; edges 1–2, 2–3, 3–1, 3–4, 5–6."],
            "lines": [
                "Search from 1:  1 → 2 → 3 → 4        component {1,2,3,4}",
                "Search from 5:  5 → 6                component {5,6}",
                "Vertex 7 unvisited                    component {7}",
                "",
                "   3 components,  |E| = 5,  n = 7",
                "   n − 1 = 6 > 5, so disconnection was guaranteed in advance.",
                "",
                "CUT VERTEX   3 — removing it separates 4 from {1,2}",
                "BRIDGES      3–4  (on no cycle),  5–6  (on no cycle)",
                "             1–2, 2–3, 3–1 are NOT bridges: they lie on the",
                "             triangle 1–2–3.",
            ],
            "after": [
                "The edge count settled the connectivity question before any search: five "
                "edges cannot connect seven vertices. That check is free and it is worth "
                "doing first."
            ],
        },
        "quiz_title": "Connectivity",
        "quiz": [
            {"q": "A path differs from a walk in that:",
             "a": ["it is shorter", "it repeats no vertex",
                   "it is closed", "it uses every edge"],
             "c": 1,
             "why": "Walks may repeat anything. A path repeats no vertex, which forces it "
                    "to repeat no edge either."},
            {"q": "A connected graph on 10 vertices has at least:",
             "a": ["10 edges", "9 edges", "45 edges", "1 edge"],
             "c": 1,
             "why": "`n − 1 = 9`. Each edge reduces the component count by at most one, "
                    "and you start with 10 components."},
            {"q": "An edge is a bridge exactly when:",
             "a": ["it joins two leaves", "it lies on no cycle",
                   "it has the largest weight", "the graph is a tree"],
             "c": 1,
             "why": "On a cycle there is an alternative route, so removal disconnects "
                    "nothing. Off every cycle there is none."},
        ],
        "mistakes": [
            ("Using \"path\" for any route",
             "In this course a path repeats no vertex. Several theorems &mdash; including "
             "the bridge characterisation &mdash; depend on the distinction."),
            ("Assuming enough edges implies connectivity",
             "`n − 1` edges is necessary and not sufficient: a triangle plus two isolated "
             "vertices has enough edges and three components."),
            ("Confusing cut vertices with bridges",
             "One is a vertex and the other an edge, and neither implies the other. A "
             "vertex may be a cut vertex with no bridge incident to it."),
        ],
        "standard": ("Finish when you can find the components and the bridges by hand.",
                     "Take a graph on eight vertices with ten edges, identify its "
                     "components, and list its bridges by checking which edges lie on no "
                     "cycle. Both are one search each."),
        "note": "Higher connectivity &mdash; how many vertices or edges must be removed to "
                "disconnect a graph &mdash; is measured by the connectivity `κ(G)` and edge "
                "connectivity `λ(G)`, and Menger's theorem relates them to the number of "
                "disjoint paths between vertices. It is the natural sequel to this lesson.",
    },
    # ---------------------------------------------------------------- 05
    {
        "slug": "graph-isomorphism",
        "title": "Subgraphs and Graph Isomorphism",
        "module": "Structure",
        "one_line": "When two different drawings are the same graph.",
        "summary": (
            "An isomorphism is a relabelling preserving adjacency. Proving two graphs "
            "isomorphic means exhibiting one; proving they are not means finding an "
            "invariant that differs."
        ),
        "key": [
            "isomorphism: a bijection f : V₁ → V₂ with  u~v  ⟺  f(u)~f(v)",
            "to PROVE isomorphic: exhibit the bijection",
            "to DISPROVE: find an invariant that differs",
            "invariants: |V|, |E|, degree sequence, cycle lengths, connectivity",
        ],
        "key_label": "Same graph, different labels",
        "concepts_intro": (
            "Isomorphism is course 2's bijection with a structure-preserving condition "
            "attached."
        ),
        "concepts": [
            ("It is a bijection that preserves adjacency",
             "Both directions: adjacent vertices map to adjacent vertices, and "
             "non-adjacent to non-adjacent."),
            ("Invariants disprove, they never prove",
             "Matching every invariant you can think of is not a proof of isomorphism. "
             "Only an explicit bijection is."),
            ("Nobody knows how hard the problem is",
             "Graph isomorphism is not known to be in P and not known to be NP-complete "
             "&mdash; an unusual position for a natural problem."),
        ],
        "read_title": "Isomorphism",
        "read_intro": "The definition, the invariants, and how to argue each way.",
        "body": [
            ("def", ("Subgraph",
                     "`H` is a <strong>subgraph</strong> of `G` when `V(H) ⊆ V(G)` and "
                     "`E(H) ⊆ E(G)`. It is <strong>induced</strong> by a vertex set `S` "
                     "when it contains every edge of `G` with both ends in `S`.")),
            ("def", ("Isomorphism",
                     "Graphs `G₁` and `G₂` are <strong>isomorphic</strong>, written "
                     "`G₁ ≅ G₂`, when there is a bijection `f : V₁ → V₂` such that `u` and "
                     "`v` are adjacent in `G₁` if and only if `f(u)` and `f(v)` are "
                     "adjacent in `G₂`.")),
            ("p", "Isomorphic graphs are the same graph with different labels and "
                  "different drawings. Every property expressible in terms of adjacency "
                  "alone &mdash; connectivity, cycle lengths, degrees, colourability "
                  "&mdash; is shared by isomorphic graphs."),
            ("h3", "Invariants"),
            ("math", [
                "number of vertices",
                "number of edges",
                "degree sequence (sorted)",
                "number of components",
                "lengths of the cycles present",
                "bipartite or not",
                "number of triangles       ( = trace(A³)/6 )",
                "connectivity, chromatic number, planarity",
            ]),
            ("p", "Any difference in any invariant proves non-isomorphism, and this is the "
                  "practical method: check the cheap invariants first and stop at the first "
                  "disagreement. Agreement on all of them proves nothing."),
            ("example", ("Same degree sequence, not isomorphic",
                         "Take `G₁` to be two disjoint triangles and `G₂` to be a 6-cycle. "
                         "Both have 6 vertices, both have 6 edges, and both are 2-regular "
                         "with degree sequence "
                         "`(2,2,2,2,2,2)`. They are not isomorphic: `G₁` has two components "
                         "and `G₂` has one, and `G₁` contains 3-cycles while `G₂`'s only "
                         "cycle has length 6.")),
            ("p", "That example is the standard warning. The degree sequence is the "
                  "invariant people reach for first, and it is genuinely weak &mdash; there "
                  "are non-isomorphic pairs agreeing on every invariant in the table above."),
            ("h3", "Proving isomorphism"),
            ("p", "The only proof is an explicit bijection, verified on every edge. A "
                  "practical strategy is to use the degrees to narrow the possibilities: a "
                  "vertex of degree 5 must map to a vertex of degree 5, and often that "
                  "pins most of the map."),
            ("example", ("A bijection",
                         "Take the 4-cycle labelled `1–2–3–4–1` and the graph on `a,b,c,d` "
                         "with edges `ab, bd, dc, ca`. Map `1→a, 2→b, 3→d, 4→c`. Check all "
                         "four edges: `12→ab ✓`, `23→bd ✓`, `34→dc ✓`, `41→ca ✓`. And there "
                         "are four edges in each, so no non-edge maps to an edge. "
                         "Isomorphic.")),
            ("h3", "How hard is the problem?"),
            ("p", "Deciding isomorphism has no known polynomial-time algorithm and is not "
                  "known to be NP-complete. It sits in an unusual middle position that very "
                  "few natural problems occupy. Babai announced a quasi-polynomial "
                  "algorithm in 2015 &mdash; running in time `exp((log n)^{O(1)})`, faster "
                  "than exponential and slower than polynomial."),
            ("p", "In practice, isomorphism testers handle graphs with thousands of "
                  "vertices routinely, because real graphs have structure the worst case "
                  "does not. This is the same gap between worst-case hardness and practical "
                  "difficulty that course 1 noted for SAT."),
        ],
        "lab": ("graph", {
            "algo": "degree", "preset": "bipartite", "n": 6,
            "panel_title": "Compare invariants",
            "panel_intro": "Build a graph, note its degree sequence and component count, "
                           "then build a different graph with the same degrees. If you "
                           "manage it, the sequence has proved nothing.",
        }),
        "steps_title": "Deciding isomorphism",
        "steps_intro": "Try to disprove first; it is much cheaper.",
        "steps": [
            ("Compare the cheap invariants",
             "Vertex count, edge count, degree sequence. Any difference ends the question "
             "immediately."),
            ("Compare structural invariants",
             "Component count, cycle lengths, triangle count, bipartiteness. These catch "
             "most remaining pairs."),
            ("If all agree, construct a bijection",
             "Use degrees to constrain it: degree-`k` vertices must map to degree-`k` "
             "vertices, and neighbourhoods must correspond."),
            ("Verify every edge",
             "Both directions. A bijection preserving edges but mapping a non-edge to an "
             "edge is not an isomorphism &mdash; though for graphs with equal edge counts, "
             "preserving edges is enough."),
        ],
        "worked": {
            "title": "Are these isomorphic?",
            "intro": ["`G₁`: 6-cycle. `G₂`: two disjoint triangles."],
            "lines": [
                "|V|              6      6         same",
                "|E|              6      6         same",
                "degree sequence  222222 222222    same",
                "components       1      2         DIFFERENT",
                "",
                "   ⟹ NOT isomorphic.",
                "",
                "A second invariant confirms it:",
                "   shortest cycle length   6      3      DIFFERENT",
                "",
                "Three invariants agreed and two disagreed. Either disagreement",
                "is a complete proof; the three agreements were worth nothing.",
            ],
            "after": [
                "This asymmetry is the whole method. Disproving is a matter of finding one "
                "difference, and proving requires exhibiting a bijection &mdash; which is "
                "why every practical algorithm spends its time trying to disprove."
            ],
        },
        "quiz_title": "Isomorphism",
        "quiz": [
            {"q": "Two graphs have the same degree sequence. Are they isomorphic?",
             "a": ["Yes", "Not necessarily", "Only if connected", "Only if regular"],
             "c": 1,
             "why": "Two triangles and a 6-cycle share the sequence `(2,2,2,2,2,2)` and "
                    "differ in component count and cycle length."},
            {"q": "To prove two graphs isomorphic you must:",
             "a": ["show all invariants match",
                   "exhibit a bijection preserving adjacency both ways",
                   "count the edges",
                   "draw them the same way"],
             "c": 1,
             "why": "Invariants can only disprove. The bijection is the definition and the "
                    "only proof."},
            {"q": "The graph isomorphism problem is:",
             "a": ["known to be in P", "known to be NP-complete",
                   "neither known to be in P nor known to be NP-complete",
                   "undecidable"],
             "c": 2,
             "why": "An unusual middle position. Babai's 2015 algorithm is "
                    "quasi-polynomial, between the two."},
        ],
        "mistakes": [
            ("Treating matching invariants as proof",
             "They are necessary conditions. Only an explicit bijection establishes "
             "isomorphism."),
            ("Assuming similar drawings mean isomorphic graphs",
             "The drawing carries no information. `K₄` drawn as a square with diagonals "
             "and as a triangle with a centre are the same graph."),
            ("Checking only that edges map to edges",
             "For graphs with equal edge counts that suffices, and stating why is part of "
             "the argument. In general both directions must be checked."),
        ],
        "standard": ("Finish when you reach for invariants before attempting a bijection.",
                     "Given two graphs on eight vertices, list the invariants you would "
                     "check and in what order. Cheapest first, and stop at the first "
                     "disagreement."),
        "note": "Isomorphism is why graph theory speaks of \"the\" cycle `Cₙ` and \"the\" "
                "complete graph `Kₙ`. There are many labelled graphs with that structure "
                "and exactly one up to isomorphism, and the theorems are about the "
                "structure.",
    },
    # ---------------------------------------------------------------- 06
    {
        "slug": "bipartite-graphs",
        "title": "Bipartite Graphs",
        "module": "Structure",
        "one_line": "Two-colourable, and equivalently free of odd cycles.",
        "summary": (
            "A bipartite graph splits into two independent sets with every edge crossing "
            "between them. That is exactly the graphs with no odd cycle, and the "
            "equivalence is proved by a colouring argument."
        ),
        "key": [
            "bipartite: V = X ∪ Y disjoint, every edge crosses X–Y",
            "bipartite  ⟺  2-colourable  ⟺  NO ODD CYCLE",
            "testable in one breadth-first search",
            "K_{m,n} is bipartite;  any odd cycle is not",
        ],
        "key_label": "Three equivalent descriptions",
        "concepts_intro": (
            "Three characterisations of one class, and the third is what makes the class "
            "easy to test for."
        ),
        "concepts": [
            ("Two sides, edges only between",
             "No edge within a side. The sides are <em>independent sets</em>, and the "
             "graph is exactly a relation between two populations."),
            ("Odd cycles are the only obstruction",
             "A graph is bipartite exactly when every cycle has even length. Nothing else "
             "can prevent it."),
            ("The test is one search",
             "Two-colour greedily by breadth-first search; a conflict is an odd cycle. "
             "Linear time, unlike almost every other question in this course."),
        ],
        "read_title": "Bipartite graphs",
        "read_intro": "Definition, the odd-cycle theorem, the test, and the applications.",
        "body": [
            ("def", ("Bipartite",
                     "A graph is <strong>bipartite</strong> when its vertices can be "
                     "partitioned into sets `X` and `Y` such that every edge joins a vertex "
                     "of `X` to one of `Y`. Equivalently, `X` and `Y` are independent sets.")),
            ("example", ("Bipartite and not",
                         "`C₄`, `C₆` and every tree are bipartite. `C₃`, `C₅` and `Kₙ` for "
                         "`n ≥ 3` are not. The complete bipartite graph `K_{m,n}` is "
                         "bipartite by construction and has `mn` edges.")),
            ("thm", ("The odd-cycle characterisation",
                     "A graph is bipartite if and only if it contains no cycle of odd "
                     "length.")),
            ("proof", [
                "<strong>(⟹)</strong> Suppose the graph is bipartite and consider any "
                "cycle. Each step crosses from one side to the other, so after an odd "
                "number of steps you are on the opposite side from where you started. A "
                "cycle returns to its start, so its length must be even.",
                "<strong>(⟸)</strong> Suppose there is no odd cycle. Work within one "
                "component; pick a vertex `r` and put each vertex in `X` or `Y` according "
                "to whether its distance from `r` is even or odd.",
                "If some edge joined two vertices of the same class, the two paths from "
                "`r` to its ends, together with that edge, would give a closed walk of odd "
                "length, and a closed walk of odd length contains an odd cycle. So no such "
                "edge exists and the partition works. Repeat for each component.",
            ]),
            ("p", "The second direction is the substantive one, and the construction it "
                  "uses is exactly the algorithm: colour by parity of distance from a root. "
                  "The proof and the test are the same thing."),
            ("thm", ("The test",
                     "Breadth-first search from each unvisited vertex, colouring each "
                     "vertex opposite to its parent. If an edge is ever found joining two "
                     "vertices of the same colour, the graph is not bipartite and that edge "
                     "closes an odd cycle. Otherwise the colouring is a bipartition. The "
                     "cost is `Θ(n + |E|)`.")),
            ("p", "Contrast that with lesson 12's chromatic number, where deciding "
                  "3-colourability is NP-complete. Two colours is easy and three is hard, "
                  "and the boundary is exactly here."),
            ("h3", "Matching"),
            ("def", ("Matching",
                     "A <strong>matching</strong> is a set of edges no two of which share "
                     "a vertex. In a bipartite graph, a matching pairs up members of `X` "
                     "with members of `Y`.")),
            ("thm", ("Hall's marriage theorem",
                     "A bipartite graph with parts `X` and `Y` has a matching saturating "
                     "`X` if and only if every subset `S ⊆ X` has at least `|S|` neighbours "
                     "in `Y`.")),
            ("p", "The condition is obviously necessary &mdash; `|S|` vertices need `|S|` "
                  "distinct partners &mdash; and the content of the theorem is that it is "
                  "sufficient. Note the resemblance to the pigeonhole principle: if some "
                  "set of `k` vertices has fewer than `k` neighbours, two of them must "
                  "share, and no matching exists."),
            ("h3", "Where bipartite graphs appear"),
            ("ul", [
                "<strong>Assignment problems.</strong> Workers and jobs, students and "
                "projects, applicants and posts &mdash; anything pairing two populations.",
                "<strong>Scheduling.</strong> Rooms and time slots.",
                "<strong>Recommendation.</strong> Users and items, with edges for "
                "interactions.",
                "<strong>Testing for structure.</strong> Bipartiteness is a cheap and "
                "informative property, and its failure exhibits an odd cycle.",
            ]),
        ],
        "lab": ("graph", {
            "algo": "bipartite", "preset": "cycle", "n": 6,
            "panel_title": "Two-colour, or find the odd cycle",
            "panel_intro": "Set the vertex count to 6 for an even cycle, then to 5. The "
                           "odd cycle cannot be two-coloured, and the lab names the edge "
                           "where the colouring fails.",
        }),
        "steps_title": "Testing bipartiteness",
        "steps_intro": "Colour by breadth-first search; a conflict is the proof it fails.",
        "steps": [
            ("Pick an unvisited vertex and colour it",
             "Say colour 0. Any starting choice works; the two colourings differ by "
             "swapping."),
            ("Colour each neighbour the opposite colour",
             "Proceeding by breadth-first search, so each vertex is coloured when first "
             "reached."),
            ("Check every edge",
             "An edge joining two vertices of the same colour means no bipartition exists, "
             "and it closes an odd cycle."),
            ("Repeat for every component",
             "Each component is coloured independently. A disconnected graph is bipartite "
             "exactly when all its components are."),
        ],
        "worked": {
            "title": "Two cycles",
            "intro": ["`C₆` and `C₅`, coloured by distance parity from vertex 1."],
            "lines": [
                "C₆:  1–2–3–4–5–6–1",
                "   distance from 1:  0 1 2 3 2 1",
                "   colours:          X Y X Y X Y",
                "   every edge crosses X–Y                     BIPARTITE",
                "   X = {1,3,5}   Y = {2,4,6}",
                "",
                "C₅:  1–2–3–4–5–1",
                "   distance from 1:  0 1 2 2 1",
                "   colours:          X Y X X Y",
                "   the edge 3–4 joins two X vertices           NOT BIPARTITE",
                "",
                "   That edge closes the odd cycle 1–2–3–4–5–1, of length 5.",
            ],
            "after": [
                "The failing edge is not an accident of the colouring order: any attempt "
                "produces a conflict somewhere, because the obstruction is the odd cycle "
                "and it is present regardless of where the search starts."
            ],
        },
        "quiz_title": "Bipartite",
        "quiz": [
            {"q": "Which is bipartite?",
             "a": ["`K₃`", "`C₅`", "`C₄`", "`K₄`"],
             "c": 2,
             "why": "`C₄` splits into alternate vertices. The other three all contain "
                    "triangles or odd cycles."},
            {"q": "A graph is bipartite if and only if it has no:",
             "a": ["cycles", "odd cycles", "even cycles", "triangles"],
             "c": 1,
             "why": "Odd cycles are the only obstruction. Even cycles are fine, and "
                    "\"no triangles\" is weaker &mdash; `C₅` is triangle-free and not "
                    "bipartite."},
            {"q": "Testing bipartiteness costs:",
             "a": ["exponential time", "`Θ(n + |E|)` — one search",
                   "`Θ(n³)`", "it is NP-complete"],
             "c": 1,
             "why": "One breadth-first search with a parity colouring. Three-colourability, "
                    "by contrast, is NP-complete."},
        ],
        "mistakes": [
            ("Assuming triangle-free means bipartite",
             "`C₅` has no triangle and is not bipartite. Every odd cycle is an obstruction, "
             "not only the shortest one."),
            ("Testing only one component",
             "A disconnected graph is bipartite exactly when every component is. Each needs "
             "its own colouring."),
            ("Reporting failure without the odd cycle",
             "The conflicting edge closes one, and naming it turns \"not bipartite\" into a "
             "proof."),
        ],
        "standard": ("Finish when you can produce the odd cycle from a failed colouring.",
                     "Two-colour a graph of your own until it fails, then trace the paths "
                     "from the root to both ends of the offending edge. Together with the "
                     "edge they form the odd cycle."),
        "note": "The gap between 2-colouring and 3-colouring is one of the sharpest in "
                "complexity theory: the first is linear time and the second is NP-complete. "
                "Lesson 12 returns to it, and course 8 explains what NP-complete means.",
    },
    # ---------------------------------------------------------------- 07
    {
        "slug": "euler-and-hamilton",
        "title": "Euler and Hamilton Paths",
        "module": "Traversal",
        "one_line": "Every edge once, or every vertex once — and the two are nothing alike.",
        "summary": (
            "An Euler circuit uses every edge once and exists exactly when the graph is "
            "connected with all degrees even. A Hamilton circuit visits every vertex "
            "once and has no such criterion &mdash; deciding it is NP-complete."
        ),
        "key": [
            "EULER    every EDGE once      criterion: connected, all degrees even",
            "         Euler PATH: exactly two odd-degree vertices",
            "HAMILTON every VERTEX once    NO simple criterion — NP-complete",
            "The problems look alike. They are not.",
        ],
        "key_label": "One easy, one hard",
        "concepts_intro": (
            "Two similar-sounding questions with completely different answers, and the "
            "contrast is the point of the lesson."
        ),
        "concepts": [
            ("Euler is decided by the degrees",
             "One pass over the vertices. Even degrees and connectivity are necessary and "
             "sufficient, which is unusually clean."),
            ("The degree condition has an obvious reason",
             "Every visit to a vertex uses two edge-ends, one in and one out. So a circuit "
             "requires every degree even."),
            ("Hamilton has no such criterion",
             "Only sufficient conditions (Dirac, Ore) and no characterisation. Deciding it "
             "is NP-complete, which course 8 defines."),
        ],
        "read_title": "Euler and Hamilton",
        "read_intro": "Both definitions, Euler's theorem with its proof, and the contrast.",
        "body": [
            ("def", ("Euler path and circuit",
                     "An <strong>Euler path</strong> uses every edge of the graph exactly "
                     "once. An <strong>Euler circuit</strong> is an Euler path that returns "
                     "to its starting vertex.")),
            ("thm", ("Euler's theorem",
                     "A connected graph has an Euler circuit if and only if every vertex "
                     "has even degree. It has an Euler path but no circuit if and only if "
                     "exactly two vertices have odd degree, and any such path starts at one "
                     "and ends at the other.")),
            ("proof", [
                "<strong>Necessity.</strong> Every time the circuit enters a vertex it "
                "leaves again, using two edges at that vertex; the start and end are the "
                "same vertex, so its first and last edges pair up too. Every edge is used "
                "exactly once, so every degree is even.",
                "<strong>Sufficiency.</strong> Suppose the graph is connected with all "
                "degrees even. Start anywhere and walk, never repeating an edge. Even "
                "degrees mean that whenever you enter a vertex other than the start there "
                "is an unused edge to leave by, so the walk can only get stuck at the "
                "start &mdash; producing a circuit.",
                "If that circuit misses some edges, connectivity gives a vertex `v` on it "
                "with unused edges. The unused edges still form a graph of even degrees, so "
                "the same argument gives a second circuit through `v`, which can be spliced "
                "into the first. Repeating exhausts the edges.",
            ]),
            ("p", "That is a complete criterion and an algorithm: check the degrees, and "
                  "the splicing argument (Hierholzer's algorithm) constructs the circuit in "
                  "linear time."),
            ("example", ("The bridges of Königsberg",
                         "Four land masses joined by seven bridges. The question &mdash; "
                         "can one walk crossing every bridge exactly once? &mdash; is "
                         "whether an Euler path exists. The four vertices have degrees 5, "
                         "3, 3 and 3: four vertices of odd degree, and a path allows at most "
                         "two. No such walk exists, and Euler proved it in 1736.")),
            ("p", "Notice how little the argument needs. The geometry, the distances and "
                  "the layout were all discarded; only the degrees mattered. That "
                  "abstraction is the founding move of graph theory."),
            ("h3", "Hamilton"),
            ("def", ("Hamilton path and circuit",
                     "A <strong>Hamilton path</strong> visits every vertex exactly once. A "
                     "<strong>Hamilton circuit</strong> is a Hamilton path returning to its "
                     "start.")),
            ("p", "There is no known criterion. Some sufficient conditions exist:"),
            ("thm", ("Dirac's theorem",
                     "If `n ≥ 3` and every vertex has degree at least `n/2`, the graph has "
                     "a Hamilton circuit.")),
            ("thm", ("Ore's theorem",
                     "If `n ≥ 3` and `deg(u) + deg(v) ≥ n` for every pair of non-adjacent "
                     "`u, v`, the graph has a Hamilton circuit.")),
            ("p", "Both are sufficient and neither is necessary: `Cₙ` has a Hamilton "
                  "circuit and every degree 2, far below `n/2`. There is no known condition "
                  "that is both."),
            ("thm", ("Hamiltonicity is NP-complete",
                     "Deciding whether a graph has a Hamilton circuit is NP-complete. No "
                     "polynomial-time algorithm is known, and one would imply P = NP.")),
            ("math", [
                "                    Euler                  Hamilton",
                "covers              every EDGE once        every VERTEX once",
                "criterion           degrees all even       none known",
                "deciding it         linear time            NP-complete",
                "constructing it     Hierholzer, linear     exponential in general",
            ]),
            ("p", "This table is the lesson. Two questions that a reader would expect to be "
                  "of similar difficulty are on opposite sides of the sharpest boundary in "
                  "computer science, and nothing in the statements reveals which is which."),
        ],
        "lab": ("graph", {
            "algo": "euler", "preset": "cycle", "n": 6,
            "panel_title": "Both questions, on your graph",
            "panel_intro": "The Euler verdict comes from counting odd degrees. Switch to "
                           "Hamilton and the lab searches orderings exhaustively &mdash; "
                           "which is why the vertex count stops at 8.",
        }),
        "steps_title": "Deciding both questions",
        "steps_intro": "Euler is a degree count. Hamilton is a search.",
        "steps": [
            ("For Euler, check connectivity and count odd degrees",
             "Zero odd degrees gives a circuit; exactly two give a path; anything else "
             "gives neither."),
            ("Construct the Euler circuit by splicing",
             "Walk until stuck, then find a vertex with unused edges and splice in a "
             "second circuit. That is Hierholzer's algorithm."),
            ("For Hamilton, check the sufficient conditions",
             "Dirac and Ore. If either holds, a circuit exists. If neither holds, nothing "
             "follows."),
            ("Otherwise search, and expect it to be slow",
             "Backtracking over orderings. For `n` beyond about 20 this is impractical, and "
             "no better general method is known."),
        ],
        "worked": {
            "title": "Königsberg, and a fix",
            "intro": ["Four land masses `A, B, C, D` with seven bridges."],
            "lines": [
                "degrees:   A: 5     B: 3     C: 3     D: 3",
                "",
                "odd-degree vertices: all four.",
                "An Euler PATH allows at most 2;  a CIRCUIT allows 0.",
                "   ⟹  neither exists.  No such walk is possible.",
                "",
                "ADD ONE BRIDGE between B and C:",
                "   degrees:  A: 5   B: 4   C: 4   D: 3",
                "   now exactly two odd (A and D)  ⟹  an Euler PATH exists,",
                "   and it must start at A and end at D.",
                "",
                "ADD A SECOND, between A and D:",
                "   degrees:  A: 6   B: 4   C: 4   D: 4",
                "   all even  ⟹  an Euler CIRCUIT exists, from anywhere.",
            ],
            "after": [
                "The bridges added were chosen to fix parity, and any bridge joining two "
                "odd-degree vertices would have done. That is the practical form of the "
                "theorem: the obstruction is parity, and parity is what you repair."
            ],
        },
        "quiz_title": "Euler and Hamilton",
        "quiz": [
            {"q": "A connected graph has exactly two odd-degree vertices. It has:",
             "a": ["an Euler circuit", "an Euler path but no circuit",
                   "neither", "a Hamilton circuit"],
             "c": 1,
             "why": "Two odd degrees give a path, which must start at one and end at the "
                    "other. A circuit requires zero."},
            {"q": "Deciding whether a Hamilton circuit exists is:",
             "a": ["a degree count", "linear time",
                   "NP-complete, with no known simple criterion", "always possible"],
             "c": 2,
             "why": "No characterisation is known. Dirac and Ore give sufficient conditions "
                    "only, and neither is necessary."},
            {"q": "Why must every degree be even for an Euler circuit?",
             "a": ["the graph must be connected",
                   "each visit to a vertex uses two edge-ends, one in and one out",
                   "even numbers are easier",
                   "it need not be"],
             "c": 1,
             "why": "The edges at each vertex pair up into entries and exits, so their "
                    "count is even."},
        ],
        "mistakes": [
            ("Confusing the two problems",
             "Euler covers edges; Hamilton covers vertices. The difficulty is completely "
             "different and nothing in the wording signals it."),
            ("Applying Dirac's condition in reverse",
             "It is sufficient, not necessary. `Cₙ` has degree 2 everywhere and a Hamilton "
             "circuit."),
            ("Forgetting connectivity in Euler's criterion",
             "Two disjoint even-degree cycles have all degrees even and no Euler circuit. "
             "The edges must lie in one component."),
        ],
        "standard": ("Finish when you can settle Euler in one pass and say why Hamilton is "
                     "different.",
                     "For a graph of your own, decide the Euler question by counting "
                     "degrees, then attempt Hamilton by hand and notice what changes: one "
                     "is a check, the other is a search."),
        "note": "The travelling salesman problem is Hamilton with weights: find the "
                "cheapest Hamilton circuit. It is the canonical hard optimisation problem, "
                "and course 8 lesson 11 places it precisely.",
    },
]
