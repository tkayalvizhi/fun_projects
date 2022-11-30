import numpy as np
import bisect

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

X_AXIS = True
Y_AXIS = False


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


class Image(object):

    def __init__(self, dim: int):

        # if dim < 501:
        #     raise Exception("Dimension of image must be larger than or equal to 501")

        self.M = dim
        self.aggregated = []
        self.num_edge_pixels = self.M ** 2 - (self.M - 2) ** 2

        self.matrix = np.zeros(shape=(self.M, self.M))

        if self.M % 2 == 0:
            self.C = int(self.M / 2),
        else:
            self.C = int((self.M + 1) / 2)

        self.center = Particle(self.C, self.C, self.M)
        self.add_to_aggregated(self.center)
        self.current = self.generate_particle()

    def random_walk(self, num_steps):
        pass

    def generate_particle(self) -> np.array:
        index = np.random.randint(0, self.num_edge_pixels)
        return Particle.from_index(index, self.M)

    def random_step(self) -> None:
        """
        The particle takes a random step to go one pixel UP, DOWN, LEFT or RIGHT.
        Image is toroidally bound.
        :return:
        """
        direction = np.random.randint(0, 3)
        self.matrix[self.current.get_xy()] = 0
        self.current.move(direction)
        self.matrix[self.current.get_xy()] = 1

    def add_to_aggregated(self, particle: Particle):
        # add to aggregated
        self.binary_search_insert(particle)
        # add to image
        self.matrix[particle.get_xy()] = 1
        pass

    def binary_search_insert(self, particle: Particle):
        pass

    def get_neighbour_indices(self, particle):
        pass

    def is_agregated(self, particle):
        pass
