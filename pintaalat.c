#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>
#include <math.h>

const char* lahdekansio = "/mnt/smartsea_data";
const char* nimialku = "NORDIC-GOB_1d";
const char* nimiloppu = "grid_T.nc";
char* apuc;

const double r2        = 40592558970441; //(6371229 m)^2;
const float latraja  = 60.2;
#ifndef KONSRAJA
#define KONSRAJA 0.1
#endif
#define NCVIRHE printf("Virhe: %s\n", nc_strerror(ncpalaute))
#define NCFUNK(funktio, ...) do {		\
    if((ncpalaute = funktio(__VA_ARGS__)))	\
      NCVIRHE;					\
  } while(0)
int ncpalaute;

int main(int argc, char** argv) {
  int ncid, id, vuosi0, vuosi1, vuosia=-1;
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
  size_t xpit, ypit;
  apuc = malloc(500);
  /*koon lukeminen*/
  sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	  lahdekansio, "A001", nimialku, 1975, 1975, nimiloppu);
  NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "x", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xpit);
  NCFUNK(nc_inq_dimid, ncid, "y", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ypit);
  size_t xy=xpit*ypit;
  const size_t countpt[] = {1,ypit,xpit};
  size_t alku[3] = {0};

  /*nämä ovat liian suuria mahtuakseen pinomuistiin*/
  float *lat, *lon, *kons;
  lat=malloc(xy*sizeof(float));
  lon=malloc(xy*sizeof(float));
  
  /*koordinaattien lukeminen*/
  NCFUNK(nc_inq_varid, ncid, "nav_lat", &id);
  NCFUNK(nc_get_var, ncid, id, lat);
  NCFUNK(nc_inq_varid, ncid, "nav_lon", &id);
  NCFUNK(nc_get_var, ncid, id, lon);
  NCFUNK(nc_close, ncid);

  /*hilaruutujen pinta-alat*/
#define PINTAALA(lat1, lat2, lon1, lon2) (((lon2)-(lon1))*r2*(sinf(lat2)-sinf(lat1))*1.0e-6)
#define RAD(a) ((a)*0.017453293)
  double* alat = malloc(xy*sizeof(double));
  //FILE *f = fopen("hilan_pintaalat.txt", "w");
  for(int j=0; j<ypit-1; j++)
    for(int i=0; i<xpit-1; i++) {
      float lat1=lat[j*xpit+i], lat2=lat[(j+1)*xpit+i], lon1=lon[j*xpit+i], lon2=lon[j*xpit+i+1];
      if(lat1==0 || lat2==0 || lon2==0)
	alat[j*xpit+i] = 0;
      else
	alat[j*xpit+i] = ((latraja<lat[j*xpit+i]) *	\
			  PINTAALA(RAD(lat1), RAD(lat2), RAD(lon1), RAD(lon2)));
      //fprintf(f, "%.5lf\t%i\t%i\t%.3f\t%.3f\t%.3f\t%.3f\n", alat[j*xpit+i], j, i, lat[j*xpit+i], lat[(j+1)*xpit+i], lon[j*xpit+i], lon[j*xpit+i+1]);
    }
  //fclose(f);

  free(lat); free(lon);
  lat=NULL; lon=NULL;
  kons = malloc(xy*sizeof(float));

  for(int ajoind=1; ajoind<argc; ajoind++) {
    if(argv[ajoind][strlen(argv[ajoind])-1] == '1') {
      vuosi0 = 1975;
      vuosi1 = 2006;
    } else {
      vuosi0 = 2006;
      vuosi1 = 2100;
    }
    if(vuosia != -1)
      vuosi1 = vuosi0 + vuosia;

    sprintf(apuc, "laajuudet_%s.txt", argv[ajoind]);
    FILE* f_ulos = fopen(apuc, "w");
    
    for(int vuosi=vuosi0; ; vuosi++) {
      /*luettavan tiedoston polku*/
      sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	      lahdekansio, argv[ajoind], nimialku, vuosi, vuosi, nimiloppu);
      printf("\rvuosi %i / %i, ajo %i / %i   ",
	     vuosi-vuosi0+1, vuosi1-vuosi0, ajoind-1, argc-1);
      //fflush(stdout);
      NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
      NCFUNK(nc_inq_varid, ncid, "soicecov", &id);
      int vuoden_pit = 365 + !(vuosi%4);
      for(int paiva=0; paiva<vuoden_pit; paiva++) {
	double pa=0;
	alku[0] = paiva;
	NCFUNK(nc_get_vara, ncid, id, alku, countpt, kons);
	for(int j=0; j<ypit-1; j++)
	  for(int i=0; i<xpit-1; i++)
	    pa += (kons[j*xpit+i]>=KONSRAJA) * alat[j*xpit+i];
	int paiva1 = (paiva+122) % vuoden_pit - 122;
	if(vuosi+(paiva1<0) >= vuosi1)
	  goto ULOS;
	fprintf(f_ulos, "%6.0lf\t%3i\t%4i\n", round(pa), paiva1, vuosi+(paiva1<0));
      }
      NCFUNK(nc_close, ncid);
    }
  ULOS:
    fclose(f_ulos);
  }
  printf("\n");
  
  free(alat);
  free(kons);
  
  free(apuc);
  return 0;
}
