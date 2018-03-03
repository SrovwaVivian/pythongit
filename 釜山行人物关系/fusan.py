#coding:utf-8
import os,sys
import jieba,codecs,math
import jieba.posseg as pseg

names = {}
relationships = {}
lineNames = []
"""
使用字典类型names保存人物，该字典的键为人物名称，值为该人物在全文中出现的次数。使用字典类型relationships保存人物关系的有向边，
该字典的键为有向边的起点，值为一个字典edge，edge的键是有向边的终点，值是有向边的权值，代表两个人物之间联系的紧密程度。
lineNames是一个缓存变量，保存对每一段分词得到当前段中出现的人物名称，lineName[i]是一个列表，列表中存储第i段中出现过的人物。

"""
jieba.load_userdict('dict.txt')
with codecs.open('busan.txt','r','utf-8') as f:
    for line in f.readlines():
        poss = pseg.cut(line)
        lineNames.append([])
        for w in poss:
            if w.flag != 'nr' or len(w.word)<2:
                continue
            lineNames[-1].append(w.word)
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1

# for name,times in names.items():
#     print(name,times)        
# print(lineNames)
# print(relationships)

for line in lineNames:
    for name1 in line: 
        for name2 in line: #每段任意两个人
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:#两人未同时出现则新建项
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] += 1#两人同时出现则次数加１
"""
将已经建好的 names 和 relationships 输出到文本，以方便 gephi 可视化处理。
输出边的过程中可以过滤可能是冗余的边，这里假设共同出现次数少于 3 次的是冗余边，则在输出时跳过这样的边。
输出的节点集合保存为 busan_node.txt ，边集合保存为 busan_edge.node 。
"""                
with codecs.open('fusan_node.txt','w','gbk') as f:
    f.write('Id Label Weight\r\n')
    for name,times in names.items():
        f.write(name+' '+name+' '+str(times)+'\r\n')

with codecs.open('fusan_edge.txt','w','gbk') as f:
    f.write('Sourde Target Weight\r\n')
    for name,edges in relationships.items():
        for v,w in edges.items():
            if w>3:
                f.write(name+' '+v+' '+str(w)+'\r\n')

