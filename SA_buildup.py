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
    
    moves_size_start = {10:50, 20:2000, 50:5000}
    moves_size_mid = {10:75, 20:1000, 50:2500}
    moves_size_end = {10:50, 20:1000, 50:1500}
    final_temp = 0
    curr_happiness = 1

    def get_happiness():
        if not is_valid_solution(student_to_room, G, s, len(room_to_student)):
            return -200
        else:
            return calculate_happiness(student_to_room, G)

    def check_swap_student(student1, student2):
        if student_to_room[student1] == student_to_room[student2]:
            return -200, 0
        student1_oldroom = student_to_room[student1]
        student2_oldroom = student_to_room[student2]
        old_stress_student = calculate_stress_for_room(room_to_student[student1_oldroom], G) + calculate_stress_for_room(room_to_student[student2_oldroom], G)
        room_to_student[student1_oldroom].remove(student1)
        room_to_student[student2_oldroom].remove(student2)
        room_to_student[student2_oldroom].append(student1)
        room_to_student[student1_oldroom].append(student2)
        student_to_room[student1] = student2_oldroom
        student_to_room[student2] = student1_oldroom
        new_stress_student = old_stress_student = calculate_stress_for_room(room_to_student[student1_oldroom], G) + calculate_stress_for_room(room_to_student[student2_oldroom], G)
        happiness = get_happiness()
        stress_diff = old_stress_student - new_stress_student

        room_to_student[student1_oldroom].remove(student2)
        room_to_student[student2_oldroom].remove(student1)
        room_to_student[student2_oldroom].append(student2)
        room_to_student[student1_oldroom].append(student1)
        student_to_room[student2] = student2_oldroom
        student_to_room[student1] = student1_oldroom
        return happiness, stress_diff

    def check_add_student(student1, new_room):
        removed = False
        oldroom_needed = False
        if student_to_room[student1] == new_room:
            return -200, 0
        student1_oldroom = student_to_room[student1]
        old_stress = 0
        if(len(room_to_student[student1_oldroom]) > 1):
            old_stress += calculate_stress_for_room(room_to_student[student1_oldroom], G)
            oldroom_needed = True
        old_stress += calculate_stress_for_room(room_to_student[new_room], G)
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
        if oldroom_needed:
            new_stress_original = calculate_stress_for_room(room_to_student[student1_oldroom], G)
            new_stress_new = calculate_stress_for_room(room_to_student[new_room], G)
            new_stress = new_stress_original + new_stress_new
        else:
            new_stress = calculate_stress_for_room(room_to_student[new_room], G)
        stress_diff = old_stress - new_stress
        happiness = get_happiness()

        if removed:
            room_to_student.append([student1])
            student_to_room[student1] = len(room_to_student) - 1
            room_to_student[new_room].remove(student1)
        else:
            room_to_student[new_room].remove(student1)
            room_to_student[student1_oldroom].append(student1)
            student_to_room[student1] = student1_oldroom
        return happiness, stress_diff

    def check_remove_student(student1):
        student1_oldroom = student_to_room[student1]
        if len(room_to_student[student1_oldroom]) == 1:
            return -200, 0
        old_stress = calculate_stress_for_room(room_to_student[student1_oldroom], G)
        room_to_student[student1_oldroom].remove(student1)
        room_to_student.append([student1])
        student_to_room[student1] = len(room_to_student) - 1
        new_stress = calculate_stress_for_room(room_to_student[student1_oldroom], G)
        happiness = get_happiness()
        stress_diff = old_stress - new_stress
        del(room_to_student[len(room_to_student) - 1])
        room_to_student[student1_oldroom].append(student1)
        student_to_room[student1] = student1_oldroom

        return happiness, stress_diff

    def check_combine_room(room1, room2):
        old_stress = calculate_stress_for_room(room_to_student[room1], G)
        old_stress +=  calculate_stress_for_room(room_to_student[room2], G)

        room1_studentlist = room_to_student[room1]
        room2_studentlist = room_to_student[room2]
        room1_studentlist.extend(room2_studentlist)
        room_to_student[room1] = room1_studentlist
        del(room_to_student[room2])
        for i in room2_studentlist:
            student_to_room[i] = room1
        for i in range(room2, len(room_to_student)):
                student_list = room_to_student[i]
                for student in student_list:
                    student_to_room[student] = i
        
        if room1 > room2:
            room1 = room1 - 1
        
        new_stress = calculate_stress_for_room(room_to_student[room1], G)
        happiness = get_happiness()
        stress_diff = old_stress - new_stress
    
        for i in room2_studentlist:
            room_to_student[room1].remove(i)
        room_to_student.append(room2_studentlist)
        for i in room2_studentlist:
            student_to_room[i] = len(room_to_student) - 1
        return happiness, stress_diff
        
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
        print(str(room_to_student))
        print(is_valid_solution(student_to_room, G, s, len(room_to_student)))

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
        print("added")
        print(str(room_to_student))
        print(is_valid_solution(student_to_room, G, s, len(room_to_student)))

    def remove_student(student1):
        student1_oldroom = student_to_room[student1]
        if len(room_to_student[student1_oldroom]) == 1:
            return get_happiness()

        room_to_student[student1_oldroom].remove(student1)
        room_to_student.append([student1])
        student_to_room[student1] = len(room_to_student) - 1
        print("removed")
        print(str(room_to_student))
        print(is_valid_solution(student_to_room, G, s, len(room_to_student)))
    
    def combine_room(room1, room2):
        room1_studentlist = room_to_student[room1]
        room2_studentlist = room_to_student[room2]
        room1_studentlist.extend(room2_studentlist)
        room_to_student[room1] = room1_studentlist
        del(room_to_student[room2])
        for i in room2_studentlist:
            student_to_room[i] = room1
        for i in range(room2, len(room_to_student)):
                student_list = room_to_student[i]
                for student in student_list:
                    student_to_room[student] = i
        
        if room1 > room2:
            room1 = room1 - 1
        print("combined")
    
    # 95% add, 5% swap -> 1500
    curr_temp = moves_size_start[len(student_to_room)]
    alpha = 0.01
    curr_stress = 0
    stress_diff = 0
    best_rooms = 0
    best_state = {} 
    best_happiness = 0
    while curr_temp > final_temp:
        chance_add = 0.6
        chance_combine = 0.3
        chance_swap = 0.09
        chance_remove = 0.01
        
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        room2 = random.randint(0, len(room_to_student) - 1)
        while room == room2:
            room2 = random.randint(0, len(room_to_student) - 1)

        if choice < chance_add:
            new_happiness, stress_diff = check_add_student(student1, room)
        elif choice >= chance_add and choice < chance_add + chance_combine:
            new_happiness, stress_diff = check_combine_room(room, room2)
        elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
            new_happiness, stress_diff = check_swap_student(student1, student2)
        else:
            new_happiness, stress_diff = check_remove_student(student1)
            

        if new_happiness > curr_happiness and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)

            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)

        elif random.uniform(0, 1) < math.exp((10 * (new_happiness - curr_happiness) + stress_diff)/curr_temp) and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)
            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)
        curr_temp = curr_temp - alpha


    # 39% swap, 60% add, 1% remove -> 2500
    curr_temp = moves_size_mid[len(student_to_room)]
    while curr_temp > final_temp:
        chance_add = 0.5
        chance_combine = 0.2
        chance_swap = 0.2
        chance_remove = 0.1
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        room2 = random.randint(0, len(room_to_student) - 1)
        while room == room2:
            room2 = random.randint(0, len(room_to_student) - 1)

        if choice < chance_add:
            new_happiness, stress_diff = check_add_student(student1, room)
        elif choice >= chance_add and choice < chance_add + chance_combine:
            new_happiness, stress_diff = check_combine_room(room, room2)
        elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
            new_happiness, stress_diff = check_swap_student(student1, student2)
        else:
            new_happiness, stress_diff = check_remove_student(student1)
            

        if new_happiness > curr_happiness and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)

            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)

        elif random.uniform(0, 1) < math.exp((10 * (new_happiness - curr_happiness) + stress_diff)/curr_temp) and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)
            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)
        curr_temp = curr_temp - alpha

    # 70% swap, 29% add, 1% remove -> 1500
    start_temp = moves_size_end[len(student_to_room)]
    curr_temp = start_temp
    while curr_temp > final_temp:
        chance_swap = 0.3
        chance_add = 0.5
        chance_combine = 0.1
        chance_remove = 0.1
        choice = random.uniform(0, 1)
        student1 = random.randint(0, len(student_to_room) - 1)
        student2 = random.randint(0, len(student_to_room) - 1)
        while student1 == student2:
            student2 = random.randint(0, len(student_to_room) - 1)
        room = random.randint(0, len(room_to_student) - 1)
        room2 = random.randint(0, len(room_to_student) - 1)
        while room == room2:
            room2 = random.randint(0, len(room_to_student) - 1)

        if choice < chance_add:
            new_happiness, stress_diff = check_add_student(student1, room)
        elif choice >= chance_add and choice < chance_add + chance_combine:
            new_happiness, stress_diff = check_combine_room(room, room2)
        elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
            new_happiness, stress_diff = check_swap_student(student1, student2)
        else:
            new_happiness, stress_diff = check_remove_student(student1)
            

        if new_happiness > curr_happiness and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)

            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)

        elif random.uniform(0, 1) < math.exp((10 * (new_happiness - curr_happiness) + stress_diff)/curr_temp) and new_happiness != -200:
            if choice < chance_add:
                add_student(student1, room)
            elif choice >= chance_add and choice < chance_add + chance_combine:
                combine_room(room, room2)
            elif choice >= chance_add + chance_combine and choice < 1 - chance_remove:
                swap_student(student1, student2)
            else:
                remove_student(student1)
            curr_happiness = new_happiness
            if curr_happiness > best_happiness and is_valid_solution(student_to_room, G, s, len(room_to_student)):
                best_state = student_to_room.copy()
                best_rooms = len(room_to_student)
                best_happiness = curr_happiness
            print(curr_happiness)
        curr_temp = curr_temp - alpha
    
    # return student_to_room, len(room_to_student)
    return best_state, best_rooms




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
