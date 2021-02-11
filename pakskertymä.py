#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
import tarpeelliset_asiat as t

### Kuvaajan plottaus mallien ja havaintojen kertymätodennäköisyyksistä ###

#kertymätodennäköisyys kysytylle paksuudelle
def p_haku(H, haku):
    i = 0; #haetaan ensin lähimmäs hakua tulevat indeksit
    while H[i] < haku:
        i+=1;
    i-=1;
    #tarkennetaan interpoloimalla kahden pisteen välillä
    P = np.linspace(0,1,len(H));
    a = (P[i+1]-P[i]) / (H[i+1]-H[i]);
    b = P[i] - a*H[i];
    p = (lambda x: a*x + b)(haku)
    return p;

def plottaa(H, vari, paksuus=0, tunniste=""):
    if paksuus == 0:
        paksuus = 1.5;
    avg = np.mean(H);
    P = np.linspace(0,1,len(H))
    plt.plot(H, P, linewidth=paksuus, color=vari, label=tunniste)
    plt.scatter(avg, p_haku(H, avg), marker='o', s=50, color=vari); #keskiarvopiste

def kuvan_asetukset(otsikko):
    plt.grid('on')
    plt.title(otsikko, fontsize=15);
    plt.ylim(0,1)
    plt.ylabel('Cumulative propability',fontsize=15)
    plt.xlabel('Annual maximum ice thickness (m)',fontsize=15)
    plt.legend(ncol=1, fontsize=11, loc='lower right');
    

alkuvuosi = 1975;
loppuvuosi = 2006; #ensimmäinen, jota ei ole
ajot = ("A001", "B001", "D001");
mallikansio = "/home/aerkkila/a/pakspaikat/";
varit = ("r", "m", "c");

hnnot = t.lue_havainnot(alku=alkuvuosi, loppu=loppuvuosi);
ajotulos = [[]]*len(ajot);
for i in range(len(ajot)):
   ajotulos[i] = t.lue_malli(kansio=mallikansio, nimiloppu="_icevolume_"+ajot[i]+"_maks.txt");

plt.figure(figsize=(18,15));

for i in range(len(hnnot)):
    ax = plt.subplot(2,3,i+1);
    plottaa(hnnot[i], 'b', tunniste="observations");
    for tmp in range(len(ajot)):
        plottaa(ajotulos[tmp][i], varit[tmp], tunniste=ajot[tmp][0]+"_history");
    kuvan_asetukset(t.paikat[i]);

if 1:
    plt.show();
else:
    plt.savefig('/home/aerkkila/a/kuvat/pakskuvat_001.png');
