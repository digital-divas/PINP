# Interface
class Tool:

    def draw(self, position):
        raise NotImplementedError("The subclass must implement this method.")

    def is_over(self, position):
        raise NotImplementedError("The subclass must implement this method.")

    def do_functionality(self):
        raise NotImplementedError("The subclass must implement this method.")