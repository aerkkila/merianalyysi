#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <math.h>

static float* luenta;
static float *todnak, *tulos;
static short* vuodet;
static int paiva0, vuosi0, vuosi1, yksipituus;

void alusta(int, int, int);
void siirra_aikaikkunaa(int);
float* esiintyvyys(float, int, int);
void vapauta();
static float* suodate(int);

void alusta(int p0, int v0, int v1) {
  paiva0 = p0;
  vuosi0 = v0; vuosi1 = v1;
  luenta = malloc(366*100*36*sizeof(float)); //36 ajoa, 100 vuotta
  vuodet = malloc(366*100*2);
  todnak = malloc(365*sizeof(float)); //hypätään karkauspäivien yli
  tulos = malloc(365*sizeof(float));
  const char* paikat[] = {"Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn"};
  const char* ajot[] = {"A002", "A005", "B002", "B005", "D002", "D005"};
  FILE *f;
  int k=0;
  char tiednimi[200];
  for(int i=0; i<6; i++)
    for(int j=0; j<6; j++) {
      sprintf(tiednimi, "/home/aerkkila/b/tiedokset/peittävyydet_%s_%s.txt", paikat[i], ajot[j]);
      if(i==0 && j==0) {
	FILE *f = fopen(tiednimi, "r");
	if(!f)
	  printf("Ei luettu tiedostoa %s\n", tiednimi);
	for(; fscanf(f, "%f%*i%hi", luenta+k,vuodet+k)==2; k++);
	yksipituus = k;
	fclose(f);
      } else {
	f = fopen(tiednimi, "r");
	if(!f)
	  printf("Ei luettu tiedostoa %s\n", tiednimi);;
	for(; fscanf(f, "%f%*i%*i", luenta+k)==1; k++);
	fclose(f);
      }
    }
}

void siirra_aikaikkunaa(int maara) {
  vuosi0 += maara;
  vuosi1 += maara;
}

float* esiintyvyys(float konsraja, int gausspit, int tiedosind) {
  /*paikallistaminen näyttää yhtyvän pythonin kanssa,
    joten tämä pitää määrittää joka kerralla erikseen*/
  setlocale(LC_ALL, "en_US.utf8");
  int kohta = tiedosind*yksipituus;
  int pituus;
  int apui = (vuosi0-1-*vuodet)*366; //ohitettavia päiviä
  pituus = (vuosi1-vuosi0+2)*366;
  
  for(int i=0; i<365; i++)
    todnak[i] = 0;
  int paivaind = 0;
  int i = apui+paiva0-gausspit+365+!((vuosi0-1)%4);
  int paate = pituus-366+i;
  for(; i<paate; i++) {
    paivaind %= 365;
    if(paivaind+paiva0-gausspit == 59 && vuodet[i]%4 == 0)
      i++; //karkauspäivän ohitus
    else if(!(luenta[i+kohta] == luenta[i+kohta])) {
      if(paivaind+paiva0-gausspit)
	printf("NAN osui väärälle päivälle: %i\n", paivaind+paiva0-gausspit);
      i++;
    }
    todnak[paivaind] += luenta[i+kohta] >= konsraja;
    paivaind++;
  }
  const float kerroin = 1.0/(vuosi1-vuosi0+1);
  for(int i=0; i<365; i++)
    todnak[i] *= kerroin;
  return suodate(gausspit);
}

void vapauta() {
  free(luenta);
  free(todnak);
  free(vuodet);
  free(tulos);
}

#define KERROIN 0.39894228 // 1/sqrt(2*pi)
#define SIGMA (gausspit*0.33333333333)
#define GAUSSPAINO(t) ( KERROIN/SIGMA * exp(-0.5*(t)*(t)/(SIGMA*SIGMA)) )
static float gausskert[200];

/*gausspit <= 100*/
static float* suodate(int gausspit) {
  float* restrict td = todnak+gausspit;
  float* gkert = gausskert + 100;
  for(int t=0; t<=gausspit; t++) {
    gkert[t] = GAUSSPAINO(t);
    gkert[-t] = GAUSSPAINO(t);
  }
  for(int i=0; i<265; i++) {
    float summa = 0;
    for(int T=-gausspit; T<=gausspit; T++)
      summa += td[i+T]*gkert[T];
    tulos[i] = summa;
  }
  return tulos;
}
