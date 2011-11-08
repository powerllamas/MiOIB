# -*- coding: utf-8 -*-

import unittest

from instance import Instance
from heuristic import Heuristic
from solution import Solution
from local_search import LocalSearch
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
        
    def test_partial_solution_similarity_identical(self):
        expected = 1.0
        actual = similarity.binary_solution_similarity(self.s1, self.s3)
        self.assertEqual(actual, expected)
        
    def test_ratio_similarity(self):
        expected = (1.0 + 2.0/3.0 + 0.5) / 3.0
        actual = similarity.ratio_similarity([3, 4, 2], [3, 6, 1])
        self.assertEqual(actual, expected)
        
    def test_partial_solution_similarity_identical(self):
        expected = 1.0
        actual = similarity.partial_solution_similarity(self.s1, self.s2, self.i)
        self.assertEqual(actual, expected)
        
    def test_partial_solution_similarity_identical2(self):
        expected = 1.0
        actual = similarity.partial_solution_similarity(self.s1, self.s3, self.i2)
        self.assertEqual(actual, expected)
        
    def test_partial_solution_similarity(self):
        expected = (1.0 + 1.0/18.0 + 4.0/30.0 ) / 3.0
        actual = similarity.partial_solution_similarity(self.s1, self.s2, self.i2)
        self.assertAlmostEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
