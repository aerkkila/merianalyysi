#include <netcdf.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* nctiedosto = "/scratch/project_2002540/siiriasi/smartsea_data/D005/NORDIC-GOB_1d_20950101_20951231_grid_T.nc";
const char* ncmuuttuja = "SST";
const int luettava_paiva = 212; //31.7.
char* paikat[] = {"Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn"};
const int lpit = 500;

#define NCFUNK(funk, ...) {if((ncpalaute = funk(__VA_ARGS__)))	\
      printf("Virhe: %s\n", nc_strerror(ncpalaute));}

int main() {
  /*luetaan paikkojen indeksit koordinaatistossa tiedostosta koordinatit.txt*/
  FILE *f = fopen("koordinaatit.txt", "r");
  char* rivi = malloc(lpit);
  const char haku[] = "indeksi = ";
  int indeksit[6];
  for(int i=0; i<6; i++) {
    fscanf(f, "%s", rivi);
    rivi[strlen(rivi)-1] = 0;
    if(strcmp(rivi, paikat[i]))
      printf("Luettiin: %s, piti olla %s\n", rivi, paikat[i]);
    fscanf(f, "%*[^\n]\n");
    fgets(rivi, lpit, f);
    char* kohta = strstr(rivi, haku) + strlen(haku);
    if(sscanf(kohta, "%i", indeksit+i) != 1)
      printf("Ei luettu indeksiä (%s: %s)\n", paikat[i], kohta);
  }
  fclose(f);
  free(rivi);
  
  /*koon lukeminen*/
  int ncid, id, ncpalaute;
  size_t xpit, ypit;
  NCFUNK(nc_open, nctiedosto, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_dimid, ncid, "x", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &xpit);
  NCFUNK(nc_inq_dimid, ncid, "y", &id);
  NCFUNK(nc_inq_dimlen, ncid, id, &ypit);
  const size_t xy=xpit*ypit;

  const size_t alku[] = {luettava_paiva, 0, 0};
  const size_t lasku[] = {1, ypit, xpit};
  float* luenta = malloc(xy*sizeof(float));
  NCFUNK(nc_open, nctiedosto, NC_NOWRITE, &ncid);
  NCFUNK(nc_inq_varid, ncid, ncmuuttuja, &id);
  NCFUNK(nc_get_vara, ncid, id, alku, lasku, luenta);
  NCFUNK(nc_close, ncid);

  char* kartta = malloc(xy);
  for(size_t i=0; i<xy; i++)
    kartta[i] = luenta[i] > 0 && luenta[i] < 100; //merkitään merialue
  for(int i=0; i<6; i++)
    kartta[indeksit[i]] = i+2; //merkitään paikat

  int32_t koko[] = {(int32_t)xpit, (int32_t)ypit};
  //xint = (int32_t)xpit;
  //yint = (int32_t)ypit;
  f = fopen("kartta.bin", "w");
  fwrite(koko, 4, 2, f);
  fwrite(kartta, xy, 1, f);
  free(kartta);
  fclose(f);

  free(luenta);
  return 0;
}
