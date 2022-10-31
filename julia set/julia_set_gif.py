# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:08:40 2022

@author: clement

"""

import numpy as np
import matplotlib.pyplot as plt
import cmath
from PIL import Image, ImageDraw  # Module de gestion des images

path = "/Users/cleme/Desktop/fractal/"

def u(c,n,u0):
    u = []
    u.append(u0)
    for i in range(1,n+1):
        u.append(u[i-1]*u[i-1]+c) 
    return u

def Julia(c, u0):
    R = 2
    l = []
    n = 100
    count = 0
    z = u0
    for i in l: 
        if(abs(i)>R):
            return count
        else: 
            count = count + 1
        z = z*z + c
    return 200;


x_min, x_max = -1.5, 1.5
y_min, y_max = -1, 1

WIDTH,HEIGHT = 1920,1080 #mettre la meilleure résolution puis resize l'image

#crée la fractal, l'affiche et l'enregistre
def fractale(c,i):
    im = Image.new('HSV', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    X = np.linspace(x_max, x_min, WIDTH)
    Y = np.linspace(y_min, y_max, HEIGHT)
    for x in range(WIDTH):
        print(x)
        for y in range(HEIGHT):
            u0 = complex(X[x],Y[y])
            n = Julia(c, u0)
            if(n < 200):
                draw.point((x,y), (n%255, 255, 255))
            else:
                draw.point((x,y), (0,0,0))
    im.convert('RGB').save(path+'/fractal_{}.png'.format(i), 'PNG')
    return im


def GIF():
    #Calcule chaque fractale
    # N = 300
    # A = np.linspace(0, 2*np.pi, N)
    # i = 0
    # for a in A:
    #     print(i)
    #     c = 0.7885*cmath.exp(complex(0,a))
    #     fractale(c, i) 
    #     i = i + 1
    
    #Creation du gif
    frames = [] 
    imgs =[]
    for i in range(300):
        imgs.append(path + "fractal_"+str(i)+".png")
    print(imgs)
    
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
        
    # Save into a GIF file that loops forever
    frames[0].save(path + 'anim.gif', format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    quality=95,
                    duration=60, loop=0)
    frames[0].resize(900,600)
    
GIF()
