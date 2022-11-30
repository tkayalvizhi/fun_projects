from p5 import *
import numpy as np

sz = 600
num_balls = 50


class Ball(object):
    def __init__(self):
        self.pos = sz * np.random.random(2)
        self.velocity = 2 * np.random.random(2) - 1
        self.radius = 20 * np.random.random() + 5
        self.m = self.radius ** 2
        self.color = [0, 0, 255]

    def move(self, scale=1):

        if (self.pos[0] >= sz) or (self.pos[0] < 0):
            self.velocity[0] *= -1

        if (self.pos[1] >= sz) or (self.pos[1] < 0):
            self.velocity[1] *= -1

        self.pos += self.velocity * scale

        self.color[2] += min(self.color[2] + 5, 255)
        self.color[0] = max(self.color[0] - 5, 0)

    def collides_with(self, other):
        return np.linalg.norm(self.pos - other.pos) < (self.radius + other.radius)

    def bounce(self, other):
        d_pos = self.pos - other.pos
        d_vel = self.velocity - other.velocity

        self.velocity -= (2 * other.m / (self.m + other.m)) * (d_vel.T @ d_pos) * d_pos / (d_pos.T @ d_pos)
        other.velocity += (2 * self.m / (self.m + other.m)) * (d_vel.T @ d_pos) * d_pos / (d_pos.T @ d_pos)

        self.color = [255, 0, 0]
        other.color = [255, 0, 0]

    def show(self):
        fill(*self.color, alpha=100)
        noStroke()
        circle(self.pos[0], self.pos[1], self.radius * 2)


balls = []

count = 0


def check_bounce():
    for i in range(num_balls):
        for j in range(i + 1, num_balls):
            if balls[i].collides_with(balls[j]):
                balls[i].bounce(balls[j])
                while balls[i].collides_with(balls[j]):
                    balls[i].move(0.1)
                    balls[j].move(0.1)


def setup():
    size(sz, sz)
    for i in range(num_balls):
        balls.append(Ball())


def draw():
    # global count
    background(250)
    check_bounce()

    for i in range(num_balls):
        balls[i].move()
    for i in range(num_balls):
        balls[i].show_state()

    # save_frame(f'frames2/{str(count).zfill(4)}.png')
    # count += 1


run()
