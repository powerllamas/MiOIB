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

        return best[0]
