p0_x = 9
p1_x = 13
p2_x = 8
p3_x = 8

p0_y = 4
p1_y = 4
p2_y = 1
p3_y = 8

s1_x = p1_x - p0_x
s1_y = p1_y - p0_y
s2_x = p3_x - p2_x  
s2_y = p3_y - p2_y
s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)
if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
    print('YES')
else:
    print('NO')