import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys, glob
from os.path import basename, normpath
import os.path


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    def get_mapping(size, mapping, i=0):
        if i == len(G.nodes):
            return mapping
        max_map, max_happiness = None, 0
        for room in range(size):
            new_map = mapping.copy()
            new_map[i] = room
            ret_map = get_mapping(size, new_map, i + 1)
            # print(ret_map, i, room)
            if ret_map != None and is_valid_solution(ret_map, G, s, size) and calculate_happiness(ret_map, G) > max_happiness:
            # if calculate_happiness(ret_map, G) > max_happiness:
                max_map = ret_map
                max_happiness = calculate_happiness(ret_map, G)
        return max_map
            
    for size in range(4, 6):
        result = get_mapping(size, dict())
        if result:
            return result, size
    # print('No result found!')
    return None
    # return result, 2


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
    inputs = glob.glob('smalls/*')
    inputs = inputs[::-1]
    for input_path in inputs:
        output_path = 'smalls_outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        ret = solve(G, s)
        if ret:
            D, k = ret
            assert is_valid_solution(D, G, s, k)
            cost_t = calculate_happiness(D, G)
            print(output_path, cost_t)
            write_output_file(D, output_path)
        else:
            print(output_path, 'No Result Found!')

