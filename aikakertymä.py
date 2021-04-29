#!/usr/bin/python3

### kuvaajat jäätymisajankohdan tai jäätalven pituuden kertymätodennäköisyyksistä ###

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
import ctypes
import locale
import matplotlib.ticker as ticker

locale.setlocale(locale.LC_ALL, "fi_FI.utf8");
paikallistaja = ticker.ScalarFormatter(useLocale=True);
def paikallista_akselit(x=1,y=1):
    if x:
        plt.gca().xaxis.set_major_formatter(paikallistaja);
    if y:
        plt.gca().yaxis.set_major_formatter(paikallistaja);

tiedot = ("jäätymispäivä", "jäätalven_kesto");
sarake = 1; #kumpi yllä olevista valitaan
xnimi = tiedot[sarake];
historia = 0; #historia-ajo vai skenaario

if historia:
    ajot = ("A001", "B001", "D001");
    ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
else:
    ajot = ("A002", "A005", "B002", "B005", "D002", "D005");
    ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
sk = "/home/aerkkila/a/pakspaikat/";
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue");
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
aika = 30;

minimi = 1000.0;
maksimi = -1000.0; #nämä selitetty alempana

def piirraKuva(paikka_ajo, alku, loppu, vuodet, fig):
    for p in range(len(paikat)):
        ax = plt.subplot(3,2,p+1);

        for a in range(len(ajot)): #malli
            dtmp = np.sort(paikka_ajo[p][a][alku:loppu]);
            F = np.array(range(1,len(dtmp)+1)) / (len(dtmp)+1.0); #kokeellinen kertymäfunktio
            kerr = 2 if historia else 1;
            plt.plot(dtmp, F, color=varit[a*kerr], label=ajonimet[a]);

        plt.grid('on');
        plt.title(paikat[p], fontsize=15);
        paikallista_akselit();
        plt.ylim(0,1);
        plt.xlim(minimi, maksimi);
        plt.ylabel('Todennäköisyyskertymä',fontsize=15);
        plt.xlabel(xnimi,fontsize=15);
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        plt.legend(ncol=1, fontsize=11, frameon=0);
        plt.tight_layout();
    fig.suptitle("%i – %i" %(vuodet[alku], vuodet[loppu-1]), fontsize=18);

    if 1:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/%s%i.png' %(xnimi,vuodet[alku]));

#luetaan malli
paikka_ajo = [[]]*len(paikat);
tied = "";

#jos ei jäätä, jäätysmisajankohta on 0x7fff eli suurin luku (int16)
#rajataan x-akseli minimiin ja maksimiin

for j in range(len(paikat)):
    paikkatulos = [[]]*len(ajot);
    for i in range(len(ajot)):
        tied = "%s%s_%s_ajankohdat.txt" %(sk, paikat[j], ajot[i]);
        paikkatulos[i] = np.genfromtxt(tied, usecols=(sarake));
        iso = np.max(paikkatulos[i][np.where(paikkatulos[i] < ctypes.c_int16(0x7fff).value)]);
        pieni = np.min(paikkatulos[i]);
        if(pieni < minimi):
            minimi = pieni
        if(iso > maksimi):
            maksimi = iso;
    paikka_ajo[j] = np.vstack(paikkatulos);

vuodet = np.genfromtxt(tied, usecols=(2));
alku0 = 0;
loppu0 = aika;
loppu1 = len(vuodet);
alku1 = loppu1-aika;

fig = plt.figure(figsize=(12,10));
piirraKuva(paikka_ajo, alku0, loppu0, vuodet, fig);
plt.close();

if alku1 - alku0 > aika/2:
    fig = plt.figure(figsize=(12,10));
    piirraKuva(paikka_ajo, alku1, loppu1, vuodet, fig);
