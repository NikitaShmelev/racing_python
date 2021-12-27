from utils import *

class Map:
    def __init__(self, x_left, y_left, x_right, y_right):
        self.images = []
        self.images_masks = []
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.y_right = y_right
        self.road_orientation = -1 # -1 = up(1=down) if road_turn == false else -1=left,1=right
        self.road_turn = False
        self.changed = False

        self.right_side_up_img = scale_image(pygame.image.load('images/bumpers/Road_14x14_right_side.png'), 1)
        self.left_side_up_img = scale_image(pygame.image.load('images/bumpers/Road_14x14_left_side.png'), 1)
        self.bottom_image = scale_image(pygame.image.load('images/bumpers/Road_2x14_bottom_bumper.png'), 1)
        self.top_image = scale_image(pygame.image.load('images/bumpers/Road_2x14_top_bumper.png'), 1)
    def draw_map(self, window):
        for img, pos in self.images:
            window.blit(img, pos)

    def step_straight_y(self, left=True, right=True):
        # road up 
        if left:
            self.y_left = self.generate_straight_road_y(
                                self.x_left, self.y_left, self.road_orientation, 
                                60, -80, side_img=self.left_side_up_img
                                )
        # młody fix image size
        if right:          
            młody_fix = -self.right_side_up_img.get_width()

            self.y_right = self.generate_straight_road_y(
                                self.x_right + młody_fix, self.y_right, self.road_orientation, 
                                -220, -80, side_img=self.right_side_up_img
                                )
    
    def generate_straight_road_y(self, x, y, direction, x_fix, y_fix, side_img):
        side_mask = pygame.mask.from_surface(side_img)
        self.images_masks.append((side_mask, x, y, x_fix, y_fix))
        self.images.append((side_img, (x, y)))
        y += direction*side_img.get_height()
        return y

    def __change_direction__(self, road_turn, n):
        if self.road_turn == road_turn:
            self.road_turn = False if road_turn else True
            self.road_orientation *= n
        else:
            self.road_turn = road_turn
            self.road_orientation *= n

    def __check_window__(self, width, height):
        if self.road_turn and self.road_orientation == 1:
            #right
            if self.x_right + self.right_side_up_img.get_width()*2 <= width:
                if self.y_right > -100:
                    return True
            elif self.x_right - self.right_side_up_img.get_width()*2 >= 0:
                self.road_orientation = -1
                self.changed = True
                return True

        elif self.road_turn and self.road_orientation == -1:
            if self.x_right - self.right_side_up_img.get_width()*2 >= 0:
                if self.y_left > -100:
                    self.changed = True
                    return True
        elif not self.road_turn and self.road_orientation == -1:
            # up
            pass
        elif not self.road_turn and self.road_orientation == 1:
            # down
            pass
        return False
    

    def check_turn(self, width, height, road_turn, n):
        self.__change_direction__(road_turn, n)
        if self.__check_window__(width, height):
            # add road_collision
            if self.__road_collision__(
                                self.bottom_image,
                                self.x_right, self.y_right):
                return True
        else:
            pass


    def __generate_straight_road_x__(self, x, y, road_orientation, x_fix, y_fix, img):
        self.images.append((img, (x, y)))
        self.images_masks.append((pygame.mask.from_surface(img), x, y, 
                                                                        x_fix, y_fix)) 
                                                                        #x_fix; y fix
        x += road_orientation*img.get_width()
        return x

    def step_straight_x(self, left=True, right=True, 
                        y_fix=False, x_fix=False):
        '''x_fix = {x_right: some, x_left: some}'''
        '''y_fix = {y_right: some, y_left: some}'''
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
                                                self.road_orientation,
                                                x_col_fix, y_col_fix, self.bottom_image)
        if left:
            print(self.changed)
            if self.changed:
                x_col_fix = -70
                y_col_fix = 60
            else:
                x_col_fix = -60
                y_col_fix = 100
            self.x_left = self.__generate_straight_road_x__(
                                                self.x_left, self.y_left, 
                                                self.road_orientation,
                                                x_col_fix, y_col_fix, self.top_image)

    def horizontal_turn(self):
        if self.road_turn and self.road_orientation == 1:
            #right
            self.step_straight_y(right=False) # left side up\
            y_fix={
                'y_left': -self.images[-1][0].get_height(), 
                'y_right': self.images[-1][0].get_height()
                }
            self.step_straight_x(right=False, y_fix=y_fix)
            self.step_straight_x()
            self.changed = False
        elif self.road_turn and self.road_orientation == -1:
            self.step_straight_y(left=False)
            y_fix={
                'y_left': self.images[-1][0].get_height(), 
                'y_right': self.images[-1][0].get_height()
                }
            x_fix={
                'x_right': -self.bottom_image.get_width(), 
                'x_left': -self.bottom_image.get_width()
            }
            self.step_straight_x(left=False, x_fix=x_fix, y_fix=y_fix)
            self.step_straight_x()
            self.changed = False
            
            
       
# def generate_straight_road_x(x, y, road_orientation, x_fix, y_fix):
#     right_side_turn = scale_image(pygame.image.load("images/bumpers/Road_2x14_top_bumper.png"), 1)
#     images.append((right_side_turn, (x, y)))
#     images_masks.append((pygame.mask.from_surface(right_side_turn), x, y, 
#                                                                     x_fix, y_fix)) 
#                                                                     #x_fix; y fix
#     x += road_orientation*right_side_turn.get_width()
#     return x

    def __road_collision__(self, road_image, x, y):
        mask = pygame.mask.from_surface(road_image)
        for i in self.images_masks:
            image_x = i[1]
            image_y = i[2]
            offset = (int(-image_x+x), int(-image_y+y))
            img_mask = i[0]
            poi = mask.overlap(img_mask, offset)
            if poi != None:
                return False
        else:
            return True