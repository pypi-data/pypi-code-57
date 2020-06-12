import re
import datetime


def start_preprocess_bychar(s):
    s1 = ""
    for char in s:
        char_new = re.sub("：", ":", re.sub("＆", '&', re.sub('）', ')', re.sub('（', '(', str(char).upper()))))
        if len(char_new) == len(char):
            s1 += char_new
        elif len(char_new) > len(char):
            s1 += char_new[0]
        else:
            s1 += char
    return s1


def white_part_map(str_withspace_raw, text_preprocess):
    if len(str_withspace_raw)>0:
        str_no_space = text_preprocess(str_withspace_raw)
        maps = {0: 0}
        # print("str_withsapce_raw", str_withspace_raw)
        # print("str_no_space", str_no_space)
        if start_preprocess_bychar(str_withspace_raw[0]) == str_no_space[0]:
            start_same = True
            str_index = 1
        else:
            start_same = False
            str_index = 0
        to_end = False
        for i in range(1, len(str_withspace_raw)):
            # print(str_withspace_raw[i], str_no_space[str_index])
            if start_preprocess_bychar(str_withspace_raw[i]) == str_no_space[str_index] and not to_end:
                if start_same == False:
                    maps[i] = maps[i - 1]
                    start_same = True
                else:
                    maps[i] = maps[i - 1] + 1
                if str_index < len(str_no_space) - 1:
                    str_index += 1
                else:
                    to_end = True
            else:
                maps[i] = maps[i - 1]
            # if i < 20:
            #     print(str_withspace_raw[i], str_no_space[str_index], i, maps[i])
            # else:
            #     exit()
        # if len(str_withspace_raw) == len(str_no_space):
        #     print("-------same length----")
        if len(str_withspace_raw) < len(str_no_space):
            maps = {}
            for i in range(len(str_withspace_raw)):
                maps[i]=i
        else:
            assert maps[len(str_withspace_raw) - 1] == len(str_no_space) - 1
        return maps
    else:
        return {}


def space_reduction_common(str_withspace_raw, str_part, start_withoutspace, end_withoutspace, text_preprocess):
    start = datetime.datetime.now()
    maps = white_part_map(str_withspace_raw, text_preprocess)
    with_id = list(maps.keys())
    without_id = list(maps.values())
    if end_withoutspace == max(without_id) + 1:
        start_without_id = without_id.index(start_withoutspace)
        end_without_id = len(str_withspace_raw) - 1
    else:
        start_without_id = without_id.index(start_withoutspace)
        end_without_id = without_id.index(end_withoutspace - 1) + 1
    start_with_id = with_id[start_without_id]
    end_with_id = with_id[end_without_id]
    if end_with_id == len(str_withspace_raw) - 1:
        end_with_id = len(str_withspace_raw)
    new_word = str_withspace_raw[start_with_id:end_with_id]
    return new_word, start_with_id, end_with_id


def space_reduction_common_cc(str_withspace_raw, maps, start_withoutspace, end_withoutspace, text_preprocess):
    with_id = list(maps.keys())
    without_id = list(maps.values())
    if end_withoutspace == max(without_id) + 1:
        start_without_id = without_id.index(start_withoutspace)
        end_without_id = len(str_withspace_raw) - 1
    else:
        start_without_id = without_id.index(start_withoutspace)
        end_without_id = without_id.index(end_withoutspace - 1) + 1
    start_with_id = with_id[start_without_id]
    end_with_id = with_id[end_without_id]
    if end_with_id == len(str_withspace_raw) - 1:
        end_with_id = len(str_withspace_raw)
    new_word = str_withspace_raw[start_with_id:end_with_id]
    return new_word, start_with_id, end_with_id


def list_space_reduction(str_withspace, entities_list, text_preprocess):
    if len(entities_list) == 0:
        return []
    else:
        maps = white_part_map(str_withspace, text_preprocess)
        for i in range(len(entities_list)):
            entity = entities_list[i]
            str_part = entity["word"]
            start_withoutspace = entity['start']
            end_withoutspace = entity["end"]
            entity['word'], entity['start'], entity['end'] = space_reduction_common_cc(str_withspace, maps,
                                                                                       start_withoutspace,
                                                                                       end_withoutspace,
                                                                                       text_preprocess)
            entities_list[i] = entity
        return entities_list
