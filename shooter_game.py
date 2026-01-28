from pygame import *
from models import *

window = display.set_mode((700,500))
background = transform.scale(image.load('media/images/galaxy.jpg'),window.get_size())
window.blit(background,(0,0))

player: Player = Player(250,400,'media/images/rocket.png',75,100,1,window)



flag = True
clock = time.Clock()
while flag:
    window.blit(background,(0,0))
    player.draw()
    player.move()
    display.update()
    clock.tick()
    events = event.get()
    for i in events:
        if i.type == QUIT:
            flag = False