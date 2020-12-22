# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 20:55:24 2020

@author: Owner
"""
import random
import math

""" Miller-Rabin primality test
        source: https://jeremykun.com/2013/06/16/miller-rabin-primality-test/
"""

def decompose(n):
   exponentOfTwo = 0

   while n % 2 == 0:
      n = n//2  # modified for python 3!
      exponentOfTwo += 1

   return exponentOfTwo, n

def isWitness(possibleWitness, p, exponent, remainder):
   possibleWitness = pow(possibleWitness, remainder, p)

   if possibleWitness == 1 or possibleWitness == p - 1:
      return False

   for _ in range(exponent):
      possibleWitness = pow(possibleWitness, 2, p)

      if possibleWitness == p - 1:
         return False

   return True

def probablyPrime(p, accuracy=100):
   if p == 2 or p == 3: return True
   if p < 2: return False

   exponent, remainder = decompose(p - 1)

   for _ in range(accuracy):
      possibleWitness = random.randint(2, p - 2)
      if isWitness(possibleWitness, p, exponent, remainder):
         return False

   return True

""" Coupon-Collector Problem (approximation)
        How many random-samplings with replacement are expected to observe each element at least once
"""
def couponcollector(n):
    return int(n*math.log(n))

""" Non-prime random-sampling
"""
def get_random_nonprime(min, max):
    max_trials = couponcollector(max-min)
    for i in range(max_trials):
        candidate = random.randint(min, max)
        if not probablyPrime(candidate):
            return candidate
    return -1
