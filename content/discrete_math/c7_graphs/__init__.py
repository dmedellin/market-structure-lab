"""Course 7 — Graphs and Trees."""

from . import part_a, part_b

COURSE = {
    "slug": "graphs-and-trees",
    "title": "Graphs and Trees",
    "level": "Intermediate",
    "summary": (
        "Vertices and edges: degree and the handshake theorem, representations, "
        "connectivity, isomorphism, bipartite graphs, Euler and Hamilton, search, "
        "shortest paths, trees, spanning trees, colouring and planarity."
    ),
    "blurb": (
        "The discrete structure that models everything with a relation on it: networks, "
        "dependencies, maps, molecules, schedules. Every theorem in this course is a "
        "claim about all graphs, and the lab lets you try to break each one."
    ),
    "key": [
        "Σ deg(v) = 2|E|                     the handshake theorem",
        "tree  ⟺  connected and |E| = |V| − 1",
        "Euler circuit  ⟺  connected and every degree even",
        "|V| − |E| + |F| = 2                 Euler's formula, planar graphs",
    ],
    "assumes_short": "Courses 1–4",
    "assumes_long": "proof, sets, relations and counting",
    "outcomes_intro": (
        "By the end you can model a problem as a graph, run the standard algorithms, "
        "and know which questions have easy criteria and which do not."
    ),
    "outcomes": [
        ("Read and build the representations",
         "Adjacency matrix, adjacency list and drawing &mdash; and know which makes a "
         "given question easy."),
        ("Apply the standard criteria",
         "Euler's degree condition, bipartiteness as the absence of odd cycles, and the "
         "tree characterisation, each with the proof behind it."),
        ("Run the algorithms",
         "Breadth-first and depth-first search, Dijkstra, Kruskal and greedy colouring, "
         "and say what each guarantees."),
        ("Tell easy problems from hard ones",
         "Euler circuits are decided in one pass; Hamilton circuits are NP-complete. The "
         "problems look alike and are not."),
    ],
    "syllabus_intro": (
        "Lessons 1 to 5 are the basics, 6 to 10 are traversals and paths, 11 to 13 are "
        "trees, and 14 is planarity."
    ),
    "how_to": [
        "Use the workbench adversarially. Every theorem here is a claim about all "
        "graphs, and the fastest way to understand one is two minutes spent trying to "
        "build a counterexample.",
        "Draw the small cases. Graph theory is one of the few parts of mathematics where "
        "the picture is the object, and most of these proofs were found by drawing.",
        "Notice which criteria are one-pass checks and which are searches. That "
        "distinction is what course 8 formalises, and it is visible here first.",
    ],
    "not_covered": [
        "Directed graphs beyond passing mentions. Everything here is undirected unless "
        "stated; digraphs, strong connectivity and topological sorting are noted where "
        "they matter and not developed.",
        "Network flow, matching algorithms beyond the bipartite criterion, and the "
        "algorithmic side of matching.",
        "Spectral graph theory, random graphs and extremal graph theory, each of which "
        "is a course in itself.",
    ],
    "footer_lead": (
        "Every algorithm on this course runs in your browser against the graph you "
        "built, and every verdict names the vertex, edge or pair that decides it. The "
        "graph workbench caps at eight vertices for one reason worth noticing: the "
        "Hamilton search is exhaustive, and 8! is where exhaustive stops being instant."
    ),
    "lessons": part_a.LESSONS + part_b.LESSONS,
}
