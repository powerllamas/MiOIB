import time
import timeit
import os
import re
import argparse
import math

import evaluator
import instance
import heuristic
import random_solver

def compute(inst, algo, n):
    results = []
    start = time.clock()
    for i in range(n):
        results.append(algo.solve(inst))
    stop = time.clock()
    elasped = (stop-start)
    mean_time = elasped / float(n) 
        
    return mean_time, results
    
def mean(data):
    return sum(data) / len(data)
    
def sd(data, mean):
    return math.sqrt(sum([math.pow(x - mean, 2) for x in data])/(len(data) - 1))    

def print_results(results, measure_names):
    for alg, instances in results.iteritems():
        result_filepath = results_dir + alg + ".dat"
        result_file = open(result_filepath, "a")
        counter = 0
        for instance in sorted(instances, key=lambda i:i[1]):            
            counter+=1#instance[1]
            result_file.write(str(counter)+" ")
            result_file.write(instance[0])
            measures = instances[instance]
            for measure in measure_names:
                value = measures[measure]
                result_file.write(" "+str(value))
            result_file.write("\n")
        result_file.close()
    
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
    parser.add_argument('-d', '--data', help='Data dir path', default='data')
    parser.add_argument('-r', '--results', help='Results dir path', default='results')
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    
    algorithms = []
    all_algorithms = [("heuristic", heuristic.Heuristic()), ("random", random_solver.Random()), ("greedy", local_search.LocalSearch(greedy=True)), ("steepest", local_search.LocalSearch())]

    for alg in all_algorithms:
        if alg[0] in args.shoosen_algorithms:
            algorithms.append(alg)

    measures = sorted(["quality", "time", "effectiveness", "quality_sd", "best_quality", "worst_quality"])
    data_dir = args.data+"/"
    results_dir = args.results+"/"    
    results = {}

    for alg in algorithms:
        results[alg[0]] = {}
        result_filepath = results_dir + alg[0] + ".dat"
        result_file = open(result_filepath, "w")
        result_file.write("N Instance")
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
        eval = evaluator.Evaluator(inst)  
        print "Instance: " + instance_name
        for alg in algorithms:
            results[alg[0]][(instance_name, len(inst))] = {}
            print "\tAlgorithm: " + alg[0]
            n = 10        
            mean_time, solutions = compute(inst, alg[1], n)                

            solutions_performance = [eval.evaluate(solution) for solution in solutions]
            solutions_quality =  [optimal_solutions_values[instance_name] / solution_performance * 100.0
                                for solution_performance in solutions_performance]

            mean_result = mean(solutions_performance)
            best_result = min(solutions_performance)
            worst_result = max(solutions_performance)
            best_quality = optimal_solutions_values[instance_name] / best_result * 100.0
            worst_quality = optimal_solutions_values[instance_name] / worst_result * 100.0
            mean_quality = mean(solutions_quality)
            quality_sd = sd(solutions_quality, mean_quality)
            
            results[alg[0]][(instance_name, len(inst))]["quality"] = mean_quality            
            results[alg[0]][(instance_name, len(inst))]["time"] = mean_time
            results[alg[0]][(instance_name, len(inst))]["effectiveness"] = mean_quality / mean_time
            results[alg[0]][(instance_name, len(inst))]["quality_sd"] = quality_sd
            results[alg[0]][(instance_name, len(inst))]["best_quality"] = best_quality
            results[alg[0]][(instance_name, len(inst))]["worst_quality"] = best_quality
            
            print "\t\tMean Time: " + str(mean_time)
            print "\t\tMean result quality: " + str(mean_quality)
            print "\t\tMean result: " + str(mean_result)
            print "\t\tQuality SD: " + str(quality_sd)
            
            
    print_results(results, measures)