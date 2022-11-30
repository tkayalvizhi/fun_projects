class Particle:
    def __init__(self, x, y, M):
        self.M = M
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def get_index(self):
        return self.y * self.M + self.x

    def move(self, direction: int):
        if direction == UP:
            self.y = (self.y - 1) % self.M
        elif direction == RIGHT:
            self.x = (self.x + 1) % self.M
        elif direction == DOWN:
            self.y = (self.y + 1) % self.M
        elif direction == LEFT:
            self.x = (self.x - 1) % self.M
        else:
            raise Exception("Invalid direction")

    @classmethod
    def from_index(cls, index, M):
        return cls(index % M, index // M, M)