# -*- coding: utf-8 -*-

from random_solver import Random
from evaluator import Evaluator


class LocalSearch(object):

    def __init__(self):
        pass

    def solve(self, instance, startpoint=None):
        if startpoint is None:
            startpoint = Random().solve(instance)

        e = Evaluator(instance)
        current = (startpoint, e.evaluate(startpoint))

        changed = True
        while changed:
            changed = False
            for n in current[0].neighbours():
                n_score = e.evaluate(n)
                if n_score < current[1]:
                    current = (n, n_score)
                    changed = True

        return current[0]
