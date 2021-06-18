import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()



size = (1000,1000)
ruutu = pygame.display.set_mode(size)

pelaaja = pygame.image.load("pelaaja.png")
pahis = pygame.image.load("pahis.png")
tausta = pygame.image.load("mcdonalds.png")


#tekstit
pelifontti = pygame.font.SysFont("Impact", 30)
pelivari = (0, 255, 85)
loppuvari = (252, 3, 44)
loppufontti = pelifontti

#musa
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

amogus = pygame.mixer.Sound("amogus.mp3")
suru = pygame.mixer.Sound("sad.mp3")



pelx = 200
pely = 200
pelinopes = 20
vihunopes = 10
hp = 5
on_tehty = False
ennatys = 0.0


vihut = [
    [100,100],
    [200,200],
    [150,150]
]

#ennatyksen lukeminen
with open("ennatys","r") as tiedosto:
    luettu = tiedosto.read()
    ennatys = int(luettu)



# aika jutut
kello = pygame.time.Clock()
fps = 30
alkuaika = pygame.time.get_ticks()


pelaaja = pygame.transform.scale(pelaaja, (10*12,15*12))
pahis = pygame.transform.scale(pahis, (128,128))
tausta = pygame.transform.scale(tausta, size)

def piira():
    ruutu.fill((0,0,0))
    ruutu.blit(tausta, (0,0))
    ruutu.blit(pelaaja, (pelx,pely))

    #vihollisten piirto
    for vihu in vihut:
        ruutu.blit(pahis,vihu)
        
        
    # teksti piirto
    hpteksti = pelifontti.render("elämät:"+str(hp), True, pelivari)
    ruutu.blit(hpteksti, (600,600))

    aika = pygame.time.get_ticks()-alkuaika
    aika = pelifontti.render("aika:"+str(aika/1000), True, pelivari)
    ruutu.blit(aika, (200,200))

    ennatysteksti = pelifontti.render("ennatys:"+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (600,400))
    
    



def peruna():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.quit:
            pygame.quit()
            sys.exit()

def pelilogiikka():
    global pelx, pely, hp, ennatys, vihunopes
    aika = pygame.time.get_ticks()-alkuaika 
    napit = pygame.key.get_pressed()
    if napit [pygame.K_d]:
        pelx += pelinopes
    if napit [pygame.K_a]:
        pelx -= pelinopes
    if napit [pygame.K_s]:
        pely += pelinopes
    if napit [pygame.K_w]:
        pely -= pelinopes
    
    #vihollisten kiihdyttaminen
    if (aika/1000) % 10 == 0: # joka kymmenne sekkaa
        vihunopes += 0.05






    if aika > ennatys:
        ennatys = aika
    
    

    for vihu in vihut:
        if vihu[1]+128 > pely and vihu[1] < pely+15*12:
            if vihu[0]+128 > pelx and vihu[0] < pelx+10*12:
                vihu[1] = 0
                hp -= 1
                vihu[0] = random.randint(10, 11000-32-10)


    if pelx  < 0:
        pelx = 0
    if pelx  > 1000-10*12:
        pelx = 1000-10*12
    
    for vihu in vihut: 
        vihu[1] += vihunopes
        if vihu[1] > 1000:
            vihu[1] = 0
            vihu[0] = random.randint(10, 1000-128-10)


def gameover():
    global on_tehty
    if not on_tehty:
        on_tehty = True
        pygame.mixer.music.stop()
        suru.play

        with open("ennatys","w") as tiedosto:
            tiedosto.write(str(ennatys))


    ruutu.fill(loppuvari)
    ennatysteksti = loppufontti.render("ennatys:"+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (600,400))
    teksti = loppufontti.render("hävisit pelin", True, pelivari)
    ruutu.blit(teksti, (30,60))




while True:
    peruna()

    if hp <= 0:
        gameover()
    else:
        pelilogiikka()
        piira()


    pygame.display.flip()
    kello.tick(fps)






