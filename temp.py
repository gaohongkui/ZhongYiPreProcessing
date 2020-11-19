import re

units = "g|支|克|片|袋|粒|ml|mg|瓶|盒|包"


def fun(raw):
    print('--------')
    print(raw.groups())
    return ""


def merge_drug_weight(raw):
    '''
    将药名与克数中夹带，的情况合并
    桑枝,20g
    制附片(先熬30分钟),20g
    天然牛黄,1/2支
    :param raw:
    :return:
    '''
    pattern = r"[\u4e00-\u9fa5)]+(,\d+[./]?[\d]*(g|支|克|片|袋|粒|ml|mg|瓶|盒))+"
    fun = lambda x: x.group(0).replace(",", "")
    return re.sub(pattern, fun, raw, flags=re.MULTILINE)


def translate_Enumber2Cnumber(str):
    dict_ = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    table = {ord(v): ord(k) for k, v in dict_.items()}
    return str.translate(table)


def covert_number2Chinese(raw):
    pattern = r"(1贯煎|3金2石2子汤|七叶\d+枝花|3七|2花|五42汤|\d+陈汤|\d+物汤|\d+仙|\d+逆|\d+妙|" \
              r"\d+拗汤|\d+君子|\d+陈|\d+子|\d+仁|\d+苓散|\d+散|\d+至丸|\d+白|\d+碧|\d+棱)"

    return re.sub(pattern, lambda x: translate_Enumber2Cnumber(x.group(0)), raw)


def split_drugs(raw):
    '''
    拆分多味药
    醋鳖甲10g白芍10g
    醋鳖甲10支白芍10ml醋鳖甲10g白芍10g
    :param raw:
    :return:
    '''
    pattern = r"([\u4e00-\u9fa5)]+\d+[./]?[\d]*(" + units + r")\B)"

    return re.sub(pattern, lambda x: x.group(1) + ",", raw, flags=re.MULTILINE)


def add_units(raw):
    pattern = r"([\u4e00-\u9fa5)]+)(\d+),?([\u4e00-\u9fa5(]+?)"
    raw = re.sub(pattern, lambda x: x.group(1) + x.group(2) + 'g,' + x.group(3), raw)
    raw = raw.replace("g,条", "条")
    return raw


# raw_text = "eq茯苓,茯苓90g,当归牛黄子(后来)20.88g,天然牛黄1/2支醋鳖甲10支白芍10ml醋鳖甲10.99g白芍10g官场"
#
# re.sub(r"([\u4e00-\u9fa5\)]+\d+[\./]?[\d]+(g|支|ml)\B)", fun, raw_text)

import pandas as pd

# fj_number = pd.read_csv("数字方剂名_v2.csv")
# print(fj_number.head())


data = pd.read_excel("./yian_fj_zc_V1_1.xlsx", index_col='auto_id', dtype=str)
count = 0
for item in data.loc[data['规范后fj_zc'].notna(), '规范后fj_zc']:
    # print(type(item))
    item = split_drugs(covert_number2Chinese(merge_drug_weight(item)))
    if re.search(r"([\u4e00-\u9fa5)]+\d+,?[\u4e00-\u9fa5(]+\d+)+", item):
        count += 1
        print('处理前：', item)

        print('处理后：', add_units(raw=item))
print(count)
# if re.search(r"l0", item):
#     print('处理前：', item)
