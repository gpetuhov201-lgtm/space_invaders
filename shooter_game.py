from pygame import *

window = display.set_mode((500,500))
background = transform.scale(image.load('media/images/galaxy.jpg'),window.get_size())
window.blit(background,(0,0))




flag = True
clock = time.Clock()
while flag:
    display.update()
    clock.tick()
    events = event.get()
    for i in events:
        if i.type == QUIT:
            flag = False