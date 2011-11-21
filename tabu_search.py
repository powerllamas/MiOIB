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
            for move in self._get_filtered_moves(current[0].moves()):
                new_solution = current[0].make_move(move)
                move_score = e.evaluate(new_solution)
                if move_score < current[1]:
                    current = (new_solution, move_score)
                    if move_score < best[1]:
                        best = (new_solution, move_score)
                    self._decrease_tabu_penalty()
                    self.tabu[move] = self.penalty_time
                    break

        return best[0]

    def _stop(self, current):
        if self._stop_best <= current[1]:
            self._stop_counter += 1
        else:
            self._stop_best = current[1]
            self._stop_counter = 0
        return self._stop_counter > 10

    def _decrease_tabu_penalty(self, tabu=None):
        if tabu is None:
            tabu = self.tabu
        for k in tabu.keys():
            tabu[k] -= 1
            if tabu[k] <= 0:
                del tabu[k]

    def _get_filtered_moves(self, moves, tabu=None):
        if tabu is None:
            tabu = self.tabu
        return (move for move in moves if move not in tabu)

    def _select_best_move(self, current, moves, e):
        scored = sorted(moves, key=lambda x: e.evaluate(current.make_move(x)))
        return scored[0]
