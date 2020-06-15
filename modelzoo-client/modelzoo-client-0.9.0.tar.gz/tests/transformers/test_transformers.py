import pathlib
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

import modelzoo
import modelzoo.transformers

from tests.mock_api_server import mock_api_server


def test_transformers_deploy() -> None:
    tiny_ctrl_path = pathlib.Path(__file__).parent.parent.joinpath("fixtures/tiny-ctrl")

    tokenizer, model = (
        AutoTokenizer.from_pretrained(str(tiny_ctrl_path)),
        AutoModelWithLMHead.from_pretrained(str(tiny_ctrl_path)),
    )
    p = pipeline("text-generation", model=model, tokenizer=tokenizer)

    with mock_api_server():
        assert (
            modelzoo.transformers.deploy(p, model_name="test", api_key="test") == "test"
        )

        modelzoo.list(api_key="test")
        modelzoo.info("test-model", api_key="test")
        modelzoo.stop("test-model", api_key="test")
        modelzoo.start("test-model", api_key="test")
        modelzoo.transformers.generate(
            "test-model", input_str="test", num_return_sequences=5, api_key="test"
        )
