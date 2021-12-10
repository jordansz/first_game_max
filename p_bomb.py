import math
import pygame

pygame.init()


class P_Bomb():
    COOLDOWN = 30

    def __init__(self, x, y, vel, on, id, img, poop_bomb):
        self.x = x
        self.id = id
        self.on = on
        self.y = y
        self.img = img
        self.poop_bomb = poop_bomb
        self.vel = vel
        self.cool_down_counter = 0
        self.frame = 0
        self.mask = None


    def get_mask(self):
        return self.mask

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

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        else:
            self.cool_down_counter += 1

    def drop(self):
        if self.cool_down_counter == 0:
            self.cool_down_counter = 1

    def move(self):
        self.cooldown()     #update cooldown
        self.y += self.vel

    def revert(self, win):
        win.blit(self.img, (-200, -200))
        self.x = 0
        self.y = 0
        self.on = False
        self.frame = 0
        self.mask = None

    def draw(self, win):
        if self.y < 800:
            win.blit(self.img, (self.x, self.y))
            self.move()

        elif self.y >= 800 and self.frame < 60:
            #print("here " + str(self.y), ", frame: " + str(self.frame))
            dookie_index = math.ceil((self.frame / 100 * 10) // 1)     # ex. frame 1-10 will be indexed to 0, 11=20 to 1, probably a better way
            win.blit(self.poop_bomb[dookie_index], (self.x, self.y - 100))
            if self.frame >= 45:
                self.mask = [pygame.mask.from_surface(self.poop_bomb[dookie_index]), self.x, self.y - 100]
            self.frame += 5
        else:
            self.revert(win)

    # def draw(self, win):
    #     self.on = True
    #     clock = pygame.time.Clock()
    #     while self.y < 800:
    #         clock.tick(60)
    #         # print("pooping")
    #         win.blit(self.emoji, (self.x, self.y))
    #         self.move(self.vel)
    #         pygame.display.update()
    #     frame = 0
    #     while frame < 60:
    #         clock.tick(60)
    #         dookie_index = math.ceil((frame / 100 * 10) // 1)     # ex. frame 1-10 will be indexed to 0, 11=20 to 1, probably a better way
    #         frame += 3
    #         win.blit(self.poop_bomb[dookie_index], (self.x - 13, self.y - 70))
    #         pygame.display.update()
    #     return
