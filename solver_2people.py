import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys
import glob
from os.path import basename, normpath


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    room_to_student = {}
    student_to_room = {}

    # Put people into their own breakout room
    for node in list(G.nodes):
        room_to_student[node] = [node]
        student_to_room[node] = node

    is_changed = 1
    while is_changed:
        is_changed = 0
        max_happiness = calculate_happiness(student_to_room, G)
        best_student = 0
        best_move = 0

        for student in list(G.nodes):
            curr_room = student_to_room[student]
            num_rooms = len(room_to_student)
            if len(room_to_student[student_to_room[student]]) == 1:
                num_rooms -= 1

            for new_room in room_to_student.keys():
                room_to_student[curr_room].remove(student)
                room_to_student[new_room].append(student)
                student_to_room[student] = new_room
                curr_happiness = calculate_happiness(student_to_room, G)

                new_room_stress = calculate_stress_for_room(room_to_student[new_room], G)
                stress_budget_room = s / num_rooms
                if new_room_stress > stress_budget_room:
                    curr_happiness = 0

                if curr_happiness > max_happiness:
                    max_happiness = curr_happiness
                    is_changed = 1
                    best_move = new_room
                    best_student = student

                room_to_student[new_room].remove(student)
                room_to_student[curr_room].append(student)
                student_to_room[student] = curr_room
            

        # Remove best student from current breakout room
        # Add best student to best breakout room
        # Change best student's breakout room to best breakout room

        if is_changed:
            room_to_student[student_to_room[best_student]].remove(best_student)
            room_to_student[best_move].append(best_student)
            student_to_room[best_student] = best_move

        rooms = list(room_to_student.keys())
        for r in rooms:
            if len(room_to_student[r]) == 0:
                room_to_student.pop(r)
    
    print("Currently at swap")
    #Check for swaps
    is_changed = 1
    while is_changed:
        is_changed = 0
        max_happiness = calculate_happiness(student_to_room, G)
        best_student = 0
        best_student2 = 0
        

        for student in list(G.nodes):
            num_rooms = len(room_to_student)
            for student2 in list(G.nodes):
                if student != student2:
                    student_old_room = student_to_room[student]
                    student2_old_room = student_to_room[student2]
                    
                    room_to_student[student2_old_room].append(student)
                    #Remove student from student room
                    student_to_room[student] = student2_old_room
                    #Put student2 in student room
                    room_to_student[student_old_room].append(student2)
                    #Remove student2 from student2 room
                    student_to_room[student2] = student_old_room

                    # Make sure students are not in same breakout room
                    student_room_stress = calculate_stress_for_room(room_to_student[student2_old_room], G)
                    student2_room_stress = calculate_stress_for_room(room_to_student[student_old_room], G)

                    stress_budget_room = s / num_rooms
                    if student_room_stress < stress_budget_room or student2_room_stress < stress_budget_room:
                        #Put student in student room
                        room_to_student[student_old_room].append(student)
                        #Remove student from student2 room
                        student_to_room[student] = student_old_room
                        #Put student2 in student room
                        room_to_student[student2_old_room].append(student2)
                        #Remove student2 from student2 room
                        student_to_room[student2] = student2_old_room    

                    else:
                        curr_happiness = calculate_happiness(student_to_room, G)
                        if curr_happiness > max_happiness:
                            max_happiness = curr_happiness
                            is_changed = 1
                            best_student = student
                            best_student2 = student2
                        #Put student in student room
                        room_to_student[student_old_room].append(student)
                        #Remove student from student2 room
                        student_to_room[student] = student_old_room
                        #Put student2 in student room
                        room_to_student[student2_old_room].append(student2)
                        student_to_room[student2] = student2_old_room   
        

        if is_changed:
            student_old_room = student_to_room[best_student]
            student2_old_room = student_to_room[best_student2]
            room_to_student[student2_old_room].append(best_student)
            student_to_room[best_student] = student2_old_room
            room_to_student[student_old_room].append(best_student2)
            student_to_room[best_student2] = student_old_room
    
    index = 0
    output = {}
    for r in room_to_student.keys():
        output[index] = room_to_student[r]
        index += 1

    return convert_dictionary(output), len(output)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        cost_t = calculate_happiness(D, G)
        write_output_file(D, output_path)
