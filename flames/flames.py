import numpy as np
import random as rd

import matplotlib.pyplot as plt
import imageio as iio
from PIL import Image, ImageDraw
from colour import Color

rd.seed(16)
np.random.seed(16)

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

def process_binary(out):
    #=# a - Binary values #=#
    
    new_output = out.copy()
    
    #==# Processing data #==#
    print("Processing data : binary ...")
    
    max = np.max(new_output[:,:,0:3])
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = new_output[i,j,3]
            
            if(alpha > 0):
                new_output[i,j] = np.array([1,1,1,1])
            else:
                new_output[i,j] = np.array([0,0,0,0])
    
    #==# Display #==#
    print("Displaying image ...")
    name = "a - binary.png"
    
    plt.imshow( new_output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    plt.savefig( path + name , dpi = 300 )
    plt.show()
    #====#
    
def process_linear(out):
    #=# b - Linear scale #=#
    
    new_output = out.copy()
    
    #==# Processing data #==#
    print("Processing data : linear ...")
    
    max = np.max(new_output[:,:,0:3])
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = new_output[i,j,3]
            
            new_output[i,j] = alpha/max * np.array([1,1,1,1])
    
    #==# Display #==#
    print("Displaying image ...")
    name = "b - linear.png"
    
    plt.imshow( new_output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    plt.savefig( path + name , dpi = 300 )
    plt.show()
    #====#
    
def process_log(out):
    #=# c - Logarithmic scale #=#
    
    new_output = out.copy()
    
    #==# Processing data #==#
    print("Processing data : logarithmic ...")
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = new_output[i,j,3]
            
            #= Log scale =#
            if(alpha>0):
                new_output[i,j] = np.log(alpha) * np.array([1,1,1,1])
    
    #= Output value : floating number from 0 to 1 =#
    new_output[:,:,0:3] = new_output[:,:,0:3] / np.max(new_output[:,:,0:3])
    
    #==# Display #==#
    print("Displaying image ...")
    name = "c - logarithmic.png"
    
    plt.imshow( new_output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    plt.savefig( path + name , dpi = 300 )
    plt.show()
    #====#

def process_colors(out):
    #=# d - Logarithmic scale and colors #=#
    
    new_output = out.copy()
    
    #==# Processing data #==#
    print("Processing data : colors ...")
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = new_output[i,j,3]
            
            #= Log scale =#
            if(alpha>0):
                new_output[i,j] *= np.log(alpha)/alpha
    
    #= Output value : floating number from 0 to 1 =#
    new_output[:,:,0:3] = new_output[:,:,0:3] / np.max(new_output[:,:,0:3])
    
    #==# Display #==#
    print("Displaying image ...")
    name = "d - colors.png"
    
    plt.imshow( new_output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    plt.savefig( path + name , dpi = 300 )
    plt.show()
    #====#
    
def process_gamma(out , gamma):
    #=# e - Logarithmic scale, colors and gamma correction #=#
    
    new_output = out.copy()
    
    #==# Processing data #==#
    print("Processing data : gamma correction ...")
    
    for i in range(xWidth):
        for j in range(yWidth):
            alpha = new_output[i,j,3]
            
            #= Log scale =#
            if(alpha>0):
                new_output[i,j] *= np.log(alpha)/alpha
    
    #= Output value : floating number from 0 to 1 =#
    new_output[:,:,0:3] = new_output[:,:,0:3] / np.max(new_output[:,:,0:3])
    
    #= Gamma factor =#
    new_output[:,:,0:3] = np.power(new_output[:,:,0:3] , 1/gamma )
    
    #==# Display #==#
    print("Displaying image ...")
    name = "e - gamma " +  str(gamma) + ".png"
    
    plt.imshow( new_output[:,:,0:3] , extent=[xMin,xMax,yMin,yMax] )
    plt.savefig( path + name , dpi = 300 )
    plt.show()
    #====#
    
def flames( output , samples , iterMax , verbose ):
    
    n = len(F_index)
    
    for i in range(samples):
        
        if( verbose and not (i % 10000)):
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
                    output[k,l,0:3] += colours[j]
                    output[k,l,3] +=1
            
            iter+=1
    
    #=# Binary #=#
    process_binary(output)
    
    #=# Linear scale #=#
    process_linear(output)
    
    #=# Logarithmic scale #=#
    process_log(output)
    
    #=# Colors #=#
    process_colors(output)
    
    #=# Gamma factors #=#
    process_gamma(output,2.2)
    process_gamma(output,4.0)

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
F_index = [ 1,3,8 ]

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
    print("Changement de repère de la fonction " + str(F_index[i]) + " : ") 
    print(A)
    print("Couleur associée ( RGB ) : ")
    print(Color(col).rgb)
    
    print("")

#===#


flames( output , samples = 500000 , iterMax = 50 , verbose = True)









