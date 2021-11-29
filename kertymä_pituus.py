#!/usr/bin/python3

kautto = "Käyttö: ./tämä alkuvuosi loppuvuosi(otetaan mukaan) konsraja*100 (1, jos tallenna kuva)"

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
import locale, sys
import matplotlib.ticker as ticker
from jaettu import *

if suomeksi:
    xnimi = 'Jäätalven pituus (päivää)'
    ynimi = 'Todennäköisyyskertymä'
    konsrajasana = 'peittävyysraja'
else:
    xnimi = 'Number of ice days'
    ynimi = 'Probability'
    konsrajasana = 'concentration limit'
    
if len(sys.argv) < 3:
    print(kautto)
    exit()
try:
    vuosi0 = int(sys.argv[1])
    vuosi1 = int(sys.argv[2])
    knsraj = int(sys.argv[3])
except Exception as e:
    print(str(e))
    print(kautto)
    exit()
    
nimialku = 'pituus%i' %knsraj

fig = plt.figure(figsize=(12,10))
ytikit = np.linspace(0,1,11)
locale.setlocale(locale.LC_ALL, paikallisuus)
ynimet = [locale.format_string("%.1f",luku) if not i%2 else '' for i,luku in enumerate(ytikit)]
for pind,p in enumerate(paikat_fi):
    ax = plt.subplot(3,2,pind+1)
    
    for aind,a in enumerate(ajot):
        tiednimi = '%s/%s_%s_%s.txt' %(kansio, nimialku, p, a)
        tiedos = np.loadtxt(tiednimi, usecols=(0,2))
        tiedos = rajaa(tiedos, vuosi0, vuosi1)
        tiedos = np.sort(tiedos[:,0])
        y = 1 - np.array(range(1,len(tiedos)+1)) / (len(tiedos)+1.0)
        plt.plot(tiedos, y, color=varit[aind], label=ajonimet[aind])

    plt.grid('on')
    plt.yticks(ticks=ytikit, labels=ynimet, fontsize=13)
    viivat=ax.yaxis.get_gridlines()
    for i,viiva in enumerate(viivat):
        if i%2:
            viiva.set_linestyle(':')
    plt.title(paikat[pind], fontsize=15)
    plt.ylim(0,1)
    plt.xlim(0,180)
    plt.ylabel(ynimi, fontsize=15)
    plt.xlabel(xnimi, fontsize=15)
    plt.xticks(fontsize=13)
    if(p=='Nordmaling'):
        plt.legend(fontsize=13, frameon=0)
fig.suptitle(locale.format_string
             ("%i–%i; %s = %.2f", (vuosi0,vuosi1,konsrajasana,knsraj/100)),
             fontsize=18)
plt.tight_layout()

if sys.argv[-1]=='1':
    plt.savefig('%s/%s_kert%i_%i.png' %(kuvat,nimialku,vuosi0,vuosi1))
else:
    plt.show()
