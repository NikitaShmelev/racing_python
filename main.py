import pygame
import time
import random
import sys
from map_generation import Map
from car import MainCar
from finish_congrats import congrats

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
programIcon = pygame.image.load('images/icon_20x20.png')
pygame.display.set_icon(programIcon)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def handle_collision(main_car, images_masks, finish):
    for mask in images_masks:
        x_fix = mask[3]
        y_fix = mask[4]
        if main_car.collide(mask=mask[0], x=mask[1], y=mask[2], x_fix=x_fix, y_fix=y_fix) != None:
            main_car.bounce()
    mask = finish['mask']
    x = finish['x']
    y = finish['y']
    x_fix = finish['x_fix']
    y_fix = finish['y_fix']
    if main_car.collide(mask=mask, x=x, y=y, x_fix=x_fix, y_fix=y_fix) != None:
        return True
    else:
        return False


def move_player(player_car):
    # ruch samochodu we wszystkie strony + jazda
    keys = pygame.key.get_pressed()
    moved = False
    ###################################
    # ride style for Nikita
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
    if keys[pygame.K_SPACE]:
        if player_car.vertical > 0:
            player_car.y_pos += -5
        elif player_car.vertical < 0:
            player_car.y_pos += 5
        if player_car.horizontal > 0:
            player_car.x_pos += -5
        elif player_car.horizontal < 0:
            player_car.x_pos += 5
    if not moved:
        player_car.reduce_speed()
    #########################################

    ###################################
    # ride style for Krzysiek
    # if keys[pygame.K_w]:
    #     moved = True
    #     player_car.move_forward()
    # if keys[pygame.K_s]:
    #     moved = True
    #     player_car.move_backward()
    # if keys[pygame.K_SPACE]:
    #     if player_car.vertical > 0:
    #         player_car.y_pos += -5
    #     elif player_car.vertical < 0:
    #         player_car.y_pos += 5
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
    ################################################

    if player_car.time == 0 and player_car.vel != 0:
        player_car.time = time.time()
    if keys[pygame.K_r]:
        return False
    return True


def draw_objects(images):
    for img, pos in images:
        window.blit(img, pos)


def gen_road(direction, map, test=False):
    # direction = random.randint(1,3)
    # testowa funkcja
    # nie dołączać do sprawozdania
    road = ''
    if direction == 3:  # right
        if map.check_turn(road_turn=True, orientation=1):
            map.horizontal_turn()
            road = 'R'
        else:
            print('ADD FINISH HERE')
    elif direction == 1:  # left
        if map.check_turn(road_turn=True, orientation=-1):
            map.horizontal_turn()
            road = 'L'
        else:
            print('ADD FINISH HERE')
    return road


def generate_map(window, map):
    map.generate_start()
    map.step_straight_y()

    ##########################
    # testowy kawałek
    # nie nie dołączać do sprawozdania
    road = 'U'
    # road += gen_road(3, map)
    # road += gen_road(1, map)
    # road += gen_road(3, map)
    # road += gen_road(3, map)

    # road += gen_road(3, map)

    # road += gen_road(3, map)

    # road += gen_road(1, map)
    # road += gen_road(1, map)
    ##############################
    # 1 - left, 2 - right

    while True:
        direction = random.choice([1, 2])
        if direction == 2:
            if map.check_turn(True, 1):
                map.horizontal_turn()
            else:
                return map.generate_finish()
        if direction == 1:
            if map.check_turn(True, -1):
                map.horizontal_turn()
            else:
                return map.generate_finish()


def create_objects():
    x_pos = random.choice([i for i in range(50, width-140-50, 140)])
    y_pos = height-140*1
    main_car = MainCar(
        x_pos=x_pos, y_pos=y_pos,
        max_vel=5, rotation_vel=4,
        image_path='images/car_images/car_small_up.png',
        acceleration=0.2*5, start_vel=0, angle=0
    )
    map = Map(
        x_left=main_car.x_pos - 50,  # x lewej strony drogi
        y_left=main_car.y_pos,  # y lewej strony drogi
        x_right=main_car.x_pos + 90,
        y_right=main_car.y_pos,
        window_width=width,
        window_height=height,
    )
    return main_car, map


def gameloop():
    main_car, map = create_objects()
    finish = generate_map(window, map)
    ##########################
    # testowy kawałek
    # nie nie dołączać do sprawozdania
    print(
        f'x_left = {map.x_left}, x_right = {map.x_right}\n'
        f'y_left = {map.y_left}, y_right = {map.y_right}\n'
        f'orientation = {map.road_orientation}, road_turn = {map.road_turn}\n'
        f'was_left = {map.was_left}, was_right={map.was_right}\n'
        f'previos = {map.previos}'
    )
    ##########################
    while run:
        clock.tick(FPS)  # dzięki tej funkcji gra działa wolniej
        window.fill((0, 0, 0))  # zaciera ślady obiektów które poruszają się
        map.draw_map(window)  # służy do rysowania mapy
        main_car.draw(window)  # narysowanie w oknie samochodzika
        for event in pygame.event.get():  # funkcja służy do zamykania gry
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not move_player(main_car):
            time.sleep(0.05)
            main_car, map = create_objects()
            finish = generate_map(window, map)
            print(
                f'x_left = {map.x_left}, x_right = {map.x_right}\n'
                f'y_left = {map.y_left}, y_right = {map.y_right}\n'
                f'orientation = {map.road_orientation}, road_turn = {map.road_turn}\n'
                f'was_left = {map.was_left}, was_right={map.was_right}\n'
                f'previos = {map.previos}'
            )
        ##############################
        # testowy kawałek
        # nie nie dołączać do sprawozdania
        # for i in range(0, width, 140):
        #     pygame.draw.line(window, 'red', (i, 0), (i, height))
        #     drawText(f'{i}', pygame.font.SysFont(
        #         "comicsans", 40), window, i, 10)
        # for i in range(0, height, 140):
        #     pygame.draw.line(window, 'red', (0, i), (width, i))
        #     drawText(f'{i}', pygame.font.SysFont(
        #         "comicsans", 40), window, 10, i)
        # drawText(f'{round(main_car.x_pos)=} {round(main_car.y_pos)=} {round(main_car.vel)=}',
        #          MAIN_FONT, window, 308, 900)  # draw some text in window
        ##############################
        if main_car.time != 0:
            # timer output edit
            current_time = time.time() - main_car.time
            if current_time > 60:
                current_time = f'{str(current_time//60)} min {(str(round(current_time%60,2)))}s'
            else:
                current_time = str(round(current_time, 2)) + ' s'
            # draw game time
            drawText(f'{current_time}',
                     MAIN_FONT, window, 0, 45)
        if handle_collision(main_car, map.images_masks, finish):
            
            congrats(window, main_car, drawText, MAIN_FONT)
            drawText(f'{current_time}', MAIN_FONT, window, 750, 500)
            main_car, map = create_objects()
            finish = generate_map(window, map)
            pygame.display.update()
            time.sleep(5)
        pygame.display.update()


if __name__ == "__main__":
    gameloop()
