import numpy as np
from Particle import Particle
from BST import BinarySearchTree

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


NUM_DIRECTIONS = 4
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

    def random_step(self, particle: Particle) -> Particle:
        """
        The particle takes a random step to go one pixel UP, DOWN, LEFT or RIGHT.
        The direction depends on the transition probability.
        :return: particle after taking a random step
        """

        self.del_from_matrix(particle)

        pmf = self.get_transition_probabilities(particle)
        cdf = np.cumsum(self.add_drift(pmf, particle))

        value = np.random.random()

        if value < cdf[0]:
            direction = UP
        elif value < cdf[1]:
            direction = RIGHT
        elif value < cdf[2]:
            direction = DOWN
        elif value < cdf[3]:
            direction = LEFT
        else:
            direction = -1  # STAY

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
        index = self.gen_index()
        if not self.from_edge:
            while self.aggregated_particles.nearest_neighbour([index % self.M, index // self.M]) < 25:
                index = self.gen_index()

        particle = Particle.from_index(index, self.M)
        self.matrix[particle.get_position()] = 1
        return particle

    def gen_index(self):
        """
        :return:
        """
        if self.from_edge:
            return np.random.choice(self.boundary_indices, 1)
        else:
            return np.random.randint(0, self.M * self.M)

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
        trans_prob = np.zeros(4)
        for direction, nbr_pos in enumerate(particle.get_nbr_positions()):
            if self.matrix[nbr_pos] == 0:
                trans_prob[direction] = 1
            else:
                trans_prob[direction] = 0

        if np.sum(trans_prob) != 0:
            return trans_prob / np.sum(trans_prob)
        return trans_prob

    def get_aggregated_nbr_count(self, particle: Particle):
        """
        get_aggregated_nbr_count gets the number of neighbours around a given particle that are already aggregated.
        :param particle: (Particle)
        :return: (int) count
        """
        count = 0
        for nbr_pos in particle.get_nbr_positions():
            if self.matrix[nbr_pos] == 1:
                count += 1
        return count

    def add_drift(self, trans_prob, particle):
        """
        a drift towards the center, speeds up the aggregation of particles.
        With drift the directions pointing towards the center of the field are preferred more.
        :param trans_prob: (list) of probabilites of transitioning to either of
        the 4 neighbouring pixels in the order [UP, RIGHT, DOWN, LEFT].
        :param particle: (Particle)
        :return: transition probabilites with drift.
        """
        pos_x, pos_y = particle.get_position()
        if pos_x < self.C:
            trans_prob[RIGHT] *= (trans_prob[RIGHT] + self.drift)
        else:
            trans_prob[LEFT] *= (trans_prob[LEFT] + self.drift)
        if pos_y < self.C:
            trans_prob[DOWN] *= (trans_prob[DOWN] + self.drift)
        else:
            trans_prob[UP] *= (trans_prob[UP] + self.drift)

        if np.sum(trans_prob) != 0:
            return trans_prob / np.sum(trans_prob)
        return trans_prob

    def is_outlier(self, particle: Particle) -> bool:
        """
        is_outlier checks if a particle is an outlier to the aggregated particles.
        :param particle: (Particle)
        :return: returns true if particle is outlier and false otherwise
        """
        return self.aggregated_particles.nearest_neighbour(particle.pos) > self.max_dist
