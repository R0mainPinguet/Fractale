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
    
    z = s . ballFold( r , f . boxFold(z) ) + c
    
    '''

    #= BoxFold =#
    if( np.real(z) > 1 ):
        z = (2-np.real(z)) + np.imag(z)
    elif(np.real(z) < -1 ):
        z = (-2-np.real(z)) + np.imag(z)
    
    if( np.imag(z) > 1 ):
        z = np.real(z) + (2-np.imag(z))
    elif(np.imag(z) < -1 ):
        z = np.real(z) + (-2-np.imag(z))
    #==#
    
    z = f * z

    #= BallFold =#
    if( np.abs(z) < r ):
        z = z / (r**2)
    elif( np.abs(z) < 1 ):
        z = z / (np.abs(z)**2)
    #==#
    
    return( s * z )
    
def mandelbox( output , s,r,f , escapeRadius , show , verbose ):
       
    for i in range( yWidth ):
        
        if(verbose):
            if( not (i % 100 )):
                print("i = " + str(i) + " / " + str(yWidth) )
            
        for j in range( xWidth ):
            
            iter = 0
            z = coord_1(i,j)
            z0 = z
            
            while ( iter<iterMax and np.abs(z) < escapeRadius ):
                z = z0 + transfo(s,r,f,z)
                
                iter += 1
            
            #==# Adding colors #==#
            if( iter == iterMax ):
                output[i,j] = [0,0,0]
            else:
                output[i,j] = colours[iter]
    
    
    if( show ):
        #==# Display #==#
        plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        plt.title('s = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f) )
        
        plt.xlabel("Real part")
        plt.ylabel("Imaginary part")
        
        plt.savefig( path + 's = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f) + ".png" , dpi=400 )
        
        plt.show()



def generateGif():
    
    images = []
    
    for i in range(imageCount):
        images.append( iio.imread( path + "..\\temp\\mandelbox_" + str(i) + ".png"  ))
    
    iio.mimsave(path + 'c = ' + str(c0) + ' R = ' + str(R) + '.gif', images)
    
    
#===# PARAMETERS #===#

#==# GRID #==#
path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\mandelbox\\"

gridRes = 2e-2
iterMax = 50

xMin = -5
xMax = 5

yMin = -5
yMax = 5

xWidth = int( (xMax - xMin) / gridRes )
yWidth = int( (yMax - yMin) / gridRes )

print("= = = = = = = = = = = = ")
print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )
print("= = = = = = = = = = = = ")

output = np.zeros((yWidth,xWidth,3),dtype = 'float')
#====#

#==# COLOURS #==#
col = ["red","blue"]
colours = []

for i in range(len(col)-1):
    colours += list(Color(col[i]).range_to(Color(col[i+1]),iterMax//(len(col)-1) ))
    
colours = [c.rgb for c in colours]
#====#

#==# MANDELBOX #==#
s = 2
r = .5
f = 1

R = 5
#====#

#==# GIF TYPE #==#

# The gif can be : "Zoom" : a zoom on a particular point z0
#                  "Turn" : a change of c in f(z) = z*z + c
#                  "None" : no gif : only a picture

gif = "None"

zoom = 50
z0 = 0

#====#

imageCount = 5

if(gif == "Turn" ):
    
    for i in range(imageCount):
        
        print("image = " + str(i+1) + " / " + str(imageCount) )
        
        mandelbox( output , s,r,f , R , show = False , verbose = True)
        
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
        
        c = c * np.exp(1j * 2*np.pi / imageCount)
        
        print("= = = = = = = = = = = = ")

    generateGif()
    
elif(gif == "Zoom"):

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
        
        mandelbox( output , s,r,f , R , show = False , verbose = True )
        
        fig,axs=plt.subplots(1,1)
        
        axs.imshow(output,extent=[xMin,xMax,yMin,yMax])
        
        axs.set_title('s = ' + str(s) + ' r = ' + str(r) + ' f = ' + str(f)  )
        
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
    mandelbox( output , s,r,f , R , show = True , verbose = True)
    
    
    
