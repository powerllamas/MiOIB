# -*- coding: utf-8 -*-

class Evaluator(object):

    def __init__(self, instance):
        self.instance = instance

    def evaluate(self, solution):
        score = 0
        flow = self.instance.flow
        distance = self.instance.distance
        sequence = solution.sequence
        for y in xrange(len(self.instance)):
            for x in xrange(len(self.instance)):
                score += flow[y][x] * distance[sequence[y]][sequence[x]]
        return score

