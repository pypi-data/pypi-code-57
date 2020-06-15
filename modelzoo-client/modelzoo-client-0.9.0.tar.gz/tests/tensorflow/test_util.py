import pathlib

from modelzoo.tensorflow import util


def test_generate_docs_from_tf_metadata():
    fixtures_path = pathlib.Path(__file__).parent.parent.joinpath("fixtures")
    assert (
        util.generate_input_output_table_from_saved_model(
            str(fixtures_path.joinpath("saved_model_half_plus_three"))
        )
        == """| | Name | Shape | Type |
|-| ---- | -----:| ----:|
| input | `x` |  | `float32` |
| output | `y` |  | `float32` |"""
    )

    assert (
        util.generate_input_output_table_from_saved_model(
            str(fixtures_path.joinpath("mnist_tf_keras"))
        )
        == """| | Name | Shape | Type |
|-| ---- | -----:| ----:|
| input | `flatten_input` | `[-1, 28, 28]` | `float32` |
| output | `dense_1` | `[-1, 10]` | `float32` |"""
    )
