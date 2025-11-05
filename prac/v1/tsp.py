import random
import math

NumEval = 0

def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    
    # First line is number of cities
    numCities = int(infile.readline()) # [1] 첫 줄을 읽어 정수로 변환
    locations = []
    
    # The rest of the lines are locations
    line = infile.readline() 
    while line != '':
        # [2] (x, y) 문자열을 튜플로 변환 (eval 사용)
        locations.append(eval(line)) 
        line = infile.readline()
        
    infile.close()
    
    # [3] 거리 행렬 계산
    table = calcDistanceTable(numCities, locations)
    
    # [4] (도시 수, 위치 리스트, 거리 행렬) 튜플 반환
    return numCities, locations, table

def calcDistanceTable(numCities, locations):
    pass

def randomInit(p):
    # p[0]에서 도시 수(n)를 가져옴
    n = p[0] 
    # 0부터 n-1까지의 숫자 리스트 생성 (예: [0, 1, 2, 3])
    init = list(range(n)) 
    # 리스트를 무작위로 섞음 (예: [2, 0, 3, 1])
    random.shuffle(init) 
    return init

def evaluate(current, p):
    pass

def inversion (current, i, j): # Perform inversion
    curCopy = current[:]
    while i < j:
        # [1] i번째와 j번째 원소를 교환
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i] 
        i += 1
        j -= 1
    return curCopy

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        # [1] 도시 좌표를 12칸 공백에 오른쪽 정렬하여 출력
        print("{0:>12}".format(str(locations[i])), end = '')
        # [2] 5개(i=4, 9, 14...) 출력할 때마다 줄바꿈
        if i % 5 == 4: 
            print()

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    # [1] tenPerRow 함수를 호출해 방문 순서를 10개씩 출력
    tenPerRow(solution) 

    # [2] 최소 거리를 반올림(round)하여 출력
    print("Minimum tour cost: {0,}".format(round(minimum))) 
    print()

    # [3] 총 평가 횟수(NumEval) 출력
    print("Total number of evaluations: {0,}".format(NumEval))

def tenPerRow(solution):
    # 1. solution 리스트(방문 순서)의 길이만큼 루프
    for i in range(len(solution)):
        # 2. 도시 ID를 5칸 공백에 오른쪽 정렬하여 출력
        #    end=''는 줄바꿈을 하지 않음
        print("{0:>5}".format(solution[i]), end='')
        
        # 3. 10개(i=9, 19, 29...)를 출력할 때마다 줄바꿈
        if i % 10 == 9: 
            print()
