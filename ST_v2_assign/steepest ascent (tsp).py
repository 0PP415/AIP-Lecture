from problem import Tsp


def main():
    # Create an object for TSP
    p = Tsp()        # Create a problem object 
    p.setVariables() # Set its class variables (numCities, locations)
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()
    
def steepestAscent(p: Tsp):
    ###
    ### Your code goes here!
    ###
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS

    p.storeResult(current, valueC)

def bestOf(neighbors, p: Tsp):
    ###
    ### Your code goes here!
    ###
    best = neighbors[0]
    bestValue = p.evaluate(best)

    for neighbor in neighbors:
        nowValue = p.evaluate(neighbor)
        if (nowValue < bestValue):
            best = neighbor
            bestValue = nowValue

    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
