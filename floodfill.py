import pygame as pg
import time




    

def fill(image,startx,starty,color,srf):
    followX = 0
    followY = 0
    positionStack = []
    startColor = image.get_at((startx,starty))
    followX = startx
    followY = starty
    for i in range(1024):
        scan = True
        image.set_at((followX,followY),color)
        if followY != 0:
            if image.get_at((followX,followY-1)) == startColor and scan:
                positionStack.append((followX,followY))
                
                followY -= 1
                scan = False
        if followY != 15:
            if image.get_at((followX,followY+1)) == startColor and scan:
                positionStack.append((followX,followY))
                
                followY += 1
                scan = False
        if followX != 0:
            if image.get_at((followX-1,followY)) == startColor and scan:
                positionStack.append((followX,followY))
                
                followX -= 1
                scan = False

        if followX != 15:
            if image.get_at((followX+1,followY)) == startColor and scan:
                positionStack.append((followX,followY))
                
                followX += 1
                scan = False
        if len(positionStack) < 1:
            return
        if scan:

            followX, followY = positionStack.pop(len(positionStack)-1)
        # Debugging:

        # srf.fill((255,255,255))
        # srf.blit( pg.transform.scale(image,(256,256)),(0,0) )
        # pg.draw.rect(srf,(255,0,0),(followX*16,followY*16,16,16))
        # pg.display.update()
        # time.sleep(0.1)
        
