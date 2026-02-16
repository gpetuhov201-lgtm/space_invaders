from pygame import *
from models import *
from random import *
from time import time as t

window = display.set_mode((700,500))
background = transform.scale(image.load('media/images/galaxy.jpg'),window.get_size())
window.blit(background,(0,0))

font.init()
text_font = font.Font(None,40)
kill_text = font.Font(None,40)
lifes_text = font.Font(None,40)
win_text = font.Font(None,80)
lose_text = font.Font(None,80)
reload_text = font.Font(None,40)
reload_win = reload_text.render('Перезарядка',True,(42, 173, 77,0.1))
x = 0
m_x = 0
y = 0
y_m = 0
x_step = window.get_size()[0] // 3
x_m_step = window.get_size()[0] // 3
y_step = -50
enemies = sprite.Group()
meteors = sprite.Group()
player: Player = Player(250,420,'media/images/rocket.png',60,85,4,window)
for i in range(9):
    cord_x = randint(x,x + x_step)
    enemy = Enemy(cord_x,y,'media/images/ufo.png',50,50,randint(1,3),window)
    x += x_step
    if i % 3 == 0:
        y += y_step
        x = 0
    enemies.add(enemy)
for i in range(3):
    cord_x_m = randint(m_x,m_x + x_m_step)
    meteor = Enemy(cord_x_m,-50,'media/images/asteroid.png',100,100,randint(1,2),window)
    m_x += x_m_step
    meteors.add(meteor)

lifes = 3
kills = 0
win_count = 20
game_flag = True
reload_flag = True
wait_flag = True

flag = True
clock = time.Clock()
FPS = 60
while flag:
    if game_flag:
        window.blit(background,(0,0))
        player.draw()
        player.move()
        if reload_flag:
            if wait_flag:
                wait_s_time = t()
                wait_flag = player.fire()
                if len(player.bullets) >= 10:
                    reload_flag = False
                    s_time = t()
        else:
            e_time = t()
            window.blit(reload_win,(300,450))
            if e_time - s_time >= 5:
                reload_flag = True
        if t() - wait_s_time > 1:
            wait_flag = True
        player.bullets.update()
        enemies.update()
        meteors.update()
        text = text_font.render('Пропущено:' + str(player.counter),True,(235, 52, 52))
        kill_counter = kill_text.render('Сбито:' + str(kills),True,(3, 252, 111))
        win = win_text.render('Вы победили',True,(20, 252, 3))
        lose = lose_text.render('Вы проиграли',True,(252, 3, 3))
        touches = sprite.spritecollide(player, enemies, True)
        meteor_touches = sprite.spritecollide(player,meteors,True)
        touches_enemies  = sprite.groupcollide(player.bullets,enemies,True,True)
        sprite.groupcollide(player.bullets,meteors,True,False)
        if touches or meteor_touches:
            lifes -= 1
            if lifes <= 0:
                window.blit(lose,(120,200))
                game_flag = False
        if len(touches_enemies) > 0:
            cord_x = randint(60,window.get_size()[0])
            enemy = Enemy(cord_x,y,'media/images/ufo.png',50,50,randint(1,3),window)
            enemies.add(enemy)
            enemy.count(player)
            kills += 1
            if kills >= win_count:
                window.blit(win,(120,200))
                game_flag = False
        text = text_font.render('Пропущено:' + str(player.counter),True,(235, 52, 52))
        kill_counter = kill_text.render('Сбито:' + str(kills),True,(3, 252, 111))
        life_counter = lifes_text.render('Жизней осталось:' + str(lifes),True,(240, 252, 3))
        window.blit(text,(30,20))
        window.blit(kill_counter,(350,20))
        window.blit(life_counter,(30,50))
    display.update()
    clock.tick(FPS)
    events = event.get()
    for i in events:
        if i.type == QUIT:
            flag = False