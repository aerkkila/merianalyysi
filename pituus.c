#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

/*vaihtaa a:ssa b:n tilalle c:n*/
char* korvaa_strstr(char* a, const char* b, const char* c) {
  char* kohta0 = strstr(a, b);
  if(!kohta0)
    return NULL;
  char* kohta1 = kohta0 + strlen(b);
  char loppu[strlen(kohta1)+1];
  strcpy(loppu, kohta1);
  strcpy(kohta0, c);
  strcat(a, loppu);
  return a;
}

int main() {
  const char* kansio = "/home/aerkkila/b/tiedokset";
  const float konsraja = 0.15;
  char cnimi[500];
  int ind;
  
  const int pit = 36600; //100 vuotta * 366 päivä / vuotta
  short* vuosi = malloc(pit*sizeof(short));
  short* paiva = malloc(pit*sizeof(short));
  float* kons = malloc(pit*sizeof(float));
  
  DIR *d = opendir(kansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", kansio);
    return 1;
  }
  struct dirent *e;

  while((e = readdir(d))) {
    /*haetaan yksi kerrallaan oikeat tiedostot*/
    if(!strstr(e->d_name, "peittävyydet_"))
      continue;
    sprintf(cnimi, "%s/%s", kansio, e->d_name);

    FILE* fc = fopen(cnimi, "r");
    if(!fc) {
      fprintf(stderr, "Ei avattu tiedostoa \"%s\"\n", cnimi);
      return 1;
    }

    /*luetaan tiedosto*/
    for(ind=0; fscanf(fc, "%f%hi%hi", kons+ind, paiva+ind, vuosi+ind)==3; ind++);

    if(!(korvaa_strstr(cnimi, "peittävyydet_", "pituus_"))) {
      fprintf(stderr, "Virhe, tunnistetta ei löytynyt nimestä\n");
      return 1;
    }
    fc = freopen(cnimi, "w", fc);

    /*haetaan ajankohdat talvittain eikä vuosittain
      esim 30.12.2020 olisi tällöin -2. päivä vuonna 2021
      talvi vaihtukaan elokuun loputtua päivänä 244,
      kun vuotta on jäljellä 122 päivää (joka vuodelle on varattu 366 päivää)*/

    /*Osoittimet, joita saa muuttaa,
      1. talvi ohitetaan, koska sitä ei ole kokonaan*/
    short* paiva1 = paiva+244;
    short* vuosi1 = vuosi+244;
    float* kons1 = kons+244;
    ind -= 244;

    while(ind>360) { //kun voidaan vielä lukea koko vuosi
      short d0 = 0x7fff; //laitetaan positiivisin luku, jos ei ole jäätä
      short dn = 0;
      for(int i=0; i<366; i++)
	if(kons1[i] >= konsraja && !dn++)
	  d0 = ((paiva1[i]+122) % 366) - 122;
      paiva1 += 366;
      vuosi1 += 366;
      kons1 += 366;
      ind -= 366;
      fprintf(fc, "%hi\t%hi\t%hi\n", dn, d0, vuosi1[0]);
    }
    fclose(fc);
  }
  free(vuosi);
  free(paiva);
  free(kons);
  closedir(d);
  return 0;
}
