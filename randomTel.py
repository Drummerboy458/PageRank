# 实现随机游走的模块
# 设定β，在算完M矩阵的分配后，每一个r的node加上β/n即可
from pickleSaveLoad import *

beta = 0.85
size = 7115

#
# def randomTel(r_new, recur):
#     randomTelVal = (1 - beta) / len(r_new)
#     for key in r_new.keys():
#         r_new[key] += randomTelVal
#     save_r_vector(r_new, recur)


def deadEndsTel(r_old, deadEndList):
    totalVal = 0;
    for item in deadEndList:
        totalVal += r_old[item]
    totalVal = totalVal / size

    randomTelVal = (1 - beta) / size

    for id in range(1000, 10000, 1000):
        r_new = load_r_new_vector(str(id))
        for key in r_new.keys():
            r_new[key] += totalVal + randomTelVal

        save_r_new_vector(r_new, str(id))
