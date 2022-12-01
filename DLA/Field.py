import numpy as np
from Particle import Particle
from BST import BinarySearchTree
from bisect import bisect_right, bisect_left

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

X = 0
Y = 1

NW, N, NE, E, SE, S, SW, W = (i for i in range(8))

NUM_DIRECTIONS = 8
SAVE = True


class NoValidDirectionError(Exception):
    """Raised when the particle is surrounded by aggregated particles"""
    pass


class Field(object):

    def __init__(self, dim: int, stickiness: float = 1, drift: float = 0.1, max_dist=200, from_edge=False):
        """
        The Field / Image class that dictates the particle movements and aggregation.
        :param dim: (int) width / height of Field -
                    also the number of pixels in each row and column of Field
        :param stickiness: (float) the stickiness factor which determines the probability of a particle aggregating
        :param drift: (float) the factor of drift towards the attractor.
                    0 -> 0% - no drift
                    1 -> 100% more - doubles the probability of moving in the direction of the attractor
                    2 -> 200% more - triples the probability of moving in the direction of the attractor
        :param max_dist: (int) maximum distance away from the nearest aggregated particle
        :param from_edge: (bool) indicator for particle to start random walk from edge of field
        """

        if dim < 101:
            raise Exception("Dimension of image must be larger than or equal to 101")
        if dim % 2 == 0:
            raise Exception("Dimension must be an odd number")
        self.M = dim

        if stickiness < 0 or stickiness > 1:
            raise Exception("stickiness is a probability and must be between 0 and 1")
        self.stickiness = stickiness

        if drift < 0:
            raise Exception("drift must be between 0 and 1")
        self.drift = drift

        self.max_dist = max_dist
        self.from_edge = from_edge

        # matrix indicating if pixel is occupied
        self.matrix = np.zeros(shape=(self.M, self.M))
        self.aggregated_particles = BinarySearchTree()

        # center particle
        self.C = int(self.M / 2)
        self.center = Particle(self.C, self.C, self.M)
        self.matrix[self.center.get_position()] = 1
        self.aggregated_particles.insert(self.center.pos)

        # List of indices along the boundary of the Field.
        self.boundary_indices = self.get_boundary_indices()
        self.scale = 20
        self.count = 0

    def random_step(self, particle: Particle):
        """
        The particle takes a random step in the direction of the nearest aggregated particle
        The direction depends on the transition probability.
        :return: particle after taking a random step
        """
        self.matrix[particle.get_position()] = 0
        unoccupied_pixels = self.get_unoccupied_nbr_pixels(particle)
        nearest = self.aggregated_particles.nearest_neighbour(particle.pos)
        # drift towards nearest aggregated particle
        cdf = np.cumsum(self.add_drift(unoccupied_pixels, particle, nearest))
        # sample a direction from the cumulative distribution function of directions
        direction = bisect_left(cdf, np.random.random())
        # take a step in the direction
        particle.move(direction)
        self.matrix[particle.get_position()] = 1
        return particle

    def random_walk(self, num_iter=40000):
        """
        random walk is a generator function that performs the random walk for the number of iterations given.
        It yields the field matrix after each random step.

        :param num_iter: number of walks to take
        :returns: yields current field matrix (ndarray) and the current iteration (int)
        """
        yield self.matrix, self.count
        while self.count < num_iter:
            particle = self.generate_particle()

            while not self.aggregated_particles.contains(particle.pos):
                yield self.matrix, self.count

                if self.aggregated_particles.nearest_neighbour_dist(particle.pos) > self.max_dist:
                    self.matrix[particle.get_position()] = 0
                    break
                # particle takes a random step
                try:
                    particle = self.random_step(particle)
                except NoValidDirectionError:
                    self.aggregated_particles.insert(particle.pos)
                    continue

                # for each neighbouring aggregated particle,
                # the current particle has "stickiness" probability of getting aggregated
                if np.random.random() < (self.stickiness * self.get_aggregated_nbr_count(particle)):
                    self.aggregated_particles.insert(particle.pos)
            else:
                # if aggregated
                # increment iteration counter
                self.count += 1
                if self.drift > 0.5:
                    self.drift *= np.exp(-0.05 * self.count)
                self.matrix[particle.get_position()] = 1
                print(f"iteration: {self.count}")
                yield self.matrix, self.count

    def get_boundary_indices(self) -> list:
        """
        get_boundary_indices gets the list of boundary pixels for a given M.
        :return: (list) of pixel indices ranging from 0 to M ** 2.
        """
        all_pixels = np.arange(0, self.M ** 2).reshape((self.M, self.M))
        pixels_excluding_boundary = all_pixels[1:-1, 1:-1]

        return list(set(all_pixels.flatten()).difference(set(pixels_excluding_boundary.flatten())))

    def generate_particle(self) -> Particle:
        """
        generate_particle generates a particle at a random pixel in the Field.
        :return: (Particle) a particle.
        """
        if self.from_edge:
            index = np.random.choice(self.boundary_indices, 1)
            particle = Particle.from_index(index, self.M)
        else:
            index = list(np.random.randint(0, self.M, 2))
            dist = self.aggregated_particles.nearest_neighbour_dist(index)
            while dist > self.max_dist or dist < 10:
                index = list(np.random.randint(0, self.M, 2))
                dist = self.aggregated_particles.nearest_neighbour_dist(index)
            particle = Particle(int(index[X]), int(index[Y]), self.M)

        self.matrix[particle.get_position()] = 1
        return particle

    def get_unoccupied_nbr_pixels(self, particle: Particle):
        """
        This function computes the naive probability of a Particle
        landing at either of the 4 neighbouring pixels.
        :param particle: (Particle)
        :return: (list) of probabilites of transitioning to either of the 4 neighbouring pixels in the order
        [UP, RIGHT, DOWN, LEFT]
        """
        nbrs = particle.get_nbr_positions()
        trans_prob = np.array([1 - self.matrix[nbrs[i]] for i in range(NUM_DIRECTIONS)])

        if np.sum(trans_prob) == 0:
            raise NoValidDirectionError
        return trans_prob

    def get_aggregated_nbr_count(self, particle: Particle):
        """
        get_aggregated_nbr_count gets the number of neighbours around a given particle that are already aggregated.
        :param particle: (Particle)
        :return: (int) count
        """
        nbrs = particle.get_nbr_positions()
        aggregated_nbrs = np.array([self.matrix[nbrs[i]] for i in range(NUM_DIRECTIONS)])

        return int(np.sum(aggregated_nbrs))

    def add_drift(self, trans_prob, particle: Particle, attractor: list = None):
        """
        a drift towards the center, speeds up the aggregation of particles.
        With drift the directions pointing towards the center of the field are preferred more.
        :param attractor:
        :param trans_prob: (list) of probabilites of transitioning to the 8 neighbouring pixels
        :param particle: (Particle)
        :return: transition probabilites with drift.
        """
        if attractor is None:
            attractor = self.center.pos
        pos = particle.get_position()

        if pos[X] < attractor[X]:
            # push towards east
            trans_prob[[NE, E, SE]] += trans_prob[[NE, E, SE]] * self.drift
        else:
            # push towards west
            trans_prob[[NW, W, SW]] += trans_prob[[NW, W, SW]] * self.drift

        if pos[Y] < attractor[Y]:
            # push towards south
            trans_prob[[SE, S, SW]] += trans_prob[[SE, S, SW]] * self.drift
        else:
            # push towards north
            trans_prob[[NE, N, NW]] += trans_prob[[NE, N, NW]] * self.drift

        return trans_prob / np.sum(trans_prob)

    def is_outlier(self, particle: Particle) -> bool:
        """
        is_outlier checks if a particle is an outlier to the aggregated particles.
        :param particle: (Particle)
        :return: returns true if particle is outlier and false otherwise
        """
        return self.aggregated_particles.nearest_neighbour_dist(particle.pos) > self.max_dist
