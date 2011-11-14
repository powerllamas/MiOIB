# -*- coding: utf-8 -*-

from collections import defaultdict

from random_solver import Random as R
from evaluator import Evaluator as E


class TabuSearch(object):

    def __init__(self, penalty_time=5):
        self.penalty_time = penalty_time

    def solve(self, instance, startpoint):
        if startpoint is None:
            startpoint = R().solve(instance)

        self.tabu = defaultdict(int)

        e = E(instance)
        current = (startpoint, e.evaluate(startpoint))
        best = current
        self._stop_counter = 0
        self._stop_best = current[1]

        while not self._stop(current):
            for move in current[0].moves():
                new_solution = current[0].make_move(move)
                move_score = e.evaluate(new_solution)
                if move_score > current[1]:
                    current = (new_solution, move_score)
                    if move_score > best[1]:
                        best = (new_solution, move_score)
                    self._decrease_tabu_penalty()
                    self.tabu[move] = self.penalty_time
                    break

        return best[0]

    def _stop(self, current):
        if self._stop_best > current[1]:
            self._stop_counter += 1
        else:
            self._stop_best = current[1]
            self._stop_counter = 0
        return self._stop_counter > 10

    def _decrease_tabu_penalty(self):
        for k in self.tabu.iterkeys():
            self.tabu[k] -= 1
            if self.tabu[k] <= 0:
                del self.tabu[k]
