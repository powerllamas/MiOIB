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
import similarity

from random_solver import Random
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch

def compute(inst, alg, n, max_time):
    results = []
    startpoints = []
    start = time.clock()
    for i in range(n):
        if alg[0] == "Greedy" or alg[0] == "Tabu" or alg[0] == "Annealing":
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

def multirandom_statistics(qualities):
    bests = []
    best = 0
    sum = 0.0
    means = []
    for q in qualities:
        best = q if q > best else best
        bests.append(best)
        sum += float(q)
        means.append(sum / float(len(bests)))
    return bests, means

def write_multirandom_statistics(currents, bests, means, instance):
    with open(results_dir+"multirandom_"+instance+".dat", "w") as file:
        file.write("i current best mean\n")
        for i, current_best_mean in enumerate(zip(currents, bests, means)):
            current, best, mean = current_best_mean
            file.write("{0} {1} {2} {3}\n".format(i, current, best, mean))
        file.close()

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
        gnuplot_file.write("set output \"gs_comparision_{0}.pdf\"\n plot \"gs_comparision_{0}.dat\" using 1:2 notitle\n unset output\n\n".format(instance))
        result_filepath = results_dir + "gs_comparision_"+instance+".dat"
        with open(result_filepath, "w") as f:
            f.write("Startpoint\tSolution\n")
            for start_quality, solution_quality in qualities:
                f.write(str(start_quality)+"\t"+str(solution_quality)+"\n")
        f.close()
    gnuplot_file.close()

def write_gnuplot_multirandom_commands(instances):
    gnuplot_file = open(results_dir + "gnuplot_multirandom.plt", "w")
    gnuplot_file.write("set ylabel \"Quality\"\n")
    gnuplot_file.write("set xlabel \"Number of restarts\"\n\n")
    gnuplot_file.write("set key right bottom\n\n")

    for instance in gs_comparision:
        gnuplot_file.write("set output \"multirandom_{0}.pdf\"\n plot \"multirandom_{0}.dat\" using 1:2 title columnheader, \"multirandom_{0}.dat\" using 1:3 title columnheader, \"multirandom_{0}.dat\" using 1:4 title columnheader with linespoints \n unset output\n\n".format(instance))
    gnuplot_file.close()

def solutions_similarity(solutions, instance):
    binary_similarities = []
    partial_similarities = []
    for s1 in solutions:
        for s2 in solutions:
            binary_similarities.append(similarity.binary_solution_similarity(s1, s2))
            partial_similarities.append(similarity.partial_solution_similarity(s1, s2, instance))
    return binary_similarities, partial_similarities


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description = "Benchmark for optimisation algorithms.",
      prog = "benchmarks",
      epilog = u"Authors:\t\tKrzysztof Urban & Tomasz Ziętkiewicz. 2011\nCopyright:\tThis is free software: you are free to change and redistribute it.\n\t\tThere is NO WARRANTY, to the extent permitted by law."
      )

    parser.add_argument('-R', '--Random', action='append_const', dest='choosen_algorithms',
                        const='Random', help='Turns on Random algorithm')
    parser.add_argument('-M', '--Multirandom', action='append_const', dest='choosen_algorithms',
                        const='Multirandom', help='Turns on Multirandom algorithm')
    parser.add_argument('-H', '--Heuristic', action='append_const', dest='choosen_algorithms',
                        const='Heuristic', help='Turns on Heuristic algorithm')
    parser.add_argument('-G', '--Greedy', action='append_const', dest='choosen_algorithms',
                        const='Greedy', help='Turns on Greedy algorithm')
    parser.add_argument('-S', '--Steepest', action='append_const', dest='choosen_algorithms',
                        const='Steepest', help='Turns on Steepest algorithm')
    parser.add_argument('-A', '--Annealing', action='append_const', dest='choosen_algorithms',
                        const='Annealing', help='Turns on simulated annealing')
    parser.add_argument('-T', '--Tabu', action='append_const', dest='choosen_algorithms',
                        const='Tabu', help='Turns on tabu search algorithm')
    parser.add_argument('-n', '--norepeats', help='Number of repeats', default='100')
    parser.add_argument('-d', '--data', help='Data dir path', default='data')
    parser.add_argument('-r', '--results', help='Results dir path', default='results')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()

    algorithms = []

    all_algorithms = [("Greedy", local_search.LocalSearch(greedy=True)),
                      ("Steepest", local_search.LocalSearch()),
                      ("Heuristic", heuristic.Heuristic()),
                      ("Random", random_solver.Random()),
                      ("Multirandom", random_solver.Random()),
                      ("Annealing", SimulatedAnnealing()),
                      ("Tabu", TabuSearch())]


    for alg in all_algorithms:
        if alg[0] in args.choosen_algorithms:
            algorithms.append(alg)

    measures = sorted(["quality", "time", "effectiveness", "quality_sd",
                       "best_quality", "z-binary_similarity", "z-partial_similarity", "z-binary_similarity_sd", "z-partial_similarity_sd"])
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
    max_time = 18
    elapsed = 0
    for instance_tuple in instances:
        inst = instance_tuple[1]
        instance_name = instance_tuple[0]
        eval_ = evaluator.Evaluator(inst)
        print "Instance: " + instance_name
        for alg in algorithms:
            results[alg[0]][(instance_name, len(inst))] = {}
            print "\tAlgorithm: " + alg[0]


            if alg[0] == "Heuristic":
                n = 1000
            elif alg[0] in ["Random", "Multirandom"]:
                n = 5000000                
            elif alg[0] in ["Greedy", "Tabu"]:
                n = 100
            elif alg[0] in ["Annealing"]:
                n = 10
            else:
                n = 10

            if alg[0] in ["Greedy", "Steepest", "Annealing", "Tabu"]:
                max_time = 180

            elapsed, mean_time, solutions, startpoints = compute(inst, alg, n, max_time)
            if alg[0] in ["Greedy", "Steepest"]:
                max_time = mean_time*1.001
               
            start = time.clock()
            solutions_performance = [float(eval_.evaluate(solution)) for solution in solutions]
            stop = time.clock()
            eval_time = stop - start
            if alg[0] == "Multirandom":
                elapsed += eval_time
            
            solutions_quality =  [(float(optimal_solutions_values[instance_name]) / solution_performance) * 100.0
                                for solution_performance in solutions_performance]

            solutions_similarities = solutions_similarity(solutions[:10], inst)
            binary_similarities = solutions_similarities[0]
            partial_similarities = solutions_similarities[1]
            mean_binary_similarity = mean(binary_similarities)
            mean_partial_similarity = mean(partial_similarities)
            binary_similarity_sd = sd(binary_similarities, mean_binary_similarity)
            partial_similarity_sd = sd(partial_similarities, mean_partial_similarity)

            if(alg[0] == "Greedy"):
                startpoints_performance = [float(eval_.evaluate(startpoint)) for startpoint in startpoints]
                startpoints_quality =  [(float(optimal_solutions_values[instance_name]) / startpoint_performance) * 100.0
                                for startpoint_performance in startpoints_performance]
                gs_comparision[instance_name] = zip(startpoints_quality, solutions_quality)
                bests, means = multirandom_statistics(solutions_quality)
                write_multirandom_statistics(solutions_quality, bests, means, instance_name)
                #solutions_performance = solutions_performance[:10]
                #solutions_quality = solutions_quality[:10]
                write_gs_comparision(gs_comparision)
                write_gnuplot_multirandom_commands(gs_comparision)

            #mean_result = mean(solutions_performance)
            best_result = min(solutions_performance)
            #worst_result = max(solutions_performance)
            best_quality = optimal_solutions_values[instance_name] / best_result * 100.0
            #worst_quality = optimal_solutions_values[instance_name] / worst_result * 100.0
            mean_quality = mean(solutions_quality[:10])
            quality_sd = sd(solutions_quality[:10], mean_quality)

            results[alg[0]][(instance_name, len(inst))]["quality"] = mean_quality
            results[alg[0]][(instance_name, len(inst))]["time"] = mean_time
            results[alg[0]][(instance_name, len(inst))]["effectiveness"] = mean_quality / mean_time
            results[alg[0]][(instance_name, len(inst))]["quality_sd"] = quality_sd
            results[alg[0]][(instance_name, len(inst))]["best_quality"] = best_quality
            results[alg[0]][(instance_name, len(inst))]["z-binary_similarity"] = mean_binary_similarity
            results[alg[0]][(instance_name, len(inst))]["z-partial_similarity"] = mean_partial_similarity
            results[alg[0]][(instance_name, len(inst))]["z-binary_similarity_sd"] = binary_similarity_sd
            results[alg[0]][(instance_name, len(inst))]["z-partial_similarity_sd"] = partial_similarity_sd
            #results[alg[0]][(instance_name, len(inst))]["worst_quality"] = worst_quality
            
            print "\t\ttime: "+str(elapsed)
            print "\t\tMean Time: " + str(mean_time)
            print "\t\tMean result quality: " + str(mean_quality)
            print "\t\tBest result quality: " + str(best_quality)
            #print "\t\tMean result: " + str(mean_result)
            print "\t\tMean effectiveness: " + str(mean_quality / mean_time)
            print "\t\tQuality SD: " + str(quality_sd)

        write_results(results, measures)


