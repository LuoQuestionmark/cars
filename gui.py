from itertools import product
from time import sleep
from matplotlib import pyplot as plt
from storage import Storage

import numpy as np

def on_close(event):
    exit(0)

class Storage_GUI():
    def __init__(self, *args) -> None:
        self.storage = Storage(*args)
        self.initialzed = False
        self.fig, self.ax = plt.subplots()
        self.mat_obj = self.ax.matshow((self.storage.data != 0), vmin = 0, vmax=2)
        self.target = None

        self.vehicle_text = list()

        self.fig.canvas.mpl_connect('close_event', on_close)

    def __call__(self) -> None:
        if not self.initialzed:
            self.update()
            plt.show(block=False)
            self.initialzed = True
        else:
            self.update()
            plt.draw()
        plt.pause(1)

    def update(self) -> None:
        for t in self.vehicle_text:
            t.remove()
        self.vehicle_text.clear()

        self.mat_obj.set_data(np.where(self.storage.data != 0, 1, 0) + np.where(self.storage.data == self.target, 1, 0))

        for i, j in product(range(self.storage.height), range(self.storage.width)):
            if self.storage.data[i, j] != 0:
                self.vehicle_text.append(self.ax.text(j, i, str(self.storage.data[i, j])))

if __name__ == '__main__':
    # init
    s_gui = Storage_GUI(7, 5)
    s_gui.storage.add(1, 1)
    s_gui.storage.add(2, 3)
    s_gui.storage.data[3, 4] = 5
    s_gui.storage.data[2, 1] = 6
    s_gui.storage.data[2, 2] = 7

    path = iter(Storage.calculate_shortest_path(s_gui.storage, 7))
    s_gui.target = 7
    origin_storage = s_gui.storage

    while True:
        # show
        s_gui()

        # update
        try:
            f, args = next(path)
            f(*args)
            new_storage = f.__self__
            s_gui.storage = new_storage
        except StopIteration:
            s_gui.storage = origin_storage
            path = iter(Storage.calculate_shortest_path(s_gui.storage, 7))
        
