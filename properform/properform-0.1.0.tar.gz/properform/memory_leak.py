#-*- coding: utf-8 -*-
# Copyright 2020 ibelie, Chen Jie, Joungtao. All rights reserved.
# Use of this source code is governed by The MIT License
# that can be found in the LICENSE file.

try:
	import tracemalloc
except:
	tracemalloc = None

import json

def start():
	tracemalloc and tracemalloc.start(1)

def collect(filename = None):
	import gc
	gc.set_debug(gc.DEBUG_LEAK)
	gc.collect()

	memleak = {}
	ids = {id(o) for o in gc.garbage}
	for o in gc.garbage:
		try:
			desc = repr(o)
		except:
			desc = "<object of %s at 0x%X, exception in __repr__()>" % (type(o), id(o))
		trace = tracemalloc and tracemalloc.get_object_traceback(o)
		frame = trace and trace[0]
		memleak[id(o)] = (str(type(o)), desc, frame and frame.filename or '', frame and frame.lineno or 0, tuple(id(r) for r in gc.get_referents(o) if id(r) in ids))

	if filename is None:
		return memleak

	with open(filename, 'w') as f:
		json.dump(collect(), f)

class Vertex(object):
	__slots__=['index', 'edges', 'visited', 'prev', 'next', 'parent']

def _list_reference_cycles_dfs_proc(vertex, on_cycle_found):
	vertex.visited = -1
	vertex.prev.next = vertex.next
	if vertex.next:
		vertex.next.prev = vertex.prev
	for next_vertex in vertex.edges:
		if next_vertex.visited == 0:
			next_vertex.parent = vertex
			_list_reference_cycles_dfs_proc(next_vertex, on_cycle_found)
		elif next_vertex.visited == -1: # found a cycle
			on_cycle_found(next_vertex, vertex)
	vertex.visited = 1

def list_reference_cycles(memleak, filename, mode = 'w'):
	# this is a graph DFS based algorithm
	vertices_list_head = Vertex() # dummy head of linked list
	vertices_list_head.next = None
	oid2vertex = {}

	# make vertices
	for i in memleak:
		vertex = Vertex()
		vertex.index = i
		vertex.visited = 0
		vertex.prev = vertices_list_head
		vertex.next = vertices_list_head.next
		if vertices_list_head.next:
			vertices_list_head.next.prev = vertex
		vertices_list_head.next = vertex
		oid2vertex[i] = vertex

	# make edges
	vertex = vertices_list_head.next
	while vertex is not None:
		vertex.edges = [oid2vertex[r] for r in memleak[vertex.index][4]]
		vertex = vertex.next

	output_file = [None]
	def on_cycle_found(vertex1, vertex2):
		"there is a path from vertex1 to vertex2, and an edge from vertex2 to vertex1"
		if output_file[0] is None:
			output_file[0] = open(filename, mode)

		output_file[0].write('---------------- a cycle is found ----------------\n')
		path = []
		v = vertex2
		while v is not vertex1:
			path = [v] + path
			v = v.parent
		path = [vertex1] + path
		for v in path:
			t, v, f, n, rs = memleak[v.index]
			output_file[0].write('%s: %s\n' %(t, v))
			output_file[0].write('%s: %s\n\n' %(f, n))
		output_file[0].write('\n')

	# DFS visit all vertices
	while vertices_list_head.next is not None:
		vertex = vertices_list_head.next
		vertex.parent = None
		_list_reference_cycles_dfs_proc(vertex, on_cycle_found)

	if output_file[0]:
		output_file[0].close()

	# clean up to remove reference cycles between Vertex objects
	for vertex in oid2vertex.values():
		vertex.edges = None
		vertex.prev = None
		vertex.next = None
		vertex.parent = None
