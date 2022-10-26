import numpy as np
import matplotlib.pyplot as plt
import imageio as iio

from colour import Color

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\mandelbox\\"


gridRes = 1e-2

xMin = -5
xMax = 5

yMin = -5
yMax = 5

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )


def coord( x , y ):
    '''
    Converts complex coordinates x+iy to pixel coordinates (i,j) on the grid of size xWidth * yWidth
    '''
    
    i = (yWidth-1) * (y-yMax)/(yMin-yMax)
    j = (xWidth-1) * ( 1 - (x-xMax)/(xMin-xMax) )
    
    return (int(i),int(j))
    
    
def transfo( s , r , f , z ):
    '''
    Applies the Mandelbox transformation to the complex z, defined as below :
    
    z = s . ballFold( r , f . boxFold(z) ) + c
    
    '''

    # BoxFold
    if( np.real(z) > 1 ):
        z = (2-np.real(z)) + np.imag(z)
    elif(np.real(z) < -1 ):
        z = (-2-np.real(z)) + np.imag(z)
    
    z = f * z

    # BallFold
    if( np.abs(z) < r ):
        z = z * r**2
    elif( np.abs(z) < 1 ):
        z = z / (np.abs(z)**2)
        
    return( s * z )
    

def mandelbox( output , s,r,f ):
    
    # For the convergence
    epsilon = 1e-1
    maxAbs = 100
    iterMax = 10

    for i in range( yWidth ):
        print("i = " +str(i))
        for j in range( xWidth ):
            
            iter = 0
            
            re = xMax + (xMin-xMax)*(1-j/(xWidth-1))
            im = yMax + i * (yMin-yMax)/(yWidth-1)
            
            z = re + im*1j 
            newZ = transfo( s,r,f , z )
            
            while ( np.abs(newZ) < maxAbs and iter<iterMax and np.abs(newZ-z)>epsilon ):
                z = newZ
                newZ = transfo( s,r,f , z )
                
                iter += 1
            
            if(np.abs(z) >= maxAbs):
                output[i,j] = [0,0,0]
    
    plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
    
    plt.title('s = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f) )
    
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    
    plt.savefig( path + str(s) + ' ' + str(r) + ' ' + str(f) + ".png" , dpi=600 )
    
    plt.show()
    
    
    
output = 1-np.zeros((yWidth,xWidth,3),dtype = 'float')

mandelbox( output , 2 , 1/2 , 1)
    
    
    
    
    
    