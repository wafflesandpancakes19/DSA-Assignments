class Empty (Exception):
    pass

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self._top = None  # The top element is empty
        self.stack_size = 0  # The stack size is zero since there are no elements

    def __len__(self):
    # SPECIFICATION: returns the length of the stack
        return self.stack_size #The attribute 'stack_size' keeps a track of the length of the stack

    def push(self, item):
    # SPECIFICATION: adds an element to the top of the stack
        temp = Node(item)  # this variable will store the data that is to be pushed onto the stack
        # The top element will now have to be item instead of the previous eloement
        if self._top is None:
            self._top = temp # for an empty stack, the top element is simply assigned the value of item
            self.stack_size = self.stack_size + 1 #the stack size is increased by 1 
        else: # ( for a non-empty stack)
            temp.next = self._top #the top element in the stack is actually assigned as the next element
            self._top = temp # and the top element now becomes the item that was to be pushed 
            self.stack_size = self.stack_size + 1 
        # takes O(1) time

    def is_empty(self):
        return (self.stack_size == 0)

    def pop(self):
    # SPECIFICATION: removes the top element of the stack
        if self._top == None:   # if the stack is empty, it raises an error
            raise Empty ("stack is empty")
        else:
            temp = self._top
            self._top = self._top.next
            self.stack_size = self.stack_size - 1 
            return temp.data    # the 'popped' item is returned
        # takes O(1) time 

    def top(self):
    # SPECIFICATION: returns the element at the top of the stack
        if self._top == None:
            raise Empty ("Stack is empty")
        else:
            return self._top.data

def evaluate(item, pos):
    """
    SPECIFICATION: The function takes the arguments 'item' which is a tuple consisting of a sign and a
    direction (X, Y, Z), and the argument 'pos' which is the position and is a list of length 4 represented 
    as [x, y, z, d], with d being the distance covered.
    It then returns an 'updated' position value, after evaluating 'item'
    """
    # the parameter 'item' is evaluated thorugh a set of conditionals as given below: 

    if item[1] == 'X':
        if item[0] == '+':
            pos[0] = pos[0] + 1
        elif item[0] == '-':
            pos[0] = pos[0] - 1
        else:
            print("There is an error in the input")
    elif item[1] == 'Y':
        if item[0] == '+':
            pos[1] = pos[1] + 1
        elif item[0] == '-':
            pos[1] = pos[1] - 1
        else:
            print("There is an error in the input")
    elif item[1] == 'Z':
        if item[0] == '+':
            pos[2] = pos[2] + 1
        elif item[0] == '-':
            pos[2] = pos[2] - 1
        else:
            print("There is an error in the input")
    else:
        print("There is an error in the input")
    pos[3] = pos[3] + 1
    # Because this is a set of comparisons that have to be made, the entire helper function takes O(1) time. 
    return pos

def findPositionandDistance(P):
    """
    SPECIFICATION: 
    This function takes a string 'P' which is a set of commands containing only +,-, X, Y, Z, and brackets. 
    It then evaluates them and returns a list 'ans' of the form [x, y, z, d] where x, y, and z represent 
    final coordinates and d represents the distance covered.
    """
    ans = [0, 0, 0, 0]  # formatted as [x, y, z, distance]
    # STEP 1: TAKING INPUT
    P = list(P) #takes the string  and converts it to a list to make it easier through iterate through it 
    # STEP 2: CREATING STACKS 
    nums = Stack()  # this stores the integers 
    comms = Stack() # This stores the commands as well as the brackets 
    """
    BASIC MOTIVATION FOR ALGORITHM:
    - commands which do not come inside brackets are executed immediately
    - for commands inside brackets, 2 stacks are maintained
    - one stack stores the integers that the commands have to be multiplied with
    - the second stack stores the commands that have to be evaluated 
    - When the program encounters an opening bracket, it pushes it onto the comms stack 
    - it continues to push commands onto comms and any integers it encounters onto nums till it 
    encounters a closing bracket - this means that the inner most bracket has been completed 
    - At this point, the program starts popping the commands from the stack and evaluating them till the time it doesn't encounter an opening bracket
    - when all the commands inside the innermost bracket have been evaluated, it multiplies the obtained sum of all the instructions with the product of all the integers
    that are present in the nums stack and adds this to the ans.
    - it then continues in a similar fashion unless another ')' is reached and the same process is repeated till there are no commands left. 
    """
    # STEP 3: INITIALISATION:
    i = 0
    val = 1 # the variable 'val' will maintain the product of all the integers that have been added to the nums stack 
    open= 0 # This keeps track of the number of open brackets encountered (so that the program keeps pushing commands onto the stack in case of nested brackets)
    while i < len(P):   # loop condition - so that the entire string is iterated over 
        if (P[i] == '(') or (open!=0):  # checks for open bracket or if an open bracket has not been closed (open != 0)
            if P[i] == '(':
                comms.push(P[i])
                open = open+1
                i = i+1 # this entire set of commands takes O(1) time 
            while P[i] != ')':  # the loop will be exited when a closing bracket has been encountered 
                if P[i] == '(':
                    comms.push(P[i])
                    open = open+1
                    i = i+1
                elif P[i] == '+' or P[i] == '-':
                    comms.push((P[i], P[i+1]))  # a simple command is pushed onto the stack in the form (sign, direction) for ease of evaluation later on
                    i = i+2
                else:
                    num = []
                    while P[i].isdigit():
                        num.append(P[i])
                        i = i+1 
                    num = int(''.join(num))
                    val = val*num
                    nums.push(num)
            i = i+1
            pos = [0, 0, 0, 0]
            # When the program does encounter a closing bracket, it'll start popping commands till it encounters an opening bracket 
            numels = 0
            while comms.top() != '(':   # the program will start popping commands and evaluating them till the top element of the stack does not become '('
                item = comms.pop()
                pos = evaluate(item, pos) # takes O(1) time 
                numels = numels+1   # numels refers to the number of commands popped - used to evaluate distance in line 155 
            comms.pop() # This is because there is still an open bracket left in the stack 
            open = open-1   # Since one bracket has been evaluated, open is decreased
            for j in range(0, 3):
                ans[j] = val*pos[j]+ans[j] # This is simply to multiply the evaluated position with the required integer and to add to the final ans - hence, O(1)
            ans[3] = ans[3] + val*numels
            val = val//nums.pop() # once the bracket has been evaluated, the integer corresponding only to that bracket is popped and val is divided by it to maintain the 
            # function of val which is to store the product of the integers that are present in stack 'nums'
        # the code from line 157 to 174 is to directly evaluate commands that do not come in brackets
        # since it is simply a set of conditionals, the time complexity is O(1)
        elif P[i] == '+':
            if P[i+1] == 'X':
                ans[0] = ans[0]+1
            elif P[i+1] == 'Y':
                ans[1] = ans[1]+1
            else:
                ans[2] = ans[2]+1
            i = i+2
            ans[3] = ans[3]+1
        elif P[i] == '-':
            if P[i+1] == 'X':
                ans[0] = ans[0]-1
            elif P[i+1] == 'Y':
                ans[1] = ans[1]-1
            else:
                ans[2] = ans[2]-1
            i = i+2
            ans[3] = ans[3]+1
        elif P[i] == ')':
            i = i+1
        else:
            num = []    # the entire set of commands is to convert the obtained string input into integers (multiple digit integers included)
            while P[i].isdigit():
                num.append(P[i])
                i= i+1
            num = int(''.join(num))
            val = val*num
            nums.push(num)
    return ans

"""
TIME COMPLEXITY ANALYSIS:
In the program, we run one counter i which iterated through the entire list. 
Because of this, it can be considered, as one while loop
All the operations performed on each element of the list are of compplexity O(1)
Therefore, the complexity of the entire algorithm is O(1)*O(n) = O(n)
Hence, the algorithm is of time complexity O(n) (as desired)
"""

# SOME TEST CASES TO TEST OUT THE CODE: 
# print(findPositionandDistance('+X+X+Y+Z21(-Z)'))
# print(findPositionandDistance('+Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))'))
# print(findPositionandDistance('+X2(+Y-X-Z)8(+Y)9(-Z-Z)'))
# print(findPositionandDistance('+X+X+Y3(+X+Y)6(+Z)'))