# -*- coding: utf-8 -*-

from collections import defaultdict

from random_solver import Random as R
from evaluator import Evaluator as E


class TabuSearch(object):

    def __init__(self, penalty_time=None, candidate_list_length=None):
        self.penalty_time = penalty_time
        self.candidate_list_length = candidate_list_length

    def solve(self, instance, startpoint):
        if startpoint is None:
            startpoint = R().solve(instance)

        self.tabu = defaultdict(int)

        if self.penalty_time is None:
            penalty = len(instance) // 4 or 1
        else:
            penalty = self.penalty_time

        if self.candidate_list_length is None:
            nr_of_moves = len(instance) // 10 or 1
        else:
            nr_of_moves = self.candidate_list_length

        list_of_moves = []

        e = E(instance)
        current = (startpoint, e.evaluate(startpoint))
        best = current

        self._update_stop_criteria(counter=0, best_score=current[1])

        while not self._stop(current):
            self._fill_moves(current, list_of_moves, nr_of_moves, e)
            for move in self._get_filtered_moves(
                    list_of_moves, e, current):
                new_solution = current[0].make_move(move)
                move_score = e.evaluate(new_solution)
                if move_score < current[1]:
                    current = (new_solution, move_score)
                    if move_score < best[1]:
                        best = (new_solution, move_score)
                    self._decrease_tabu_penalty()
                    self.tabu[move] = penalty
                    break

        return best[0]

    def _update_stop_criteria(self, counter=None, best_score=None):
        if counter is not None:
            self._stop_counter = counter
        if best_score is not None:
            self._stop_best = best_score

    def _stop(self, current):
        if self._stop_best <= current[1]:
            self._stop_counter += 1
        else:
            self._update_stop_criteria(counter=0, best_score=current[1])
        return self._stop_counter > 10

    def _fill_moves(self, current, moves, nr_of_moves, e):
        if len(moves) <= nr_of_moves // 2:
            found = self._select_best_moves(current[0],
                    current[0].moves(), e, nr_of_moves)
            moves[:] = found

    def _decrease_tabu_penalty(self, tabu=None):
        if tabu is None:
            tabu = self.tabu
        for k in tabu.keys():
            tabu[k] -= 1
            if tabu[k] <= 0:
                del tabu[k]

    def _get_filtered_moves(self, moves, e=None, current=None, tabu=None):
        if tabu is None:
            tabu = self.tabu
        if e is None or current is None:
            filter_f = lambda m: m not in tabu
        else:
            filter_f = (lambda m: m not in tabu
                    or e.evaluate(current[0].make_move(m)) > current[1])
        return (move for move in moves if filter_f(move))

    def _select_best_move(self, current, moves, e):
        moves = self._select_best_moves(current, moves, e, 1)
        return moves[0] if len(moves) > 0 else None

    def _select_best_moves(self, current, moves, e, amount):
        scored = sorted(moves, key=lambda x: e.evaluate(current.make_move(x)))
        return scored[0:amount]
