import time
import pygame


def congrats(window, main_car, drawText, MAIN_FONT):
    window.fill((0, 0, 0))
    pygame.display.update()
    drawText(f'HANDS UP AND DONT TOUCH KEYBOARD',
             MAIN_FONT, window, 540, 280)
    window.fill((0, 0, 0))
    pygame.display.update()

    # W
    pygame.draw.line(window, 'red', (480, 140), (750, 840))
    pygame.draw.line(window, 'red', (750, 840), (840, 610))
    pygame.draw.line(window, 'red', (840, 610), (930, 840))
    pygame.draw.line(window, 'red', (930, 840), (1200, 140))

    # ### P
    pygame.draw.line(window, 'red', (1200, 140), (1020, 140))
    pygame.draw.line(window, 'red', (1020, 140), (1020, 840))
    # main_car.angle = 135
    time.sleep(0.1)
    # draw w
    k = 2.5925
    b = -1104.40
    main_car.angle = -159
    for x in range(480-5, 755, 5):
        # x = y
        main_car.x_pos = x
        main_car.y_pos = k*x + b
        main_car.draw(window=window)
        time.sleep(0.01)
        pygame.display.update()
    k = -2.55
    b = 2752.5
    main_car.angle = -21.38
    for x in range(750, 845, 5):
        main_car.x_pos = x - 50
        main_car.y_pos = k*x + b
        main_car.draw(window=window)
        time.sleep(0.01)
        pygame.display.update()
    k = +2.55
    b = -1532
    main_car.angle = 21.38 + 180
    for x in range(840, 935, 5):
        main_car.x_pos = x - 20
        main_car.y_pos = k*x + b
        main_car.draw(window=window)
        time.sleep(0.01)
        pygame.display.update()

    k = -2.5925
    b = 3151.025
    main_car.angle = 159 + 180
    for x in range(930 - 40, 1205, 5):
        main_car.x_pos = x
        main_car.y_pos = k*x + b
        main_car.draw(window=window)
        time.sleep(0.01)
        pygame.display.update()

    # draw p
    main_car.angle = 90
    main_car.y_pos = 110
    for x in range(1200, 935, -5):
        main_car.x_pos = x
        main_car.draw(window=window)
        time.sleep(0.01)
        pygame.display.update()

    main_car.x_pos = 990
    main_car.angle = 180
    for y in range(50, 845, 5):
        main_car.y_pos = y
        main_car.draw(window=window)
        time.sleep(0.001)
        pygame.display.update()
    
