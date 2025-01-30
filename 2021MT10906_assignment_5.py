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


f = open(r'C:\Users\shrey\OneDrive\Desktop\IIT Delhi Assignments and Coursework\SEMESTER 1\COL 100 (Intro to Comp Science)\Assignments\COL Assignment 5\input_file.txt', 'r')
l = [0]
data = []
k = 1
breaker = False # This variable is used to break the loop in case an error is encountered. 

while l and not breaker:
    l = f.readline() # the input document is read line by line 
    line = l.split(" ") # the input is split on the basis of spaces 
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
                break
        if type(b) is str:
            if (b == 'True'):
                b = True
            elif (b == 'False'):
                b = False 
            elif b.isdigit(): # isdigit() checks if a is a numeric value. 
                b = int(b)
            else: 
                print(f"INVALID INPUT (line {k}): the variable {line[4]} is not defined")
                breaker = True
                break
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
                breaker = True # Breaker is changed to True so that the outer loop breaks 
                break
        # The same thing is done for the rest of the cases 
        elif line[3] == '-':
            if type(a) is int and type(b) is int:
                ans = a - b
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '*':
            if type(a) is int and type(b) is int:
                ans = a*b
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '/':
            if type(a) is int and type(b) is int:
                ans = a//b
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '>':
            if type(a) is int and type(b) is int:
                ans = (a>b)
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '<':
            if type(a) is int and type(b) is int:
                ans = (a<b)
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '>=':
            if type(a) is int and type(b) is int:
                ans = (a >= b)
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        elif line[3] == '<=':
            if type(a) is int and type(b) is int:
                ans = (a <= b)
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
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
                breaker = True
                break
        elif line[3] == 'or':
            if type(a) is bool and type(b) is bool:
                ans = (a or b)
                (found, i) = inList(data, ans)
                d = find_value(found, i, ans, data)
                add_to_list(var, d, data)
            else:
                print(f"INVALID INPUT (line {k}): Please enter the correct type")
                breaker = True
                break
        else:
            print(f"INVALID INPUT (line {k}): Please use a valid binary operator")
            breaker = True
            break
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
                breaker = True
                break
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
            # If the type is int, then the operator used will be '-'. So, the answer will be the addtiive inverse. 
            ans = (-1)*c
            (found, i) = inList(data, ans)
            d = find_value(found, i, ans, data)
            add_to_list(var, d, data)
        else:
            print(f"INVALID INPUT (line {k}): Please enter the correct input")
            breaker = True
            break

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
                breaker = True
                break

        ans = e # When the length is 3, input is of the form (variable = (value)). So, the answer is simply e. 
        (found, i) = inList(data, ans) # It then checks to see if the ans is already in the 'data' list. 
        d = find_value(found, i, ans, data) # It then finds the position where the ans is present or adds it if need be
        add_to_list(var, d, data) # finally, it appends the variable and its reference address to the 'data' list. 
    elif n == 2: 
        # The input statement cannot have length '2'. If it does, then that means it is incomplete. 
        # in such a case, the loop is broken and an error is shown.
        print(f"INVALID INPUT (line {k}): Please enter complete statement")
        breaker = True 
        break
    elif n == 1:
        breaker = True
        break
    else:
        print(f"INVALID INPUT (line {k}): Please use only one operator")
    k = k+1

    """
    CRUDE TIME COMPLEXITY ANALYSIS:

    Each iteration takes O(n) time complexity, where 'n' is the length of the data list.
    Let 'p' be the number of lines in the input file.
    Then, we know that the length of the data list depends linearly on p.
    So, the total time complexity will be the summation of the time complexities for each iteration for all 'p' iterations
    Hence, time complexity is O(p^2)
    """

print(f"GARBAGE: {garbage_collect(data)}") # A list containing all the 'garbage values' is printed 
# This list contains all the values in 'data' which are not being referenced by any variable  
values = var_value(data)
print(data)
# Printing the values of the variables:
for item in values:
    print(f"{item[0]} = {item[1]}")
    # The operation has time complexity O(m), where 'm' is the number of variables 