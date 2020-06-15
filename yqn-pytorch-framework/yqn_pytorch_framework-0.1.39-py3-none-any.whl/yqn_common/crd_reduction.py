# !/home/wcg/tools/local/anaconda3/bin/python
# coding=utf8
import re


def crd_reduction_common(str_with_special, entry_list, special_character, text_process):
    txt_with_special_string = str_with_special
    special_characters = special_character.split("|")

    txt_with_special_string_list = []
    for i in range(len(txt_with_special_string)):
        if txt_with_special_string[i] in special_characters:
            txt_with_special_string_list.append('0')
        else:
            txt_with_special_string_list.append('1')

    for i in range(len(entry_list)):
        start = int(entry_list[i]['start'])
        word = entry_list[i]["word"]
        # word = entry_list[i]["value"]
        start_new = get_whithout_special_crd(txt_with_special_string_list, start)
        if text_process:
            word_new = text_process(word)
        else:
            word_new = re.sub(special_character, "", word)
        end_new = start_new + len(word_new)
        entry_list[i]['start'] = start_new
        entry_list[i]['end'] = end_new
        entry_list[i]["word"] = word_new
        # entry_list[i]["value"] = word_new
    return entry_list


def get_whithout_special_crd(txt_withspecialstring_list, num):
    crd_reduc = 0
    for i in range(num):
        crd_reduc = crd_reduc + int(txt_withspecialstring_list[i])
    return crd_reduc
