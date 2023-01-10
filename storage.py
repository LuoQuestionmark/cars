import numpy as np

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
        self.left_pad_level = 0
        self.right_pad_level = 0

    def __str__(self) -> str:
        return str(self.data)

    def add(self, col_num, value) -> bool:
        if col_num not in range(1, self.width):
            return False
        if col_num == 0 and self.left_pad_level != 0:
            return False
        if col_num == self.width - 1 and self.right_pad_level != 0:
            return 0
        if self.data[0, col_num] != 0:
            return False

        self.data[-1, col_num] = value

    def remove(self, col_num) -> bool:
        if col_num not in range(self.width):
            return False
        if self.data[0, col_num] == 0:
            return False

        self.data[-1, col_num] = 0

    def pop(self, level: int) -> bool:
        if level not in range(self.height):
            return False

        if level != self.right_pad_level:
            return False

        level = (self.height - 1) - level
        if self.data[level, -1] != 0:
            return False

        for i in reversed(range(1, self.width)):
            self.data[level][i] = self.data[level][i - 1]
        self.data[level][0] = 0

    def popleft(self, level: int) -> bool:
        if level not in range(self.height):
            return False

        if level != self.left_pad_level:
            return False

        level = (self.height - 1) - level
        if self.data[level, 0] != 0:
            return False

        for i in range(0, self.width - 1):
            self.data[level][i] = self.data[level][i + 1]
        self.data[level][self.width - 1] = 0

    def up(self) -> bool:
        if self.right_pad_level >= self.height - 1:
            return False

        level = self.height - self.right_pad_level - 1

        if self.data[level, self.width - 1] != 0:
            self.data[level - 1 , -1] = self.data[level, -1]
            self.data[level, -1] = 0

        self.right_pad_level += 1

        return True
    
    def upleft(self) -> bool:
        if self.left_pad_level >= self.height - 1:
            return False

        level = self.height - self.left_pad_level - 1

        if self.data[level, 0] != 0:
            self.data[level - 1 , 0] = self.data[level, 0]
            self.data[level, 0] = 0

        self.left_pad_level += 1

        return True

    def down(self) -> bool:
        if self.right_pad_level <= 0:
            return False

        level = self.height - self.right_pad_level - 1

        if self.data[level, -1] != 0:
            self.data[level + 1 , -1] = self.data[level, -1]
            self.data[level, -1] = 0

        self.right_pad_level -= 1

        return True

    def downleft(self) -> bool:
        if self.left_pad_level <= 0:
            return False

        level = self.height - self.left_pad_level - 1

        if self.data[level, 0] != 0:
            self.data[level + 1 , 0] = self.data[level, 0]
            self.data[level, 0] = 0

        self.left_pad_level -= 1

        return True


if __name__ == '__main__':
    storage = Storage(7, 5)
    print(storage)
    print("")

    storage.add(3, value=1)
    storage.add(4, value=2)
    storage.add(5, value=3)
    print(storage)
    print("")

    storage.pop(0)
    print(storage)
    print("")

    storage.up()
    print(storage)
    print("")

    storage.down()
    print(storage)
    print("")

    storage.popleft(0)
    storage.popleft(0)
    storage.popleft(0)
    storage.popleft(0)
    print(storage)
    print("")

    storage.upleft()
    print(storage)
    print("")

    storage.downleft()
    print(storage)
    print("")
