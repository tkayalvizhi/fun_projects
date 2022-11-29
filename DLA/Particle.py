from DLA import *
import numpy as np

X = 0
Y = 1


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Particle:
    def __init__(self, x: int, y: int, M: int):
        self.M = M
        self.pos = [x, y]

    def get_xy(self):
        return self.pos[X], self.pos[Y]

    def get_position(self):
        return self.pos

    def move(self, direction: int):
        if direction == UP:
            self.pos[Y] = (self.pos[Y] - 1) % self.M
        elif direction == RIGHT:
            self.pos[X] = (self.pos[X] + 1) % self.M
        elif direction == DOWN:
            self.pos[Y] = (self.pos[Y] + 1) % self.M
        elif direction == LEFT:
            self.pos[X] = (self.pos[X] - 1) % self.M
        else:
            raise Exception("Invalid direction to move()")

    @classmethod
    def from_index(cls, index, M):
        return cls(index % M, index // M, M)

    def get_nbr_positions(self):
        return [(self.pos[X], int((self.pos[Y] - 1) % self.M)),
                (int((self.pos[X] + 1) % self.M), self.pos[Y]),
                (self.pos[X], int((self.pos[Y] + 1) % self.M)),
                (int((self.pos[X] - 1) % self.M), self.pos[Y])]
