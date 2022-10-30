import numpy as np
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

def mandelbrot( output , power , R , show , verbose ):
    
    for i in range( yWidth ):
        if(verbose):
            if( not (i % 100 )):
                print("i = " + str(i) + " / " + str(yWidth) )
            
        for j in range( xWidth ):
            
            iter = 0
            z = 0+0j
            
            c = coord_1(i,j)
            
            f = lambda x : x**power + c
            
            while ( iter<iterMax and np.abs(z) < R ):
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
        
        plt.title("z**"+str(power)+"+c" )
        
        plt.xlabel("Real part")
        plt.ylabel("Imaginary part")
        
        plt.savefig( path + "z^" + str(power) + " + c .png" , dpi=600 )
        
        plt.show()



def generateGif():
    
    images = []
    
    for i in range(imageCount):
        images.append( iio.imread( path + "..\\temp\\fractale_" + str(i) + ".png"  ))
    
    if(gif=="Power"):
        iio.mimsave(path + "power = " + str(pMin) + "-" + str(pMax) + ".gif", images)
    elif(gif=="Zoom"):
        iio.mimsave(path + "power = " + str(power) + ".gif", images)
        

#===# PARAMETERS #===#

#==# GRID #==#
path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\mandelbrot\\"

gridRes = 5e-3
iterMax = 100

xMin = -2
xMax = 2

yMin = -2
yMax = 2

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("= = = = = = = = = = = = ")
print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )
print("= = = = = = = = = = = = ")

output = np.zeros((yWidth,xWidth,3),dtype = 'float')
#====#

#==# COLOURS #==#
col = ["red","blue","purple"]
colours = []

for i in range(len(col)-1):
    colours += list(Color(col[i]).range_to(Color(col[i+1]),iterMax//(len(col)-1) ))
    
colours = [c.rgb for c in colours]
#====#

#==# Mandelbrot and gif type #==#

# The gif can be : "Zoom" : a zoom on a particular point z0
#                  "Power" : changes the power p in the function f(z) = z**p + c , with p between pMin to pMax
#                  "None" : no gif : only a picture with f(z) = z**power + c

gif = "Power"
imageCount = 60
R = 2

#= Zoom parameters =#
zoom = 50
z0 = 0

#= Power parameters =#
pMin = 1
pMax = 3

#= None parameters =#
power = 2

#====#

if(gif == "Zoom"):

    #== Saving the inital window size ==#
    xSize0 = xMax - xMin
    ySize0 = yMax - yMin
    center0 = ((xMin+xMax)/2 + 1j*(yMin+yMax)/2)
    #====#
    
    for i in range(imageCount):
        
        #==# Interpolates the window size ==#
        center = z0 * i/(imageCount-1) + center0 * (imageCount-1-i)/(imageCount-1)
        
        xSize = xSize0/zoom * i/(imageCount-1) + (imageCount-1 - i)/(imageCount-1) * xSize0
        ySize = ySize0/zoom * i/(imageCount-1) + (imageCount-1 - i)/(imageCount-1) * ySize0
        
        xMin = np.real(center) - xSize/2
        xMax = np.real(center) + xSize/2
        
        yMin = np.imag(center) - ySize/2
        yMax = np.imag(center) + ySize/2
        #====#
        
        print("image = " + str(i+1) + " / " + str(imageCount) )
        
        mandelbrot( output , power , R , show = False , verbose = True )
        
        fig,axs=plt.subplots(1,1)
        
        axs.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        axs.set_title('c = ' + str(c0) + ' R = ' + str(R) )
        
        axs.set_xlabel("Real part")
        axs.set_ylabel("Imaginary part")
        
        fig.canvas.draw()
        image_from_plot=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot=image_from_plot.reshape(fig.canvas.get_width_height()[::-1]+(3,))
        
        plt.savefig( path + "..\\temp\\fractale_" + str(i) + ".png"  , dpi=200 )
        
        plt.close()
            
        print("= = = = = = = = = = = = ")

    generateGif()

elif(gif == "Power"):

    for i in range(imageCount):
        
        #==# Interpolates the window size ==#
        power = pMax * i/(imageCount-1) + pMin * (imageCount-1-i)/(imageCount-1)
        #====#
        
        print("image = " + str(i+1) + " / " + str(imageCount) )
        
        mandelbrot( output , power , R , show = False , verbose = True )
        
        fig,axs=plt.subplots(1,1)
        
        axs.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        axs.set_title('f(z) = z**'+str(power) + '+c')
        
        axs.set_xlabel("Real part")
        axs.set_ylabel("Imaginary part")
        
        fig.canvas.draw()
        image_from_plot=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot=image_from_plot.reshape(fig.canvas.get_width_height()[::-1]+(3,))
        
        plt.savefig( path + "..\\temp\\fractale_" + str(i) + ".png"  , dpi=200 )
        
        plt.close()
            
        print("= = = = = = = = = = = = ")

    generateGif()
    
elif(gif == "None"):
    
    output = np.zeros((yWidth,xWidth,3),dtype = 'float')
    mandelbrot( output , power , R , show = True , verbose = True)
    
    
