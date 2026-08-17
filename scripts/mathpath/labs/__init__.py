"""The lab registry.

A lesson names a lab by key and hands it a config. Adding a lab means adding a
function here; a lesson can never inline its own widget, which is the rule that
keeps 106 lessons from becoming 106 slightly different implementations of the
same control.
"""

from . import algorithms, counting, graph, induction, logic, number, probability, sets
from .common import QUIZ_MARKUP, QUIZ_SCRIPT, Lab, cfg_literal

REGISTRY = {
    "truth_table": logic.truth_table,
    "quantifier": logic.quantifier,
    "sets": sets.set_lab,
    "relation": sets.relation_lab,
    "function": sets.function_lab,
    "counting": counting.counting_lab,
    "pascal": counting.pascal_lab,
    "inclusion_exclusion": counting.inclusion_exclusion,
    "induction": induction.induction_lab,
    "recurrence": induction.recurrence_lab,
    "number": number.number_lab,
    "rsa": number.rsa_lab,
    "graph": graph.graph_lab,
    "probability": probability.probability_lab,
    "distribution": probability.distribution_lab,
    "algorithm": algorithms.algorithm_lab,
}


def build(key, cfg):
    if key not in REGISTRY:
        raise KeyError("no lab named %r; known labs: %s" % (key, ", ".join(sorted(REGISTRY))))
    return REGISTRY[key](cfg or {})


__all__ = ["REGISTRY", "build", "Lab", "QUIZ_MARKUP", "QUIZ_SCRIPT", "cfg_literal"]
