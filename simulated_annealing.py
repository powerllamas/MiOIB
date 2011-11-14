# -*- coding: utf-8 -*-

from math import exp, log
from random import random

from random_solver import Random as R
from evaluator import Evaluator as E


class SimulatedAnnealing(object):

    def __init__(self, temperature0=None, steps=None, alpha=0.9):
        self.temperature0 = temperature0
        self.steps = steps
        self.alpha = alpha

    def solve(self, instance, startpoint=None):
        if startpoint is None:
            startpoint = R().solve(instance)
        if self.temperature0 is None:
            self.temperature0 = self._guess_temp(instance)
        if self.steps is None:
            self.steps = self._guess_steps(instance)

        e = E(instance)
        current = (startpoint, e.evaluate(startpoint))
        temperature = self.temperature0

        self.iteration = 0
        self._stop_counter = 0
        self._stop_best = current[1]
        best = current

        while not self._stop(current):
            for step in xrange(self.steps):
                for n in current[0].neighbours():
                    n_score = e.evaluate(n)
                    if n_score <= current[1]:
                        current = (n, n_score)
                        if current[1] > best[1]:
                            best = current
                        break
                    else:
                        diff = float(current[1] - n_score)
                        print "{0} {1} {2} {3}".format(diff, temperature, diff / temperature, exp(diff / temperature))
                        p = exp(diff / temperature)
                        if p > random():
                            current = (n, n_score)
                            if current[1] > best[1]:
                                best = current
                            break
                self.iteration += 1
                temperature = self._calc_temp(temperature)
        return best[0]

    def _guess_temp(self, instance, samples=1000, prob=0.95, df=None):
        if df is None:
            r = R()
            e = E(instance)
            diffs = 0
            for i in xrange(samples):
                solution = r.solve(instance)
                neighbour = solution.neighbours().next()
                diff = abs(e.evaluate(solution) - e.evaluate(neighbour))
                diffs += diff
            df = float(diffs) / float(samples)
        return -(df / log(1.0 - prob))

    def _guess_steps(self, instance):
        r = R()
        solution = r.solve(instance)
        neighbours = list(solution.neighbours())
        return len(neighbours)

    def _stop(self, current):
        if self._stop_best > current[1]:
            self._stop_counter += 1
        else:
            self._stop_best = current[1]
            self._stop_counter = 0
        return self._stop_counter > 10

    def _calc_temp(self, temp):
        return temp * self.alpha
