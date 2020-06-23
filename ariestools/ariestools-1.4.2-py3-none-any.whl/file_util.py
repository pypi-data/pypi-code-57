import os


def write_file(file_path, content, mode='w', encoding='utf-8'):
    """
    写文件. 如果目录存在会自动新建. 默认以覆盖的方式写入.
    :param file_path:
    :param content:
    :param mode:
    :param encoding:
    :return:
    """
    abspath = os.path.abspath(file_path)
    abs_dir = os.path.dirname(abspath)

    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)

    with open(abspath, mode=mode, encoding=encoding) as fp:
        fp.write(content)


if __name__ == '__main__':
    write_file('./testData/write', '1测试1')
