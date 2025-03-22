
from time import time as timer
from random import *
from pygame import *
import sys
import os

def give_me_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

img_background = give_me_path('images/galaxy.jpg')
img_asteroid = give_me_path('images/asteroid.png')
img_bullet = give_me_path('images/bullet.png')
img_rocket = give_me_path('images/rocket.png')
img_ufo = give_me_path('images/ufo.png')

width_screen = 700
height_screen = 500
window = display.set_mode((width_screen, height_screen))
display.set_caption('Шутер')
run = True
finish = False
clock = time.Clock()
background = transform.scale(image.load(img_background), (width_screen, height_screen))
mixer.init()
fire_snd = mixer.Sound(give_me_path('sounds/fire.ogg'))
missed_score = 0
score = 0
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
font.init()
font = font.Font(give_me_path('fonts/Sigmar-Regular.ttf'), 40)

lose = font.render('You LOSE!!!!!!!!', True, red)
win = font.render('You WIN!!!!!!!!!!', True, green)
rel_txt = font.render('WAIT, Reloading...', True, red)

mixer.music.load(give_me_path('sounds/space.ogg'))
mixer.music.set_volume(0.5)
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, path, x, y, width, height, speed):
        sprite.Sprite.__init__(self, )
        self.image = transform.scale(image.load(path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def shot(self):
        patron = Bullet(img_bullet, self.rect.centerx - 2, self.rect.y, 5, 10, 7)
        patrones.add(patron)
        
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width_screen - 80:
            self.rect.x += self.speed
        
class Enemy(GameSprite):
    def update(self):
        global missed_score
        self.rect.y += self.speed
        if self.rect.y >= height_screen :
            self.rect.y = 0
            random_x = randint(0, width_screen - 99)
            self.rect.x = random_x
            missed_score += 1
            missed = font.render('missed: ' + str(missed_score), True, white)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

patrones = sprite.Group()
enemies = sprite.Group()
asteroides = sprite.Group()

for i in range(5):
    random_speed = randint(1, 2)
    random_x = randint(0, width_screen - 99)
    enemy = Enemy(img_ufo, random_x, -10, 99, 50, random_speed)
    enemies.add(enemy)

for i in range(2):
    random_speed = randint(1, 2)
    random_x = randint(0, width_screen - 99)
    asteroid = Enemy(img_asteroid, random_x, -10, 50, 50, random_speed)
    asteroides.add(asteroid)

space_ship = Player(img_rocket, 325, 440, 50, 50, 10)

ammo = 5
rel_time = False 
count = font.render('score: ' + str(score), True, white)

while run:
    for kaktus in event.get():
        if kaktus.type == QUIT:
            run = False
        if kaktus.type == KEYDOWN:
            if kaktus.key == K_SPACE:
                if ammo != 0 and not rel_time:
                    space_ship.shot()
                    fire_snd.play()
                    ammo -= 1 
                if ammo == 0 and not rel_time:
                    rel_time = True
                    st_time = timer()
                        
    if not finish:
        window.blit(background, (0, 0))
        space_ship.reset()
        space_ship.update()
        enemies.update()
        patrones.update()
        asteroides.update()
        asteroides.draw(window)
        enemies.draw(window)
        patrones.draw(window)
        if sprite.groupcollide(enemies, patrones, True, True):
            score += 1
            random_speed = randint(1, 1)
            random_x = randint(0, width_screen - 99)
            enemy = Enemy(img_ufo, random_x, -50, 99, 50, random_speed)
            enemies.add(enemy)
            count = font.render('score: ' + str(score), True, white)
            if score >= 10:
                window.blit(win, (200, 220))
                finish = True
        if missed_score >= 10 or sprite.spritecollide(space_ship, enemies, True) or sprite.spritecollide(space_ship, asteroides, True):
            finish = True
            window.blit(lose, (200, 220))
        if rel_time:
            window.blit(rel_txt, (250, 0))
            now_time = timer()
            if now_time - st_time >= 3:
                rel_time = False
                ammo = 5
        missed = font.render('missed: ' + str(missed_score), True, white)
        window.blit(missed, (0, 40))
        window.blit(count, (0, 0))
        display.update()
        clock.tick(60)
        

















