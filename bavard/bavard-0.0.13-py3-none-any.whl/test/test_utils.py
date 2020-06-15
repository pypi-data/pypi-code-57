import bavard.text.utils as utils


def test_get_char_to_word_idx():
    text = "The man went to the store to buy some milk."
    char_to_word_map = utils.get_char_to_word_map(text)

    assert char_to_word_map[0] == 0
    assert char_to_word_map[4] == 1
    assert char_to_word_map[8] == 2
    assert char_to_word_map[13] == 3
    assert char_to_word_map[-1] == 9
