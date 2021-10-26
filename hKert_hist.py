#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
from jaettu import *
import locale, sys
import matplotlib.ticker as ticker

locale.setlocale(locale.LC_ALL, paikallisuus);

paikkaind = (2, 8, 6, 11);

#luetaan havainnot
hnnot = [[]]*(loppuvuosi-alkuvuosi);
data=np.genfromtxt(hnnotTied, delimiter=",", comments="#", usecols=paikkaind);
for i in range(len(paikkaind)):
    v0 = alkuvuosi;
    v1 = loppuvuosi;
    if(paikat[i] == "Nordmaling"): #täältä on eri aikasarja
        v0 += 1;
        v1 += 1;
    H = data[v0-1912 : v1-1912, i] #valitaan aika ja paikka
    H = H[~np.isnan(H)];
    hnnot[i] = H;

#luetaan malli
paikka_ajo = [[]]*len(paikat);
for j in range(len(paikat)):
    paikkatulos = [[]]*len(ajot);
    for i in range(len(ajot)):
        tied = "%s%s_%s_%s_maks.txt" %(sk, paikat[j], muuttuja, ajot[i]);
        paikkatulos[i] = np.genfromtxt(tied, usecols=(0));

    paikka_ajo[j] = np.vstack(paikkatulos);
    
plt.figure(figsize=(12,10));

for p in range(len(paikat)):
    ax = plt.subplot(3,2,p+1);
    
    if(p < len(paikkaind)): #havainnot
        htmp = np.sort(hnnot[p]);
        F = np.array(range(1,len(htmp)+1)) / (len(htmp)+1.0); #kokeellinen kertymäfunktio
        plt.plot(htmp, F, color='k', label="havainnot");        
    for a in range(len(ajot)): #malli
        htmp = np.sort(paikka_ajo[p][a])
        F = np.array(range(1,len(htmp)+1)) / (len(htmp)+1.0); #kokeellinen kertymäfunktio
        plt.plot(htmp, F, color=varit[a], label=ajonimet[a]);
    
    plt.grid('on')
    plt.title(paikat[p], fontsize=15);
    paikallista_akselit();
    plt.ylim(0,1)
    plt.xlim(0,110)
    plt.ylabel('Todennäköisyyskertymä',fontsize=15)
    plt.xlabel('Paksuuden vuosimaksimi (cm)',fontsize=15)
    plt.yticks(fontsize=13);
    plt.xticks(fontsize=13);
    plt.legend(ncol=1, fontsize=11, loc='upper left', frameon=0);
    plt.tight_layout();

if len(sys.argv)==2 and sys.argv[1]=='1':
    plt.savefig('/home/aerkkila/a/kuvat1/pakskert_hist.png');
else:
    plt.show();
