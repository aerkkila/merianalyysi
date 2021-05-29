#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "jaagrid.h"
#include "pintaalavakiot.h"

#define KOKOPIT grid.gridpit

int main(int argc, char** argv) {
  char ulakansio[] = "/home/aerkkila/a";
  char uloskansio[] = "pintaalat";
  char siskansio[] = "ncteksti";
  char latlontied[] = "latlon.txt";
  char paksalku[] = "icevolume";
  char konsalku[] = "soicecov";
  char *tiednimi = malloc(200);
  grid_t grid;
  int alkuvuosi, loppuvuosi;

  /*komentorivillä olkoot ajonimet, sanan alussa saa olla muutakin,
    lopussa olkoot alku- ja loppuvuosi*/
  if(argc < 4) {
    fprintf(stderr, "Virhe: Liian vähän argumentteja\n");
    return 1;
  }
  if(!sscanf(argv[argc-1], "%i", &loppuvuosi)) {
    fprintf(stderr, "Ei annettu loppuvuotta\n");
    return 1;
  }
  if(!sscanf(argv[argc-2], "%i", &alkuvuosi)) {
    fprintf(stderr, "Ei annettu alkuvuotta\n");
    return 1;
  }
  if(alkuvuosi > loppuvuosi)
    printf("Varoitus: alkuvuosi = %i, loppuvuosi = %i\n", alkuvuosi, loppuvuosi);
  loppuvuosi++; //olkoon tämä ensimmäinen vuosi, jota ei ole

  if(LATRAJA1 < LATRAJA0)
    printf("Varoitus: Leveyspiirien yläraja on alarajaa pienempi\n");
  if(LONRAJA1 < LONRAJA0)
    printf("Varoitus: Pituuspiirien yläraja on alarajaa pienempi\n");

  sprintf(tiednimi, "%s/%s/%s", ulakansio, siskansio, latlontied);
  grid = lue_grid(tiednimi);

  /*lasketaan ruutujen pinta-alat*/
  maapintaala_t maa;
  maa = maapintaala(grid.lat, grid.lon, KOKOPIT, LATRAJA0, LATRAJA1, LONRAJA0, LONRAJA1);

  /*Luetaan aina yksi tiedosto ja lasketaan jään pinta-alat eri ajanhetkillä*/
  char* jaassa = malloc(maa.pituus); //joka ruudulle arvo 0/1 sen mukaan, onko jäässä
  for(int ajoind=1; ajoind<argc-2; ajoind++) {
    char* ajo = argv[ajoind]+strlen(argv[ajoind])-4;
    for(int vuosi=alkuvuosi; vuosi<loppuvuosi; vuosi++) {
      printf("\rvuosi %i / %i, ajo %i / %i",
	     vuosi-alkuvuosi+1, loppuvuosi-alkuvuosi, ajoind, argc-3);
      fflush(stdout);
      /*luetaan tiedostot*/
      sprintf(tiednimi, "%s/%s/%s_%s_%i.txt",
	      ulakansio, siskansio, paksalku, ajo, vuosi);
      float* paks = lue_jaa(tiednimi, grid.gridpit, maa.indeksit, maa.pituus);
      sprintf(tiednimi, "%s/%s/%s_%s_%i.txt",
	      ulakansio, siskansio, konsalku, ajo, vuosi);
      float* kons = lue_jaa(tiednimi, grid.gridpit, maa.indeksit, maa.pituus);
  
      /*tallennetaan joka ruudusta tieto, onko siinä jonkin kategorian jäätä
	sen jälkeen lasketaan kyseisten ruutujen pinta-alat yhteen
	toistetaan tämä joka aika-askelella*/
      float* ala = calloc(AIKAASK, sizeof(float));
      float* apup = paks;
      float* apuk = kons;
      for(int ask=0; ask<AIKAASK; ask++) {
	for(int i=0; i<maa.pituus; i++)
	  jaassa[i] = 0;
	
	for(int kat=0; kat<KATEG; kat++)
	  for(int i=0; i<maa.pituus; i++) {
	    if(*apup >= PAKSRAJA && *apuk >= KONSRAJA)
	      jaassa[i] = 1;
	    apuk++;
	    apup++;
	  }

	for(int i=0; i<maa.pituus; i++)
	  if(jaassa[i])
	    ala[ask] += maa.alat[i];
      }
      free(paks);
      free(kons);
  
      /*tallennetaan tämä yhden vuoden tieto*/
      FILE *f;
      sprintf(tiednimi, "%s/%s_%li_%li/pa_%s_%i.bin",	\
	      ulakansio, uloskansio, lround(KONSRAJA*100), lround(PAKSRAJA*100), ajo, vuosi);
      f = fopen(tiednimi, "w");
      fwrite(ala, AIKAASK, sizeof(float), f);
      fclose(f);
      free(ala);
    }
  }
  printf("\n");
  free(jaassa);
  vapauta_grid(grid);
  free(maa.alat);
  free(maa.indeksit);
  free(tiednimi);
  return 0;
}
