# -*-coding:utf-8-*-
#数据预处理
import numpy as np
from pickleSaveLoad import save_M_vector,save_r_vector,save_deadEnd_list

deadEndListName="deadEndList"
#读入文件并按顺序排好并写回
def dataSort():
    fileName="./data/WikiData.txt"
    rawData = np.loadtxt(fileName)
    np.savetxt("./data/sortedWikiData.txt", rawData[np.argsort(rawData[:, 0])])

#生成M矩阵，切块，每块包含ID跨度为1000
def generateMR():
    fileName="./data/sortedWikiData.txt"
    sortedWikiData = np.loadtxt(fileName)
    flag=1000;
    dict_M={}#id+list，这是存M矩阵的
    dict_R={}#黑洞是只作为to，不作为from
    for fromID,toID in sortedWikiData:
        if toID not in dict_R:#不能直接覆盖，如果存在就略过，不存在先置为0
            dict_R[toID]=0;
        dict_R[fromID]=1#作为fromNode，必然不是黑洞点

        if fromID in dict_M:
            dict_M[fromID][0]+=1
            dict_M[fromID].append(toID)
        else:
            dict_M[fromID]=[1,toID]
        if fromID>flag:
            save_M_vector(dict_M,str(flag))
            flag+=1000
            dict_M.clear()
    if bool(dict_M):
        save_M_vector(dict_M, str(flag))
        dict_M.clear()

    #这一块从dict_R得到符合要求的R向量和黑洞点
    #先算黑洞
    deadEnds=[]
    for key,value in dict_R.items():
        if value==0:
            deadEnds.append(key)
    print(deadEnds)
    save_deadEnd_list(deadEnds,deadEndListName)
    #R向量就是dict_R的所有keys（这里先整体存储）TODO：更细的切分
    count=len(dict_R)
    initval=1/count

    for key in dict_R.keys():
        dict_R[key]=initval
    save_r_vector(dict_R,str(0))
    print(dict_R)
    for key in dict_R.keys():
        dict_R[key]=0
    save_r_vector(dict_R,"empty")
    print("len(M)"+str(len(dict_M)))
    print("len(R"+str(len(dict_R)))
    print("len(dead"+ str(len(deadEnds)))


generateMR()
