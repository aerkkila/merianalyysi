#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>

const char* restrict tiednimi = "/home/aerkkila/b/jääkartat/netcdf/19901112140000_icechart.nc";

const float latraja  = 60.2;
#ifndef KONSRAJA
#define KONSRAJA 1.0 //prosentteina
#endif
#define NCVIRHE(arg) printf("Netcdf-virhe: %s\n", nc_strerror(arg))
#define NCFUNK(fun, ...)			\
  do {						\
    if((ncpalaute = fun(__VA_ARGS__)))		\
      NCVIRHE(ncpalaute);			\
  } while(0)

const int ypit2=3120, xpit2=2640;
const int xpit0=700; //muutettaessa huomioitakoon myös countpt
const size_t countpt0[] = {1, 1, 700};
int ypit0, yalku0=0;
int xpit1, xalku0;
int ncpalaute;
float *lat, *lon, *lat0;
char* var;
FILE* f_ulos;

void lue_koordinaatit1(int ncid);
void maarita_i_alut(int* i_alku);
int  lue_muuttuja0(int ncid, int* i_alku);

/*Tarvittavat koot ovat
  xypit2: koko kartan koko
  xypit0: se osa, joka todellisuudessa tarvitaan. Tämä on viimeisenä määritettävä tarkin arvo.*/
int main(int argc, char** argv) {
  char apuc[300];
  int vuosi0=1991, vuosi1=2021;
  size_t xypit2 = xpit2*ypit2;
  
  /*mahdolliset komentoriviargumentit*/
  if(argc > 1)
    if(sscanf(argv[1], "%i", &vuosi0)!=1)
      printf("Ei luettu alkuvuotta\n");
  if(argc > 2)
    if(sscanf(argv[2], "%i", &vuosi1)!=1)
      printf("Ei luettu loppuvuotta\n");

  lat = malloc(ypit2*sizeof(float));
  lon = malloc(xpit2*sizeof(float));

  int ncid;
  NCFUNK(nc_open, tiednimi, NC_NOWRITE, &ncid);
  lue_koordinaatit1(ncid);

  /*tarkempi alkupiste*/
  while(lat[++yalku0] < latraja);
  ypit0 = ypit2-yalku0;
  lat0 = lat+yalku0;

  size_t xypit0 = ypit0 * xpit0;
  int i_alku[ypit0];
  maarita_i_alut(i_alku);

  var = malloc(xypit0); //vino kartta
  char* kartta = malloc(xpit1*ypit0); //oikaistu kartta
  memset(kartta, 1, xpit1*ypit0); //maa on 1, meri 0
  
  if(lue_muuttuja0(ncid, i_alku)) //var
    return 1;
  NCFUNK(nc_close, ncid);
  
  /*kartta täytyy oikaista tulostettaessa*/
  for(int j=0; j<ypit0; j++) {
    size_t vasen = i_alku[j]-xalku0;
    memcpy(kartta+j*xpit1+vasen, var+j*xpit0, xpit0);
  }
  FILE* f_ulos = fopen("kartmask.bin", "wb");
  fwrite(kartta, xpit1*ypit0, 1, f_ulos);
  fclose(f_ulos);
  free(lat); free(lon); free(var); free(kartta);
  return 0;
}

/*alueesta luetaan aina xpit0:n pituinen pätkä y:n mukaan vaihtelevasta alkukohdasta
  lat ja lon ovat koko alueesta tässä vaiheessa*/
void maarita_i_alut(int* i_alku) {
  int j=0;
  int lukema = 950;
  xalku0 = lukema;
  while(lat0[j] < 63.0)
    i_alku[j++] = lukema;
  while(lat0[j] < 64.68)
    i_alku[j++] = ++lukema;
  while(j < ypit0)
    i_alku[j++] = lukema;
  xpit1 = xpit0 + lukema-xalku0;
}

void lue_koordinaatit1(int ncid) {
  int id;
  NCFUNK(nc_inq_varid, ncid, "lat", &id);
  NCFUNK(nc_get_var, ncid, id, lat);
  NCFUNK(nc_inq_varid, ncid, "lon", &id);
  NCFUNK(nc_get_var, ncid, id, lon);
}

int lue_muuttuja0(int ncid, int* i_alku) {
  int id;
  NCFUNK(nc_inq_varid, ncid, "kFmiLandSeaMask", &id);
  if(ncpalaute)
    return ncpalaute;
  size_t alku[3] = { [0] = 0, [1] = yalku0-1 };
  for(int j=0; j<ypit0; j++) {
    alku[2] = i_alku[j];
    alku[1]++;
    NCFUNK(nc_get_vara_uchar, ncid, id, alku, countpt0, var+j*xpit0);
  }
  return 0;
}
