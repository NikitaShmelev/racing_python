from utils import *

class Map:
    def __init__(self, x_left, y_left, x_right, y_right,
                window_width, width_height):
        self.images = []
        self.images_masks = []
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.y_right = y_right
        self.road_orientation = -1 # -1 = up(1=down) if road_turn == false else -1=left,1=right
        self.road_turn = False
        self.changed = False
        

        self.window_width = window_width
        self.width_height = width_height
        self.right_side_up_img = scale_image(pygame.image.load('images/bumpers/Road_14x14_right_side.png'), 1)
        self.left_side_up_img = scale_image(pygame.image.load('images/bumpers/Road_14x14_left_side.png'), 1)
        self.bottom_image = scale_image(pygame.image.load('images/bumpers/Road_2x14_bottom_bumper.png'), 1)
        self.top_image = scale_image(pygame.image.load('images/bumpers/Road_2x14_top_bumper.png'), 1)
        self.img_width = self.bottom_image.get_width()
        self.img_height = self.left_side_up_img.get_height()

    def draw_map(self, window):
        for img, pos in self.images:
            window.blit(img, pos)

    def step_straight_y(self, left=True, right=True, horizontal_fix=False, test=False):
        # road up
        
        # if self.y_right == self.y_left or extra_fix:
        
        if left:
            self.y_left = self.generate_straight_road_y(
                                self.x_left, self.y_left, self.road_orientation, 
                                60, -80, side_img=self.left_side_up_img)
        if right:
            # młody fix image size     
            młody_fix = -self.img_width
            if test:
                print('sss')
            self.y_right = self.generate_straight_road_y(
                                self.x_right + młody_fix, self.y_right, self.road_orientation, 
                                -220, -60, side_img=self.right_side_up_img)

       
        #                 self.y_left = self.generate_straight_road_y(
        #                                     self.x_left, self.y_left, self.road_orientation, 
        #                                 85, -50, side_img=self.left_side_up_img)
        #                 self.x_right += -self.img_width
        #                 self.y_right = self.generate_straight_road_y(
        #                                     self.x_right, self.y_right, self.road_orientation, 
        #                                     -220, -80, side_img=self.right_side_up_img)
        #                 self.y_right = self.generate_straight_road_y(
        #                                     self.x_right + 0, self.y_right, self.road_orientation, 
        #                                     -220, -80, side_img=self.right_side_up_img)


        #             self.y_left = self.generate_straight_road_y(
        #                                 self.x_left, self.y_left, self.road_orientation, 
        #                                 60, -80, side_img=self.left_side_up_img)
        #             self.y_left = self.generate_straight_road_y(
        #                                 self.x_left + 0, self.y_left, self.road_orientation, 
        #                                 60, -80, side_img=self.left_side_up_img)
  
 

    def generate_straight_road_y(self, x, y, direction, x_fix, y_fix, side_img):
        side_mask = pygame.mask.from_surface(side_img)
        self.images_masks.append((side_mask, x, y, x_fix, y_fix))
        self.images.append((side_img, (x, y)))
        y += direction*side_img.get_height()
        return y

    def __change_direction__(self, road_turn, orientation):
        if self.road_orientation == -1 and self.road_turn == False:
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
            #left dir
            if road_turn == True and orientation == -1:
                # double left = down dir
                self.road_orientation = 1
                self.road_turn = False
            elif road_turn == True and orientation == 1:
                # right after left = up dir
                self.road_orientation = -1
                self.road_turn = False
        elif self.road_orientation == 1 and self.road_turn == True:
            #right dir
            if road_turn == True and orientation == 1:
                # double right = down dir
                self.road_orientation = 1
                self.road_turn = False
            elif road_turn == True and orientation == -1:
                # left after right = up dir
                self.road_orientation = -1
                self.road_turn = False
        

    def __check_window__(self):
        # check place in window for turn
        if self.road_turn and self.road_orientation == 1:
            #right
            if self.x_right + self.img_width*2 <= self.window_width:
                if self.y_right > -100:
                    return True
            elif self.x_right - self.img_width*2 >= 0:
                self.road_orientation = -1
                self.changed = True
                return True
            else:
                return False
        elif self.road_turn and self.road_orientation == -1:
            #left
            if self.x_right - self.img_width*2 >= 0:
                if self.y_left > -100:
                    self.changed = True
                    return True
        elif not self.road_turn and self.road_orientation == -1:
            #up
            if (self.y_right - self.img_height and self.y_right - self.img_height) > -100 + self.img_height:
                #top check
                return True
            
        elif not self.road_turn and self.road_orientation == 1:
            if (self.y_right + self.img_height and self.y_right + self.img_height) < self.width_height:
                # bottom check
                self.road_orientation = 1
                return True
        return False
    

    def check_turn(self, road_turn, orientation, test=False):
        """sprawdzanie możliwości do zarkętu"""
        self.__change_direction__(road_turn, orientation)
        if test:
            print(f'{self.y_left=} {self.y_right=}')
        if self.__check_window__():
            # add road_collision
            if test:
                print(f'{self.y_left=} {self.y_right=}')
            if self.__road_collision__(
                                self.bottom_image,
                                self.x_right, self.y_right):
                if test:
                    print(f'{self.y_left=} {self.y_right=}')
                return True
        else:
            return False
        


    def __generate_straight_road_x__(self, x, y, road_orientation, x_fix, y_fix, img):
        self.images.append((img, (x, y)))
        self.images_masks.append((pygame.mask.from_surface(img), x, y, 
                                                                        x_fix, y_fix)) 
                                                                        #x_fix; y fix
        x += road_orientation*img.get_width()
        return x

    def step_straight_x(self, imgs, left=True, right=True, 
                        y_fix=False, x_fix=False, orientation_fix=1):
        '''x_fix = {x_right: some, x_left: some}'''
        '''y_fix = {y_right: some, y_left: some}'''
        # if self.y_left > self.y_right:
        #     left = True
        # else:
        #     right = True
        # if not self.road_orientation and self.road_orientation == -1:
        #     left, right = right, left
        
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
                y_col_fix = 60
            else:
                x_col_fix = -50
                y_col_fix = 100
                
            self.x_left = self.__generate_straight_road_x__(
                                                self.x_left, self.y_left, 
                                                self.road_orientation*orientation_fix,
                                                x_col_fix, y_col_fix, imgs['left'])
    
    def horizontal_turn(self, orientation_fix=1, fix=0, test=False):
        imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                'right': self.top_image if self.y_left > self.y_right else self.bottom_image,}
        if test:
            print(self.x_right, self.x_left)
        if self.road_turn and self.road_orientation == 1:
            #right
            if self.x_right > self.x_left:
                self.step_straight_y(right=False) # left side up\
                y_fix={
                    'y_left': -self.img_height, 
                    'y_right': self.img_height
                    }
                imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                        'right': self.top_image if self.y_left > self.y_right else self.bottom_image,}
                self.step_straight_x(right=False, imgs=imgs, y_fix=y_fix)
                self.step_straight_x(imgs=imgs)
            else:
                self.step_straight_y(left=False)
                imgs['left'] = self.top_image
                imgs['right'] = self.top_image
                self.y_left += self.img_height
                self.x_left -= self.img_width
                self.changed = True
                self.step_straight_x(right=False, imgs=imgs)
                self.y_right -= self.img_height
                self.x_right += self.img_width
                self.step_straight_x(imgs=imgs)
                self.changed = False
            # self.changed = False
        elif self.road_turn and self.road_orientation == -1:
            #left
            if self.x_right > self.x_left:
                self.step_straight_y(left=False) # right side up\
                y_fix={
                    'y_left': self.img_height, 
                    'y_right': self.img_height
                    }
                x_fix={
                    'x_right': -self.img_width, 
                    'x_left': -self.img_width
                }
                # imgs={left: ....   right:...}
                imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                        'right': self.top_image if self.y_left > self.y_right else self.bottom_image,}
                self.step_straight_x(left=False, imgs=imgs, y_fix=y_fix, x_fix=x_fix)
                self.step_straight_x(imgs=imgs)
            else:
                imgs['right'] = self.top_image
                imgs['left'] = self.top_image
                
                self.step_straight_y(right=False)
                # self.x_right -= self.img_width
                self.x_left -= 2*self.img_width
                self.y_left += self.img_height
                self.y_right += self.img_height
                self.step_straight_x(left=False, imgs=imgs)
                self.step_straight_x(imgs=imgs)

            # self.changed = False
        elif not self.road_turn and self.road_orientation == -1:
            imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                'right': self.top_image if self.y_left > self.y_right else self.bottom_image,}
            
            if self.y_right < self.y_left:
                self.step_straight_x(right=False, imgs=imgs)
                self.x_left += self.img_width
                self.x_right += self.img_width
                self.y_left -= self.img_height
                self.y_right -= self.img_height
                self.step_straight_y()
                self.step_straight_y(right=False)
            else:
                imgs['right'] = self.top_image
                self.step_straight_x(left=False, imgs=imgs, orientation_fix=-1)
                self.y_left -= self.img_height
                self.y_right -= self.img_height
                self.step_straight_y(left=False, test=True)
                self.step_straight_y()

            # if self.x_left < self.x_right:
            
        
            # if self.road_orientation == -1:
            #         self.y_left = self.generate_straight_road_y(
            #                         self.x_left, self.y_left, self.road_orientation, 
            #                         60, -80, side_img=self.left_side_up_img)
            #     else:
            #         młody_fix = -self.img_width
            #         self.y_right = self.generate_straight_road_y(
            #                         self.x_right + młody_fix, self.y_right, self.road_orientation, 
            #                         -220, -60, side_img=self.right_side_up_img)
                
                # self.y_right += self.img_height
        elif not self.road_turn and self.road_orientation == 1:
            imgs = {'left': self.top_image if self.y_left > self.y_right else self.bottom_image,
                'right': self.top_image if self.y_left > self.y_right else self.bottom_image,}
            
            # print(f'{self.y_left=} {self.y_right=}')
            if self.y_right < self.y_left:
                self.step_straight_x(left=False, imgs=imgs)
                self.y_left -= self.img_height
                self.y_right += self.img_height
                self.step_straight_y()
                self.step_straight_y(right=False)
            elif self.y_right > self.y_left:
                imgs['left'] = self.top_image
                self.step_straight_x(right=False, imgs=imgs)
                self.step_straight_y()
                self.step_straight_y(right=False, test=True)
            elif self.y_right == self.y_left:
                pass



            # self.x_right -= self.img_width
                print('right side generated')
            # self.x_left -= self.img_width
            # if self.x_left < self.x_right:
            #     self.x_left += self.img_width
            #     self.x_right += self.img_width
            #     self.y_left -= self.img_height
            #     self.y_right -= self.img_height
            # else:
            #     print('GG')

                # self.x_left -= self.img_width
                # self.y_right += self.img_height
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