from pygame import *
from models import *
from random import *
from time import time as t

window = display.set_mode((700,500))
background = transform.scale(image.load('media/images/galaxy.jpg'),window.get_size())
window.blit(background,(0,0))

mixer.init()
font.init()
text_font = font.Font(None,40)
kill_text = font.Font(None,40)
lifes_text = font.Font(None,40)
win_text = font.Font(None,80)
lose_text = font.Font(None,80)
reload_text = font.Font(None,40)
reload_win = reload_text.render('Перезарядка',True,(42, 173, 77,0.1))
restart = Button(220,320,'media/images/restart.png',240,60,0,window)
start = Button(280,150,'media/images/play.png',170,60,0,window)
exit_game = Button(280,250,'media/images/exit.png',170,60,0,window)
exit_menu = Button(250,420,'media/images/menu.png',170,60,0,window)
mixer.music.load('media/music/space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('media/music/fire.ogg')
fire_sound.set_volume(0.2)
player: Player = Player(250,420,'media/images/rocket.png',60,85,4,window)

def draw_enemy():
    enemies = sprite.Group()
    x = 0
    y = 0
    x_step = window.get_size()[0] // 3
    y_step = -50
    for i in range(9):
        cord_x = randint(x,x + x_step)
        enemy = Enemy(cord_x,y,'media/images/ufo.png',50,50,randint(1,3),window)
        x += x_step
        if i % 3 == 0:
            y += y_step
            x = 0
        enemies.add(enemy)
        enemy.count(player)
    return enemies

def draw_meteor():
    meteors = sprite.Group()
    m_x = 0
    y_m = 0
    x_m_step = window.get_size()[0] // 3
    for i in range(3):
        cord_x_m = randint(m_x,m_x + x_m_step)
        meteor = Enemy(cord_x_m,-50,'media/images/asteroid.png',100,100,randint(1,2),window)
        m_x += x_m_step
        meteors.add(meteor)
    return meteors


game_flag = False
reload_flag = True
wait_flag = True
flag = True
menu_flag = True

clock = time.Clock()
FPS = 60
while flag:
    if menu_flag:
        window.blit(background,(0,0))
        enemies = draw_enemy()
        meteors = draw_meteor()
        start.draw()
        exit_game.draw()
        if start.check():
            game_flag = True
            lifes = 3
            kills = 0
            player.counter = 0
            player.rect.x = 250
            win_count = 20
            menu_flag = False
        if exit_game.check():
            flag = False
    if restart.check():
        game_flag = True
        enemies = draw_enemy()
        meteors = draw_meteor()
        lifes = 3
        kills = 0
        player.counter = 0
        player.rect.x = 250
    if exit_menu.check():
        menu_flag = True
    if game_flag:
        window.blit(background,(0,0))
        player.draw()
        player.move()
        if reload_flag:
            if wait_flag:
                wait_s_time = t()
                wait_flag = player.fire(fire_sound)
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
                window.blit(background,(0,0))
                window.blit(lose,(140,200))
                game_flag = False
                restart.draw()
                exit_menu.draw()
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