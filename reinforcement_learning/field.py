import numpy as np
from p5 import *

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
STAY = 4


def show_text(value: float = 0):
    fill(255)
    text(str(np.round(value, 1)), 0, 0)


class State(object):
    def __init__(self, x, y, side):
        self.row = y
        self.col = x
        self.side = side
        self.goal = 0
        self.o_x, self.o_y = self.get_center()

    def get_center(self):
        row = self.side * self.row + (self.side / 2)
        col = self.side * self.col + (self.side / 2)
        return row, col

    def show_state(self, value: float = 0):
        stroke(0)
        stroke_weight(1)
        if value > 0:
            fill(0, value, 0)
        else:
            fill(0, 0, 0)

        square(0, 0, self.side, mode='CENTER')

    def show_arrow(self, dir: int = -1):
        stroke(150)
        stroke_weight(1)
        if dir == STAY:
            circle(0, 0, self.goal)
            return
        elif dir == LEFT:
            rotate(np.pi / 2)
        elif dir == RIGHT:
            rotate(3 * np.pi / 2)
        elif dir == DOWN:
            rotate(0)
        elif dir == UP:
            rotate(np.pi)
        triangle(-self.side / 16, 0, 0, self.side / 4, self.side / 16, 0)


class Obstacle(object):
    def __init__(self, x, y, ox, oy, side):
        self.p1 = (y * side, x * side)
        self.p2 = (oy * side, ox * side)

    def show(self):
        stroke(255)
        stroke_weight(3)
        line(self.p1, self.p2)


class Field(object):
    def __init__(self, num_row: int, num_col: int, side: int):

        if num_row < 1 or num_col < 1:
            raise Exception("Sorry, no numbers below one")

        if side <= 0:
            raise Exception("Side must be greater than zero")

        self.num_row = num_row
        self.num_col = num_col
        self.side = side
        self.states = []
        self.obstacles = []

        for i in range(self.num_row):
            row = []
            for j in range(self.num_col):
                row.append(State(i, j, self.side))
            self.states.append(row)

        self.T = self.set_transition_probabilities()
        self.rewards = np.full(shape=(self.num_row, self.num_col,  # state
                                      5,  # action
                                      self.num_row, self.num_col  # other state
                                      ), fill_value=-0.1)
        self.values = np.full(shape=(self.num_row, self.num_col), fill_value=0)
        self.policy = np.zeros_like(self.values)

    def show(self) -> None:

        for i in range(self.num_row):
            for j in range(self.num_col):
                value = self.values[i][j]
                push_matrix()
                x, y = self.states[i][j].get_center()
                translate(x, y)
                self.states[i][j].show_state(value)
                self.states[i][j].show_arrow(dir=self.policy[i][j])
                pop_matrix()

        for obs in self.obstacles:
            obs.show()

    def show_with_text(self):
        for i in range(self.num_row):
            for j in range(self.num_col):
                value = self.values[i][j]
                push_matrix()
                x, y = self.states[i][j].get_center()
                translate(x, y)
                self.states[i][j].show_state(value)
                show_text(value)
                pop_matrix()

        for obs in self.obstacles:
            obs.show()

    def set_transition_probabilities(self) -> np.array:
        """
        Here the actions are deterministic
        actions : 0-left, 1-right, 2-up, 3-down, 4-rest
        transition_probabilities: [state, action, other_state]
        :return:
        """
        transition_probabilities = np.zeros(shape=(self.num_row, self.num_col, 5, self.num_row, self.num_col))

        for i in range(self.num_row):
            for j in range(self.num_col):
                # all columns except first column
                if j != 0:
                    # if action is LEFT probability of moving LEFT one state
                    transition_probabilities[i][j][LEFT][i][j - 1] = 0.9
                    transition_probabilities[i][j][LEFT][i][j] = 0.1

                # all columns except last column
                if j != self.num_col - 1:
                    # if action is RIGHT probability of moving RIGHT one state
                    transition_probabilities[i][j][RIGHT][i][j + 1] = 0.9
                    transition_probabilities[i][j][RIGHT][i][j] = 0.1
                # all rows except first row
                if i != 0:
                    # if action is UP probability of moving UP one state
                    transition_probabilities[i][j][UP][i - 1][j] = 0.9
                    transition_probabilities[i][j][UP][i][j] = 0.1

                # all rows except last row
                if i != self.num_row - 1:
                    # if action is DOWN probability of moving DOWN one state is
                    transition_probabilities[i][j][DOWN][i + 1][j] = 0.9
                    transition_probabilities[i][j][DOWN][i][j] = 0.1

                transition_probabilities[i][j][STAY][i][j] = 1

        return transition_probabilities

    def set_goal(self, row, col, value):

        # probability of transitioning from  goal state to other states is 0
        # self.T[row, col, :] = np.zeros(shape=(self.num_row, self.num_col))
        # probability of transitioning from  goal state to itself is 1
        # self.T[row, col, :, row, col] = 1
        # reward collected after reaching goal is given value
        self.rewards[row, col, STAY, row, col] = value
        self.states[row][col].goal = value

    def value_iteration_step(self, gamma=0.5):
        values = self.values
        q_value = np.zeros(shape=(self.num_row, self.num_col, 5))

        for i in range(self.num_row):
            for j in range(self.num_col):
                for action in range(5):
                    q_value[i][j][action] = np.sum(
                        self.T[i][j][action] * (self.rewards[i][j][action] + (gamma * values)))

        self.values = np.max(q_value, axis=2)
        self.policy = np.argmax(q_value, axis=2)
        return self.values

    def value_iteration(self, epsilon=0.001, gamma=0.5):
        old_values = self.values.copy()
        new_values = self.value_iteration_step(gamma)

        while all(new_values - old_values > epsilon):
            old_values = new_values.copy()
            new_values = self.value_iteration_step(gamma)

    def get_policy(self, state) -> int:
        """

        :param state: current state
        :return: best action to quickly reach state of highest value
        """
        return self.policy[state[0], state[1]]

    def set_obstacles(self, c, r, oc, o_r):
        # case of UP - DOWN obstacle
        if c - oc == 0 and abs(r - o_r) == 1:
            r1 = min(r, o_r)
            r2 = max(r, o_r)
            self.obstacles.append(Obstacle(c, r2,  # state UP of obstacle "SU"
                                           c + 1, r2,  # state UP of obstacle "SD"
                                           self.side))
            # transition probability for taking DOWN from SU to reach is SD = 0
            self.T[c, r1, DOWN, c, r2] = 0
            # instead the transitioning ends up at same state SU
            self.T[c, r1, DOWN, c, r1] = 1

            self.T[c, r2, UP, c, r1] = 0
            self.T[c, r2, UP, c, r2] = 1

            # penalize for taking action towards the obstacle
            self.rewards[c, r1, DOWN, :, :] = -1
            self.rewards[c, r2, UP, :, :] = -1

        # case of LEFT - RIGHT obstacle
        elif r - o_r == 0 and abs(c - oc) == 1:
            c1 = min(c, oc)
            c2 = max(c, oc)
            self.obstacles.append(Obstacle(c2, r,  # state left of obstacle "SL"
                                           c2, r + 1,  # state right of obstacle "SR"
                                           self.side))

            # transition probability for taking RIGHT from SL to reach is SR = 0
            self.T[c1, r, RIGHT, c2, r] = 0
            # instead the transitioning ends up at same state SL
            self.T[c1, r, RIGHT, c1, r] = 1

            self.T[c2, r, LEFT, c1, r] = 0
            self.T[c2, r, LEFT, c2, r] = 1

            # penalize for taking action towards the obstacle
            self.rewards[c1, r, RIGHT, :, :] = -1
            self.rewards[c2, r, LEFT, :, :] = -1

        else:
            return
