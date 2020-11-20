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


def handle_po_bid(raw):
    pattern = r",?(((qd|bid|po|tid|ivgtt|iv|st|ivgt),?)+)"

    def fun(m):
        return '(' + m.group(1).rstrip(',') + '),'

    raw = re.sub(pattern, fun, raw).rstrip(',')
    return raw


def split_diff_fj(raw):
    if re.search(r"(\(2\)|②|乙方|2方|2诊|2,)", raw):
        if re.search(r"1,.*2,", raw):
            raw = raw.replace("1,", "")
            raw = re.sub(r",?\d,", ";", raw)
        if re.search(r"\(1\).*\(2\)", raw):
            raw = raw.replace("(1)", "")
            raw = re.sub(r",?\(\d\),?", ";", raw)
        elif re.search(r"①.*②", raw):
            raw = raw.replace("①", "")
            raw = re.sub(r",?[①②③④⑤⑥⑦⑧⑨],?", ";", raw)
        elif re.search(r"甲方.*乙方", raw):
            raw = re.sub(r",?([乙丙丁戊己庚辛壬葵]方:?)", lambda x: ";" + x.group(1), raw)
        elif re.search(r"1方.*2方", raw):
            raw = re.sub(r",?(第?[2-9]方[,:]?)", lambda x: ";" + x.group(1), raw)
        elif re.search(r"初诊.*2诊", raw):
            raw = re.sub(r",?([2-9]诊[,:]?)", lambda x: ";" + x.group(1), raw)
    return raw.strip(",")


import pandas as pd
import string

# fj_number = pd.read_csv("数字方剂名_v2.csv")
# print(fj_number.head())


data = pd.read_excel("./yian_fj_zc_V2.xlsx", index_col='auto_id', dtype=str)
count = 0
for auto_id, (item, message, info_additional) in data.loc[
    data['规范后fj_zc'].notna(), ['规范后fj_zc', '处理方式', '信息补充']].iterrows():
    # print(type(item))
    # if re.search(r"(\(2\)|②|乙方|2方|2诊|2,)", item):
    #     split_diff_fj(raw=item)
    if re.search(r"(\(2\)|②|乙方|2方|2诊|2,)", item):
        count += 1
        print('处理前：', auto_id, item)

        print('处理后：', auto_id, split_diff_fj(raw=item))
print(count)
# if re.search(r"l0", item):
#     print('处理前：', item)
