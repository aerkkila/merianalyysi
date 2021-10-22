#include <stdio.h>
#include <stdlib.h>
#include <string.h>

inline void laskentalajittele(short* a, int pit, short* ulos);
char apuc[100];
const char* const kirjaimet = "ABD";

int main() {
  char* ulosnimet[3];
  ulosnimet[0] = strdup("pituus10_X001.bin");
  ulosnimet[1] = strdup("pituus50_X001.bin");
  ulosnimet[2] = strdup("pituus90_X001.bin");
  int aind=0;
 SILMUKKA:
  sprintf(apuc, "pituudet_%c001.bin", kirjaimet[aind]);
  FILE* f = fopen(apuc, "rb");
  if(!f) {
    fprintf(stderr, "Ei avattu tiedostoa\n");
    return 1;
  }
  int16_t otsake[4];
  fread(otsake, 2, 4, f);
  int xy = otsake[0]*otsake[1];
  int vuosia = otsake[3]-otsake[2];
  short vuodet[vuosia];
  short lvuodet[vuosia];
  int kohdat[] = {vuosia/10-1, vuosia/2-1, vuosia/10*9-1};

  /*kuvien alustamiset*/
  FILE* kuvat[3];
  for(int i=0; i<3; i++) {
    ulosnimet[i][strlen("pituusXX_")] = kirjaimet[aind];
    kuvat[i] = fopen(ulosnimet[i], "wb");
    fwrite(otsake, 2, 4, kuvat[i]);
  }

  for(int ruutu=0; ruutu<xy; ruutu++) {
    fseek(f, 8+ruutu*2, SEEK_SET);
    for(int v=0; v<vuosia; v++) {
      fread(vuodet+v, 1, 2, f);
      fseek(f, (xy-1)*2, SEEK_CUR); //yksi luettiin, joten hilan pituudesta vähennetään yksi
    }
    laskentalajittele(vuodet, vuosia, lvuodet);
    for(int i=0; i<3; i++)
      fwrite(lvuodet+kohdat[i], 2, 1, kuvat[i]); //olisiko parempi laittaa taulukkoon ja kirjoittaa tiedosto kerralla?
  }
  for(int i=0; i<3; i++)
    fclose(kuvat[i]);
  fclose(f);
  if(kirjaimet[++aind])
    goto SILMUKKA;
  for(int i=0; i<3; i++)
    free(ulosnimet[i]);
  return 0;
}

int pitdet[367] = {0};
inline void __attribute__((always_inline)) laskentalajittele(short* a, int pit, short* ulos) {
  for(int i=0; i<pit; i++)
    pitdet[a[i]]++;
  int uind = 0;
  for(int i=0; i<367; i++) {
    for(int m=0; m<pitdet[i]; m++)
      ulos[uind++] = i;
    pitdet[i] = 0;
  }
}
