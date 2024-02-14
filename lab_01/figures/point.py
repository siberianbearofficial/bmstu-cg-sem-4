class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        x = self.x if isinstance(self.x, int) else f'{self.x:.4g}'.strip()
        y = self.y if isinstance(self.y, int) else f'{self.y:.4g}'.strip()
        return f"({x}, {y})"

