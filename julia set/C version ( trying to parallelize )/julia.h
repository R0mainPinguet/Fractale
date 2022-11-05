#ifndef JULIAHEADER
#define JULIAHEADER

typedef struct complex{
  double re;
  double im;
  double norm2;
} complex ;

/* Color defined with rgb from 0 to 255 */
typedef struct color{
  int r;
  int g;
  int b;
} color ;

typedef struct img{
  int rows;
  int cols;
  int* data;
} img ;

void print_complex(complex*);

img* create_img(int,int);
void create_complex( complex* , double,double );

void julia_img(double,double,double,double, int,double,complex* , int , int);

#endif




