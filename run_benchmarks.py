import time
import timeit
import os
import re

import benchmarks
import evaluator
import instance
import heuristic
import random_solver


#timer = Timer(stmt='benchmark.Bench_Heuristic.compute()', setup='benchmark.Bench_Heuristic.setup()',  timer=time.clock())

# results = min(timeit.repeat(stmt='benchmarks.Heuristic_benchmark.compute(h)', 
                            # setup='import benchmarks; h = benchmarks.Heuristic_benchmark.setup()',
                            # timer=time.clock, repeat=5, number=n))

 # print "Execution time: " + str(results/n)

# results = min(timeit.repeat(stmt='benchmarks.Random_benchmark.compute(r)',
                            # setup='import benchmarks; r = benchmarks.Random_benchmark.setup()',
                            # timer=time.clock, repeat=5, number=n))

# print "Execution time: " + str(results/n)



def measure(inst, algo, n):
    start = time.clock()
    for i in range(n):
        sol = algo.solve(inst)
    stop = time.clock()

    elasped = (stop-start) / float(n)
    eval = evaluator.Evaluator(inst)
    result = eval.evaluate(sol)
    return elasped, result
    
algorithms = [("Heuristic", heuristic.Heuristic()), ("Random", random_solver.Random())]
data_dir = "data/"

ls = os.walk(data_dir)
instance_names = []
for dirpath, dirnames, filenames in ls:
    instance_names += [re.sub(r"\.dat", "", file) for file in filenames if re.search(r"\.dat", file)]
    
optimal_solutions_values = {}
for instance_name in instance_names:
    with open(data_dir+instance_name+".sln") as f:
        value = int(f.readline().split()[1])
        optimal_solutions_values[instance_name] = value
        
print optimal_solutions_values.items()
    
for instance_name in instance_names:
    inst = instance.Instance(filename = data_dir+instance_name+".dat")
    print "Instance: " + instance_name
    for alg in algorithms:
        print "\tAlgorithm: " + alg[0]
        n = 10
        results = []
        for i in range(1):
            results.append(measure(inst, alg[1], n))
        fastest = min(results, key = lambda t: t[0])
        best_result = max(results, key = lambda t: t[1])
        result_quality =  optimal_solutions_values[instance_name] / best_result[1] * 100.0

        print "\t\tBest time: " + str(fastest[0])
        print "\t\tResult quality: " + str(result_quality)
        # print "Result with best time: " + str(fastest[1])

        print "\t\tBest result: " + str(best_result[1])
        # print "Time of best result: " + str(best_result[0])