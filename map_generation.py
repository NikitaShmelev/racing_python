from math import fabs
import numpy as np
import random
# shape = (45, 30)
# map = np.zeros(shape, dtype=float, order='C')

map = [
    [0 for i in range(30)] for i in range(50)
]
start_pos_x = 9
start_pos_y = len(map) - 1
width = 4

map[start_pos_y][start_pos_x] = 2

right_road_x = start_pos_x + int(width/2)
left_road_x = start_pos_x - int(width/2)
left_road_y = start_pos_y
right_road_y = left_road_y

map[right_road_y][right_road_x] = 1
map[left_road_y][left_road_x] = 1

direction = 1 #random.randint(0, 1)
rand_anle = 45 #random.randint(1, 89)
# 0 - left, 1 - right
if direction:
    left_road_y = len(map) - int((start_pos_x + 1) * np.sin(round(rand_anle*np.pi/180)) / (np.sin(
                    fabs(round(
                        np.pi/2 - rand_anle*np.pi/180
                    ))
                )) - 1)
map[left_road_y][0] = 1


for line in map:
    print(line)
print(start_pos_x, start_pos_y, width)


# print(y)
