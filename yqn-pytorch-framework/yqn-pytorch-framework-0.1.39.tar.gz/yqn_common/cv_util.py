import os

import cv2


def draw_block(image_binary_array, mutipage_texts_row_blocked, file_name, config):
    '''
    文档分块 将分块绘制到远图中，以判断分块效果
    :param image_binary_array: numpy.array 表示多个图片的binary信息 由 read_and_convert_file返回
    :param mutipage_texts_row_blocked: numpy.array 表示分块信息 由tests_to_blocks 返回
    :param file_name: str 文件名称
    :param config: BasicConfig 表config实例 传入为LocalConfig实例
   :return: Null
    '''
    assert len(image_binary_array) == len(mutipage_texts_row_blocked), "图片数要和页数相等"
    for i in range(len(image_binary_array)):
        image_binary = image_binary_array[i]
        texts_rows_blocked = mutipage_texts_row_blocked[i]
        img = cv2.imdecode(image_binary, cv2.IMREAD_COLOR)
        h, w, _ = img.shape
        for texts_rows in texts_rows_blocked:
            block_index = texts_rows["block_index"]
            text_contents = texts_rows["text_contexts"]
            if len(text_contents) <= 1:
                continue
            row_min = text_contents[0]
            row_max = text_contents[-1]
            row_min_left = row_min[0]
            row_max_right = row_max[-1]
            y_top_min = row_min_left.values()[1]
            y_bottom_max = row_max_right.values()[3]

            draw_x_min = 0
            draw_x_max = w
            draw_y_min = y_top_min
            draw_y_max = y_bottom_max
            cv2.rectangle(img, (draw_x_min, draw_y_min), (draw_x_max, draw_y_max), (255, 0, 0), 2)
            cv2.imwrite(os.path.join(config.convert_config.get_tmp_file_dir(),
                                     "draw_blocked_" + file_name + "_" + str(i) + ".jpg"), img)
