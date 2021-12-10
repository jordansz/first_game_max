import pygame

def play_rand_noise(file):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    return

