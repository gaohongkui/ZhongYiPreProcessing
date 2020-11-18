import re


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
    pattern = r"[\u4e00-\u9fa5)]+(,\d+[./]?[\d]*(g|支|片|袋|粒|ml|mg|瓶|盒))+"
    fun = lambda x: x.group(0).replace(",", "")
    return re.sub(pattern, fun, raw, flags=re.MULTILINE)


# raw_text = "eq茯苓,茯苓90g,当归牛黄子(后来)20.88g,天然牛黄1/2支醋鳖甲10支白芍10ml醋鳖甲10.99g白芍10g官场"
#
# re.sub(r"([\u4e00-\u9fa5\)]+\d+[\./]?[\d]+(g|支|ml)\B)", fun, raw_text)

import pandas as pd

data = pd.read_excel("./yian_fj_zc_V1.xlsx", index_col='auto_id', dtype=str)
for item in data.loc[data['规范后fj_zc'].notna(), '规范后fj_zc']:
    # print(type(item))
    # if re.search(r"[\u4e00-\u9fa5)]+(,\d+[./]?[\d]*(g|支|片|袋|粒|ml|mg|瓶|盒))+", item):
    #     print('处理前：', item)
    #     print('处理后：', merge_drug_weight(item))
    if re.search(r"l0", item):
        print('处理前：', item)
