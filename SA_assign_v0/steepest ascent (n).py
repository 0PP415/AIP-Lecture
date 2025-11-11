import random
import math

from numeric import *

def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def mutants(current, p): ###
    neighbors = []
    num_vars = len(p[1][0])
    for i in range(num_vars):
        neighbors.append(mutate(current, i, DELTA, p))
        neighbors.append(mutate(current, i, -DELTA, p))
    return neighbors     # Return a set of successors


def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(neighbors[0], p)

    for neighbor in neighbors:
        nowValue = evaluate(neighbor, p)
        if (nowValue < bestValue):
            best = neighbor
            bestValue = nowValue
    return best, bestValue


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)


main()
