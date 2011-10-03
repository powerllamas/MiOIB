# -*- coding: utf-8 -*-

import random

from solution import Solution

class Random(object):

    def __init__(self, instance):
        self._instance = instance

    def solve(self):
        sequence = list(xrange(len(self._instance)))
        random.shuffle(sequence)
        return Solution(tuple(sequence))
        
