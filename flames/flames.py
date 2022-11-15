import numpy as np
import random as rd

import matplotlib.pyplot as plt
import imageio as iio
from PIL import Image, ImageDraw
from colour import Color

rd.seed(256)
np.random.seed(256)

#== Gamma correction ==#
gamma = 2.2
#====#

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
    


def flames( output , samples , iterMax , show , verbose ):
    
    n = len(F_index)
    
    for i in range(samples):
        
        if( verbose and not (i % 5000)):
            print("Samples = " + str(i) + " / " + str(samples) )
            
        arr = np.array([rd.random()*2-1 , rd.random()*2-1])

        iter = 0
        
        while( iter < iterMax ):
    
            j = rd.randint(0,n-1)
            
            arr = V[F_index[j]]( basis[j] @ np.array([arr[0],arr[1],1]).T )
            (k,l) = coord(arr[0],arr[1])
        
            #==# Adding colors #==#
            if( iter > 20 ):
                if( arr[0] < xMax and arr[0] > xMin and arr[1] < yMax and arr[1] > yMin ):
                    output[k,l,0:3] = (colours[j] + output[k,l,0:3])/2
                    output[k,l,3] +=1
                    
            iter+=1
        
    # #==# Processing data #==#
    print("Processing data ...")
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = output[i,j,3]
            
            #= Log scale =#
            if(alpha>0):
                output[i,j] *= np.log(alpha)/alpha
    
    #= Output value : floating number from 0 to 1 =#
    output = output / np.max(output[:,:,0:3])

    
    if( show ):
        
        name = ""
        for index in F_index:
            name += str(index) + " " 
        
        #==# Display #==#
        print("Displaying image ...")
        
        plt.imshow( output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    
        plt.savefig( path + name + ".png" , dpi = 300 )
        
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
S0 = lambda x,y : (   x/2   ,   y/2   )
S1 = lambda x,y : ( (x+1)/2 ,   y/2   )
S2 = lambda x,y : (   x/2   , (y+1)/2 )
#==#

#= LINEAR =#
def V0(arr):
    return(arr)

#= SINUS =#
def V1(arr):
    return(np.sin(arr))

#= SPHERICAL =#
def V2 (arr):
    x , y = arr[0] , arr[1]
    r2 = x**2 + y**2
    return(arr/r2)

#= SWIRL =#
def V3(arr):
    x , y = arr[0] , arr[1]
    r2 = x**2 + y**2
    return( np.array([ x * np.sin(r2) - y * np.cos(r2) , x * np.cos(r2) + y * np.sin(r2) ] ) )

#= HORSESHOE=#
def V4(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    return( np.array([(x-y)*(x+y) , 2*x*y ]) / r )

#= POLAR =#
def V5(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([theta/np.pi , r - 1 ]))

#= HANDERKCHIEF =#
def V6(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([ np.sin(theta + r) , np.cos(theta - r) ] ) * r )

#= HEART =#
def V7(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([r * np.sin(theta*r) , - r * np.cos(theta*r) ] ))

#= DISC =#
def V8(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([theta/np.pi * np.sin(np.pi * r) , theta/np.pi * np.cos(np.pi * r)] ))

#= SPIRAL =#
def V9(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([np.cos(theta) + np.sin(r) , np.sin(theta) - np.cos(r) ]) / r )

#= HYPERBOLIC =#
def V10(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([ np.sin(theta)/r , r * np.cos(theta) ]) )

#= DIAMOND =#
def V11(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    return( np.array([np.sin(theta)*np.cos(r) , np.cos(theta)*np.sin(r) ]) )

#= EX =#
def V12(arr):
    x , y = arr[0] , arr[1]
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(x/y)
    p0 , p1 = np.sin(theta+r) , np.cos(theta-r)
    return( np.array([ p0**3 + p1**3 , p0**3 - p1**3 ]) * r )
    
#=====#

V = [V0,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12]
F_index = [ 0 , 1 , 2 ]

possibleColours = ["red" , "orange" , "yellow" , "lightgreen" , "green" , "blue" , "cyan" , "purple" , "violet" ]
# rd.shuffle(possibleColours)

F = []
basis = []
colours = []


print("Index des fonctions : ")
print(F_index)

print("\n")

for i in range(len(F_index)):

    A = 2*np.random.random((2,3))-1
    basis.append( A )

    #== Associating a colour to each transformation ==#
    col = possibleColours.pop(0)
    colours.append( Color(col).rgb )
    possibleColours.append(col)
    
    #== Debug ==#
    print("Changement de repère de la fonction " + str(i) + " : ") 
    print(A)
    print("Couleur associée ( RGB ) : ")
    print(Color(col).rgb)
    
    print("")

#===#


flames( output , samples = 500000 , iterMax = 300 , show = True, verbose = True)









