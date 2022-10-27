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

def julia( output , c , escapeRadius , show , verbose):
       
    #==# f(z) = z*z + c #==#
    f = lambda z : z**2 + c
    

    for i in range( yWidth ):
        if(verbose):
            if( not (i % 100 )):
                print("i = " + str(i) + " / " + str(yWidth) )
            
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
    
    
    if( show ):
        #==# Display #==#
        plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        plt.title('c = ' + str(c) + ' R = ' + str(escapeRadius) )
        
        plt.xlabel("Real part")
        plt.ylabel("Imaginary part")
        
        plt.savefig( path + "c=" + str(c) + ' R=' + str(escapeRadius) + ".png" , dpi=500 )
        
        plt.show()


#===# MAIN #===#
    
path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\julia set\\"

gridRes = 3e-3
iterMax = 100

xMin = -1.5
xMax = 1.5

yMin = -1.5
yMax = 1.5

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("= = = = = = = = = = = = ")
print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )
print("= = = = = = = = = = = = ")

col = ["blue","red","yellow"]
colours = []

for i in range(len(col)-1):
    colours += list(Color(col[i]).range_to(Color(col[i+1]),iterMax//(len(col)-1) ))
    
colours = [c.rgb for c in colours]

gif = True

c = -.4 + .6j
R = 2

if(gif):
    
    images = []
    
    imageCount = 10

    for i in range(imageCount):
        
        print("image = " + str(i) + " / " + str(imageCount) )
        
        output = np.zeros((yWidth,xWidth,3),dtype = 'float')
        
        julia( output , c , R , show = False , verbose = True)
        
        fig,axs=plt.subplots(1,1)
        
        axs.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        axs.set_title('c = ' + str(c) + ' R = ' + str(R) )
        
        axs.set_xlabel("Real part")
        axs.set_ylabel("Imaginary part")
        
        fig.canvas.draw()
        image_from_plot=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot=image_from_plot.reshape(fig.canvas.get_width_height()[::-1]+(3,))
        
        images.append(image_from_plot)
        
        plt.close()
        
        c = c * np.exp(1j * 2*np.pi / imageCount)
    
    iio.mimsave(path + 'c = ' + str(c) + ' R = ' + str(R) + '.gif', images)
    
else:
    
    output = np.zeros((yWidth,xWidth,3),dtype = 'float')
    julia( output , c , R , show = True , verbose = True)
    
    
    
