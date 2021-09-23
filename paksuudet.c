#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <netcdf.h>
#include <locale.h>

const char* lahdekansio = "/scratch/project_2002540/siiriasi/smartsea_data";
const char* nimialku = "NORDIC-GOB_1d";
const char* nimiloppu = "grid_T.nc";
char apuc[500];
#define PAIKKOJA 6
char* paikat[] = {"Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn"};
char* paikat_en[] = {"Kemi", "Kalajoki", "Korsholm", "Nordmaling", "Rauma", "Söderhamn"};
float paikatlat[] = {65.6322, 64.2250, 63.1579, 63.4498, 61.1050, 61.3897};
float paikatlon[] = {24.4908, 23.6921, 21.2553, 19.6341, 21.4220, 17.1539};

const double sade = 6360963.529; //maan säde 63:nnella leveyspiirillä
#define RAD 0.017453293 //radiaanit = asteet*RAD
/*kulma = asin(sqrt(MATKA))/2, tässä siis lasketaan vain se osa jota tarvitaan vertailuun*/
#define MATKA(lat1, lon1, lat2, lon2) (pow(sinf((lat2-lat1)/2),2) + cosf(lat1)*cosf(lat2)*pow(sinf((lon2-lon1)/2),2))

#define NCFUNK(funk, ...) {if((ncpalaute = funk(__VA_ARGS__)))	\
      printf("Virhe: %s\n", nc_strerror(ncpalaute));}

int main(int argc, char** argv) {
  int ncid, ncpalaute, id, alkuvuosi, loppuvuosi, vuosia=-1;
  /*onko annettu jokin toinen vuosien määrä*/
  for(int i=1; i<argc; i++)
    if(sscanf(argv[i], "--vuosia=%i", &vuosia)==1) {
      argc--;
      for(;i<argc;i++)
	argv[i]=argv[i+1];
      break;
    }
  if(argc < 2) {
    printf("Käyttö: ./ohjelma A001 A002 ...\n");
    return 1;
  }
  /*koon lukeminen*/
  size_t xpit, ypit;
  sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	  lahdekansio, "A001", nimialku, 1975, 1975, nimiloppu);
  NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "x", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xpit);
  NCFUNK(nc_inq_dimid, ncid, "y", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ypit);
  size_t xy=xpit*ypit;

  /*nämä eivät välttämättä mahtuisi pinomuistiin*/
  float *lat, *lon;
  lat=malloc(xy*sizeof(float));
  lon=malloc(xy*sizeof(float));
  
  /*koordinaattien lukeminen*/
  NCFUNK(nc_inq_varid, ncid, "nav_lat", &id);
  NCFUNK(nc_get_var, ncid, id, lat);
  NCFUNK(nc_inq_varid, ncid, "nav_lon", &id);
  NCFUNK(nc_get_var, ncid, id, lon);
  NCFUNK(nc_close, ncid);

  /*haetaan paikkoja lähimpänä olevat sijainnit*/
  setlocale(LC_ALL, "fi_FI.utf8");
  FILE *f = fopen("koordinaatit.txt", "w");
  int sijainnit[PAIKKOJA];
  for(int p=0; p<PAIKKOJA; p++) {
    int pienin_ind = 0;
    double pienin_matka = INFINITY;
    float lat1=paikatlat[p]*RAD;
    float lon1=paikatlon[p]*RAD;
    for(int i=0; i<xy; i++) {
      double matka = MATKA(lat1, lon1, lat[i]*RAD, lon[i]*RAD);
      if(matka < pienin_matka) {
	pienin_matka = matka;
	pienin_ind = i;
      }
    }
    fprintf(f, ("%s:\t Haettiin %.4f°N\t %.4f°E\t Saatiin:\t %.4f°N\t %.4f°E\t\n" \
		"matka = %.0lf m\t indeksi = %i\n"),			\
	    paikat[p], paikatlat[p], paikatlon[p], lat[pienin_ind], lon[pienin_ind], \
	    asin(sqrt(pienin_matka))/2*sade, pienin_ind);
    sijainnit[p] = pienin_ind;
  }
  /*taulukko koordinaateista suomeksi ja englanniksi*/
  f = freopen("koordinaatit_taul.txt", "w", f);
  setlocale(LC_ALL, "fi_FI.utf8");
  fprintf(f, "paikka & koordinaatit\\\\\n\\hline\n");
  for(int i=0; i<PAIKKOJA; i++)
    fprintf(f, "%s & %.4f °N %.4f °E \\\\\n", paikat[i], lat[sijainnit[i]], lon[sijainnit[i]]);
  /*englanniksi*/
  f = freopen("koordinaatit_taul_en.txt", "w", f);
  setlocale(LC_ALL, "en_US.utf8");
  fprintf(f, "place & coordinates\\\\\n\\hline\n");
  for(int i=0; i<PAIKKOJA; i++)
    fprintf(f, "%s & %.4f°N %.4f°E \\\\\n", paikat_en[i], lat[sijainnit[i]], lon[sijainnit[i]]);
  fclose(f);
  free(lat);
  free(lon);
  lat=NULL; lon=NULL;

  /*paksuuksien *lukeminen*/
  float *paksluenta = malloc(xy*366*sizeof(float));
  float *paks = malloc(PAIKKOJA*100*366*sizeof(float));
#define PAKS(paikka, vuosi, paiva) (paks[(paikka)*366*(loppuvuosi-alkuvuosi)+(vuosi)*366+paiva])
  for(int aind=1; aind<argc; aind++) {
    if(argv[aind][strlen(argv[aind])-1] == '1') {
      alkuvuosi = 1975;
      loppuvuosi = 2006;
    } else {
      alkuvuosi = 2006;
      loppuvuosi = 2100;
    }
    if(vuosia != -1)
      loppuvuosi = alkuvuosi+vuosia;
    
    for(int v=alkuvuosi; v<loppuvuosi; v++) {
      sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",	\
	      lahdekansio, argv[aind], nimialku, v, v, nimiloppu);
      printf("\rVuosi %i / %i; ajo %i / %i ", v-alkuvuosi+1, loppuvuosi-alkuvuosi, aind, argc-1);
      fflush(stdout);
      NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
      NCFUNK(nc_inq_varid, ncid, "icevolume", &id);
      NCFUNK(nc_get_var, ncid, id, paksluenta);
      NCFUNK(nc_close, ncid);
      for(int p=0; p<PAIKKOJA; p++)
	for(int paiva=0; paiva<366; paiva++)
	  PAKS(p, v-alkuvuosi, paiva) = paksluenta[paiva*xy+sijainnit[p]];
    }
    int i=0;
    const char *restrict muoto = "%5.1f\t%3i\t%4i\n";
    for(int p=0; p<PAIKKOJA; p++) {
      sprintf(apuc, "paksuudet_%s_%s.txt", paikat[p], argv[aind]);
      FILE *f = fopen(apuc, "w");
      for(int vuosi=alkuvuosi; vuosi<loppuvuosi; vuosi++) {
	for(int paiva=1; paiva<=366; paiva++, i++)
	  fprintf(f, muoto, paks[i]*100, paiva, vuosi); //muutettaessa muutettakoon myös tuleva fseek
	if(vuosi % 4) {
	  fseek(f, -15, SEEK_CUR);
	  fprintf(f, muoto, NAN, 366, vuosi);
	}
      }
      fclose(f);
    }
  }
  putchar('\n');	

  free(paksluenta);
  free(paks);
  return 0;
}
