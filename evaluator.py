# -*- coding: utf-8 -*-


class Evaluator(object):

    def __init__(self, instance, cached=True):
        self.instance = instance
        self.cached = cached
        self.cache = {}

    def evaluate(self, solution):
        if solution.sequence in self.cache:
            return self.cache[solution.sequence]
        score = 0
        flow = self.instance.flow
        distance = self.instance.distance
        sequence = solution.sequence
        for y in xrange(len(self.instance)):
            for x in xrange(len(self.instance)):
                score += flow[y][x] * distance[sequence[y]][sequence[x]]
        if self.cached:
            self.cache[solution.sequence] = score
        return score
