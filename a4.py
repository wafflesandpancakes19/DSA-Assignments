import random
import math
from re import X

# theoretical space and time complexities will be assessed
#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]
# the time complexity for this function is ignored in the rest of the complexity analysis

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

def convertStr(p):
	# SPECIFICATION: function converts a given character 'p' to the corresponding number from 0 to 25
	# TIME COMPLEXITY = O(1)
	# SPACE COMPLEXITY: O(1) since it will be less than the constant log(26)
	return (ord(p)-65)
# It is working!

def findSum(t, q):
	# SPECIFICATION: This function will find the bijective mapping for the given input string p
	m = len(t)
	i = 0
	sum = 0
	while i<m:
		sum = (convertStr(t[i]) + 26*sum)%q
		i = i+1
	# TIME COMPLEXITY: This is a while loop, which will run m times, performing O(logq) operations since the time for performing
	# arithmetic on a q bit no. is O(logq)
	# Therefore, time complexity is O(mlogq)
	# Since finally, a single no. between 0 and q-1 will be returned, SPACE COMPLEXITY = O(log(q))
	return (sum)

def findWildcard(p):
	# SPECIFICATION: This function will find and return the index of the wildcard in the given string p
	# TIME COMPLEXITY: the worst case time complexity is O(m), when it has to iterate over the entire string
	# SPACE COMPLEXITY: since the variables m and i are being stored, space complexity will be O(logm)
	m = len(p)
	i = 0
	while i<m:
		if p[i] == '?':
			return i
		i = i+1

def findWildSum(t, p, q):
	# SPECIFICATION: This function will find the bijective mapping for the given input string p
	m = len(t)
	i = 0
	sum = 0
	j = findWildcard(t)	#we find the index which has the wildcard
	# The required sum is calculated using iteration
	while i<m:
		if i == j:
			sum = (26*sum)%q	# basic arithmetic operations are being performed, hence, Time complexity is O(log(q))
		else:
			sum = (convertStr(p[i])+1 + 26*sum)%q	# basic arithmetic is being performed, hence time complexity is O(log(q))
		i = i+1
	# TIME COMPLEXITY: This is a while loop, which will run m times, performing O(logq) operations
	# Therefore, time complexity is O(mlogq)
	# SPACE COMPLEXITY: 
	# m, i and sum are being maintained here
	# m and i both will take O(logm) space and sum will take O(logq) space because of modulo q
	# therefore, space complexity can be taken as O(logm+logq)
	return (sum)


#print(findSum('ABCD', 1001))

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	"""
	REASONING/PROOF:
	1. an error will turn up when f(p)modq = f(t)modq but f(p)!=f(t)
	2. in such a scenario, let f(p)modq = f(t)modq = r
	3. then, f(p) = a*q+r and f(t) = b*q+r
	4. this means that f(p)-f(t) = q*(a-b) and is therefore divisible by q 
	5. we know that the maximum number of primes that will divide this are log2(f(p)-f(t))
	6. the maximum possible value of f(p)-f(t) is 26*(26**(m-1)) = 26**m
	7. the total no. of primes less than N are N/2log2(N)
	8. So, probability of error (eps) >= log2(26**m)/(N/2*log2(N))
	9. rearranging, we get, (N/log2(N)) >= 2*(m/eps)log2(26)
	10. we now need to find an N that satisfies this inequality
	11. for this, we will use binary search 
	12. the lower bound will be 2 and the upper bound can be taken as the square of the rhs
	"""
	low = 2
	a = 2*(m/eps)*math.log2(26)
	high = a*a
	while high>=low:
		mid = (high+low)//2
		ab = mid/(math.log2(mid))
		if ab<a:
			low = mid+1
		elif ab>a:
			high = mid-1
		else:
			return int(mid)
	"""
	TIME COMPLEXITY ANALYSIS:
	this is the standard algorithm for binary search. Therefore, time complexity is O(log(a-2)), 
	where the expression for q has been given in the code itself 
	"""
	return int(mid) 

print(findN(0.03,100))#/math.log2(findN(0.03,100)))
print(findN(0.4,3))#/math.log2(findN(0.4,3)))
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	# can be implemented by simply adjusting the string value to compute x[i+1] from x[i]
	# we first compute the function for the pattern (hence, compute f(p))
	# this is done using a helper function
	ans = []	# this is the list of indices that will be returned 
	m = len(p)
	#print(m)
	n = len(x)
	h = (26**(m-1))%q # takes O(logq) space
	fp = findSum(p, q)	# It is calculated in O(mlogq) time and takes O(logq) space
	fx = findSum(x[:m], q)	# this is the value of the function for x. It is calculated in O(mlogq) time and takes O(logq) space
	i = 0
	if m==0:
		return ans
	elif m ==1:
		while i<n-m:
			if fp==fx:
				ans.append(i)
			fx = (convertStr(x[i])+1)%q
			i = i+1
		if fp == fx:
			ans.append(i)
		return ans
	else:
		while i < n-m:	#since i can go upto n-m, we can say that it takes O(logn) space 
			if fp == fx:
				ans.append(i)
			fx = 26*(fx - h*convertStr(x[i]))	#takes O(logq) time since arithmetic operations are being performed and O(logq) space because modq is being stored
			fx = (fx + convertStr(x[i+m])%q)%q   #takes O(logq) time since arithmetic operations are being performed and O(logq) space because modq is being stored
			i = i+1
		if fp == fx:
			ans.append(i)
	"""
	FINAL TIME COMPLEXITY:
	1. we start by evaluating the function for the pattern, leading to a complexity of O(mlogq)
	2. Then, a loop is run with O(logq) operations performed in every iteration and with approx n iterations, leading to O(nlogq)
	3. hence, total time complexity becomes O((m+n)logq) 
	"""
	"""
	SPACE COMPLEXITY:
	1. assuming the output list takes k space, we have O(k)
	2. the iterator i takes O(logn) space 
	3. the variables fp and fx both take O(logq) space
	4. Therefore, the total space complexity becomes O(logn + logq + k)
	"""
	return ans

# Return sorted list of starting indices where p matches x

def modPatternMatchWildcard(q,p,x):
	ans = []	# this list will finally be returned and will contain the starting indices of the patterns
	m = len(p)
	n = len(x)
	h = (26**(m-1))%q	# takes O(logq) space
	j = findWildcard(p)	# takes O(logq) space and O(m) time
	hj = (26**(m-j))%q	# takes O(logq) space and O(m) time 
	hjj = (26**(m-j-1))%q # takes O(logq) space and O(m) time 
	fp = findWildSum(p, p, q)	# takes O(logq) space and O(mlogq) time
	fx = findWildSum(p, x[:m], q)	# takes O(logq) space and O(mlogq) time
	i = 0
	if m == 0:
		return []
	elif m == 1:
		while i<n-m:
			if fp==fx:
				ans.append(i)
			fx = (convertStr(x[i])+1)%q
			i = i+1
		if fp == fx:
			ans.append(i)
		return ans
	if m == 2:
		while i<n-m:	# i will end up taking O(logn) space 
			if fp == fx:
				ans.append(i)
			#print(fp, fx)
			fx = findWildSum(p, x[i+1:i+3], q)	
			i = i+1
		if fp == fx:
			ans.append(i)
		return ans
	else:
		while i < n-m:	# i will end up taking O(logn) space 
			if fp == fx:
				ans.append(i)
			#print(f"x[i], x[i+j], x[i+j+1], x[i+m]: {x[i]}, {x[i+j]}, {x[i+j+1]}, {x[i+m]}")
			"""
			LOGIC FOR CONVERSION OF F(X[I]) TO F(X[I+1]):
			1. because of how the function is constructed, the element at the jth position will be zero
			2. However, now, everything would be shifted by 1, so x[i+j-1]*(26**(m-j-1)) will be added 
			3. However, now, the successor of the element initially at the wildcard position will have to be subtracted
			4. Therefore, fx - x[i+j]*(26**(m-j-2))
			5. apart from this, the first term will have to be subtracted and the last term will have to be added after shifting
			"""
			fx = 26*(fx - h*(convertStr(x[i])+1))	#takes O(logq) time since arithmetic operations are being performed and O(logq) space because modq is being stored
			fx = (fx + (convertStr(x[i+m])+1)%q+hj*(convertStr(x[i+j])+1)- hjj*(convertStr(x[i+j+1])+1))%q	#takes O(logq) time since arithmetic operations are being performed and O(logq) space because modq is being stored
			i = i+1
		#print(fx)
		if fp == fx:
			ans.append(i)
		"""
		FINAL TIME COMPLEXITY:
		1. we start by evaluating the function for the pattern, leading to a complexity of O(mlogq)
		2. Then, a loop is run with O(logq) operations performed in every iteration and with approx n iterations, leading to O(nlogq)
		3. hence, total time complexity becomes O((m+n)logq)
		"""
		"""
		SPACE COMPLEXITY:
		1. assuming the output list takes k space, we have O(k)
		2. the iterator i takes O(logn) space 
		3. the variables fp and fx both take O(logq) space
		4. Therefore, the total space complexity becomes O(logn + logq + k)
		"""
		return ans
"""
print(modPatternMatch(1000000007, 'CD', 'ABCDE'))
print(modPatternMatch(1000000007, 'AA', 'AAAAA'))
print(modPatternMatchWildcard(1000000007, 'D?', 'ABCDE'))
print(modPatternMatchWildcard(1000000007, '?A', 'ABCDE'))
print(modPatternMatch(2, 'AA', 'ACEGI'))
print(modPatternMatchWildcard(1000000007, 'CD?F', 'ABCDEF'))
print(modPatternMatchWildcard(22343, 'AZEJVWQBAMDDO?JYS', 'CPDKNHHFVRJSPSKCG'))
"""