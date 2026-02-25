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
    
class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        self.draw()
        if self.rect.y < 0:
            self.kill()

class Player(Character):
    bullets = sprite.Group()
    counter = 0
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < self.window.get_size()[0] - self.rect.width:
            self.rect.x += self.speed
    def fire(self,f_sound):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            f_sound.play()
            bullet = Bullet(self.rect.centerx,self.rect.y,'media/images/bullet.png',10,15,2,self.window)
            self.bullets.add(bullet)
            return False
        return True


class Enemy(Character):
    player = None
    def update(self):
        self.draw()
        if self.rect.y < self.window.get_size()[1] - self.rect.height:
            self.rect.y += self.speed
        else:
            self.rect.y = randint(-200,0)
            if self.player:
                self.player.counter += 1
            self.speed = randint(1,3)
    def count(self,player):
        self.player = player


class Button(Character):
    def check(self):
        mouse_pressed = mouse.get_pressed()
        if mouse_pressed[0]:
            return self.rect.collidepoint(mouse.get_pos()[0],mouse.get_pos()[1])
