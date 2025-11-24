import random
import math

from setup import Setup


class Problem(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._solution = []
        self._value = 0
        self._numEval = 0

        self._pFileName = ''
        self._bestSolution = []
        self._bestMinimum = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._sumOfNumEval = 0
        self._avgWhen = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pFileName = parameters['pFileName']
    
    def getSolution(self):
        return self._solution

    def getValue(self):
        return self._value

    def getNumEval(self):
        return self._numEval

    def resetNumEval(self):
        self._numEval = 0

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

    def storeExpResult(self, results):
        self._bestSolution = results[0]
        self._bestMinimum = results[1]
        self._avgMinimum = results[2]
        self._avgNumEval = results[3]
        self._sumOfNumEval = results[4]
        self._avgWhen = results[5]

    def report(self):
        aType = self._aType
        if 1 <= aType <= 4:  # No need to take average for SA, GA
            print("Average number of evaluations: {0:,}" \
                  .format(round(self._avgNumEval)))
        if 5 <= aType <= 6:
            print("Average iteration of finding the best: {0:,}"
                  .format(self._avgWhen))
        print()
 
    def reportNumEvals(self):
        if 1 <= self._aType <= 4:
            print()
            print("Total number of evaluations: {0:,}"
                  .format(self._sumOfNumEval))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []     # domain as a list
    
    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)

        self._pFileName = parameters["pFileName"]
        varNames = []
        low = []
        up = []
        with open(self._pFileName, 'r') as f:
            self._expression = f.readline().strip()
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    varNames.append(parts[0])
                    low.append(float(parts[1]))
                    up.append(float(parts[2]))
        
        self._domain = [varNames, low, up]

    def randomInit(self): # Return a random initial point as a list
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]

        init = []
        for i in range(len(varNames)):
            value = random.uniform(low[i], up[i])
            init.append(value)

        return init  # list of values

    def evaluate(self, current):
        self._numEval += 1

        varNames = self._domain[0] 
        
        vars = {}    
        vars['math'] = math
        for i in range(len(varNames)):
            vars[varNames[i]] = current[i]

        return eval(self._expression, vars)

    def mutants(self, current):
        neighbors = []
        num_vars = len(self._domain[0])
        for i in range(num_vars):
            neighbors.append(self.mutate(current, i, self._delta))
            neighbors.append(self.mutate(current, i, -self._delta))
        return neighbors     # Return a set of successors

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        mutant = current[:]
        l = self._domain[1][i]     # Lower bound of i-th
        u = self._domain[2][i]     # Upper bound of i-th
        if l <= (mutant[i] + d) <= u:
            mutant[i] += d
        return mutant

    def randomMutant(self, current):
        num_vars = len(self._domain[0])
        i = random.randrange(num_vars)
        d = random.choice([self._delta, -self._delta])

        return self.mutate(current, i, d) # Return a random successor

    def takeStep(self, x, v): # Take gradient and make update if legal
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
        avgMinimum = round(self._avgMinimum, 3)
        print()
        print("Average objective value: {0:,}".format(avgMinimum))
        Problem.report(self)
        print("Best solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self._bestMinimum))
        self.reportNumEvals()

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []       # A list of tuples
        self._distanceTable = []

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)

        self._pFileName = parameters["pFileName"]
        infile = open(self._pFileName, 'r')

        # First line is number of cities
        self._numCities = int(infile.readline())

        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        
        self._distanceTable = self.calcDistanceTable()
        
    def calcDistanceTable(self):
        table = [[0.0] * self._numCities for _ in range(self._numCities)]

        for start in range(self._numCities):
            for dest in range(self._numCities):
                if start != dest:
                    table[start][dest] = math.sqrt((self._locations[start][0] - self._locations[dest][0])**2 + (self._locations[start][1] - self._locations[dest][1])**2)

        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        init = list(range(self._numCities))
        random.shuffle(init)
        return init

    def evaluate(self, current):
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
        mutant = current[:]
        while i < j:
            mutant[i], mutant[j] = mutant[j], mutant[i]
            i += 1
            j -= 1
        return mutant

    def randomMutant(self, current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j:
                mutant = self.inversion(current, i, j)
                break
        return mutant

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
        avgMinimum = round(self._avgMinimum)
        print()
        print("Average tour cost: {0:,}".format(avgMinimum))
        Problem.report(self)
        print("Best tour found:")
        self.tenPerRow()  # Print 10 cities per row
        print("Best tour cost: {0:,}" \
              .format(round(self._bestMinimum)))
        self.reportNumEvals()

    def tenPerRow(self):
        solution = self._bestSolution
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

