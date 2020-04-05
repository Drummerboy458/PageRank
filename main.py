# -*-coding:utf-8-*-
from pickleSaveLoad import load_r_vector,load_M_vector,load_deadEnd_list
from randomTel import randomTel,deadEndsTel,beta
import numpy as np
import time


deadEndList=load_deadEnd_list("deadEndList")
#使用L1范式判断结构是否收敛到一定程度
def test(r_new,r_old):
    limitation=0.000001
    sum=0
    for key in r_new.keys():
        sum+=(r_new[key]-r_old[key])
    if abs(sum)<limitation:
        print(sum)
        return True
    else:
        print(sum)
        return False

def Top100(r_new):
    result = sorted(r_new.items(), key=lambda item: item[1], reverse=True)
    np.savetxt("./data/result.txt",result)


#pageRank函数主体处理M*r_old
#先实现r向量不分块的写法：每次取出一块M，在一块M中每次选一个key，从r_old中找对应的值，乘完挨个加到r_new
#r_new是整个存在内存中的
if __name__ == '__main__':
    flag=False
    recur=0
    while not flag:
        r_new = load_r_vector("empty")
        r_old=load_r_vector(str(recur))
        for M_id in range(1000,10000,1000):
            dict_M=load_M_vector(str(M_id))
            for key in dict_M.keys():
                count=dict_M[key][0]#该节点的N
                val=beta*r_old[key]
                avgVal=val/count
                for node in dict_M[key][1:]:
                    r_new[node]+=avgVal

        recur+=1
        deadEndsTel(r_new,r_old,deadEndList)
        randomTel(r_new,str(recur))
        flag=test(r_new,r_old)
    Top100(r_new)



