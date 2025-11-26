import random
import math
from setup import Setup


class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0   # Type of problem
        self._numExp = 0  # Total number of experiments

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:
            print("Mutation step size:", self._delta)


class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitStuck = 0  # Max evaluations allowed for no improvement
        self._numRestart = 0         # Number of restart

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2 <= self._aType <= 3:  # First-Choice, Stochastic
            print("Max evaluations with no improvement: {0:,} iterations"
                  .format(self._limitStuck))

    def run(self):
        pass

    def randomRestart(self, p):          # 'alg' is the chosen hill climber
        i = 1
        self.run(p)
        
        bestSolution = p.getSolution()
        bestMinimum  = p.getValue()

        while i < self._numRestart:
            self.run(p)

            newSolution = p.getSolution()
            newMinimum  = p.getValue()
            if newMinimum < bestMinimum:
                bestSolution = newSolution
                bestMinimum  = newMinimum

            i += 1

        p.storeResult(bestSolution, bestMinimum)


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)

        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS

        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)

        for neighbor in neighbors:
            nowValue = p.evaluate(neighbor)
            if (nowValue < bestValue):
                best = neighbor
                bestValue = nowValue

        return best, bestValue


class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()   # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1

        p.storeResult(current, valueC)


class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0

        while i < self._limitStuck:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS >= valueC:
                i += 1
            else:
                current = successor
                valueC = valueS
                i = 0

        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]

        largeValue   = max(valuesForMin) + 1
        valuesForMax = [(largeValue - val) for val in valuesForMin]

        total     = sum(valuesForMax)
        randValue = random.uniform(0, total) 

        s = 0
        nextSolution = neighbors[-1]
        nextValue    = valuesForMin[-1]
        for i in range(len(valuesForMax)):
            s += valuesForMax[i]
            if s >= randValue:
                nextSolution = neighbors[i]
                nextValue = valuesForMin[i]
                break

        return nextSolution, nextValue


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        HillClimbing.displaySetting(self)
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        current  = p.randomInit()
        valueC   = p.evaluate(current)

        while True:
            successor = p.takeStep(current, valueC)
            valueS    = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC  = valueS
            else:
                break
        
        p.storeResult(current, valueC)


class MetaHeuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitEval = 0     # Total # evaluations until temination
        self._whenBestFound = 0 # This is actually a result of experiment

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self._limitEval))

    def run(self):
        pass


class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._numSample = 100  # Number of samples used to determine 
                               #  initial temperature
                               
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)

    def run(self, p):
        current  = p.randomInit()
        valueC   = p.evaluate(current)
        currTemp = self.initTemp(p)

        best      = current[:]
        valueBest = valueC

        i = 0
        whenBestFound = 0

        while currTemp > 0 and i < self._limitEval:
            successor = p.randomMutant(current)
            valueS    = p.evaluate(successor)

            dE = valueS - valueC

            if dE < 0:
                current = successor
                valueC  = valueS
            else:
                if random.uniform(0, 1) < math.exp(-dE / currTemp):
                    current = successor
                    valueC  = valueS

            if valueC < valueBest:
                best      = current[:]
                valueBest = valueC 
                whenBestFound = i
            
            i += 1
            currTemp  = self.tSchedule(currTemp)

        self._whenBestFound = whenBestFound
        p.storeResult(best, valueBest)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

