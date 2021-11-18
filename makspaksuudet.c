#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  float arvo;
  int paikka;
} maks_t;

/*Paksuuksia ei enää lasketa samana talvena, jos tietyn päivän (PAIVARAJA)
  jälkeen on riittävästi päiviä peräkkäin (N_PAIVIA),
  jolloin paksuus on enintään OHUUSRAJA*/
#ifndef PAIVARAJA
#define PAIVARAJA 80
#endif
#ifndef N_PAIVIA
#define N_PAIVIA 5
#endif
#ifndef OHUUSRAJA
#define OHUUSRAJA 0.6
#endif
#ifndef KASVURAJA
#define KASVURAJA 20.0
#endif

maks_t hae_maksimi(float* h, short* d, int pit) {
  maks_t r = (maks_t){h[0], 0};
  int n_paivia = 0;
  
  for(int i=1; i<pit; i++) {
    if (h[i] > r.arvo) {
      r = (maks_t){h[i], i};
      continue;
    }
    if (d[i] > PAIVARAJA && d[i] < 240) {
      if(h[i+1]-h[i] >= KASVURAJA)
	return r;
      if (h[i] < OHUUSRAJA) {
	if (++n_paivia >= N_PAIVIA)
	  return r;
      } else
	n_paivia = 0;
    }
  }
  return r;
}

/*vaihtaa a:ssa b:n tilalle c:n*/
char* korvaa_strstr(char* a, const char* restrict b, const char* restrict c) {
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

const char* vanha_tunniste = "paksuudet_";
const char* uusi_tunniste = "maksh_";

int main() {
  const char* kansio = "/home/aerkkila/b/tiedokset";
  DIR *d = opendir(kansio);
  if(!d) {
    fprintf(stderr, "Kansiota \"%s\" ei voitu avata\n", kansio);
    return 1;
  }
  struct dirent *e;
  char* hnimi = malloc(500);
  char* cnimi = malloc(500);
#define PIT 36600 //100 vuotta * 366 päivää/vuosi
  short* vuosi = malloc(PIT*sizeof(short));
  short* paiva = malloc(PIT*sizeof(short));
  float* paks = malloc(PIT*sizeof(float));
#undef PIT
  int ind;
  while((e = readdir(d))) {
    /*haetaan yksi kerrallaan oikeat paksuustiedostot*/
    if(!strstr(e->d_name, vanha_tunniste))
      continue;
    sprintf(hnimi, "%s/%s", kansio, e->d_name);

    FILE* fh = fopen(hnimi, "r");
    if(!fh) {
      fprintf(stderr, "Ei avattu tiedostoa \"%s\"\n", hnimi);
      return 1;
    }

    /*luetaan tiedostot*/
    ind = 0;
    while(1) {
      int tmp;
      if((tmp = fscanf(fh, "%f%hi%hi", paks+ind, paiva+ind, vuosi+ind)) != 3)
	break;
      ind++;
    }

    if(!(korvaa_strstr(hnimi, vanha_tunniste, uusi_tunniste))) {
      fprintf(stderr, "Virhe, tunnistetta ei löytynyt nimestä\n");
      return 1;
    }
    fh = freopen(hnimi, "w", fh);
    /*haetaan maksimit talvittain eikä vuosittain
      esim 30.12.2020 olisi tällöin päivä -2 vuonna 2021
      talvi vaihtukaan elokuun loputtua päivänä 244,
      kun vuotta on jäljellä 122 päivää (joka vuodelle on varattu 366 päivää)*/
    
    /*osoittimet, joita saa muuttaa*/
    short* paiva1 = paiva;
    short* vuosi1 = vuosi;
    float* paks1 = paks;
    
    maks_t m = hae_maksimi(paks, paiva, 244);
    fprintf(fh, "%5.1f\t%hi\t%hi\n", m.arvo, paiva1[m.paikka], vuosi1[m.paikka]);

    paks1 += 244;
    paiva1 += 244;
    vuosi1 += 244;
    ind -= 244;

    while(ind>360) { //kun voidaan vielä lukea koko vuosi
      m = hae_maksimi(paks1, paiva1, 366);
      short tmppaiva = ((paiva1[m.paikka]+122) % 366) - 122;
      short tmpvuosi = vuosi1[m.paikka];
      if(tmppaiva < 0)
	tmpvuosi++;
      fprintf(fh, "%5.1f\t%hi\t%hi\n", m.arvo, tmppaiva, tmpvuosi);

      paks1 += 366;
      paiva1 += 366;
      vuosi1 += 366;
      ind -= 366;
    }
    fclose(fh);
  }
  FILE* f = fopen("maksh_parametrit.txt", "w");
  fprintf(f, ("n_päiviä = %i\n"
	      "päiväraja = %i\n"
	      "ohuusraja = %.4f cm\n"),
	  N_PAIVIA, PAIVARAJA, (float)OHUUSRAJA);
  fclose(f);
  free(hnimi);
  free(vuosi);
  free(paiva);
  free(paks);
  closedir(d);
  return 0;
}
