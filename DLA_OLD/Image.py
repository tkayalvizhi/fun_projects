import numpy as np

from DLA_OLD.BinarySearchTree import BinarySearchTree
from DLA_OLD.Particle import Particle


class Image(object):

    def __init__(self, dim: int, sticking=1):

        # if dim < 501:
        #     raise Exception("Dimension of image must be larger than or equal to 501")

        self.M = dim
        self.sticking = sticking
        self.aggregated = BinarySearchTree()
        self.boundary_indices = self.generate_boundary_indices()
        self.matrix = np.zeros(shape=(self.M, self.M))

        if self.M % 2 == 0:
            self.C = int(self.M - 1 / 2),
        else:
            self.C = int(self.M / 2)

        self.center = Particle(self.C, self.C, self.M)
        self.add_to_aggregated(self.center)

    def generate_boundary_indices(self):
        with_boundary = np.arange(0, self.M ** 2).reshape((self.M, self.M))
        without_boundary = with_boundary[1:-1, 1:-1]

        return list(set(with_boundary.flatten()).difference(set(without_boundary.flatten())))

    def generate_particle(self) -> np.array:
        index = np.random.choice(self.boundary_indices, 1)
        particle = Particle.from_index(index, self.M)
        self.matrix[particle.get_position()] = 1
        return particle

    def add_to_aggregated(self, particle: Particle):
        self.aggregated.insert(particle.get_position())
        self.matrix[particle.get_xy()] = 1

    def nbrs_aggregated(self, particle: Particle):
        for nbr_pos in particle.get_nbr_positions():
            if self.aggregated.contains(nbr_pos):
                return True
        return False

    def nbr_aggregated(self, nbr, particle: Particle):
        pass

    def random_step(self, particle: Particle) -> None:
        """
        The particle takes a random step to go one pixel UP, DOWN, LEFT or RIGHT.
        Image is toroidally bound.
        :return:
        """
        direction = np.random.randint(0, 3)
        self.matrix[particle.get_xy()] = 0
        particle.move(direction)
        self.matrix[particle.get_xy()] = 1

    def random_walk(self, num_iter):
        for i in range(num_iter):
            particle = self.generate_particle()
            self_aggregated = False
            while not self_aggregated:
                self.show()
                self.random_step(particle)

                if self.nbrs_aggregated(particle) and np.random.random() < self.sticking:
                    self.add_to_aggregated(particle)
                    self_aggregated = True




    def show(self):
        print(self.matrix)
