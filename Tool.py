# Interface
class Tool:

    def draw(self, position):
        return NotImplementedError("The subclass must implement this method.")

    def is_over(self, position):
        return NotImplementedError("The subclass must implement this method.")

    def do_functionality(self):
        return NotImplementedError("The subclass must implement this method.")