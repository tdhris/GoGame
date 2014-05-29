class Position:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def change_position(self, new_x, new_y):
        self._x = new_x
        self._y = new_y
