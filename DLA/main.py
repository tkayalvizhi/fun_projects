from DLA import *
from DLA.Field import Field
from p5 import *
import numpy

M = 101
img = Field(M, sticking=0.05)
# image.random_walk(3)


def setup():
    size(M, M)
    background(255)
    mat = img.matrix
    mat = 255 - mat * 255
    with load_pixels():
        pixels = list(mat.flatten())


def draw():
    for mat in img.random_walk(25):
        mat = 255 - mat * 255
        print(mat)

        with load_pixels():
            pixels = list(mat.flatten())[:]

        image(width, height, img=pixels)



run()
