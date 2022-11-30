UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

X = 0
Y = 1


class Particle:
    def __init__(self, x: int, y: int, M: int):
        """
        A particle object that performs the random walk.
        :param x: x-axis position.
        :param y: y-axis position.
        :param M: the x-axis and y-axis extent
        """
        self.M = M
        if x < 0 or x > M:
            raise Exception("x - axis value must be between 0 and M")

        if y < 0 or y > M:
            raise Exception("y - axis value must be between 0 and M")

        self.pos = [x, y]

    def get_position(self):
        """
        get_position returns the current position of the particle.
        :return:
        """
        return self.pos[X], self.pos[Y]

    def move(self, direction: int) -> None:
        """
        This function moves the particle in a given direction.
        The image is toroidally bound. a particle moving off the left edge enters on the right,
        a particle moving off the right edge enters on the left, similarly for top and bottom.
        :param direction: (int) 0 - UP, 1 - RIGHT, 2 - DOWN, 3 - LEFT
        :return: None
        """
        if direction == UP:
            self.pos[Y] = (self.pos[Y] - 1) % self.M
        elif direction == RIGHT:
            self.pos[X] = (self.pos[X] + 1) % self.M
        elif direction == DOWN:
            self.pos[Y] = (self.pos[Y] + 1) % self.M
        elif direction == LEFT:
            self.pos[X] = (self.pos[X] - 1) % self.M
        else:
            return

    @classmethod
    def from_index(cls, index, M):
        """
        from_index method creates a Particle object from the index of a pixel of the image.
        :param index: (int) index of a pixel
        :param M:
        :return:
        """
        if index < 0 or index >= M ** 2:
            raise Exception("Index of pixel is out of bounds")
        return cls(index % M, index // M, M)

    def get_nbr_positions(self) -> list:
        """
        get-nbr positions return the Particle's current neighbours in the order - UP, RIGHT, DOWN, LEFT.
        The image is toroidally bound. A particle moving off the left edge enters on the right,
        a particle moving off the right edge enters on the left, similarly for top and bottom.
        :return:
        """
        return [(self.pos[X], int((self.pos[Y] - 1) % self.M)),  # Upward neighbour
                (int((self.pos[X] + 1) % self.M), self.pos[Y]),  # Rightward neighbour
                (self.pos[X], int((self.pos[Y] + 1) % self.M)),  # Downward neighbour
                (int((self.pos[X] - 1) % self.M), self.pos[Y])]  # Leftward neighbour
