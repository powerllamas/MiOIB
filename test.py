# -*- coding: utf-8 -*-

import unittest

from collections import defaultdict

from evaluator import Evaluator as E
from instance import Instance
from heuristic import Heuristic
from solution import Solution
from local_search import LocalSearch
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
import similarity


class Test_heuristic(unittest.TestCase):

    def setUp(self):
        self.flow = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]
               ]
        self.distance = [
                [0, 5, 2],
                [1, 0, 1],
                [6, 2, 0]
               ]
        self.i = Instance(None, self.distance, self.flow)
        self.h = Heuristic()

    def test_sorted_list_flow(self):
        expected = [(2, 0, 7), (1, 2, 5), (1, 0, 4),
                (0, 2, 2), (2, 1, 2), (0, 1, 1)]
        actual = self.h.sorted_list(self.i.flow, True)
        self.assertEqual(actual, expected)

    def test_sorted_list_distance(self):
        expected = [(1, 0, 1), (1, 2, 1), (0, 2, 2),
                (2, 1, 2), (0, 1, 5), (2, 0, 6)]
        actual = self.h.sorted_list(self.i.distance, False)
        self.assertEqual(actual, expected)

    def test_unique_rows_columns_flow(self):
        expected = [2, 0, 1]
        actual = self.h.unique_rows_columns(
                self.h.sorted_list(self.i.flow, True))
        self.h.append_unpaired(actual, len(self.i.flow))
        self.assertEqual(actual, expected)

    def test_unique_rows_columns_distance(self):
        expected = [1, 0, 2]
        actual = self.h.unique_rows_columns(
                self.h.sorted_list(self.i.distance, False))
        self.h.append_unpaired(actual, len(self.i.distance))
        self.assertEqual(actual, expected)

    def test_heuristic_solution(self):
        expected = Solution((0, 2, 1))
        actual = self.h.solve(self.i)
        self.assertTupleEqual(actual.sequence, expected.sequence)


class TestLocalSearch(unittest.TestCase):

    def setUp(self):
        self.flow = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]]
        self.distance = [
                [0, 5, 2],
                [1, 0, 1],
                [6, 2, 0]]
        self.i = Instance(None, self.distance, self.flow)
        self.ls_steepest = LocalSearch()
        self.ls_greedy = LocalSearch(greedy=True)
        self.startpoint = Solution((0, 1, 2))

    def test_solve_steepest_with_startpoint(self):
        expected = (2, 1, 0)
        actual = self.ls_steepest.solve(self.i, self.startpoint).sequence
        self.assertEqual(expected, actual)

    def test_solve_greedy_with_startpoint(self):
        expected = (2, 1, 0)
        actual = self.ls_greedy.solve(self.i, self.startpoint).sequence
        self.assertEqual(expected, actual)

class TestSimulatedAnnealing(unittest.TestCase):

    def setUp(self):
        self.flow = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]]
        self.distance = [
                [0, 5, 2],
                [1, 0, 1],
                [6, 2, 0]]
        self.i = Instance(None, self.distance, self.flow)
        self.sa = SimulatedAnnealing()
        self.startpoint = Solution((0, 1, 2))

    def test_solve_with_startpoint(self):
        expected = (2, 1, 0)
        actual = self.sa.solve(self.i, self.startpoint).sequence
        self.assertEqual(expected, actual)

    def test_guess_temperature(self):
        expected = 255.0
        actual = self.sa._guess_temp(None, prob=0.98, df=1000)
        self.assertAlmostEqual(expected, actual, -1)

    def test_guess_temperature_for_given_instance(self):
        expected = 3.5
        actual = self.sa._guess_temp(self.i, prob=0.95)
        self.assertAlmostEqual(expected, actual, 0)

class TestTabuSearch(unittest.TestCase):

    def setUp(self):
        self.flow = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]]
        self.distance = [
                [0, 5, 2],
                [1, 0, 1],
                [6, 2, 0]]
        self.i = Instance(None, self.distance, self.flow)
        self.e = E(self.i)
        self.ts = TabuSearch()
        self.startpoint = Solution((0, 1, 2))

    def test_filter_moves(self):
        moves = [(1,2), (1,3), (2,3)]
        tabu = defaultdict(int, {(1,2): 1, (2,3): 1})
        expected = [(1,3)]
        actual = list(self.ts._get_filtered_moves(moves, tabu=tabu))
        self.assertEqual(expected, actual)

    def test_filter_moves_with_aspiration(self):
        self.i = Instance(None, self.distance, self.flow)
        self.e = E(self.i)
        self.startpoint = Solution((2, 1, 0))

        moves = [(0,1), (0,2), (1,2)]
        tabu = defaultdict(int, {(0,1): 1, (1,2): 2, (0,2): 3})
        expected = [(0,1), (0,2), (1,2)]
        actual = list(self.ts._get_filtered_moves(moves, e=self.e,
            current=(self.startpoint, self.e.evaluate(self.startpoint)),
            tabu=tabu))
        self.assertEqual(expected, actual)

    def test_decrease_tabu_penalty(self):
        tabu = defaultdict(int, {(1,2): 2, (2,3): 1})
        expected = [(1,2)]
        self.ts._decrease_tabu_penalty(tabu)
        actual = tabu.keys()
        self.assertEqual(expected, actual)

    def test_select_best_move(self):
        current = self.startpoint
        moves = [(0,1), (0,2), (1,2)]
        expected = (0,2)
        actual = self.ts._select_best_move(current, moves, self.e)
        self.assertEqual(expected, actual)

    def test_with_startpoint(self):
        expected = (2, 1, 0)
        actual = self.ts.solve(self.i, self.startpoint).sequence
        self.assertEqual(expected, actual)

class SimilarityTest(unittest.TestCase):
    def setUp(self):
        self.s1 = Solution((0,1,2))
        self.s2 = Solution((0,2,1))
        self.s3 = Solution((0,1,2))
        self.flow = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]]
        self.distance = [
                [0, 5, 5],
                [4, 2, 2],
                [4, 2, 2]]
        self.i = Instance(None, self.distance, self.flow)

        self.flow2 = [
                [0, 1, 2],
                [4, 0, 5],
                [7, 2, 0]]
        self.distance2 = [
                [0, 5, 2],
                [1, 0, 1],
                [6, 2, 0]]
        self.i2 = Instance(None, self.distance2, self.flow2)

    def test_binary_similarity(self):
        expected = 0.3333333333333333
        actual = similarity.binary_solution_similarity(self.s1, self.s2)
        self.assertAlmostEqual(actual, expected)

    def test_partial_solution_similarity_identical1(self):
        expected = 1.0
        actual = similarity.binary_solution_similarity(self.s1, self.s3)
        self.assertEqual(actual, expected)

    def test_ratio_similarity(self):
        expected = (1.0 + 2.0/3.0 + 0.5) / 3.0
        actual = similarity.ratio_similarity([3, 4, 2], [3, 6, 1])
        self.assertEqual(actual, expected)

    def test_partial_solution_similarity_identical2(self):
        expected = 1.0
        actual = similarity.partial_solution_similarity(self.s1, self.s2, self.i)
        self.assertEqual(actual, expected)

    def test_partial_solution_similarity_identical3(self):
        expected = 1.0
        actual = similarity.partial_solution_similarity(self.s1, self.s3, self.i2)
        self.assertEqual(actual, expected)

    def test_partial_solution_similarity(self):
        expected = (1.0 + 1.0/18.0 + 4.0/30.0 ) / 3.0
        actual = similarity.partial_solution_similarity(self.s1, self.s2, self.i2)
        self.assertAlmostEqual(actual, expected)

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.s = Solution((0, 1, 2))

    def test_move_generation(self):
        expected = [(0, 1), (0, 2), (1, 2)]
        actual = list(self.s.moves())
        self.assertEqual(actual, expected)

    def test_make_move1(self):
        expected = (1, 0, 2)
        actual = self.s.make_move((0, 1)).sequence
        self.assertEqual(actual, expected)

    def test_make_move2(self):
        expected = (2, 1, 0)
        actual = self.s.make_move((0, 2)).sequence
        self.assertEqual(actual, expected)

    def test_make_move3(self):
        expected = (0, 2, 1)
        actual = self.s.make_move((1, 2)).sequence
        self.assertEqual(actual, expected)

    def test_neighbours_generation(self):
        expected = [(1, 0, 2), (2, 1, 0), (0, 2, 1)]
        actual = map(lambda s: s.sequence, list(self.s.neighbours()))
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
