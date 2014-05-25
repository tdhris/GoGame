class Position:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        pass

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        pass

    def change_position(self, new_x, new_y):
        self._x = new_x
        self._y = new_y
