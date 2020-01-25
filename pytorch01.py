# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 17:08:51 2020

@author: us
"""

import torch
x = torch.rand(5,3)
print(x)

x = torch.empty(5, 3)
print(x)

x = torch.zeros(5, 3, dtype=torch.long)
print(x)

x = x.new_ones(5, 3, dtype=torch.double)      
# new_* methods take in sizes
print(x)

x = torch.randn_like(x, dtype=torch.float)    
# override dtype!
print(x)                                      
# result has the same size

print(x.size())
y = torch.rand(5, 3)
print(x + y)

x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8) 

print(x)
print(x.item())