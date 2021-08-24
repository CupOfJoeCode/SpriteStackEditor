import pygame as pg
from math import *

HUE_TABLE = pg.Surface((1,360))
for hue in range(360):
    r = cos(radians(hue))/2 + 0.5
    g = sin(radians(hue))/2 + 0.5
    b = -cos(radians(hue))/2 + 0.5
    HUE_TABLE.set_at( (0,hue) ,( int(r*255) , int(g*255) , int(b*255) ))

SAT_MASK = pg.Surface((256,256),pg.SRCALPHA)
VAL_MASK = pg.Surface((256,256),pg.SRCALPHA)

for x in range(256):
    for y in range(256):
        VAL_MASK.set_at((x,y) , (  255-y,255-y,255-y,y  )  )
        SAT_MASK.set_at((x,y) , (  255-y,255-y,255-y,x  )  )


def pickColor(surf,hsv):
    running = True
    hue = hsv[0]
    sat = hsv[1]
    val = hsv[2]
    outcol = (0,0,0)
    while running:
        wheel = pg.Surface((256,256))
        wheel.fill(HUE_TABLE.get_at((0,hue)))
        wheel.blit(VAL_MASK,(0,0))
        wheel.blit(SAT_MASK,(0,0))
        outcol = wheel.get_at((sat,val))
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.MOUSEBUTTONDOWN:
                mouseX,mouseY = pg.mouse.get_pos()
                if mouseX-10 in range(16) and mouseY-10 in range(360):
                    hue = mouseY - 10
                    wheel = pg.Surface((256,256))
                    wheel.fill(HUE_TABLE.get_at((0,hue)))
                    wheel.blit(VAL_MASK,(0,0))
                    wheel.blit(SAT_MASK,(0,0))
                    outcol = wheel.get_at((sat,val))
                if mouseX-40 in range(256) and mouseY-10 in range(256):
                    sat = mouseX-40
                    val = mouseY-10
                    


        
        
        surf.fill((255,255,255))
        surf.blit( pg.transform.scale(HUE_TABLE,(16,360)) ,(10,10) )
        
        
        surf.blit(wheel,(40,10))

        pg.draw.circle(surf, outcol, (sat+40,val+10) , 16 )

        pg.draw.rect(surf, outcol, (600,10,64,64))

        pg.display.update()
    return [outcol,(hue,sat,val)]