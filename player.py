import pygame
pygame.init()


class Player():
    def __init__(self, x, y, width, height, color, img, id):
        self.standing = None
        self.x = x
        self.y = y
        self.width = width
        self.on = False
        self.height = height
        self.color = color
        self.img = img
        self.rect = (x, y, width, height)
        self.vel = 11
        self.text = ""
        self.pooping = False
        self.shooting = False
        self.e_frame = 20
        self.score = 0
        self.walk_count = 0
        self.left = False
        self.right = False
        self.id = id
        self.win = False
        self.win_img = ''

    def revert(self):
        self.win_img = ''
        self.left = False
        self.right = False
        self.score = 0
        self.e_frame = 20
        self.on = False
        self.text = ""
        self.pooping = False
        self.shooting = False
        if self.id == 0:
            #print("reverted p1")
            self.x = 20
            self.y = 20
        elif self.id ==1:
            #print("reverted p2")
            self.x = 1350
            self.y = 20

    def get_id(self):
        return self.id

    def set_win_status(self,x):
        self.win = x

    def set_win_img(self, x):
        self.win_img = x

    def get_win_img(self):
        return self.win_img

    def get_win_status(self):
        return self.win

    def increase_score(self, x):
        self.score += x

    def get_score(self):
        return self.score

    def set_standing(self, x):
        self.standing = x

    def set_on(self, x):
        self.on = x

    def get_on(self):
        return self.on

    def get_shooting_status(self):
        return self.shooting

    def set_shooting_status(self, x):
        self.shooting = x

    def get_poop_status(self):
        return self.pooping

    def set_poop_status(self, x):
        self.pooping = x

    def get_height(self):
        return self.height

    def set_img(self, img):
        self.img = img

    def get_poop_bool(self):
        return self.pooping

    def set_pooping(self, x):
        self.pooping = x

    def set_text(self, text):
        self.text = text

    def set_cords(self, x, y):
        self.x = x
        self.y = y

    def get_cords(self):
        return (self.x, self.y)


    def get_text(self):
        return self.text


    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def draw_enemy(self,win):
        self.enemy.draw(win)

    def get_draw_specs(self):
        index = self.walk_count // 3
        return self.x, self.y, self.left, self.right, index, self.id

    def move(self):
        #print("here")
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x - self.vel >= 0:
            self.x -= self.vel
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x + self.width + 8 < 1482:
            self.x += self.vel
            self.left = False
            self.right = True
        elif keys[pygame.K_UP] and self.y - self.vel > 0:
            self.y -= self.vel
            self.left = False
            self.right = False
        elif keys[pygame.K_DOWN] and self.y + self.vel + self.height < 500:
            self.y += self.vel
            self.left = False
            self.right = False
        else:
            self.left = False
            self.right = False
            self.walk_count = 0
        self.walk_count += 1

        # self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
