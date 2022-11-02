# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:31:56 2022

@author: cleme
"""

import math
from PIL import Image, ImageDraw  # Module de gestion des images

ratio = 0.8 #angle initiale
length = 200
alpha = 2*math.pi/11
WIDTH,HEIGHT = 1000,1000

#crée la fractal, l'affiche et l'enregistre
im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

def drawTree(a, b, angle, length):
    if length > 15:
        c = a + math.cos(angle)*length*ratio
        d = b + math.sin(angle)*length*ratio
        draw.line([(a,b), (c,d)], fill = (255,215,0) , width = 2)
        drawTree(c, d, angle - alpha, length*ratio)
        drawTree(c, d, angle + alpha, length*ratio)

drawTree(WIDTH/2, HEIGHT, -math.pi/2, length)
im.show()
