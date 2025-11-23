from setup import Setup


"""
HillClimbing 클래스는 구현이 완료되었으며, 더 이상 수정할 것이 없습니다.
There is nothing to edit/modify for the HillClimbing class!
"""
class HillClimbing(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0        # Problem type
        self._limitStuck = 100 # Max evaluations with no improvement

    def setVariables(self, pType):
        self._pType = pType

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size:", self._delta)

    def run(self):
        pass


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

    def run(self, p):
        ###
        # Your code goes here!
        # 기존의 steepestAscent 함수 활용
        ...?

    def bestOf(self, neighbors, p):
        ###
        # Your code goes here!
        # 기존의 bestOf 함수 활용
        ...?


class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))

    def run(self, p):
        ###
        # Your code goes here!
        # 기존의 firstChoice 함수 활용
        ...?


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        ###
        # Your code goes here!
        # 기존의 gradientDescent 함수 활용
        ...?