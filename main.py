import pygame
pygame.init() #initializes the Pygame
from pygame.locals import* #import all modules from Pygame
width = 1200
height = 720
screen = pygame.display.set_mode((width, height))

#changing title of the game window
pygame.display.set_caption('Racing Beast')


#defining our gameloop function
def gameloop():

    #setting background image
    # bg = pygame.image.load('car game/bg.png')

    
    # setting our player
    maincar = pygame.image.load('car_small.png')
    maincarX = 350
    maincarY = 495
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
                    y_speed -= 0.5
                    
                if event.key == pygame.K_DOWN:
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
        elif maincarX >= width - x_coords_fix:
            maincarX = width - x_coords_fix
            x_speed = 0
        
        maincarY += y_speed
        if maincarY <= 0:
            maincarY = 0
            y_speed = 0
        elif maincarY >= height - y_coords_fix:
            maincarY = height - y_coords_fix
            y_speed = 0

        pygame.display.update()

if __name__ == "__main__":
    gameloop()