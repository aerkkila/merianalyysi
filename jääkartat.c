#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>
#include <math.h>
//#include <zip.h>
#include <dirent.h>

const char* lahdekansio = "/home/aerkkila";

const double R2      = 40592558970441; //(6371229 m)^2
const float latraja  = 60.2;
#ifndef KONSRAJA
#define KONSRAJA 0.01 //prosentteina
#endif
#define NCVIRHE(arg) do {printf("Virhe: %s\n", nc_strerror(arg)); exit(1);} while(0)
#define NCFUNK(fun, ...)			\
  do {						\
    if((ncpalaute = fun(__VA_ARGS__)))		\
      NCVIRHE(ncpalaute);			\
  } while(0)

//const int yalku1=1600, yloppu1=3120;
const int ypit2=3120, xpit2=2640;
const int xpit0=700; //muutettaessa huomioitakoon myös countpt
const size_t countpt0[] = {1, 1, 700};
int ypit0, yalku0=0;
int ncpalaute;
float *lat, *lon, *lat0;
double *var, *alat;
FILE* f_ulos;

DIR* avaa_vuosi(int vuosi, char* polku_ulos);
int pura_seuraava(DIR *d, char* volatile polku, char* osanimi);
void poista_tiedosto(const char* nimi);
int avaa_netcdf(const char* restrict);
void lue_koordinaatit1(int ncid);
void maarita_i_alut(int* i_alku);
void lue_muuttuja0(int ncid, int* i_alku);
void laske_pintaalat(int* i_alku);
double maarita_laajuus();
int maarita_paiva(const char* restrict nimi, int* paiva, int* vuosi);

/*Tarvittavat koot ovat
  xypit2: koko kartan koko
  xypit0: se osa, joka todellisuudessa tarvitaan. Tämä on viimeisenä määritettävä tarkin arvo.*/
int main(int argc, char** argv) {
  char apuc[300], *apuc1;
  int vuosi0=1980, vuosi1=2011;
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
  sprintf(apuc, "laajuudet%.0f_kartasta.txt", round(KONSRAJA*100));
  FILE* f_ulos = fopen(apuc, "w");

  DIR* d = avaa_vuosi(1980, apuc);
  apuc1 = apuc+strlen(apuc); //tähän kopioidaan tiedoston nimi
  if(pura_seuraava(d, apuc, apuc1)) {
    printf("Ei purettu yhtään vuodesta 1980\n");
    exit(1);
  }
  int ncid = avaa_netcdf(apuc1);
  lue_koordinaatit1(ncid);

  /*tarkempi alkupiste*/
  while(lat[++yalku0] < latraja);
  ypit0 = ypit2-yalku0;
  lat0 = lat+yalku0;

  size_t xypit0 = ypit0 * xpit0;
  int i_alku[ypit0];
  maarita_i_alut(i_alku);
  var = malloc(xypit0*sizeof(double));
  alat= malloc(xypit0*sizeof(double));
  laske_pintaalat(i_alku);
  
  NCFUNK(nc_close, ncid); //silmukka on helpompi, kun nämä suljetaan tässä välissä
  closedir(d);

  int paiv, vuos;
  for(int vuosi=vuosi0; vuosi<vuosi1; vuosi++) {
    d = avaa_vuosi(vuosi, apuc);
    if(!d)
      break;
    while(1) {
      if(pura_seuraava(d, apuc, apuc1))
	break;
      ncid = avaa_netcdf(apuc1);
      //tarkista_koordinaatit(ncid);
      lue_muuttuja0(ncid, i_alku);
      double pa = maarita_laajuus();
      if(maarita_paiva(apuc1, &paiv, &vuos)) {
	printf("Virheellinen tiedostonnimi: \"%s\"\n", apuc1);
	exit(1);
      }
      printf("%lf\t%i\t%i\n", pa, paiv, vuos);
      NCFUNK(nc_close, ncid);
      //poista_tiedosto(apuc1);
    }
    closedir(d);
    d = NULL;
  }
  if(d)
    closedir(d);
  free(lat); free(lon); free(var); free(alat);
  fclose(f_ulos);
  return 0;
}

int maarita_paiva(const char* restrict nimi, int* paiva, int* vuosi) {
  int kk;
  static int vuosi365[] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334}; //kuukauden alussa kuluneet päivät
  static int vuosi366[] = {0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335};
  if(sscanf(nimi, "%4d%2d%2d", vuosi, &kk, paiva) != 3)
    return 1;
  if(*vuosi%4) {
    *paiva = vuosi365[kk-1] + *paiva-1; //kuukauden päivästä vuoden päiväksi
    int tmp = *paiva; //ilman tätä tämä ei toimi, vaikka nähdäkseni pitäisi
    *paiva = (tmp+122) % 365 - 122; //vähintään 243 pyörähtää ympäri ja palaa negatiiviseksi
  } else {
    *paiva = vuosi366[kk-1] + *paiva-1;
    int tmp = *paiva;
    *paiva = (tmp+122) % 366 - 122;
  }
  *vuosi += (*paiva<0);
  return 0;
}

DIR* avaa_vuosi(int vuosi, char* polku) {
  sprintf(polku, "%s/%i/", lahdekansio, vuosi);
  DIR *d = opendir(polku);
  if(!d) {
    printf("Kansiota \"%s\" ei voitu avata\n", polku);
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
    sprintf(kmnt, "unzip -u '%s' -d .", polku);
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

/*alueesta luetaan aina xpit0:n pituinen pätkä y:n mukaan vaihtelevasta alkukohdasta
  lat ja lon ovat koko alueesta tässä vaiheessa*/
void maarita_i_alut(int* i_alku) {
  int j=0;
  int lukema = 950;
  while(lat0[j] < 63.0)
    i_alku[j++] = lukema;
  while(lat0[j] < 64.68)
    i_alku[j++] = ++lukema;
  while(j < ypit0)
    i_alku[j++] = lukema;
}

int avaa_netcdf(const char* restrict tnimi) {
  int ncid, id;
  size_t xtesti, ytesti;
  NCFUNK(nc_open, tnimi, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "lon", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xtesti);
  NCFUNK(nc_inq_dimid, ncid, "lat", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ytesti);
  if(xtesti != xpit2 || ytesti != ypit2) {
    fprintf(stderr, "Eri kokoinen hila kuin oletettiin: %lu, %lu\n", xtesti, ytesti);
    exit(1);
  }
  return ncid;
}

void lue_koordinaatit1(int ncid) {
  int id;
  //size_t alku[] = {0, yalku1};
  NCFUNK(nc_inq_varid, ncid, "lat", &id);
  NCFUNK(nc_get_var, ncid, id, lat);
  NCFUNK(nc_inq_varid, ncid, "lon", &id);
  NCFUNK(nc_get_var, ncid, id, lon);
}

void lue_muuttuja0(int ncid, int* i_alku) {
  int id;
  NCFUNK(nc_inq_varid, ncid, "kFmiIceConcentration", &id);
  size_t alku[3] = { [0] = 0, [1] = yalku0-1 };
  for(int j=0; j<ypit0; j++) {
    alku[2] = i_alku[j];
    alku[1]++;
    NCFUNK(nc_get_vara, ncid, id, alku, countpt0, var+j*xpit0);
  }
}

#define PINTAALA(lat1, lat2, lon1, lon2) (((lon2)-(lon1))*R2*(sinf(lat2)-sinf(lat1))*1e-6)
#define RAD(a) ((a)*0.017453293)

void laske_pintaalat(int* i_alku) {
#ifdef TALLENNA_PINTAALAT
  FILE *f = fopen("hilan_pintaalat.txt", "w");
#endif
  for(int j=0; j<ypit0-1; j++)
    for(int i=0; i<xpit0-1; i++) {
      float lat1=lat0[j], lat2=lat0[j+1], lon1=lon[i_alku[j]+i], lon2=lon[i_alku[j]+i+1];
      alat[j*xpit0+i] = PINTAALA(RAD(lat1), RAD(lat2), RAD(lon1), RAD(lon2));
#ifdef TALLENNA_PINTAALAT 
      fprintf(f, "%.5lf\t%i\t%i\t%.3f\t%.3f\t%.3f\t%.3f\n",
	      alat[j*xpit0+i], j, i, lat0[j], lat0[j+1], lon[i_alku[j]+i], lon[i_alku[j]+i+1]);
#endif
    }
#ifdef TALLENNA_PINTAALAT
  fclose(f);
#endif
}

#define IND j*xpit0+i
double maarita_laajuus() {
  double pa = 0;
  for(int j=0; j<ypit0-1; j++)
    for(int i=0; i<xpit0-1; i++)
      pa += (var[IND]>=KONSRAJA) * (var[IND]<1000) * alat[IND]; //1000 poistaa täyttöarvon
  return pa;
}
#undef IND
