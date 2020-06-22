from tokenizer_tools.tagset.offset.plottable_counter import PlottableCounter


def test_plottable_counter():
    data = "abbcccdddd"

    pc = PlottableCounter(data)
    fig = pc.get_figure()

    result = fig.to_json()

    assert len(result)
