# -*- coding: utf-8 -*-

from itertools import combinations

class Solution(object):

    def __init__(self, sequence):
        self.sequence = sequence

    def neighbours(self):
        for x, y in combinations(self.sequence, 2):
            old = list(self.sequence)
            old[x], old[y] = old[y], old[x]
            neighbour = Solution(tuple(old))
            yield neighbour

    def __str__(self):
        return str(self.sequence)

    def __repr__(self):
        return str(self)

