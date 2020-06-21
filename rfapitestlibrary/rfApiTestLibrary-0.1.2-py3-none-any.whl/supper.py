'''
Documentation: 为了方便测试，提供的一些超级方法
'''

import json
import rfApiTestLibrary.requestLib as requestLib
from robot.libraries.Collections import _Dictionary
import rfApiTestLibrary.jsonLib as jsonLib
import rfApiTestLibrary.log as log
from rfApiTestLibrary import regularExpressionLib as rel
import pymysql


METHOD_SUPPORT=['GET','POST','PUT','DELETE','PATCH']

def at_one_http_interface_test(method, uri, params=None, data=None,req_json=None,req_headers=None,
                                timeout=None,allow_redirects=None,
                                expect_status_code=None,expect_resp_headers_contains=None,
                                expect_resp_json=None, expect_resp_body=None,
                                expect_resp_json_contains=None,expect_resp_body_contains=None,
                                expect_resp_json_regular_expression_contains=None,
                                expect_resp_body_regular_expression_contains=None,
                                expect_resp_json_special_contains=None):
    '''
    单一接口测试，超级方法。暂时不支持上传文件的multipart/form-data和x-www-form-urlencoded。如果需要支持，后续添加。
    :param method: string类型。方法名，必填字段，不区分大小写。支持get, post, put, delete
    :param uri: string类型。uri地址。必填字段。
    :param params: 字典类型，或者可以转成字典的String类型。请求中的parameter
    :param data: String类型。request请求body.
    :param req_json: 字典类型或者可以转成字典的String类型。request请求json body.
    :param req_headers: 字典类型或者可以转成字典的String类型。request请求 headers。
    :param timeout: int类型，单位秒
    :param allow_redirects: 布尔型。如果是None,requests里默认是True,就是到重定向后的response
    :param expect_status_code: int类型。期待的response status code。检查点。
    :param expect_resp_headers_contains: 字典类型或者可以转成字典的String类型。验证response header包含期待的字典.检查点。
    :param expect_resp_json:  json类型或者可以转成json的String类型。验证response json body和期待的相同。检查点。
    :param expect_resp_body:  String类型。验证response body和期待的相同。 检查点。
    :param expect_resp_json_contains: json类型或者可以转成json的String类型。验证response json body包含key,而且里面的value是包含关系。检查点。
    :param expect_resp_body_contains: string类型。验证response body包含string.检查点。
    :param expect_resp_json_regular_expression_contains: 字典类型,验证response json body的jsonpath下某个值正则匹配，key是jsonpath,value是正则匹配的规则。比如{"$.aa.0.bb":"\d+"}
    :param expect_resp_body_regular_expression_contains: string类型, 验证response body正则匹配包含。
    :param expect_resp_json_special_contains: json类型或者可以转成json的String类型。验证response json body包含,针对list包含是无序的，不过不支持多层嵌套。检查点。
    :return: 字典类型,返回response
    '''
    #第一步检查参数：
    _verify_object_is_string(method,'method')
    if method.upper() not in METHOD_SUPPORT:
        raise AssertionError('请求方法['+method+']不支持，请求方法目前支持'+str(METHOD_SUPPORT))
    method=method.upper()
    _verify_object_is_string(uri, 'URI')
    params=_verify_object_is_json_or_json_str(params,'params')
    _verify_object_is_string(data, 'data')
    req_json=_verify_object_is_json_or_json_str(req_json,'req_json')
    req_headers=_verify_object_is_json_or_json_str(req_headers,'req_headers')
    _verify_object_is_int(timeout,'timeout')
    _verify_object_is_bool(allow_redirects,'allow_redirects')
    _verify_object_is_int(expect_status_code,'expect_status_code')
    expect_resp_headers_contains = _verify_object_is_json_or_json_str(expect_resp_headers_contains,'expect_resp_headers_contains')
    expect_resp_json=_verify_object_is_json_or_json_str(expect_resp_json,'expect_resp_json')
    _verify_object_is_string(expect_resp_body,'expect_resp_body')
    expect_resp_json_contains=_verify_object_is_json_or_json_str(expect_resp_json_contains,'expect_resp_json_contains')
    _verify_object_is_string(expect_resp_body_contains,'expect_resp_body_contains')
    expect_resp_json_regular_expression_contains=_verify_object_is_dict_or_dict_str(expect_resp_json_regular_expression_contains)
    expect_resp_json_special_contains=_verify_object_is_json_or_json_str(expect_resp_json_special_contains,'expect_resp_json_special_contains')
    resp=requestLib.at_http_request(method, uri, params=params, data=data,json=req_json,headers=req_headers,
                    timeout=timeout,allow_redirects=allow_redirects)
    status_code=requestLib.at_get_http_response_status_code(resp)
    resp_headers=requestLib.at_get_http_response_header(resp)
    if expect_resp_json is not None or expect_resp_json_contains is not None:
        resp_json_body=requestLib.at_get_http_response_json_body(resp)
    resp_body=requestLib.at_get_http_response_body(resp)
    if expect_status_code is not None and expect_status_code!=status_code:
        raise AssertionError('response返回码不是'+str(expect_status_code)+',而是'+str(status_code))
    if expect_resp_headers_contains is not None:
        robotDict=_Dictionary()
        robotDict.dictionary_should_contain_sub_dictionary(resp_headers,expect_resp_headers_contains,  "response headers不包含"+str(expect_resp_headers_contains), values=True)
    if expect_resp_json is not None:
        if resp_json_body != expect_resp_json:
            raise AssertionError('response json body完全匹配失败:期待的response body是%s;但是实际上是%s'% (str(expect_resp_json),str(resp_json_body)))
    if expect_resp_body is not None:
        if resp_body != expect_resp_body:
            raise AssertionError('response body不一致:期待的response body是%s;但是实际上是%s'% (expect_resp_body,resp_body))
    if expect_resp_json_contains is not None:
        log.info("开始比较response json body是否包含",also_console=True,html=True)
        jsonLib.json_contain_sub_json(expect_resp_json_contains,resp_json_body)
        log.info("比较response json body是否包含完成,结果正确", also_console=True, html=True)
    if expect_resp_body_contains is not None:
        if expect_resp_body_contains not in resp_body:
            raise AssertionError('response body不包含期待的response body是%s' % (expect_resp_body))
    if expect_resp_json_regular_expression_contains is not None:
        resp_json_body = requestLib.at_get_http_response_json_body(resp)
        for expect_resp_json_regular_expression_contains_key, expect_resp_json_regular_expression_contains_value in expect_resp_json_regular_expression_contains.items():
            print(expect_resp_json_regular_expression_contains_key)
            print(expect_resp_json_regular_expression_contains_value)
            rel.json_path_regular_match(resp_json_body,expect_resp_json_regular_expression_contains_key,expect_resp_json_regular_expression_contains_value)
    if expect_resp_body_regular_expression_contains is not None:
        rel.str_regular_match(resp_body,expect_resp_body_regular_expression_contains)
    if expect_resp_json_special_contains is not None:
        resp_json_body=requestLib.at_get_http_response_json_body(resp)
        jsonLib.json_contains_not_orderd_sub_json(expect_resp_json_special_contains,resp_json_body)
    return resp

def _verify_object_is_int(obj,param_name):
    if obj is not None and not isinstance(obj,int):
        raise AssertionError('参数['+param_name+']必须是int类型')

def _verify_object_is_bool(obj,param_name):
    if obj is not None and not isinstance(obj,bool):
        raise AssertionError('参数['+param_name+']必须是bool类型')

def _verify_object_is_string(obj,param_name):
    '''
    验证object是string类型，不是抛出异常
    :param obj: 对象
    :param param_name: string类型，用于报错信息
    :return:
    '''
    if obj is not None and not isinstance(obj,str):
        raise AssertionError('参数['+param_name+']必须是string类型')

def _verify_object_is_dict_or_dict_str(obj):
    if obj is not None:
        if isinstance(obj,dict):
            return obj
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)
                if isinstance(obj,list):
                    raise AssertionError(obj + "不是能转成字典的string")
                return obj
            except Exception as e:
                raise AssertionError(obj+" : 不是能转成字典的string")
        else:
            raise AssertionError(str(obj)+" : 不是能转成字典的string")

    return obj

def _verify_object_is_json_or_json_str(obj,param_name):
    '''
    验证是否是json类型的字典或者string
    :param obj:对象
    :param param_name: string类型，用于报错信息
    '''
    if obj is not None:
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)
            except Exception as e:
                raise AssertionError( param_name+'参数[' + obj + ']必须是json类型或者能转成json的string.' + str(e))
        elif not isinstance(obj, dict):
            raise AssertionError('['+param_name+']参数必须是字典类型或者能转成字典的string')
    return obj

def at_run_sql(sql, config, expect_count=None, expect_result=None, expect_contains=None, should_be_none=None):
    '''
    运行sql。操作查询都可以支持。
    :param sql: string类型。注意不要用超过2个以上包括2个空格。
    :param config: 字典类型,含有host,port,user,password,db等信息的配置。
    :return: 如果是操作数据库，返回int类型,就是影响的行数。如果是查询数据库，如果没有数据返回，返回None。如果有数据返回，返回list类型。
    '''
    if isinstance(config,str):
        config=json.loads(config,encoding='utf-8')
    if isinstance(config['port'],str):
        config.update({'port':int(config['port'])})
    conn=None
    cursor=None
    count_flag = False
    result_flag = False
    count = -1
    result_list = []
    if expect_count is not None and not isinstance(expect_count,int):
        raise AssertionError('expect_count必须是int类型')
    if isinstance(expect_result,str):
        expect_result=json.loads(expect_result,encoding='utf-8')
    if expect_result is not None and not isinstance(expect_result,list):
        raise AssertionError('expect_result必须是list类型')
    if isinstance(expect_contains,str):
        expect_contains=json.loads(expect_contains,encoding='utf-8')
    if expect_contains is not None and not (isinstance(expect_contains,list) or isinstance(expect_contains,dict)):
        raise AssertionError('expect_contains必须是list类型或者dict类型')
    if should_be_none is not None and not isinstance(should_be_none,bool):
        raise AssertionError('should_be_none必须是bool类型')
    log.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
    try:
        if config.get("charset") is None:
            config['charset'] = 'utf8'
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        count = cursor.execute(sql)
        # 取出所有行
        result = cursor.fetchall()
        if cursor.description is not None:
            fields_list = []
            for field in cursor.description:
                # field[0]是field名字，如果使用别名，就是别名
                fields_list.append(field[0])
            conn.commit()
            result_flag = True
            if result is None or len(result) == 0:
                log.info("数据库返回结果: None", html=True, also_console=True)
                result_list=None
            if result_list is not None:
                for i in range(len(result)):
                    row_dict = {}
                    row = result[i]
                    for j in range(len(row)):
                        row_dict[fields_list[j]] = row[j]
                    result_list.append(row_dict)
                log.info("数据库返回结果: " + str(result_list), html=True, also_console=True)
        else:
            log.info("被影响的行数: " + str(count),also_console=True, html=True)
            count_flag=True
            conn.commit()
    except pymysql.OperationalError as e:
        raise AssertionError(str(e))
    except pymysql.MySQLError as e:
        raise AssertionError('连接数据库失败，原因：%s' % str(e))
    finally:
        try:
            if cursor is not None:
                cursor.close()
        except pymysql.MySQLError as e:
            raise AssertionError(str(e))
        except pymysql.OperationalError as e:
            raise AssertionError(str(e))
        try:
            if conn is not None:
                conn.close()
        except pymysql.MySQLError as e:
            raise AssertionError(str(e))
        except pymysql.OperationalError as e:
            raise AssertionError(str(e))
    if result_flag:
        if result_list is None:
            if expect_result is not None:
                raise AssertionError("数据库返回结果是None,而不是expect_result:"+str(expect_result))
            if expect_contains is not None:
                raise AssertionError("数据库返回结果是None,而不是expect_contains:" + str(expect_contains))
            if should_be_none is not None and not should_be_none:
                raise AssertionError('数据库返回结果是None,而不是should_be_none:'+str(should_be_none))
        else:
            if should_be_none is not None and should_be_none:
                raise AssertionError('数据库返回结果不是None')
            if expect_result is not None:
                if expect_result !=result_list:
                    raise AssertionError("数据库返回结果不是expect_result: "+expect_result)
            if expect_contains is not None:
                if not list_contain_collection(result_list,expect_contains):
                    raise AssertionError('数据库返回结果不包含expect_contains: '+expect_contains)

        return result_list

    if count_flag:
        if expect_result is not None or expect_contains is not None or should_be_none is not None:
            log.warn('这是操作数据库的sql，请不要设置expect_result或者expect_contains或者should_be_none',html=True)
        if expect_count is not None:
            if count !=expect_count:
                raise AssertionError('期待的影响行数不同,真实影响的行数是'+str(count)+',而不是期待的'+str(expect_count))
        return count
    return None



def list_contain_collection(lst,collection):
    '''
    验证数据库使用。验证list是否包含字典或者列表。不是通用方法。
    :param lst: list类型。数据库的返回结果。
    :param collection: 验证时候被包含的列表或者字典
    :return:
    '''
    flag=False
    dic = _Dictionary()
    if isinstance(collection,dict):
        for item in lst:
            try:
                dic.dictionary_should_contain_sub_dictionary(item,collection)
                return True
            except AssertionError:
                continue
    if isinstance(collection,list):
        for item in collection:
            for lst_item in lst:
                try:
                    dic.dictionary_should_contain_sub_dictionary(lst_item, item)
                    flag = True
                    break
                except AssertionError:
                    continue
            if not flag:
                return False
            flag=False
        return True
    return False

def at_execute_many_sql(sql_list,config):
    '''
    操作多个sql
    :param sql_list:
    :param config:
    :return:
    '''
    conn = None
    cursor = None
    if isinstance(config,str):
        try:
            config=json.loads(config,encoding='utf-8')
        except:
            raise AssertionError("数据库的设置配置有问题，不是字典类型")
    if isinstance(config['port'],str):
        config.update({'port':int(config['port'])})
    if isinstance(sql_list,str):
        try:
            sql_list=json.loads(sql_list)
            if not isinstance(sql_list,list):
                raise AssertionError("sql_list不是list类型或者能转成list类型的string")
        except:
            raise AssertionError("sql_list不是list类型或者能转成list类型的string")
    try:
        if config.get("charset") is None:
            config['charset'] = 'utf8'
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        for sql in sql_list:
            log.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
            count = cursor.execute(sql)
            log.info("被影响的行数: " + str(count), html=True, also_console=True)
        conn.commit()  # 提交事务
    except pymysql.OperationalError as e:
        raise AssertionError(str(e))
    except pymysql.MySQLError as e:
        raise AssertionError('连接数据库失败，原因：%s' % str(e))
    finally:
        try:
            if cursor is not None:
                cursor.close()
        except pymysql.MySQLError as e:
            raise AssertionError(str(e))
        except pymysql.OperationalError as e:
            raise AssertionError(str(e))
        try:
            if conn is not None:
                conn.close()
        except pymysql.MySQLError as e:
            raise AssertionError(str(e))
        except pymysql.OperationalError as e:
            raise AssertionError(str(e))