# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:15:29 2019
new-2-gram
2. 使用新数据源完成语言模型的训练
按照我们上文中定义的prob_2函数，我们更换一个文本数据源，获得新的Language Model:

下载文本数据集（你可以在以下数据集中任选一个，也可以两个都使用）
可选数据集1，保险行业问询对话集： 
https://github.com/Computing-Intelligence/insuranceqa-corpus-zh/raw/release/corpus/pool/train.txt.gz
可选数据集2：豆瓣评论数据集：
https://github.com/Computing-Intelligence/datasource/raw/master/movie_comments.csv
修改代码，获得新的2-gram语言模型
进行文本清洗，获得所有的纯文本
将这些文本进行切词
送入之前定义的语言模型中，判断文本的合理程度
@author: us
"""
import jieba
from collections import Counter
import pandas as pd
import re

corpus = 'C:/Users/us/Desktop/train.txt'
FILE = open(corpus,'rb').read()
# print(len(FILE))
df = pd.read_table(corpus,header=None)
corpus = ''.join(df[0].tolist())
# 提取中文语料

def get_chinese(line):
    line_chinese = re.findall('[\u4e00-\u9fa5]+',line,re.S)
    return line_chinese
TOKENS = ''.join(get_chinese(corpus))

def cut(string):
    return list(jieba.cut(string))
TOKENS = cut(TOKENS)

#两个词一组
_2_gram_words = [TOKENS[i] + TOKENS[i+1] for i in range(len(TOKENS)-1)]



#两词计数
_2_gram_word_counts = Counter(_2_gram_words)
#每个词计数
words_count = Counter(TOKENS)
'''
def get_1_gram_count(word):
    #输入word的计数
    if word in words_count: return words_count[word]
    else:
        return words_count.most_common()[-1][-1]
def get_2_gram_count(word):
    #输入俩字词的计数
    if word in _2_gram_word_counts: return _2_gram_word_counts[word]
    else:
        return _2_gram_word_counts.most_common()[-1][-1]
'''
def get_gram_count(word, wc):
    #输入word，从wc这个dict匹配计数数量
    if word in wc: return wc[word]
    else:
        return wc.most_common()[-1][-1]
#
get_gram_count('你',words_count)
#
get_gram_count('那么', _2_gram_word_counts)

def two_gram_model(sentence):
    # 2-gram langauge model
    tokens = cut(sentence)    
    probability = 1    
    for i in range(len(tokens)-1):
        word = tokens[i]
        next_word = tokens[i+1]        
        _two_gram_c = get_gram_count(word+next_word, _2_gram_word_counts)
        _one_gram_c = get_gram_count(next_word, words_count)
        pro =  _two_gram_c / _one_gram_c        
        probability *= pro    
    return probability  

pro = two_gram_model('这个保险什么时候赔付')
print(pro)
