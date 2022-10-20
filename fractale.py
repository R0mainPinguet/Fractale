import numpy as np
import matplotlib.pyplot as plt

# from colour import Color

# ==== --- PARAMETERS --- ==== #

width = 800

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
    
transfo = lambda M , z : ( M[0,0] * z + M[0,1] )/(M[1,0] * z + M[1,1])


class Tree():
    def __init__(self,indice):
        self.indice = indice
        self.childs = []
        
        if (self.indice == -1 ):
            self.childs = []
    
    def clear(self):
        self.indice = -1
        self.childs = []
        
    def size(self):
        if(self.childs == [] ):
            return(1)
        else:
            s = 0
            for x in self.childs:
                s += x.size()
                
            return(1+s)

    # def create_childs(self , N):
    #     if(N>0):
    #         index = self.indice
    #         l = [0,1,2,3]
    #         
    #         if( index != -1 ):
    #             
    #             l.remove( [1,0,3,2][index] )
    #             
    #         for x in l:
    #             self.childs.append( Tree(x) )
    #         
    #         for child in self.childs:
    #             child.create_childs(N-1)
                

    def print_fractal(self , output , transfo_list , z_list , depth , N):
        
        if( N>0):
            
            index = self.indice
            l = [0,1,2,3]
            
            if( index != -1 ):
                l.remove( [1,0,3,2][index] )
                
            if( index == -1 ):
                
                for z in z_list:
        
                    (x,y) = coord( np.real(z) , np.imag(z) )
                    if( x >= 0 and x<width and y>=0 and y<width):
                        output[ x,y ] = colours[0]
                
                for c in l:
                    self.childs.append( Tree(c) )
                
                for child in self.childs:
                    child.print_fractal( output ,  transfo_list , z_list , depth+1 , N-1 )
                    
            else:
                
                z_list = [ transfo( transfo_list[self.indice] , z ) for z in z_list ]
                
                for i in range(len(z_list)-1,-1,-1):
                    
                    z = z_list[i]
                    
                    (x,y) = coord( np.real(z) , np.imag(z) )
                    if( x >= 0 and x<width and y>=0 and y<width):
                        
                        # If the grid has already been changed
                        if( (output[x,y]==[1,1,1]).all()):
                            output[ x,y ] = colours[depth]
                        else:
                            z_list.pop(i)
                
                for c in l:
                    self.childs.append( Tree(c) )
                    
                if( z_list != [] ):
                    for child in self.childs:
                        child.print_fractal( output , transfo_list , z_list , depth+1 , N-1)
                
            
            
            
            


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
    
    arbre = Tree(-1)
    
    arbre.print_fractal( output , [ A , A_1 , B , B_1 ] , z_list , depth=0 , N=iter)

    print(arbre.size())
    
    # === ---- === #
    
    plt.imshow(output,extent=[xMin,xMax,yMin,yMax])
    
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    
    plt.show()




fractal( tr_a = 1.87 + .1j , tr_b = 1.87 - .1j )




