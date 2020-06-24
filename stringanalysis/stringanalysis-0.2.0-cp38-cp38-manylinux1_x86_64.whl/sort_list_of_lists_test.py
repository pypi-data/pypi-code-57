from stringanalysis.sort_list_of_lists import sort_list_of_lists

def test_sort_list_of_lists():
    results = sort_list_of_lists([
        [("a", 2), ("b", 3)]
    ])
    assert results == [["b", "a"]]


def test_sort_list_of_lists_keep_scores():
    results = sort_list_of_lists([
        [("a", 2), ("b", 3)]
    ], keep_scores=True)
    assert results == [[("b", 3), ("a", 2)]]

