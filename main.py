# -*-coding:utf-8-*-
import json
import time

from pickleSaveLoad import *
from randomTel import beta
from preproc import dataSort, generateMR


def Top100(r_new):
    dict_res = {}
    result = sorted(r_new.items(), key=lambda item: item[1], reverse=True)
    for i in range(0, 100):
        dict_res[result[i][0]] = result[i][1]

    with open('./data/result.json', 'w+') as f:
        json.dump(dict_res, f, ensure_ascii=False, indent=4)
        f.write('\n')
    f.close()

    with open('./data/result.txt', 'w+') as f:
        for key in dict_res.keys():
            f.write(str(key) + "\t" + str(dict_res[key]) + "\n")
    f.close()


# pageRank函数主体处理M*r_old
# r_old在内存中
if __name__ == '__main__':
    dataSort()
    generateMR()
    deadEndList = load_deadEnd_list("deadEndList")
    recur = 0
    err = 1

    time_start = time.time()
    r_old = load_r_vector(str(recur))
    size = len(r_old)
    while err > 0.000001:
        err = 0
        recur += 1
        for M_id in range(1000, 10000, 1000):
            dict_M = load_M_vector(str(M_id))
            r_new = load_r_new_vector(str(M_id))  # 对应分片后M矩阵的r_new向量
            for key in dict_M.keys():
                count = dict_M[key][0]  # 该节点的出度
                val = beta * r_old[key]
                avgVal = val / count
                for node in dict_M[key][1:]:
                    if node not in r_new.keys():
                        print(M_id, key, node)
                    r_new[node] += avgVal
                    # print(key,node,r_new[node])

            save_r_new_vector(r_new, str(M_id))

        # dead_ends的能量分给所有节点，最后都加上一个随机游走，即为这一轮最终的迭代结果
        totalVal = 0
        for item in deadEndList:
            totalVal += r_old[item]
        totalVal = totalVal / size

        randomTelVal = (1 - beta) / size

        for id in range(1000, 10000, 1000):
            r_new = load_r_new_vector(str(id))
            for key in r_new.keys():
                r_new[key] += totalVal + randomTelVal

                err += abs(r_new[key] - r_old[key])  # 计算误差

                r_old[key] = r_new[key]  # 更新r_old

                r_new[key] = 0  # 清0

            save_r_new_vector(r_new, str(id))
    time_end = time.time()
    print("迭代次数：", recur, '\ttime cost：', time_end - time_start, 's')
    # r_old最终结果其实即为r_new的结果
    Top100(r_old)
