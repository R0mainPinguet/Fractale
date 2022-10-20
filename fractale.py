import numpy as np
import matplotlib.pyplot as plt

from colour import Color

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\"

# ==== --- PARAMETERS --- ==== #

width = 3200

resolution = 1e-3

xMin = -5
xMax = 20

yMin = -5
yMax = 20

iter = 800


# red = Color("red")
# blue = Color("blue")
black = Color("black")

# colours = list(red.range_to(blue,iter+1))
colours = list(black.range_to(black,iter+1))
colours = [col.rgb for col in colours]



# ==== ------ ==== #

    
def coord( x , y ):
    i = (width-1) * (y-yMax)/(yMin-yMax)
    j = (width-1) * ( 1 - (x-xMax)/(xMin-xMax) )
    
    return (int(i),int(j))
    
def transfo( M , z ): 
    return ( M[0,0] * z + M[0,1] ) / (M[1,0] * z + M[1,1])




class point_obj():
    
    def __init__(self , lastTransfo , coord ):
        self.lastTransfo = lastTransfo
        self.coord = coord
            
def fractal( tr_a , tr_b ):
    
    output = 1-np.zeros((width,width,3),dtype = 'float')

    # === -- Définition des transformations A B A**-1 B**-1 -- === #
    
    tr_ab = ( tr_a * tr_b - np.sqrt(tr_a**2 * tr_b**2 -4*tr_a**2 -4*tr_b**2) ) / 2
    
    z0 = (tr_ab - 2) * tr_b / ( tr_b * tr_ab - 2*tr_a +2j*tr_ab )

    A = np.array([[tr_a/2 , (tr_a*tr_ab-2*tr_b+4j)/(z0*(2*tr_ab+4))],[(tr_a*tr_ab-2*tr_b-4j)*z0/(2*tr_ab-4) , tr_a/2]])
    
    B = np.array([[(tr_b-2j)/2 , tr_b/2],[tr_b/2 , (tr_b+2j)/2]])
    
    A_1 = np.array([[ A[1,1] , -A[1,0] ],[ -A[0,1] , A[0,0] ]])
    
    B_1 = np.array([[ B[1,1] , -B[1,0] ],[ -B[0,1] , B[0,0] ]])

    # === ---- === #
    
    # Fixed points of each transformation
    z_list = [ (A[0,0]-A[1,1] + np.sqrt( (A[0,0]-A[1,1])**2 +4*A[1,0]*A[0,1] ) )/(2*A[1,0]) , 
               (A[0,0]-A[1,1] - np.sqrt( (A[0,0]-A[1,1])**2 +4*A[1,0]*A[0,1] ) )/(2*A[1,0]) ,
               
               (B[0,0]-B[1,1] + np.sqrt( (B[0,0]-B[1,1])**2 +4*B[1,0]*B[0,1] ) )/(2*B[1,0]) , 
               (B[0,0]-B[1,1] - np.sqrt( (B[0,0]-B[1,1])**2 +4*B[1,0]*B[0,1] ) )/(2*B[1,0]) ,
               
               (A_1[0,0]-A_1[1,1] + np.sqrt( (A_1[0,0]-A_1[1,1])**2 +4*A_1[1,0]*A_1[0,1] ) )/(2*A_1[1,0]) , 
               (A_1[0,0]-A_1[1,1] - np.sqrt( (A_1[0,0]-A_1[1,1])**2 +4*A_1[1,0]*A_1[0,1] ) )/(2*A_1[1,0]) ,
               
               (B_1[0,0]-B_1[1,1] + np.sqrt( (B_1[0,0]-B_1[1,1])**2 +4*B_1[1,0]*B_1[0,1] ) )/(2*B_1[1,0]) , 
               (B_1[0,0]-B_1[1,1] - np.sqrt( (B_1[0,0]-B_1[1,1])**2 +4*B_1[1,0]*B_1[0,1] ) )/(2*B_1[1,0]) ]
    
    
    # z_list = [z0]
    
    # for z in z_list:
    #     print(z)
    
    # === -- Calcul et affichage de toutes les transformations réduites possibles -- === #
    
    point_list = [ point_obj( -1 , z ) for z in z_list ]
    visited_points = []
    
    while( len(point_list) > 0 ):
        
        print(len(point_list))
        
        N = len(point_list) - 1
        
        for i in range(N , -1 , -1):
            
            point = point_list[i]
            
            newTransfo = [0,1,2,3]
            if( point.lastTransfo != -1 ):
                newTransfo.remove( [1,0,3,2][point.lastTransfo] )
            
            (x,y) = coord( np.real(point.coord) , np.imag(point.coord) )
            if( x >= 0 and x<width and y>=0 and y<width):

                # If the grid point has never been reached
                if( (output[x,y]==[1,1,1]).all()):
                    output[ x,y ] = [0,0,0]
                    
                    for tr in newTransfo:
                        point_list.append( point_obj( tr , transfo( [A,A_1,B,B_1][tr] , point.coord ) ) )
                    
            point_list.pop(i)
    
    # === ---- === #
    
    plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
    
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    
    plt.savefig( path + "img.png" , dpi=600 )
    
    plt.show()




fractal( tr_a = 1.87 + .1j , tr_b = 1.87 - .1j )




