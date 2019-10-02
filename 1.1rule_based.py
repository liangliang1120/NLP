# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 15:59:29 2019
#复现课堂代码
@author: us
"""

import random

hello_rules='''
say_hello = names hello tail
names = name names | name
name = kk | mm | bb | pp
hello = hello|hi|你好
tail = ya|!
'''
stmt_split = '='
or_split = '|'
rules=dict()
for line in hello_rules.split('\n'):
    if not line:continue
    stmt,expr = line.split(stmt_split)
    # print(stmt,expr.split(or_split))
    rules[stmt.strip()] = expr.split(or_split)
    
def generate(grammar_rule, target):
    if target in grammar_rule:
        candidates = grammar_rule[target]
        candidate = random.choice(candidates)
        return ''.join(generate(grammar_rule, target=c.strip()) for c in candidate.split())
    else:
        return target
    
c= generate(rules,target='say_hello')
print(c)  

#===============================================================================
    
simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => Adj | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

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
d = get_generation_by_gram(simple_grammar,target='sentence',stmt_split = '=>')
print(d)  


#===============================================================================
     
simpel_programming = '''
if_stmt => if ( cond ) { stmt }
cond => var op var
op => | == | < | >= | <= 
stmt => assign | if_stmt
assign => var = var
var =>  char var | char
char => a | b |  c | d | 0 | 1 | 2 | 3
'''
for i in range(20):
    print(get_generation_by_gram(simpel_programming, target='if_stmt', stmt_split='=>'))
