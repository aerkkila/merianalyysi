#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>
#include <math.h>
//#include <zip.h>
#include <dirent.h>

const char* lahdekansio = "/mnt/share/data/balticsea/icechart/netcdf";

const double r        = 6371229;
const float latraja  = 60.2;
#ifndef KONSRAJA
#define KONSRAJA 0.0
#endif
#define NCVIRHE(arg) printf("Virhe: %s\n", nc_strerror(arg))
#define NCFUNK(fun, ...)			\
  do {						\
    if((ncpalaute = fun(__VA_ARGS__)))		\
      NCVIRHE(ncpalaute);			\
  } while(0)

const int j0=1600, j1=3120;
const int ypit2=3120, xpit2=2640;
const int xpit0=700;
size_t alkupiste, loppupiste;
size_t alkuind; //tähän laitetaan tarkempi arvo
int ypit0;
int ncpalaute;
float *lat, *lon;
double *var, *alat;
FILE* f_ulos;

DIR* avaa_vuosi(int vuosi, char* polku_ulos, char* osanimi_ulos);
int pura_seuraava(DIR *d, char* volatile polku, char* osanimi);
void poista_tiedosto(const char* nimi);
int avaa_netcdf(const char* restrict);
void lue_koordinaatit1(char* tnimi, size_t alkupiste, size_t loppupiste);
void maarita_i_alut(float* lat, float* lon, int* i_alku);
int lue_muuttuja0(int ncid, int* i_alku);
int lue_koordinaatit0(int ncid, int* i_alku);
void laske_pintaalat();

/*Tarvittavat koot ovat
  xypit2: koko kartan koko
  xypit1: yhtenäisen enintään luettavan alueen koko
  xypit0: se osa, joka todellisuudessa tarvitaan*/
int main(int argc, char** argv) {
  char apuc[300], *apuc1;
  int vuosi0=1980, vuosi1=2010, xtark, ytark;
  alkupiste  = j0*xpit2;
  loppupiste = j1*xpit2;
  size_t xypit1=loppupiste-alkupiste, xypit2=xpit2*ypit2;
  
  /*mahdolliset komentoriviargumentit*/
  if(argc > 1)
    if(sscanf(argv[1], "%i", &vuosi0)!=1)
      printf("Ei luettu alkuvuotta\n");
  if(argc > 2)
    if(sscanf(argv[2], "%i", &vuosi1)!=1)
      printf("Ei luettu loppuvuotta\n");

  /*nämä voivat olla liian suuria mahtuakseen pinomuistiin*/
  lat = malloc(xypit1*sizeof(float));
  lon = malloc(xypit1*sizeof(float));
  sprintf(apuc, "laajuudet%.0f_kartasta.txt", round(KONSRAJA*100));
  FILE* f_ulos = fopen(apuc, "w");

  DIR* d = avaa_vuosi(1980, apuc, apuc1);
  if(pura_seuraava(d, apuc, apuc1)) {
    printf("Ei purettu yhtään vuodesta 1980\n");
    exit(1);
  }
  int ncid = avaa_netcdf(apuc1);
  lue_koordinaatit1(apuc1, alkupiste, loppupiste);
  maarita_i_alut(lat, lon, i_alku);

  /*tarkempi alkupiste*/
  int lisa = 0;
  while(lat[++lisa] < latraja);
  alkuind = alkupiste + lisa; //x=0, ei kohta jossain keskellä x≠0

  xypit0 = xypit2 - alkuind;
  ypit0 = xypit0 / xpit2;
  if(xypit0 % xpit2)
    printf("Varoitus: alkuind ei ollut nurkassa\n");
  int i_alku[ypit0];
  var = malloc(xypit0*sizeof(double));
  alat= malloc(xypit0*sizeof(double));
  lat = realloc(lat, xypit0*sizeof(float)); //lyhennetään näitä
  lon = realloc(lon, xypit0*sizeof(float));
  
  lue_koordinaatit0(ncid, i_alku);

  NCFUNK(nc_close, ncid);
  closedir(d);
  free(lat); free(lon); free(var); free(alat);
  fclose(f_ulos);
  return 0;
}

DIR* avaa_vuosi(int vuosi, char* polku, char* osanimi) {
  sprintf(polku, "%s/%i/", lahdekansio, vuosi);
  osanimi = polku+strlen(polku); //tähän kopioidaan tiedoston nimi
  DIR *d = opendir(apuc);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", kansio);
    return NULL;
  }
  return d;
}

/*Ei taida kohtuudella onnistua avata nc-tiedostoa, joka on luettu zip-kansiosta RAM-muistiin.
  Täytyy siis ensin purkaa zip-kansio kovalevylle ja sitten lukea tiedosto sieltä
  vaikka sitä kautta lukeminen onkin hitaampaa.*/
int pura_seuraava(DIR *d, char* volatile polku, char* osanimi) {
  struct dirent* e;
  while((e = readdir(d))) {
    if(!strstr(e->d_name, ".zip"))
      continue;
    char kmnt[200];
    strcpy(osanimi, e->d_name);
    sprintf(kmnt, "unzip '%s' -d .", polku);
    system(kmnt);
    strcpy(osanimi+strlen(osanimi)-4, ".nc"); // *.zip --> *.nc
    return 0; //annettiin unzip-käsky onnistuneesti
  }
  return -1; //kansio loppui
}

void poista_tiedosto(const char* nimi) {
  char kmnt[200];
  sprintf(kmnt, "rm '%s'", nimi);
  system(kmnt);
}

/*alueesta luetaan aina xpit0:n pituinen pätkä y:n mukaan vaihtelevasta alkukohdasta*/
void maarita_i_alut(float* lat, float* lon, int* i_alku) {
  int j=0;
  int ind=0;
  int lukema = 950;
  while(lat[ind+=xpit2] < 63.0)
    i_alku[j++] = lukema;
  while(lat[ind+=xpit2] < 64.68)
    i_alku[j++] = ++lukema;
  while(j < ypit0)
    i_alku[j++] = lukema;
}

int avaa_netcdf(const char* restrict tnimi) {
  int ncid, id;
  NCFUNK(nc_open, tnimi, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "x", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xkoko);
  NCFUNK(nc_inq_dimid, ncid, "y", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ykoko);
  if(xtark != xkoko || ytark != ykoko) {
    free(lat); free(lon);
    fprintf(stderr, "Eri kokoinen hila kuin oletettiin: %i, %i\n", xkoko, ykoko);
    exit(1);
  }
  return ncid;
}

void lue_koordinaatit1(int ncid, size_t alkupiste, size_t loppupiste) {
  int id;
  NCFUNK(nc_inq_varid, ncid, "lat", &id);
  NCFUNK(nc_get_vara, ncid, alkupiste, loppupiste, lat);
  NCFUNK(nc_inq_varid, ncid, "lon", &id);
  NCFUNK(nc_get_vara, ncid, alkupiste, loppupiste, lon);
}

void lue_koordinaatit0(int ncid, int* i_alku) {
  int idlat, idlon;
  NCFUNK(nc_inq_varid, ncid, "lat", &idlat);
  NCFUNK(nc_inq_varid, ncid, "lon", &idlon);
  int alkunurkka = alkuind;
  for(int j=0; j<ypit0; j++) {
    NCFUNK(nc_get_vara, ncid, idlat, alkunurkka+i_alku[j], alkunurkka+i_alku[j]+xpit0, lat+j*xpit0);
    NCFUNK(nc_get_vara, ncid, idlat, alkunurkka+i_alku[j], alkunurkka+i_alku[j]+xpit0, lon+j*xpit0);
    alkunurkka += xpit2;
  }
}

void lue_muuttuja0(int ncid, int* i_alku) {
  int id;
  NCFUNK(nc_inq_varid, ncid, "kFmiIceConcentration", &id);
  int alkunurkka = alkuind;
  for(int j=0; j<ypit0; j++) {
    NCFUNK(nc_get_vara, ncid, idlat, alkunurkka+i_alku[j], alkunurkka+i_alku[j]+xpit0, lat+j*xpit0);
    alkunurkka += xpit2;
  }
}

#define PINTAALA(lat1, lat2, lon1, lon2) (((lon2)-(lon1))*r*r*(sinf(lat2)-sinf(lat1))*1.0e-6)
#define RAD(a) ((a)*0.017453293)

void laske_pintaalat() {
#ifdef TALLENNA_PINTAALAT
  FILE *f = fopen("hilan_pintaalat.txt", "w");
#endif
  for(int j=0; j<ypit0-1; j++)
    for(int i=0; i<xpit0-1; i++) {
      float lat1=lat[j*xpit0+i], lat2=lat[(j+1)*xpit0+i], lon1=lon[j*xpit0+i], lon2=lon[j*xpit0+i+1];
      alat[j*xpit+i] = PINTAALA(RAD(lat1), RAD(lat2), RAD(lon1), RAD(lon2)));
#ifdef TALLENNA_PINTAALAT 
      fprintf(f, "%.5lf\t%i\t%i\t%.3f\t%.3f\t%.3f\t%.3f\n", alat[j*xpit+i], j, i, lat[j*xpit+i], lat[(j+1)*xpit+i], lon[j*xpit+i], lon[j*xpit+i+1]);
#endif
    }
#ifdef TALLENNA_PINTAALAT
  fclose(f);
#endif
}

#if 0
  double pa = 0;
  for(int j=0; j<ypit-1; j++)
    for(int i=0; i<xpit-1; i++)
      pa += (kons[j*xpit+i] >= KONSRAJA) * alat[j*xpit+i];
  fprintf(f_ulos, "%6.0lf\n", round(pa)); //,\t%3i\t%4i\n", round(pa), paiva+1, vuosi);
  }
  return 0;
}
#endif
