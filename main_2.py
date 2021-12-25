import pygame
import time
import random
import math, sys
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
# TRACK_BORDER = scale_image(pygame.image.load("images/track-border.png"), 0.9)
# TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
images = [
    
    # (img, (x, y))
]
images_masks = [
    # (mask, x, y)
]

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
        
    def collide(self, mask, x=0, y=0, x_fix=50):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(-x+self.x_pos + x_fix), int(-y+self.y_pos))
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

def handle_collision(main_car):
    for mask in images_masks:
        print(mask[0].get_size())
        x_fix = 0 if len(mask) == 4 else 50
        if main_car.collide(mask=mask[0], x=mask[1], y=mask[2], x_fix=x_fix) != None:
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

def generate_straight_road_y(x_left, x_right, y, direction):
    left_side = scale_image(pygame.image.load("images/road/road_left.png"), 1)
    left_side_mask = pygame.mask.from_surface(left_side)
    right_side = scale_image(pygame.image.load("images/road/road_right.png"), 1)
    right_side_mask = pygame.mask.from_surface(right_side)
    images_masks.append((left_side_mask, x_left, y))
    images_masks.append((right_side_mask, x_right, y))
    images.append((left_side, (x_left, y)))
    images.append((right_side, (x_right, y)))
    y += direction*left_side.get_height()
    return y


def road_collision(road_image, x, y):
    mask = pygame.mask.from_surface(road_image)
    for i in images_masks:
        image_x = i[1]
        image_y = i[2]
        offset = (int(-image_x+x + 50), int(-image_y+y))
        img_mask = i[0]
        poi = mask.overlap(img_mask, offset)
        if poi != None:
            return False
    else:
        return True


def generate_map(main_car):
    x_left = main_car.x_pos - 50
    x_right = main_car.x_pos + 90

    road_turn = False
    road_orientation = -1 # -1 = up(1=down) if road_turn == false else -1=left,1=right
    #first step
    y = generate_straight_road_y(
        x_left, x_right, main_car.y_pos, road_orientation
        # direction -1 = up; +1 = down
    )
    # y_left, y_right = generate_straight_road_x(main_car)
    
    y_left, y_right = y, y
    

    # while True:
    
    # if y > 0 and y < height:
    direction = 1#random.randint(1,3)
        # 1 - left, 2 - straight, 3 - right
    if direction == 1:
        left_side = scale_image(pygame.image.load("images/road/Turn_left_1.png"), 1)
        if x_left - left_side.get_width() <= 2*left_side.get_width():
            # no widht for turn left
            # then turn right
            right_side = scale_image(pygame.image.load("images/road/Turn_right_1.png"), 1)
            if road_collision(right_side, x_right, y_right):
                road_orientation = 1
                road_turn = True

                left_side_up = scale_image(pygame.image.load("images/road/road_left.png"), 1)
                images.append((left_side_up, (x_left, y_left)))
                images_masks.append((pygame.mask.from_surface(left_side_up), x_left, y_left))
                y_left -= left_side_up.get_height()

                left_side_turn = scale_image(pygame.image.load("images/road/Turn_right_1.png"), 1.4)
                images.append((left_side_turn, (x_left, y_left)))
                images_masks.append((pygame.mask.from_surface(left_side_turn), x_left, y_left, 0)) #50 - x fix
                x_left += left_side_turn.get_width()
                y_left -= left_side_turn.get_height()
                
            else:
                print('huit')
        else:
            print('git add left turn')
    # else:
    #     break
        
            
        # break

def gameloop():
    main_car = MainCar(
        x_pos=100, y_pos=height-100,
        max_vel=10, rotation_vel=4,
        image_path='images/car_images/car_small_up.png', 
        acceleration=0.2, start_vel=0,
        angle=0
        )
    generate_map(main_car)
    while run:
        clock.tick(FPS)

        window.fill((0,0,0))
        draw_objects(images)
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
            # game_info
            )
        pygame.display.update()

        
    pygame.quit()




if __name__ == "__main__":
    gameloop()
