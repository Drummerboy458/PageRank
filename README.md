# PageRank

> 李汶蔚
>
> 张婕
>
> 李瑞峰 1711347

[TOC]

# 算法简介和实现思路

要说下核心算法的公式

$$
r_{new}=M*r_{old}
$$

# 数据集说明

输入指令查看下数据集格式

```commonlisp
cat -e -t -v WikiData.txt
```

```
···
8262^I7389^M$
8263^I4940^M$
8263^I7389^M$
8264^I7238^M$
8265^I7238^M$
8266^I7238^M$
7637^I7833^M$
8270^I4940^M$
8270^I7833^M$
8271^I7833^M$
···
```

格式为：

**FromNodeID^IToNodeID^M$**

^M应该是因为该数据集是在windowOS下生成的，所以在linux环境下需要注意。

# 关键代码分析

## 数据预处理

数据预处理的相关函数写在了`preproc.py`文件中。

### 生成必要文件夹

生成文件夹来存储相关数据。

+ `./m_vector`用来存放分块后的M矩阵。
+ `./r_vector`用来存放整体的r矩阵。
+ `./r_new_vector`是用来存分块后的r矩阵。
+ `./deadEndList`是用来存黑洞点集合的。


```python
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
```

### 数据读入

数据读入使用了numpy开源包，根据`FromNodeID`由小到大，将数据处理成更有序的形式存储。为之后生成M矩阵和r矩阵做预备工作。

```python
# 读入文件并按顺序排好并写回
def dataSort():
    fileName = "./data/WikiData.txt"
    rawData = np.loadtxt(fileName)
    np.savetxt("./data/sortedWikiData.txt", rawData[np.argsort(rawData[:, 0])])
```

### 中间结果存储

不同中间结果，对应不同的存储函数和读取函数。借助`pickle`开源包实现。函数在`pickleSaveLoad.py`文件中。

```python
def save_r_new_vector(obj, range):
def load_r_new_vector(range)

def save_M_vector(obj, range)
def load_M_vector(range)

def save_r_vector(obj, recur)
def load_r_vector(recur)

def save_deadEnd_list(obj, name):
def load_deadEnd_list(name)
```

### 矩阵分块

使用排好序的`WikiData`，进行遍历。同时进行两个操作：

1. 将M矩阵按照字典的格式建立（稀疏矩阵存储的解决办法），存储在`dict_M = {}` 中，格式如下:
   ` {"src":{"degree":degree,"link":[link]}}`
   `src`是`FromNodeID`，`degree`是指向的Node总数，`link`里存的就是`ToNodeID`，以数组形式存储。
2. 遍历时，将所有NodeID记录在`dict_R`字典中，同时要标记每个点是作为FromNodeID还是作为ToNodeID，还是两个都有。这个记录是为了筛选出黑洞点。

经过遍历后，得到了`dict_R`和`dict_M = {} `。根据`dict_R`中所有出现过的点，生成r矩阵（未切分），同时赋初始值。根据`dict_R`的标记，筛选出黑洞点，保存在`deadEnds`数组中。对`dict_M`进行切片，本实验中，按照`ToNodeID`号，每1000个为一组，进行切分，结果存在`./m_vector`中。

```python
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

```

## 迭代过程

每次迭代过程，我们以**r<sub>new</sub>**和**r<sub>old</sub>**的L1范式的差来进行判断，本次实验中，阈值为`0.000001`，即如果L1范式的差小于阈值，我们认为其收敛，并根据r矩阵输出Rank前100的结果。

迭代过程的计算主要分为三个点：

+ M矩阵与R矩阵的相乘运算
+ 随机游走
  + 黑洞点的能量补充（均匀分给其余每个节点）
  + （1-β）的随机游走

### M矩阵与R矩阵的相乘运算

核心代码如下:

```python
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
    save_r_new_vector(r_new, str(M_id))
```

之前已经对于M矩阵和r矩阵都分块了，此时只需要循环将小块M矩阵和r矩阵读入，进行相乘得到结果，并保存即可。

### 随机游走

这部分值实际上是常量，可以计算出后，直接加在矩阵上，不需要在相乘运算中实现，有利于减少代码的计算量。核心代码如下，计算出黑洞点们分给每个节点的totalVal，计算出（1-β）的随机游走的randomTelVal，遍历r矩阵，将常量加上，再计算L1范式判断是否需要继续迭代。

```python
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
```

# 主机运行结果

优化下显示

# 实验结果



# 结果分析



实验报告内容（包括但不限于）：数据集说明、关键代码细节、云主机运行截图、实验结果、结果分析等



程序源码。C，C++，JAVA，Python，四者之一。无需提交数据集，但是需要在实验报告中说明数据调用 位置。



可执行文件。请说明具体运行方式，提交前请确认在其他电脑上也可以运行。C/C++ 编译选择release 方式 进行静态编译（debug方式生成的exe文件在其他电脑上运行可能会有缺少dll文件等问题）。JAVA 和Python 请借助第三方软件生成exe可执行文件，并集成相关依赖包。
