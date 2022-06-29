class Axis:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def zero():
        return Axis(0, 0)
    
    def to_list(self):
        return [self.x, self.y]