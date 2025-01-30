# ASSIGNMENT 5: FINDING MAX CAPACITY PATH FROM SOURCE NODE TO TARGET NODE
# INPUT FORMAT:
"""
n: nuber of routers in the network
links: a list of 3-tuples of integers of he form (u, v, c), where c is the capacity of the edge 
s: source router
t: target router
"""
# AIM: To find the path with the maximum capacity from the source node t the target node 

"""
DATA STRUCTURES USED:

1. ADJACENCY LIST REPRESENTATION OF GRAPHS:
    will create a class 'Vertex' with the following attributes:
        - index: refers to the vertexindex (an integer)
        - capacity: refers to the max capacity path from source node to this node
        - prev: refers to the node before this in the max capacity path from source node
        - adjlist: the adjacency list corresponding to this vertex - this list contains 
            tuples with 2 values each representing the node and the corresponding capacity of the edge

2. MAX HEAP:
    this is needed to create a priority queue of node capacities 
"""
#TARGET TIME COMPLEXITY: O(mlogm) where m is the number of edges in the graph ad 'n' is the number of vertices

"""
ALGORITHM DESCRIPTION:
1. all the neighbours of the source node are added to max heap
2. we initialise the capacities of al the neighbour nodes and make a heap
3. then, the max is popped from the max heap, and its neighbours are iterated through and capacities updated 
4. If these nodes are not already present in the max heap, then they are added 
4. UPDATING CAPACITY:
    - if the edge capacity from current node to neighbour is smaller than current node capacity, store that in a variable
    - if this variable is greater than the capacity of the neighbour node, update capacity and prev 
6. Finally, when the popped max corresponds to the target node, break ot of the loop and return the capacity 
7. To find the path, we'll have to return the indices of the previous nodes using the prev attribute starting from the target node 
    
"""

import math

neginf = (-1)*math.inf
inf = math.inf

class Vertex:
    # all the following are of constant time (O(1))    

    def __init__(self, index):
        self.index = index
        self.capacity = neginf
        self.prev = None
        self.adjlist = []
        self.tree_index = index
        self.in_queue = False

    def __lt__(self, other):
        if self.capacity != other.capacity:
            return (self.capacity < other.capacity)
        else:
            return (self.index < other.index)
    
    def __gt__(self, other):
        if self.capacity != other.capacity:
            return (self.capacity > other.capacity)
        else:
            return (self.index > other.index)

    def __eq__(self, other):
        return (self.capacity == other.capacity)

class MaxHeap:

    def __init__(self):
        self.heap = []
    
    def left_child(self, i):
        if (2*i + 1) < self.length():
            return 2*i + 1
        else:
            return None

    def right_child(self, i):
        if 2*i+2 < self.length():
            return 2*i+2
        else:
            return None 

    def length(self):
        return len(self.heap)

    def parent(self, i):
        if (i-1)//2 < 0:
            return None
        else:
            return (i-1)//2

    def get_value(self, i):
        return self.heap[i]

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i].tree_index, self.heap[j].tree_index = self.heap[j].tree_index, self.heap[i].tree_index # their tree indiced are also sapped 

    def heap_up(self, u):
        # for a given index u, it will compare the value in u with the value of u's parent and make sure the heap condition is followed
        # O(logn) 
        while ((self.parent(u) is not None) and (self.heap[self.parent(u)] < self.heap[u])):
            self.swap(u, self.parent(u))
            u = self.parent(u)

    def heap_down(self, u):
        # for a given index u, it will compare the value in u with the value of u's child and swap if condition is not followed 
        # O(logn)
        while (self.left_child(u)): 
            if (self.right_child(u)) and ((self.heap[self.left_child(u)]>self.heap[u]) or (self.heap[self.right_child(u)]>self.heap[u])):
                if self.heap[self.left_child(u)] < self.heap[self.right_child(u)]:
                    self.swap(u, self.right_child(u))
                    u = self.right_child(u)
                else:
                    self.swap(u, self.left_child(u))
                    u = self.left_child(u)
            elif (self.heap[self.left_child(u)]>self.heap[u]):
                self.swap(u, self.left_child(u))
                u = self.left_child(u)
            else:
                break

    def enqueue(self, u):
        # O(logn)
        self.heap.append(u) # u is added to the end of the almost complete binary tree such that the structural condition is satisfied 
        i = self.length()
        u.tree_index = i-1
        self.heap_up(i-1)

    def get_max(self):
        # O(logn)
        # this will remove the min value from the heap and return it 
        # it will also then make sure that the remaining nodes still form a heap 
        if self.length() == 0:
            return None
        else:
            max = self.heap[0]
            self.swap(0, -1)
            self.heap.pop() #this will remove the min value 
            self.heap_down(0)
            return max

    def change_key(self, u, x):
        # O(logn)
        # this will replace the value at index u with x
        org = self.heap[u]
        self.heap[u] = x
        # now, we need to make sure the heap condition is still being satisfied 
        if x > org :
            self.heap_up(u)
        elif x < org:
            self.heap_down(u)
        # the third case is when they are equal, in which is case, nothing is to be done 

def build_heap(l):
    # O(n)
    # for a given list of keys 'l', it creates a maxheap and returns it.
    new_heap = MaxHeap()
    new_heap.heap = l.copy()
    u = len(l) - 1
    while u >= 0 :
        new_heap.heap_down(u)
        u = u-1
    return new_heap

def findMaxCapacity(n, edges, s, t):
    # INPUT is as outlined above (edges used instead of links)
    vertices = []
    for i in range (0, n):  # O(n)
        vertices.append(Vertex(i))  # this means I'm turning all of them into vertices
    # processing the edges: 
    for item in edges:
        u = item[0]
        v = item[1]
        c = item[2]
        # the edge, along with the capacity, has to be added to each edge's adjacency list
        vertices[u].adjlist.append((v, c))
        vertices[v].adjlist.append((u, c))
    # Takes time O(m)
    # Now, graph has been constructed!
    # We will work on constructing the max heap 'capacities'
    nbs = []
    i = 0
    tree = 0
    adj = vertices[s].adjlist
    while i < len(adj):
        if adj[i][1] > vertices[adj[i][0]].capacity:
            vertices[adj[i][0]].capacity = adj[i][1]    # initialising the capacities to edge weights
            #vertices[adj[i][0]].in_queue = True
            vertices[adj[i][0]].prev = s
            if not vertices[adj[i][0]].in_queue:
                nbs.append(vertices[adj[i][0]])
                vertices[adj[i][0]].in_queue = True
                vertices[adj[i][0]].tree_index = tree
                tree = tree+1
        i = i+1
        # takes time O(deg(s))
    capacities = build_heap(nbs)    # takes time O(deg(s))
    while capacities.length != 0 and capacities.heap[0].index != t:
        max = capacities.get_max()
        if max.capacity == neginf:
            break
        nbrs = max.adjlist
        for nb in nbrs:
            temp = min(max.capacity, nb[1])
            if temp > vertices[nb[0]].capacity:
                vertices[nb[0]].capacity = temp
                vertices[nb[0]].prev = max.index
                # now, there can be two cases - either the vertex is alread in the heap, or, it has to be added
                # for this, I'll just maintain an attribute in_queue which will have a boolean value 
                if vertices[nb[0]].in_queue:
                    capacities.heap_up(vertices[nb[0]].tree_index)
                else:
                    # i thie case, the node will have to be added
                    vertices[nb[0]].tree_index = len(capacities.heap)-1
                    capacities.enqueue(vertices[nb[0]])
                    vertices[nb[0]].in_queue = True
    cap = vertices[t].capacity
    # now that we have found the max capacity, we can move on to finding the path by tracing it
    path = []
    u = t
    while u!=s:
        path.append(u)
        u = vertices[u].prev
    path.append(u)
    # list will have to be reversed since curently it contains the path from t to s and we want one from s to t
    i = 0
    l = len(path)
    while i < l//2:
        path[i], path[l-i-1] = path[l-i-1], path[i]
        i = i+1
    return (cap, path)

"""
TIME COMPLEXITY ANALYSIS:
1. The maxheap contains all the neighbours of the source node 
2. The max possible value of this is the total no. of vertices, which is n
3. So, the operations conducted in each loop are O(logn)
4. the loop runs O(m) times, so the total time complexity is O(mlogn)

PROVING THAT O(m) = O(n):
1. We use the formula for graphs -sum of deg of vertices = 2*(no. of edges)
2. since this is a connected graph, minimum degree is 1
3. so, we have n <= 2m
4. So, O(n)=O(m)
"""
"""
print(findMaxCapacity(3, [(0, 1,1),(1,2,1)],0,1))
print(findMaxCapacity(4,[(0,1,30),(0,3,10),(1,2,40),(2,3,50),(0,1,60),(1,3,50)],0,3))
print(findMaxCapacity(4,[(0,1,30),(1,2,40),(2,3,50),(0,3,10)],0,3))
print(findMaxCapacity(5,[(0,1,3),(1,2,5),(2,3,2),(3,4,3),(4,0,8),(0,3,7),(1,3,4)],0,2))
print(findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4),(2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))

print(findMaxCapacity(100, [(0, 1, 80), (1, 2, 93), (2, 3, 69), (3, 4, 79), (4, 5, 43), (5, 6, 52), (6, 7, 77), (7, 8, 11), (8, 9, 80), (9, 10, 64), (10, 11, 51), (11, 12, 30), (12, 13, 97), (13, 14, 58), (14, 15, 89), (15, 16, 69), (16, 17, 1), (17, 18, 65), (18, 19, 60), (19, 20, 50), (20, 21, 67), (21, 22, 27), (22, 23, 89), (23, 24, 16), (24, 25, 27), (25, 26, 50), (26, 27, 86), (27, 28, 24), (28, 29, 71), (29, 30, 51), (30, 31, 99), (31, 32, 78), (32, 33, 25), (33, 34, 55), (34, 35, 64), (35, 36, 43), (36, 37, 54), (37, 38, 83), (38, 39, 49), (39, 40, 93), (40, 41, 40), (41, 42, 56), (42, 43, 83), (43, 44, 100), (44, 45, 7), (45, 46, 45), (46, 47, 70), (47, 48, 63), (48, 49, 15), (49, 50, 43), (50, 51, 1), (51, 52, 86), (52, 53, 16), (53, 54, 32), (54, 55, 100), (55, 56, 84), (56, 57, 5), (57, 58, 90), (58, 59, 39), (59, 60, 87), (60, 61, 30), (61, 62, 76), (62, 63, 86), (63, 64, 21), (64, 65, 69), (65, 66, 95), (66, 67, 86), (67, 68, 50), (68, 69, 96), (69, 70, 71), (70, 71, 19), (71, 72, 71), (72, 73, 16), (73, 74, 40), (74, 75, 19), (75, 76, 85), (76, 77, 44), (77, 78, 6), (78, 79, 6), (79, 80, 9), (80, 81, 10), (81, 82, 79), (82, 83, 71), (83, 84, 79), (84, 85, 68), (85, 86, 70), (86, 87, 1), (87, 88, 48), (88, 89, 73), (89, 90, 97), (90, 91, 72), (91, 92, 3), (92, 93, 37), (93, 94, 58), (94, 95, 26), (95, 96, 62), (96, 97, 77), (97, 98, 50), (98, 99, 67), (7, 55, 80), (64, 41, 98), (99, 9, 29), (7, 76, 32), (82, 20, 2), (52, 59, 98), (10, 75, 75), (87, 27, 91), (49, 80, 6), (9, 55, 10), (0, 82, 68), (3, 16, 79), (79, 78, 33), (70, 34, 90), (84, 87, 83), (90, 58, 52), (92, 30, 31), (80, 7, 93), (92, 59, 12), (5, 59, 55), (85, 77, 98), (83, 39, 82), (76, 44, 83), (12, 11, 79), (56, 15, 30), (92, 8, 38), (90, 7, 60), (92, 65, 2), (22, 67, 90), (78, 76, 82), (37, 62, 9), (36, 63, 67), (33, 17, 51), (26, 36, 66), (39, 22, 86), (53, 76, 67), (53, 72, 52), (56, 80, 27), (6, 81, 24), (12, 1, 33), (55, 16, 85), (79, 68, 67), (38, 17, 43), (63, 82, 100), (36, 49, 20), (25, 42, 11), (37, 33, 83), (9, 13, 85), (61, 40, 86), (75, 50, 50), (78, 57, 38), (40, 44, 85), (94, 41, 34), (38, 73, 14), (23, 77, 7), (41, 52, 50), (24, 19, 90), (55, 27, 66), (68, 65, 57), (61, 69, 96), (15, 34, 89), (49, 46, 47), (37, 75, 64), (81, 20, 40), (72, 53, 62), (28, 22, 53), (55, 95, 86), (57, 94, 2), (46, 98, 75), (59, 22, 8), (14, 19, 80), (76, 37, 34), (52, 64, 74), (75, 49, 82), (62, 43, 2), (19, 14, 6), (70, 74, 69), (36, 17, 57), (44, 62, 34), (99, 43, 92), (71, 61, 19), (99, 77, 7), (24, 21, 53), (69, 20, 82), (30, 82, 47), (71, 77, 23), (50, 72, 36), (56, 52, 52), (35, 38, 2), (23, 40, 52), (29, 84, 77), (28, 35, 31), (13, 74, 8), (46, 41, 28), (36, 73, 50), (13, 46, 82), (84, 82, 36), (44, 62, 88), (22, 45, 85), (72, 70, 73), (70, 37, 55), (63, 70, 4), (35, 21, 3), (65, 74, 33), (26, 84, 14), (52, 41, 69), (35, 82, 43), (25, 4, 60), (0, 99, 92), (79, 54, 59), (45, 94, 67), (49, 45, 55), (81, 5, 81), (27, 64, 69), (65, 5, 64), (41, 94, 71), (34, 49, 23), (30, 90, 47), (23, 98, 29), (71, 54, 21), (14, 25, 95), (72, 2, 64), (83, 41, 76), (41, 72, 67), (30, 24, 90), (5, 88, 72), (33, 17, 81), (76, 33, 18), (91, 99, 97), (56, 58, 24), (32, 72, 58), (60, 55, 25), (48, 93, 92), (7, 38, 36), (32, 25, 80), (2, 80, 48), (56, 63, 40), (43, 45, 80), (65, 56, 51), (43, 70, 75), (80, 10, 48), (20, 70, 1), (92, 84, 77), (35, 3, 23), (29, 74, 90), (64, 72, 77), (72, 97, 66), (95, 78, 67), (2, 33, 42), (92, 13, 99), (41, 62, 91), (9, 42, 53), (93, 16, 76), (11, 71, 66), (66, 36, 4), (71, 33, 69), (94, 45, 42), (65, 1, 38), (64, 37, 57), (16, 56, 95), (7, 63, 5), (22, 45, 95), (59, 9, 90), (94, 55, 29), (33, 14, 53), (31, 72, 84), (84, 22, 37), (43, 37, 76), (21, 9, 68), (25, 16, 46), (1, 35, 3), (43, 76, 28), (43, 52, 28), (2, 85, 14), (50, 41, 41), (86, 69, 80), (28, 80, 65), (25, 37, 2), (77, 41, 78), (77, 49, 45), (34, 2, 82), (31, 9, 28), (47, 13, 69), (35, 15, 81), (9, 72, 76), (89, 92, 81), (8, 44, 26), (54, 37, 8), (46, 58, 97), (72, 66, 25), (53, 57, 33), (77, 20, 89), (44, 49, 86), (95, 43, 3), (90, 11, 82), (23, 30, 15), (11, 39, 37), (28, 6, 60), (0, 6, 69), (57, 44, 9), (86, 59, 94), (92, 51, 10), (29, 84, 62), (62, 82, 90), (10, 78, 6), (15, 64, 61), (27, 47, 88), (28, 52, 95), (13, 69, 60), (43, 38, 46), (22, 53, 8), (89, 45, 47), (15, 11, 42), (58, 21, 72), (78, 96, 24), (85, 17, 19), (26, 60, 39), (7, 23, 36), (26, 20, 84), (59, 8, 77), (41, 36, 85), (25, 58, 98), (77, 27, 39), (54, 15, 36), (2, 0, 5), (11, 84, 62), (19, 45, 74), (21, 76, 12), (2, 81, 99), (32, 33, 97), (40, 0, 7), (68, 54, 15), (17, 28, 77), (82, 96, 60), (79, 95, 21), (81, 18, 94), (74, 78, 71), (16, 67, 92), (98, 94, 1), (66, 15, 25), (73, 20, 50), (79, 65, 17), (93, 22, 6), (96, 87, 1), (64, 57, 70), (19, 78, 56), (39, 19, 21), (43, 4, 50), (52, 87, 71), (64, 86, 19), (9, 70, 62), (33, 60, 57), (19, 51, 41), (3, 29, 7), (96, 77, 23), (3, 65, 38), (33, 66, 14), (0, 87, 22), (16, 65, 20), (42, 71, 86), (0, 37, 41), (40, 52, 68), (78, 22, 25), (71, 70, 95), (23, 7, 100), (10, 63, 48), (19, 2, 33), (18, 76, 18), (75, 30, 1), (73, 68, 41), (13, 7, 54), (4, 11, 41), (57, 66, 70), (97, 34, 24), (99, 8, 59), (84, 3, 84), (52, 54, 89), (54, 88, 22), (19, 94, 89), (23, 62, 6), (43, 86, 6), (7, 67, 4), (75, 23, 2), (17, 65, 10), (74, 90, 86), (87, 60, 17), (99, 37, 95), (29, 80, 98), (49, 30, 23), (72, 57, 96), (55, 71, 9), (72, 81, 61), (7, 54, 1), (42, 53, 75), (30, 41, 30), (94, 7, 82), (69, 98, 10), (25, 58, 56), (49, 83, 51), (0, 19, 36), (37, 4, 72), (13, 56, 56), (94, 15, 55), (30, 18, 51), (10, 24, 12), (20, 72, 6), (77, 69, 77), (39, 35, 49), (28, 91, 39), (4, 23, 73), (88, 10, 69), (44, 10, 55), (80, 52, 54), (53, 98, 17), (81, 58, 40), (36, 22, 17), (1, 93, 22), (58, 56, 64), (45, 60, 44), (10, 71, 22), (55, 64, 71), (44, 95, 27), (23, 82, 13), (53, 36, 53), (10, 93, 49), (4, 23, 89), (46, 15, 18), (62, 24, 42), (3, 45, 63), (98, 59, 68), (89, 51, 51), (65, 7, 90), (38, 56, 14), (40, 67, 58), (21, 31, 26), (59, 87, 3), (69, 90, 33), (45, 1, 76), (73, 68, 63), (20, 1, 53), (23, 14, 96), (72, 6, 7), (86, 66, 22), (3, 33, 72), (50, 29, 51), (87, 5, 55), (42, 57, 32), (10, 56, 15), (92, 91, 58), (31, 84, 66), (83, 93, 43), (4, 2, 36), (20, 84, 21), (0, 99, 48), (84, 85, 73), (33, 8, 95), (83, 17, 89), (26, 48, 59), (19, 77, 84), (80, 20, 26), (60, 17, 87), (99, 97, 85), (66, 48, 57), (4, 62, 32), (28, 1, 78), (83, 26, 83), (34, 50, 96), (65, 29, 82), (99, 1, 93), (15, 10, 43), (13, 36, 93), (7, 57, 90), (35, 89, 92), (35, 74, 7), (53, 21, 51), (10, 34, 72), (68, 77, 42), (47, 30, 19), (63, 55, 38), (27, 95, 84), (62, 0, 81), (63, 34, 42), (18, 84, 82), (88, 11, 77), (37, 17, 72), (73, 15, 7), (43, 98, 60), (44, 85, 23), (72, 82, 24), (91, 87, 32), (80, 58, 41), (34, 0, 75), (79, 36, 50), (36, 62, 42), (70, 93, 65), (88, 76, 21), (59, 39, 47), (90, 92, 67), (45, 28, 48), (86, 52, 99), (8, 5, 66), (44, 54, 48), (69, 39, 47), (46, 55, 53), (14, 33, 52), (34, 92, 93), (2, 63, 96), (78, 46, 81), (2, 46, 7), (17, 91, 98), (71, 72, 50), (73, 53, 85), (75, 76, 67), (55, 97, 71), (58, 31, 93), (56, 51, 25), (81, 2, 69), (37, 42, 76), (79, 71, 31), (1, 13, 72), (20, 70, 73), (0, 61, 83), (68, 0, 96), (24, 60, 78), (13, 11, 84), (84, 15, 78), (51, 26, 20), (37, 9, 90), (25, 29, 1), (92, 97, 37), (10, 76, 99), (97, 78, 91), (23, 5, 39), (85, 25, 89), (69, 40, 16), (8, 1, 96), (66, 20, 46), (77, 18, 95), (24, 89, 71), (15, 22, 55), (2, 35, 25), (96, 88, 13), (15, 88, 43), (65, 76, 44), (56, 40, 77), (73, 36, 6), (99, 98, 1), (32, 53, 12), (71, 21, 58), (14, 42, 40), (72, 46, 25), (16, 51, 52), (72, 16, 47), (64, 88, 16), (28, 9, 4), (12, 92, 59), (23, 95, 53), (3, 44, 37), (52, 88, 43), (92, 71, 44), (5, 36, 4), (98, 39, 81), (46, 44, 20), (82, 13, 81), (28, 61, 33), (16, 67, 25), (63, 26, 91), (8, 27, 26), (50, 80, 34), (10, 94, 84), (18, 78, 92), (73, 88, 14), (88, 63, 99), (80, 68, 70), (16, 92, 56), (70, 6, 72), (12, 93, 59), (28, 44, 8), (2, 10, 63), (1, 17, 69), (42, 18, 6), (82, 47, 69), (95, 86, 91), (86, 61, 52), (26, 80, 31), (50, 21, 42), (33, 58, 77), (30, 67, 31), (99, 39, 76), (39, 49, 64)], 73, 5))
"""