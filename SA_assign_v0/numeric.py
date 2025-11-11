import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.

    file_name = input("Enter the file name of a function: ")

    expression = ""
    varName = []
    low = []
    up = []
    with open(file_name, 'r') as f:
        expression = f.readline().strip()
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                varName.append(parts[0])
                low.append(float(parts[1]))
                up.append(float(parts[2]))
    domain = (varName, low, up)
    
    return expression, domain


def randomInit(p): ###
    domain = p[1]

    varName = domain[0]
    low = domain[1]
    up = domain[2]

    init = []
    for i in range(len(varName)):
        value = random.uniform(low[i], up[i])
        init.append(value)

    return init    # Return a random initial point
                   # as a list of values


def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    NumEval += 1

    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    
    vars = {}    
    vars['math'] = math
    for i in range(len(varNames)):
        vars[varNames[i]] = current[i]

    return eval(expr, vars)


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy


def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 


def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))


def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple

