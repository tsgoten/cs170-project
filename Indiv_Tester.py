import networkx as nx
from parse import read_input_file, read_output_file, write_output_file
from utils import *
import sys
import glob, random
from os.path import basename, normpath
import os.path
import math
from math import floor

path = sys.argv[1]
G, s = read_input_file(path)

def test(G, s):
	student_to_room = {}
	for node in list(G.nodes):
		student_to_room[node] = node
	room_to_student = [[47, 12], [24, 34, 4], [3, 23, 32, 39, 41], [48, 36], [15, 45, 26], [38], [33, 9, 18, 43], [40, 16], [29, 14], [22, 28], [30, 25], [31, 0, 42, 13], [46, 35], [5, 49], [20], [21, 7], [19], [27], [1], [37], [10], [17], [44], [6, 2], [8], [11]]
	for node in list(G.nodes):
		student_to_room[node] = node
	for k in range(0, len(room_to_student)):
		student_list = room_to_student[k]
		for i in student_list:
			student_to_room[i] = k
	print(is_valid_solution(student_to_room, G, s, len(room_to_student)))
test(G, s)
