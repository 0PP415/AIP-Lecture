from numeric import *

def steepestAscent(p):
    # 1. 임의의 시작점(current)과 그 값(valueC)을 계산
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)

    while True:
        # 2. 모든 이웃(neighbors)을 생성
        neighbors = mutants(current, p)

        # 3. 이웃 중 최고(successor)와 그 값(valueS)을 찾음
        successor, valueS = bestOf(neighbors, p)

        # 4. (종료 조건) 최고 이웃이 현재보다 나쁘거나 같으면 멈춤
        if valueS >= valueC:
            break
        # 5. (이동) 최고 이웃이 더 좋으면 current를 업데이트
        else:
            current = successor
            valueC = valueS

    # 6. 최종 해와 그 값을 반환
    return current, valueC

def mutants(current, p):
    neighbors = []
    num_vars = len(p[1][0])
    for i in range(num_vars):
        neighbors.append(mutate(current, i, DELTA, p))
        neighbors.append(mutate(current, i, -DELTA, p))
    return neighbors

def bestOf(neighbors, p):
    bestNeighbor = neighbors[0]
    bestValue = evaluate(neighbors[0], p)

    for neighbor in neighbors:
        nowValue = evaluate(neighbor, p)
        if (nowValue < bestValue):
            bestNeighbor = neighbor
            bestValue = nowValue

    return (bestNeighbor, bestValue)
    
def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def main():
    # 1. Create an instance of numerical optimization problem
    p = createProblem() # 'p': (expr, domain)

    # 2. Call the search algorithm
    solution, minimum = steepestAscent(p)

    # 3. Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()

    # 4. Report results
    displayResult(solution, minimum)


if __name__ == "__main__":
    main()
