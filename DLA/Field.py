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


class Field(object):

    def __init__(self, dim: int, stickiness: float = 1, drift: float = 0.1, max_dist=200, from_edge=False):
        """
        The Field / Image class that dictates the particle movements and aggregation.
        :param dim: (int) width / height of Field -
                    also the number of pixels in each row and column of Field
        :param stickiness: (float) the stickiness factor which determines the probability of a particle aggregating
        :param drift: the factor of drift towards the center
        """

        if dim < 1:
            raise Exception("Dimension of image must be larger than or equal to 1")

        if dim % 2 == 0:
            raise Exception("Dimension must be an odd number")

        self.M = dim

        if stickiness < 0 or stickiness > 1:
            raise Exception("Sticking factor must be between 0 and 1")

        self.stickiness = stickiness
        self.drift = drift
        self.max_dist = max_dist
        self.from_edge = from_edge

        # matrix indicating if pixel is occupied
        self.matrix = np.zeros(shape=(self.M, self.M))
        self.aggregated_particles = BinarySearchTree()

        # center particle
        self.C = int(self.M / 2)
        self.center = Particle(self.C, self.C, self.M)
        self.add_to_matrix(self.center)
        self.aggregated_particles.insert(self.center.pos)

        # List of indices along the boundary of the Field.
        self.boundary_indices = self.get_boundary_indices()
        self.scale = 20

    def random_step(self, particle: Particle) -> Particle:
        """
        The particle takes a random step in the direction of the nearest aggregated particle
        The direction depends on the transition probability.
        :return: particle after taking a random step
        """
        self.del_from_matrix(particle)

        pmf = self.get_transition_probabilities(particle)

        # if not all neighbouring pixels are occupied by aggregated particles
        if np.sum(pmf) != 0:
            nearest = self.aggregated_particles.nearest_neighbour(particle.pos)
            # drift towards nearest aggregated particle
            cdf = np.cumsum(self.add_drift(pmf, particle, nearest))
            # sample a direction from the cumulative distribution function of directions
            direction = bisect_left(cdf, np.random.random())
            # take a step in the direction
            particle.move(direction)

        self.add_to_matrix(particle)

        return particle

    def random_walk(self, num_iter=40000):
        """
        random walk is a generator function that performs the random walk for the number of iterations given.
        It yields the field matrix after each random step.

        :param num_iter: number of walks to take
        :returns: yields current field matrix (ndarray) and the current iteration (int)
        """
        count = 0
        yield self.matrix, count
        while count < num_iter:
            particle = self.generate_particle()

            while not self.aggregated_particles.contains(particle.pos):
                yield self.matrix, count

                if not self.from_edge:
                    # if particle is far from the aggregated particles
                    if self.is_outlier(particle):
                        # delete particle and start over again
                        self.del_from_matrix(particle)
                        break

                # particle takes a random step
                particle = self.random_step(particle)

                # for each neighbouring aggregated particle,
                # the current particle has "stickiness" probability of getting aggregated
                for _ in range(self.get_aggregated_nbr_count(particle)):
                    if np.random.random() < self.stickiness:
                        self.add_to_matrix(particle)
                        self.aggregated_particles.insert(particle.pos)
                        break

            # if aggregated
            else:
                # increment iteration counter
                count += 1
                print(f"iteration: {count}")
                yield self.matrix, count

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
        if not self.from_edge:
            index = np.random.randint(0, self.M * self.M)
            while self.aggregated_particles.nearest_neighbour([index % self.M, index // self.M]) < 5:
                index = np.random.randint(0, self.M * self.M)
        else:
            index = np.random.choice(self.boundary_indices, 1)

        particle = Particle.from_index(index, self.M)
        self.matrix[particle.get_position()] = 1
        return particle

    def add_to_matrix(self, particle: Particle) -> None:
        """
        add_to_matrix adds a particle to the Field matrix. The additions only reflect on the image.
        It does NOT add the particle to the "self.aggregated" BST.
        :param particle: (Particle)
        :return: None
        """
        self.matrix[particle.get_position()] = 1

    def del_from_matrix(self, particle: Particle) -> None:
        self.matrix[particle.get_position()] = 0

    def get_transition_probabilities(self, particle: Particle):
        """
        This function computes the naive probability of a Particle
        landing at either of the 4 neighbouring pixels.
        :param particle: (Particle)
        :return: (list) of probabilites of transitioning to either of the 4 neighbouring pixels in the order
        [UP, RIGHT, DOWN, LEFT]
        """
        nbrs = particle.get_nbr_positions()
        trans_prob = np.array([1 - self.matrix[nbrs[i]] for i in range(NUM_DIRECTIONS)])

        if np.sum(trans_prob) != 0:
            return trans_prob / np.sum(trans_prob)
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

        if np.sum(trans_prob) != 0:
            return trans_prob / np.sum(trans_prob)
        return trans_prob

    def is_outlier(self, particle: Particle) -> bool:
        """
        is_outlier checks if a particle is an outlier to the aggregated particles.
        :param particle: (Particle)
        :return: returns true if particle is outlier and false otherwise
        """
        return self.aggregated_particles.nearest_neighbour_dist(particle.pos) > self.max_dist
