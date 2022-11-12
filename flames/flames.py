import numpy as np
import random as rd

import matplotlib.pyplot as plt
import imageio as iio
from PIL import Image, ImageDraw
from colour import Color

def coord( x , y ):
    '''
    Converts complex coordinates x+iy to pixel coordinates (i,j) on the grid of size xWidth * yWidth
    '''
    
    i = (yWidth-1) * (y-yMax)/(yMin-yMax)
    j = (xWidth-1) * ( 1 - (x-xMax)/(xMin-xMax) )
    
    return (int(i),int(j))
    
def coord_1( i , j ):
    '''
    Converts pixel coordinates (i,j) on the grid of size xWidth * yWidth to complex coordinates x+iy
    '''         
       
    re = xMax + (xMin-xMax)*(1-j/(xWidth-1))
    im = yMax + i * (yMin-yMax)/(yWidth-1)
    
    return( re + im*1j )

def norm(x,y):
    return( np.sqrt( x**2 + y**2 ) )
    
    
def flames( output , functions , samples , iterMax , show , verbose ):
    
    n = len(functions)
    
    for i in range(samples):
        
        if( verbose and not (i % 10)):
            print("Samples = " + str(i) + " / " + str(samples) )
            
        x,y = rd.random()*2-1 , rd.random()*2-1
        x0,y0 = x+1,y+1
        
        iter = 0
        
        while( norm( x-x0,y-y0 ) > gridRes and iter < iterMax ):
            (x0,y0) = (x,y)
            
            j = rd.randint(0,n-1)
            
            (x,y) = functions[j](x,y)
            (k,l) = coord(x,y)
        
            #==# Adding colors #==#
            if( iter > 20 ):
                if( x < xMax and x > xMin and y < yMax and y > yMin ):
                    output[k,l,0:3] += colours[j]
                    output[k,l,3] +=1
            
            iter+=1
        
    #==# Processing data #==#
    print("Processing data ...")
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = output[i,j,3]
            
            #= Log scale =#
            if(alpha!=0):
                output[i,j] *= np.log(alpha)/alpha
    
    #= Output value : floating number from 0 to 1 =#
    output /= np.max(output)

    
    if( show ):
        
        #==# Display #==#
        print("Displaying image ...")
        
        plt.imshow( output , extent=[xMin,xMax,yMin,yMax] )
    
        plt.savefig( path + "flames.png" , dpi=500 )
        
        plt.show()



#===# PARAMETERS #===#

#==# GRID #==#
path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\flames\\"

gridRes = 2e-3
iterMax = 100

xMin = -1
xMax = 1

yMin = -1
yMax = 1

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("= = = = = = = = = = = = ")
print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )
print("= = = = = = = = = = = = ")

output = np.zeros((yWidth,xWidth,4),dtype = 'float')
#====#

#=== PRESETS ===#

#= Sierspinski triangle =#
V0 = lambda x,y : (   x/2   ,   y/2   )
V1 = lambda x,y : ( (x+1)/2 ,   y/2   )
V2 = lambda x,y : (   x/2   , (y+1)/2 )
#==#

#= SINUS =#
V3 = lambda x,y : (np.sin(x),np.sin(y))
#==#

F = [V0,V1,V2,V3]
col = ["red","yellow","green","blue"]

#==# COLOURS OF EACH TRANSFORMATION #==#
colours = []

for c in col:
    colours.append( Color(c).rgb )
#====#

flames( output , functions = F , samples = 50000 , iterMax = 10000 , show = True, verbose = True)









