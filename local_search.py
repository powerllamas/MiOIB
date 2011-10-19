# -*- coding: utf-8 -*-

from random_solver import Random
from evaluator import Evaluator


class LocalSearch(object):

    def __init__(self):
        pass

    def solve(self, instance, startpoint=None, greedy=False):
        if startpoint is None:
            startpoint = Random().solve(instance)

        e = Evaluator(instance)
        current = (startpoint, e.evaluate(startpoint))

        select_step = self._steepest
        if greedy:
            select_step = self._greedy

        while True:
            next_step = select_step(e, current)
            if not next_step:
                break
            else:
                current = next_step

        return current[0]

    def _greedy(self, evaluator, current):
        for n in current[0].neighbours():
            n_score = evaluator.evaluate(n)
            if n_score < current[1]:
                return (n, n_score)
        return None

    def _steepest(self, evaluator, current):
        best = current
        improved = False
        for n in current[0].neighbours():
            n_score = evaluator.evaluate(n)
            if n_score < best[1]:
                best = (n, n_score)
                improved = True
        if improved:
            return best
        return None
