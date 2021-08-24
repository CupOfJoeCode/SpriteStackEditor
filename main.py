import pygame as pg
from colorpick import pickColor
import floodfill
import sys
import spritestack
from random import randint
import easygui as gui
from opensimplex import OpenSimplex
sys.setrecursionlimit(20000)


# C:\Users\joega\AppData\Roaming\Python\Python39\Scripts\pyinstaller main.py -w --onefile

pg.init()

d = pg.display.set_mode((800,600))


tools = [
    {'name':'Pencil','file':'images/pencil.png'},
    {'name':'Eraser','file':'images/eraser.png'},
    {'name':'Eyedropper','file':'images/eyedrop.png'},
    {'name':'Fill Bucket','file':'images/bucket.png'},
]

actions = [
    {'name':'New Layer','file':'images/newlayer.png'},
    {'name':'Duplicate Layer','file':'images/duplicate.png'},
    {'name':'Select Up','file':'images/up.png'},
    {'name':'Select Down','file':'images/down.png'},
    {'name':'Move Up','file':'images/moveup.png'},
    {'name':'Move Down','file':'images/movedown.png'},
    {'name':'Noise','file':'images/noise.png'},
    {'name':'Sphere','file':'images/sphere.png'},
    {'name':'Simplex','file':'images/simplex.png'},

    {'name':'Save','file':'images/save.png'},
    {'name':'Open','file':'images/open.png'},

]

for tool in tools:
    tool['file'] = pg.image.load(tool['file'])

for action in actions:
    action['file'] = pg.image.load(action['file'])


layers = [pg.Surface((16,16),pg.SRCALPHA)]
layers[0].fill((0,0,0,0))

layer = 0

alphaBG = pg.Surface((32,32),pg.SRCALPHA)
for x in range(32):
    for y in range(32):
        clr = (255,255,255,100)
        if (x+y)%2 == 0:
            clr = (200,200,200,100)
        alphaBG.set_at((x,y),clr)
alphaBG = pg.transform.scale(alphaBG,(256,256))

grid = pg.Surface((256,256),pg.SRCALPHA)
grid.fill((0,0,0,0))
for i in range(16):
    pg.draw.rect(grid,(150,150,150),(i*16,0,1,256))
    pg.draw.rect(grid,(150,150,150),(0,i*16,256,1))

color = (0,0,0)
prevhsv = (0,0,0)

toolIndex = 0


angle = 45

mousedown = False

drr = 0


def layerClone(srff):
    tmpOut = pg.Surface((16,16),pg.SRCALPHA)
    tmpOut.fill((0,0,0,0))
    tmpOut.blit(srff,(0,0))
    return tmpOut


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.MOUSEBUTTONDOWN:
            mousedown = True
        if e.type == pg.MOUSEBUTTONUP:
            mousedown = False
        if e.type == pg.KEYUP:
            drr = 0
        if e.type == pg.KEYDOWN:
        
            if e.key == pg.K_LEFT:
                drr = -1
            if e.key == pg.K_RIGHT:
                drr = 1
           
                

            
            
                
                
           

    angle -= drr*1
    mouseX , mouseY = pg.mouse.get_pos()

    d.fill((255,255,255))
    
    scaledLayer = pg.transform.scale(layers[layer],(256,256))
    if layer > 0:
        scaledPrevLayer = pg.transform.scale(layers[layer-1],(256,256))
        d.blit(scaledPrevLayer,(0,0))
        maskSurface = pg.Surface((256,256),pg.SRCALPHA)
        maskSurface.fill((255,255,255,100))
        d.blit(maskSurface,(0,0))

    d.blit(alphaBG,(0,0))
    d.blit(scaledLayer,(0,0))

    d.blit(grid,(0,0))

    
    pg.draw.rect(  d, color,   (0,260,16,32)  )
    if mouseX in range(14) and mouseY-260 in range(32) and mousedown:
        color,prevhsv = pickColor(d,prevhsv)
        
        mousedown = False

    for i in range(len(tools)):
        pg.draw.rect(d, (0,0,0) , (i*32,340,31,31) )
        if toolIndex == i:
            pg.draw.rect(d, (200,200,200) , (i*32+1,341,29,29) )
        else:
            pg.draw.rect(d, (255,255,255) , (i*32+1,341,29,29) )
        d.blit(tools[i]['file'],(i*32,340))


    if int(mouseX/32) in range(len(actions)) and mouseY - 440 in range(32) and mousedown:
            indX = int(mouseX/32)

            
            if indX == 0:
                layers.append(pg.Surface((16,16),pg.SRCALPHA))
                layer= len(layers)-1
                layers[layer].fill((0,0,0,0))
            if indX == 1:
                tempSurf = pg.Surface((16,16),pg.SRCALPHA)
                tempSurf.fill((0,0,0,0))
                tempSurf.blit(layers[layer],(0,0))
                layers.append(tempSurf)
                layer = len(layers)-1
            if indX == 2:
                layer = min(layer+1,len(layers)-1)
            if indX == 3:
                layer = max(layer-1,0)
            if indX == 4:
                if layer < len(layers) - 1:
                    tmplayer = layerClone(layers[layer+1])
                    layers[layer+1] =  layerClone(layers[layer])
                    layers[layer] = layerClone(tmplayer)
                    layer+=1

            if indX == 5:
                if layer > 0:
                    tmplayer = layerClone(layers[layer-1])
                    layers[layer-1] =  layerClone(layers[layer])
                    layers[layer] = layerClone(tmplayer)
                    layer-=1
            
            if indX == 6:
                for l in layers:
                    for x in range(16):
                        for y in range(16):
                            ccolor = l.get_at((x,y))
                            r = ccolor[0]
                            g = ccolor[1]
                            b = ccolor[2]
                            a = ccolor[3]
                            r = max(min(r+randint(0,32)-16,255),0)
                            g = max(min(g+randint(0,32)-16,255),0)
                            b = max(min(b+randint(0,32)-16,255),0)
                            if a == 0:
                                r,g,b = (0,0,0)
                            l.set_at((x,y),(r,g,b,a))
            if indX == 7:
                layers = []
                layer = 0
                for z in range(16):
                    tempSurf = pg.Surface((16,16),pg.SRCALPHA)
                    tempSurf.fill((0,0,0,0))
                    for x in range(16):
                        for y in range(16):
                            if (x-8)**2 + (y-8)**2 + (z-8)**2 <= 8*8:
                                tempSurf.set_at((x,y),(255,0,0))
                    layers.append(tempSurf)

            if indX == 8:
                layers = []
                layer = 0
                noise = OpenSimplex(randint(-1024,1024))
                for z in range(16):
                    tempSurf = pg.Surface((16,16),pg.SRCALPHA)
                    tempSurf.fill((0,0,0,0))
                    for x in range(16):
                        for y in range(16):
                            if noise.noise3d( x/8.,y/8.,z/8.  ) < 0.1:
                                tempSurf.set_at((x,y),(255,0,0))
                    layers.append(tempSurf)
            if indX == 9:
                fname = gui.filesavebox(default='sprites/*.png',filetypes=['png','*'])
                if fname != None:
                    outsprite = pg.Surface(( len(layers)*16 ,16),pg.SRCALPHA)
                    for i in range(len(layers)):
                        outsprite.blit(layers[i],(i*16,0))
                    pg.image.save(outsprite,fname)

            if indX == 10:
                fname = gui.fileopenbox(default='sprites/*.png',filetypes=['png','*'])
                layer = 0
                if fname != None:
                    imprt = pg.image.load(fname)
                    tmpw = imprt.get_size()[0]
                    layers = []
                    for i in range(int(tmpw/16)):
                        layers.append(pg.Surface((16,16),pg.SRCALPHA))
                        tmps = pg.Surface((16,16),pg.SRCALPHA)
                        tmps.fill((0,0,0,0))
                        tmps.blit(imprt,(-i*16,0))
                        layers[i].fill((0,0,0,0))
                        layers[i].blit(tmps,(0,0))
            
            mousedown = False

    for i in range(len(actions)):


        pg.draw.rect(d, (0,0,0) , (i*32,440,31,31) )
        
        pg.draw.rect(d, (255,255,255) , (i*32+1,441,29,29) )
        d.blit(actions[i]['file'],(i*32,440))
    

    if int(mouseX/32) in range(len(tools)) and mouseY - 340 in range(32) and mousedown:
        toolIndex = int(mouseX/32)
        mousedown = False

    mx = int(mouseX/16)
    my = int(mouseY/16)
    if mx in range(16) and my in range(16):
        if mousedown:
            if toolIndex == 0:
                layers[layer].set_at((mx,my),color)
            if toolIndex == 1:
                layers[layer].set_at((mx,my),(0,0,0,0))
            if toolIndex == 2:
                color = layers[layer].get_at((mx,my))
            if toolIndex == 3:
                floodfill.fill(layers[layer],mx,my,color,d)
            
         
    for i in range(len(layers)):
        tmpsrr = spritestack.isometrize(layers[i],angle)
        for j in range(4):
            d.blit( tmpsrr , (360 , 256 - i*4 - j) )
    tmpsrr = spritestack.isometrize(layers[layer],angle)
    for j in range(4):
        
        d.blit(tmpsrr , (580 , 256 - layer*4 - j) )
    # angle += 1
    pg.display.update()