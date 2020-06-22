from validation.value_validation import ValidateValue

def bmr_results(client):
    results = BMRFormulas(client).add_bmr_results_to_dictionary()
    return results

def harris_benedict_bmr(client):
    results = BMRFormulas(client).add_bmr_results_to_dictionary()
    harris_benedict = results['harris_benedict_bmr']
    return harris_benedict

def mifflin_bmr(client):
    results = BMRFormulas(client).add_bmr_results_to_dictionary()
    mifflin = results['mifflin_st_jeor_bmr']
    return mifflin


class MetabolicClient(object):
    def __init__(self, sex, weight, height, age):
        self._sex = ValidateValue(sex).valueIsMaleFemale()
        self._weight = ValidateValue(weight).valueIsPositiveFloat()
        self._height = ValidateValue(height).valueIsPositiveFloat()
        self._age = ValidateValue(age).valueIsPositiveInteger()

class BMRFormulas(object):
    def __init__(self, client):
        self._client = client


    def add_bmr_results_to_dictionary(self):
        formulas = {
            'harris_benedict_bmr':self._harris_benedict_bmr(),
            'mifflin_st_jeor_bmr':self._mifflin_st_jeor_bmr()
        }
        results = {}
        for key, value in formulas.items():
            results[key] = value

        return results


    def _harris_benedict_bmr(self):
        if self._client._sex == 'male':
            bmr = (88.4 + 13.4 * self._client._weight) + (4.8 * self._client._height) - (5.68 * self._client._age)

        if self._client._sex == 'female':
            bmr = (447.6 + 9.25 * self._client._weight) + (3.10 * self._client._height) - (4.33 * self._client._age)

        return bmr


    def _mifflin_st_jeor_bmr(self):
        if self._client._sex == 'male':
            bmr = (9.99 * self._client._weight) + (6.25 * self._client._height) - (4.92 * self._client._age) + 5

        if self._client._sex == 'female':
            bmr = (9.99 * self._client._weight) + (6.25 * self._client._height) - (4.92 * self._client._age) - 161

        return bmr
