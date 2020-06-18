from __future__ import division

def int_label_to_letter_label(number):
    result = []

    while True:
        number -= 1
        result.append(number%26)
        if number//26-1 < 0:
            break
        number //= 26

    return ''.join([chr(ord('A') + x) for x in reversed(result)])

def letter_label_to_int_label(letters):
    letters_ord = [ord(letter) - ord('A') + 1 for letter in list(letters)]
    result_list = [l * 26**i for i, l in enumerate(reversed(letters_ord))]

    result = 0
    for r in result_list:
    	result += r

    return result