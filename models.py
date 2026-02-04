from pygame import *
from random import *

class Character(sprite.Sprite):
    def __init__(self,x,y,outfit,w,h,speed,window):
        super().__init__()
        self.window = window
        self.speed = speed
        self.image = transform.scale(image.load(outfit),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        self.window.blit(self.image,(self.rect.x, self.rect.y))

class Player(Character):
    counter = 0
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < self.window.get_size()[0] - self.rect.width:
            self.rect.x += self.speed

class Enemy(Character):
    def update(self):
        self.draw()
        if self.rect.y < self.window.get_size()[1] - self.rect.height:
            self.rect.y += self.speed
        else:
            self.rect.y = randint(-200,0)
            self.player.counter += 1
            self.speed = randint(1,3)
    def count(self,player):
        self.player = player