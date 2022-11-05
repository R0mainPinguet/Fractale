#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <omp.h>

#include "julia.h"

int main( int argc , char* argv[] ){
  
  /* JULIA PARAMETERS */
  
  int WIDTH = 1800;
  int HEIGHT = 1800;
  
  double xMin = -2;
  double xMax = 2;
  double yMin = -2;
  double yMax = 2;

  int iterMax = 100;
  double R = 2;
  
  /* ----- */

  /* PROGRAM AND GIF PARAMETERS */
  
  int choice;
  double tStart;
  double tEnd;
  
  if(argc<4 || argc>5){
    printf("Wrong number of arguments !\nFirst argument : 0 = No gif ; 1 = Gif\n");
    printf("Second and Third argument : real and imaginary parts of c\n");
    printf("If we are making a gif : Fourth argument : number of images\n");
    return(0);
  }

  sscanf( argv[1] , "%d" , &choice );
  /* ----- */

  tStart = omp_get_wtime();

  if(choice == 0 ){
    
    double re = 0;
    double im = 0;
    complex* c = malloc( sizeof(complex) );
    
    sscanf( argv[2] , "%lf" , &re);
    sscanf( argv[3] , "%lf" , &im);
    create_complex( c , re , im );
    
    printf("c = ");
    print_complex(c);
    printf("\n");
    
    julia_img(xMin,xMax,yMin,yMax , iterMax , R , c , WIDTH , HEIGHT );
    
    free(c);
      
  }else{
    int i = 0;
    int imageCount;
        
    double re = 0;
    double im = 0;
    complex* c0 = malloc(sizeof(complex));

    sscanf( argv[2] , "%lf" , &re);
    sscanf( argv[3] , "%lf" , &im);
    create_complex( c0 ,  re , im );

    sscanf( argv[4] , "%d" , &imageCount );
    
    #pragma omp parallel for schedule(dynamic)
    for (i = 0 ; i < imageCount ; i++){

      complex* c = malloc(sizeof(complex));
      double theta = i *  2 * 3.141592 / ( (double) imageCount);
      
      /* Name definition */
      char iString[32];
      char name[32] = "temp/fractale_";
      
      sprintf(iString , "%d", i);
      strcat(name , iString);
      strcat(name , ".data");
      /* ----- */
            
      create_complex(c , c0->re*cos(theta) - c0->im*sin(theta) , c0->re*sin(theta) + c0->im*cos(theta) );
      
      printf("c = ");
      print_complex(c);
      printf("\n");
      
      julia_img(xMin,xMax,yMin,yMax , iterMax , R , c , WIDTH , HEIGHT );

      free(c);
      
    }

    free(c0);
  }

  tEnd = omp_get_wtime();
  
  printf("Time for the serial gif : %f\n", tEnd - tStart );

  return 0;
}
