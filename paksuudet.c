#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*Tämä hakee tekstiksi käännetyistä nc-tiedostoista halutuista koordinaateista paksuudet ja tulostaa kahdeksi eri tiedostoksi koko aikasarjan sekä vuosittaiset maksimit. Maksimeiksi hyväksytään vain kiintojää.
  Jää oletetaan ajojääksi, jos kasvunopeus ylittää valitun raja-arvon.

  Komentorivillä annetaan ajojen nimet ja lopussa ensimmäinen ja viimeinen vuosi, esimerkiksi ./paksuudet A001 B001 D001 1975 2005. Tiedostoista icevolume*.nc on oltava jään paksuudet tekstiksi käännettyinä ja tarvitaan myös tiedosto latlon.txt, jossa on ensin jokaisen koordinaattiruudun leveys- ja sitten pituuspiirit joitten viimeistenkin arvojen jälkeen on oltava pilkku ja sitten puolipiste. Muuta ei saa olla.*/

typedef struct {
  float* lat;
  float* lon;
  int gridpit;
} latlon;

/*matka² karkeasti ottaen: ajatellaan lon-eron olevan 0,4*lat-ero näillä leveyspiireillä
  ja, että maanpinnan kaarevuus on vähäistä
  tällä ainoastaan haetaan lähin piste, joten ei tarvita tarkempaa matkaa tai maapallon sädettä*/
#define MATKA(lat,lon,lat1,lon1) pow((lat-lat1), 2) + pow((lon-lon1)*0.4, 2)

/*haetaan indeksi annettuja koordinaatteja lähimmäs osuvalle pisteelle*/
int hae_koord_indeksi(latlon ktit,  float lat, float lon) {
  int lyhin_ind = 0;
  int ind = 0;
  float lyhin = 100.0;
  float matka;
  while(*ktit.lat > -0.5 && *ktit.lon > -0.5) {
    matka = MATKA(lat, lon, *ktit.lat++, *ktit.lon++);
    if (matka < lyhin) {
      lyhin = matka;
      lyhin_ind = ind;
    }
    ind++;
  }
  return lyhin_ind;
}

/*luetaan jokaisen ruudun pituus- ja leveyspiiri*/
latlon lue_koordtit(char* latlontied) {
  int i = 0;
  latlon ktit;
  FILE *f = fopen(latlontied, "r");
  char c;
  if(!f) {
    fprintf(stderr, "Virhe: tiedoston \"%s\" avaaminen ei onnistu\n", latlontied);
    return ktit;
  }
  
  /*haetaan tarvittava taulukon pituus*/
  ktit.gridpit = 0; //viimeisenkin jälkeen tulee pilkku
  while( (( c=fgetc(f) )) != ';' )
    if(c==',')
      ktit.gridpit++;
  rewind(f);

  ktit.lat = calloc(ktit.gridpit+2, sizeof(float));
  ktit.lon = calloc(ktit.gridpit+2, sizeof(float));

  /*luetaan koordinaatit*/
  float* apu = ktit.lat;
  while(fscanf(f, "%f,", apu++));
  *apu = -1.0; // -1 merkitsee taulukon päättymistä
  
  while(fgetc(f) != ';');
  apu = ktit.lon;
  while(fscanf(f, "%f,", apu++));
  *apu = -1.0;
  
  fclose(f);
  return ktit;
}

float* lue_vuoden_paks(FILE* f, int indeksi, int gridpit) {
  float* vuoden_paks = calloc(367, sizeof(float));
  float* apu = vuoden_paks;
  float turha;
    
  /*siirrytään indeksin kohdalle*/
  char c;
  int j=0;
  while(j<indeksi) {
    if( (( c = fgetc(f) )) == ';')
      goto MURRA;
    if(c == ',')
      j++;
  }

  int kerta = 0;
  while(1) {
    /*luetaan arvo*/
    if(!fscanf(f, "%f", apu++)) {
      fprintf(stderr, "Virhe: Ei luettu arvoa %i. kerralla\n", kerta);
      goto MURRA;
    }
    kerta++;
    /*luetaan seuraavaan samaan indeksiin asti
      tässä mennään koko kierros, koska äskeinen arvo lasketaan mukaan,
      koska pilkkua ei luettu sen jälkeen, ei siis lopeteta gridpit-1:en*/
    j=0;
    while(j<gridpit) {
      if( (( c=fgetc(f) )) == ';')
	goto MURRA;
      if( c == ',')
	j++;
    }
  }
  
 MURRA:
  *apu = -1.0;
  return vuoden_paks;
}

#define arrpit(x) (int)(sizeof(x)/sizeof(x[0]))

int main(int argc, char** argv) {
  char ulakansio[] = "/home/aerkkila/a/";
  char uloskansio[] = "pakspaikat/";
  char siskansio[] = "ncteksti/";
  char latlontied[] = "latlon.txt";
  char* paikat[] = {"Kemi_", "Hailuoto_", "Raahe_", "Kalajoki_", "Pietarsaari_", "Mustasaari_"};
  float paikatlat[] = {65.6322, 64.9307, 64.6508, 64.2245, 63.7466, 63.1579};
  float paikatlon[] = {24.4908, 24.6760, 24.3768, 23.6939, 22.5434, 21.2553};
  char muuttuja[] = "icevolume_";
  char ajo[5];
  char tmpnimi[200];
  int alkuvuosi;
  int loppuvuosi;
  FILE *f;

  /*komentorivillä olkoot ensin halutut ajonimet sanojen lopussa ja lopussa alku- ja loppuvuosi*/
  if(argc < 4) {
    fprintf(stderr, "Liian vähän argumentteja\n");
    return 1;
  }
  if(!sscanf(argv[argc-1], "%i", &loppuvuosi)) {
    fprintf(stderr, "Ei annettu loppuvuotta\n");
    return 1;
  }
  if(!sscanf(argv[argc-2], "%i", &alkuvuosi)) {
    fprintf(stderr, "Ei annettu alkuvuotta\n");
    return 1;
  }
  if(alkuvuosi > loppuvuosi)
    printf("Varoitus: alkuvuosi = %i, loppuvuosi = %i\n", alkuvuosi, loppuvuosi);

  loppuvuosi++; //olkoon tämä ensimmäinen vuosi, jota ei ole
  int vuosia=loppuvuosi-alkuvuosi;

  sprintf(tmpnimi, "%s%s%s", ulakansio, siskansio, latlontied);
  latlon ktit = lue_koordtit(tmpnimi);

  /*haetaan paikkojen indeksit gridissä*/
  sprintf(tmpnimi, "%s%skoordinaatit.txt", ulakansio, uloskansio);
  f = fopen(tmpnimi, "w");
  int* pind = malloc(arrpit(paikatlat)*sizeof(int));
  for(int i=0; i<arrpit(paikatlat); i++) {
    pind[i] = hae_koord_indeksi(ktit, paikatlat[i], paikatlon[i]);    
    printf("%s:\nIndeksi:\t%i\nHaettiin:\t%.4f\t%.4f\nSaatiin:\t%.4f\t%.4f\n\n", \
	   paikat[i], pind[i], paikatlat[i], paikatlon[i], ktit.lat[pind[i]], ktit.lon[pind[i]]);
    fprintf(f, "%s:\nIndeksi:\t%i\nHaettiin:\t%.4f\t%.4f\nSaatiin:\t%.4f\t%.4f\n\n", \
	   paikat[i], pind[i], paikatlat[i], paikatlon[i], ktit.lat[pind[i]], ktit.lon[pind[i]]);
  }
  fclose(f);

  sprintf(tmpnimi, "%s%sajojäät.txt", ulakansio, uloskansio);
  FILE *fajojaa = fopen(tmpnimi, "w");

  for (int ajoind=1; ajoind<argc-2; ajoind++) {
    char *apu = argv[ajoind]+strlen(argv[ajoind])-4; //viimeiset neljä ovat esim A001
    strcpy(ajo, apu);
    printf("\r%s (%i / %i)                      \n", ajo, ajoind, argc-3);

    int paikkoja = arrpit(paikatlat);
    for(int paikka=0; paikka<paikkoja; paikka++) {
      /*avataan ulostulot
       esim /kansio/pakspaikat/Kemi_icevolume_A001_max.txt*/
      sprintf(tmpnimi, "%s%s%s%s%s_kaikki.txt",
	      ulakansio, uloskansio, paikat[paikka], muuttuja, ajo);
      FILE* fkaikki = fopen(tmpnimi, "w");
    
      sprintf(tmpnimi, "%s%s%s%s%s_maks.txt",
	      ulakansio, uloskansio, paikat[paikka], muuttuja, ajo);
      FILE* fmaks = fopen(tmpnimi, "w");
  
      for(int i=0; i<vuosia; i++) {
	/* avataan luettava tiedosto,
	   esim /home/aerkkila/a/ncteksti/icevolume_A001_1999.txt */
	sprintf(tmpnimi, "%s%s%s%s_%i.txt",
		ulakansio, siskansio, muuttuja, ajo, i+alkuvuosi);
	FILE *sis = fopen(tmpnimi, "r");
	if(!sis) {
	  fprintf(stderr, "Virhe: Ei avattu tiedostoa \"%s\"\n", tmpnimi);
	  return 1;
	}
	float* paks = lue_vuoden_paks(sis, pind[paikka], ktit.gridpit);
	printf("\r%i / %i\t (paikka %i / %i)", i+1, vuosia, paikka+1, paikkoja);
	fflush(stdout);
	for(int j=1; j<=366; j++)
	  fprintf(fkaikki, "%.3f\t%i\t%i\n", paks[j], j, i+alkuvuosi);
	fclose(sis);
    
	/*haetaan ja tulostetaan maksimi ajankohtineen
	  loppukeväällä voi ajautua paksua ajojäätä,
	  asetetaan siksi raja-arvo päivittäiselle kasvulle,
	  jonka ylityttyä oletetaan jään olevan ajojäätä ja hylätään*/
	float kasvuraja = 0.25; //metriä päivässä
	float maks = 0;
	int maksind = 0;
	for(int j=1; j<366; j++) {
	  if(paks[j]-paks[j-1] > kasvuraja) {
	    fprintf(fajojaa, "\n%s, %s, vuosi %i, päivä %i, Δh = %.1f cm / d\n",
		   paikat[paikka], argv[ajoind], i+alkuvuosi, j+1, (paks[j]-paks[j-1])*100);
	    break;
	  }
	  if(paks[j] > maks) {
	    maks = paks[j];
	    maksind = j;
	  }
	}
	fprintf(fmaks, "%.3f\t%i\t%i\n", maks, maksind+1, i+alkuvuosi);
	free(paks);
      }
      
      fclose(fkaikki);
      fclose(fmaks);
    }
  }
  fclose(fajojaa);
  free(ktit.lat);
  free(ktit.lon);
  free(pind);
  putchar('\n');
  return 0;
}
