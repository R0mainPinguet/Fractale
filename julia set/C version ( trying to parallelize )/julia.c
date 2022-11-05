#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#include "julia.h"

void print_complex(complex* z){
  printf("%f + %fi" , z->re , z->im);
}


img* create_img(int n_row , int n_col){
  img* image = malloc(sizeof(img));
  image->rows = n_row;
  image->cols = n_col;

  image->data = malloc(sizeof(int)*n_row*n_col);

  return(image);
}

void freeImage(img* im){
  free(im->data);
  free(im);
}

void create_complex( complex* z , double a , double b ){
  z->re = a;
  z->im = b;
  z->norm2 = pow( a , 2 ) + pow( b , 2 ); 
}

complex* coord(int i , int j , int width , int height ,
	       double xMin , double xMax , double yMin , double yMax){
  
  complex* z = malloc(sizeof(complex));

  z->re = xMax + (xMin-xMax) * (1 - (j/((double)width-1)) );
  z->im = yMax + (yMin-yMax) * (i /((double)height-1));
  z->norm2 = pow( z->re , 2 ) + pow( z->im , 2 );
  return(z);
}


/* f(z) = z**2 + c */
void f(complex* z , complex* c){
  double re = z->re;
  double im = z->im;

  z->re = pow(re,2) - pow(im,2) + c->re;
  z->im = 2 * re * im + c->im;

  z->norm2 = pow( z->re , 2 ) + pow( z->im , 2 );
  
}


/* Applies f(z) = z**2 + c until the norm exceeds R */
int julia(complex* z , complex* c , int iterMax , double R){
  int i = 0;

  while((i < iterMax) && ( z->norm2 < R*R) ){
    f(z,c);
    i++;
  }

  if(i == iterMax){
    return(-1);
  }else{
    return(i);
  }
  
}



void julia_img(double xMin , double xMax , double yMin , double yMax, int iterMax , double R, complex* c, int width , int height){

  int i = 0;
  int j = 0;
  
  img* image = create_img( width , height );

  double tStart;
  double tEnd;

  tStart = omp_get_wtime();
  
  /* For each complex, computes it's julia iterations */
  for(i = 0 ; i < height ; i++){
    
    for(j = 0 ; j < width ; j++){
      complex* z = coord( i,j , width,height , xMin,xMax,yMin,yMax );
	
      image->data[i*width + j ] = julia(z,c , iterMax , R);
      
      free(z);      
    }

  }

  tEnd = omp_get_wtime();
  
  printf("Work took %f seconds\n", tEnd - tStart);
  
  freeImage(image);
  
}
