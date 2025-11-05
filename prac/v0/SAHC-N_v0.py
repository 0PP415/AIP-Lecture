import random
import math

NumEval = 0
DELTA = 0.01 # Mutation step size

def createProblem():
    file_name = input("Enter the file name of a function: ")

    expr = ""
    var = []
    low = []
    max = []
    with open(file_name, 'r') as f:
        expr = f.readline().strip()
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                var.append(parts[0])
                low.append(float(parts[1]))
                max.append(float(parts[2]))
    domain = (var, low, max)
    return (expr, domain)

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

# SA's Helper Functions
def randomInit(p):
    domain = p[1]
    var = domain[0]
    low = domain[1]
    max = domain[2]

    init_solution = []
    for i in range(len(var)):
        value = random.uniform(low[i], max[i])
        init_solution.append(value)

    return init_solution

def mutants(current, p):
    neighbors = []
    num_vars = len(p[1][0])
    for i in range(num_vars):
        neighbors.append(mutate(current, i, DELTA, p))
        neighbors.append(mutate(current, i, -DELTA, p))
    return neighbors

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    # 1. 원본이 아닌 복사본을 수정하기 위해 리스트를 복사
    curCopy = current[:]

    # 2. 문제 p에서 domain 정보를 가져옴
    domain = p[1]                 # p[1] is domain: [VarNames, low, up]

    # 3. i번째 변수의 최소(l) / 최대(u) 범위를 가져옴
    l = domain[1][i]              # Lower bound of i-th
    u = domain[2][i]              # Upper bound of i-th

    # 4. (핵심) i번째 값을 d만큼 변경한 값이 여전히 범위(l~u) 내에 있는지 확인
    if l <= (curCopy[i] + d) <= u:
        # 5. 범위 내라면, 복사본의 값을 변경
        curCopy[i] += d

    # 6. 변경된 복사본 (mutant)을 반환
    return curCopy

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    
    # 1. 평가 횟수를 카운트하기 위해 전역 변수 NumEval을 1 증가시킴
    global NumEval
    NumEval += 1

    # 2. p에서 '수식'과 '변수 이름 리스트'를 가져옴
    expr = p[0] 
    varNames = p[1][0] 

    # 3. [수정] 변수 값을 저장할 딕셔너리(scope) 생성
    var_scope = {}

    # 4. [선택] 수식에 math.sqrt() 등이 있을 경우를 대비해 math 모듈 추가
    var_scope['math'] = math 

    # 5. [수정] exec() 대신 딕셔너리에 'x1' = 3.5 처럼 값을 직접 할당
    for i in range(len(varNames)):
        var_scope[varNames[i]] = current[i]
    
    # 6. [수정] eval() 함수에 딕셔너리를 전달
    # eval()은 expr을 계산할 때 x1, x2 같은 변수를 var_scope에서 찾아 사용함
    return eval(expr, var_scope)

def bestOf(neighbors, p):
    bestNeighbor = neighbors[0]
    bestValue = evaluate(neighbors[0], p)

    for neighbor in neighbors:
        nowValue = evaluate(neighbor, p)
        if (nowValue < bestValue):
            bestNeighbor = neighbor
            bestValue = nowValue

    return (bestNeighbor, bestValue)

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])  # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i]))
    
def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    # 1. solution을 coordinate 함수로 변환(반올림, 튜플)하여 출력
    print(coordinate(solution)) # Convert list to tuple
    
    # 2. minimum 값을 소수점 3자리까지 포맷하여 출력
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    
    # 3. 전역 변수 NumEval (총 평가 횟수)를 포맷하여 출력
    print("Total number of evaluations: {0}".format(NumEval))

def coordinate(solution):
    # 1. 리스트의 각 값을 소수점 3째 자리에서 반올림(round)함
    c = [round(value, 3) for value in solution]
    
    # 2. 반올림된 리스트를 튜플(tuple)로 변환하여 반환
    return tuple(c) # Convert the list to a tuple

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