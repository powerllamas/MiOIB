# -*- coding: utf-8 -*-

import random

from solution import Solution


class Random(object):

    def __init__(self):
        pass

    def solve(self, instance):
        sequence = list(xrange(len(instance)))
        random.shuffle(sequence)
        return Solution(tuple(sequence))
