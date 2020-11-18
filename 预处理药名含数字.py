import pandas as pd
import re


def translate_Cnumber2Enumber(str):
    dict_ = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    table = {ord(k): ord(v) for k, v in dict_.items()}
    return str.translate(table)


def translate_Enumber2Cnumber(str):
    dict_ = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    table = {ord(v): ord(k) for k, v in dict_.items()}
    return str.translate(table)


# fj_cb = pd.read_excel('./方剂词表.xlsx', header=None)
# fj_cb.columns = ['name']
# for i in range(fj_cb.shape[0]):
#     fj_cb.loc[i, 'name'] = translate_Cnumber2Enumber(fj_cb.loc[i, 'name'])
#
#
# def regex_function(raw):
#     if raw:
#         return True if re.search(r"\d+", raw) else False
#     else:
#         return False
#
#
# df_fliter = fj_cb[fj_cb.loc[:, 'name'].apply(regex_function)]
#
# df_fliter.loc[:, 'name'].to_csv('数字方剂名.csv', index=False)


## 处理含有两个数字的
fj_cb_number = pd.read_csv('数字方剂名.csv')
for item in fj_cb_number['name']:
    m = re.search(r"(.*)(\d)(.*)(\d)(.*)", item)
    if m:
        # print(m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5))
        fj_cb_number.loc[len(fj_cb_number)] = [
            m.group(1) + translate_Enumber2Cnumber(m.group(2)) + m.group(3) + m.group(4) + m.group(5)]
        fj_cb_number.loc[len(fj_cb_number)] = [
            m.group(1) + m.group(2) + m.group(3) + translate_Enumber2Cnumber(
                m.group(4)) + m.group(5)]
fj_cb_number.to_csv('数字方剂名_v2.csv', index=False)
