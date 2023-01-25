from copy import deepcopy
from typing import Callable, Iterable, Self
import numpy as np

DEBUG = False

class Storage:
    """
    This class include the storage system, information of each position is saved
    as a value in a 2D array. 0 -> no car; positive values: -> car number.

    This class will support visualization by `matshow` the data.

    This class contains equally the rules which describe all available moves, which are:
    - add(col_num), remove(col_num): add/remove cars on the ground level
    - rise(level), riseleft(level): put the car on the right/left to the given level,
      then put the car from the other side back to the ground

    to grant a step-to-step animation, we define these "basic" actions, too:
    - up(), upleft()
    - down(), downleft()
    - pop(level), popleft(level)
    """
    def __init__(self, width: int, height: int) -> None:
        """
        width: the num of col available on the ground floor
        height: the num of levels
        """
        self.data = np.zeros((height, width), dtype=int)
        self.width = width
        self.height = height

        # the following integers represent the current level of the moving platform,
        # numbering from 0 to the (height - 1)
        self.left_plat_level = 0
        self.right_plat_level = 0

    def __str__(self) -> str:
        return str(self.data) + f"\nleft plat level: {self.left_plat_level}\nright plat level: {self.right_plat_level}"

    def add(self, col_num, value, copy=False) -> bool|Self:
        if col_num not in range(0, self.width):
            return False
        if col_num == 0 and self.left_plat_level != 0:
            return False
        if col_num == self.width - 1 and self.right_plat_level != 0:
            return False
        if self.data[0, col_num] != 0:
            return False

        if copy:
            self = deepcopy(self)
        self.data[-1, col_num] = value
        if copy:
            return self
        else:
            return True

    def remove(self, col_num, copy=False) -> bool|Self:
        if col_num not in range(self.width):
            return False
        if self.data[-1, col_num] == 0:
            return False

        if copy:
            self = deepcopy(self)
        self.data[-1, col_num] = 0
        if copy:
            return self
        else:
            return True

    def pop(self, level: int, copy=False) -> bool|Self:
        if level not in range(self.height):
            return False

        if level != self.right_plat_level:
            return False

        level = (self.height - 1) - level
        if self.data[level, -1] != 0:
            return False

        if copy:
            self = deepcopy(self)

        for i in reversed(range(1, self.width)):
            self.data[level][i] = self.data[level][i - 1]
        self.data[level][0] = 0

        if copy:
            return self
        else:
            return True

    def popleft(self, level: int, copy=False) -> bool|Self:
        if level not in range(self.height):
            return False

        if level != self.left_plat_level:
            return False

        level = (self.height - 1) - level
        if self.data[level, 0] != 0:
            return False

        if copy:
            self = deepcopy(self)

        for i in range(0, self.width - 1):
            self.data[level][i] = self.data[level][i + 1]
        self.data[level][self.width - 1] = 0

        if copy:
            return self
        else:
            return True

    def up(self, copy=False) -> bool|Self:
        if self.right_plat_level >= self.height - 1:
            return False

        level = self.height - self.right_plat_level - 1

        if self.data[level, self.width - 1] != 0:
            self.data[level - 1 , -1] = self.data[level, -1]
            self.data[level, -1] = 0

        if copy:
            self = deepcopy(self)

        self.right_plat_level += 1

        if copy:
            return self
        else:
            return True
    
    def upleft(self, copy=False) -> bool|Self:
        if self.left_plat_level >= self.height - 1:
            return False

        level = self.height - self.left_plat_level - 1

        if copy:
            self = deepcopy(self)

        if self.data[level, 0] != 0:
            self.data[level - 1 , 0] = self.data[level, 0]
            self.data[level, 0] = 0

        self.left_plat_level += 1

        if copy:
            return self
        else:
            return True

    def down(self, copy=False) -> bool|Self:
        if self.right_plat_level <= 0:
            return False

        level = self.height - self.right_plat_level - 1

        if copy:
            self = deepcopy(self)

        if self.data[level, -1] != 0:
            self.data[level + 1 , -1] = self.data[level, -1]
            self.data[level, -1] = 0

        self.right_plat_level -= 1

        if copy:
            return self
        else:
            return True

    def downleft(self, copy=False) -> bool|Self:
        if self.left_plat_level <= 0:
            return False

        level = self.height - self.left_plat_level - 1

        if copy:
            self = deepcopy(self)

        if self.data[level, 0] != 0:
            self.data[level + 1 , 0] = self.data[level, 0]
            self.data[level, 0] = 0

        self.left_plat_level -= 1

        if copy:
            return self
        else:
            return True

    def available_options(self) -> list[tuple[Callable[..., bool], Iterable]]:
        ret = list()

        true_left_level = self.height - self.left_plat_level - 1
        if self.left_plat_level > 0:
            # descend left plat
            ret.append((self.downleft, []))
        if self.left_plat_level < self.height - 1:
            # rise left plat
            ret.append((self.upleft, []))
        if self.data[true_left_level, 0] == 0:
            # no car on the left platform
            ret.append((self.popleft, [self.left_plat_level]))

        true_right_level = self.height - self.right_plat_level - 1
        if self.right_plat_level > 0:
            # descend right plat
            ret.append((self.down, []))
        if self.right_plat_level < self.height - 1:
            # rise right plat
            ret.append((self.up, []))
        if self.data[true_right_level, -1] == 0:
            # no car on the right platform
            ret.append((self.pop, [self.right_plat_level]))

        for i in range(self.width):
            # a car on the ground level (to remove)
            if self.data[-1, i] != 0:
                ret.append((self.remove, [i, ]))

        return ret

    def eval(self, vehicle_num: int) -> int:
        """
        estimate the minimum step to remove vehcle with given number
        if the vehicle number is not found, then return False,
        otherwise return the number of minimum steps
        """
        if np.any(self.data == vehicle_num) == False:
            # if it is not found
            return -1

        if np.any(self.data[-1] == vehicle_num) == True:
            # if on the ground
            return 0

        for i in range(1, self.height):
            if vehicle_num in self.data[i]:
                val = list(self.data[i]).index(vehicle_num)
                val = self.width - np.abs(int(self.width / 2) - val)
                return self.height - i + val

        raise RuntimeError("unexpected condition, potential bugs")

    @classmethod
    def calculate_shortest_path(cls, storage: Self, vehicle_num: int) -> Iterable[list[tuple[Callable[..., bool], Iterable]]] | None:
        """
        return the shortest sequence that make the given car on the ground
        """
        if storage.eval(vehicle_num) == -1:
            return None

        possibles = list() # list of (storage, [operations])
        possibles.append((storage, []))

        examined = set() # set of storage.data

        while possibles:
            studying_case, operations = possibles.pop(0)
            if (studying_case.eval(vehicle_num) == 0):
                # if successed, return
                return operations

            if str(studying_case) in examined:
                # if already examined, continue to the next case
                continue
            else:
                # otherwise add it to the set
                examined.add(str(studying_case))

            for operation, args in studying_case.available_options():
                if operation.__name__ == "remove":
                    continue
                new_case = operation(*args, copy=True)
                if new_case == False:
                    raise RuntimeError
                temp = list(operations)
                temp.append([operation, args])
                possibles.append((new_case, temp))
                if DEBUG:
                    print(f"add new case: \n{new_case}\nwith operation \"{operation.__name__}({args})\"")
                    print(f"eval: {new_case.eval(vehicle_num)}")

            possibles = sorted(possibles, key=lambda case: case[0].eval(vehicle_num))


if __name__ == '__main__':
    storage = Storage(7, 5)
    storage.add(1, 1)
    storage.add(2, 3)
    storage.data[3, 4] = 5
    storage.data[2, 1] = 6
    storage.data[2, 2] = 7

    # for f, args in storage.available_options():
    #     print(f.__name__, args)
    #     new_state = f(*args, copy=True)
    #     print(new_state)
    #     print(new_state.eval(5))

    print(storage)

    r = Storage.calculate_shortest_path(storage, 7)
    if r != None:
        r = [(i[0].__name__, i[1]) for i in r]
    print(r)
    # storage2 = storage.add(3, value=1, copy=True)

    # print(storage)
    # print(storage2)
    # storage.add(4, value=2)
    # storage.add(5, value=3)
    # print(storage)
    # print("")

    # storage.pop(0)
    # print(storage)
    # print("")

    # storage.up()
    # print(storage)
    # print("")

    # storage.down()
    # print(storage)
    # print("")

    # storage.popleft(0)
    # storage.popleft(0)
    # storage.popleft(0)
    # storage.popleft(0)
    # print(storage)
    # print("")

    # storage.upleft()
    # print(storage)
    # print("")

    # storage.downleft()
    # print(storage)
    # print("")
