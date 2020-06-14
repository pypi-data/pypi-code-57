import configparser


class ConfigUtils(object):
    """
    配置文件工具类: 配置文件分为3级, section -> option -> item

    """

    def __init__(self, config_file_path):
        """
        根据传入配置文件的路径, 创建配置文件对象

        :param config_file_path: 配置文件的路径
        """

        self.config = configparser.ConfigParser()
        self.config.read(config_file_path, encoding="utf-8")

    def get_sections(self):
        """
        以列表形式, 返回配置文件中的所有section名

        :return:
        """
        return self.config.sections()

    def get_options_by_section(self, section_name):
        """
        以列表形式, 根据传入的section名, 获取该section下的所有options

        :param section_name:
        :return:
        """
        return self.config.options(section_name)

    def get_items_by_section(self, section_name):
        """
        以列表形式, 根据传入的section名, 获取该section下的所有options

        :param section_name:
        :return:
        """
        return self.config.items(section_name)

    def get_value_by_section_and_option(self, section_name, option_name):
        """
        以字符串形式, 根据section名和option名, 获取值

        :param section_name:
        :param option_name:
        :return:
        """
        return self.config.get(section_name, option_name)

    def get_values_in_dict(self):
        """
        以字典形式, 返回所有options的值

        :return:
        """
        self.config_dict = {}
        for section in self.get_sections():
            for option in self.get_options_by_section(section):
                value = self.get_value_by_section_and_option(section, option)
                self.config_dict[option] = value
        return self.config_dict


if __name__ == '__main__':
    pass

    # 测试获取
    # config = ConfigUtils('./launcher_time.ini')
    # print(config.get_values_in_dict())
