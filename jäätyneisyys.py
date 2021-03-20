#!/usr/bin/python3

### kuvaajat jäätyneenä olemisen todennäköisyydestä vuoden kuluessa ###

import matplotlib.pyplot as plt
import numpy as np

historia = 0;

if historia:
    ajot = ("A001", "B001", "D001");
    ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
else:
    ajot = ("A002", "A005", "B002", "B005", "D002", "D005");
    ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
sk = "/home/aerkkila/a/pakspaikat";
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue");
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
aika = 30;

#piirrettäköön kuvaaja 1.11. – 15.6.
miinuspaiva = 61;
pluspaiva = 166;

def piirraKuva(paikka_ajot, alkuv, loppuv, fig):
    kerr = 2 if historia else 1;
    for pind in range(len(paikat)):
        ax = plt.subplot(3,2,pind+1);
        sarakt = np.shape(paikka_ajot)[2] - 2; #lopussa päivä ja vuosi
        for aind in range(sarakt):
            paivia = len(np.where(paikka_ajot[pind][:,-1] == alkuv+1)[0]);
            F = [0]*(paivia);
            alkuind = np.where(paikka_ajot[pind][:,-1] == alkuv)[0][pluspaiva];
            w = np.where(paikka_ajot[pind][:,-1] == loppuv)[0];
            loppuind = w[pluspaiva] if(len(w)) else len(paikka_ajot);
            ind = alkuind
            xPaivat = np.arange(-miinuspaiva,0);
            xPaivat = np.append(xPaivat, np.arange(1,pluspaiva+1));
            while(ind < loppuind):
                for d in range(paivia):
                    if(paikka_ajot[pind][ind][aind] == 0):
                        F[d] += 1;
                    ind+=1;
            F = np.array(F);
            F = F/(loppuv-alkuv); #nimittäjänä n eikä n+1
            plt.plot(xPaivat, F, color=varit[aind*kerr], label=ajonimet[aind]);
        plt.grid('on');
        plt.ylim([-0.05, 1.05]);
        plt.title(paikat[pind], fontsize=15);
        plt.ylabel('jään todennäköisyys',fontsize=15);
        plt.legend(ncol=1, fontsize=11, frameon=0);
        plt.tight_layout();
    fig.suptitle("%i – %i" %(alkuv+1, loppuv), fontsize=18);
    if 1:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/jäätyneisyys%i.png' %(alkuv+1));

paikka_ajot = [[]]*len(paikat);
for pind in range(len(paikat)):
    tied = "%s/%s_sulako%s.txt" %(sk, paikat[pind], "Hist" if historia else "");
    suluus = np.genfromtxt(tied, comments="#", dtype='int16');
    #1. vuosi jää pois, koska talvea ei ole kokonaan, samaten viim. puoli vuotta
    pit = len(suluus);
    mukaan = np.zeros(len(suluus), dtype='bool');
    for i in range(pit-miinuspaiva):
        vuosi = suluus[i,-1];
        paiva = suluus[i,-2];
        if(vuosi%4 and 365 >= paiva and paiva > 365-miinuspaiva):
            mukaan[i] = True;
        elif(vuosi%4==0 and 366 >= paiva and paiva > 366-miinuspaiva):
            mukaan[i] = True;
        elif(paiva <= pluspaiva):
            mukaan[i] = True;

    paikka_ajot[pind] = suluus[mukaan];

alkuv = paikka_ajot[0][0,-1]; #kirjoitettakoon suurempi vuosiluku, koska vuosi vaihtuu
loppuv = paikka_ajot[0][-1,-1];
valiv = 0;

if((loppuv-alkuv)/aika < 1.5):
    valiv = loppuv
    loppuv = 0;
else:
    valiv = alkuv+aika;
    valiv1 = loppuv-aika;

fig = plt.figure(figsize=(12,10));
piirraKuva(paikka_ajot, alkuv, valiv, fig);
plt.close();

if(loppuv):
    fig = plt.figure(figsize=(12,10));
    piirraKuva(paikka_ajot, valiv1, loppuv, fig);
