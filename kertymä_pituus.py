#!/usr/bin/python3

kautto = "Käyttö: ./tämä alkuvuosi loppuvuosi (1, jos tallenna kuva)"

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
import locale, sys
import matplotlib.ticker as ticker
from jaettu import *

if suomeksi:
    xnimi = 'Jäätalven pituus (päivää)'
    ynimi = 'Todennäköisyyskertymä'
else:
    xnimi = 'Ice season length (days)'
    ynimi = 'Cumulative propability'

if len(sys.argv) < 3:
    print(kautto)
    exit()
nimialku = 'pituus'
try:
    vuosi0 = int(sys.argv[1])
    vuosi1 = int(sys.argv[2])
except Exception as e:
    print(str(e))
    print(kautto)
    exit()

fig = plt.figure(figsize=(12,10))
for pind,p in enumerate(paikat_fi):
    ax = plt.subplot(3,2,pind+1)
    
    for aind,a in enumerate(ajot):
        tiednimi = '%s/%s_%s_%s.txt' %(kansio, nimialku, p, a)
        tiedos = np.loadtxt(tiednimi, usecols=(0,2))
        tiedos = rajaa(tiedos, vuosi0, vuosi1)
        tiedos = np.sort(tiedos[:,0])
        F = np.array(range(1,len(tiedos)+1)) / (len(tiedos)+1.0) #kertymäfunktio
        plt.plot(tiedos, F, color=varit[aind], label=ajonimet[aind])

    plt.grid('on')
    plt.title(paikat[pind], fontsize=15)
    locale.setlocale(locale.LC_ALL, paikallisuus)
    paikallista_akselit()
    plt.ylim(0,1)
    plt.xlim(0,180)
    plt.ylabel(ynimi, fontsize=15)
    plt.xlabel(xnimi, fontsize=15)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)
    plt.legend(fontsize=11, frameon=0)
fig.suptitle("%i–%i"%(vuosi0,vuosi1), fontsize=18)
plt.tight_layout()

if sys.argv[-1]=='1':
    plt.savefig('%s/%s_kert%i_%i.png' %(kuvat,nimialku,vuosi0,vuosi1))
else:
    plt.show()
