# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 18:28:14 2019
基于模式匹配的对话机器人实现 1完全匹配
@author: us
"""

def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])


def pat_match(pattern, saying):
    if not pattern or not saying: return []
    
    if is_variable(pattern[0]):
        return [(pattern[0], saying[0])] + pat_match(pattern[1:], saying[1:])
    else:
        if pattern[0] != saying[0]: return []
        else:
            return pat_match(pattern[1:], saying[1:])
#a=pat_match("?X greater than ?Y and ?Z".split(), "3 greater than 2 and 1".split())

'''
如果我们知道了每个变量对应的是什么，那么我们就可以很方便的使用我们定义好的模板进行替换：

为了方便接下来的替换工作，我们新建立两个函数，
一个是把我们解析出来的结果变成一个 dictionary，
一个是依据这个 dictionary 依照我们的定义的方式进行替换
'''
def pat_to_dict(patterns):
    return {k: v for k, v in patterns}

def subsitite(rule, parsed_rules):
    if not rule: return []    
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)

got_patterns = pat_match("I want ?X".split(), "I want iPhone".split())

b=subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns))

' '.join(subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns)))

john_pat = pat_match('?P needs ?X'.split(), "John needs resting".split())
subsitite("Why does ?P need ?X ?".split(), pat_to_dict(john_pat))
' '.join(subsitite("Why does ?P need ?X ?".split(), pat_to_dict(john_pat)))


defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"], 
    "My ?X told me something":\
    ["Talk about more about your ?X", "How do you think about your ?X ?"]
}


#===================================================================================
import random

def get_response(saying, defined_patterns):
    """" please implement the code, to get the response as followings:
    
    >>> get_response('I need iPhone') 
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
    """
    
    for (rul,k) in defined_patterns.items():
        got_patterns = pat_match(rul.split(), saying.split())
        if got_patterns: 
            res_rule = random.choice(defined_patterns[rul])
            res = ' '.join(subsitite(res_rule.split(), pat_to_dict(got_patterns)))
    return res

saying='My mother told me something'
c=get_response(saying, defined_patterns)
print(c)



