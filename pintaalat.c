#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <string.h>
#include <math.h>

const char* lahdekansio = "/scratch/project_2002540/siiriasi/smartsea_data";
const char* nimialku = "NORDIC-GOB_1d";
const char* nimiloppu = "grid_T.nc";
char* apuc;

const double r        = 6371229;
const float latraja  = 60.2;
const float konsraja = 0.15;
#define NCVIRHE printf("Virhe: %s\n", nc_strerror(ncpalaute))

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
  size_t xpit, ypit;
  apuc = malloc(500);
  /*koon lukeminen*/
  sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	  lahdekansio, "A001", nimialku, 1975, 1975, nimiloppu);
  if((ncpalaute = nc_open(apuc, NC_NOWRITE, &ncid)))
    NCVIRHE;
  if((ncpalaute = nc_inq_dimid(ncid, "x", &id)))
    NCVIRHE;
  if((ncpalaute = nc_inq_dimlen(ncid, id, &xpit)))
    NCVIRHE;
  if((ncpalaute = nc_inq_dimid(ncid, "y", &id)))
    NCVIRHE;
  if((ncpalaute = nc_inq_dimlen(ncid, id, &ypit)))
    NCVIRHE;
  size_t xy=xpit*ypit;

  /*nämä ovat liian suuria mahtuakseen pinomuistiin*/
  float *lat, *lon, *kons;
  lat=malloc(xy*sizeof(float));
  lon=malloc(xy*sizeof(float));
  
  /*koordinaattien lukeminen*/
  if((ncpalaute = nc_inq_varid(ncid, "nav_lat", &id)))
    NCVIRHE;
  if((ncpalaute = nc_get_var(ncid, id, lat)))
    NCVIRHE;
  if((ncpalaute = nc_inq_varid(ncid, "nav_lon", &id)))
    NCVIRHE;
  if((ncpalaute = nc_get_var(ncid, id, lon)))
    NCVIRHE;
  if((ncpalaute = nc_close(ncid)))
    NCVIRHE;

  /*hilaruutujen pinta-alat*/
#define PINTAALA(lat1, lat2, lon1, lon2) (((lon2)-(lon1))*r*r*(sinf(lat2)-sinf(lat1))*1.0e-6)
#define RAD(a) ((a)*0.017453293)
  double* alat = malloc(xy*sizeof(double));
  FILE *f = fopen("hilan_pintaalat.txt", "w");
  for(int j=0; j<ypit-1; j++)
    for(int i=0; i<xpit-1; i++) {
      float lat1=lat[j*xpit+i], lat2=lat[(j+1)*xpit+i], lon1=lon[j*xpit+i], lon2=lon[j*xpit+i+1];
      if(lat1==0 || lat2==0 || lon2==0)
	alat[j*xpit+i] = 0;
      else
	alat[j*xpit+i] = ((latraja<lat[j*xpit+i]) *	\
			  PINTAALA(RAD(lat1), RAD(lat2), RAD(lon1), RAD(lon2)));
      fprintf(f, "%.5lf\t%i\t%i\t%.3f\t%.3f\t%.3f\t%.3f\n", alat[j*xpit+i], j, i, lat[j*xpit+i], lat[(j+1)*xpit+i], lon[j*xpit+i], lon[j*xpit+i+1]);
    }
  fclose(f);

  free(lat); free(lon);
  lat=NULL; lon=NULL;
  kons = malloc(366*xy*sizeof(float));
#ifdef PAKSRAJA
  float  *paks;
  paks = malloc(366*xy*sizeof(float));
#endif

  for(int ajoind=1; ajoind<argc; ajoind++) {
    if(argv[ajoind][strlen(argv[ajoind])-1] == '1') {
      alkuvuosi = 1975;
      loppuvuosi = 2006;
    } else {
      alkuvuosi = 2006;
      loppuvuosi = 2100;
    }
    if(vuosia != -1)
      loppuvuosi = alkuvuosi+vuosia;

    sprintf(apuc, "pintaalat_%s.txt", argv[ajoind]);
    FILE* f_ulos = fopen(apuc, "w");
    
    for(int vuosi=alkuvuosi; vuosi<loppuvuosi; vuosi++) {
      /*luettavan tiedoston polku*/
      sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	      lahdekansio, argv[ajoind], nimialku, vuosi, vuosi, nimiloppu);
      printf("\rvuosi %i / %i, ajo %i / %i   ",
	     vuosi-alkuvuosi+1, loppuvuosi-alkuvuosi, ajoind, argc-1);
      fflush(stdout);
      if((ncpalaute = nc_open(apuc, NC_NOWRITE, &ncid)))
	NCVIRHE;
      if((ncpalaute = nc_inq_varid(ncid, "soicecov", &id)))
	NCVIRHE;
      if((ncpalaute = nc_get_var(ncid, id, kons)))
	NCVIRHE;
#ifdef PAKSRAJA
      if((ncpalaute = nc_inq_varid(ncid, "icevolume", &id)))
	NCVIRHE;
      if((ncpalaute = nc_get_var(ncid, id, paks)))
	NCVIRHE;
#endif
      for(int paiva=0; paiva<=365; paiva++) {
	double pa=0;
	for(int j=0; j<ypit-1; j++)
	  for(int i=0; i<xpit-1; i++)
	    pa += (kons[paiva*xy+j*xpit+i]>=konsraja) * alat[j*xpit+i];
	fprintf(f_ulos, "%6.0lf\t%3i\t%4i\n", round(pa), paiva+1, vuosi);
      }
      if(vuosi % 4) { //ei-karkausvuosina 366. päivälle nan
	fseek(f_ulos, -16, SEEK_CUR);
	fprintf(f_ulos, "%6.0lf\t%3i\t%4i\n", NAN, 366, vuosi);
      }
      
      if((ncpalaute = nc_close(ncid)))
	NCVIRHE;
    }
    fclose(f_ulos);
  }
  printf("\n");
  
  free(alat);
  free(kons);
#ifdef PAKSRAJA
  free(paks);
#endif
  
  free(apuc);
  return 0;
}
