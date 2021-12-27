import pygame
import time
import random
import math, sys
from map_generation import Map
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()
over_font = pygame.font.Font('freesansbold.ttf', 26)
run = True
FPS = 60
width = 1680
height = 1030
window = pygame.display.set_mode((width, height))
TEXTCOLOR = (255, 255, 255)
clock = pygame.time.Clock()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)


class MainCar:
    def __init__(self, x_pos, y_pos, 
                max_vel, rotation_vel, 
                image_path, acceleration, 
                start_vel, angle):
        self.img = scale_image(pygame.image.load(image_path), 0.55)
        # self.img = pygame.image.load(image_path)
        self.max_vel = max_vel
        self.vel = start_vel
        self.rotation_vel = rotation_vel
        self.angle = angle
        self.x_pos, self.y_pos = x_pos, y_pos
        self.acceleration = acceleration

    

    def draw(self, window):
        blit_rotate_center(
                    window, self.img, 
                    (self.x_pos, self.y_pos), 
                    self.angle
                    )

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y_pos -= vertical
        self.x_pos -= horizontal

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x_pos, self.y_pos, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
    def collide(self, mask, x=0, y=0, x_fix=0, y_fix=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(-x+self.x_pos + x_fix), int(-y+self.y_pos+y_fix))
        poi = car_mask.overlap(mask, offset)
        return poi
    

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


    def bounce(self):
        self.vel = -self.vel
        self.move()



def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def handle_collision(main_car, images_masks):
    for mask in images_masks:
        #0 50
        x_fix = mask[3]
        # 100 0
        y_fix = mask[4]
        # y_fix = -10 if len(mask) == 4 else 0

        if main_car.collide(mask=mask[0], x=mask[1], y=mask[2], x_fix=x_fix, y_fix=y_fix) != None:
            main_car.bounce()
        
            

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False


    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def draw_objects(images):
    for img, pos in images:
        window.blit(img, pos)








# def road_up_turn_right(x_right, y_right, x_left, y_left, road_orientation):
#     # right_side = scale_image(pygame.image.load("images/road/Turn_right_1.png"), 1)
#     # if road_collision(right_side, x_right, y_right):
        
#     y_left = generate_straight_road_y(x_left, y_left, road_orientation, 50, 0)
#     y_left = generate_straight_road_y(x_left, y_left, road_orientation, 50, 0)
#     y_right = generate_straight_road_y(x_right, y_right, road_orientation, 45, -60)
#     corner_left = scale_image(pygame.image.load("images/road/Road_turn_corner_5.png"), 1)
#     images.append((corner_left, (x_left-corner_left.get_width()+13, y_left+35)))
#     x_left += 10
#     y_left += 25 
#     y_left += images[-1][0].get_height()
#     road_orientation = 1
#     x_left = generate_straight_road_x(x_left, y_left , road_orientation, -50, 100)
#     x_left = generate_straight_road_x(x_left, y_left, road_orientation, -50, 100)
#     corner_right = scale_image(pygame.image.load("images/road/Road_turn_corner_5.png"), 1)
#     images.append(
#         (corner_right, (
#             x_right-corner_right.get_width()+13, y_right+37
#             ))
#         )
#     x_right += 15
#     y_right += 87+37
#     x_right = generate_straight_road_x(x_right, y_right, road_orientation, -70, 50)
#     return x_right, y_right, x_left, y_left, road_orientation


def generate_map(main_car, map):
    map.step_straight_y()
    # map.step_straight_y()
    
   

  
    # while True:
    
    # if y > 0 and y < height:
    direction = 2#random.randint(1,3)
    
        # 1 - left, 2 - straight, 3 - right
    if direction == 3:
        if map.check_turn(width, height, True, -1):
            map.horizontal_turn()
        else:
            print('nie git')
    elif direction == 1:
        if map.check_turn(width, height, True, 1):
            map.horizontal_turn()
        else:
            print('nie git')
    else:
        map.step_straight_y()
            # change direction 
            
        # left_side = scale_image(pygame.image.load("images/road/Turn_left_1.png"), 1)
        # if x_left - left_side.get_width() <= 2*left_side.get_width():
        #     # no widht for turn left
        #     # then turn right
        #     right_side = scale_image(pygame.image.load("images/road/Turn_right_1.png"), 1)
        #     if road_collision(right_side, x_right, y_right):
                
        #         road_up_turn_right(x_right, y_right, x_left, y_left, road_orientation)

        #     else:
        #         print('huit')
        # else:
        #     print('git add left turn')
    # else:
    #     break
        
            
        # break

def gameloop():
    # while True:
    #     x_pos = random.randint(100, width-70)
    #     if x_pos + 90 < width - 70:
    #         break
    #     elif  x_pos - 50 > 100:
    #         break
    #     else:
    #         continue 
    x_pos = 1450 #- 140
    y_pos = height-100
    main_car = MainCar(
        x_pos=x_pos, y_pos= y_pos,
        max_vel=5, rotation_vel=4,
        image_path='images/car_images/car_small_up.png', 
        acceleration=0.2*5, start_vel=0,
        angle=0
        )
    map = Map(
        x_left=main_car.x_pos - 50,
        y_left=main_car.y_pos,
        x_right=main_car.x_pos + 90,
        y_right=main_car.y_pos
    )

    generate_map(main_car, map)
    while run:
        clock.tick(FPS)

        window.fill((0,0,0))

        map.draw_map(window)
        main_car.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.KEYDOWN:
        move_player(main_car)
        # over_text = over_font.render(f'{main_car.x_pos=} {main_car.y_pos=}', True, (255, 255, 255))
        
        drawText(f'{round(main_car.x_pos)=} {round(main_car.y_pos)=}', MAIN_FONT, window, 128, 0)
        # pygame.draw.line(
        #     window, 'red', (1029, 1679), (20, 20), width=1
        # )
        handle_collision(
            main_car,
            map.images_masks
            # game_info
            )
        pygame.display.update()

        
    pygame.quit()




if __name__ == "__main__":
    gameloop()
