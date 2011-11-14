# -*- coding: utf-8 -*-

from random_solver import Random as R
from evaluator import Evaluator as E


class TabuSearch(object):

    class TabuList(object):
        pass

    def __init__(self):
        pass

    def solve(self, instance, startpoint):
        if startpoint is None:
            startpoint = R().solve(instance)

        e = E(instance)
        current = (startpoint, e.evaluate(startpoint))
        best = current
        self._stop_counter = 0
        self._stop_best = current[1]

        while not self._stop(current):
            pass

        return best[0]

    def _stop(self, current):
        if self._stop_best > current[1]:
            self._stop_counter += 1
        else:
            self._stop_best = current[1]
            self._stop_counter = 0
        return self._stop_counter > 10
