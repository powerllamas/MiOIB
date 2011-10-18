# -*- coding: utf-8 -*-

from solution import Solution

class Heuristic(object):

    def __init__(self):
        pass

    def sorted_list(self, matrix, reversed):
        list = []
        for row_index, row in enumerate(matrix):
            list += [(row_index, column_index, flow_value) for column_index, flow_value in enumerate(matrix[row_index]) if column_index != row_index]
        list.sort(key = lambda d: d[2], reverse = reversed)
        return list

    def unique_rows_columns(self, list):
        unique = []
        used = {}
        for el in list:
            if el[0] not in used and el[1] not in used:
                used[el[0]] = 1
                used[el[1]] = 1
                unique.append(el[0])
                unique.append(el[1])
        return unique

    def append_unpaired(self, unique, size):
        if len(unique)  < size:
            for el in range(size):
                if el not in unique:
                    unique.append(el)

    def solve(self, instance):
        flows = self.sorted_list(instance.flow, True)
        distances = self.sorted_list(instance.distance, False)

        unique_distances = self.unique_rows_columns(distances)
        unique_flows = self.unique_rows_columns(flows)
        self.append_unpaired(unique_distances, len(instance.distance))
        self.append_unpaired(unique_flows, len(instance.flow))

        solution = [pair[0] for pair in sorted(zip(unique_distances, unique_flows), key = lambda p: p[1])]

        return Solution(tuple(solution))

