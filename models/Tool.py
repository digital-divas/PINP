class Tool:

    def __init__(self):
        # Position on X, Y, Width and Height
        self._position = (0,0,0,0)

    def draw(self, screen, position):
        raise NotImplementedError("The subclass must implement this method.")

    def do_functionality(self, event, canvas, color_picker):
        raise NotImplementedError("The subclass must implement this method.")

    def _is_over_axis_x(self, x_position):
        if x_position >= self._position[0] and x_position <= self._position[0] + self._position[2]:
            return True

        return False

    def _is_over_axis_y(self, y_position):
        if y_position >= self._position[1] and y_position <= self._position[1] + self._position[3]:
            return True

        return False

    def is_over(self, position):
        if self._is_over_axis_x(position[0]) and self._is_over_axis_y(position[1]):
            return True