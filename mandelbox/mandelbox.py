import numpy as np
import matplotlib.pyplot as plt
import imageio as iio

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

def transfo( s , r , f , z ):
    '''
    Applies the Mandelbox transformation to the complex z, defined as below :
    
    z = s . ballFold( r , f . boxFold(z) )
    
    '''

    #= BoxFold =#
    if( np.imag(z) > 1 ):
        z = np.real(z) + (2-np.imag(z))*1j
    elif(np.imag(z) < -1 ):
        z = np.real(z) + (-2-np.imag(z))*1j
    
    if( np.real(z) > 1 ):
        z = (2-np.real(z)) + np.imag(z)*1j
    elif(np.real(z) < -1 ):
        z = (-2-np.real(z)) + np.imag(z)*1j
    
    
    #==#
    
    z = f * z

    #= BallFold =#
    if( np.abs(z) < r ):
        z = z / (r**2)
    elif( np.abs(z) < 1 ):
        z = z / (np.abs(z)**2)
    #==#
    
    return( s * z )
    
def mandelbox( output , s,r,f , maxRadius , show , verbose ):
       
    for i in range( yWidth ):
        
        if(verbose):
            if( not (i % 100 )):
                print("i = " + str(i) + " / " + str(yWidth) )
            
        for j in range( xWidth ):
            
            iter = 0
            z = coord_1(i,j)
            z0 = z
            
            while ( iter<iterMax and np.abs(z) < maxRadius):
                z = z0 + transfo(s,r,f,z)
                
                iter += 1
            
            #==# Adding colors #==#
            if( iter == iterMax ):
                output[i,j] = Color("blue").rgb
            else:
                output[i,j] = [1,1,1]
    
    
    if( show ):
        #==# Display #==#
        plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        plt.title('s = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f) )
        
        plt.xlabel("Real part")
        plt.ylabel("Imaginary part")
        
        plt.savefig( path + 's = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f) + ".png" , dpi=400 )
        
        plt.show()


#===# PARAMETERS #===#

#==# GRID #==#
path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\mandelbox\\"

gridRes = 2e-2
iterMax = 20

xMin = -7
xMax = 7

yMin = -7
yMax = 7

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("= = = = = = = = = = = = ")
print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )
print("= = = = = = = = = = = = ")

output = np.zeros((yWidth,xWidth,3),dtype = 'float')
#====#

#==# MANDELBOX #==#
s = 2
r = .5
f = 1

maxRadius = 20
#====#

    
output = np.zeros((yWidth,xWidth,3),dtype = 'float')
mandelbox( output , s,r,f , maxRadius , show = True , verbose = True)


