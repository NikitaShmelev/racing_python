from utils import *
from random import randint


class Map:
    def __init__(self, x_left, y_left, x_right, y_right,
                 window_width, window_height):
        self.images = []
        self.images_masks = []
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.y_right = y_right
        # -1 = up(1=down) if road_turn == false else -1=left,1=right
        self.road_orientation = -1
        self.road_turn = False
        self.changed = False

        self.was_right = False
        self.was_left = False

        self.window_width = window_width
        self.window_height = window_height
        self.right_side_up_img = scale_image(pygame.image.load(
            'images/bumpers/Road_14x2_right_bumper.png'), 1)
        self.left_side_up_img = scale_image(pygame.image.load(
            'images/bumpers/Road_14x2_left_bumper.png'), 1)
        self.bottom_image = scale_image(pygame.image.load(
            'images/bumpers/Road_2x14_bottom_bumper.png'), 1)
        self.top_image = scale_image(pygame.image.load(
            'images/bumpers/Road_2x14_top_bumper.png'), 1)
        self.img_width = self.bottom_image.get_width()
        self.img_height = self.left_side_up_img.get_height()
        self.previos = None

    def draw_map(self, window):
        # (img, (x, y), orientation)
        for item in self.images:
            img = item[0]
            pos = item[1]
            window.blit(img, pos)

    def step_straight_y(self, left=True, right=True, extra_fix=0, test=False,
                        imgs=False):
        if left:
            if imgs:
                img = imgs['left']
                młody_fix = -20
            else:
                img = self.left_side_up_img
                młody_fix = 0
            self.y_left = self.generate_straight_road_y(
                self.x_left + młody_fix, self.y_left, self.road_orientation,
                60, -50, side_img=img)
        if right:
            # młody fix image size
            if imgs:
                img = imgs['right']
                młody_fix = extra_fix
            else:
                młody_fix = -20
                img = self.right_side_up_img
            self.y_right = self.generate_straight_road_y(
                self.x_right + młody_fix, self.y_right, self.road_orientation,
                50, -40, side_img=img)

    def generate_straight_road_y(self, x, y, direction, x_fix, y_fix, side_img):
        side_mask = pygame.mask.from_surface(side_img)
        self.images_masks.append((side_mask, x, y, x_fix, y_fix))
        self.images.append((side_img, (x, y)))
        y += direction*side_img.get_height()
        return y

    def __change_direction__(self, road_turn, orientation):
        if self.road_orientation == -1 and self.road_turn == False:
            self.previos = 'up'
            # up dir
            if self.road_orientation == road_turn and self.road_turn == orientation:
                self.road_orientation = -1
                self.road_turn = False
            elif road_turn == True and orientation == 1:
                # change direction frop up to right
                self.road_orientation = 1
                self.road_turn = True
            elif road_turn == True and orientation == -1:
                # change direction frop up to left
                self.road_orientation = -1
                self.road_turn = True

        elif self.road_orientation == 1 and self.road_turn == False:
            self.previos = 'down'
            # down dir
            if self.road_orientation == road_turn and self.road_turn == orientation:
                self.road_orientation = 1
                self.road_turn = False
            elif road_turn == True and orientation == 1:
                # change direction frop down to left
                # (but was recieved right)
                self.road_orientation = -1
                self.road_turn = True
            elif road_turn == True and orientation == -1:
                # change direction frop down to right
                # (but was recieved left)
                self.road_orientation = 1
                self.road_turn = True
        elif self.road_orientation == -1 and self.road_turn == True:
            self.previos = 'left'
            # left dir
            if road_turn == True and orientation == -1:
                # double left = down dir
                self.road_orientation = 1
                self.road_turn = False
            elif road_turn == True and orientation == 1:
                # right after left = up dir
                self.road_orientation = -1
                self.road_turn = False
                # self.y_right += self.img_height
                # self.y_left += self.img_height
        elif self.road_orientation == 1 and self.road_turn == True:
            self.previos = 'right'
            # right dir
            if road_turn == True and orientation == 1:
                # double right = down dir
                self.road_orientation = 1
                self.road_turn = False
            elif road_turn == True and orientation == -1:
                # left after right = up dir
                self.road_orientation = -1
                self.road_turn = False

    def __check_bottom__(self):
        if (self.y_right + self.img_height) < self.window_height:
            if (self.y_right + self.img_height) < self.window_height - self.img_height:  # 840
                print(self.y_right + self.img_height, self.window_height)
                # bottom check
                return True
        return False

    def __check_top__(self):
        if (self.y_right - self.img_height) >= 0:
            if (self.y_right - self.img_height) >= 0:
                # top check
                return True
        return False

    def __check_critical_positions__(self):
        if self.y_right == 0 and self.y_left == 0:
            return False
        if self.y_right == self.window_height and self.y_left == self.window_height:
            return False
        if self.x_left == 0 and self.x_right == 0:
            return False
        if self.x_left == self.window_width and self.x_right == self.window_width:
            return False
        return True

    def check_window(self):
        # check place in window for turn
        if not self.__check_critical_positions__():
            print('THIS IS THE END!')
            return False

        if self.road_turn and self.road_orientation == 1:
            # right
            if self.x_right + self.img_width*2 <= self.window_width:
                if self.x_right > self.x_left:
                    if self.__check_top__():
                        return True
                else:
                    if self.__check_bottom__():
                        return True
                return False

            elif self.x_right - self.img_width*2 >= 0:
                self.road_orientation = -1
                self.changed = True
                return True
            else:
                return False
        elif self.road_turn and self.road_orientation == -1:
            # left
            if self.x_right > self.x_left:
                if self.__check_top__():
                    return True
            else:
                if self.__check_bottom__():
                    return True
            return True
        elif not self.road_turn and self.road_orientation == -1:
            # up
            if self.__check_top__():
                print('hmm')
                # top check
                return True
            elif self.__check_bottom__():
                self.road_orientation = 1
                return True
            return False

        elif not self.road_turn and self.road_orientation == 1:
            if self.__check_bottom__():
                return True
            elif self.__check_top__():
                self.road_orientation = -1
                return True
        return False

    def check_turn(self, road_turn, orientation, straight=False):
        """sprawdzanie możliwości do zarkętu"""
        if not straight:
            self.__change_direction__(road_turn, orientation)
        if straight:
            print('XD')
            print(self.road_turn, self.road_orientation)
        if self.check_window():
            # add road_collision
            if self.__all_sides_collision__():
                return True
            return False

        else:
            return False

    def __generate_straight_road_x__(self, x, y, road_orientation, x_fix, y_fix, img):
        if self.road_turn:
            if road_orientation:
                orientation = 'UP'
            else:
                orientation = 'DOWN'
        else:
            if road_orientation:
                orientation = 'RIGHT'
            else:
                orientation = 'LEFT'
        self.images.append(
            (img, (x, y), orientation)
        )
        self.images_masks.append((pygame.mask.from_surface(img), x, y,
                                  x_fix, y_fix))
        # x_fix; y fix
        x += road_orientation*img.get_width()
        return x

    def step_straight_x(self, imgs=False, left=True, right=True,
                        y_fix=False, x_fix=False, orientation_fix=1):
        '''x_fix = {x_right: some, x_left: some}'''
        '''y_fix = {y_right: some, y_left: some}'''
        if not imgs:
            imgs['right'] = self.top_image
            imgs['left'] = self.top_image

        if x_fix:
            self.x_left += x_fix['x_left']
            self.x_right += x_fix['x_right']
        if y_fix:
            self.y_left += y_fix['y_left']
            self.y_right += y_fix['y_right']
        if right:
            if self.changed:
                x_col_fix = -70
                y_col_fix = 100
            else:
                x_col_fix = -70
                y_col_fix = 50
            self.x_right = self.__generate_straight_road_x__(
                self.x_right, self.y_right,
                self.road_orientation*orientation_fix,
                x_col_fix, y_col_fix, imgs['right'])
        if left:
            if self.changed:
                x_col_fix = -70
                y_col_fix = -60
            else:
                x_col_fix = -50
                y_col_fix = 100

            self.x_left = self.__generate_straight_road_x__(
                self.x_left, self.y_left,
                self.road_orientation*orientation_fix,
                x_col_fix, y_col_fix, imgs['left'])

    def horizontal_turn(self, orientation_fix=1, fix=0, test=False):
        imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                'right': self.top_image if self.y_left > self.y_right else self.bottom_image, }
        if self.road_turn and self.road_orientation == 1:
            # right
            if self.x_right > self.x_left:
                if not self.was_right and not self.was_left:
                    self.was_right = True
                elif not self.was_right and self.was_left:
                    self.was_right = True
                elif self.was_right and self.was_left:
                    self.y_left -= self.img_height
                    self.y_right -= self.img_height
                self.step_straight_y(right=False)  # left side up\
                y_fix = {
                    'y_left': -self.img_height,
                    'y_right': self.img_height
                }
                imgs = {'left': self.top_image, }

                if self.y_right > self.y_left:
                    imgs['right'] = self.bottom_image
                else:
                    # self.changed = True
                    imgs['right'] = self.top_image
                self.step_straight_x(right=False, imgs=imgs, y_fix=y_fix)
                self.step_straight_x(imgs=imgs)
                self.changed = False
            else:
                imgs_up = {'right': self.right_side_up_img}
                imgs['left'] = self.top_image
                imgs['right'] = self.top_image
                self.step_straight_y(left=False, imgs=imgs_up, extra_fix=-20)
                self.y_left += self.img_height
                self.x_left -= self.img_width
                self.changed = True
                self.step_straight_x(right=False, imgs=imgs)
                self.y_left -= self.img_height
                self.x_right += self.img_width
                self.step_straight_x(imgs=imgs)
                self.x_right += self.img_width
                self.x_left += self.img_width
                self.changed = False
        elif self.road_turn and self.road_orientation == -1:
            # left
            if self.x_right > self.x_left:
                if not self.was_right and not self.was_left:
                    self.was_left = True

                elif self.was_right and not self.was_left:
                    self.was_left = True
                elif self.was_right and self.was_left:
                    self.y_left -= self.img_height
                    self.y_right -= self.img_height
                self.changed = True
                self.step_straight_y(left=False)  # right side up\
                y_fix = {
                    'y_left': self.img_height,
                    'y_right': self.img_height
                }
                x_fix = {
                    'x_right': -self.img_width,
                    'x_left': -self.img_width
                }
                # imgs={left: ....   right:...}
                imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                        'right': self.top_image if self.y_left > self.y_right else self.bottom_image, }
                self.step_straight_x(left=False, imgs=imgs,
                                     y_fix=y_fix, x_fix=x_fix)
                self.step_straight_x(imgs=imgs)
            else:
                imgs['right'] = self.top_image
                imgs['left'] = self.top_image
                imgs_up = {'left': self.right_side_up_img}
                self.step_straight_y(right=False, imgs=imgs_up)
                self.x_right -= self.img_width
                self.y_left += 2*self.img_height
                self.x_left -= self.img_width
                self.changed = False
                self.step_straight_x(right=False, imgs=imgs)
                self.step_straight_x(imgs=imgs)
                self.x_left += self.img_width
                self.x_right += self.img_width
                self.changed = False

            # self.changed = False
        elif not self.road_turn and self.road_orientation == -1:
            # up
            imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                    'right': self.top_image if self.y_left > self.y_right else self.bottom_image, }
            if self.y_right < self.y_left:
                self.step_straight_x(right=False, imgs=imgs)
                self.x_left += self.img_width
                self.x_right += self.img_width
                self.y_left -= self.img_height
                self.y_right -= self.img_height
                self.step_straight_y()
                self.step_straight_y(right=False)
            else:
                if self.was_right and not self.was_left:
                    self.was_left = True
                elif self.was_left and not self.was_right:
                    self.was_right = True
                imgs['right'] = self.top_image
                self.step_straight_x(left=False, imgs=imgs, orientation_fix=-1)
                self.y_left -= self.img_height
                self.y_right -= self.img_height
                self.step_straight_y(left=False, test=True)
                self.step_straight_y()
                self.y_left += self.img_height
                self.y_right += self.img_height
            if self.previos == 'left':
                self.y_left += self.img_height
                self.y_right += self.img_height

        elif not self.road_turn and self.road_orientation == 1:
            # down
            imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                    'right': self.top_image if self.y_left > self.y_right else self.bottom_image, }
            if self.y_right < self.y_left:
                self.step_straight_x(left=False, imgs=imgs)
                self.y_left -= self.img_height
                self.y_right += self.img_height
                self.step_straight_y()
                self.step_straight_y(right=False)
                self.x_left += self.img_width
                self.x_right -= self.img_width
            elif self.y_right > self.y_left:
                imgs['left'] = self.top_image
                self.step_straight_x(right=False, imgs=imgs)
                self.step_straight_y()
                self.step_straight_y(right=False, test=True)
            elif self.y_right == self.y_left:
                pass

    def __road_collision__(self, road_image, x, y):
        mask = pygame.mask.from_surface(road_image)
        if self.road_turn:
            if self.road_orientation:
                x += 140
        else:
            if self.road_orientation:
                y += 140
        for i in self.images_masks:
            image_x = i[1]
            image_y = i[2]
            img_mask = i[0]
            offset = (int(-image_x+x), int(-image_y+y))
            poi = img_mask.overlap(mask, offset)
            if poi != None:
                return False
        else:
            return True

    def __all_sides_collision__(self):
        if self.__road_collision__(
                self.bottom_image if self.road_turn else self.left_side_up_img,
                self.x_right, self.y_right):
            return True
        self.road_orientation *= -1

        if self.__road_collision__(
                self.bottom_image if self.road_turn else self.left_side_up_img,
                self.x_right, self.y_right):
            return True
        self.road_turn = False if self.road_turn else True
        if self.__road_collision__(
                self.bottom_image if self.road_turn else self.left_side_up_img,
                self.x_right, self.y_right):
            return True
        self.road_orientation *= -1
        if self.__road_collision__(
                self.bottom_image if self.road_turn else self.left_side_up_img,
                self.x_right, self.y_right):
            return True
        return False
