#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "jaagrid.h"
#include "pintaalavakiot.h"

#define dA(lat1, lat2, lon1, lon2) ((lon2-lon1)*R*R*(sin(lat2)-sin(lat1))*1.0e-6)
#define rad(kulma) (kulma*pi/180)
#define pi 3.14159265
#define PATKA 1000

maapintaala_t maapintaala(float* lat, float* lon, int gridpit,	\
			  float lata, float laty,		\
			  float lona, float lony) {
  float lat0=0, lat1=0, lon0, lon1;
  maapintaala_t maa;
  maa.alat = malloc(1);
  maa.indeksit = malloc(1);
  int patkia = -1;
  int gridind=0, lukuind=0;
  
  while(1) {
    /*alustetaan muistia alussa yksi pätkä ja sen täyttyessä aina uusi pätkä*/
    maa.alat = realloc(maa.alat, (++patkia+1)*PATKA*sizeof(float));
    maa.indeksit = realloc(maa.indeksit, (patkia+1)*PATKA*sizeof(int));
    /*kierrokselta yksi oikean tai nolla väärän välin pinta-alaa*/
    while(lukuind+1 < PATKA*(patkia+1)) {
      if(gridind+1 >= gridpit)
	goto LOPPU;
      lat0 = lat[gridind];
      lon0 = lon[gridind];
      gridind++;
      /*ollaanko haluttujen koordinaattirajojen sisäpuolella*/
      if(lat0 < lata || lat0 > laty)
	continue;
      if(lon0 < lona || lon0 > lony)
	continue;
      
      /*tarvittaessa haetaan uusi yläraja,
	johon leveyspiiri rajoittuu eli seuraava suurempi lat
	ruutuja iteroidaan vasemmalta oikealla alhaalta ylös
	eli lat ei vaihdu joka ruudussa, mutta lon vaihtuu*/
      if( !(lat0 < lat1) )
	for(int i=gridind; i<gridpit; i++)
	  if(lat[i] > lat0) {
	    lat1 = lat[i];
	    break;
	  }
      
      if(lat1 < lata || lat1 > laty)
	continue;
      
      /*haetaan nyt pituuspiirin rajoittajaväli*/
      lon1 = lon[gridind];
      if( !(lon0 < lon1) )
        continue;

      if(lon1 < lona || lon1 > lony)
	continue;

      /*otetaan pinta-ala*/
      maa.indeksit[lukuind] = gridind;
      maa.alat[lukuind] =\
	dA(rad(lat0), rad(lat1), rad(lon0), rad(lon1));
      
      lukuind++;
    }
  }
 LOPPU:
  maa.alat[lukuind] = -1.0;
  maa.pituus = lukuind;
  return maa;
}
