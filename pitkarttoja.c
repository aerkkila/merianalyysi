#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*Tekee kartan tietyistä pituuden prosenttiosuuksista,
  kun pituuskartat on jo laskettu ohjelmilla pktied.c (simulaatio) ja pitkart_kartoista.c (jääkartat)*/

inline void laskentalajittele(short* a, int pit, short* ulos);
char apuc[100];
const char* const kirjaimet = "ABDK";
#define N_ULOS 3

#define _MERKKIJONO(jotain) #jotain
#define MERKKIJONO(jotain) _MERKKIJONO(jotain)
#ifndef AJONRO
#define AJONRO 1
#endif

int main() {
  char ulosnimet[N_ULOS][18];
  int i=0;
  strcpy(ulosnimet[i++], "pituus10_X00" MERKKIJONO(AJONRO) ".bin");
  strcpy(ulosnimet[i++], "pituus50_X00" MERKKIJONO(AJONRO) ".bin");
  strcpy(ulosnimet[i++], "pituus90_X00" MERKKIJONO(AJONRO) ".bin");
  int aind=0;
 SILMUKKA:
  sprintf(apuc, "pituudet_%c00%i.bin", kirjaimet[aind], AJONRO);
  FILE* f = fopen(apuc, "rb");
  if(!f) {
    fprintf(stderr, "Ei avattu tiedostoa\n");
    return 1;
  }
  int16_t otsake[4];
  if(fread(otsake, 2, 4, f) != 4)
    exit(1);
  int xy = otsake[0]*otsake[1];
  int vuosia = otsake[3]-otsake[2];
  short vuodet[vuosia];
  short lvuodet[vuosia];
  int kohdat[] = {(int)round((vuosia+1)*0.1)-1, (int)round((vuosia+1)*0.5)-1, (int)round((vuosia+1)*0.9)-1};

  /*kuvien alustamiset*/
  FILE* kuvat[3];
  for(int i=0; i<N_ULOS; i++) {
    ulosnimet[i][strlen("pituusXX_")] = kirjaimet[aind];
    kuvat[i] = fopen(ulosnimet[i], "wb");
    fwrite(otsake, 2, 4, kuvat[i]);
  }

  for(int ruutu=0; ruutu<xy; ruutu++) {
    fseek(f, 8+ruutu*2, SEEK_SET);
    for(int v=0; v<vuosia; v++) {
      if(fread(vuodet+v, 1, 2, f) != 2)
	printf("Virhe vuoden %i lukemisessa\n", v);
      fseek(f, (xy-1)*2, SEEK_CUR); //yksi luettiin, joten hilan pituudesta vähennetään yksi
    }
    laskentalajittele(vuodet, vuosia, lvuodet);
    for(int i=0; i<N_ULOS; i++)
      fwrite(lvuodet+kohdat[i], 2, 1, kuvat[i]); //olisiko parempi laittaa taulukkoon ja kirjoittaa tiedosto kerralla?
  }
  for(int i=0; i<N_ULOS; i++)
    fclose(kuvat[i]);
  fclose(f);
  if(kirjaimet[++aind])
    goto SILMUKKA;
  return 0;
}

int pitdet[367] = {0};
inline void __attribute__((always_inline)) laskentalajittele(short* a, int pit, short* ulos) {
  for(int i=0; i<pit; i++) {
#ifdef DEBUG
    if(i > 350 || i < 0)
      asm("int $3");
#endif
    pitdet[a[i]]++;
  }
  int uind = 0;
  for(int i=0; uind<pit; i++) //lopettaa kun kaikki on löytynyt, mikä on ennen kuin i==imax
    for(int m=0; m<pitdet[i]; m++)
      ulos[uind++] = i;
  memset(pitdet, 0, 367*sizeof(int));
}
