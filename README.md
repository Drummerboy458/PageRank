# PageRank

> Dataset: WikiData.txt

> Data format :
>
> cat -e -t -v makefile /Users/liruifeng/Downloads/WikiData.txt
>
> ...
>
> FromNodeID^IToNodeID^I^M$
>
> ...
>
> FromNodeID 未按顺序排列



Task： you need to report the Top 100 NodeID with their PageRank scores. 

You can choose different parameters, such as the teleport parameter, to compare different results. One result you must report is that when setting the teleport parameter to 0.85.

In addition to the basic PageRank algorithm, you need to implement the Block-Stripe Update algorithm.



要求：

1. 考虑黑洞和spider trap： **黑洞考虑预处理**，**spider trap解决办法是常量，不需要干扰矩阵**
2. 优化稀疏矩阵：**python的话，考虑用数组存，字典没有必要**
3. 实现分块计算：**既然分块，就假设r(new),r(old),M每个单独都装不下，给r(new)分块**
4. 迭代至收敛：**L1范式的差应该定多少呢？**
5. 结果格式：[NodeID] [Score]，.txt文件格式



计划完成顺序：

1. 把数据读入并做排序处理，处理成有序的再写回（方便找黑洞）**ID的意义似乎被我搞错了，这一步没什么有用**

但是可以按ID打包？0-1000，1001-2000，用字典存

如何确认node的个数？遍历一遍，用字典存吧（速度快一点，还可以顺便判断黑洞的情况）

1. 黑洞预处理：碰到黑洞，用全局变量记录，最后挨个分一下就行（同样可以用.txt先存着）

   算完M矩阵的分配后，按照endNodeList中的值，一个一个为所有节点分即可（全局变量，累加，最后一块分）

2. spider trap：~~计算当前节点时~~计算完全部节点，用β/N 给每个节点分一下就可以

3. 

