# DEFINING HELPER FUNCTIONS FOR DATA HANDLING:

# 1. TO FIND AN ELEMENT IN THE LIST AND RETURN ITS POSITION:
def inList(L, k):
    # SPECIFICATION: It takes the input of a list L and an element k and returns a tuple of the form (found, i), where, found is a 
    # Boolean value indicating whether k is in L and i is the index of k if it is in L.
    # INITIALISATION:
    i = 0 
    l = len(L)
    found = False
    # LOOP:
    while i<l and not found:
        # TERMINATION: Since (l-i) decreases from l to 0, the loop will terminate. 
        if L[i] == k and type(L[i]) is type(k):
            # Types are also being compared to avoid confusions like confusing True and 1 or False and 0.
            found = True
            # Since found is updated to True, loop condition will no longer be satisfied and the loop will break and return (found, i)
        else:
            i = i+1
            # Otherwise, if the element is not found, it'll check the next list element 
    """
    TIME COMPLEXITY:
    Worst case: When the last element matches the required element or when the element is not present in the list
    In this case, time complexity is O(n), where n is the length of the list.
    """
    return (found, i)

# 2. TO FIND THE ADDRESS A VARIABLE IS POINTING TO, IF THE VARIABLE HAS ALREADY BEEN DEFINED 
def find_reference(var, L):
    # SPECIFICATION: this function returns the pair of the variable and the reference position if the variable is present in the list 
    # If the variable is not present, then it returns false. 
    # INITIALISATION:
    found = False
    i = 0 
    for item in L:
        # the variable and its reference are stored in the form of a tuple in the list.
        # So, the first check it performs is whether the type of the element is a tuple 
        if type(item) is tuple:
            # If it is a tuple, we need to check that the tuple is for the variable we are looking for 
            if item[0] != var:
                found = False
            else:
                found = True
                i = item[1]
                break # Function will break out of the loop when it finds the variable
    """
    TIME COMPLEXITY:
    Since the function iterates over the list, time complexity is O(n), where n is the length of the list L. 
    """
    return (found, i)

# 3. TO ASSIGN AN ADDRESS TO THE VARIABLE AFTER THE EXPRESSION HAS BEEN EVALUATED
def find_value(found, i, ans, data):
    # SPECIFICATION: the function returns the place of ans in the list. 
    # If ans is already in the list, then it returns the position where ans is stored 
    # If ans is not in the list, it appends the ans to the list, and returns the index of the last element 
    if found:
        d = i
    else:
        data.append(ans)
        d = len(data)-1
    """
    TIME COMPLEXITY:
    We see that the operations to be performed take constant time.
    Hence, time complexity is O(1). 
    """
    return d

# 4. TO ADD THE TUPLE TO THE LIST:
def add_to_list(var, d, data):
    # SPECIFICATION: It updates the variable and the reference.
    (found, i) = find_reference(var, data)
    if not found:
        # If the variable is not already in the list, it adds it
        data.append((var, d))
    else:
        # if the variable is already in the list, it updates it 
        (f, j) = inList(data, (var, i))
        data[j] = (var, d)
    """
    TIME COMPLEXITY:
    - 'n' is the length of 'data'
    1. The function first calls find_reference(), which has time complexity O(n).
    2. It may then call the function inList() in the worst case scenario. inList() has time complexity O(n). 
    3. So, the worst case time complexity is O(n)+O(n) = O(n).
    """

# 5. GARBAGE COLLECTION
def garbage_collect(data):
    # SPECIFICATION: It makes a list of all the elements in data that are not being referenced by any variable 
    use = []
    garbage = []
    for item in data:
        if type(item) is tuple:
            # It first makes a list of all the 'useful' items
            # the list contains all the variables and all the values that these variables are pointing at
            use.append(item)
            use.append(data[item[1]])
    for item in data:
        # then, if an item is not in the 'useful' list, it is added to the garbage list.
        if item not in use:
            garbage.append(item)
    """
    TIME COMPLEXITY:
    Since we are iterating over the list 'data' twice,
    Time complexity is O(n).
    Where, 'n' is the length of the list 'data'.
    """
    return garbage 

# 6. LIST OF VARIABLES AND THEIR VALUES
def var_value(data):
    # SPECIFICATION: It returns a list of all the variables and their values.
    # Each element in the list is represented as ('variable_name', 'value')
    values = []
    for item in data:
        if type(item) is tuple:
            # If the item is a tuple, it is storing the variable and the address it is referencing 
            values.append((item[0], data[item[1]]))
    """
    TIME COMPLEXITY:
    Since the function is iterating over the list 'data',
    The time complexity is O(n).
    Where 'n' is the length of the 'data' list. 
    """
    return values 

data = []

INSTRUCTION_LIST = []

"""
PROGRESSION OF THOUGHTS:
1. Code I have: can detect statements of the form x = expression and evaluate them as desired 
2. code I don't have: 
    In case of a while loop, the expression may not be of the form mentioned above 
    For example, instead of x = a > b, it'll ve while a > b
    One way to solve this problem is if i insert another element after the while token so that the statement
    behaves like the set statements 
3. How do I handle the code inside the while loop?
4. How do I go back to the beginning of the loop after each iteration?
    will have to store the code for this instead of executing it line by line
5. What all should I include in the instructions class?
    a. Type of Branch:
        BLE - Branch if less than or equal to
        BLT - Branch if less than
        BE - branch if equal to
        Branch - branch unconditionally 
6. First get the instruction list ready along with the kind of instructions you'll be giving 
7. Then, start reading the list one by one and executing the statements like it was done in assignment 5 
"""

class instruction:
    def __init__(self, statement, tabs):
        self.type = 'ASSIGN' # the default is 'ASSIGN', this will however get updated later 
        self.operands = [] # stores the variables that the instruction is manipulating
        self.address = len(INSTRUCTION_LIST)
        self.statement = statement # instruction statement
        self.end = self.address # The index of the instruction in the list 
        self.start = self.address 
        self.tabs = tabs # counts no. of tabs in front of the statement
        self.branch_count = 0 # no. of statements of the type

    def assign_type(self): # works well!
        # assigns the type of the instruction
        if self.statement[0] == 'while':
            if self.statement[2] == '>':
                self.type = 'BLE'
                a = self.statement[1] # 1st operand
                b = self.statement[3] # 2nd operand
                b = b[:(len(b)-1)] # colon is removed since a > b: is written
            elif self.statement[2] == '>=':
                self.type = 'BLT'
                a = self.statement[1]
                b = self.statement[3]
                b = b[:(len(b)-1)]
            elif self.statement[2] == '==':
                self.type = 'BE'
                a = self.statement[1]
                b = self.statement[3]
                b = b[:(len(b)-1)]
            elif self.statement[2] == '<': # if the instruction has <=, it is of BLE type but with the operands reversed 
                self.type = 'BLE' # The operands are swapped so that it beomes BLE type 
                b = self.statement[1]
                a = self.statement[3]
                a = a[:(len(a)-1)]
            elif self.statement[2] == '<=': # If the instruction has <, it is of BLT type but with the operands reversed.
                self.type = 'BLT' # the operands are swapped so that it becomes BLT type
                b = self.statement[1]
                a = self.statement[3]
                a = a[:(len(a)-1)]
            else:
                print(f"INVALID INPUT: line{self.address}: Please enter valid condition in while loop")
            self.operands.append(a)
            self.operands.append(b)
        else:
            self.type = 'ASSIGN' # It is a simple expression in which a value is being assigned to a variable 
        # Time complexity is O(1) because all of the functions used take constant time

    def __str__(self):
        return self.statement # The string form of an instruction is the statement
        # Takes O(1) time complexity

    def evaluate_stat(self, w):
        # This function evaluates the given statement 
        line = self.statement
        k = self.address
        if self.type == 'ASSIGN': # If the statement is a simple assignemnt, then:
            var = line[0] # Since the input is of the form var = expression, the 0th element of the list is the variable. 
            n = len(line)
            if n==5:
                # the length is 5 when a binary operator is used.
                # The only possible binary operators are: '+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', 'and', and 'or'
                a = line[2]
                b = line[4]
                if b[-1] == '\n': # The '\n' is added by default if something is written in the next line in the input 
                    b = b[:-1] # This has to be removed for string comparison to be effective. 
                else:
                    b = b
                # In case a or b is a variable, it checks if any of them has a reference in the list.
                (f1, j1) = find_reference(a, data)
                (f2, j2) = find_reference(b, data)
                # If that is the case, it fetches the reference value.
                if f1:
                    a = data[j1]
                if f2:
                    b = data[j2]
                # Below, the program converts the inputs a and b into suitable data types (either int or bool)
                if type(a) is str:
                    if (a == 'True'):
                        a = True
                    elif (a == 'False'):
                        a = False 
                    elif a.isdigit(): # isdigit() checks if a is a numeric value. 
                        a = int(a)
                    else: 
                        print(f"INVALID INPUT (line {k}): the variable {line[2]} is not defined")
                        breaker = True
                if type(b) is str:
                    if (b == 'True'):
                        b = True
                    elif (b == 'False'):
                        b = False 
                    elif b.isdigit(): # isdigit() checks if a is a numeric value. 
                        b = int(b)
                    else: 
                        print(f"INVALID INPUT (line {k}): the variable {line[4]} is not defined")
                        w = -1
                # Now, before storing the values of a and b in data, it checks if they are already in the list.
                (found1, i1) = inList(data, a) 
                # If they are not, they are added to the data list 
                if not found1:
                    data.append(a)
                (found2, i2) = inList(data, b)
                if not found2:
                    data.append(b)
                # After this, the program performs string comparison on the operator in order to evaluate the expression. 
                if line[3] == '+':
                    if type(a) is int and type(b) is int: # it first checks if the input type is correct for the operator type 
                        ans = a + b # It then evaluates the expression
                        (found, i) = inList(data, ans) # It checks if the answer is already present in the data list
                        d = find_value(found, i, ans, data) # It then uses find_value() to fetch the reference address for the variable 
                        add_to_list(var, d, data) # Finally, it adds it to the list using add_to_list()
                    else: # if the types of the operator and of the input do not match, it gives an error. 
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                # The same thing is done for the rest of the cases 
                elif line[3] == '-':
                    if type(a) is int and type(b) is int:
                        ans = a - b
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == '*':
                    if type(a) is int and type(b) is int:
                        ans = a*b
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        breaker = True
                elif line[3] == '/':
                    if type(a) is int and type(b) is int:
                        ans = a//b
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == '>':
                    if type(a) is int and type(b) is int:
                        ans = (a>b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == '<':
                    if type(a) is int and type(b) is int:
                        ans = (a<b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        breaker = True
                elif line[3] == '>=':
                    if type(a) is int and type(b) is int:
                        ans = (a >= b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == '<=':
                    if type(a) is int and type(b) is int:
                        ans = (a <= b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == '==':
                    ans = (a == b)
                    (found, i) = inList(data, ans)
                    d = find_value(found, i, ans, data)
                    add_to_list(var, d, data)
                elif line[3] == '!=':
                    ans = (a != b)
                    (found, i) = inList(data, ans)
                    d = find_value(found, i, ans, data)
                    add_to_list(var, d, data)
                
                elif line[3] == 'and':
                    if type(a) is bool and type(b) is bool:
                        ans = (a and b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                elif line[3] == 'or':
                    if type(a) is bool and type(b) is bool:
                        ans = (a or b)
                        (found, i) = inList(data, ans)
                        d = find_value(found, i, ans, data)
                        add_to_list(var, d, data)
                    else:
                        print(f"INVALID INPUT (line {k}): Please enter the correct type")
                        w = -1
                else:
                    print(f"INVALID INPUT (line {k}): Please use a valid binary operator")
                    w = -1
            elif n==4:
                # The length is 4 when a unary operator is used 
                # The unary operator can be either '-' or 'not' 
                c = line[3]
                if c[-1] == '\n':
                    c = c[:-1]
                else:
                    c = c 
                # This is done to remove the last character '\n' that is stored in the list by default.
                # If this character is not removed, then the equality conditions do not hold.
                (f3, j3) = find_reference(c, data) # If c is a variable it obtains the value of c from the data list
                # It then assigns that value to c.
                if f3:
                    c = data[j3]
                # Checking the input and converting it to suitable data type
                if type(c) is str:
                    if (c == 'True'):
                    # If the input has either true or false, then it is to be converted to a bool.
                        c = True
                    elif (c == 'False'):
                        c = False 
                    elif c.isdigit():
                    # Otherwise, if input is a number, it has to be converted to an integer
                        c = int(c)
                    else:
                    # if input is neither a boolean value, nor an integer, it is an invalid input. So, the loop breaks. 
                        print(f"INVALID INPUT (line {k}): the variable '{line[3]}' is not defined")
                        w = -1
                # Now, it checks if c is already in the list. If it isn't, it appends it to the list.
                (found3, i3) = inList(data, c)
                
                if not found3:
                    data.append(c)

                # Evaluating the expression:
                if type(c) is bool and line[2] == 'not':
                    # If the type is bool, then the operator used will be 'not'. So, answer willl be 'not c'
                    ans = not c
                    (found, i) = inList(data, ans)
                    d = find_value(found, i, ans, data)
                    add_to_list(var, d, data)
                elif type(c) is int and line[2] == '-':
                    # If the type is int, then the operator used will be '-'. So, the answer will be the additiive inverse. 
                    ans = (-1)*c
                    (found, i) = inList(data, ans)
                    d = find_value(found, i, ans, data)
                    add_to_list(var, d, data)
                else:
                    print(f"INVALID INPUT (line {k}): Please enter the correct input")
                    w = -1

            elif n == 3:
                # the length is 3 when a value is directly assigned 
                e = line[2]
                if e[-1] == '\n':
                    e = e[:-1]
                else:
                    e = e 
                # This is done to remove the last character '\n' that is stored in the list by default.
                # If this character is not removed, then the equality conditions do not hold.

                (f4, j4) = find_reference(e, data) # It looks for the reference address that the variable is poitning to
                if f4:
                    # if it is a variable, then it assigns e the value that the vatiable is referencing.
                    e = data[j4]
                
                # Checking the input and converting it to suitable data type
                if type(e) is str:
                    if (e == 'True'):
                    # If the input has either true or false, then it is to be converted to a bool.
                        e = True
                    elif (e == 'False'):
                        e = False 
                    elif e.isdigit():
                    # Otherwise, if input is a number, it has to be converted to an integer
                        e = int(e)
                    else:
                    # if input is neither a boolean value, nor an integer, it is an invalid input. So, the loop breaks. 
                        print(f"INVALID INPUT (line{k}): the variable '{line[2]}' is not defined")
                        w = -1

                ans = e # When the length is 3, input is of the form (variable = (value)). So, the answer is simply e. 
                (found, i) = inList(data, ans) # It then checks to see if the ans is already in the 'data' list. 
                d = find_value(found, i, ans, data) # It then finds the position where the ans is present or adds it if need be
                add_to_list(var, d, data) # finally, it appends the variable and its reference address to the 'data' list. 
            elif n == 2: 
                # The input statement cannot have length '2'. If it does, then that means it is incomplete. 
                # in such a case, the loop is broken and an error is shown.
                print(f"INVALID INPUT (line {k}): Please enter complete statement")
                w = -1
            elif n == 1:
                w = -1
            else:
                print(f"INVALID INPUT (line {k}): Please use only one operator")
                w = -1
            w = w+1
            """
            CRUDE TIME COMPLEXITY ANALYSIS:

            Each iteration takes O(n) time complexity, where 'n' is the length of the data list.
            Let 'p' be the number of lines in the input file.
            Then, we know that the length of the data list depends linearly on p.
            So, the total time complexity will be the summation of the time complexities for each iteration for all 'p' iterations
            Hence, time complexity is O(p^2)
            """
        elif self.type == 'BLE':
            a = self.operands[0]
            b = self.operands[1]
            # Conversion of the operands to correct data type
            if a.isdigit():
                a1 = int(a)
            else:
                (a0, a1) = find_reference(a, data)
                a1 = data[a1]
            
            if b.isdigit():
                b1 = int(b)
            else:
                (b0, b1) = find_reference(b, data)
                b1 = data[b1]
            if a1 <= b1:
                # the interpreter will skip the rest of the loop and directly move to the end
                # basically it'll have to go to the end value of the loop 
                w = self.end + 1 
            else:
                # the interpreter evaluates the next statement in the loop
                w = w+1
        elif self.type == 'BLT':
            a = self.operands[0]
            b = self.operands[1]
            if a.isdigit():
                a1 = int(a)
            else:
                (a0, a1) = find_reference(a, data)
                a1 = data[a1]
            
            if b.isdigit():
                b1 = int(b)
            else:
                (b0, b1) = find_reference(b, data)
                b1 = data[b1]
            if a1 < b1:
                w = self.end + self.branch_count
            else:
                w = w+1
        elif self.type == 'BE':
            a = self.operands[0]
            b = self.operands[1]
            if a.isdigit():
                a1 = int(a)
            else:
                (a0, a1) = find_reference(a, data)
                a1 = data[a1]
            
            if b.isdigit():
                b1 = int(b)
            else:
                (b0, b1) = find_reference(b, data)
                b1 = data[b1]
            if a1 != b1:
                w = self.end + 1
            else:
                w = w+1
        elif self.type == 'Branch':
            w = self.start
        else:
            """
            ERROR:
            If the instruction is not one of the fixed types, then it shows an error 
            """
            print("INVALID INSTRUCTION")
            w = -1 # w = -1 acts as a loop breaker 
        return w

    def find_end(self):
        # This function finds the 'end' of the instruction
        # if the instruction is not a loop, then the end is the instruction address itself
        # If the instruction is a loop, then it finds the address where the loop ends
        j = 0
        if self.type != 'ASSIGN' and self.type != 'Branch':
            j = self.address + 1
            while j < len(INSTRUCTION_LIST) and INSTRUCTION_LIST[j].tabs > self.tabs:
                if INSTRUCTION_LIST[j].type == 'Branch':
                    self.branch_count = self.branch_count + 1 # counts the no of branches associated with the instruction
                j = j + 1
            self.end = j
        else:
            self.end = self.address
        return self.end
        """
        TIME COMPLEXITY:
        Max time complexity is O(n) where n is the length of instruction list
        """
    def insert_branch(self):
        # It inserts a 'branch always' statement at the end of the for loop 
        if self.type != 'ASSIGN' and self.type != 'Branch':
            j = self.end # Finds the end of the while loop
            branch = instruction('Branch', self.tabs) # creates the branch instruction
            branch.type = 'Branch' # assigns type
            branch.start = self.address # the 'start' of the branch is assigned as the start of the while loop
            INSTRUCTION_LIST.insert(j, branch)
            # takes time complexity O(n) due to insert function
    def update_address(self):
        self.address = inList(INSTRUCTION_LIST, self)[1] 
        # address of the instruction is updated 
        # Time complexity is O(n) due to inList()


# We also need to keep a count of the number of tabs before the instruction 
    # def method to evaluate the expression
    # def method to turn instruction into evaluable form * not needed now 
    # def method to assign type and to assign destination to the instruction so that it can be stored effectively

lines = [] # initalise to empty list
with open('C:/Users/shrey/OneDrive/Desktop/IIT Delhi Assignments and Coursework/SEMESTER 1/COL 100 (Intro to Comp Science)/Assignments/COL Assignment 6/input_file.txt') as f:
    lines = f.readlines() # read all lines into a list of strings
for statement in lines: # each statement is on a separate line
    token_list = statement.split() # split a statement into a list of tokens
    tabs = 0
    while statement[tabs] == '\t':
        tabs = tabs + 1
    token_list = instruction(token_list, tabs)
    token_list.assign_type() # A type is assigned to the token list
    INSTRUCTION_LIST.append(token_list)
    # using this, all the instructions are stored in the instruction list. 
    # Now, they have to be processed, for which a while loop is needed 
l = len(INSTRUCTION_LIST)
m = 0
while m < l:
    instr = INSTRUCTION_LIST[m]
    instr.update_address()
    e = instr.find_end()
    instr.insert_branch()
    m = m+1
l = len(INSTRUCTION_LIST)
w = 0
while (w < l) and (w >= 0):
    # It reads the instructions sequantially and executes them
    # if an instruction requires branching, then this can be done by changing the value of i accordingly  
    instr = INSTRUCTION_LIST[w]
    instr.update_address() # updates address just to be on the safer side
    e = instr.find_end()
    w = instr.evaluate_stat(w) # evaluates the statement - the method automatically updates the value of w 

print(data)
for stat in INSTRUCTION_LIST:
    print(stat.statement)

print(garbage_collect(data))
print(var_value(data))

"""
TEST CASES AND THEIR OUTPUTS:

TEST CASE 1:
Input:
i = 0
while i < 3:
    i = i + 1
j = 9
Output:
[0, ('i', 4), 1, 2, 3, 9, ('j', 5)]
['i', '=', '0']
['while', 'i', '<', '3:']
['i', '=', 'i', '+', '1']
Branch
['j', '=', '9']
[0, 1, 2]
[('i', 3), ('j', 9)]

TEST CASE 2:
Input:
a = 5
while a > 1:
	a = a - 1
b = 5
Output:
[5, ('a', 2), 1, 4, 3, 2, ('b', 0)]
['a', '=', '5']
['while', 'a', '>', '1:']
['a', '=', 'a', '-', '1']
Branch
['b', '=', '5']
[4, 3, 2]
[('a', 1), ('b', 5)]

TEST CASE 3:

Input:
i = 0
while i < 3:
	j = 0
	while j < 2:
		j = j + 1
	i = i + 1
x = 2

Output:
[0, ('i', 5), ('j', 4), 1, 2, 3, ('x', 4)]
['i', '=', '0']
['while', 'i', '<', '3:']
['j', '=', '0']
['while', 'j', '<', '2:']
['j', '=', 'j', '+', '1']
Branch
['i', '=', 'i', '+', '1']
Branch
['x', '=', '2']
[0, 1]
[('i', 3), ('j', 2), ('x', 2)]
"""