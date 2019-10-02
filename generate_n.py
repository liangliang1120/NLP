# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:07:22 2019
生成自己的语言
然后，使用自己之前定义的generate函数，使用此函数生成句子。
然后，定义一个函数，generate_n，将generate扩展，使其能够生成n个句子:
@author: us
"""
import random

#点餐机器人询问点餐时的语句生成
host1 = '''
点餐 = 问好 报时 询问 业务相关 结尾
问好 = 称谓 打招呼
称谓 = 人称
人称 = 小朋友 | 女士 | 先生 
打招呼 = 您好 | 欢迎光临
报时 = 现在是 时段
时段 = 早晨 | 下午 | 晚上 | 凌晨
询问 = 请问您是想 | 您需要
业务相关 = 点餐还是别的什么 | 预约
结尾 = 吗？
'''

#上班打卡提醒
remind = '''
提醒 = 打招呼 询问 结尾
打招呼 = 您好, | 你好,
询问 = 请问今天打卡了吗? | 记得打卡哦!
结尾 = 祝您生活愉快！ | 今天又是美好的一天~
'''

    
def generate(grammar_rule, target):
    if target in grammar_rule:
        candidates = grammar_rule[target]
        candidate = random.choice(candidates)
        return ''.join(generate(grammar_rule, target=c.strip()) for c in candidate.split())
    else:
        return target
    
def get_generation_by_gram(grammar_str: str, target, stmt_split='=', or_split='|'):
    rules = dict() # key is the @statement, value is @expression
    for line in grammar_str.split('\n'):
        if not line: continue
        # skip the empty line
      #  print(line)
        stmt, expr = line.split(stmt_split)    
        rules[stmt.strip()] = expr.split(or_split)   
    generated = generate(rules, target=target)    
    return generated

def generate_n(simple_grammar,target, n):
    sentence_n = []
    for i in range(n):
        sentence = get_generation_by_gram(simple_grammar,target)
        sentence_n.append(sentence)
    return sentence_n

if __name__=='__main__':
    result_host = generate_n(host1,'点餐', 5)
    print(result_host)
    
    result_host = generate_n(remind,'提醒', 5)
    print(result_host)