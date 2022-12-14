import numpy as np
import matplotlib.pyplot as plt
import imageio as iio

from colour import Color

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\kleinian\\"

# ==== --- PARAMETERS --- ==== #

epsilon = 5e-2
iterMax = 13

xMin = -50
xMax = 50

yMin = -50
yMax = 50

xWidth = int( (xMax - xMin) / epsilon )
yWidth = int( (yMax - yMin) / epsilon )

print("xWidth = " + str(xWidth) )
print("yWidth = " + str(yWidth) )

# ==== ------ ==== #

# ==== --- VISUALS --- ==== #

# orange = Color("orange")
# red = Color("red")
# purple = Color("purple")
# blue = Color("blue")
# green = Color("green")
# yellow = Color("yellow")

# colours = list(orange.range_to(red,int((iterMax+1)/5)))
# colours += list(red.range_to(purple,int((iterMax+1)/5)))
# colours += list(purple.range_to(blue,int((iterMax+1)/5)))
# colours += list(blue.range_to(green,int((iterMax+1)/5)))
# colours += list(green.range_to(yellow,int((iterMax+1)/5)))

black = Color("black")
colours = list(black.range_to(black,iterMax+1))

colours = [col.rgb for col in colours]


# For the gif
images = []

# ==== ------ ==== #


    
def coord( x , y ):
    '''
    Converts complex coordinates x+iy to pixel coordinates (i,j) on the grid of size xWidth * yWidth
    '''
    
    i = (yWidth-1) * (y-yMax)/(yMin-yMax)
    j = (xWidth-1) * ( 1 - (x-xMax)/(xMin-xMax) )
    
    return (int(i),int(j))
    
def transfo( M , z ):
    '''
    Applies the Mobius transformation M to the complex z
    '''
    
    return ( M[0,0] * z + M[0,1] ) / (M[1,0] * z + M[1,1])

class point_obj():
    
    def __init__(self , lastTransfo , coord ):
        '''
        The lastTransfo integer represents how the complex coord got there.
        For example, if it has reached coord with the transformation A , 
        the next iteration of the coord will be calculated using A, B and B^(-1) ( and not A^(-1) )
        '''
        
        self.lastTransfo = lastTransfo
        self.coord = coord

def is_far(z1,z2):
    '''
    Returns True if the complex z1 is far enough from the complex z2. False otherwise
    '''
    res = 1
    
    return( np.abs(z1-z2) > res )
    

def fractal( output , tr_a , tr_b , gif , iterMax ):
    
    iter = 0
    
    # === -- D??finition des transformations A B A^(-1) et B^(-1) -- === #
    
    tr_ab = ( tr_a * tr_b - np.sqrt(tr_a**2 * tr_b**2 -4*tr_a**2 -4*tr_b**2) ) / 2
    
    z0 = (tr_ab - 2) * tr_b / ( tr_b * tr_ab - 2*tr_a +2j*tr_ab )

    A = np.array([[tr_a/2 , (tr_a*tr_ab-2*tr_b+4j)/(z0*(2*tr_ab+4))],[(tr_a*tr_ab-2*tr_b-4j)*z0/(2*tr_ab-4) , tr_a/2]])
    
    B = np.array([[(tr_b-2j)/2 , tr_b/2],[tr_b/2 , (tr_b+2j)/2]])
    
    A_1 = np.array([[ A[1,1] , -A[1,0] ],[ -A[0,1] , A[0,0] ]])
    
    B_1 = np.array([[ B[1,1] , -B[1,0] ],[ -B[0,1] , B[0,0] ]])

    # === ---- === #
    
    # Fixed points of each transformation
    z_list = [ z0,
                             
               (A[0,0]-A[1,1] + np.sqrt( (A[0,0]-A[1,1])**2 +4*A[1,0]*A[0,1] ) )/(2*A[1,0]) , 
               (A[0,0]-A[1,1] - np.sqrt( (A[0,0]-A[1,1])**2 +4*A[1,0]*A[0,1] ) )/(2*A[1,0]) ,
               
               (B[0,0]-B[1,1] + np.sqrt( (B[0,0]-B[1,1])**2 +4*B[1,0]*B[0,1] ) )/(2*B[1,0]) , 
               (B[0,0]-B[1,1] - np.sqrt( (B[0,0]-B[1,1])**2 +4*B[1,0]*B[0,1] ) )/(2*B[1,0]) ,
               
               (A_1[0,0]-A_1[1,1] + np.sqrt( (A_1[0,0]-A_1[1,1])**2 +4*A_1[1,0]*A_1[0,1] ) )/(2*A_1[1,0]) , 
               (A_1[0,0]-A_1[1,1] - np.sqrt( (A_1[0,0]-A_1[1,1])**2 +4*A_1[1,0]*A_1[0,1] ) )/(2*A_1[1,0]) ,
               
               (B_1[0,0]-B_1[1,1] + np.sqrt( (B_1[0,0]-B_1[1,1])**2 +4*B_1[1,0]*B_1[0,1] ) )/(2*B_1[1,0]) , 
               (B_1[0,0]-B_1[1,1] - np.sqrt( (B_1[0,0]-B_1[1,1])**2 +4*B_1[1,0]*B_1[0,1] ) )/(2*B_1[1,0]) ]
    
    
    # z_list = [z0]
    
    print("===\nz list :")
    for z in z_list:
        print(z)
    print("===")
    
    initial_z_list = z_list.copy()
    
    # === ---- === #
    
    
    # === -- Calcul et affichage de toutes les transformations r??duites possibles -- === #
    
    point_list = [ point_obj( -1 , z ) for z in z_list ]
    
    while( (len(point_list) > 0) and (iter < iterMax) ):
        
        iter+=1
        
        N = len(point_list) - 1
        
        print("===\nIteration : "+ str(iter) +" / " + str(iterMax))
        print("Length of the points list : " + str(N+1)+"\n===")
        
        for i in range(N , -1 , -1):
            
            point = point_list.pop(i)
            
            newTransfo = [0,1,2,3]
            if( point.lastTransfo != -1 ):
                newTransfo.remove( [1,0,3,2][point.lastTransfo] )
            
            # If the point is inside our grid
            if( np.real(point.coord) > xMin and np.real(point.coord) < xMax and np.imag(point.coord) > yMin and np.imag(point.coord) < yMax):
                
                (x,y) = coord( np.real(point.coord) , np.imag(point.coord) )
                output[ x,y ] = colours[iter]
                
                if (iter < iterMax ):
                    for tr in newTransfo:
                        new_point = transfo( [A,A_1,B,B_1][tr] , point.coord )
                        
                        # If the new point is not too close from the previous point
                        if( is_far( point.coord , new_point) ):
                            
                            point_list.append( point_obj( tr , new_point ) )
    
        
        # == Saving the gif == #
        if( gif ):
            
            fig,axs=plt.subplots(1,1)
            
            axs.imshow(output,extent=[xMin,xMax,yMin,yMax])
            
            axs.set_title('tr_a = ' + str(tr_a) + ' tr_b = ' + str(tr_b) )
            
            axs.set_xlabel("Real part")
            axs.set_ylabel("Imaginary part")
            
            fig.canvas.draw()
            image_from_plot=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            image_from_plot=image_from_plot.reshape(fig.canvas.get_width_height()[::-1]+(3,))
            
            images.append(image_from_plot)
            
            plt.close()
        
        
    # === ---- === #
    
    if( gif ):
        print("Saving the gif ...")
        iio.mimsave( path + str(tr_a) + str(tr_b) + '.gif', images , fps = 5 )
        print("Gif saved !")
    
    for z in initial_z_list:
        (x,y) = coord( np.real(z) , np.imag(z) )
        if( x >= 0 and x<xWidth and y>=0 and y<yWidth):
            output[ x,y ] = [1,0,0]
                
    plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
    
    plt.title('tr_a = ' + str(tr_a) + ' tr_b = ' + str(tr_b) )
    
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    
    plt.savefig( path + str(tr_a) + str(tr_b) + ".png" , dpi=600 )
    
    plt.show()
    
    
output = 1-np.zeros((yWidth,xWidth,3),dtype = 'float')

fractal( output,  tr_a = 1.91 +.05j , tr_b = 3+0j , gif = False , iterMax = iterMax )




