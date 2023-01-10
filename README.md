# Cars

This is for the visualization of my grandpa's conception.

## Description of the concept

This idea of this program is to simulate the function of a parking slot of multiple stages. To do the work, the parking slot is simulated by a program python, which track the used and available parking slots in an `array`. Lator on I am planning to show it in a GUI by using the module of `matplotlib`, specially the function `matshow`.

The development of this program is divided into several stages:

1. create a `Storage` class that save the parking slots, including the array; in which class there will be all the basic operation, e.g. addint a new car, removing an existing car;
2. implement the algorithms of graph that calculate the movement of cars, these movements will be calculated then saved as individual variables, so that they can be used seperately;
3. create a class that do the visualization, including animation, maybe also a textualized version so that it can be easily understood.

## Basic movements

The basic movements are the following:

- `add`, `remove`: to add or to remove a car to or from the parking slots;
- `pop`, `popleft`: to move a car into the platform that can rise or descend a car;
- `up`, `upleft`: to lift a car on the platform on the right side/left side;
- `down`, `downleft`: to descend a car on the platform on the right side/left side.

## Data representation

The data is saved in an array with the help of class `numpy.array`. The data saves the information of all parking slots in 2D, the following code is a example:

```python
# example of a parking slot array, six cars in total
# three cars on the ground, two on the second floor, one on the third
data = np.array(
    [
        [0, 0, 0, 1, 0],
        [0, 2, 3, 0, 0],
        [8, 7, 4, 0, 0]
    ]
)
```
