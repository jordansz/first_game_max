# fixes to make, make the cannon class and bomb class inherit from a base class.
# make max a player object so moving the screen doesn't affect gameplay.
# figure a better way to figure out enemy picture to use.  (pickle doesn't work)
# window size might be to big for smaller screens.
# winning screen 

# Client class holds the games logic, bringing together the multiplayer game
# For it to work both clients (players essentially) run this script after starting 
# the server, images are loaded in, set to desired size attributes and the game begins

import pygame
import math
from network import Network
import text_to_speach as ts
from player import *
from p_bomb import *
from cannon import *
from _thread import *
import sys, os
from noise_player import *
import random


#basic pop up window stuff, size of the screen and initialization of pygame module

pygame.init()
width = 1482
height = 915
win = pygame.display.set_mode((width, height))
bg = pygame.image.load('assets/game_background.png').convert()
bg = pygame.transform.scale(bg, (1482, 915))
pygame.display.set_caption("T")


# start to load in all the images

entity_standing = pygame.image.load('assets/standing.png')
entity_walking_left = [pygame.image.load('assets/L1.png').convert_alpha(), pygame.image.load('assets/L2.png').convert_alpha(), pygame.image.load('assets/L3.png').convert_alpha(),
            pygame.image.load('assets/L4.png').convert_alpha(), pygame.image.load('assets/L5.png').convert_alpha(), pygame.image.load('assets/L6.png').convert_alpha(),
            pygame.image.load('assets/L7.png').convert_alpha(), pygame.image.load('assets/L8.png').convert_alpha(), pygame.image.load('assets/L9.png').convert_alpha()]

entity_walking_right = [pygame.Surface] * 9       #same size list as walking left list


# Must change some of the images to be properly laid out and the correct size

entity_standing = pygame.transform.scale(entity_standing, (120, 120))
i = 0
while i < 9:
    entity_walking_left[i] = pygame.transform.scale(entity_walking_left[i], (120, 120))
    entity_walking_right[i] = pygame.transform.flip(entity_walking_left[i], True, False)
    i += 1


# loading in the dropping asset images

cannon = pygame.image.load('assets/cannon.png').convert_alpha()
cannon = pygame.transform.scale(cannon, (150, 244))
cannonL = pygame.transform.flip(cannon, True, False)


cannon_ball = pygame.image.load('assets/cannon_ball.png').convert_alpha()
cannon_ballR = pygame.transform.scale(cannon_ball, (50, 50))
cannon_ballL = pygame.transform.flip(cannon_ballR, True, False)
explosion = pygame.image.load('assets/explosion.png')
explosion = pygame.transform.scale(explosion, (75, 75))

cannon_r = [cannon_ballR, explosion]

cannon_l = [cannon_ballL, explosion]

poop_emoji = pygame.image.load('assets/poop_emoji.png').convert_alpha()
poop_bomb = [pygame.image.load('assets/poop1.png').convert_alpha(), pygame.image.load('assets/poop2.png').convert_alpha(), pygame.image.load('assets/poop3.png'),
             pygame.image.load('assets/poop4.png').convert_alpha(), pygame.image.load('assets/poop5.png'), pygame.image.load('assets/poop6.png')]
i = 0
while i < 6:
    poop_bomb[i] = pygame.transform.scale2x(poop_bomb[i])
    i += 1
poop_emoji = pygame.transform.scale(poop_emoji, (90, 150))


# sounds
pygame.mixer.init()


# RANDNOISE = pygame.USEREVENT
# pygame.time.set_timer(RANDNOISE, 10000)  #random noise every 8 seconds


# Setting up the fonts to be rendered to certain text aswell as declaring the chat box
chat_box = pygame.Rect(10, height - 44, 273, 34)
p1_font = pygame.font.Font(pygame.font.get_default_font(), 40)
p2_font = pygame.font.Font(pygame.font.get_default_font(), 40)
p1_ready_font = pygame.font.Font(pygame.font.get_default_font(), 40)
p2_ready_font = pygame.font.Font(pygame.font.get_default_font(), 40)

intro_font = pygame.font.Font(pygame.font.get_default_font(), 40)
controls_font = pygame.font.Font(pygame.font.get_default_font(), 40)
wait_p2 = controls_font.render("Waiting for Player 2", True, (255, 255, 255))
wait_p = controls_font.render("Waiting for you", True, (255, 255, 255))
intro_text = controls_font.render("Welcome!", True, (255, 255, 255))
controls_text = controls_font.render("Controls.              Cooldown.", True, (255, 255, 255))
controls1_text=controls_font.render("Left click:    Poop Bomb.     2s", True, (255, 255, 255))
controls2_text=controls_font.render("Right click: Cannon shot.    3s", True, (255, 255, 255))
waiting = controls_font.render("Waiting for two players, hit enter to ready up", 1, (255, 255, 255))


# put this in class sometime
def check_cooldown(x, y):
    if x < y and x != 0:
        x += 1
    elif x <= y:
        x = 0
    return x


# At the top of the screen both players scores will be displayed with this function

def display_score(p, p2, win):
    p1_score = p1_font.render(f"Player 1 score: {p.get_score()}", True, (0, 0, 0))
    p2_score = p2_font.render(f"Player 2 score: {p2.get_score()}", True, (0, 0, 0))
    win.blit(p1_score, (20, 20))
    win.blit(p2_score, (width - 350, 20))



# This function is used to redraw the game screen each frame.
# It utilizes multiple other display functions from different classes.

def redraw_window(win, player, player2, mouse_pos, text, bomb1, bomb2, cannon1, cannon2):
    win.blit(bg, (0, 0))
    display_score(player, player2, win)
    draw_player(player)
    draw_player(player2)

    chat_box.w = text.get_width() + 10
    if mouse_pos[0] > 10 and mouse_pos[0] < 283 and mouse_pos[1] > height - 44 and mouse_pos[1] < height - 10:  # mouse is in text box
        pygame.draw.rect(win, (255, 255, 0), chat_box, 2)
    else:
        pygame.draw.rect(win, (255, 0, 0), chat_box, 2)

    if bomb1.get_status():
        bomb1.draw(win)
    if bomb2.get_status():
        bomb2.draw(win)

    if cannon1.get_status():
        cannon1.draw(win)
    if cannon2.get_status():
       cannon2.draw(win)


# Collision checking between falling assets and the ai is done here
# I need to fix this and add a basic ai class, possibly a seperate or child class to player

def collision(max_img, max_x, max_y, bomb1, bomb2, cannon1, cannon2, p, p2):
    max_mask = pygame.mask.from_surface(max_img)
    bomb1_mask = bomb1.get_mask()
    bomb2_mask = bomb2.get_mask()
    cannon1_mask = cannon1.get_mask()
    cannon2_mask = cannon2.get_mask()

    if bomb1_mask is not None:
        offset_x = max_x - bomb1_mask[1]
        offset_y = max_y - bomb1_mask[2]
        if max_mask.overlap(bomb1_mask[0], (offset_x, offset_y)) != None:
            p.increase_score(1)

    if bomb2_mask is not None:
        offset_x = max_x - bomb2_mask[1]
        offset_y = max_y - bomb2_mask[2]
        if max_mask.overlap(bomb2_mask[0], (offset_x, offset_y)) != None:
            p2.increase_score(2)

    if cannon1_mask is not None:
        offset_x = max_x - cannon1_mask[1]
        offset_y = max_y - cannon1_mask[2]
        if max_mask.overlap(cannon1_mask[0], (offset_x, offset_y)) != None:
            p.increase_score(2)

    if cannon2_mask is not None:
        offset_x = max_x - cannon2_mask[1]
        offset_y = max_y - cannon2_mask[2]
        if max_mask.overlap(cannon2_mask[0], (offset_x, offset_y)) != None:
            p2.increase_score(2)


# If a player types text it is played using this function

def play_text(p1, p2):                  #may cause problems if both clients taunt at the same time
    text1 = p1.get_text()
    text2 = p2.get_text()
    if text1:       # not empty
        start_new_thread(ts.play_mp3, (text1, 1))
        p1.set_text("")
        os.remove("taunt.mp3")
    elif text2:
        start_new_thread(ts.play_mp3, (text2, 2))
        p2.set_text("")
        os.remove("taunt2.mp3")


# Once there is a winner, all of the player attributes are set back to default, and a little bit of 
# text is displayed who won or lost on either players screen

def winner(win, p, p2, n, winner):
    p.revert()
    p2.revert()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(5)
        win.blit(bg, (0, 0))
        display_intro_text(p, p2, win)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if winner == 0 and p.get_id() == 0:
            winner_text = controls_font.render("You Win!", 1, (r,g,b))
            win.blit(winner_text, (((width // 2) - (winner_text.get_width() // 2)), 500))
        elif winner == 0 and p.get_id() == 1:
            loser_text = controls_font.render("You Lose!", 1, (r,g,b))
            win.blit(loser_text, (((width // 2) - (loser_text.get_width() //2)), 500))
        elif winner == 1 and p2.get_id() == 0:
            loser_text = controls_font.render("You Lose!", 1, (r, g, b))
            win.blit(loser_text, (((width // 2) - (loser_text.get_width() // 2)), 500))
        if winner == 1 and p2.get_id() == 1:
            winner_text = controls_font.render("You Win!", 1, (r,g,b))
            win.blit(winner_text, (((width // 2) - (winner_text.get_width() // 2)), 500))

        pygame.display.update()
        p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # second cond is right enter (<-|)
                    p.set_on(True)
                    print()
        if p.get_on() and p2.get_on():
            # print("here starting again")
            run = False
            main(p, p2, n)


# draw_player draws each given players image
# To achieve this the players basic attributes, direction (left, right) and current possition
# aswell as the player id, to correctly draw a player

def draw_player(p):
    x, y, left, right, index, id = p.get_draw_specs()
    if left and not right and id == 0:
        win.blit(entity_walking_left[index], (x, y))
    elif not left and right and id == 0:
        win.blit(entity_walking_right[index], (x, y))
    elif not left and not right and id == 0:
        win.blit(entity_standing, (x, y))
    elif left and not right and id == 1:
        win.blit(entity_walking_left[index], (x, y))
    elif not left and right and id == 1:
        win.blit(entity_walking_right[index], (x, y))
    else:
        win.blit(entity_standing, (x, y))


# At the start of the game this function will display the rules and
# the status of which players are ready or not

def display_intro_text(p, p2, win):
    win.blit(intro_text, (((width // 2) - (intro_text.get_width() //2)), 10))
    win.blit(controls1_text, (((width // 2) - (controls1_text.get_width() // 2)), 200))
    win.blit(controls2_text, (((width // 2) - (controls2_text.get_width() // 2)), 250))
    if not p.get_on() and not p2.get_on():
        win.blit(waiting, (((width // 2) - (waiting.get_width() // 2)), 50))  #+ (waiting.get_width() // 2))
    elif p.get_on() and not p2.get_on():
        win.blit(wait_p2, (((width // 2) - (wait_p2.get_width() // 2)), 50))
    elif not p.get_on() and p2.get_on():
        win.blit(wait_p, (((width // 2) - (wait_p.get_width() // 2)), 50))


# intro before main game loop to display the wanted graphics, aswell as sets up the Network for communication

def intro():
    n = Network()
    p = n.getP()
    run = True
    while run:
        p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # second cond is right enter (<-|)
                    p.set_on(True)


        win.blit(bg, (0, 0))
        draw_player(p)
        draw_player(p2)
        display_intro_text(p, p2, win)
        pygame.display.update()
        if p.get_on() and p2.get_on():
            run = False
            main(p, p2, n)
    pygame.quit()


# main starts all the games initial rules and player setup,
# once thats done the main game loop takes place and the game begins

def main(p, p2, n): 
    p2.set_win_status(False)       
    global run
    run = True
    clock = pygame.time.Clock()
    user_text = ""
    enter_count = 0
    mwalk_count = 0
    frame_walk = 5
    m_left = False
    m_right = True
    bomb1 = P_Bomb(0, 0, 20, False, 1, poop_emoji, poop_bomb)
    bomb2 = P_Bomb(0, 0, 20, False, 2, poop_emoji, poop_bomb)
    bomb1.revert(win)
    bomb2.revert(win)
    cannon1 = Cannon(0, 0, 12, False, 1, cannon, cannon_r)
    cannon1.revert(win)        #this fixed the problem where the first  drop wasn't moving like i wanted
    cannon2 = Cannon(0, 0, 12, False, 2, cannonL, cannon_l)
    cannon2.revert(win)
    s1_cd = 0
    s2_cd = 0
    n2_cd = 0
    n1_cd = 0
    sound_index = 0
    max_stat = 0        

    # text font stuff
    font = pygame.font.SysFont("monospace", 32)
    text = font.render("Enter to taunt", 1, (0, 255, 255))

    while p.get_on():
        clock.tick(27)      # must be 27 for images to be rendered in correct walking order
        p2 = n.send(p)
        mouse_pos = pygame.mouse.get_pos()
        # there has to be a better way to check scores???!!

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:            # second cond is right enter (<-|)
                    enter_count += 1
                if enter_count == 1:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                    text = font.render(user_text, 1, (0, 255, 255))

                elif enter_count == 2:
                    enter_count = 0
                    p.set_text(user_text)
                    user_text = ""
                    text = font.render("Enter to taunt", 1, (0, 255, 255))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and s1_cd == 0:
                s1_cd = 1
                x, y = p.get_cords()
                p.set_poop_status(True)
                bomb1.set_status(True)      # may not need
                bomb1.set_cords(x, y)


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and n1_cd == 0:
                n1_cd = 1
                x, y = p.get_cords()
                p.set_shooting_status(True)
                cannon1.set_status(True)
                cannon1.set_cords(x, y)
                fall_dist = 700 - p.get_height() - y
                angle = 20 / fall_dist
                if m_right:
                    cannon1.set_direction_photos(cannon, cannon_r)
                    cannon1.set_angle(angle)
                else:
                    cannon1.set_direction_photos(cannonL, cannon_l)
                    cannon1.set_dir(True)
                    cannon1.set_angle(-1 * angle)

        p.set_poop_status(bomb1.get_status())
        p.set_shooting_status(cannon1.get_status())
        if p2.get_poop_status() and s2_cd == 0:
            s2_cd = 1
            x, y = p2.get_cords()
            bomb2.set_cords(x, y)
            bomb2.set_status(True)

        if p2.get_shooting_status() and n2_cd == 0:
            n2_cd = 1
            x, y = p2.get_cords()
            cannon2.set_status(True)
            cannon2.set_cords(x, y)
            fall_dist = 700 - p2.get_height() - y
            angle = 20 / fall_dist
            if m_right:
                cannon2.set_direction_photos(cannon, cannon_r)
                cannon2.set_angle(angle)
            else:
                cannon2.set_direction_photos(cannonL, cannon_l)
                cannon2.set_dir(True)
                cannon2.set_angle(-1 * angle)



        # to ensure theres no spam dropping stuff these are placed here
        
        s1_cd = check_cooldown(s1_cd, 53)
        s2_cd = check_cooldown(s2_cd, 53)
        n1_cd = check_cooldown(n1_cd, 80)
        n2_cd = check_cooldown(n2_cd, 80)


        play_text(p, p2)
        p.move()
        redraw_window(win, p, p2, mouse_pos, text, bomb1, bomb2, cannon1, cannon2)
        win.blit(text, (12, height - 44))

        if mwalk_count + 1 >= 27:
            mwalk_count = 0

        mwalk_count += 1
        if m_right and frame_walk < width - 100:            #frame_walk is used to figure out x pos
            win.blit(entity_walking_right[mwalk_count // 3], (frame_walk, 740))
            max_stat = 0
            frame_walk += 8
        elif m_right and frame_walk >= width - 900:                     #why does 900 work??? to tired now, figure out later
            win.blit(entity_walking_right[mwalk_count // 3], (frame_walk, 740))
            max_stat = 0
            m_right = False
            m_left = True
            frame_walk -= 8
        elif m_left and frame_walk > 20:
            win.blit(entity_walking_left[mwalk_count // 3], (frame_walk, 740))
            max_stat = 1
            frame_walk -= 8
        else:
            win.blit(entity_walking_left[mwalk_count // 3], (frame_walk, 740))
            max_stat = 1
            m_left = False
            m_right = True
            frame_walk += 8

        if max_stat == 0:            # jordan find a better way to do this
            collision(entity_walking_left[mwalk_count // 3], frame_walk, 740, bomb1, bomb2, cannon1, cannon2, p, p2)
        else:
            collision(entity_walking_right[mwalk_count // 3], frame_walk, 740, bomb1, bomb2, cannon1, cannon2, p, p2)

        pygame.display.update()

        if p.get_score() >= 1 and p.get_id() == 0:
            print("here2")
            run = False
            p.set_on(False)
            p2.set_on(False)
            winner(win, p, p2, n, 0)
            return
        elif p.get_score() >= 1 and p.get_id() == 1:
            run = False
            p.set_on(False)
            p2.set_on(False)
            winner(win, p, p2, n, 1)
            return
        elif p2.get_score() >= 1 and p2.get_id() == 1:
            print("heren")
            run = False
            p.set_on(False)
            p2.set_on(False)
            winner(win, p, p2, n, 1)
            return

        elif p2.get_score() >= 1 and p2.get_id() == 0:
            print("here3")
            run = False
            p.set_on(False)
            p2.set_on(False)
            winner(win, p, p2, n, 0)
            return


# intro leads to the start of the initial lobby

intro()
