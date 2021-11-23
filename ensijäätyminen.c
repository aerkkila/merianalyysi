#include <stdio.h>
#include <stdlib.h>
#include <netcdf.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

const char* lahdekansio = "/scratch/project_2002540/siiriasi/smartsea_data";
const char* nimialku = "NORDIC-GOB_1d";
const char* nimiloppu = "grid_T.nc";

#define NCFUNK(funk, ...) {if((ncpalaute = funk(__VA_ARGS__)))	\
      printf("Virhe: %s\n", nc_strerror(ncpalaute));}

//const char* const ajot[] = {"A001", "B001", "D001"};
//const char* const ajot[] = {"A002", "B002", "D002", "A005", "B005", "D005"};
#ifndef KONSRAJA
#define KONSRAJA 0.1
#endif
#define PIENIN_ARVO -92
#define SUURIN_ARVO 120

int main(int argc, char** argv) {
  
  int ncid, ncpalaute, id;
  size_t xpit, ypit, xy;
  char* apuc = malloc(1000);
  /*koon lukeminen*/
  sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s",
	  lahdekansio, "A001", nimialku, 1975, 1975, nimiloppu);
  NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "x", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xpit);
  NCFUNK(nc_inq_dimid, ncid, "y", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ypit);
  xy = xpit*ypit;
  printf("xpit = %i, ypit = %i, xy = %i\n", (int)xpit, (int)ypit, (int)xy);

  /*peittävyyksien lukeminen kerrallaan yhdeltä vuodelta*/
  float* peitt = malloc(xy*366*sizeof(float));
  int16_t* ensijaa = malloc(xy*2);
  int ajoja = argc-1;
  int16_t vuosi0, vuosi1;
  for(int aind=1; aind<argc; aind++) {
    if(argv[aind][strlen(argv[aind])-1] == '1') {
      vuosi0 = 1976;
      vuosi1 = 2006;
    } else {
      vuosi0 = 2007;
      vuosi1 = 2100;
    }
    sprintf(apuc, "ensijäätyminen1_%s.bin", argv[aind]);
    FILE *f = fopen(apuc, "w");
    if(!f) {
      fprintf(stderr, "Ei avattu ulostuloa\n");
      exit(1);
    }
    int16_t tmp_ensi[] = {xpit, ypit, vuosi0, vuosi1};
    fwrite(tmp_ensi, 2, 4, f);
    int v = vuosi0-1;
    while(1) {
      sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s", lahdekansio, argv[aind], nimialku, v, v, nimiloppu);
      printf("\rVuosi %i / %i; ajo %i / %i   ", v-vuosi0+1, vuosi1-vuosi0, aind+1, ajoja);
      //fflush(stdout);
      NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
      NCFUNK(nc_inq_varid, ncid, "soicecov", &id);
      NCFUNK(nc_get_var, ncid, id, peitt);
      NCFUNK(nc_close, ncid);
#define EHTO(taul,ind) (taul[ind] < 2 && taul[ind] >= KONSRAJA)
      int ind = 0;
      if(v != vuosi0-1) {
	for(int16_t paiva=0; paiva<SUURIN_ARVO; paiva++)
	  for(int ruutu=0; ruutu<xy; ruutu++, ind++)
	    if(EHTO(peitt,ind) && ensijaa[ruutu] == SUURIN_ARVO)
	      ensijaa[ruutu] = paiva;
	fwrite(ensijaa, xy, 2, f);
      }
      if(++v == vuosi1) //viimeisestä talvesta ei mennä saman vuoden loppuun
	break;
      for(int i=0; i<xy; i++)
	ensijaa[i] = SUURIN_ARVO;
      const int raja = 365+!(v%4);
      ind = (raja+PIENIN_ARVO)*xy;
      for(int16_t paiva=PIENIN_ARVO; paiva<0; paiva++)
	for(int ruutu=0; ruutu<xy; ruutu++, ind++)
	  if(EHTO(peitt,ind) && ensijaa[ruutu] == SUURIN_ARVO)
	    ensijaa[ruutu] = paiva;
    }
#undef EHTO
    fclose(f);
  }
  putchar('\n');

  free(apuc);
  free(peitt);
  free(ensijaa);
  return 0;
}
