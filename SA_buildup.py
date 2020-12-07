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


    room_to_student = []
    student_to_room = {}

    # Put people into their own breakout room
    print(list(G.nodes))
    for node in list(G.nodes):
        room_to_student.append([node])
        student_to_room[node] = node
    
    moves_size_start = {10:50, 20:200, 50:1500}
    moves_size_mid = {10:75, 20:200, 50:2500}
    moves_size_end = {10:50, 20:100, 50:1500}
    final_temp = 0
    curr_happiness = 1

    def get_happiness():
        if not is_valid_solution(student_to_room, G, s, len(room_to_student)):
            return -200
        else:
            return calculate_happiness(student_to_room, G)

    def check_swap_student(student1, student2):
        if student_to_room[student1] == student_to_room[student2]:
            return -200
        student1_oldroom = student_to_room[student1]
        student2_oldroom = student_to_room[student2]

        room_to_student[student1_oldroom].remove(student1)
        room_to_student[student2_oldroom].remove(student2)
        room_to_student[student2_oldroom].append(student1)
        room_to_student[student1_oldroom].append(student2)
        student_to_room[student1] = student2_oldroom
        student_to_room[student2] = student1_oldroom

        happiness = get_happiness()

        room_to_student[student1_oldroom].remove(student2)
        room_to_student[student2_oldroom].remove(student1)
        room_to_student[student2_oldroom].append(student2)
        room_to_student[student1_oldroom].append(student1)
        student_to_room[student2] = student2_oldroom
        student_to_room[student1] = student1_oldroom
        return happiness

    def check_add_student(student1, new_room):
        removed = False
        if student_to_room[student1] == new_room:
            return -200
        student1_oldroom = student_to_room[student1]
        room_to_student[student1_oldroom].remove(student1)
        room_to_student[new_room].append(student1)
        student_to_room[student1] = new_room
        
        if len(room_to_student[student1_oldroom]) == 0:
            del(room_to_student[student1_oldroom])
            for i in range(student1_oldroom, len(room_to_student)):
                student_list = room_to_student[i]
                for student in student_list:
                    student_to_room[student] = i
            if new_room > student1_oldroom:
                new_room = new_room - 1
            removed = True

        happiness = get_happiness()

        if removed:
            room_to_student.append([student1])
            student_to_room[student1] = len(room_to_student) - 1
            room_to_student[new_room].remove(student1)
        else:
            room_to_student[new_room].remove(student1)
            room_to_student[student1_oldroom].append(student1)
            student_to_room[student1] = student1_oldroom
        return happiness

    def check_remove_student(student1):
        student1_oldroom = student_to_room[student1]
        if len(room_to_student[student1_oldroom]) == 1:
            return get_happiness()

        room_to_student[student1_oldroom].remove(student1)
        room_to_student.append([student1])
        student_to_room[student1] = len(room_to_student) - 1

        happiness = get_happiness()

        del(room_to_student[len(room_to_student) - 1])
        room_to_student[student1_oldroom].append(student1)
        student_to_room[student1] = student1_oldroom

        return happiness

    def swap_student(student1, student2):
        student1_oldroom = student_to_room[student1]
        student2_oldroom = student_to_room[student2]

        room_to_student[student1_oldroom].remove(student1)
        room_to_student[student2_oldroom].remove(student2)
        room_to_student[student2_oldroom].append(student1)
        room_to_student[student1_oldroom].append(student2)
        student_to_room[student1] = student2_oldroom
        student_to_room[student2] = student1_oldroom
        print("swapped")
    def add_student(student1, new_room):
        student1_oldroom = student_to_room[student1]
        room_to_student[student1_oldroom].remove(student1)
        room_to_student[new_room].append(student1)
        student_to_room[student1] = new_room

        if len(room_to_student[student1_oldroom]) == 0:
            del(room_to_student[student1_oldroom])
            for i in range(student1_oldroom, len(room_to_student)):
                student_list = room_to_student[i]
                for student in student_list:
                    student_to_room[student] = i
            if new_room > student1_oldroom:
                new_room = new_room - 1
        print(str(student1) + "was add3d t0" + str(new_room))

    def remove_student(student1):
        student1_oldroom = student_to_room[student1]
        if len(room_to_student[student1_oldroom]) == 1:
            return get_happiness()

        room_to_student[student1_oldroom].remove(student1)
        room_to_student.append([student1])
        student_to_room[student1] = len(room_to_student) - 1
        print("removed")
    # 95% add, 5% swap -> 1500
    curr_temp = moves_size_start[len(student_to_room)]
    alpha = 0.01
    while curr_temp > final_temp:
        chance_add = 0.95
        chance_swap = 0.05
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        if choice < chance_add:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_swap_student(student1, student2)

        ratio = (new_happiness - curr_happiness) / (curr_happiness + 1)
        if new_happiness > curr_happiness:
            if choice < chance_add:
                add_student(student1, room)
            else:
                swap_student(student1, student2)
            curr_happiness = new_happiness

        elif random.uniform(0, 3) < math.exp((new_happiness - curr_happiness)/curr_temp) and new_happiness != -100:
            if choice < chance_add:
                add_student(student1, room)
            else:
                swap_student(student1, student2)
            curr_happiness = new_happiness
        curr_temp = curr_temp - alpha




    # 39% swap, 60% add, 1% remove -> 2500
    curr_temp = moves_size_mid[len(student_to_room)]
    while curr_temp > final_temp:
        chance_add = 0.6
        chance_swap = 0.3
        chance_remove = 0.1
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        if choice < chance_swap:
            new_happiness = check_swap_student(student1, student2)
        elif choice >= chance_swap and choice < chance_swap + chance_add:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_remove_student(student1)
        
        ratio = (new_happiness - curr_happiness) / (curr_happiness + 1)
        if new_happiness > curr_happiness:
            if choice < chance_swap:
                swap_student(student1, student2)
            elif choice >= chance_swap and choice < chance_swap + chance_add:
                add_student(student1, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness

        elif random.uniform(0, 3) < math.exp((new_happiness - curr_happiness)/curr_temp) and new_happiness != -200:
            if choice < chance_swap:
                swap_student(student1, student2)
            elif choice >= chance_swap and choice < chance_swap + chance_add:
                add_student(student1, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness
        curr_temp = curr_temp - alpha

    # 70% swap, 29% add, 1% remove -> 1500
    start_temp = moves_size_end[len(student_to_room)]
    curr_temp = start_temp
    max_happiness = 0
    while curr_temp > final_temp:
        chance_swap = 0.4
        chance_add = 0.4
        chance_remove = 0.2
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        if choice < chance_swap:
            new_happiness = check_swap_student(student1, student2)
        elif choice >= chance_swap and choice < chance_swap + chance_add:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_remove_student(student1)
        
        
        if curr_temp == 10:
            max_happiness = curr_happiness
            best_student = student_to_room.copy()
            best_rooms = len(room_to_student)
        if curr_temp < 10:
            if new_happiness > max_happiness:
                if choice < chance_swap:
                    swap_student(student1, student2)
                elif choice >= chance_swap and choice < chance_add + chance_swap:
                    add_student(student1, room)
                else:
                    remove_student(student1)
                curr_happiness = new_happiness
                max_happiness = new_happiness
                best_student = student_to_room.copy()
                best_rooms = len(room_to_student)
        else: 
            if new_happiness > curr_happiness:
                if choice < chance_swap:
                    swap_student(student1, student2)
                elif choice >= chance_swap and choice < chance_add + chance_swap:
                    add_student(student1, room)
                else:
                    remove_student(student1)
                curr_happiness = new_happiness

            elif random.uniform(0, 1) < math.exp((new_happiness - curr_happiness)/curr_temp) and new_happiness != -100:
                if choice < chance_swap:
                    swap_student(student1, student2)
                elif choice >= chance_swap and choice < chance_swap + chance_add:
                    add_student(student1, room)
                else:
                    remove_student(student1)
                curr_happiness = new_happiness
        curr_temp = curr_temp - alpha
    
    return best_student, best_rooms




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
