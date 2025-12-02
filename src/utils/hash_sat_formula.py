from entities.sat_formula import SatFormula


def hash_sat_formula(sat_formula: SatFormula) -> int:
    return hash(frozenset(sat_formula))
