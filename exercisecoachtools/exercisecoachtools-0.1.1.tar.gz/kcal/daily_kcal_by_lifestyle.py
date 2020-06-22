from .metabolic_rate_prediction import bmr_results


def get_calories_by_activity(activity_level, bmr):
    ACTIVITY_FACTORS = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extremely active': 1.9
    }

    if activity_level in ACTIVITY_FACTORS:
        results = ACTIVITY_FACTORS[activity_level] * bmr
        return results
