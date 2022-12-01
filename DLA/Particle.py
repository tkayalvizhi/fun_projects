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
        self.update_list = [[-1, -1], [0, -1], [1, -1],
                            [-1, 0], [1, 0],
                            [-1, 1], [0, 1], [1, 1]]

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
        :param direction: (int)
                        0 - NW, 1 - N, 2 - NE,
                        3 - W, 4 - E,
                        5 - SW, 6 - S, 7-SE
        :return: None
        """
        update = self.update_list[direction]

        self.pos[X] = (self.pos[X] + update[X]) % self.M
        self.pos[Y] = (self.pos[Y] + update[Y]) % self.M

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
        x, y = self.pos
        up = int((y - 1) % self.M)
        down = int((y + 1) % self.M)
        left = int((x - 1) % self.M)
        right = int((x + 1) % self.M)

        return [(left, up), (x, up), (right, up),
                (left, y), (right, y),
                (left, down), (x, down), (right, down)]
