from string import ascii_lowercase, punctuation


def get_character_map():
    # allowed characters: alphabets, numbers, symbols
    allowed_string_characters = [letter for letter in ascii_lowercase]

    allowed_punctuation = [mark for mark in punctuation]
    # remove quotes to make things easier
    for mark in ("'", '"', "`"):
        allowed_punctuation.remove(mark)

    allowed_integers = [str(number) for number in range(10)]

    # create an evenly distributed list so that we don't necessarily get a
    # result that is all numbers or symbols
    all_allowed_characters = dict()
    character_index = 1
    while (
        (len(allowed_string_characters) > 0)
        or (len(allowed_punctuation) > 0)
        or (len(allowed_integers) > 0)
    ):
        for allowed_list in (
            allowed_string_characters,
            allowed_punctuation,
            allowed_integers,
        ):
            if len(allowed_list) > 0:
                all_allowed_characters[allowed_list[0]] = character_index
                allowed_list.pop(0)
                character_index += 1

    return all_allowed_characters


def flip_dict(regular_dict):
    return {value: key for key, value in regular_dict.items()}
