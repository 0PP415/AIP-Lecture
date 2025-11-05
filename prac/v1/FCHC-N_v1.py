from numeric import *

LIMIT_STUCK = 100

def firstChoice(p):
    # 1. (동일) 임의의 시작점(current)과 그 값(valueC)을 계산
    current = randomInit(p) 
    valueC = evaluate(current, p)
    
    # 2. 'stuck' 카운터를 0으로 초기화
    i = 0
    
    # 3. 'stuck' 카운터가 LIMIT_STUCK에 도달할 때까지 반복
    while i < LIMIT_STUCK:
        # 4. (핵심) '무작위' 이웃 하나(successor)를 생성
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        
        # 5. (이동) 이웃이 현재보다 좋으면 (최소화 문제)
        if valueS < valueC:
            current = successor
            valueC = valueS
            # 6. 'stuck' 카운터를 0으로 리셋! (개선 성공)
            i = 0 
        # 7. (실패) 이웃이 현재보다 나쁘면
        else:
            # 8. 'stuck' 카운터를 1 증가
            i += 1
            
    # 9. (종료) 루프가 끝나면(i == LIMIT_STUCK),
    #    최종 찾은 해(Local Minimum)를 반환
    return current, valueC

def randomMutant(current, p):
    num_vars = len(p[1][0])
    idx = random.randrange(num_vars)

    d_sign = random.choice([DELTA, -DELTA])

    randomNeighbor = mutate(current, idx, d_sign, p)
    return randomNeighbor
    
def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing") 
    print()
    print("Mutation step size:", DELTA)

def main():
    # 1. (동일) 문제 생성
    p = createProblem() # 'p': (expr, domain)

    # 2. (변경!) firstChoice 알고리즘 호출
    solution, minimum = firstChoice(p)

    # 3. (동일) 문제 설명 (displaySetting은 수정 필요)
    describeProblem(p)
    displaySetting() # 이 함수는 31페이지에서 수정됩니다.

    # 4. (동일) 결과 리포트
    displayResult(solution, minimum)

if __name__ == "__main__":
    main()
