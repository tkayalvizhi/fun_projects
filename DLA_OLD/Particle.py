from DLA_OLD import *


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Particle:
    def __init__(self, x, y, M):
        self.M = M
        self.pos = Position(x, y)

    def get_xy(self):
        return self.pos.x, self.pos.y

    def get_position(self):
        return self.pos

    def get_index(self):
        return self.pos.y * self.M + self.pos.x

    def move(self, direction: int):
        if direction == UP:
            self.pos.y = (self.pos.y - 1) % self.M
        elif direction == RIGHT:
            self.pos.x = (self.pos.x + 1) % self.M
        elif direction == DOWN:
            self.pos.y = (self.pos.y + 1) % self.M
        elif direction == LEFT:
            self.pos.x = (self.pos.x - 1) % self.M
        else:
            raise Exception("Invalid direction to move()")

    @classmethod
    def from_index(cls, index, M):
        return cls(index % M, index // M, M)

    def get_nbr_positions(self):
        return [
            Position(self.pos.x, (self.pos.y - 1) % self.M),
            Position((self.pos.x + 1) % self.M, self.pos.y),
            Position(self.pos.x, (self.pos.y + 1) % self.M),
            Position((self.pos.x - 1) % self.M, self.pos.y),
        ]
