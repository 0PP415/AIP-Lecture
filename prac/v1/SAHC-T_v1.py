from tsp import * 

def steepestAscent(p):
    """
    핵심 탐색 알고리즘입니다.
    p를 받아 Local Minimum을 찾을 때까지 탐색합니다.
    """
    # 1. tsp.randomInit() 호출 (무작위 경로 생성)
    current = randomInit(p) 
    # 2. tsp.evaluate() 호출 (경로 총합 계산)
    valueC = evaluate(current, p)

    while True:
        # 3. SAHC-T의 mutants() 호출
        neighbors = mutants(current, p)

        # 4. 최고 이웃 선택
        successor, valueS = bestOf(neighbors, p)

        # 5. (최소화) 종료 조건
        if valueS >= valueC:
            break
        # 6. (이동)
        else:
            current = successor
            valueC = valueS

    # 7. 최종 해와 그 값을 반환
    return current, valueC

def bestOf(neighbors, p):
    """
    이웃 리스트(neighbors)를 받아 가장 좋은(값이 작은)
    이웃(bestNeighbor)과 그 값(bestValue)을 반환합니다.
    """
    bestNeighbor = neighbors[0]
    bestValue = evaluate(neighbors[0], p) # tsp.evaluate() 호출

    for neighbor in neighbors:
        nowValue = evaluate(neighbor, p) # tsp.evaluate() 호출
        
        if (nowValue < bestValue): 
            bestNeighbor = neighbor
            bestValue = nowValue

    return (bestNeighbor, bestValue)

def mutants(current, p):
    """
    무작위 (i, j) 쌍을 n번 뽑아 n개의 이웃을 생성합니다.
    """
    n = p[0] # 도시 수
    neighbors = []
    count = 0
    triedPairs = []
    
    while count <= n: # n개의 이웃을 생성할 때까지
        
        # 무작위 인덱스 2개(i, j)를 뽑아 정렬
        i, j = sorted([random.randrange(n) for _ in range(2)])
        
        # (i, j)가 유효하고, 시도한 적이 없다면
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            
            # tsp.inversion()을 호출해 이웃 생성
            curCopy = inversion(current, i, j) 
            count += 1
            neighbors.append(curCopy)
            
    return neighbors

def displaySetting():
    """
    SAHC-T 알고리즘 설정을 출력합니다.
    """
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

def main():
    """
    프로그램의 메인 실행 함수입니다.
    """
    # 1. tsp.createProblem() 호출
    p = createProblem() 
    if p[0] is None:
         print("Problem creation failed. Exiting.")
         return

    # 2. SAHC-T의 steepestAscent() 호출
    solution, minimum = steepestAscent(p)

    # 3. tsp.describeProblem() 및 SAHC-T의 displaySetting() 호출
    describeProblem(p)
    displaySetting()

    # 4. tsp.displayResult() 호출
    displayResult(solution, minimum)

if __name__ == "__main__":
    main()
