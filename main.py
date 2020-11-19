import pandas as pd
import string
import re
import numpy as np

units = "g|支|克|片|袋|粒|ml|mg|瓶|盒|包"


def get_fj_cb():
    fj_cb = pd.read_excel('./方剂词表.xlsx', header=None)
    fj_cb.columns = ['name']
    return fj_cb['name'].tolist()


def C_trans_to_E(str):
    '''
    中文符号转为英文符号
    :param string:
    :return:
    '''
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    return str.translate(table)


def remove_head_tail(raw):
    '''
    去除空格、制表符、换行
    去除首尾的，号
    去除以“治以，处方”开头的文字
    :param raw:
    :return:
    '''
    raw = re.sub("[" + string.whitespace + "]+", "", raw)
    raw = raw.lstrip("治以处方:,")

    return raw


def replace_l_with1(raw):
    '''
    将错误的lI替换为1
    :param raw:
    :return:
    '''
    message = ''
    if re.search(r"[lI]+[,\d]*(" + units + ")", raw):
        raw = re.sub(r"[lI]+[,\d]*(" + units + ")",
                     lambda x: x.group(0).replace("l", "1").replace("I", "1"), raw)
        message += '将错误的lI替换为1;'
    return raw, message


def merge_duplicate_number_dot_g(raw):
    '''
    去除连续重复的，号
    合并数字，g。例如吴茱萸3,g,黄连3,g
    去除重复出现xxgxxgxxg
    :param raw:
    :return:
    '''
    message = ''
    if re.search(r",{2,}", raw):
        raw = re.sub(r",{2,}", ",", raw)
        message += '去除连续重复的，号;'
    if re.search(r"(\d+),(g)", raw):
        raw = re.sub(r"(\d+),(g)", lambda x: x.group(1) + x.group(2), raw)
        message += '合并数字，g;'
    if re.search(r",(\d+g){2,},", raw):
        raw = re.sub(r",(\d+g){2,},", ",", raw)  # 先处理很多重复
        message += '删除多个重复,xxgxxgxxg,;'
    if re.search(r"(\d+g)(\d+g)+", raw):
        raw = re.sub(r"(\d+g)(\d+g)+", lambda x: x.group(1), raw)  # 再处理多选一的情况
        message += '多个xxgxxg选一个'

    return raw, message


def merge_drug_name(raw):
    '''
    去除药名中的特殊字符（主要是标点符号）
    :param raw:
    :return:
    '''
    message = ''
    drug_names = ["茯苓", "通草", "竹茹", "丹参", "姜夏", "黄连", "仙茅",
                  "黄柏", "胆星", "黄精", "蝉衣", "黄芩", "生地", "连翘",
                  "党参", "赤芍", "红枣", "防风", "甘草", "枳实", "佩兰",
                  "虎杖", "川穹", "当归", "百部", "茵陈", "山药", "山萸",
                  "牛膝", "郁金", "麦冬", "黄芪", "苏木", "红花", "水蛭",
                  "泽兰", "泽泻", "苍术", "白术", "陈皮", "川断", "萹蓄",
                  "桃仁", "制军", "桔梗", "玄参", "射干", "银花", "制蚕",
                  "蝉衣", "石苇", "地龙", "石韦", "制军", "荷叶", "小蓟",
                  "扁蓄", "乌药", "川贝", "远志", "茯神", "橘红", "青皮",
                  "葛根", "秦艽", "薤白", "法夏", "甘松", "半夏", "红参",
                  "桂枝", "猪苓", "坤草", "钩藤", "川芎", "苦参", "炮姜",
                  "熟地", "泡参", "杜仲", "天冬", "百合", "大枣",
                  "防己", "米仁", "砂仁", "麻黄", "狗脊", "佛手",
                  "香附", "香橼", "瓜蒌", "桑椹", "枸杞", "淮山", "桃红", "白英",
                  "玉竹", "丹皮", "桑枝", "黄苓", "白芍", "柴胡",
                  "龟板", "云苓", "何首乌", "细辛", "全蝎", "寄生", "菊花",
                  "浙贝", "杏仁", "芦根", "天麻", "藿香", "桑叶", "紫草", "茜草",
                  "莪术", "龙骨", "牡蛎", "苡仁", "蜈蚣", "薄荷", "枳壳", "菖蒲",
                  "干姜", "焦3仙"]
    flag = False
    # 处理A_BC型
    if re.search(r"[\u4e00-\u9fa5]+_[\u4e00-\u9fa5]+", raw):
        flag = True

        def fun(m):
            return m.group(0).replace('_', '')

        raw = re.sub(r"[\u4e00-\u9fa5]+_[\u4e00-\u9fa5]+", fun, raw)
    for drug in drug_names:
        drug_split = [i for i in drug]
        if len(drug_split) > 2:
            drug_pattern = (drug_split[0] + "[" + string.punctuation + "]+") + \
                           ("[" + string.punctuation + "]*").join(drug_split[1:])
        else:
            drug_pattern = ("[" + string.punctuation + "]+").join(drug_split)
        # print(drug_pattern)
        # print(("["+string.punctuation+"]").join(drug))
        # pattern = r"茯[" + string.punctuation + "]+苓"
        if re.search(drug_pattern, raw):
            flag = True
            raw = re.sub(drug_pattern, drug, raw, flags=re.MULTILINE)
    if flag:
        message += '去除药名中的特殊字符;'
    return raw, message


def merge_drug_weight(raw):
    '''
    将药名与克数中夹带，的情况合并
    桑枝,20g
    制附片(先熬30分钟),20g
    天然牛黄,1/2支
    :param raw:
    :return:
    '''
    message = ''
    pattern = r"[\u4e00-\u9fa5)]+(,\d+[./]?[\d]*(g|支|克|片|袋|粒|ml|mg|瓶|盒))+"
    if re.search(pattern, raw):
        raw = re.sub(pattern, lambda x: x.group(0).replace(",", ""), raw, flags=re.MULTILINE)
        message += '将药名与单位中夹带，号的情况合并;'
    return raw, message


def translate_Enumber2Cnumber(str):
    dict_ = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    table = {ord(v): ord(k) for k, v in dict_.items()}
    return str.translate(table)


def covert_number2Chinese(raw):
    '''
    将药名中含有小写数字的转为大写
    :param raw:
    :return:
    '''
    message = ''
    pattern = r"(1贯煎|3金2石2子汤|七叶\d+枝花|3七|2花|五42汤|\d+陈汤|\d+物汤|\d+仙|\d+逆|\d+妙|" \
              r"\d+拗汤|\d+君子|\d+陈|\d+子|\d+仁|\d+苓散|\d+散|\d+至丸|\d+白|\d+碧|\d+棱)"
    if re.search(pattern, raw):
        raw = re.sub(pattern, lambda x: translate_Enumber2Cnumber(x.group(0)), raw)
        message += '将药名中含有小写数字的转为大写;'

    return raw, message


def split_drugs(raw):
    '''
    拆分多味药
    醋鳖甲10g白芍10g
    醋鳖甲10支白芍10ml醋鳖甲10g白芍10g
    :param raw:
    :return:
    '''
    message = ''
    pattern = r"([\u4e00-\u9fa5)]+\d+[./]?[\d]*(" + units + r")\B)"
    if re.search(pattern, raw):
        raw = re.sub(pattern, lambda x: x.group(1) + ",", raw, flags=re.MULTILINE)
        message += '拆分多味药名没分割的情况;'
    return raw, message


def add_units(raw):
    '''
    给药品添加单位g;
    :param raw:
    :return:
    '''
    message = ''
    pattern = r"([\u4e00-\u9fa5)]+)(\d+),?([\u4e00-\u9fa5(]+?)"
    if re.match(r"([\u4e00-\u9fa5)]+\d+,?[\u4e00-\u9fa5(]+\d+)+", raw):
        raw = re.sub(pattern, lambda x: x.group(1) + x.group(2) + 'g,' + x.group(3), raw)
        raw = raw.replace("g,条", "条")
        message += '给药品添加单位g;'
    return raw, message


if __name__ == '__main__':
    data = pd.read_excel("./yian_fj_zc_V1_1.xlsx", index_col='auto_id', dtype=str)
    # print(data.dtypes)
    data.replace(np.nan, '', inplace=True)
    # print(data.columns)
    # data.to_excel("./yian_fj_zc_V0.xlsx", engine='xlsxwriter')

    for auto_id, (item, message) in data.loc[data['规范后fj_zc'].notna(), ['规范后fj_zc', '处理方式']].iterrows():
        try:
            item = item.strip(",")
            # res = C_trans_to_E(item)
            # res = remove_head_tail(res)
            # res, msg = replace_l_with1(res)
            # message += msg
            # res, msg = merge_duplicate_number_dot_g(res)
            # message += msg
            # res, msg = merge_drug_name(raw=res)
            # message += msg
            res, msg = merge_drug_weight(item)
            message += msg
            res, msg = covert_number2Chinese(res)
            message += msg
            res, msg = split_drugs(res)
            message += msg
            res, msg = add_units(res)
            message += msg

            data.loc[auto_id, '规范后fj_zc'] = res
            data.loc[auto_id, '处理方式'] = message
        except Exception as e:
            print(e)
            print(auto_id, item)
            data.loc[auto_id, '规范后fj_zc'] = item
            break
    data.to_excel("./yian_fj_zc_V2.xlsx", engine='xlsxwriter')
    # merger_drug_name("丹参20g,瓜蒌20g,炙_甘草10g,桂枝10g,竹茹10g,枳壳10g,白术10g,陈皮10g,半夏10g,生地15g,茯苓15g,麦冬15g,党参15g")
