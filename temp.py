import re


def fun(raw):
    print('--------')
    print(raw.groups())
    return ""


raw_text = "eq茯苓,茯苓90g,当归牛黄子(后来)20.88g,天然牛黄1/2支醋鳖甲10支白芍10ml醋鳖甲10.99g白芍10g官场"

re.sub(r"([\u4e00-\u9fa5\)]+\d+[\./]?[\d]+(g|支|ml)\B)", fun, raw_text)

import pandas as pd

data = pd.read_csv("./yian_fj_zc.csv", index_col='auto_id', dtype={'fj_zc': 'str'})
for item in data.loc[data['fj_zc'].notna(), 'fj_zc']:
    # print(type(item))
    if re.search(r'(\d+g){2,}', item):
        print('处理前：', item)
        item = re.sub(r"(\d+),(g)", lambda x: x.group(1) + x.group(2), item)
        item = re.sub(r",(\d+g){2,},", ",", item)
        print('处理后：', re.sub(r"(\d+g)(\d+g){1,}", lambda x: x.group(1), item))
