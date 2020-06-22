from validation.value_validation import ValidateValue


def percentage_value(percentage, max_value):
    value = (percentage * 0.01) * max_value
    return value
