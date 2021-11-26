import pygame
from pygame.transform import rotate
pygame.init() #initializes the Pygame
from pygame.locals import* #import all modules from Pygame

width = 1680
height = 1030
screen = pygame.display.set_mode((width, height))
over_font = pygame.font.Font('freesansbold.ttf', 64)

#changing title of the game window
pygame.display.set_caption('Racing Beast')

def game_over_text():
    over_text = over_font.render("Pojebało pana", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

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
    

   
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_speed += 0.5
            
                if event.key == pygame.K_LEFT:
                    x_speed -= 0.5
                
                if event.key == pygame.K_UP:
                    if rotate_down:
                        maincar = pygame.transform.rotate(maincar, 180)
                        rotate_down, rotate_up = False, True
                    y_speed -= 0.5
                    
                if event.key == pygame.K_DOWN:
                    if rotate_up:
                        maincar = pygame.transform.rotate(maincar, 180)
                        rotate_up, rotate_down = False, True
                    y_speed += 0.5



        #CHANGING COLOR WITH RGB VALUE, RGB = RED, GREEN, BLUE 
        screen.fill((0,0,0))


        #displaying our main car
        screen.blit(maincar,(maincarX,maincarY))

       
        #updating the values
        maincarX += x_speed
        if maincarX <= -10:
            maincarX = -10
            x_speed = 0
            game_over_text()
            
        elif maincarX >= width - x_coords_fix:
            maincarX = width - x_coords_fix
            x_speed = 0
            game_over_text()
        
        maincarY += y_speed
        if maincarY <= 0:
            maincarY = 0
            y_speed = 0
            game_over_text()
        elif maincarY >= height - y_coords_fix:
            maincarY = height - y_coords_fix
            y_speed = 0
            game_over_text()

        pygame.display.update()

if __name__ == "__main__":
    gameloop()