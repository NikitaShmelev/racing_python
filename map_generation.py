from math import fabs
import numpy as np
import random
# shape = (45, 30)
# map = np.zeros(shape, dtype=float, order='C')
height = 10
width = 10
map = [
    [0 for i in range(height)] for i in range(width)
]
start_pos_x = int((len(map[0]) - 1)/2)
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
    y = len(map) - int((start_pos_x + 1) * np.sin(round(rand_anle*np.pi/180)) / (np.sin(
                    fabs(round(
                        np.pi/2 - rand_anle*np.pi/180
                    ))
                )) - 1)

vektors = {0: {
                'right_start': (right_road_x, right_road_y), # start of right road's side
                'left_start' : (left_road_x, left_road_y) # start of left road's side
                # ends of the roads will be added later - required len of dicts = 4
                }
            }
while left_road_y != y:
    if y < left_road_y - 1:
        left_road_y -= 1
        left_road_x -= 1
        right_road_y -= 1
        right_road_x -= 1
        map[left_road_y][left_road_x] = 1 if map[left_road_y][left_road_x] != 1 else 0
        map[right_road_y][right_road_x] = 1 if map[right_road_y][right_road_x] != 1 else 0
    else:
        
        num_key = list(vektors.keys())[-1]
        len_of_coords = len(vektors[num_key].keys())
        if len_of_coords != 4:
            vektors[num_key]['right_end'] = (right_road_x, right_road_y) # end
            vektors[num_key]['left_end'] = (left_road_x, left_road_y) # end
        else:
            num_key += 1
            vektors[num_key]['right_start'] = vektors[num_key-1]['right_end']
            vektors[num_key]['left_start'] = vektors[num_key-1]['left_end']
        break

for line in map:
    print(line)
for key in vektors.keys():
    print(vektors[key])

# print(y)
