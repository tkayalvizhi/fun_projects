from tkinter import *
from PIL import Image, ImageTk
from DLA.Field import Field


class Window(object):
    def __init__(self, dimension):
        self.master = Tk()
        self.master.update()
        self.field = Field(dim=dimension, sticking=1, drift=0.7)
        self.count = 0

        canvas = Canvas(self.master, width=dimension, height=dimension)
        canvas.pack()

        for matrix, to_save in self.field.random_walk():
            img = Image.fromarray(self.transform_matrix(matrix))
            imgTk = ImageTk.PhotoImage(image=img)
            canvas.create_image(0, 0, image=imgTk, anchor='nw')
            self.master.update()

            if to_save:
                img = img.convert("L")
                img.save(f'frames/{str(self.count).zfill(5)}.png')
                self.count += 1

        self.master.mainloop()

    def transform_matrix(self, matrix):
        return 255 - matrix*255

Window(501)

