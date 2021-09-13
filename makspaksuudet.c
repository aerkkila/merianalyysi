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
  const char* kansio = "/home/aerkkila/b/tiedokset";
  const float konsraja = 0.9;
  DIR *d = opendir(kansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", kansio);
    return 1;
  }
  struct dirent *e;
  char *hnimi = malloc(500);
  char *cnimi = malloc(500);
#define PIT 36600 //100 vuotta * 366 päivää/vuosi
  short* vuosi = malloc(PIT*sizeof(short));
  short* paiva = malloc(PIT*sizeof(short));
  short* paks = malloc(PIT*sizeof(short));
  float* kons = malloc(PIT*sizeof(float));
#undef PIT
  int ind;
  while((e = readdir(d))) {
    /*haetaan yksi kerrallaan oikeat paksuustiedostot*/
    if(strstr(e->d_name, "paksuudet_")) {
      sprintf(hnimi, "%s/%s", kansio, e->d_name);

      /*vastaava konsentraatiotiedosto*/
      strcpy(cnimi, hnimi);
      cnimi = korvaa_strstr(cnimi, "paksuudet_", "peittävyydet_");

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
	if(!(fscanf(fh, "%hi%hi%hi", paks1+ind, paiva1+ind, vuosi1+ind)))
	  break;	
	if(!(fscanf(fc, "%f%*i%*i", kons1+ind)))
	  fprintf(stderr, "Virhe, peittävyydet loppuivat ennen paksuuksia\n");
	ind++;
      }

      if(!(korvaa_strstr(hnimi, "paksuudet_", "maksh_"))) {
	fprintf(stderr, "Virhe, tunnistetta ei löytynyt nimestä\n");
	return 1;
      }
      fh = freopen(hnimi, "w", fh);
      /*haetaan maksimit talvittain eikä vuosittain
	esim 30.12.2020 olisi tällöin päivä -2 vuonna 2021
	talvi vaihtukaan elokuun loputtua päivänä 244,
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
