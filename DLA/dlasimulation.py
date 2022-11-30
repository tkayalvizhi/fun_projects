from tkinter import *
from PIL import Image, ImageTk
from Field import Field
import sys


def transform_matrix(matrix):
    return 255 - matrix * 255


class DlaSimulation(object):
    def __init__(self, dimension,
                 stickiness=0.05,
                 drift: float = 1,
                 max_dist=500,
                 frame_rate=100,
                 iterations=40000,
                 folder_path: str = 'frames'):

        self.master = Tk()
        self.master.update()
        self.field = Field(dim=dimension,
                           stickiness=stickiness,
                           drift=drift,
                           max_dist=max_dist)

        self.canvas = Canvas(self.master, width=dimension, height=dimension)
        self.canvas.pack()
        self.run(iterations, frame_rate, folder_path)
        self.master.mainloop()

    def run(self, iterations, frame_rate, folder_path):

        for matrix, count in self.field.random_walk(iterations):

            img = Image.fromarray(transform_matrix(matrix))
            imgTk = ImageTk.PhotoImage(image=img)

            self.canvas.create_image(0, 0, image=imgTk, anchor='nw')
            self.master.update()

            if count % frame_rate == 0:
                self.save(img, count, folder_path)

    def save(self, img, count, folder_path):
        img = img.convert("L")
        img.save(folder_path + f'/img_{str(count).zfill(5)}.png')


if __name__ == "__main__":
    DlaSimulation(dimension=int(sys.argv[1]),
                  stickiness=float(sys.argv[2]),
                  drift=float(sys.argv[3]),
                  max_dist=int(sys.argv[4]),
                  iterations=int(sys.argv[5]),
                  folder_path=sys.argv[6]
                  )
