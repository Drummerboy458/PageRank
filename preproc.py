# -*-coding:utf-8-*-
# 数据预处理
import numpy as np
from pickleSaveLoad import *
import os
import math
from pathlib import Path

deadEndListName = "deadEndList"


# 读入文件并按顺序排好并写回
def dataSort():
    fileName = "./data/WikiData.txt"
    rawData = np.loadtxt(fileName)
    np.savetxt("./data/sortedWikiData.txt", rawData[np.argsort(rawData[:, 0])])


# 生成M矩阵，切块，每块包含ID跨度为1000
def makeDir():
    m_vector = Path("./m_vector")
    r_vector = Path("./r_vector")
    r_new_vector = Path("./r_new_vector")
    deadEndList = Path("./deadEndList")
    if not m_vector.exists():
        os.mkdir('m_vector')
    if not r_vector.exists():
        os.mkdir('r_vector')
    if not deadEndList.exists():
        os.mkdir('deadEndList')

    if not r_new_vector.exists():
        os.mkdir('r_new_vector')


def generateMR():
    makeDir()
    fileName = "./data/sortedWikiData.txt"
    sortedWikiData = np.loadtxt(fileName)
    dict_M = {}  # 存"M矩阵"，格式： {"src":{"degree":degree,"link":[link]}}
    dict_R = {}  # 黑洞是只作为to，不作为from

    #  预处理，寻找黑洞,暂时保存在dict_R中；同时，扫描得到"M矩阵"
    for fromID, toID in sortedWikiData:
        if toID not in dict_R:  # 不能直接覆盖，如果存在就略过，不存在先置为0
            dict_R[toID] = 0
        dict_R[fromID] = 1  # 作为fromNode，必然不是黑洞点

        if fromID in dict_M:
            dict_M[fromID]["degree"] += 1
            dict_M[fromID]["link"].append(toID)
        else:
            dict_M[fromID] = {"degree": 1, "link": [toID]}

    # 计算黑洞点
    deadEnds = []
    for key, value in dict_R.items():
        if value == 0:
            deadEnds.append(key)
    save_deadEnd_list(deadEnds, deadEndListName)

    # R向量是dict_R的所有keys，这里整体储存，作为r_old向量，初始化为1/N
    for key in dict_R.keys():
        dict_R[key] = 1 / len(dict_R)
    save_r_vector(dict_R, str(0))

    # 以下是对M矩阵分片
    for key in dict_M.keys():
        dict_M[key]["link"].sort(reverse=False)  # 对列表进行从小到大排序
        # print(key, dict_M[key]["degree"], dict_M[key]["link"])

    for key in dict_M.keys():
        dict_m_slice = {}
        start = 1000
        degree = dict_M[key]["degree"]

        dict_m_slice[key] = [degree]
        for dest in dict_M[key]["link"]:
            pos = math.ceil(dest / 1000) * 1000
            if start != pos:
                # 需要保存当前结果
                save_M_vector(dict_m_slice, str(start))
                start = pos
                dict_m_slice[key] = [degree]
            dict_m_slice[key].append(dest)

        if bool(dict_m_slice):
            save_M_vector(dict_m_slice, str(start))

    # 以下将r_new向量分片
    flag = 1000
    dict_r_new_slice = {}
    list_R = sorted(dict_R.items(), key=lambda item: item[0], reverse=False)
    for i in range(0, len(list_R)):
        if list_R[i][0] > flag:
            save_r_new_vector(dict_r_new_slice, str(flag))
            flag += 1000
            dict_r_new_slice.clear()
        dict_r_new_slice[list_R[i][0]] = 0
    if bool(dict_r_new_slice):
        save_r_new_vector(dict_r_new_slice, str(flag))
        dict_r_new_slice.clear()
