import random
import math

"""
[Problem] class is complete as it is.
Do not need to modify!!!
"""
class Problem:
    def __init__(self):
        self._solution = []
        self._value = 0
        self._numEval = 0

    def setVariables(self):
        pass
    
    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self, current):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []     # domain as a list
        self._delta = 0.01    # Step size for axis-parallel mutation

        self._alpha = 0.01    # Update rate for gradient descent
        self._dx = 10 ** (-4) # Increment for calculating derivative
    

    def setVariables(self):
        ###
        ### Your code goes here!
        ### note: code here should be almost the same as 
        ###       createProblem() you coded before
        ###    
        file_name = input("Enter the file name of a function: ")

        varName = []
        low = []
        up = []
        with open(file_name, 'r') as f:
            self._expression = f.readline().strip()
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    varName.append(parts[0])
                    low.append(float(parts[1]))
                    up.append(float(parts[2]))
        self._domain = (varName, low, up)
        
    def getDelta(self):
        return self._delta

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._dx


    def randomInit(self): # Return a random initial point as a list
        ###
        ### Your code goes here!
        ###
        varName = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]

        init = []
        for i in range(len(varName)):
            value = random.uniform(low[i], up[i])
            init.append(value)

        return init     # Return a random initial point
                        # as a list of values

    def evaluate(self, current):
        ###
        ### Your code goes here!
        ###
        self._numEval += 1

        varNames = self._domain[0] 
        
        vars = {}    
        vars['math'] = math
        for i in range(len(varNames)):
            vars[varNames[i]] = current[i]

        return eval(self._expression, vars)

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        ###
        ### Your code goes here!
        ###
        curCopy = current[:]
        l = self._domain[1][i]     # Lower bound of i-th
        u = self._domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def mutants(self, current):
        ###
        ### Your code goes here!
        ###
        neighbors = []
        num_vars = len(self._domain[0])
        for i in range(num_vars):
            neighbors.append(self.mutate(current, i, self._delta))
            neighbors.append(self.mutate(current, i, -self._delta))
        return neighbors     # Return a set of successors

    def randomMutant(self, current):
        ###
        ### Your code goes here!
        ###
        num_vars = len(self._domain[0])
        i = random.randrange(num_vars)
        d = random.choice([self._delta, -self._delta])

        return self.mutate(current, i, d) # Return a random successor


    def takeStep(self, x, v): # Take gradient and make update if legal
        ###
        ### Your code goes here!
        ###        
        # 1. get the gradient at point 'x'
        grad = self.gradient(x, v)

        # 2. get a new neighbor
        x_new = []
        for i in range(len(x)):
            x_new.append(x[i] - self._alpha * grad[i])

        # 3. check if the new neighbor is within the domain (isLegal?)
        if self.isLegal(x_new):
            #   if yes, return the new neighbor
            return x_new    
        else:
            #   if no, return the current point x
            return x

    def gradient(self, x, v): # 'x' is a vector (list of valules)
        ###
        ### Your code goes here!
        ###
        grad = []   # Calculate partial derivatives and combine them
        for i in range(len(x)):
            # 1. make a copy of x
            x_copy = x[:]
            
            # 2. increase x_copy[i] by dx
            x_copy[i] += self._dx

            # 3. compute the gradient "g" for x_copy = {new_eval - curr_eval} / dx
            new_eval = self.evaluate(x_copy)
            g = (new_eval - v) / self._dx
            grad.append(g)

        return grad

    def isLegal(self, x):   # Check if 'x' is within the domain
        ###
        ### Your code goes here!
        ###
        low = self._domain[1]
        up = self._domain[2]

        # flag = True if all 'x' are within the domain
        # flag = False if any of 'x' is outside the domain
        flag = True
        for i in range(len(x)):
            val = x[i]
            if val < low[i] or val > up[i]:
                flag = False
                break

        # 물론 강의 자료에서는 
        # "벡터 x를 구성하는 모든 xi 각각이, 지정된 범위를 벗어나지 않은 경우" 
        # 를 legal 로 지정하고 있지만 
        # 내가 생각하기엔 한 feature 에 대해서 범위를 벗어난 경우엔 
        # 그 feature 만 범위 내로 되돌리고 나머지 변수는 적용해야 하지 않나 싶다

        return flag


    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)
        print("Search space:")
        varNames = self._domain[0] # domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value))
        Problem.report(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []       # A list of tuples
        self._distanceTable = []


    def setVariables(self):
        ###
        ### Your code goes here!
        ### note: code here should be almost the same as 
        ###       createProblem() before
        ###
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')

        # First line is number of cities
        self._numCities = int(infile.readline())

        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        
        self._distanceTable = self.calcDistanceTable()

    def calcDistanceTable(self):
        ###
        ### Your code goes here!
        ###
        table = [[0.0] * self._numCities for _ in range(self._numCities)]

        for start in range(self._numCities):
            for dest in range(self._numCities):
                if start != dest:
                    table[start][dest] = math.sqrt((self._locations[start][0] - self._locations[dest][0])**2 + (self._locations[start][1] - self._locations[dest][1])**2)

        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        ###
        ### Your code goes here!
        ###
        init = list(range(self._numCities))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        ###
        ### Your code goes here!
        ###
        self._numEval += 1
        cost = 0.0

        for i in range(self._numCities - 1):
            curr = current[i]
            next = current[i+1]
            cost += self._distanceTable[curr][next]

        first = current[-1]
        last  = current[0]
        cost += self._distanceTable[first][last]

        return cost

    def mutants(self, current): # Inversion only
        ###
        ### Your code goes here!
        ###
        neighbors = []
        count = 0
        triedPairs = []
        while count <= self._numCities:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):  ## Perform inversion
        ###
        ### Your code goes here!
        ###
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def randomMutant(self, current): # Inversion only
        ###
        ### Your code goes here!
        ###
        while True:
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy


    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        Problem.report(self)

    def tenPerRow(self):
        solution = self._solution
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

