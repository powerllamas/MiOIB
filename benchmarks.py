import time
import timeit
import os
import re
import argparse

import evaluator
import instance
import heuristic
import random_solver


def compute(inst, algo, n):
    start = time.clock()
    for i in range(n):
        sol = algo.solve(inst)
    stop = time.clock()

    elasped = (stop-start) / float(n)
    eval = evaluator.Evaluator(inst)
    result = eval.evaluate(sol)
    return elasped, result


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description = "Benchmark for optimasation algorithms",
      prog = "benchmarks",
      epilog = u"Authors:\t\tKrzysztof Urban & Tomasz Ziętkiewicz. 2011\nCopyright:\tThis is free software: you are free to change and redistribute it.\n\t\tThere is NO WARRANTY, to the extent permitted by law."
      )
    parser.add_argument('-R', '--random', action='append_const', dest='shoosen_algorithms', const='random', help='Turns on random algorithm')
    parser.add_argument('-H', '--heuristic', action='append_const', dest='shoosen_algorithms', const='heuristic', help='Turns on heuristic algorithm')
    parser.add_argument('-G', '--greedy', action='append_const', dest='shoosen_algorithms', const='greedy', help='Turns on greedy algorithm')
    parser.add_argument('-S', '--steepest', action='append_const', dest='shoosen_algorithms', const='steepest', help='Turns on steepest algorithm')
    parser.add_argument('-n', '--norepeats', help='Number of repeats', default='100')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    
    algorithms = []
    all_algorithms = [("heuristic", heuristic.Heuristic()), ("random", random_solver.Random())]

    for alg in all_algorithms:
        if alg[0] in args.shoosen_algorithms:
            algorithms.append(alg)

    measures = ["quality", "time", "effectiveness"]
    data_dir = "data/"
    results_dir = "results/"
    results = {}

    for alg in algorithms:
        results[alg[0]] = {}
        result_filepath = results_dir + alg[0] + ".dat"
        result_file = open(result_filepath, "w")
        result_file.write("Instance")
        for measure in measures:
            result_file.write(" " + measure)
        result_file.write("\n")
        result_file.close()

    ls = os.walk(data_dir)
    instance_names = []
    for dirpath, dirnames, filenames in ls:
        instance_names += [re.sub(r"\.dat", "", file) for file in filenames if re.search(r"\.dat", file)]
        
    optimal_solutions_values = {}
    for instance_name in instance_names:
        with open(data_dir+instance_name+".sln") as f:
            value = int(f.readline().split()[1])
            optimal_solutions_values[instance_name] = value
       
        
    for instance_name in instance_names:    
        inst = instance.Instance(filename = data_dir+instance_name+".dat")
        print "Instance: " + instance_name
        for alg in algorithms:
            results[alg[0]][instance_name] = {}
            print "\tAlgorithm: " + alg[0]
            n = 10        
            stats = []
            for i in range(1):
                stats.append(compute(inst, alg[1], n))
            fastest = min(stats, key = lambda t: t[0])
            best_result = max(stats, key = lambda t: t[1])
            result_quality =  optimal_solutions_values[instance_name] / best_result[1] * 100.0
            
            results[alg[0]][instance_name]["quality"] = result_quality
            results[alg[0]][instance_name]["time"] = fastest[0]
            results[alg[0]][instance_name]["effectiveness"] = result_quality / fastest[0]
            
            print "\t\tBest time: " + str(fastest[0])
            print "\t\tResult quality: " + str(result_quality)
            # print "Result with best time: " + str(fastest[1])

            print "\t\tBest result: " + str(best_result[1])
            # print "Time of best result: " + str(best_result[0]):
            
    for alg, instances in results.iteritems():
        result_filepath = results_dir + alg + ".dat"
        result_file = open(result_filepath, "a")
        for instance, measures in instances.iteritems():
            result_file.write(instance)
            for measure, value in measures.iteritems():
                result_file.write(" "+str(value))
            result_file.write("\n")
        result_file.close()