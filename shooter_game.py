from pygame import *
from models import *
from random import *

window = display.set_mode((700,500))
background = transform.scale(image.load('media/images/galaxy.jpg'),window.get_size())
window.blit(background,(0,0))

font.init()
text_font = font.Font(None,60)
x = 0
y = 0
x_step = window.get_size()[0] // 3
y_step = -50
enemies = sprite.Group()
player: Player = Player(250,420,'media/images/rocket.png',60,85,4,window)
for i in range(9):
    cord_x = randint(x,x + x_step)
    enemy = Enemy(cord_x,y,'media/images/ufo.png',50,50,randint(1,3),window)
    print(cord_x,y,x_step)
    x += x_step
    if i % 3 == 0:
        y += y_step
        x = 0
    enemies.add(enemy)
    enemy.count(player)
print(len(enemies))



flag = True
clock = time.Clock()
FPS = 60
while flag:
    window.blit(background,(0,0))
    player.draw()
    player.move()
    player.fire()
    player.bullets.update()
    enemies.update()
    text = text_font.render('Пропущено:' + str(player.counter),True,(235, 52, 52))
    window.blit(text,(50,50))
    display.update()
    clock.tick(FPS)
    events = event.get()
    for i in events:
        if i.type == QUIT:
            flag = False