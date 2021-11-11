#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>
#include <stdint.h>
#include <dirent.h>

const char* restrict lahdekansio = "/home/aerkkila/b/jääkartat";
const char* restrict nckansio = "/home/aerkkila/b/jääkartat/netcdf/";

const float latraja  = 60.2;
#ifndef KONSRAJA
#define KONSRAJA 1.0 //prosentteina
#endif
#define NCVIRHE(arg) do {printf("Netcdf-virhe: %s\n", nc_strerror(arg)); exit(1);} while(0)
#define NCFUNK(fun, ...)			\
  do {						\
    if((ncpalaute = fun(__VA_ARGS__)))		\
      NCVIRHE(ncpalaute);			\
  } while(0)

typedef struct {
  int patka;
  int tilaa;
  int pit;
  char** p;
} lista;
void listalle(lista*, char*);
void poista_lista(lista*);

const int ypit2=3120, xpit2=2640;
const int xpit0=700; //muutettaessa huomioitakoon myös countpt
const size_t countpt0[] = {1, 1, 700};
int ypit0, yalku0=0;
int xpit1, xalku0;
int ncpalaute;
float *lat, *lon, *lat0;
double *var, *alat;
FILE* f_ulos;

DIR* avaa_vuosi(int vuosi, char* polku_ulos);
int pura_seuraava(DIR *d, char* polku, char* osanimi);
void poista_tiedosto(const char* nimi);
int avaa_netcdf(const char* restrict);
void lue_koordinaatit1(int ncid);
void maarita_i_alut(int* i_alku);
void lue_muuttuja0(int ncid, int* i_alku);
void laske_pintaalat(int* i_alku);
double maarita_laajuus();
int maarita_paiva(const char* restrict nimi, int* paiva, int* vuosi);
void nimet_jarjestuksessa(DIR* d, lista* lis);

/*Tarvittavat koot ovat
  xypit2: koko kartan koko
  xypit0: se osa, joka todellisuudessa tarvitaan. Tämä on viimeisenä määritettävä tarkin arvo.*/
int main(int argc, char** argv) {
  char apuc[300];
  int vuosi0=1980, vuosi1=2007;
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

  char kansionimi[80];
  DIR* d = avaa_vuosi(1980, kansionimi);
  strcpy(apuc, kansionimi);
  char tiedostonnimi[120];
  strcpy(tiedostonnimi, nckansio);
  if(pura_seuraava(d, apuc, tiedostonnimi+strlen(tiedostonnimi))) {
    printf("Ei purettu yhtään vuodesta 1980\n");
    exit(1);
  }
  int ncid = avaa_netcdf(tiedostonnimi);
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
  
  NCFUNK(nc_close, ncid); //silmukka on helpompi, kun nämä suljetaan tässä välissä
  closedir(d);
  lista lis = {.patka=20, .tilaa=20, .pit=0, .p=NULL};
  lis.p = malloc(20*sizeof(char*));
  int16_t* pit_vuosi = malloc(xypit0*2); //vino kartta
  int16_t* kartta = calloc(xpit1*ypit0, 2); //oikaistu kartta
  FILE* f_ulos = fopen("pituudet_K001.bin", "wb");
  int16_t tmp_pit[] = {xpit1, ypit0, vuosi0+1, vuosi1}; //korjataan lopussa, jos viimeinen vuosi oli väärin
  fwrite(tmp_pit, 2, 4, f_ulos);
  FILE *fpaivia = fopen("paivia.txt", "w");

  int paiv, vuos, vanha_paiv, vanha_vuos, vuosi, paivia;
  for(vuosi=vuosi0; vuosi<vuosi1; vuosi++) {
    d = avaa_vuosi(vuosi, kansionimi);
    if(!d)
      break;
    nimet_jarjestuksessa(d, &lis);
    closedir(d);
    d=NULL;
    memset(pit_vuosi, 0, xypit0*2);
    for(int i=0; i<lis.pit; i++) {
      if(maarita_paiva(lis.p[i], &paiv, &vuos)) {
	printf("Virheellinen tiedostonnimi: \"%s\"\n", tiedostonnimi);
	exit(1);
      }
      if(vuos != vanha_vuos) {
	vanha_paiv = paiv;
	vanha_vuos = vuos;
	continue;
      }
      paivia = paiv - vanha_paiv;
      vanha_paiv = paiv;
      vanha_vuos = vuos;
      sprintf(apuc, "unzip -u '%s/%s' -d %s/netcdf", kansionimi, lis.p[i], lahdekansio);
      system(apuc);
      strcpy(lis.p[i]+strlen(lis.p[i])-4, ".nc"); // .zip --> .nc
      sprintf(apuc, "%s/%s", nckansio, lis.p[i]);
      ncid = avaa_netcdf(apuc);
      //tarkista_koordinaatit(ncid);
      lue_muuttuja0(ncid, i_alku);
      NCFUNK(nc_close, ncid);
      if(paivia < 0)
	asm("int $3");
      fprintf(fpaivia, "%i\t%i: %i\n", paivia, vuos, paiv);
      for(int xy=0; xy<xypit0; xy++)
	pit_vuosi[xy] += (var[xy]>=KONSRAJA && var[xy]<1000 ) * paivia;
      //poista_tiedosto(lis.p[i]);
    }
#ifdef DEBUG
    for(int xy=0; xy<xypit0; xy++)
      if(pit_vuosi[xy] < 0 || pit_vuosi[xy] > 350)
	asm("int $3");
#endif
    /*kartta täytyy oikaista tulostettaessa*/
    for(int j=0; j<ypit0; j++) {
      size_t vasen = i_alku[j]-xalku0;
      memcpy(kartta+j*xpit1+vasen, pit_vuosi+j*xpit0, xpit0*2);
    }
    fwrite(kartta, xpit1*ypit0, 2, f_ulos);
    for(int i=0; i<lis.pit; i++)
      free(lis.p[i]);
    lis.pit=0;
  }
  fclose(fpaivia);
  if(d)
    closedir(d);
  free(lat); free(lon); free(var); free(alat); free(kartta);
  poista_lista(&lis);
  fseek(f_ulos, 6, SEEK_SET);
  fwrite(&vuosi, 2, 1, f_ulos); //vuosi = vuosi1 tai pienempi, jos loppuivat kesken
  fclose(f_ulos);
  return 0;
}

void poista_lista(lista* lis) {
  for(int i=0; i<lis->pit; i++)
    free(lis->p[i]);
  free(lis->p);
  lis->p=NULL;
  lis->pit=0;
  lis->tilaa=0;
}

void listalle(lista* lis, char* mjono) {
  if(++lis->pit > lis->tilaa)
    lis->p = realloc(lis->p, (lis->tilaa+=lis->patka)*sizeof(char*));
  lis->p[lis->pit-1] = mjono;
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
  sprintf(polku, "%s/%i", lahdekansio, vuosi);
  DIR *d = opendir(polku);
  if(!d) {
    printf("Kansiota \"%s\" ei voitu avata\n", polku);
    return NULL;
  }
  return d;
}

/*lukee nimistä osion yyyymmdd ja kantalukulajittelee sillä perusteella nimet*/
void nimet_jarjestuksessa(DIR* d, lista* lis) {
  struct dirent* e;
  while((e = readdir(d))) {
    if(!strstr(e->d_name, "_icechart.zip"))
      continue;
    listalle(lis, strdup(e->d_name));
  }
  uint32_t* luvut[2];
  char* apu[lis->pit];
  for(int i=0; i<2; i++)
    luvut[i] = malloc(lis->pit*4);
  for(int i=0; i<lis->pit; i++)
    sscanf(lis->p[i], "%8d", luvut[0]+i);
  int lasku[256];
  unsigned siirto = 0;
  for(int j=0; j<4; j++, siirto+=8) {
    memset(lasku, 0, 256*sizeof(int));
    for(int i=0; i<lis->pit; i++)
      lasku[luvut[0][i]>>siirto & 0xff]++;
    for(int i=1; i<256; i++)
      lasku[i] += lasku[i-1];
    for(int i=lis->pit-1; i>=0; i--) {
      int ind = --lasku[luvut[0][i]>>siirto & 0xff];
      luvut[1][ind] = luvut[0][i];
      if(j%2)
	lis->p[ind] = apu[i];
      else
	apu[ind] = lis->p[i];
    }
    uint32_t* tmp = luvut[0];
    luvut[0] = luvut[1];
    luvut[1] = tmp;
  }
  for(int i=0; i<2; i++)
    free(luvut[i]);
}

/*Ei taida kohtuudella onnistua avata nc-tiedostoa, joka on luettu zip-kansiosta RAM-muistiin.
  Täytyy siis ensin purkaa zip-kansio kovalevylle ja sitten lukea tiedosto sieltä
  vaikka sitä kautta lukeminen onkin hitaampaa.*/
int pura_seuraava(DIR *d, char* polku, char* nimiulos) {
  struct dirent* e;
  while((e = readdir(d))) {
    if(!strstr(e->d_name, ".zip"))
      continue;
    char kmnt[500];
    sprintf(kmnt, "unzip -u '%s/%s' -d %s/netcdf", polku, e->d_name, lahdekansio);
    system(kmnt);
    strcpy(nimiulos, e->d_name);
    strcpy(nimiulos+strlen(nimiulos)-4, ".nc"); // *.zip --> *.nc
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
  xalku0 = lukema;
  while(lat0[j] < 63.0)
    i_alku[j++] = lukema;
  while(lat0[j] < 64.68)
    i_alku[j++] = ++lukema;
  while(j < ypit0)
    i_alku[j++] = lukema;
  xpit1 = xpit0 + lukema-xalku0;
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
