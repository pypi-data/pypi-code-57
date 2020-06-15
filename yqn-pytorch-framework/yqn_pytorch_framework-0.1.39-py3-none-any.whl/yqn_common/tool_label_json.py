'''
生成NER标注前的文件
输入： 文件（解析成图片和文本块之后）， 需要标注的标签类型， classes , annotations
输出： 符合工具模式的json文件（且已经预标注）
'''
import json
import os


def in_which_block(e, block_len):
    word_end = e["end"]
    block_length = list(block_len.values())
    block_id = -1
    for i in range(len(block_length) - 1):
        if word_end >= block_length[i] and word_end < block_length[i + 1]:
            block_id = i + 1
            break
    if block_id > 0:
        e["start"] = e["start"] - block_length[block_id - 1]
        e["end"] = e["end"] - block_length[block_id - 1]
    return e, block_id


def gen_json(filename, contents, keys_nlp, classes, annotations, save_path):
    json_info = {"file_id": filename,
                 "classes": classes,
                 "annotations": annotations,
                 "labels": []}
    # pre_entities 的每个元素是每一块的预标注内容
    # 先把内容做成一整个文档，为什么不分块？因为现在NER没有分块
    predict_class = ""
    real_class = ""
    state = True
    block_text = {}
    min_x = contents[0]["text_rectangle"]["llx"]
    min_y = contents[0]["text_rectangle"]["lly"]
    max_x = contents[-1]["text_rectangle"]["urx"]
    max_y = contents[-1]["text_rectangle"]["ury"]
    # 有block的范围吗？
    for i in range(len(contents)):
        block_id = contents[i]["block_index"]
        ttext = contents[i]["text"]
        if block_id not in block_text:
            block_text[block_id] = ttext.split("#")[0]
        else:
            block_text[block_id] += ttext.split("#")[0]
    block_len = {}
    for k, v in block_text.items():
        if k == 0:
            block_len[k] = len(v)
        else:
            block_len[k] = len(v) + block_len[k - 1]
    print("block_len", block_len)
    block_anno = {}
    for k, v in block_text.items():
        block_anno[k] = []

    position = {"left": min_x,
                "top": min_y,
                "right": max_x,
                "bottom": max_y}
    # anno = []
    for e in keys_nlp:
        e, block_id = in_which_block(e, block_len)
        block_anno[block_id].append({"start": e["start"],
                                     "end": e["end"],
                                     "annotation": e["type"].split("#")[0]})
    for k, v in block_text.items():
        json_info["labels"].append({"index": k,
                                    "text": v,
                                    "predict_class": predict_class,
                                    "real_class": real_class,
                                    "state": state,
                                    "position": position,
                                    "annotations": block_anno[k]})
    # json_info["labels"].append({"index": index,
    #                             "text": text,
    #                             "predict_class": predict_class,
    #                             "real_class": real_class,
    #                             "state": state,
    #                             "position": position,
    #                             "annotations": anno})
    json_info_string = json.dumps(json_info, ensure_ascii=False)
    f = open(os.path.join(save_path, str(filename) + ".json"), "w", encoding="utf-8")
    f.write(json_info_string)
    f.close()

    return
