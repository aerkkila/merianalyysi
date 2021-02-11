#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  short arvo;
  short paikka;
} maks_t;

maks_t hae_maksimi(short* p, int pit, int kasvuraja) {
  maks_t r = (maks_t){p[0], 0};
  for(int i=1; i<pit; i++) {
    if(p[i-1] == 0)
      continue;
    /*paksu ajojää pois*/
    if(p[i]-p[i-1] > kasvuraja)
      break;
    if (p[i] > r.arvo) {
      r.arvo = p[i];
      r.paikka = i;
    }
  }
  return r;
}

int main() {
  char siskansio[] = "/home/aerkkila/a/pakspaikat/";
  char uloskansio[] = "/home/aerkkila/a/pakspaikat/";
  char muuttuja[] = "icevolume";
  char tunniste[] = "kaikki.txt";
  char uusi_tunniste[] = "maks.txt";
  int kasvuraja = 17;
  DIR *d = opendir(siskansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", siskansio);
    return 1;
  }
  struct dirent *e;
  char *nimi = malloc(500);
  /*tämä on vain nopeasti koodattu, joten ohjelma ei määritä pituutta itse*/
  int pit = 20000;
  short* vuosi = malloc(pit*sizeof(short));
  short* paiva = malloc(pit*sizeof(short));
  short* paks = malloc(pit*sizeof(short));
  float apu; //paksuus on tallennettu metreinä, mutta otetaan sentteinä
  int ind;
  while((e = readdir(d))) {
    if(strstr(e->d_name, muuttuja) && strstr(e->d_name, tunniste)) {
      
      sprintf(nimi, "%s%s", siskansio, e->d_name);
      FILE* f = fopen(nimi, "r");
      if(!f) {
	fprintf(stderr, "Ei avattu tiedostoa \"%s\"\n", e->d_name);
	return 1;
      }

      
      short* paks1 = paks;
      short* paiva1 = paiva;
      short* vuosi1 = vuosi;

      /*luetaan tiedosto*/
      ind = 0;
      while(!feof(f)) {
	if(!(fscanf(f, "%f%hi%hi", &apu, paiva1+ind, vuosi1+ind)))
	  break;
	paks1[ind] = (int)(apu*100+0.000001);
	ind++;
      }

      strcpy(strstr(nimi, tunniste), uusi_tunniste);
      f = freopen(nimi, "w", f);
      /*haetaan maksimit talvittain eikä vuosittain
	esim 30.12.2020 olisi tällöin päivä -2 vuonna 2021
	talvi vaihtukoon elokuun loputtua päivänä 244,
	kun vuotta jäljellä 121 päivää*/
      maks_t m = hae_maksimi(paks, 244, kasvuraja);
      fprintf(f, "%hi\t%hi\t%hi\n", m.arvo, paiva1[m.paikka], vuosi1[m.paikka]);

      paks1 += 244;
      paiva1 += 244;
      vuosi1 += 244;
      ind -= 244;

      while(ind>300) {
	m = hae_maksimi(paks1, 366, kasvuraja);
	short d = ((paiva1[m.paikka]+121) % 365) - 121;
	short a = vuosi1[m.paikka];
	if(d < 0) a++;
	fprintf(f, "%hi\t%hi\t%hi\n", m.arvo, d, a);

	paks1 += 366;
	paiva1 += 366;
	vuosi1 += 366;
	ind -= 366;
      }
      fclose(f);
    }
  }
  free(nimi);
  free(vuosi);
  free(paiva);
  free(paks);
  closedir(d);
  return 0;
}
