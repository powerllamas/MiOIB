import solution
import instance
import evaluator

def binary_similarity(sequence1, sequence2):
    similarity = 0.0
    for e1, e2 in zip(sequence1, sequence2):
        if e1 == e2:
            similarity += 1.0
    return similarity / float(len(min(sequence1, sequence2)))

def ratio_similarity(vector1, vector2):
    similarity = 0.0
    for v1, v2 in zip(vector1, vector2):        
        ratio = float(min(v1, v2)) / float(max(v1,v2))
        similarity += ratio
    similarity = similarity / float(len(vector1))
    return similarity
    
def binary_solution_similarity(solution1, solution2):
    return binary_similarity(solution1.sequence, solution2.sequence)
   
def partial_solution_similarity(solution1, solution2, instance):
    similarity = 0.0
    for e1, e2 in zip(solution1.sequence, solution2.sequence):
        if e1 == e2:
            similarity += 1.0
        else:
            distances_to1 = instance.distance[e1]
            distances_to2 = instance.distance[e2]
            similarity += ratio_similarity(distances_to1, distances_to2) / float(2)
            ratio = ratio_similarity(distances_to1, distances_to2) / float(2)
            distances_from1 = [vector[e1] for vector in instance.distance]
            distances_from2 = [vector[e2] for vector in instance.distance]
            similarity += ratio_similarity(distances_from1, distances_from2) / float(2)
    return float(similarity) / float(len(solution1.sequence))
            