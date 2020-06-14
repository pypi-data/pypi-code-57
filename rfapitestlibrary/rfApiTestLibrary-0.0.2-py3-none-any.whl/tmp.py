import json_tools
import re

son_dict={
	"code": 1,
	"message": "",
	"result": [{
			"companyName": "湖北襄阳二汽有限公司分公司4",
			"taxNum": "111101027906600004",
			"companyCode": "ASWDI98279",
			"lockFlag": "0",
			"companyNameAbbr": "",
			"contactorName": "马老师",
			"contactorEmail": "13487183439@163.com",
			"contactorTel": "7311011"
		},
		{
			"companyName": "沃尔玛（江西）百货有限公司",
			"taxNum": "91360000680930876T",
			"companyCode": "ASXXN73343",
			"lockFlag": "0",
			"companyNameAbbr": "",
			"contactorName": "陈攀",
			"contactorEmail": "",
			"contactorTel": "15051667460"
		}
	]
}

father_dict={
	"code": 1,
	"message": "",
	"result": [{
		"companyName": "安博供应链管理（上海）有限公司",
		"taxNum": "91310000088514638D",
		"companyCode": "AHKNR22555",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "",
		"contactorEmail": "",
		"contactorTel": ""
	}, {
		"companyName": "票易通销售连锁有限公司",
		"taxNum": "91440167439892787C",
		"companyCode": "ASDSP62427",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "庞梦姣",
		"contactorEmail": "pangmengjiao@xforceplus.com",
		"contactorTel": "13062697875"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司12",
		"taxNum": "111101027906600012",
		"companyCode": "ASSWS97558",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487283119@163.com",
		"contactorTel": "7129014"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司10",
		"taxNum": "111101027906600010",
		"companyCode": "AQGHN34937",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183499@163.com",
		"contactorTel": "7311011"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司8",
		"taxNum": "111101027906600008",
		"companyCode": "ARVXP27256",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183476@163.com",
		"contactorTel": "7194014"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司7",
		"taxNum": "111101027906600007",
		"companyCode": "AGDJI85672",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183469@163.com",
		"contactorTel": "7311011"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司6",
		"taxNum": "111101027906600006",
		"companyCode": "ATQBX35532",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487283459@163.com",
		"contactorTel": "7129014"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司5",
		"taxNum": "111101027906600005",
		"companyCode": "AQXCK29527",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183446@163.com",
		"contactorTel": "7194014"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司4",
		"taxNum": "111101027906600004",
		"companyCode": "ASWDI98279",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183439@163.com",
		"contactorTel": "7311011"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司3",
		"taxNum": "111101027906600003",
		"companyCode": "ASMEI89834",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487283429@163.com",
		"contactorTel": "7129014"
	}, {
		"companyName": "湖北襄阳二汽有限公司分公司1",
		"taxNum": "111101027906600001",
		"companyCode": "ASTXG82862",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "马老师",
		"contactorEmail": "13487183419@163.com",
		"contactorTel": "7311011"
	}, {
		"companyName": "黑龙江禾淘电子商务有限公司",
		"taxNum": "91230104571933242K",
		"companyCode": "AELNG77966",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "你",
		"contactorEmail": "111@qq.com",
		"contactorTel": "12312313"
	}, {
		"companyName": "上海易果电子商务有限公司",
		"taxNum": "91310105798972772X",
		"companyCode": "AJXCN89392",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "刘备",
		"contactorEmail": "222@qq.com",
		"contactorTel": "21313"
	}, {
		"companyName": "海南鼎圣置业有限公司",
		"taxNum": "914600005949392760",
		"companyCode": "ASUWW79484",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "",
		"contactorEmail": "",
		"contactorTel": ""
	}, {
		"companyName": "沃尔玛（江西）百货有限公司",
		"taxNum": "91360000680930876T",
		"companyCode": "ASXXN73343",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "陈攀",
		"contactorEmail": "",
		"contactorTel": "15051667460"
	}, {
		"companyName": "嘉兴云砺信息科技有限公司",
		"taxNum": "91330483MA2B9TGC9G",
		"companyCode": "AHWVS28327",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "刘美德",
		"contactorEmail": "liumeide@xforceplus.com",
		"contactorTel": "18602184098"
	}, {
		"companyName": "上海云砺信息科技有限公司",
		"taxNum": "91310113342290888U",
		"companyCode": "310113342290888",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "",
		"contactorEmail": "",
		"contactorTel": ""
	}, {
		"companyName": "税收分类购方公司",
		"taxNum": "1234567890ABCDE",
		"companyCode": "AQGDK47684",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "袁学恒",
		"contactorEmail": "1156787924@qq.com",
		"contactorTel": "18075093230"
	}, {
		"companyName": "玩具反斗城（中国）商贸有限公司唐山路南分公司",
		"taxNum": "91130200398890882D",
		"companyCode": "AWEXA73844",
		"lockFlag": "0",
		"companyNameAbbr": "",
		"contactorName": "",
		"contactorEmail": "",
		"contactorTel": ""
	}]
}

def diff(son,father):
    result = json_tools.diff(son, father)
    lst = []
    if not isinstance(result,list):
        raise AssertionError("json_tools的返回结果不是list,有可能是输入数据有误！")
    msg="两个json对比结果: "+str(result)
    if result==[]:
        return
    for item in result:
        if not isinstance(item,dict):
            raise AssertionError("json_tools的返回结果具体内容不是字典,有可能是输入数据有误！")
        #不处理'add'，只处理'remove'，'replace'
        if 'remove' in item:
            raise AssertionError(msg)
        if 'replace' in item:
            pattern_str = '/\d+'
            pattern = re.compile(pattern_str)
            value_list = pattern.findall(item['replace'])
            if value_list==[]:
                raise AssertionError(msg)

            temp_start = 0
            temp_str = ''
            for value_item in value_list:
                index = item['replace'].index(value_item, temp_start)
                temp_str = temp_str + item['replace'][temp_start:index]
                if not temp_str in lst:
                    for lst_item in lst:
                        if lst_item.index(temp_str)==0 or temp_str.index(lst_item)==0:
                            raise AssertionError("不支持超过1层的list比较")
                    lst.append(temp_str)
                temp_start = index + len(value_item)
    for lst_item in lst:
        son_data=parse_json_by_path(son,lst_item)
        father_data=parse_json_by_path(father,lst_item)
        son_data_length=len(son_data)
        father_data_length = len(father_data)
        if son_data_length>father_data_length:
            raise AssertionError(msg)
        for son_data_item in son_data:
            match1=set()
            for father_data_item in father_data:
                match2=set()
                for son_key,son_value in son_data_item.items():
                    if son_key not in father_data_item:
                        match2.add(False)
                        break
                    father_value = father_data_item[son_key]
                    if type(father_value) != type(son_value):
                        match2.add(False)
                        break
                    if isinstance(son_value,list):
                        match2.add(False)
                        raise AssertionError("不支持超过1层的list比较")
                    if isinstance(son_value, str) or isinstance(son_value, bool) or isinstance(son_value,int) or isinstance(son_value, float):
                        if son_value != father_value:
                            match2.add(False)
                            break
                        match2.add(True)
                if len(match2)==0 or False in match2:
                    continue
                if True in match2:
                    match1.add(True)
                    break
            if len(match1)==0:
                raise AssertionError(msg)
                break



def parse_json_by_path(json,path):
    '''

    :param json:
    :param path:
    :return:
    '''
    arr=path.split('/')
    new_json=json
    for item in arr:
        if item=='':
            continue
        pattern_str = '\d+'
        pattern = re.compile(pattern_str)
        value_list = pattern.findall(item)
        if len(value_list)!=0:
            new_json=new_json[int(value_list[0])]
            continue
        new_json=new_json[item]
    return new_json

diff(son_dict,father_dict)




