from NodeBuilder import NodeBuilder
from NodePool import NodePool
from Node import Node

class AStar:
    def __init__(self, heuristic):
        self._nodePool = NodePool()
        self._nodeBuilder = NodeBuilder()
        self._heuristic = heuristic

    def solve(self, position):
        self._bootstrap(position)
        while not self._nodePool.isEmpty():
            currentNode = self._nodePool.pop()
            if currentNode.getHScore() == 0:
                return currentNode.getMoves()
            children = self._nodeBuilder.getChildNodes(currentNode)
            for child in children:
                self._nodePool.add(child)
        return None

    def _bootstrap(self, position):
        node = Node(position, [], self._heuristic)
        self._nodePool.add(node)