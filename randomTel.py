#实现随机游走的模块
#设定β，在算完M矩阵的分配后，每一个r的node加上β/n即可
from pickleSaveLoad import save_r_vector
beta=0.85


def randomTel(r_new,recur):
    randomTelVal=(1-beta)/len(r_new)
    for key in r_new.keys():
        r_new[key]+=randomTelVal
    save_r_vector(r_new,recur)

def deadEndsTel(r_new,r_old,deadEndList):
    totalVal=0;
    for item in deadEndList:
        totalVal+=beta*r_old[item]
    totalVal=totalVal/len(r_new)
    for key in r_new.keys():
        r_new[key]+=totalVal

