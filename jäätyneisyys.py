#!/usr/bin/python3

### kuvaajat jäätyneenä olemisen todennäköisyydestä vuoden kuluessa ###

import matplotlib.pyplot as plt
import numpy as np

historia = 1;

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

def piirraKuva(paikka_ajot, alkuv, loppuv, fig):
    for pind in range(len(paikat)):
        ax = plt.subplot(3,2,pind+1);
        sarakt = np.shape(paikka_ajot)[2] - 2; #lopussa päivä ja vuosi
        for aind in range(sarakt):
            F = [0]*365;
            alkuind = alkuv*366 + 244;
            loppuind = loppuv*366 + 244;
            ind = alkuind
            while(ind + 366 < loppuind):
                for d in range(366):
                    if(paikka_ajot[pind][ind+d][aind] == 0):
                        paiva = paikka_ajot[pind][ind+d][-2];
                        if(paiva != 366):
                            F[paiva-1] += 1;
                ind += 366;
            F = np.array(F);
            F = F/(loppuv-alkuv); #nimittäjänä n eikä n+1
            plt.plot(np.arange(365), F, color=varit[aind]);
    if 1:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/jäätyneisyys%i.png' %paikka_ajot[0][alkuv*366][0]);
    print(F)

paikka_ajot = [[]]*len(paikat);
for pind in range(len(paikat)):
    tied = "%s/%s_sulako%s.txt" %(sk, paikat[pind], "Hist" if historia else "");
    suluus = np.genfromtxt(tied, comments="#", dtype='int16');
    paikka_ajot[pind] = suluus;

print(paikka_ajot[0][365][-2])
alku0 = 0;
loppu0 = aika;

fig = plt.figure(figsize=(12,10));
piirraKuva(paikka_ajot, alku0, loppu0, fig);
plt.close();
