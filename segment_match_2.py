# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:40:38 2019
基于模式匹配的对话机器人实现 2 *多个匹配
@author: us
"""

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
    
    return (seg_pat, saying), len(saying)

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
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail
    
a=segment_match('?*P is very good'.split(), "My dog and my cat is very good".split())
    
b=pat_match_with_seg('?*P is very good and ?*X'.split(),\
                   "My dog is very good and my cat is very cute".split())
    
c=pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split())   
def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns} 
def subsitite(rule, parsed_rules):
    if not rule: return []    
    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)
d=subsitite("Why do you neeed ?X".split(), \
            pat_to_dict(pat_match_with_seg('I need ?*X'.split(), 
                  "I need an iPhone".split()))) 

   


    
    
    
    
    
    
    
    