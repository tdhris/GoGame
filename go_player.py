class GoPlayer():
    def __init__(self, symbol):
        self._symbol = symbol
        self._stones = []
        self._captured_stones = 0

    @property
    def stones(self):
        return self._stones

    @property
    def captured_stones(self):
        return self._captured_stones

    @property
    def symbol(self):
        return self._symbol

    def put_stone(self, position):
        self._stones.append(position)

    def remove_stone(self, stone):
        if stone in self.stones:
            self._stones.remove(stone)

    def capture_stone(self):
        self._captured_stones += 1
