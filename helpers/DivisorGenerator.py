# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 21:16:35 2020

@author: Owner
"""

def divisor_generator(n: int):
    for i in range(1, int(n**0.5+1)):
        if n%i == 0: yield i
    yield n