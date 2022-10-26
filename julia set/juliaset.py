import numpy as np
import matplotlib.pyplot as plt
import imageio as iio

from colour import Color

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\julia set\\"

gridRes = 5e-3
iterMax = 100

xMin = -2
xMax = 2

yMin = -2
yMax = 2

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )

col = ["black","white"]
colours = []

for i in range(len(col)-1):
    colours += list(Color(col[i]).range_to(Color(col[i+1]),iterMax//(len(col)-1) ))
    
colours = [c.rgb for c in colours]


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

def julia( output , c , escapeRadius):
    
    #==# f(z) = z*z + c #==#
    f = lambda z : z**2 + c
    

    for i in range( yWidth ):
        print("i = " + str(i) )
        for j in range( xWidth ):
            
            iter = 0
            z = coord_1(i,j)
            
            while ( iter<iterMax and np.abs(z) < escapeRadius ):
                z = f(z)
                
                iter += 1
            
            #==# Adding colors #==#
            if( iter == iterMax ):
                output[i,j] = [0,0,0]
            else:
                output[i,j] = colours[iter]
    
    
    #==# Display #==#
    plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
    
    plt.title('c = ' + str(c) + ' R = ' + str(escapeRadius) )
    
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    
    plt.savefig( path + "c=" + str(c) + ' R=' + str(escapeRadius) + ".png" , dpi=600 )
    
    plt.show()
    
    
    
output = 1-np.zeros((yWidth,xWidth,3),dtype = 'float')

julia( output , -0.835 - 0.2321j, 10)
    
    
    
    
    
    