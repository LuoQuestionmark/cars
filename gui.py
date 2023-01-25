from collections import deque
from itertools import count, product
from random import choice, random
# import sys
from typing import Callable, Iterable

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from storage import Storage

import numpy as np

# import matplotlib
# matplotlib.use('Agg')

# config font so that it can show Chinese text correctly in Windows
import matplotlib.font_manager as fm
font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')

def chinese_interpretor(function: Callable, args: Iterable) -> str:
    chinese_intp = {
        "up": "上升右平台",
        "upleft": "上升左平台",
        "down": "下降右平台",
        "downleft": "下降左平台",
        "pop": "右移， 层数=",
        "popleft": "左移， 层数="
    }
    if chinese_intp.get(function.__name__) is None:
        return ""
    ret = chinese_intp[function.__name__] + ''.join([str(i) for i in args])
    return ret

class Storage_GUI():
    def __init__(self, *args) -> None:
        self.storage = Storage(*args)
        self.initialzed = False
        self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, sharey=True)
        self.mat_obj = self.ax1.matshow((self.storage.data != 0), vmin = 0, vmax=2)
        self.target = -1

        self.vehicle_text = list()
        self.vehicle_plat_obj = list()

        self.literal_text = deque(maxlen=9)
        self.literal_obj = list()

        self.fig.canvas.mpl_connect('close_event', lambda _: exit(0))

    def __call__(self) -> None:
        if not self.initialzed:
            self.update()
            plt.show(block=False)
            self.initialzed = True
        else:
            self.update()
            plt.draw()
        plt.pause(1)

    def print(self, text: str):
        self.literal_text.append(text)

        # clear old text
        for t in self.literal_obj:
            t.remove()
        self.literal_obj.clear()

        # create new text
        for index, t in enumerate(self.literal_text):
            self.literal_obj.append(self.ax2.text(0, index * 0.5, t, fontproperties=font))

    def update(self) -> None:
        # clear old drawings
        for t in self.vehicle_text:
            t.remove()
        self.vehicle_text.clear()

        for rect in self.vehicle_plat_obj:
            rect.remove()
        self.vehicle_plat_obj.clear()

        # update matshow
        self.mat_obj.set_data(np.where(self.storage.data != 0, 1, 0) + np.where(self.storage.data == self.target, 1, 0))

        self.vehicle_plat_obj.append(Rectangle((-0.5, self.storage.height - self.storage.left_plat_level - 0.8), 1, 0.3, facecolor = 'cyan'))
        self.vehicle_plat_obj.append(Rectangle((-1.5 + self.storage.width, self.storage.height - self.storage.right_plat_level - 0.8), 1, 0.3, facecolor = 'cyan'))
        
        for r in self.vehicle_plat_obj:
            self.ax1.add_patch(r)

        # update text
        for i, j in product(range(self.storage.height), range(self.storage.width)):
            if self.storage.data[i, j] != 0:
                self.vehicle_text.append(self.ax1.text(j, i, str(self.storage.data[i, j])))

    def randomize(self) -> None:
        """
        randomize the storage + the target
        """
        number = count(1) # a brand new counter
        number_list = list()
        
        # clear the old data
        self.storage.data = np.zeros_like(self.storage.data)
        self.target = -1
        self.storage.left_plat_level = 0
        self.storage.right_plat_level = 0

        for r, c in product(range(self.storage.height), range(1, self.storage.width - 1)):
            if (random() < 0.3):
                tmp = next(number)
                self.storage.data[r, c] = tmp
                number_list.append(tmp)

        self.target = choice(number_list)

if __name__ == '__main__':
    # init
    s_gui = Storage_GUI(7, 5)
    # s_gui.storage.add(1, 1)
    # s_gui.storage.add(2, 3)
    # s_gui.storage.data[3, 4] = 5
    # s_gui.storage.data[2, 1] = 6
    # s_gui.storage.data[2, 2] = 7
    # s_gui.target = 7
    img_count = count()
    while True:
        s_gui.randomize()

        path = Storage.calculate_shortest_path(s_gui.storage, s_gui.target)
        if path is None:
            continue

        path_iter = iter(path)
        while True:
            # show
            s_gui()
            plt.savefig(f"output_image{next(img_count)}")
            # update
            try:
                f, args = next(path_iter)
                f(*args)
                new_storage = f.__self__
                s_gui.storage = new_storage
                # print(new_storage)

                s_gui.print(chinese_interpretor(f, args))
            except StopIteration:
                break

        # s_gui.print("hello")
        
