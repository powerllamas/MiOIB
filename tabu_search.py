# -*- coding: utf-8 -*-

from random_solver import Random as R
from evaluator import Evaluator as E


class TabuSearch(object):

    def __init__(self):
        pass

    def solve(self, instance, startpoint):
        if startpoint is None:
            startpoint = R().solve(instance)

        return startpoint
