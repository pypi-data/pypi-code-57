import math


from validation.value_validation import ValidateValue


def one_rep_max_estimation(reps, weight):
    results = OneRepMaxEquations(reps,weight).add_results_to_dictionary()
    return results


class OneRepMaxEquations(object):
    def __init__(self, reps, weight):
        self._reps = float(ValidateValue(reps).valueIsLessThan10())
        self._weight = ValidateValue(weight).valueIsPositiveFloat()

    def add_results_to_dictionary(self):
        formulas = {
            'brzycki_formula': self._brzycki_formula(),
            'epley_formula': self._epley_formula(),
            'mayhew_formula': self._mayhew_formula(),
            'lander_formula': self._lander_formula(),
            'lombardi_formula': self._lombardi_formula()
        }

        results = {}

        for key, value in formulas.items():
            results[key] = value

        return results

    def _brzycki_formula(self):
        brzycki_one_rep_max = self._weight/(1.0278-(0.0278*self._reps))
        return brzycki_one_rep_max

    def _epley_formula(self):
        # Reps need to be more than 1
        epley_one_rep_max = self._weight * (1 + (self._reps/30))
        return epley_one_rep_max

    def _mayhew_formula(self):
        mayhew_one_rep_max = (100 * self._weight)/(52.2 + (41.9 * math.exp(-0.055**self._reps)))
        return mayhew_one_rep_max

    def _lander_formula(self):
        lander_one_rep_max = self._weight/(1.013-(0.0267123*self._reps))
        return lander_one_rep_max

    def _lombardi_formula(self):
        lombardi_one_rep_max = self._weight*self._reps**0.10
        return lombardi_one_rep_max
