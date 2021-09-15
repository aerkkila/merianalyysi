#!/usr/bin/python3

import numpy as np
import pandas as pd
from matplotlib.pyplot import *
from jaettu import *
from ctypes import *
import sys, os, locale

def kautto(virheviesti=''):
    if(len(virheviesti)):
        print("Virhe: %s" %virheviesti)
    print("Käyttö: ./tämä konsraja alkuvuosi loppuvuosi")
    exit()

class Lukija:
    def __init__(self, paiva0, vuosi0, vuosi1, gausspit):
        self.ckirj = CDLL("./esiintyvyys.so")
        self.ckirj.esiintyvyys.restype = POINTER(c_float*365)
        self.ckirj.alusta(c_int(paiva0), c_int(vuosi0), c_int(vuosi1))
        self.tulos = np.zeros(paiva1-paiva0, dtype=float)
        self.paiva0=paiva0
        self.vuosi0=vuosi0
        self.vuosi1=vuosi1
        self.gausspit=gausspit
    def __enter__(self):
        return self
    def lue(self, tiednimi, konsraja):
        tulos = self.ckirj.esiintyvyys( c_char_p(tiednimi.encode('utf-8')),
                                        c_float(konsraja),
                                        c_int(gausspit) )
        tulos = tulos.contents
        for i in range(paiva1-paiva0):
            self.tulos[i] = tulos[i]
        return self.tulos
    def __exit__(self, type, value, traceback):
        self.ckirj.vapauta()

try:
    konsraja = float(sys.argv[1])
    vuosi0 = int(sys.argv[2])
    vuosi1 = int(sys.argv[3])
except Exception as e:
    kautto(str(e))

#kuvaajan aikaväli olkaan 1.11. – 15.6.
paiva0 = -61
paiva1 = 166
xakseli = np.arange(paiva0, paiva1)
gausspit = 15

fig = figure(figsize=(12,10))
axs = fig.subplots(3,2).flatten()
xtikit = np.arange(-50,151,12.5)
ajat = pd.to_datetime(xtikit, unit='D')
#figure() vaihtaa paikallistamiseen oletusasetukset
locale.setlocale(locale.LC_ALL, paikallisuus)
xnimet = ajat.strftime("%e. %b")

with Lukija(paiva0, vuosi0, vuosi1, gausspit) as lukija:
    for pind,paikka in enumerate(paikat):
        sca(axs[pind])
        ylim((-0.05, 1.05))
        for aind,ajo in enumerate(ajot):
            nimi = "%s/peittävyydet_%s_%s.txt" %(kansio, paikat_fi[pind], ajo)
            lukija.lue(nimi, konsraja)
            plot(xakseli, lukija.tulos, color=varit[aind], label=ajonimet[aind])
        grid('on')
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit(0,1)
        xticks(xtikit, xnimet, rotation=45, fontsize=11)
        yticks(fontsize=12)
        if(paikka != 'Kemi'):
            legend(loc='upper right',frameon=False, fontsize=10)
        else:
            legend(loc='lower center',frameon=False, fontsize=10)
        title(paikka)
        #50 päivän välein korostettu viiva
        gridx = axs[pind].xaxis.get_gridlines()
        for i,g in enumerate(gridx):
            if i%4==0:
                g.set_linewidth(1.5)
                g.set_color('k')
    suptitle("%i–%i; $3\sigma=$%i" %(vuosi0,vuosi1,gausspit))
    tight_layout()
    show()
