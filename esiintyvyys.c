#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <math.h>

static float* luenta;
static float *todnak, *tulos;
static short* vuodet;
static int paiva0, vuosi0, vuosi1;

void alusta(int, int, int);
void siirra_aikaikkunaa(int);
float* esiintyvyys(const char*, float, int);
void vapauta();
static float* suodate(int);

void alusta(int p0, int v0, int v1) {
  paiva0 = p0;
  vuosi0 = v0; vuosi1 = v1;
  luenta = malloc(366*(v1-v0+2)*sizeof(float));
  vuodet = malloc(366*(v1-v0+2)*2);
  todnak = malloc(365*sizeof(float)); //hypätään karkauspäivien yli
  tulos = malloc(365*sizeof(float));
}

void siirra_aikaikkunaa(int maara) {
  vuosi0 += maara;
  vuosi1 += maara;
}

float* esiintyvyys(const char* tiednimi, float konsraja, int gausspit) {
  /*paikallistaminen näyttää yhtyvän pythonin kanssa,
    joten tämä pitää määrittää joka kerralla erikseen*/
  setlocale(LC_ALL, "en_US.utf8");
  int pituus;
  FILE *f = fopen(tiednimi, "r");
  if(!f) {
    printf("Ei avattu tiedostoa: \"%s\"\n", tiednimi);
    return NULL;
  }
  /*siirrytään ensimmäisen vuoden kohdalle*/
  fscanf(f, "%*f%*i%hi\n", vuodet);
  /*rivit ovat yhtä pitkiä*/
  int rivi = 0;
  do
    rivi++;
  while(fgetc(f) != '\n');
  int apui = (vuosi0-1-*vuodet)*366; //ohitettavia päiviä
  fseek(f,apui*rivi,SEEK_SET); //lukeminen alkaa ennen vuosi0:n alkua
  pituus = (vuosi1-vuosi0+2)*366; //+2: esim 2007̇–2007 vaatii myös 2006:n lukemisen
  for(int i=0; i<pituus; i++)
    fscanf(f, "%f%*i%hi", luenta+i, vuodet+i);
  fclose(f);
  
  for(int i=0; i<365; i++)
    todnak[i] = 0;
  int paivaind = 0;
  int i = paiva0-gausspit+365+!((vuosi0-1)%4);
  int paate = pituus+i-366;
  for(; i<paate; i++) {
    paivaind %= 365;
    if(paivaind+paiva0-gausspit == 59 && vuodet[i]%4 == 0)
      i++; //karkauspäivän ohitus
    else if(!(luenta[i] == luenta[i])) {
      if(paivaind+paiva0-gausspit)
	printf("NAN osui väärälle päivälle: %i\n", paivaind+paiva0-gausspit);
      i++;
    }
    todnak[paivaind] += luenta[i] >= konsraja;
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
