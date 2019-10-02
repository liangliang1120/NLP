# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:53:19 2019
3. 获得最优质的的语言
当我们能够生成随机的语言并且能判断之后，
我们就可以生成更加合理的语言了。
请定义 generate_best 函数，
该函数输入一个语法 + 语言模型，
能够生成n个句子，并能选择一个最合理的句子
@author: us
"""
#import random
#import generate_n 
from generate_n import generate_n
from new_2_gram import two_gram_model
#保险行业询问对话
host1 = '''
询问 = 问好 咨询 业务相关 结尾
问好 = 称谓 打招呼
称谓 = 人称
人称 = 女士 | 先生 
打招呼 = 您好 | 你好
咨询 = 请问 | 我想问一下
业务相关 = 人寿保险 | 财产保险 | 医疗保险
结尾 = 可以吗？| 的具体情况？
'''
result_host = generate_n(host1,'询问', 5)
corpus = 'C:/Users/us/Desktop/train.txt'

def generate_best(result_host): 
    list_ask = []
    for ask_sen in result_host:
        pro = two_gram_model(ask_sen, corpus)
        list_ask.append((pro, ask_sen))
    res = sorted(list_ask, key=lambda x: x[0], reverse=True)
    #print(res)
    return res[0][1]
    pass
result = generate_best(result_host)
print(result)

'''
Q: 这个模型有什么问题？ 你准备如何提升？
Ans:这里判断合语句理性，可能与语料中词语出现的频率相关。模型可能不是特别准确，提升方法：语料补充，模型提升成3-gram
'''
