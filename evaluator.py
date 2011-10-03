# -*- coding: utf-8 -*-

class Evaluator(object):

    def __init__(self, instance):
        self.instance = instance

    def evaluate(self, solution):
        score = 0
        for y in xrange(len(self.instance)):
            for x in xrange(len(self.instance)):
                pass #TODO score += self.instance.flow[y][solution.sequence[x]] * self.instance.distance[y][x]
        return score
        
