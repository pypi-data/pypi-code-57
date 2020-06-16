import random as r

def mock(no_of_char=10, lower_inc=True, uppper_inc=True, special_inc=False, number_inc=False):
    if no_of_char is None:
        no_of_char = 10
    
    string_value = ""
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = "1234567890"
    special = "!\"#$%&""()*+,-./:;<=>?@[\]^_`{|}~"

    if lower_inc:
        string_value += lower
    if uppper_inc:
        string_value += upper
    if number_inc:
        string_value += number
    if special_inc:
        string_value += special

    result = ""
    for i in range(no_of_char):
        result += r.choice(string_value)
        
    return result