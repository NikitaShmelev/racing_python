import pygame
import time
import random
import math, sys
from map_generation import Map
from car import MainCar
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()
over_font = pygame.font.Font('freesansbold.ttf', 26)
run = True
FPS = 60
width = 1680
height = 980
window = pygame.display.set_mode((width, height))
TEXTCOLOR = (255, 255, 255)
clock = pygame.time.Clock()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def handle_collision(main_car, images_masks):
    for mask in images_masks:
        x_fix = mask[3]
        y_fix = mask[4]
        if main_car.collide(mask=mask[0], x=mask[1], y=mask[2], x_fix=x_fix, y_fix=y_fix) != None:
            main_car.bounce()


def move_player(player_car):
    #ruch samochodu we wszystkie strony + jazda
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

    # if keys[pygame.K_w]:
    #     moved = True
    #     player_car.move_forward()
    #     if keys[pygame.K_a]:
    #         player_car.rotate(left=True)
    #     if keys[pygame.K_d]:
    #         player_car.rotate(right=True)
    # if keys[pygame.K_s]:
    #     moved = True
    #     player_car.move_backward()
    #     if keys[pygame.K_a]:
    #         player_car.rotate(right=True)
    #     if keys[pygame.K_d]:
    #         player_car.rotate(left=True)
    # if not moved:
    #     player_car.reduce_speed()

def draw_objects(images):
    for img, pos in images:
        window.blit(img, pos)


def generate_map(main_car, map):
    map.step_straight_y()
    map.step_straight_y()
    map.step_straight_y()
    map.step_straight_y()
    # map.step_straight_y()
    # map.step_straight_y()
    # while True:
    
    # if y > 0 and y < height:
    direction = 1#random.randint(1,3)
    
        # 1 - left, 2 - straight, 3 - right
    if direction == 3:
        if map.check_turn(True, -1):
            if map.road_turn:
                
                map.horizontal_turn()
            else:
                
                map.step_straight_y()
        else:
            pass
    elif direction == 1:
        if map.check_turn(True, 1):
            if map.road_turn:
                map.horizontal_turn()
            else:
                map.step_straight_y()
        else:
            pass
    else:
        map.step_straight_y()
            # change direction 

############################################################
    # DONE
    ### turn left after right turn 
    # direction = 1
    # if direction == 1:
    #     print('here')
    #     if map.check_turn(True, 1):
    #         if map.road_turn:
    #             map.horizontal_turn()
    #         else:
    #             print('here')

    #             map.step_straight_y(left=False, right=False)

    #     else:
    #         print('ADD FINISH HERE')
############################################################

    ### turn right after left turn
    direction = 3
    if direction == 3:
        print(map.road_turn, map.road_orientation)
        if map.check_turn(True, 1):

            if map.road_turn:
                map.horizontal_turn()
            else:
                print('git!!!')
                map.step_straight_y(left=False, right=False)

        else:
            print('nie git')


def gameloop():
    # while True:
    #     x_pos = random.randint(100, width-70)
    #     if x_pos + 90 < width - 70:
    #         break
    #     elif  x_pos - 50 > 100:
    #         break
    #     else:
    #         continue 
    x_pos = 1450 - 140*7
    y_pos = height-100
    main_car = MainCar(
        x_pos=x_pos, y_pos= y_pos,
        max_vel=5, rotation_vel=4,
        image_path='images/car_images/car_small_up.png', 
        acceleration=0.2*5, start_vel=0, angle=0)
    map = Map(
        x_left=main_car.x_pos - 50, #x lewej strony drogi
        y_left=main_car.y_pos,      #y lewej strony drogi
        x_right=main_car.x_pos + 90,
        y_right=main_car.y_pos, 
        window_width=width,
        width_height=height,
    )

    generate_map(main_car, map)
    while run:
        clock.tick(FPS) #dzięki tej funkcji gra działa wolniej

        window.fill((0,0,0)) #zaciera ślady obiektów które poruszają się

        map.draw_map(window) #służy do rysowania mapy
        main_car.draw(window) #narysowanie w oknie samochodzika

        for event in pygame.event.get(): #funkcja służy do zamykania gry
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_player(main_car)

        drawText(f'{round(main_car.x_pos)=} {round(main_car.y_pos)=}', MAIN_FONT, window, 828, 0)
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