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
    def get_hap(D, G, k):
        if not is_valid_solution(D, G, s, k):
            return -100
        else:
            return calculate_happiness(D, G)

    students = len(G.nodes) 
    # DEFAULT ASSIGNMENT #
    old_D = read_output_file(output_file, G, s)
    old_happiness = calculate_happiness(old_D, G)

    def get_D(rooms):
        D = {}
        D = read_output_file(output_file, G, s)
        # RANDOM ASSIGNMENT #
        # for n in range(students):
        #     D[n] = random.randrange(rooms)

        room_to_student = {}
        for k, v in D.items():
            room_to_student.setdefault(v, []).append(k)
        S = s / len(room_to_student)

        if len(room_to_student) > rooms:
            return D
        # Modify #
        for n in range(len(room_to_student), rooms, 1):
            if rooms > len(room_to_student):
                D[n] = random.randrange(len(room_to_student), rooms)

        room_to_student = {}
        for k, v in D.items():
            room_to_student.setdefault(v, []).append(k)
        S = s / len(room_to_student)
        print(get_hap(D, G, rooms), len(room_to_student))

        def get_happiness():
            if not is_valid_solution(D, G, s, len(room_to_student)):
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
            curr_hap = get_happiness()
            swap_hap = swap_happiness(n1, n2)
            r = random.random()
            p = math.exp((swap_hap - curr_hap) / T)
            # print(n1, n2, swap_hap, curr_hap, r, p)
            if (r < p and swap_hap > 0) or (swap_hap > curr_hap and curr_hap < 0):
                # print('SWAPPED!', rooms)
                swap(n1, n2)
        
        for countdown in range(400, 0, -1):
            for _ in range(students**2):
                n1, n2 = floor(random.randrange(students)), floor(random.randrange(students))
                if D[n1] != D[n2]:
                    maybe_swap(n1, n2, countdown * 10)
        return D

    assns =  [(get_D(rooms), rooms) for rooms in range(1, floor(students))]
    output, rooms = max(assns, key=lambda d: get_hap(d[0], G, d[1]))
    print([get_hap(a, G, b) for a, b in assns])
    # print(calculate_happiness(output, G)) 
    if calculate_happiness(output, G) > old_happiness and is_valid_solution(output, G,s, rooms):
        return output, rooms
    else:
        return None



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    output_path = 'outputs/' + basename(normpath(path))[:-3] + '.out'
    G, s = read_input_file(path)
    sol = solve(G, s, output_path)
    if sol:
        D, k = sol
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)), k)
        write_output_file(D, 'out/' + output_path)


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         # if not os.path.exists(output_path):
#         G, s = read_input_file(input_path, 100)
#         sol = solve(G, s, output_path)
#         if sol:
#             D, k = sol
#             assert is_valid_solution(D, G, s, k)
#             cost_t = calculate_happiness(D, G)
#             write_output_file(D, output_path)
