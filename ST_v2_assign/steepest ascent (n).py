from problem import Numeric


def main():
    # Create a Problme object for numerical optimization
    p = Numeric()    # Create a problem object 
    p.setVariables() # Set its class variables (expression, domain)
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def steepestAscent(p: Numeric):
    ###
    ### Your code goes here!
    ###
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS

    p.storeResult(current, valueC)

def bestOf(neighbors, p: Numeric):
    ###
    ### Your code goes here!
    ###
    best = neighbors[0]
    bestValue = p.evaluate(neighbors[0])

    for neighbor in neighbors:
        nowValue = p.evaluate(neighbor)
        if (nowValue < bestValue):
            best = neighbor
            bestValue = nowValue
    return best, bestValue

def displaySetting(p: Numeric):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()
