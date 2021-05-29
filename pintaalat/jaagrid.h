#ifndef _JAAGRID_
typedef struct grid_s {
  float* lat;
  float* lon;
  int gridpit;
} grid_t;

typedef struct {
  float* alat;
  int* indeksit;
  int pituus;
} maapintaala_t;
#define _JAAGRID_
#endif

maapintaala_t maapintaala(float* lat, float* lon, int gridpit,	\
			  float lata, float laty,		\
			  float lona, float lony);
grid_t lue_grid(char* tiedosto);
float* lue_jaa(char* tiedosto, int gridpit, int* indeksit, int lukupituus);
void vapauta_grid(grid_t);
