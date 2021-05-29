#include <stdlib.h>
#include <stdio.h>
#include "jaagrid.h"
#include "pintaalavakiot.h"
#include <unistd.h>

#define KOKOPIT tulos.gridpit

grid_t lue_grid(char* tiedosto) {
  FILE *f = fopen(tiedosto, "r");
  if(!f) {
    fprintf(stderr, "Virhe: ei tiedostoa \"%s\"\n", tiedosto);
    return (grid_t){NULL, NULL, 0};
  }
  grid_t tulos;

  /*lasketaan gridin kokonaispituus
   myös viimeisen arvon on päätyttävä pilkkuun*/
  char c;
  KOKOPIT = 0;
  while( (( c=fgetc(f) )) != ';')
    if(c == ',')
      KOKOPIT++;

  rewind(f);
  
  int i;
  tulos.lat = malloc(KOKOPIT*sizeof(float));
  tulos.lon = malloc(KOKOPIT*sizeof(float));
  
  /*luetaan leveys- ja pituuspiirit*/
  for (i=0; i<KOKOPIT; i++)
    if( !(fscanf(f, "%f,", tulos.lat+i)) )
      fprintf(stderr, "Virhe: pituuspiirin luenta ei onnistunut\n");
  
  while(fgetc(f) != ';');
  for(i=0; i<KOKOPIT; i++)
    if( !(fscanf(f, "%f,", tulos.lon+i)) )
      fprintf(stderr, "Virhe: leveyspiirin luenta ei onnistunut\n");

  fclose(f);
  return tulos;
}

float* lue_jaa(char* tiedosto, int gridpit, int* indeksit, int lukupit) {
  /*luetaan jääkategorioitten konsentraatiot tai muu tieto halutuissa datapisteissä,
    joitten indeksit on annettu muuttujassa "indeksit", jonka pituus on "lukupit"*/
  char c;
  float *jaa = malloc(KATEG*AIKAASK*lukupit*sizeof(float));
  if(!jaa)
    fprintf(stderr, "Virhe: jään luennan alustaminen ei onnistunut\n");
  FILE *f = fopen(tiedosto, "r");
  if(!f)
    fprintf(stderr, "Virhe: ei tiedostoa \"%s\"\n", tiedosto);

  while(fgetc(f) != '=');

  int gridind=0; //monennessako koordinaattiruudussa ollaan
  int lukuind=0; //tämä iteroi "indeksit"-muuttujan
  float* apujaa=jaa;
  int askelia=0;
  while(1) {
    if(gridind==indeksit[lukuind]) { //ollaan halutussa pisteessä
      if( !(fscanf(f, "%f", apujaa++)) )
	fprintf(stderr, "Virhe: halutussa paikassa ei voitu lukea jäätä\n");
      else
	lukuind++;
    }
    if( (( c=fgetc(f) )) == ',')
      gridind++;
    else if (c == ';')
      break;
    if(gridind == gridpit) { //yhden aika-askelen tiedot luettu
      gridind=0;
      lukuind=0;
      askelia++;
    }
  }
  fclose(f);
  return jaa;
}

void vapauta_grid(grid_t jaa) {
  free(jaa.lat);
  free(jaa.lon);
}
