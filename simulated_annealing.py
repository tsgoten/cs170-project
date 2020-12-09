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
    old_assignment = {}
    for k, v in old_D.items():
        old_assignment.setdefault(v, []).append(k)
    old_rooms = len(old_assignment)

    def get_D():
        new_high, best_D, best_k = 0, None, 100
        D = {}
        for n in range(students):
            D[n] = 0
        nonlocal s
        # D = read_output_file(output_file, G, s)
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
            r1.remove(n1)
            if not r1:
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
        
        def add_happiness(n1, room):
            old_room = room_to_student[D[n1]][:]
            old_room.remove(n1)
            new_room = room_to_student[room][:]
            new_room.append(n1)
            happiness_old = get_room_happiness(old_room)
            happiness_new = get_room_happiness(new_room)
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
                r1.remove(n1)
                D[n1] = len(room_to_student)
                room_to_student[D[n1]] = [n1]

        def maybe_swap(n1, n2, T):
            curr_hap = get_happiness()
            swap_hap = swap_happiness(n1, n2)
            delta = curr_hap - swap_hap
            # print(n1, n2, swap_hap, curr_hap, r, p)
            r = random.random()
            if delta < 0:
                swap(n1, n2)
            elif swap_hap > 0 and r < math.exp(-delta/T):
                swap(n1, n2)


        def maybe_add(n1, T):
            room = random.randrange(len(room_to_student))
            curr_hap = get_room_happiness(room_to_student[room])
            curr_hap += get_room_happiness(room_to_student[D[n1]])
            add_hap= add_happiness(n1, room)
            delta = curr_hap - add_hap
            # print(n1, n2, swap_hap, curr_hap, r, p)
            r = random.random()
            if delta < 0:
                add_student(n1, room)
            elif add_hap > 0 and r < math.exp(-delta/T**2):
                add_student(n1, room)

        print('---Original Stress: ', s, ' Original Happiness: ', old_happiness, 'Orig. Rooms: ', old_rooms)

        # original_s = s
        # s = 1.5 * s
        loops = 100

        for countdown in range(loops*5, loops*4, -1):
            # if s > original_s:
            #     s -= (loops - countdown + 1)**2 * s / loops
            # if s < original_s:
            #     s = original_s
            curr, curr_rooms = get_happiness(), len(room_to_student)
            print(curr, 'Stress: ', s, 'Rooms: ', curr_rooms, countdown)
            # if curr > new_high and is_valid_solution(D, G, s, curr):                    
            #     new_high, best_D, best_k = curr, D.copy(), curr_rooms
            # else:
            #     print(curr, 'Stress: ', s, 'Rooms: ', curr_rooms, countdown)
            #     break

            for _ in range(students * 4 ):
                curr, curr_rooms = get_happiness(), len(room_to_student)
                print(curr, 'Stress: ', s, 'Rooms: ', curr_rooms, countdown)
                n1, n2 = floor(random.randrange(students)), floor(random.randrange(students))
                # ADD CASE
                if random.random() < countdown / (loops) and countdown > loops:
                    maybe_add(n1, countdown)
                # REMOVE CASE
                if random.random() < countdown / (loops*1000) and curr < -50:
                    remove(n1)
                # SWAP CASE
                if D[n1] != D[n2]:
                    maybe_swap(n1, n2, countdown)

        # if best_D and is_valid_solution(best_D, G, s, best_k):
        #     return best_D, best_k
        return D, len(room_to_student)

    output, rooms = get_D()
    new_happiness = calculate_happiness(output, G)
    validity = is_valid_solution(output, G,s, rooms)
    if new_happiness > old_happiness and validity: 
        print("Nice! Original: ", old_happiness, "New: ", new_happiness, validity)
        return output, rooms
    else:
        print("sadness :( Original: ", old_happiness, "New: ", new_happiness, validity)
        print('Original Stress: ', s, ' Original Happiness: ', old_happiness, 'Orig. Rooms: ', old_rooms)
        print()
        return None



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    output_path = 'outputs/' + basename(normpath(path))[:-3] + '.out'
    G, s = read_input_file(path)
    print('Solving: ' + path)
    sol = solve(G, s, output_path)
    if sol:
        D, k = sol
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)), k)
        write_output_file(D, output_path)


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     # inputs = inputs[::-1]
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         # if not os.path.exists(output_path):
#         G, s = read_input_file(input_path, 100)
#         print("Solving: ", input_path)
#         sol = solve(G, s, output_path)
#         if sol:
#             D, k = sol
#             assert is_valid_solution(D, G, s, k)
#             cost_t = calculate_happiness(D, G)
#             write_output_file(D, output_path)
