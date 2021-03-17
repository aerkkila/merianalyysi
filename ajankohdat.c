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
  const char siskansio[] = "/home/aerkkila/a/pakspaikat/";
  const char uloskansio[] = "/home/aerkkila/a/pakspaikat/";
  const char hmuuttuja[] = "_icevolume";
  const char cmuuttuja[] = "_soicecov";
  const char tunniste[] = "kaikki";
  const char uusi_tunniste[] = "ajankohdat";
  const float konsraja = 0.15;
  const int paksraja = 0.01;
  float apu; //paksuus on tallennettu metreinä, mutta otetaan sentteinä
  char *hnimi = malloc(500);
  char *cnimi = malloc(500);
  int ind;
  
  /*tämä on vain nopeasti koodattu, joten ohjelma ei määritä pituutta itse*/
  int pit = 20000;
  short* vuosi = malloc(pit*sizeof(short));
  short* paiva = malloc(pit*sizeof(short));
  short* paks = malloc(pit*sizeof(short));
  float* kons = malloc(pit*sizeof(float));
  
  DIR *d = opendir(siskansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", siskansio);
    return 1;
  }
  struct dirent *e;

  while((e = readdir(d))) {
    /*haetaan yksi kerrallaan oikeat paksuustiedostot*/
    if(! (strstr(e->d_name, hmuuttuja) && strstr(e->d_name, tunniste)) )
      continue;

    sprintf(hnimi, "%s%s", siskansio, e->d_name);

    /*haetaan vastaava konsentraatiotiedosto*/
    strcpy(cnimi, hnimi);
    cnimi = korvaa_strstr(cnimi, hmuuttuja, cmuuttuja);

    FILE* fh = fopen(hnimi, "r");
    FILE* fc = fopen(cnimi, "r");
    if(!fc || !fh) {
      fprintf(stderr, "Ei avattu tiedostoa \"%s\"\n", (!fc)? cnimi : hnimi);
      return 1;
    }

    /*luetaan tiedostot*/
    ind = 0;
    while(!feof(fh)) {
      if(!(fscanf(fh, "%f%hi%hi", &apu, paiva+ind, vuosi+ind)))
	break;
      paks[ind] = (int)(apu*100+0.000001);
	
      if(!(fscanf(fc, "%f%*i%*i", kons+ind)))
	fprintf(stderr, "Virhe, konsentraatiot loppuivat ennen paksuuksia\n");
      ind++;
    }

    if(!(korvaa_strstr(hnimi, tunniste, uusi_tunniste))) {
      fprintf(stderr, "Virhe, tunnistetta ei löytynyt nimestä\n");
      return 1;
    }
    if(!(korvaa_strstr(hnimi, hmuuttuja, ""))) {
      fprintf(stderr, "Virhe, muuttujan nimeä ei löytynyt nimestä\n");
      return 1;
    }
    fh = freopen(hnimi, "w", fh);

    /*haetaan ajankohdat talvittain eikä vuosittain
      esim 30.12.2020 olisi tällöin -2. päivä vuonna 2021
      talvi vaihtukaan elokuun loputtua päivänä 244,
      kun vuotta on jäljellä 122 päivää (joka vuodelle on varattu 366 päivää)*/

    /*Pointterit, joita saa muuttaa,
      1. talvi ohitetaan, koska sitä ei ole kokonaan*/
    short* paks1 = paks+244;
    short* paiva1 = paiva+244;
    short* vuosi1 = vuosi+244;
    float* kons1 = kons+244;
    ind -= 244;

    while(ind>360) { //kun voidaan vielä lukea koko vuosi
      short d0 = 0x7fff; //laitetaan positiivisin numero, jos ei jäätä
      short dn = 0;
      for(int i=0; i<366; i++)
	if(paks1[i] >= paksraja && kons1[i] >= konsraja)
	  if(!dn++)
	    d0 = ((paiva1[i]+122) % 366) - 122;
      paks1 += 366;
      paiva1 += 366;
      vuosi1 += 366;
      kons1 += 366;
      ind -= 366;
      fprintf(fh, "%hi\t%hi\t%hi\n", d0, dn, vuosi1[0]);
    }
    fclose(fh);
    fclose(fc);
  }
  free(hnimi);
  free(cnimi);
  free(vuosi);
  free(paiva);
  free(paks);
  free(kons);
  closedir(d);
  return 0;
}
