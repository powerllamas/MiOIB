import time
import os
import re
import argparse
import math

import evaluator
import instance
import heuristic
import random_solver
import local_search
from random_solver import Random

def compute(inst, alg, n, max_time):
    results = []
    startpoints = []
    start = time.clock()
    for i in range(n):
        if alg[0] == "greedy":
            startpoint = Random().solve(inst)
            startpoints.append(startpoint)
            results.append(alg[1].solve(inst, startpoint))
        else:
            results.append(alg[1].solve(inst))
        elapsed = (time.clock()-start)
        if elapsed >= max_time:
            break
    stop = time.clock()
    elapsed = (stop-start)
    mean_time = elapsed  / float(len(results)) 
        
    return elapsed, mean_time, results, startpoints
    
def mean(data):
    return sum(data) / len(data)
    
def sd(data, mean):
    return math.sqrt(sum([math.pow(x - mean, 2) for x in data])/(len(data) ))    

def write_results(results, measure_names):
    for alg, instances in results.iteritems():
        result_filepath = results_dir + alg + ".dat"
        result_file = open(result_filepath, "w")
        result_file.write("N Instance")
        for measure in sorted(measure_names):
            result_file.write(" " + measure)
        result_file.write("\n")
        counter = 0
        for instance in sorted(instances, key=lambda i:i[1]):            
            counter+=1#instance[1]
            result_file.write(str(counter)+" ")
            result_file.write(instance[0])
            measures = instances[instance]
            for measure in sorted(measure_names):
                value = measures[measure]
                result_file.write(" "+str(value))
            result_file.write("\n")
        result_file.close()

def write_gs_comparision(gs_comparision):
    gnuplot_file = open(results_dir + "gnuplot_gs.plt", "w")
    for instance, qualities in gs_comparision.items():
        gnuplot_file.write("set output \"gs_comparision.{0}.pdf\"\n plot \"gs_comparision.{0}.dat\" using 1:2 title columnheader\n unset output\n\n".format(instance))    
        result_filepath = results_dir + "gs_comparision."+instance+".dat"    
        with open(result_filepath, "w") as f:
            f.write("Startpoint\tSolution\n")
            for start_quality, solution_quality in qualities:
                f.write(str(start_quality)+"\t"+str(solution_quality)+"\n")
        f.close()
    gnuplot_file.close()
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description = "Benchmark for optimasation algorithms",
      prog = "benchmarks",
      epilog = u"Authors:\t\tKrzysztof Urban & Tomasz Ziętkiewicz. 2011\nCopyright:\tThis is free software: you are free to change and redistribute it.\n\t\tThere is NO WARRANTY, to the extent permitted by law."
      )
    parser.add_argument('-R', '--random', action='append_const', dest='choosen_algorithms', const='random', help='Turns on random algorithm')
    parser.add_argument('-H', '--heuristic', action='append_const', dest='choosen_algorithms', const='heuristic', help='Turns on heuristic algorithm')
    parser.add_argument('-G', '--greedy', action='append_const', dest='choosen_algorithms', const='greedy', help='Turns on greedy algorithm')
    parser.add_argument('-S', '--steepest', action='append_const', dest='choosen_algorithms', const='steepest', help='Turns on steepest algorithm')
    parser.add_argument('-n', '--norepeats', help='Number of repeats', default='100')
    parser.add_argument('-d', '--data', help='Data dir path', default='data')
    parser.add_argument('-r', '--results', help='Results dir path', default='results')
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    
    algorithms = []
    all_algorithms = [("greedy", local_search.LocalSearch(greedy=True)), ("steepest", local_search.LocalSearch()), ("heuristic", heuristic.Heuristic()), ("random", random_solver.Random())]

    for alg in all_algorithms:
        if alg[0] in args.choosen_algorithms:
            algorithms.append(alg)

    measures = sorted(["quality", "time", "effectiveness", "quality_sd", "best_quality"])
    data_dir = args.data+"/"
    results_dir = args.results+"/"    
    results = {}
    gs_comparision = {}
    
    for alg in algorithms:
        results[alg[0]] = {}


    ls = os.walk(data_dir)
    instance_names = []
    for dirpath, dirnames, filenames in ls:
        instance_names += [re.sub(r"\.dat", "", file) for file in filenames if re.search(r"\.dat", file)]
        
    instances = sorted(
                        [(instance_name, instance.Instance(filename = data_dir+instance_name+".dat")) 
                         for instance_name in instance_names],
                         key=lambda i:len(i[1]))
        
    optimal_solutions_values = {}
    for instance_name in instance_names:
        with open(data_dir+instance_name+".sln") as f:
            value = int(f.readline().split()[1])
            optimal_solutions_values[instance_name] = value

    n = 10        
    max_time = 180      
    elapsed = 0    
    for instance_tuple in instances:    
        inst = instance_tuple[1]
        instance_name = instance_tuple[0]
        eval_ = evaluator.Evaluator(inst)  
        print "Instance: " + instance_name       
        for alg in algorithms:
            results[alg[0]][(instance_name, len(inst))] = {}
            print "\tAlgorithm: " + alg[0]
            
            
            if alg[0] == "heuristic":
                n = 1000
            elif alg[0] == "random":
                n = 5000000
            elif alg[0] == "greedy":
                n = 100
            else:
                n = 10              
            
            if alg[0] in ["greedy", "steepest"]:
                max_time = 180
            
            elapsed, mean_time, solutions, startpoints = compute(inst, alg, n, max_time)                
            print "\t\ttime: "+str(elapsed)
            if alg[0] in ["greedy", "steepest"]:
                max_time = elapsed*1.001

            solutions_performance = [eval_.evaluate(solution) for solution in solutions]
            solutions_quality =  [optimal_solutions_values[instance_name] / solution_performance * 100.0
                                for solution_performance in solutions_performance]

            if(alg[0] == "greedy"):
                startpoints_performance = [eval_.evaluate(startpoint) for startpoint in startpoints]
                startpoints_quality =  [optimal_solutions_values[instance_name] / startpoint_performance * 100.0
                                for startpoint_performance in startpoints_performance]
                solutions_performance = solutions_performance[:10]
                solutions_quality = solutions_quality[:10]
                                
            #mean_result = mean(solutions_performance)
            best_result = min(solutions_performance)
            #worst_result = max(solutions_performance)
            best_quality = optimal_solutions_values[instance_name] / best_result * 100.0
            #worst_quality = optimal_solutions_values[instance_name] / worst_result * 100.0
            mean_quality = mean(solutions_quality)
            quality_sd = sd(solutions_quality, mean_quality)
            
            results[alg[0]][(instance_name, len(inst))]["quality"] = mean_quality            
            results[alg[0]][(instance_name, len(inst))]["time"] = mean_time
            results[alg[0]][(instance_name, len(inst))]["effectiveness"] = mean_quality / mean_time
            results[alg[0]][(instance_name, len(inst))]["quality_sd"] = quality_sd
            results[alg[0]][(instance_name, len(inst))]["best_quality"] = best_quality
            #results[alg[0]][(instance_name, len(inst))]["worst_quality"] = worst_quality
            
            print "\t\tMean Time: " + str(mean_time)
            print "\t\tMean result quality: " + str(mean_quality)
            print "\t\tBest result quality: " + str(best_quality)
            #print "\t\tMean result: " + str(mean_result)
            print "\t\tMean effectiveness: " + str(mean_quality / mean_time)
            print "\t\tQuality SD: " + str(quality_sd)
                                                
            write_results(results, measures)
                        
            if(alg[0] == "greedy"):
                gs_comparision[instance_name] = zip(solutions_quality, startpoints_quality)
        write_gs_comparision(gs_comparision)