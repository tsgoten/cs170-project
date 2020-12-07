import networkx as nx
from parse import read_input_file, read_output_file, write_output_file
from utils import *
import sys
import glob, random
from os.path import basename, normpath
import os.path
import math
from math import floor

def solve(G, s, output_file=''):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    students = len(G.nodes) 
    # DEFAULT ASSIGNMENT #
    old_D = read_output_file(output_file, G, s)
    old_happiness = calculate_happiness(old_D, G)
    if old_happiness == 0:
        return
    normalizer = 10000 / (old_happiness + 1)
    print(old_happiness)
    def get_D(rooms):
        D = {}
        D = read_output_file(output_file, G, s)
        room_to_student = {}
        for k, v in D.items():
            room_to_student.setdefault(v, []).append(k)
        rooms = len(room_to_student)
        # for n in room_to_student[rooms - 1]:
        #     D[n] = 0
        # room_to_student[0] += room_to_student.pop(rooms - 1)
        # rooms = len(room_to_student)
        # if rooms < 1:
        #     return D, rooms + 1
        # D = {}

        # # # RANDOM ASSIGNMENT #
        # for n in range(students):
        #     D[n] = random.randrange(rooms)

        # room_to_student = {}
        # for k, v in D.items():
        #     room_to_student.setdefault(v, []).append(k)
        # rooms = len(room_to_student)
        # S = s / rooms
        def get_happiness():

            if not is_valid_solution(D, G, s, len(room_to_student)):
                # return - is_valid_solution_stress(D, G, s, len(room_to_student))
                return -100
            else:
                return calculate_happiness(D, G)

        def swap_happiness(n1, n2):
            swap(n1, n2)
            # r1, r2 = room_to_student[D[n1]], room_to_student[D[n2]]
            # if calculate_stress_for_room(r1, G) > S or calculate_stress_for_room(r2, G) > S:
            happiness = get_happiness()
            swap(n1, n2)
            return happiness

        def swap(n1, n2):
            r1, r2 = room_to_student[D[n1]], room_to_student[D[n2]]
            i1, i2 = r1.index(n1), r2.index(n2)
            r1[i1], r2[i2] = n2, n1
            D[n2], D[n1] = D[n1], D[n2]

        def maybe_swap(n1, n2, T):
            curr_hap = get_happiness() * normalizer
            swap_hap = swap_happiness(n1, n2) * normalizer
            r = random.random()
            p = math.exp((swap_hap - curr_hap) / T)
            # print(n1, n2, swap_hap, curr_hap, r, p)
            if r < p:
                # print(p)
                # print('SWAPPED!')
                # print(room_to_student)
                swap(n1, n2)
        prev, curr = 0, 0
        converged = 0
        for countdown in range(100, 0, -1):
            curr = get_happiness()
            # print(curr)
            for _ in range(200):
                n1, n2 = floor(random.randrange(students)), floor(random.randrange(students))
                if D[n1] != D[n2]:
                    maybe_swap(n1, n2, countdown)
            if prev == curr:
                converged += 1
            prev = curr
            if converged >= 4:
                break
        return D, rooms

    # assns =  [(get_D(rooms), rooms) for rooms in range(1, floor(students))]
    # output, rooms = max(assns, key=lambda d: calculate_happiness(d[0], G))
    # print(calculate_happiness(output, G)) 
    max_rooms = 0
    for i in range(1, len(old_D)):
        if old_D[i] > max_rooms:
            max_rooms = old_D[i]
    max_rooms = max_rooms + 1
    best_output = old_D
    best_rooms = max_rooms
    for i in range(1, max_rooms):
        output, rooms = get_D(i) # <-----------------------------------------------------CHANGE THIS FOR THE ROOMS YOU WANT
        print(output)
        print(is_valid_solution(output, G, s, rooms))
        # print(calculate_happiness(output, G))
        if calculate_happiness(output, G) > old_happiness and is_valid_solution(output, G,s, rooms):
            best_output = output
            best_rooms = rooms
    if best_output == old_D and best_rooms == max_rooms + 1:
        return None
    else:
        return best_output, best_rooms



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     output_path = 'outputs/' + basename(normpath(path))[:-3] + '.out'
#     G, s = read_input_file(path)
#     sol = solve(G, s, output_path)
#     if sol:
#         D, k = sol
#         assert is_valid_solution(D, G, s, k)
#         print("Total Happiness: {}".format(calculate_happiness(D, G)), k)
#         write_output_file(D, 'out/' + output_path)


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)

if __name__ == '__main__':
    inputs = glob.glob('inputs_parallel/Medium/m6/*')
    inputs = sorted(inputs)
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        # if not os.path.exists(output_path):
        G, s = read_input_file(input_path, 100)
        print("Solving: ", input_path)
        sol = solve(G, s, output_path)
        if sol:
            D, k = sol
            assert is_valid_solution(D, G, s, k)
            cost_t = calculate_happiness(D, G)
            write_output_file(D, output_path)
