#include <complex.h> /*bibliothèque pour afficher en c*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

/*Resolution*/
int WIDTH = 3840;
int HEIGHT = 2160;
/******************/

void printc(float complex);
void print_tabc(float complex *u, int n);
float complex *un(float complex, int, float complex, float complex*);
float *inter(float, float, int, float*);
int julia(float complex, float complex);
void save_texture(SDL_Renderer *, SDL_Texture *, const char *);

/************************************************/
/************Fonctions Annexes*******************/
/************************************************/

/***Affichage complexes et tableau de complexe***/
void printc(float complex z){
    printf("%f + %fj", creal(z), cimag(z));
}

void print_tabc(float complex *u, int n){
    for(int i = 0; i<n; i++){
        printc(u[i]);
        printf(" ");
    }
    printf("\n");
}

void print_tab(float *tab, int n){
    for(int i = 0; i<n; i++){
        printf("%f ", tab[i]);
    }
    printf("\n");
}

/************************************************/

float* inter(float min, float max, int nbrelement, float* intervalle){
    intervalle[0] = min;
    for (int i = 1; i<nbrelement; i++){
        intervalle[i] = intervalle[i-1] + (max - min)/(nbrelement-1);
    } 
    return intervalle;
}


/************************************************/
/************Fonctions Principales***************/
/************************************************/

float complex *un(float complex c, int n, float complex u0, float complex *u){
    u[0] = u0;
    for (int i = 1; i<n; i++){
        u[i] = u[i-1]*u[i-1] + c;
    }
    return u;
}

 int julia(float complex c, float complex u0){
    int R = 4;
    int nbr = 100;
    int count = 0;
    
    float complex z = u0;
    for (int i = 0; i<nbr; i++){
        if(cabsf(z) > R){  /*valeur absolue de l[i]*/
            return count;
        }
        else {
            count += 1;
        }
        z = z*z + c;
    }
    return 200;
 }

void save_texture(SDL_Renderer *ren, SDL_Texture *tex, const char *filename)
{
    SDL_Texture *ren_tex;
    SDL_Surface *surf;
    int st;
    int w;
    int h;
    int format;
    void *pixels;

    pixels  = NULL;
    surf    = NULL;
    ren_tex = NULL;
    format  = SDL_PIXELFORMAT_RGBA32;

    /* Get information about texture we want to save */
    st = SDL_QueryTexture(tex, NULL, NULL, &w, &h);
    if (st != 0) {
        SDL_Log("Failed querying texture: %s\n", SDL_GetError());
        goto cleanup;
    }

    ren_tex = SDL_CreateTexture(ren, format, SDL_TEXTUREACCESS_TARGET, w, h);
    if (!ren_tex) {
        SDL_Log("Failed creating render texture: %s\n", SDL_GetError());
        goto cleanup;
    }

    /*
     * Initialize our canvas, then copy texture to a target whose pixel data we 
     * can access
     */
    st = SDL_SetRenderTarget(ren, ren_tex);
    if (st != 0) {
        SDL_Log("Failed setting render target: %s\n", SDL_GetError());
        goto cleanup;
    }

    SDL_SetRenderDrawColor(ren, 0x00, 0x00, 0x00, 0x00);
    SDL_RenderClear(ren);

    st = SDL_RenderCopy(ren, tex, NULL, NULL);
    if (st != 0) {
        SDL_Log("Failed copying texture data: %s\n", SDL_GetError());
        goto cleanup;
    }

    /* Create buffer to hold texture data and load it */
    pixels = malloc(w * h * SDL_BYTESPERPIXEL(format));
    if (!pixels) {
        SDL_Log("Failed allocating memory\n");
        goto cleanup;
    }

    st = SDL_RenderReadPixels(ren, NULL, format, pixels, w * SDL_BYTESPERPIXEL(format));
    if (st != 0) {
        SDL_Log("Failed reading pixel data: %s\n", SDL_GetError());
        goto cleanup;
    }

    /* Copy pixel data over to surface */
    surf = SDL_CreateRGBSurfaceWithFormatFrom(pixels, w, h, SDL_BITSPERPIXEL(format), w * SDL_BYTESPERPIXEL(format), format);
    if (!surf) {
        SDL_Log("Failed creating new surface: %s\n", SDL_GetError());
        goto cleanup;
    }

    /* Save result to an image */
    st = SDL_SaveBMP(surf, filename);
    if (st != 0) {
        SDL_Log("Failed saving image: %s\n", SDL_GetError());
        goto cleanup;
    }

    SDL_Log("Saved texture as BMP to \"%s\"\n", filename);

cleanup:
    SDL_FreeSurface(surf);
    free(pixels);
    SDL_DestroyTexture(ren_tex);
}


int main(int argc, char** argv)
{    
    SDL_Window *window = NULL;
    SDL_Renderer *renderer = NULL;

    //Création d'un rectangle

    int statut = EXIT_FAILURE;
    if(0 != SDL_Init(SDL_INIT_VIDEO))
    {
        printf("Erreur SDL_Init: %s\n", SDL_GetError());
        goto Quit;
    }
    window = SDL_CreateWindow("SDL2", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,WIDTH,HEIGHT,SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE );
    if(NULL == window)
    {
        printf("Erreur SDL_CreateWindow: %s\n", SDL_GetError());
        goto Quit;
    }
    renderer = SDL_CreateRenderer(window, -1,SDL_RENDERER_ACCELERATED);
    if(NULL == renderer)
    {
        printf("Erreur SDL_CreateRenderer: %s\n", SDL_GetError());
        goto Quit;
    }
    
    /*couleur de fond blanche*/
    SDL_SetRenderDrawColor(renderer, 255,255,255,255);
    SDL_RenderClear(renderer);

    float temps;
    clock_t t1, t2;

    float x_min = -1.8, x_max = 1.8;
    float y_min = -1.2, y_max = 1.2;
    float complex c = 0.3 + 0.5*I;

    t1 = clock();
    float *X = (float*)malloc(WIDTH*sizeof(float));
    float *Y = (float*)malloc(HEIGHT*sizeof(float));

    X = inter(x_min, x_max, WIDTH, X);
    Y = inter(y_min, y_max, HEIGHT, Y);

    int conv = 0;

    for(int x = 0; x<WIDTH; x++){
        printf("%d\n",x);
        for(int y = 0; y<HEIGHT; y++){
            float complex u0 = X[x] + Y[y]*I;
            conv = julia(c, u0);
            if(conv < 200){
                SDL_SetRenderDrawColor(renderer, conv%255,255,255,255);
                SDL_RenderDrawPoint(renderer,x,y);
            }
            else{
                SDL_SetRenderDrawColor(renderer, 0,0,0,255);
                SDL_RenderDrawPoint(renderer,x,y);
            }
        }
    }

    SDL_RenderPresent(renderer);

    SDL_Surface* pScreenShot = SDL_CreateRGBSurface(0, WIDTH, HEIGHT, 32, 0, 0,0, 0);

    if(pScreenShot)
    {
      // Read the pixels from the current render target and save them onto the surface
      SDL_RenderReadPixels(renderer, NULL, SDL_GetWindowPixelFormat(window), pScreenShot->pixels, pScreenShot->pitch);

      // Create the png screenshot file
      IMG_SavePNG(pScreenShot, "Screenshot.png");

      // Destroy the screenshot surface
      SDL_FreeSurface(pScreenShot);
    }

    free(X);
    free(Y);

    t2 = clock();
    temps = (float)(t2-t1)/CLOCKS_PER_SEC;
    printf("temps = %f\n", temps); 
    statut = EXIT_SUCCESS;

    //SDL_Event e; int quit = 0; while( quit == 0 ){ while( SDL_PollEvent( &e ) ){ if( e.type == SDL_QUIT ) quit = 1; } }
    
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
Quit:
    SDL_Quit();
    return statut;
}


        
    