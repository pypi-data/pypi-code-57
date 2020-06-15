import base64


def encode_task_string(id_string):
    return base64.encodebytes(id_string.encode("utf-8")).decode("utf-8")


def decode_task_string(encoded_string):
    return base64.decodebytes(encoded_string.encode("utf-8")).decode("utf-8")


def test_task_encoding():
    id_str = "47,93,345,3445"
    assert id_str == decode_task_string(encode_task_string(id_str))


def task_string_to_context(task_string):
    [model_id, asset_model_id, operation_id, task_id] = decode_task_string(
        task_string
    ).split(",")
    return {
        "modelId": int(model_id),
        "assetModelId": int(asset_model_id),
        "operationId": int(operation_id),
        "taskId": int(task_id),
    }


def pretty_result(result):
    s = ""

    s += "Output\n----------\n"
    s += result["output"]
    s += "\nErrors\n----------\n"
    s += result["errors"] if result["errors"] else "None"
    s += "\n\n"

    return s
