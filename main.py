import pygame
from pygame.transform import rotate
pygame.init() #initializes the Pygame
from pygame.locals import* #import all modules from Pygame

width = 1680
height = 1030
TEXTCOLOR = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
over_font = pygame.font.Font('freesansbold.ttf', 64)

#changing title of the game window
pygame.display.set_caption('Racing Beast')

# def lower_speed_to_zero(x_speed, y_speed):
#     x_speed = 0
#     y_speed = 0


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def game_over_text():
    over_text = over_font.render("Pojebało pana", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#defining our gameloop function
def gameloop():

    #setting background image
    # bg = pygame.image.load('car game/bg.png')

    
    # setting our player
    maincar = pygame.image.load('car_small.png')
    maincarX = 350
    maincarY = 495
    rotate_down, rotate_up = False, True
    x_speed = 0
    y_speed = 0
    
    x_coords_fix = 100
    y_coords_fix = 180
    
    rotate_angle = 0
    max_angle = 20
    

    font = pygame.font.SysFont(None, 30)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if y_speed != 0:
                        if rotate_angle > -max_angle:
                            rotate_angle -= 1
                            maincar = rot_center(pygame.image.load('car_small.png'), rotate_angle)
                        x_speed += 0.5
                    
            
                if event.key == pygame.K_LEFT:
                    if y_speed != 0:
                        if rotate_angle < max_angle:
                            rotate_angle += 1
                            maincar = rot_center(pygame.image.load('car_small.png'), rotate_angle)
                        x_speed -= 0.5
                
                if event.key == pygame.K_UP:
                    # if rotate_down:
                    # if not y_speed:
                    #     maincar = pygame.transform.rotate(maincar, 180)
                            
                            # rotate_down, rotate_up = False, True
                    
                    y_speed -= 0.1
                    

                    
                if event.key == pygame.K_DOWN:
                    # if rotate_up:
                    # if not y_speed:
                    #     maincar = pygame.transform.rotate(maincar, 180)
                            # rotate_up, rotate_down = False, True
                    y_speed += 0.5
            print(rotate_angle)


        #CHANGING COLOR WITH RGB VALUE, RGB = RED, GREEN, BLUE 
        screen.fill((0,0,0))


        #displaying our main car
        screen.blit(maincar,(maincarX,maincarY))

       
        #updating the values
        maincarX += x_speed
        if rotate_angle > 0:
            if rotate_angle < max_angle:
                rotate_angle += 0.01
                maincar = rot_center(pygame.image.load('car_small.png'), rotate_angle)
        elif rotate_angle < 0:
            if rotate_angle > -max_angle:
                rotate_angle -= 0.01
                maincar = rot_center(pygame.image.load('car_small.png'), rotate_angle)
        if maincarX <= -10:
            maincarX = -10
            x_speed, y_speed = 0, 0.1
            game_over_text()
            
        elif maincarX >= width - x_coords_fix:
            maincarX = width - x_coords_fix
            x_speed, y_speed = 0, 0.1
            game_over_text()
        
        maincarY += y_speed
        if maincarY <= 0:
            maincarY = 0
            x_speed, y_speed = 0, 0
            game_over_text()
        elif maincarY >= height - y_coords_fix:
            maincarY = height - y_coords_fix
            x_speed, y_speed = 0, 0
            game_over_text()

        drawText('x speed: %s' % (x_speed), font, screen, 128, 0)
        drawText('y speed: %s' % (y_speed), font, screen, 128, 20)
        drawText('rotate angle: %s' % (rotate_angle), font, screen, 128, 40)
        pygame.display.update()

if __name__ == "__main__":
    gameloop()