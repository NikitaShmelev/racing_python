from math import fabs
from numpy import pi, sin
import random

height = 1030
width = 1680
angle_round_precision = 5
map = [
    [0 for i in range(height)] for i in range(width)
]

width = 20



right_road_x = len(map[0]) - 1#start_pos_x + int(width/2)
left_road_x = right_road_x - width#start_pos_x - int(width/2)
left_road_y = len(map) - 1
right_road_y = left_road_y

start_pos_x = right_road_x - round(width/2)
start_pos_y = left_road_y
map[start_pos_y][start_pos_x] = 2

map[right_road_y][right_road_x] = 1
map[left_road_y][left_road_x] = 1

direction = 1 #random.randint(0, 1)
rand_anle = 30 #random.randrange(15, 90, 15) #random.randint(1, 89)
print(f'{rand_anle=} {left_road_y=} {left_road_x=}')
# 0 - left, 1 - right

if direction:
    rand_anle = round(rand_anle*pi/180, angle_round_precision)
    second_angle = fabs(round(
                        pi/2 - rand_anle, angle_round_precision
                    ))
    y = round(len(map) - int((start_pos_x + 1) * sin(rand_anle) / (sin(second_angle))))- 1
    # breakpoint()
print(f'{y=}')
vektors = {0: {
                'right_start': (right_road_x, right_road_y), # start of right road's side
                'left_start' : (left_road_x, left_road_y) # start of left road's side
                # ends of the roads will be added later - required len of dicts = 4
                }
            }
x = round(y*sin(second_angle)/sin(rand_anle)) + 1
y = round(x*sin(rand_anle)/sin(second_angle)) + 1
vektors[0]['left_end'] = (x,y)
vektors[0]['right_end'] = (x+4,y)
# while True:
#     print(left_road_y, y)
#     print(map[right_road_y][right_road_x])
#     if y < left_road_y  and left_road_x > 0:
#         if round(rand_anle*180/pi) == 45:
#             left_road_x -= 1
#             right_road_x -= 1
#             right_road_y -= 1
#             left_road_y -= 1
#         elif round(rand_anle*180/pi) == 30:
#             if left_road_x != 1:
#                 left_road_x -= 2
#                 right_road_x -= 2
#                 right_road_y -= 1
#                 left_road_y -= 1
#             else:
#                 left_road_x -= 1
#                 right_road_x -= 1
#                 right_road_y -= 1
#                 left_road_y -= 1
#         if map[left_road_y][left_road_x] != 1 and map[right_road_y][right_road_x] != 1:
        
#             map[left_road_y][left_road_x] = 1 
#             map[right_road_y][right_road_x] = 1
#     else:
    
#         print('else')
#         # left_road_y += 1
#         # left_road_x += 1
#         # right_road_y += 1
#         # right_road_x += 1
#         num_key = list(vektors.keys())[-1]
#         len_of_coords = len(vektors[num_key].keys())
#         if len_of_coords != 4:
#             vektors[num_key]['right_end'] = (right_road_x, right_road_y) # end
#             vektors[num_key]['left_end'] = (left_road_x, left_road_y) # end
#         else:
#             num_key += 1
#             vektors[num_key]['right_start'] = vektors[num_key-1]['right_end']
#             vektors[num_key]['left_start'] = vektors[num_key-1]['left_end']
#         break

# for line in map:
#     print(line)
for key in vektors.keys():
    print(vektors[key])

# print(y)
