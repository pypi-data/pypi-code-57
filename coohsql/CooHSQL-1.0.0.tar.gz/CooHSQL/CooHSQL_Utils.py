import datetime
import decimal


def is_number(num):
    try:
        if num is None:
            return False
        float(num)
        return True
    except (ValueError, TypeError):
        return False


def merge_cond(tem_cond):
    """
        合并 UPDATE 语句中的 SET 部分
        :param tem_cond:
        :return:
        """
    option_list = list()
    for k, v in tem_cond.items():
        tem_equ = "`" + str(k) + "`" + "=" + (
            str(v) if is_number(v) else "'" + str(v) + "'")
        option_list.append(tem_equ)
    return ','.join(option_list)


def seg_dict(event_dict):
    """
    :param event_dict:
    :return:
    """
    keys, values = list(), list()
    for k, v in event_dict.items():
        keys.append(k)
        if str(v).isdigit() and v:
            values.append(str(v))
        else:
            values.append("'" + str(v) + "'")

    return ','.join(keys), ','.join(values)


def clear_event_type(event):
    """
    加载进来的 binlog 时间类型也被转换为 datetime
    此方法是将 datetime 类型转换为 str 方便后续操作
    :param event:
    :return:
    """
    for k, v in event.items():
        if isinstance(v, datetime.datetime):
            event[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(v, decimal.Decimal):
            event[k] = str(v)
    return event


def reverse_delete(event):
    """
    逆向 delete 语句 insert
    :param event:
    :return:
    """
    tem_key, tem_value = seg_dict(event['data'])
    template = "INSERT INTO `{0}`.`{1}`({2}) VALUE ({3});".format(event['schema'], event['table'],
                                                                  tem_key, tem_value)
    return template


def filter_where(event_df, max_filtration_len):
    """
    筛选组合 where 条件
    如果 where 字段条件太多或者复杂的话
    会影响执行效率
    :return:
    """
    option_list = list()
    for k, v in event_df.items():
        if len(str(v)) <= max_filtration_len and v:
            tem_equ = "`" + str(k) + "`" + "=" + (
                str(v) if is_number(v) else "'" + str(v) + "'")
            option_list.append(tem_equ)
    return ' and '.join(option_list)


def check_parm(tem_mode):
    """
    校验参数 mode
    :return:
    """
    mode_parm = ['flashback', 'dump']
    if tem_mode not in mode_parm:
        print(tem_mode)
        raise KeyError('Invalid parameter: must be "flashback" or "dump" default to flashback')


def dump_update(event, filtration_len):
    template = "UPDATE `{0}`.`{1}` SET {2} WHERE {3};".format(event["schema"], event['table'],
                                                              merge_cond(event['after_data']),
                                                              filter_where(event['before_data'],
                                                                           filtration_len))
    return template


def reverse_insert(event, filtration_len):
    """
    逆向 insert 语句 DELETE
    :return:
    """
    template = "DELETE FROM `{0}`.`{1}` WHERE {2};".format(event["schema"], event['table'],
                                                           filter_where(event['data'], filtration_len))
    return template


def reverse_update(event, filtration_len):
    """
    逆向 update 语句 update
    :return:
    """
    template = "UPDATE `{0}`.`{1}` SET {2} WHERE {3};".format(event["schema"], event['table'],
                                                              merge_cond(event['before_data']),
                                                              filter_where(event['after_data'],
                                                                           filtration_len))
    return template


def check_datetime(time_pram):
    if time_pram:
        try:
            time_pram = datetime.datetime.strptime(time_pram, "%Y-%m-%d %H:%M:%S")
            return time_pram
        except ValueError:
            raise ValueError("Please pass in the correct time format, for example: 2020-1-10 00:00:00")
    else:
        return None


def opinion_time(time_pram1, time_pram2):
    d1 = datetime.datetime.strptime(str(time_pram1), '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(str(time_pram2), '%Y-%m-%d %H:%M:%S')
    if d1 >= d2:
        return True
    else:
        return False
