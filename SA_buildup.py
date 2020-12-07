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
    moves_size_mid = {10:75, 20:400, 50:2500}
    moves_size_end = {10:50, 20:200, 50:1500}
    final_temp = 0
    curr_happiness = 0

    def get_happiness():
    if not is_valid_solution(student_to_room, G, s, len(room_to_student)):
        return -100
    else:
        return calculate_happiness(student_to_room, G)

    def check_swap_student(student1, student2):
        student1_oldrooom = student_to_room[student1]
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
        student1_oldroom = student_to_room[student1]
        room_to_student[student1_oldroom].remove(student1)
        room_to_student[new_room].append(new_room)
        student_to_room[student1] = new_room
        
        if len(room_to_student[student1_oldroom]) == 0:
            room_to_student.remove(student1_oldroom)
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

        room_to_student.remove(len(room_to_student) - 1)
        room_to_student[student1_oldroom].append(student1)
        student_to_room[student1] = student1_oldroom

        return happiness

    def swap_student(student1, student2):
        student1_oldrooom = student_to_room[student1]
        student2_oldroom = student_to_room[student2]

        room_to_student[student1_oldroom].remove(student1)
        room_to_student[student2_oldroom].remove(student2)
        room_to_student[student2_oldroom].append(student1)
        room_to_student[student1_oldroom].append(student2)
        student_to_room[student1] = student2_oldroom
        student_to_room[student2] = student1_oldroom

    def add_student(student1, new_room):
        student1_oldroom = student_to_room[student1]
        room_to_student[student1_oldroom].remove(student1)
        room_to_student[new_room].append(new_room)
        student_to_room[student1] = new_room

        if len(room_to_student[student1_oldroom]) == 0:
            room_to_student.remove(student1_oldroom)
        
    def remove_student(student1):
        student1_oldroom = student_to_room[student1]
        if len(room_to_student[student1_oldroom]) == 1:
            return get_happiness()

        room_to_student[student1_oldroom].remove(student1)
        room_to_student.append([student1])
        student_to_room[student1] = len(room_to_student) - 1
    
    # 80% add, 20% swap -> 1500
    curr_temp = moves_size_start[len(student_to_room)]
    alpha = 1
    while curr_temp > final_temp:
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room))
        student2 = random.randint(0, len(student_to_room))
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room))
        room = random.randint(0, len(room_to_student))
        if choice < 0.8:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_swap_student(student1, student2)
        
        if new_happiness > curr_happiness:
            if choice < 0.8:
                add_student(student1, room)
            else:
                swap_student(student1, room)
            curr_happiness = new_happiness

        elif random.uniform(0, 1) < math.exp((new_happiness - curr_happiness) / (curr_temp * curr_happiness)) and new_happiness != -100:
            if choice < 0.8:
                add_student(student1, room)
            else:
                swap_student(student1, room)
            curr_happiness = new_happiness
        
        curr_temp = curr_temp - alpha

    # 50% swap, 30% add, 20% remove -> 2500
    alpha = 1
    curr_temp = moves_size_mid[len(student_to_room)]
    while curr_temp > final_temp:
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room))
        student2 = random.randint(0, len(student_to_room))
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room))
        room = random.randint(0, len(room_to_student))
        if choice < 0.5:
            new_happiness = check_swap_student(student1, student2)
        elif choice >= 0.5 and choice < 0.8:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_remove_student(student1)
        
        if new_happiness > curr_happiness:
            if choice < 0.5:
                swap_student(student1, student2)
            elif choice >= 0.5 and choice < 0.8:
                add_student(student, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness

        elif random.uniform(0, 1) < math.exp((new_happiness - curr_happiness) / (curr_temp * curr_happiness)) and new_happiness != -100:
            if choice < 0.5:
                swap_student(student1, student2)
            elif choice >= 0.5 and choice < 0.8:
                add_student(student, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness
        
        curr_temp = curr_temp - alpha

    # 80% swap, 10% add, 10% remove -> 1500
    start_temp = moves_size_end[len(student_to_room)]
    alpha = 1
    curr_temp = start_temp
    while curr_temp > final_temp:
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room))
        student2 = random.randint(0, len(student_to_room))
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room))
        room = random.randint(0, len(room_to_student))
        if choice < 0.8:
            new_happiness = check_swap_student(student1, student2)
        elif choice >= 0.8 and choice < 0.9:
            new_happiness = check_add_student(student1, room)
        else:
            new_happiness = check_remove_student(student1)

        if new_happiness > curr_happiness:
            if choice < 0.8:
                swap_student(student1, student2)
            elif choice >= 0.8 and choice < 0.9:
                add_student(student1, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness

        elif random.uniform(0, 1) < math.exp((new_happiness - curr_happiness) / (curr_temp * curr_happiness)) and new_happiness != -100:
            if choice < 0.8:
                swap_student(student1, student2)
            elif choice >= 0.8 and choice < 0.9:
                add_student(student1, room)
            else:
                remove_student(student1)
            curr_happiness = new_happiness

        curr_temp = curr_temp - alpha
    
    return student_to_room, len(room_to_student)




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
    inputs = glob.glob('larges/*')
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
