class NodePool:
    def __init__(self):
        self._pool = []
        self._history = {}

    def add(self, node):
        if str(node.getPosition()) in self._history:
            return
        self._history[str(node.getPosition())] = True
        self._insort(node)

    def pop(self):
        return self._pool.pop(0)

    def isEmpty(self):
        return len(self._pool) == 0

    def _insort(self, node):
        lo = 0
        hi = len(self._pool)
        while lo < hi:
            mid = (lo+hi)//2
            if node.getFScore() < self._pool[mid].getFScore(): hi = mid
            else: lo = mid + 1
        self._pool.insert(lo, node)