import pygame as pg

def isometrize(image,a):
    rotated = pg.transform.rotate(pg.transform.scale(image,(256,256)),a)
    scaled = pg.transform.scale(rotated,(128,64))
    return scaled