from gtts import gTTS
import pygame
from pygame import mixer
import playsound
import os


pygame.init()
pygame.mixer.init()

def play_mp3(text, p_num):
    if p_num == 1:
        fp = "taunt.mp3"
    else:
        fp = "taunt2.mp3"

    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)

    myobj.save(fp)
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while mixer.music.get_busy():       #weird fix but best I could find.
        pass
    mixer.music.load("sounds/empty.mp3")
    #os.remove(fp)   # important!!

def play_wav(file):
    pygame.mixer.music.load(file)
    pygame.mixer.musuic.play()
    while mixer.music.get_busy():
        pass
    mixer.music.load("sounds/empty.mp3")

