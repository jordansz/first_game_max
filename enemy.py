import pygame

pygame.init()

class Enemy():
    def __init__(self, x, y, s_img, walkingL, walkingR):
        self.frame = x
        self.y = y
        self.left = False
        self.right = False
        self.walk_count = 0
        self.s_img = s_img
        self.walkingL = walkingL
        self.walkingR = walkingR

    def set_frame(self, x):
        self.frame = x

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        self.walk_count += 1
        if self.right and self.frame < win.get_width() - 100:
            win.blit(self.walkingR[self.walk_count // 3], (self.frame, self.y))
            self.frame += 6
        elif self.right and self.frame >= win.get_width() - 900:                     #why does 900 work??? figure out later
            win.blit(self.walkingR[self.walk_count // 3], (self.frame, self.y))
            self.right = False
            self.left = True
            self.frame -= 6
        elif self.left and self.frame > 20:
            win.blit(self.walkingL[self.walk_count // 3], (self.frame, self.y))
            self.frame -= 6
        else:
            win.blit(self.walkingL[self.walk_count // 3], (self.frame, self.y))
            self.left = False
            self.right = True
            self.frame += 6