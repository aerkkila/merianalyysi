#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  short arvo;
  short paikka;
} maks_t;

maks_t hae_maksimi(short* h, float* c, int pit, float konsraja) {
  maks_t r = (maks_t){h[0], 0};
  
  for(int i=1; i<pit; i++) {      
    if (h[i] > r.arvo && c[i] > konsraja)
      r = (maks_t){h[i], i};
  }
  return r;
}

/*vaihtaa a:ssa b:n tilalle c:n*/
char* korvaa_strstr(char* a, char* b, char* c) {
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
  char siskansio[] = "/home/aerkkila/a/pakspaikat/";
  char uloskansio[] = "/home/aerkkila/a/pakspaikat/";
  char hmuuttuja[] = "icevolume";
  char cmuuttuja[] = "soicecov";
  char tunniste[] = "kaikki.txt";
  char uusi_tunniste[] = "maks.txt";
  float konsraja = 0.9;
  DIR *d = opendir(siskansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", siskansio);
    return 1;
  }
  struct dirent *e;
  char *hnimi = malloc(500);
  char *cnimi = malloc(500);
  /*tämä on vain nopeasti koodattu, joten ohjelma ei määritä pituutta itse*/
  int pit = 20000;
  short* vuosi = malloc(pit*sizeof(short));
  short* paiva = malloc(pit*sizeof(short));
  short* paks = malloc(pit*sizeof(short));
  float* kons = malloc(pit*sizeof(float));
  float apu; //paksuus on tallennettu metreinä, mutta otetaan sentteinä
  int ind;
  while((e = readdir(d))) {
    /*haetaan yksi kerrallaan oikeat paksuustiedostot*/
    if(strstr(e->d_name, hmuuttuja) && strstr(e->d_name, tunniste)) {

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
      
      short* paks1 = paks;
      short* paiva1 = paiva;
      short* vuosi1 = vuosi;
      float* kons1 = kons;

      /*luetaan tiedostot*/
      ind = 0;
      while(!feof(fh)) {
	if(!(fscanf(fh, "%f%hi%hi", &apu, paiva1+ind, vuosi1+ind)))
	  break;
	paks1[ind] = (int)(apu*100+0.000001);
	
	if(!(fscanf(fc, "%f%*i%*i", kons1+ind)))
	  fprintf(stderr, "Virhe, konsentraatiot loppuivat ennen paksuuksia\n");
	ind++;
      }

      if(!(korvaa_strstr(hnimi, tunniste, uusi_tunniste))) {
	fprintf(stderr, "Virhe, tunnistetta ei löytynyt nimestä\n");
	return 1;
      }
      fh = freopen(hnimi, "w", fh);
      /*haetaan maksimit talvittain eikä vuosittain
	esim 30.12.2020 olisi tällöin päivä -2 vuonna 2021
	talvi vaihtukoon elokuun loputtua päivänä 244,
	kun vuotta on jäljellä 122 päivää (joka vuodelle on varattu 366 päivää)*/
      maks_t m = hae_maksimi(paks, kons, 244, konsraja);
      fprintf(fh, "%hi\t%hi\t%hi\n", m.arvo, paiva1[m.paikka], vuosi1[m.paikka]);

      paks1 += 244;
      kons1 += 244;
      paiva1 += 244;
      vuosi1 += 244;
      ind -= 244;

      while(ind>300) { //tässä voisi olla 365 tai 366, mutta näin on varmempaa
	m = hae_maksimi(paks1, kons1, 366, konsraja);
	short d = ((paiva1[m.paikka]+122) % 366) - 122;
	short a = vuosi1[m.paikka];
	if(d < 0) a++;
	fprintf(fh, "%hi\t%hi\t%hi\n", m.arvo, d, a);

	paks1 += 366;
	kons1 += 366;
	paiva1 += 366;
	vuosi1 += 366;
	ind -= 366;
      }
      fclose(fh);
      fclose(fc);
    }
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
