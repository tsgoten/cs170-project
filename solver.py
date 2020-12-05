import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys


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

    # Create a new graph to build up on
    # new_graph = nx.Graph()
    # new_graph.add_nodes_from(list(G.nodes))

    is_changed = 1
    while is_changed:
        is_changed = 0
        # which student gives us best happiness
        max_happiness = calculate_happiness(student_to_room, G)
        best_student = 0
        best_move = 0

        # Iterate through every vertex to see if it is more optimal to be in another breakout room
        for student in list(G.nodes):
            curr_room = student_to_room[student]
            # Iterate through every breakout room to see whether the student fits in this room
            for new_room in room_to_student.keys():
                # Remove breakout room if nobody is inside it
                if len(room_to_student[new_room]) == 0:
                    room_to_student.pop(new_room)
                    break

                # Remove student from old breakout room
                room_to_student[curr_room].remove(student)
                # Add student to new breakout room
                room_to_student[new_room].append(student)
                # Change student's breakout room to new breakout room
                student_to_room[student] = new_room
                curr_happiness = calculate_happiness(student_to_room, G)

                new_room_stress = calculate_stress_for_room(room_to_student[new_room], G)
                stress_budget_room = s / len(room_to_student)
                print('Room stress: ', new_room_stress, '\t\t\tRoom Budget: ', stress_budget_room, 'Num of rooms: ', len(room_to_student))
                if new_room_stress > stress_budget_room:
                    print('Room stress: ', new_room_stress, '\t\t\tRoom Budget: ', stress_budget_room, 'Num of rooms: ', len(room_to_student))
                    break

                if curr_happiness > max_happiness:
                    print(student, new_room)
                    max_happiness = curr_happiness
                    is_changed = 1
                    best_move = new_room
                    best_student = student

                # Remove student from new breakout room
                # Add student to old breakout room
                # Change student's breakout room to old breakout room
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

    return student_to_room, len(student_to_room)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
