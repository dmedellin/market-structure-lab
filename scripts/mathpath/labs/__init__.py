"""The lab registry.

A lesson names a lab by key and hands it a config. Adding a lab means adding a
function here; a lesson can never inline its own widget, which is the rule that
keeps 106 lessons from becoming 106 slightly different implementations of the
same control.
"""

from . import (
    algebra_basics,
    algebra_equations,
    algebra_expo,
    algebra_functions,
    algebra_polynomials,
    algebra_quadratic,
    algebra_rational,
    algebra_systems,
    algorithms,
    counting,
    graph,
    induction,
    logic,
    number,
    probability,
    sets,
)
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

    # The algebra path. Its labs share the exact-arithmetic core in
    # algebra_core.py: rationals over BigInt, polynomials over those
    # rationals, an expression parser for what a reader types, and an SVG
    # grapher that samples the function rather than storing a shape.
    "expression": algebra_basics.expression_lab,
    "realline": algebra_basics.realline_lab,
    "exponents": algebra_basics.exponents_lab,
    "radicals": algebra_basics.radicals_lab,
    "equation": algebra_equations.equation_lab,
    "inequality": algebra_equations.inequality_lab,
    "expo": algebra_expo.expo_lab,
    "logarithm": algebra_expo.logarithm_lab,
    "line": algebra_functions.line_lab,
    "grapher": algebra_functions.grapher_lab,
    "transform": algebra_functions.transform_lab,
    "funcops": algebra_functions.funcops_lab,
    "polynomial": algebra_polynomials.polynomial_lab,
    "factoring": algebra_polynomials.factoring_lab,
    "rationalfn": algebra_rational.rationalfn_lab,
    "complex": algebra_rational.complex_lab,
    "system": algebra_systems.system_lab,
    "matrix": algebra_systems.matrix_lab,
    "sequence": algebra_systems.sequence_lab,
    "quadratic": algebra_quadratic.quadratic_lab,
}


def build(key, cfg):
    if key not in REGISTRY:
        raise KeyError("no lab named %r; known labs: %s" % (key, ", ".join(sorted(REGISTRY))))
    return REGISTRY[key](cfg or {})


__all__ = ["REGISTRY", "build", "Lab", "QUIZ_MARKUP", "QUIZ_SCRIPT", "cfg_literal"]
