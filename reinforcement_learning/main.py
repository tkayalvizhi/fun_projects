from p5 import *
from field import Field
import numpy as np
import time

num_row = 15
num_col = 15
side = 50
offset = 2
goals = [[3, 3], [1, 9]]
gamma = 0.85
epsilon = 0.001
field = Field(num_row, num_col, side)
count = 0


def gen_rand_obs():
    x = np.random.randint(1, num_col)
    y = np.random.randint(1, num_row)
    if np.random.random() < 0.5:
        return [x, y, x, y - 1]
    else:
        return [x, y, x - 1, y]


def setup():
    size(int(num_row + offset) * 2 * side, int(num_col + offset) * side)

    mono = createFont("cour.ttf", 15)
    textFont(mono)
    text_align("CENTER", "CENTER")

    field.set_goal(row=4, col=4, value=10)
    field.set_goal(row=9, col=1, value=10)
    field.set_goal(row=3, col=8, value=5)

    # for k in range(100):
    #     pairs = gen_rand_obs()
    #     field.set_obstacles(*pairs)


def draw():
    global count
    background(0)
    translate(((offset / 2) * side), ((offset / 2) * side))
    field.show()

    translate(((offset / 2 + num_row) * side), 0)
    field.show_with_text()

    old_values = field.values.copy()
    new_values = field.value_iteration_step(gamma)

    if (new_values - old_values < epsilon).all():
        translate(0, 0)
        fill(255)
        text("Value iteration algorithm converged", width * side / 2, offset * side / 2)
        noLoop()

    else:
        save_frame(f'frames/{str(count).zfill(4)}.png')
        count += 1


run()
