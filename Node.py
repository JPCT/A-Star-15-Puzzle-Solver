import copy

class Node:
    def __init__(self, position, moves, heuristic):
        self._position = position
        self._moves = moves
        self._heuristic = heuristic
        self._hScore = None

    def getPosition(self):
        return copy.deepcopy(self._position)

    def getGScore(self):
        return len(self._moves)

    def getHScore(self):
        if self._hScore is None:
            self._hScore = self._heuristic.compute(self)
        return self._hScore

    def getFScore(self):
        return self.getGScore() + self.getHScore()

    def getMoves(self):
        return copy.copy(self._moves)

    def getHeuristic(self):
        return self._heuristic

    def getCoordByValue(self, value):
        i = 0
        for row in self._position:
            j = 0
            for cell in row:
                if cell == value:
                    return [i, j]
                j += 1
            i += 1