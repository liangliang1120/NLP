# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:54:02 2019
基于模式匹配的对话机器人实现 3 *多个匹配,中文对话
@author: us
"""

import jieba
import random
import re

def get_response(saying, defined_patterns):
    for (rul,k) in defined_patterns.items():
        rul_jieba = jieba_rule(rul)
        
        saying_jieba = list(jieba.cut(saying))
        got_patterns = pat_match_with_seg(rul_jieba, saying_jieba)
        
        if got_patterns==[True,None]: 
            continue
        else:
            #for patt in got_patterns:
            #    patt[1] = ''.join(patt[1])
            res_rule = random.choice(defined_patterns[rul])
            res = ''.join(subsitite(jieba_rule_res(res_rule), pat_to_dict(got_patterns)))
            return res

def jieba_rule_res(rul):
    if rul:
        try:
            var_p = re.search('\?', rul).span()
            if var_p[0]>0:
                return list(jieba.cut(rul[0:var_p[0]])) + [rul[var_p[0]:var_p[1]+1]] +jieba_rule_res(rul[var_p[1]+1:])
            else:
                return [rul[var_p[0]:var_p[1]+1]] + jieba_rule_res(rul[var_p[1]+1:])
        except:
            return list(jieba.cut(rul))
    else:
        return []
    
def jieba_rule(rul):
    if rul:
        try:
            var_p = re.search('\?\*', rul).span()
            if var_p[0]>0:
                return list(jieba.cut(rul[0:var_p[0]])) + [rul[var_p[0]:var_p[1]+1]] +jieba_rule(rul[var_p[1]+1:])
            else:
                return [rul[var_p[0]:var_p[1]+1]] + jieba_rule(rul[var_p[1]+1:])
        except:
            return list(jieba.cut(rul))
    else:
        return []
        
           
def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])

def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])

def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)    
    
    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i
    
    return [True, None]#(seg_pat, saying), len(saying)

def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

fail = [True, None]

def pat_match_with_seg(pattern, saying):
    if not pattern or not saying: return []
    
    pat = pattern[0]
    
    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        if match == True and index == None:
            return fail
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail

def pat_to_dict(patterns):
    return {k: ''.join(v) if isinstance(v, list) else v for k, v in patterns} 

def subsitite(rule, parsed_rules):
    if not rule: return []    
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)





rule_responses = {    
    '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
    '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了'],
    '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y'],
    '?*x喜欢?*y': ['喜欢?y的哪里？', '?y有什么好的呢？', '你想要?y吗？'],
    '?*x讨厌?*y': ['?y怎么会那么讨厌呢?', '讨厌?y的哪里？', '?y有什么不好呢？', '你不想要?y吗？'],
    '?*xAI?*y': ['你为什么要提AI的事情？', '你为什么觉得AI要解决你的问题？'],
    '?*x机器人?*y': ['你为什么要提机器人的事情？', '你为什么觉得机器人要解决你的问题？'],
    '?*x对不起?*y': ['不用道歉', '你为什么觉得你需要道歉呢?'],
    '?*x我记得?*y': ['你经常会想起这个吗？', '除了?y你还会想起什么吗？', '你为什么和我提起?y'],
    
    '?*x头发?*y': ['早点休息，保护头发', '?x的头发还好吗吗？', '你为什么想起?x的头发'],
    '?*x放假?*y': ['我也等放假好久啦', '放假去哪里玩？'],
    '?*x上海?*y': ['上海有很多好吃的甜品', '你想去上海看东方明珠吗？'],
    '?*x': ['很有趣', '请继续', '我不太确定我很理解你说的, 能稍微详细解释一下吗?']
}



saying='老板我想要冰激凌'
c=get_response(saying, rule_responses)
print(c)

saying='宝贝我想吃饭'
c=get_response(saying, rule_responses)
print(c)

saying='我讨厌很甜的食物'
c=get_response(saying, rule_responses)
print(c)

saying='我喜欢葡萄'
c=get_response(saying, rule_responses)
print(c)

saying='我记得你说过星星的光芒是很多年之前的'
c=get_response(saying, rule_responses)
print(c)

saying='小美头发很多'
c=get_response(saying, rule_responses)
print(c)

saying='放假了可以学习'
c=get_response(saying, rule_responses)
print(c)

saying='周末我在上海'
c=get_response(saying, rule_responses)
print(c)

saying='我饿了'
c=get_response(saying, rule_responses)
print(c)

'''
这样的程序有什么优点？有什么缺点？你有什么可以改进的方法吗？
Ans:优点是可以根据输入内容回答相关的问题，缺点是只能按照事先设计好的模式回答。改进：可以连接网络获取网络上的答案
什么是数据驱动？数据驱动在这个程序里如何体现？

Ans:数据驱动指，收集数据并根据数据组织建模，不改变代码实现过程。
    在这个程序里，根据输入saying的变化，输出respose相应变化，只要设定好模式，可以自动输出对应的回答
    
数据驱动与 AI 的关系是什么？
Ans:AI是基于数据的科学，要做的事情正是让机器对大量的数据自动建模分析，AI是数据驱动的一个应用
'''