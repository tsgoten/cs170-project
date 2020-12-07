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
    print(old_happiness)

    def get_D():
        D = {}
        D = read_output_file(output_file, G, s)
        room_to_student = {}
        for k, v in D.items():
            room_to_student.setdefault(v, []).append(k)

        def get_room_happiness(arr):
            if calculate_stress_for_room(arr, G) > s / len(room_to_student):
                return -100
            else:
                return calculate_happiness_for_room(arr, G)

        def get_happiness():
            if not is_valid_solution(D, G, s, len(room_to_student)):
                return -100
            else:
                return calculate_happiness(D, G)

        def swap_happiness(n1, n2):
            swap(n1, n2)
            happiness = get_happiness()
            swap(n1, n2)
            return happiness

        def add_student(n1, room):
            room_to_student[room].append(n1)
            r1 = room_to_student[D[n1]]
            old_room = D[n1]
            D[n1] = room
            # i1 = r1.index(n1)
            r1.remove(n1)
            if not r1:
                print('ran', room_to_student)
                room_to_student.pop(old_room)
                index = 0
                temp = {}
                for r in room_to_student.keys():
                    temp[index] = room_to_student[r]
                    index += 1
                room_to_student.clear()
                for k, v in temp.items():
                    room_to_student[k] = v
                D.clear()
                for k, v in convert_dictionary(room_to_student).items():
                    D[k] = v
                print('after', room_to_student)
        
        def add_happiness(n1, room):
            old_room = room_to_student[D[n1]][:]
            old_room.remove(n1)
            new_room = room_to_student[room][:]
            new_room.append(n1)
            happiness_old = get_room_happiness(old_room)
            happiness_new = get_room_happiness(new_room)
            # if len(room_to_student[D[n1]]) == 1:
            #     happiness = get_room_happiness()
            #     remove(n1)
            #     new_room = len(room_to_student) - 1
            # else:
            #     old_room = D[n1]
            #     add_student(n1, room)
            #     happiness = get_happiness()
            #     add_student(n1, old_room)
            #     new_room = room
            if happiness_new > 0:
                return happiness_new + happiness_old
            else:
                return happiness_new

        def swap(n1, n2):
            r1, r2 = room_to_student[D[n1]], room_to_student[D[n2]]
            i1, i2 = r1.index(n1), r2.index(n2)
            r1[i1], r2[i2] = n2, n1
            D[n2], D[n1] = D[n1], D[n2]

        def remove(n1):
            r1 = room_to_student[D[n1]]
            if len(r1) > 1:
                # i1 = r1.index(n1)
                print('called@')
                r1.remove(n1)
                D[n1] = len(room_to_student)
                room_to_student[D[n1]] = [n1]

        def maybe_swap(n1, n2, T):
            curr_hap = get_happiness()
            swap_hap = swap_happiness(n1, n2)
            if swap_hap < 0:
                return
            r = random.random()
            p = math.exp((swap_hap - curr_hap) / T)
            # print(n1, n2, swap_hap, curr_hap, r, p)
            if r < p:
                # print(p)
                # print('SWAPPED!')
                swap(n1, n2)

        def maybe_add(n1, T):
            room = random.randrange(len(room_to_student))
            curr_hap = get_room_happiness(room_to_student[room])
            curr_hap += get_room_happiness(room_to_student[D[n1]])
            # curr_hap *= normalizer
            add_hap= add_happiness(n1, room)
            if add_hap < 0:
                return
            r = random.random()
            p = math.exp((add_hap - curr_hap) / T) 
            # p = 0.05
            # print(n1, n2, add_hap - curr_hap, r, p)
            if r < p and add_hap > 0:
                # print('added')
                add_student(n1, room)
        
        def maybe_remove(n1, T):
            r = random.random()
            p = 0.01
            # p = math.exp((swap_hap - curr_hap) / T)
            # print(n1, n2, swap_hap, curr_hap, r, p)
            if r < p:
                # print(p)
                print('going to remove...', n1, is_valid_solution(D, G, s, len(room_to_student)))
                print(D)
                remove(n1)
                print('removed...', is_valid_solution(D, G, s, len(room_to_student)))
                print(D)
        prev, curr = 0, 0 
        repeats = 0
        for countdown in range(200, 0, -1):
            curr = get_happiness()
            print(curr, room_to_student)
            for _ in range(2000):
                n1, n2 = floor(random.randrange(students * 1.2)), floor(random.randrange(students * 1.2))
                if n2 > students and n1 < students:
                    # Move student into random breakout room that exists
                    # print('adding')
                    maybe_add(n1, countdown)
                # elif n2 < students and n1 > students:
                #     # Move student into breakout room by itself
                #     maybe_remove(n2, countdown)
                    # print('removing')
                elif n1 < students and n2 < students and D[n1] != D[n2]:
                    maybe_swap(n1, n2, countdown)
                    # print('swapping')
            # if curr == prev:
            #     repeats += 1
            # else:
            #     repeats = 0
            # prev = curr
            # if repeats > 8:
            #     break 
        return D, len(room_to_student)


    output, rooms = get_D()
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
#     inputs = glob.glob('larges/*')
#     inputs = sorted(inputs)
#     for input_path in inputs:
#         output_path = 'test_outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         # if not os.path.exists(output_path):
#         G, s = read_input_file(input_path, 100)
#         print("Solving: ", input_path)
#         sol = solve(G, s, output_path)
#         if sol:
#             D, k = sol
#             assert is_valid_solution(D, G, s, k)
#             cost_t = calculate_happiness(D, G)
#             write_output_file(D, output_path)
