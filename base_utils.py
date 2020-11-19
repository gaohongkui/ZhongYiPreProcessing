import re
import string


def number2chinese_numerals(raw):
    dict_ = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    return dict_[raw]


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
    去除首尾的，
    去除连续重复的，
    去除以“治以，处方”开头的文字
    :param raw:
    :return:
    '''
    raw = re.sub("[" + string.whitespace + "]+", "", raw)
    raw = raw.lstrip("处方:")
    raw = raw.lstrip("处方,")
    raw = raw.strip(",")
    raw = raw.lstrip("治以")
    raw = raw.lstrip("处方:")
    raw = re.sub(r",{2,}", ",", raw)
    return raw


def merger_drug_name(raw):
    '''
    去除药名中的特殊字符（主要是标点符号）
    :param raw:
    :return:
    '''
    # pattern = r"茯[\^%&.',;=?$\x22|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]+苓"
    drug_names = ["茯苓", "当归", "牛黄子", "茯苓草","生甘草"]
    for drug in drug_names:
        drug_split = [i for i in drug]
        drug_pattern = ("[" + string.punctuation + "]*").join(drug_split)
        # print(("["+string.punctuation+"]").join(drug))
        # pattern = r"茯[" + string.punctuation + "]+苓"
        raw = re.sub(drug_pattern, drug, raw, flags=re.MULTILINE)
        # print(raw)
    return raw
    # print(re.findall(drug_pattern, raw))


def merger_drug_weight(raw):
    '''
    将药名与克数中夹带，的情况合并
    桑枝,20g
    制附片(先熬30分钟),20g
    天然牛黄,1/2支
    :param raw:
    :return:
    '''
    pattern = r"[\u4e00-\u9fa5)]+,\d+[\./]?[\d]*(g|支|克|片|袋|粒|ml|mg|瓶|盒)"
    fun = lambda x: x.group(0).replace(",", "")
    return re.sub(pattern, fun, raw, flags=re.MULTILINE)


def split_drugs(raw):
    '''
    拆分多味药
    醋鳖甲10g白芍10g
    醋鳖甲10支白芍10ml醋鳖甲10g白芍10g
    :param raw:
    :return:
    '''
    pattern = r"([\u4e00-\u9fa5\)]+\d+[\./]?[\d]*(g|支|克|片|袋|粒|ml|mg|瓶|盒)\B)"

    fun = lambda x: x.group(1) + ","

    print(re.sub(pattern, fun, raw, flags=re.MULTILINE))


if __name__ == '__main__':
    raw_text = "钩藤10g白芷6g辛夷6g白芍10ml醋鳖甲10.99g白芍10g大黄汤150ml入胃管，云南白药胶囊,0.25g×32/0.5g,po,bid,"
    raw_text = C_trans_to_E(raw_text)
    print(raw_text)
    raw_text = remove_head_tail(raw_text)
    print(raw_text)
    raw_text = merger_drug_name(raw_text)
    print(raw_text)
    raw_text = merger_drug_weight(raw_text)
    print(raw_text)
    split_drugs(raw_text)
