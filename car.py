import pygame
import math
from utils import *
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
        # score check 
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