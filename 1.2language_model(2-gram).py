# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:56:52 2019
2-gram复现代码
@author: us
"""
import jieba
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

corpus = 'C:/Users/us/Desktop/article_9k.txt'
FILE = open(corpus,'rb').read()
print(len(FILE))

def cut(string):
    return list(jieba.cut(string))
sub_file = FILE[:1000000]
TOKENS = cut(sub_file)

words_count = Counter(TOKENS)
words_count.most_common(20)
words_with_fre = [f for w, f in words_count.most_common()]
words_with_fre[:10]
plt.plot(np.log(np.log(words_with_fre)))
list(jieba.cut('一加手机5要做市面最轻薄'))
_2_gram_words = [TOKENS[i] + TOKENS[i+1] for i in range(len(TOKENS)-1)]
_2_gram_word_counts = Counter(_2_gram_words)
words_count.most_common()[-1][-1]
def get_1_gram_count(word):
    if word in words_count: return words_count[word]
    else:
        return words_count.most_common()[-1][-1]
def get_2_gram_count(word):
    if word in _2_gram_word_counts: return _2_gram_word_counts[word]
    else:
        return _2_gram_word_counts.most_common()[-1][-1]
def get_gram_count(word, wc):
    if word in wc: return wc[word]
    else:
        return wc.most_common()[-1][-1]
get_gram_count('XXX',words_count)
get_gram_count('XXX', _2_gram_word_counts)

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

two_gram_model('此外自本周6月12日起除小米手机6等15款机型')
