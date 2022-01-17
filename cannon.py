# cannon class for the dropping cannon asset, Fires a cannon ball once it hits the ground

import pygame
import math
pygame.init()

class Cannon():
    def __init__(self, x, y, vel, on, id, cannon, shots):
        self.x = x
        self.id = id
        self.on = on
        self.y = y
        self.original = cannon    
        self.cannon = cannon
        self.copy = cannon
        self.shots = shots
        self.vel = vel
        self.frame = 27
        self.frame2 = 0
        self.angle = 0
        self.dir = False
        self.mask = None


# To check for a collision an image of the mask is used

    def get_mask(self):
        return self.mask




    # def set_dir(self, x):
    #     self.dir = x


# set_direction_photos changes the direction the cannon faces, this is based on the direction 
# The ai is walking when its dropped.  For some reason I couldn't get the image to work properly
# so I added an extra cannon image, this problem might be from a draw_cannon somewhere unintended

    def set_direction_photos(self, x, y):
        self.canon = x
        self.original = x
        self.copy = x
        self.shots = y

# returns the velocity, I used this for testing when figuring out how to make the cannon drop
#  and look proper

    def get_vel(self):
        return self.vel     #for testing


# set_angle changes the angle of the cannon image while it drops 

    def set_angle(self, x):
        self.angle = x


# get_indexed_pic is for the cannonball getting fired animation       

    def get_indexed_pic(self, x):
        return self.shots[x]


# get_frame is used as rendering

    def get_frame(self):
        return self.frame

    def get_frame2(self):
        return self.frame2

    def add_frame2(self, x):
        self.frame2 += x

    def add_frame(self, x):
         self.frame += x

    def set_cords(self, x, y):
        self.x = x
        self.y = y

    def get_cords(self):
        return self.x, self.y

    def get_status(self):
        return self.on

    def set_status(self, val):
        self.on = val

    # def rotate_cannon(self):
    #     rotated_cannon = pygame.transform.rotate(self.cannon, self.angle)
    #     return rotated_cannon

    def revert(self):
        self.cannon = self.original
        self.copy = self.original
        self.frame = 0


    def cannon_drop(self):
        self.frame += 1 % 360
        self.cannon = pygame.transform.rotate(self.copy, -1 *self.angle * self.frame * 40)
        self.y += self.vel


# once the cannon hits the ground, shoots it will dissapper
# its attributes are set back to its base initialization

    def revert(self, win):
        win.blit(self.cannon, (-200, -200))
        self.on = False
        self.frame2 = 0
        self.frame = 0
        self.angle = 0
        self.x = 0
        self.y = 0
        self.cannon = self.original
        self.copy = self.original
        self.dir = False
        self.mask = None



    def draw(self, win):
        print(self.frame2)
        if self.y < 700:
            win.blit(self.cannon, (self.x, self.y))
            self.cannon_drop()
        elif self.y >= 700 and self.frame2 < 60:
            load_index = math.ceil((self.frame2 / 100 * 10 // 1))
            win.blit(self.cannon, (self.x, self.y))
            if not self.dir:
                if load_index == 5:
                    win.blit(self.shots[1], (self.x + 450, self.y + 45))
                    self.mask = [pygame.mask.from_surface(self.shots[1]), self.x + 450, self.y + 45]
                else:
                    win.blit(self.shots[0], (self.x + 250 + self.frame2 * 3, self.y + 30))   # draws shot to right + 160 for cannon space
                    if self.frame2 >= 45:
                        self.mask = [pygame.mask.from_surface(self.shots[0]), self.x + 250 + self.frame2 * 3, self.y + 30]
            else:
                if load_index == 5:
                    win.blit(self.shots[1], (self.x - 270, self.y + 45))
                    self.mask = [pygame.mask.from_surface(self.shots[1]), self.x - 270, self.y + 45]
                else:
                    win.blit(self.shots[0], (self.x - 30 - self.frame2 * 3, self.y + 30))
                    if self.frame2 >= 45:
                        self.mask = [pygame.mask.from_surface(self.shots[0]), self.x - 30 - self.frame2 * 3, self.y + 30]
            self.frame2 += 3

        else:
           self.revert(win)
