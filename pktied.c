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
const char* const ajot[] = {"A002", "B002", "D002", "A005", "B005", "D005"};
#ifndef KONSRAJA
#define KONSRAJA 0.1
#endif

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
  int16_t* pit_vuosi = malloc(xy*2);
  int ajoja;
  if(argc > 1)
    sscanf(argv[1], "%i", &ajoja);
  else
    ajoja = sizeof(ajot) / sizeof(*ajot);
  int16_t vuosi0, vuosi1;
  for(int aind=0; aind<ajoja; aind++) {
    if(ajot[aind][strlen(ajot[aind])-1] == '1') {
      vuosi0 = 1976;
      vuosi1 = 2006;
    } else {
      vuosi0 = 2007;
      vuosi1 = 2100;
    }
    sprintf(apuc, "pituudet1_%s.bin", ajot[aind]);
    FILE *f = fopen(apuc, "w");
    if(!f) {
      fprintf(stderr, "Ei avattu ulostuloa\n");
      exit(1);
    }
    int16_t tmp_pit[] = {xpit, ypit, vuosi0, vuosi1};
    fwrite(tmp_pit, 2, 4, f);
    int v = vuosi0-1;
    while(1) {
      sprintf(apuc, "%s/%s/%s_%i0101_%i1231_%s", lahdekansio, ajot[aind], nimialku, v, v, nimiloppu);
      printf("\rVuosi %i / %i; ajo %i / %i   ", v-vuosi0+1, vuosi1-vuosi0, aind+1, ajoja);
      //fflush(stdout);
      NCFUNK(nc_open, apuc, NC_NOWRITE, &ncid);
      NCFUNK(nc_inq_varid, ncid, "soicecov", &id);
      NCFUNK(nc_get_var, ncid, id, peitt);
      NCFUNK(nc_close, ncid);
      /*ensimmäisenä vuonna ohitetaan alun lukeminen
	muina vuosina luetaan alku, asetetaan tulos kaikkiin vuosiin, nollataan, luetaan loppu*/
#define EHTO(taul,ind) (taul[ind] < 2 && taul[ind] >= KONSRAJA)
      if(v != vuosi0-1) {
	for(int ind=0; ind<180*xy;)
	  for(int ruutu=0; ruutu<xy; ruutu++, ind++)
	    pit_vuosi[ruutu] += EHTO(peitt,ind);
	fwrite(pit_vuosi, xy, 2, f);
      }
      if(++v == vuosi1)
	break;
      memset(pit_vuosi, 0, xy*2);
      const int raja = xy*(365+!(v%4));
      for(int ind=244*xy; ind<raja;)
	for(int ruutu=0; ruutu<xy; ruutu++, ind++)
	  pit_vuosi[ruutu] += EHTO(peitt,ind);
    }
#undef EHTO
    fclose(f);
  }
  putchar('\n');

  free(apuc);
  free(peitt);
  free(pit_vuosi);
  return 0;
}
