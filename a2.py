# ASSIGNMENT 2: TRACKING COLLISIIONS

"""
INPUT:
1.M: a list of positive floats, where M[i]is the mass of the i'th object
2.x: a sorted list of floats, where x[i]is the initial position of the i'th object
3.v: a list of floats, where v[i]is the initial velocity of the i'th object
4.m: a non-negative integer
5.T: a non-negative float
"""

"""
OUTPUT:
List of collisions
each collision is represented as (t, i, x) where t is the time, i is the collsion between i and i+1th element, and x is the position
the list will end when either 'm' collisions happen or the total time exceeds 'T', whichever happens first
"""

# TARGETED TIME COMPLEXITY: O(n + mlog(n))

"""
WHAT SORT OF STRUCTURES ARE REQUIRED?
1. class that defines objects in the given space:
    ATTRIBUTES:
        - position
        - velocity
        - index
        - mass
        - tree_index
        - last_collision
    METHODS:
        - update_position
        - update_velocity
        - collide (self, other) # maybe this will automatically update the position and location in case of a collision?
2. BINARY HEAPS (for O(log(n)) time calculations):
    maintain a binary heap of collision times - need enqueue and dequeue operations (both take O(logn) time)
    buildHeap is also needed
    METHODS:
        - heapUp()
        - heapDown() - will be used for extracting minimum and buildHeap()
        - changeKey() - will be used for the other 2 changes that are made in every iteration 
        - buildHeap() - will be used for building the initial heap 
        - enqueue()
        - dequeue()   
"""
"""
WHAT FORMULAS ARE REQUIRED? (FROM PHYSICS)
1. formula for velocities in case of an elastic collision
2. formula for finding time ( t = (x2-x1)/(v1-v2) )
3. x = x + v(t2-t1)
"""
"""
NEW ALGORITHM:
1. take in all the inputs and create RealObjects from them (O(n) time)
2. calculate the time taken for collision for each of the n-1 collisions
3. construct a binary heap from these collisions
4. for every collision, dequeue the root of the binary heap
5. make the respective objects 'collide'
6. recalculate the times for (i-1, i), (i, i+1), (i+1, i+2) collisions and enqueue these (need a way to find their indices in the minheap)
time elapsed will also have to be added to these
7. update positions of the colliding objects 
8. dequeue the root again and repeat the process

total time complexity: O(n+mlog(n))
"""

import math

class BinaryHeap:

    def __init__(self):
        self.heap = []  # self.heap represents the list containing the values of all the nodes 

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
        self.heap[i].tree_index, self.heap[j].tree_index = self.heap[j].tree_index, self.heap[i].tree_index # their tree indiced are also swapped 

    def heap_up(self, u):
        # for a given index u, it will compare the value in u with the value of u's parent and make sure the heap condition is followed 
        while ((self.parent(u) is not None) and (self.heap[self.parent(u)] > self.heap[u])):
            self.swap(u, self.parent(u))
            u = self.parent(u)

    def heap_down(self, u):
        # for a given index u, it will compare the value in u with the value of u's child and swap if condition is not followed 
        while (self.left_child(u)): 
            if (self.right_child(u)) and ((self.heap[self.left_child(u)]<self.heap[u]) or (self.heap[self.right_child(u)]<self.heap[u])):
                if self.heap[self.left_child(u)] > self.heap[self.right_child(u)]:
                    self.swap(u, self.right_child(u))
                    u = self.right_child(u)
                else:
                    self.swap(u, self.left_child(u))
                    u = self.left_child(u)
            elif (self.heap[self.left_child(u)]<self.heap[u]):
                self.swap(u, self.left_child(u))
                u = self.left_child(u)
            else:
                break

    def enqueue(self, u):
        self.heap.append(u) # u is added to the end of the almost complete binary tree such that the structural condition is satisfied 
        i = self.length()
        u.tree_index = i-1
        self.heap_up(i-1)

    def get_min(self):
        # this will remove the min value from the heap and return it 
        # it will also then make sure that the remaining nodes still form a heap 
        if self.length() == 0:
            return None
        else:
            min = self.heap[0]
            self.swap(0, -1)
            self.heap.pop() #this will remove the min value 
            self.heap_down(0)
            return min

    def change_key(self, u, x):
        # this will replace the value at index u with x
        org = self.heap[u]
        self.heap[u] = x
        # now, we need to make sure the heap condition is still being satisfied 
        if x < org :
            self.heap_up(u)
        elif x > org:
            self.heap_down(u)
        # the third case is when they are equal, in which is case, nothing is to be done 

def build_heap(l):
    # for a given list of keys 'l', it creates a minheap and returns it.
    new_heap = BinaryHeap()
    new_heap.heap = l.copy()
    u = len(l) - 1
    while u >= 0 :
        new_heap.heap_down(u)
        u = u-1
    return new_heap

class RealObject:

    def __init__(self, position, velocity, index, mass):
        self.position = position
        self.velocity = velocity
        self.index = index
        self.mass = mass
        self.collision_time = math.inf
        self.last_collision = 0
        self.tree_index = index 
        # Time complexity: O(1)

    # setter methods for mass and index have not been defined because these do not change for a particular object 

    # operator overloading has been done for comparison operators to make it easier to compare objects in binary heap
    def __lt__(self, other):
        if self.collision_time != other.collision_time:
            return (self.collision_time < other.collision_time)
        else:
            return (self.index < other.index)

    def __gt__(self, other):
        if self.collision_time != other.collision_time:
            return (self.collision_time > other.collision_time)
        else:
            return (self.index > other.index)

    def __eq__(self, other):
        if self.collision_time != other.collision_time:
            return (self.collision_time == other.collision_time)
        else:
            return (self.index == other.index) 

    def update_position(self, position):
        self.position = position
        # Time compllexity: O(1)

    def update_velocity(self, velocity):
        self.velocity = velocity
        # Time complexity: O(1)

    def update_collision_time(self, time):
        self.collision_time = time
        # Time complexity = O(1)

    def collide(self, other):
        u1 = self.velocity
        u2 = other.velocity
        self.velocity = ((self.mass - other.mass)*u1 + 2*other.mass*u2)/(self.mass + other.mass)
        other.velocity = ((other.mass - self.mass)*u2 + 2*self.mass*u1)/(self.mass + other.mass)
        # Time complexity: O(1)

    def time_to_collide(self, other):
        if self.velocity == other.velocity:
            return math.inf
        else:
            t = (other.position-self.position)/(self.velocity-other.velocity)   # time taken is difference in pos./relative vel
            if t<0: # in such a case, the objects are moving in diff directions and hence would never collide 
                return math.inf # hence, returning infinity 
            else:   # in such a case, objects would collide at time 't'
                return t


def listCollisions(M, x, v, m, T):
    # PART I: PROCESSING INPUT AND CREATING OBJECTS OF CLASS RealObject:
    list_objects = []
    collisions = [] # this will be the output list 
    for i in range(0, len(M)):
        ball = RealObject(x[i], v[i], i, M[i])
        list_objects.append(ball)
        if i == 0:
            continue
        else:
            list_objects[i-1].collision_time = list_objects[i-1].time_to_collide(list_objects[i])   # collision times have been calculated 
    # PART II: MAKING A MINHEAP:
    times = build_heap(list_objects)
    # PART III: COLLISIONS: 
    # this will run in a while loop with 2 conditions: either no of collisions > m or total collision time > T (maintain variable tot_t)
    tot_t = 0
    num_coll = 0
    while (tot_t <= T) and (num_coll < m):
        coll = times.get_min()  # pull out the collision that takes the min time
        if coll.collision_time == math.inf:
            return collisions
        else:
            i = coll.index
            #x = coll.position + coll.velocity*coll.collision_time
            tot_t = coll.collision_time # the time elapsed from the start is the time of the collision
            coll.position = coll.position + coll.velocity*(tot_t - coll.last_collision) # it has maintained this velocity since the time of its last collision
            x = coll.position   # the new updated position 
            list_objects[i+1].position = x  # the other object will have the same position
            coll.last_collision = tot_t    # time of last collision is updated to tot_t
            list_objects[i+1].last_collision = tot_t    # same is happening here
            coll.collide(list_objects[i+1]) # new velocities are calculated and updated 
            coll.collision_time = math.inf   # they won't collide after this unless they collide with other objects first 

            if i > 0:
                t_ind1 = list_objects[i-1].tree_index   # will help change the key in the tree 
                org = list_objects[i-1].position    # this stores the original position of the object
                list_objects[i-1].position = list_objects[i-1].position + list_objects[i-1].velocity*(tot_t - list_objects[i-1].last_collision) # their position is temporarily updated
                t1 = list_objects[i-1].collision_time   # original collision_time is stored (will be used to maintain minheap)
                list_objects[i-1].collision_time = list_objects[i-1].time_to_collide(list_objects[i]) + tot_t   # collision time is updated 
                list_objects[i-1].position = org    # initial position is restored 
                if list_objects[i-1].collision_time > t1:   # basically to maintain the heap 
                    times.heap_down(t_ind1)
                else:
                    times.heap_up(t_ind1)

            if i < len(M)-2:
                t_ind2 = list_objects[i+1].tree_index   
                org = list_objects[i+2].position
                list_objects[i+2].position = list_objects[i+2].position + list_objects[i+2].velocity*(tot_t - list_objects[i+2].last_collision)
                t2 = list_objects[i+1].collision_time 
                list_objects[i+1].collision_time = list_objects[i+1].time_to_collide(list_objects[i+2]) + tot_t
                list_objects[i+2].position = org
                if list_objects[i+1].collision_time > t2:
                    times.heap_down(t_ind2)
                else:
                    times.heap_up(t_ind2)
            times.enqueue(list_objects[i]) # it has been re-added to the list with the updated collision time
            if tot_t <= T:
                collisions.append((tot_t, i, x))    # collision is appended to the list 
            num_coll = num_coll + 1
    res = []
    for item in collisions:
        res.append((round(item[0], 4), item[1], round(item[2], 4)))
    return res


"""
print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
print(listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5,5.0))
print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))
print(listCollisions([1, 1, 1, 1, 1, 1], [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], [1.0, 0.0, 1.0, 0.0, 1.0, 0.0], 8, 100))
"""