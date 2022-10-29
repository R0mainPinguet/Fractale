# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:32:19 2022

@author: cleme
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:46:24 2022

@author: cleme
"""

import numpy as np
import math
import plotly.express as px #bibliotheque (plotly) utilise pour afficher en html et mieux gerer la rotation 3d

path = "/Users/cleme/Desktop/mandelbulb/"

##--## Paramètrage du problème ##--##
n = 8 #puissance du mandelbulb
N = 64 #nbr de point (pas) sur chaque axes
itermax = 20;
##--## fonctions ##--##

def spherical_coord(x,y,z): #attention version wiki (la def est différente)
    r = math.sqrt(x**2 + y**2 + z**2)
    
    if (x==0):
        theta = np.sign(y)*np.pi/2
    else:
        theta = math.atan(y/x)
    
    if (r==0):
        phi = np.sign(z)*np.pi/2
    else:
        phi = math.asin(z/r)
    
    return [r,theta,phi]


X = np.linspace(-1,1, N)
Y = np.linspace(-1,1, N)
Z = np.linspace(-1,1, N)
data = [[],[],[]]

def mandibulb():
    for x in X: #ici c est un point de notre maillage 
        for y in Y:
            edge = False 
            for z in Z:
                n=8
                iteration = 0
                zeta = [0,0,0] #z0
                r = 0
                while(iteration <= itermax and r < 2):
                    
                    sphericalz = spherical_coord(zeta[0], zeta[1], zeta[2]) #pour mettre z à la puissance n
                    r = sphericalz[0]
                    theta = sphericalz[1]
                    phi = sphericalz[2]
                    
                    nx = pow(r, n) * math.cos(theta*n) * math.cos(phi*n);
                    ny = pow(r, n) * math.sin(theta*n) * math.cos(phi*n);
                    nz = pow(r, n) * math.sin(phi*n);
                    
                    zeta[0] = nx + x
                    zeta[1] = ny + y 
                    zeta[2] = nz + z
                    
                    iteration = iteration + 1 
                    
                if(r > 2):
                    if (edge is True):
                        edge = False
                    
                if(iteration > itermax):
                    if (edge is False):
                        edge = True
                        data[0].append(x)
                        data[1].append(y)
                        data[2].append(z)
                    
    fig = px.scatter_3d(data, x=data[0], y=data[1], z=data[2])
    fig.update_traces(marker=dict(size=1.3,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),selector=dict(mode='markers'))

    fig.write_html('tmp.html', auto_open=True)              

mandibulb()

