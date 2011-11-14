# -*- coding: utf-8 -*-

from math import exp
from random import random

from random_solver import Random as R
from evaluator import Evaluator as E


class SimulatedAnnealing(object):

    def __init__(self, temperature0=None, steps=None):
        self.temperature0 = temperature0
        self.steps = steps

    def solve(self, instance, startpoint=None):
        if startpoint is None:
            startpoint = R().solve(instance)
        if self.temperature is None:
            self.temperature = self._guess_temp(instance)
        if self.steps is None:
            self.steps = self._guess_steps(instance)

        e = E(instance)
        current = (startpoint, e.evaluate(startpoint))
        temperature = self.temperature0

        while not self._stop():
            for step in xrange(self.steps):
                for n in current.neighbours():
                    n_score = e.evaluate(n)
                    if n_score <= current[1]:
                        current = (n, n_score)
                        break
                    else:
                        diff = float(current[0] - n_score)
                        p = exp(diff / temperature)
                        if p > random():
                            current = (n, n_score)
                            break
        return current[0]

    def _guess_temp(self, instance):
        pass

    def _guess_steps(self, instance):
        pass

    def _stop(self):
        return False
