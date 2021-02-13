#!/usr/bin/python3

### Kuvaajan piirtäminen paksuuden kertymätodennäköisyyksistä ###

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *

ajot = ("A002", "A005", "B002", "B005", "D002", "D005");
ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
sk = "/home/aerkkila/a/pakspaikat/";
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue");
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
muuttuja = "icevolume"
aika = 30;

def piirraKuva(paikka_ajo, alku, loppu, vuodet, fig):
    for p in range(len(paikat)):
        ax = plt.subplot(3,2,p+1);

        for a in range(len(ajot)): #malli
            htmp = np.sort(paikka_ajo[p][a][alku:loppu]);
            F = np.array(range(1,len(htmp)+1)) / (len(htmp)+1.0); #kokeellinen kertymäfunktio
            plt.plot(htmp, F, color=varit[a], label=ajonimet[a]);

        plt.grid('on');
        plt.title(paikat[p], fontsize=15);
        plt.ylim(0,1);
        plt.xlim(0,110);
        plt.ylabel('Kertymätodennäköisyys',fontsize=15);
        plt.xlabel('Paksuuden vuosimaksimi (cm)',fontsize=15);
        if(paikat[p] == "Kemi"):
            legsij = 'upper left';
        else:
            legsij = 'lower right';
        plt.legend(ncol=1, fontsize=11, loc=legsij, frameon=0);
        plt.tight_layout();
    fig.suptitle("%i – %i" %(vuodet[alku], vuodet[loppu-1]));

    if 1:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/pakskert_tulev%i.png' %alku);


#luetaan malli
paikka_ajo = [[]]*len(paikat);
tied = "";
for j in range(len(paikat)):
    paikkatulos = [[]]*len(ajot);
    for i in range(len(ajot)):
        tied = "%s%s_%s_%s_maks.txt" %(sk, paikat[j], muuttuja, ajot[i]);
        paikkatulos[i] = np.genfromtxt(tied, usecols=(0));
    paikka_ajo[j] = np.vstack(paikkatulos);
    
vuodet = np.genfromtxt(tied, usecols=(2));

alku0 = 0;
loppu0 = aika;
loppu1 = len(vuodet);
alku1 = loppu1-aika;

fig = plt.figure(figsize=(12,10));
piirraKuva(paikka_ajo, alku0, loppu0, vuodet, fig);
plt.close();

fig = plt.figure(figsize=(12,10));
piirraKuva(paikka_ajo, alku1, loppu1, vuodet, fig);
