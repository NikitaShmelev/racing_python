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
    if player_car.time == 0 and player_car.vel != 0:
        player_car = time.time()
    if keys[pygame.K_r]:
        return False
    return True
    # if keys[pygame.K_w]:
    #     moved = True
    #     player_car.move_forward()
    # if keys[pygame.K_s]:
    #     moved = True
    #     player_car.move_backward()
    # if player_car.vel > 0:
    #     if keys[pygame.K_a]:
    #         player_car.rotate(left=True)
    #     if keys[pygame.K_d]:
    #         player_car.rotate(right=True)
    # if player_car.vel < 0:
    #     if keys[pygame.K_a]:
    #         player_car.rotate(right=True)
    #     if keys[pygame.K_d]:
    #         player_car.rotate(left=True)
    # if not moved:
    #     player_car.reduce_speed()
    



def draw_objects(images):
    for img, pos in images:
        window.blit(img, pos)

def gen_road(direction, map, test=False):
    # direction = random.randint(1,3)
    road = ''
    if direction == 3:
        if map.check_turn(True, 1, test=False):
            map.horizontal_turn()
            road += '-R'
        else:
            # break
            print('ADD FINISH HERE')
    elif direction == 1:
        if map.check_turn(True, -1, test=False):
            map.horizontal_turn()
            road += '-L'
        else:
            # break
            print('ADD FINISH HERE')
    else:
        if map.road_turn:
            pass
        else:
            map.y_right -= map.img_height
            map.y_left -= map.img_height
            map.step_straight_y()
            map.y_right += map.img_height
            map.y_left += map.img_height
    return road

def generate_map(main_car, map):
    map.step_straight_y()
    
    # while True:
    
    # if y > 0 and y < height:
    
    road='U'
        # 1 - left, 2 - straight, 3 - right
    test= False
    i = 0
    while True:
        if i == 0:
            direction = random.choice([1,3])
        else:
            direction = random.randint(1,3)
        i += 1
        print(direction)
        if direction == 3:
            if map.check_turn(True, 1, test=test):
                map.horizontal_turn()
                road += '-R'
            else:
                print('ADD FINISH HERE R')
                break
        elif direction == 1:
            if map.check_turn(True, -1, test=test):
                map.horizontal_turn()
                road += '-L'
            else:
                print('ADD FINISH HERE L')
                break
        else:
            if map.road_turn:
                imgs = {'left': map.top_image if map.y_left > map.y_right else map.bottom_image,
                        'right': map.top_image if map.y_left > map.y_right else map.bottom_image,}
                map.step_straight_x(imgs=imgs)
                if map.road_orientation:
                    road += '-R'
                else:
                    road += '-L'
            else:
                map.y_right -= map.img_height
                map.y_left -= map.img_height
                map.step_straight_y()
                map.y_right += map.img_height
                map.y_left += map.img_height
    # road += gen_road(3, map)
    # road += gen_road(1, map)
    # road += gen_road(2, map)
    # road += gen_road(2, map)
    # road += gen_road(3, map)

    # road += gen_road(3, map)
    
    # map.step_straight_y()
    # map.step_straight_y()
        
    
    
#######################################33
    
    
    
    print(road)
    
    
    print(
        f'x_left = {map.x_left} x_right = {map.x_right}\n'
        f'y_left = {map.y_left}, y_right = {map.y_right}\n'
        f'orientation = {map.road_orientation}, road_turn = {map.road_turn}'
        )

def create_objects():
    x_pos = 1450 - 140*6
    y_pos = height-140*1
    main_car = MainCar(
        x_pos=x_pos, y_pos= y_pos,
        max_vel=5, rotation_vel=4,
        image_path='images/car_images/car_small_up.png', 
        acceleration=0.2*5, start_vel=0, angle=0,
        start_pos=(x_pos, y_pos)
        )
    map = Map(
        x_left=main_car.x_pos - 50, #x lewej strony drogi
        y_left=main_car.y_pos,      #y lewej strony drogi
        x_right=main_car.x_pos + 90,
        y_right=main_car.y_pos, 
        window_width=width,
        width_height=height,
    )
    return main_car, map


def gameloop():
    main_car, map = create_objects()
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

        if move_player(main_car):
            pass
        else:
            main_car, map = create_objects()
            generate_map(main_car, map)

        drawText(f'{round(main_car.x_pos)=} {round(main_car.y_pos)=} {round(main_car.vel)=}', 
                    MAIN_FONT, window, 308, 900) # draw some text in window
        
        if main_car.time != 0:
            current_time = time.time() - main_car.time
        # if current_time > 60:
        #     current_time = f'{str(current_time//60)} min {(str(current_time%60))}s'
            drawText(f'{current_time}', 
                        MAIN_FONT, window, 908, 50) 
        for i in range(0, width, 140):
            pygame.draw.line(window, 'red', (i, 0), (i, height))
            drawText(f'{i}', pygame.font.SysFont("comicsans", 40), window, i, 10)
        for i in range(0, height, 140):
            pygame.draw.line(window, 'red', (0, i), (width, i))
            drawText(f'{i}', pygame.font.SysFont("comicsans", 40), window, 10, i)
        
        handle_collision(
            main_car,
            map.images_masks
            # game_info
            ) # crash check
        pygame.display.update()

        
    pygame.quit()




if __name__ == "__main__":
    gameloop()