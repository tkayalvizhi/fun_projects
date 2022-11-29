import numpy as np
from DLA import *
from DLA.Particle import Particle

NUM_DIRECTIONS = 4
SAVE = True


class Field(object):

    def __init__(self, dim: int, sticking=1, drift=0.1):

        # if dim < 501:
        #     raise Exception("Dimension of image must be larger than or equal to 501")

        self.M = dim
        self.sticking = sticking
        self.boundary_indices = self.generate_boundary_indices()
        self.matrix = np.zeros(shape=(self.M, self.M))
        self.drift = drift

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
        self.matrix[particle.get_xy()] = 1
        return particle

    def add_to_aggregated(self, particle: Particle):
        self.matrix[particle.get_xy()] = 1

    def get_transition_probabilities(self, particle: Particle):
        trans_prob = np.zeros(4)
        for direction, nbr_pos in enumerate(particle.get_nbr_positions()):
            if self.matrix[nbr_pos] == 0:
                trans_prob[direction] = 1
            else:
                trans_prob[direction] = 0

        return trans_prob

    def get_aggregated_nbr_count(self, particle: Particle):
        count = 0
        for nbr_pos in particle.get_nbr_positions():
            if self.matrix[nbr_pos] == 1:
                count += 1
        return count

    def add_drift(self, trans_prob, particle):
        pos_x, pos_y = particle.get_xy()
        if pos_x < self.C:
            trans_prob[RIGHT] *= (trans_prob[RIGHT] + self.drift)
        else:
            trans_prob[LEFT] *= (trans_prob[LEFT] + self.drift)
        if pos_y < self.C:
            trans_prob[DOWN] *= (trans_prob[DOWN] + self.drift)
        else:
            trans_prob[UP] *= (trans_prob[UP] + self.drift)

        return trans_prob / np.sum(trans_prob)

    def random_step(self, particle: Particle) -> Particle:
        """
        The particle takes a random step to go one pixel UP, DOWN, LEFT or RIGHT.
        Image is toroidally bound.
        :return:
        """
        # if one of the neighbour is already aggregated, do not move there.
        pmf = self.get_transition_probabilities(particle)
        cdf = np.cumsum(self.add_drift(pmf, particle))

        value = np.random.random()

        if value < cdf[0]:
            direction = UP
        elif value < cdf[1]:
            direction = RIGHT
        elif value < cdf[2]:
            direction = DOWN
        else:
            direction = LEFT

        self.matrix[particle.get_xy()] = 0
        particle.move(direction)
        self.matrix[particle.get_xy()] = 1

        return particle

    def random_walk(self, num_iter=40000):
        yield self.matrix, not SAVE
        for _ in range(num_iter):
            particle = self.generate_particle()
            self_aggregated = False

            while not self_aggregated:
                yield self.matrix, not SAVE
                particle = self.random_step(particle)

                for _ in range(self.get_aggregated_nbr_count(particle)):
                    if np.random.random() < self.sticking:
                        self.add_to_aggregated(particle)
                        self_aggregated = True
                        break
            yield self.matrix, SAVE

    def show(self):
        print(self.matrix)
