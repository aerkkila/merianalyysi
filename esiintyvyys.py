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
    print("Käyttö: ./tämä konsraja alkuvuosi loppuvuosi (1, jos tallenna)")
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
        self.tulos = tulos[0:paiva1-paiva0]
        return self.tulos
    def siirra_aikaikkunaa(self, nvuosia):
        self.ckirj.siirra_aikaikkunaa(c_int(nvuosia))
        self.vuosi0 += nvuosia
        self.vuosi1 += nvuosia
    def __exit__(self, type, value, traceback):
        self.ckirj.vapauta()

def painettaessa(tapaht):
    global nimet, lukija, konsraja, viivat
    if tapaht.key == 'left':
        nvuosia = -1
    elif tapaht.key == 'right':
        nvuosia = 1
    elif tapaht.key == 'down':
        nvuosia = -5
    elif tapaht.key == 'up':
        nvuosia = 5
    else:
        return
    lukija.siirra_aikaikkunaa(nvuosia)
    tulos = []
    for ind,nimi in enumerate(nimet):
        lukija.lue(nimi, konsraja)
        viivat[ind].set_ydata(lukija.tulos)
    suptitle(locale.format_string("%i–%i; $3\sigma=$%i\n%s ≥ %4.2f",
                                  (lukija.vuosi0,lukija.vuosi1,gausspit,konsstr,konsraja)))
    draw()

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
gausspit = 12

if suomeksi:
    konsstr = 'peittävyys'
else:
    konsstr = 'concentration'

fig = figure(figsize=(12,10))
axs = fig.subplots(3,2).flatten()
xtikit = np.arange(-50,151,12.5)
ajat = pd.to_datetime(xtikit, unit='D')
locale.setlocale(locale.LC_ALL, paikallisuus)
xnimet = ajat.strftime("%e. %b")
fig.canvas.mpl_connect('key_press_event', painettaessa)

ytikit = np.linspace(0,1,11)
locale.setlocale(locale.LC_ALL, paikallisuus)
ynimet = [locale.format_string("%.1f",luku) if not i%2 else '' for i,luku in enumerate(ytikit)]

with Lukija(paiva0, vuosi0, vuosi1, gausspit) as lukija:
    nimet = []
    viivat = []
    for pind,paikka in enumerate(paikat):
        sca(axs[pind])
        ylim((-0.05, 1.05))
        for aind,ajo in enumerate(ajot):
            nimi = "%s/peittävyydet_%s_%s.txt" %(kansio, paikat_fi[pind], ajo)
            nimet.append(nimi)
            lukija.lue(nimi, konsraja)
            viiva, = plot(xakseli, lukija.tulos, color=varit[aind], label=ajonimet[aind])
            viivat.append(viiva)
        grid('on')
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit(0,1)
        xticks(xtikit, xnimet, rotation=45, fontsize=11)
        yticks(ytikit, ynimet, fontsize=12)
        if(paikka != 'Kemi'):
            legend(loc='upper right',frameon=False, fontsize=10)
        else:
            legend(loc='lower center',frameon=False, fontsize=10)
        title(paikka)
        #50 päivän välein korostettu viiva
        viivat = axs[pind].xaxis.get_gridlines()
        for i,g in enumerate(viivat):
            if i%4==0:
                g.set_linewidth(1.5)
                g.set_color('k')
                
        viivat=axs[pind].yaxis.get_gridlines()
        for i,viiva in enumerate(viivat):
            if not i%2:
                pass
            elif any((1,5,9)[j] == i for j in range(3)):
                viiva.set_linestyle(':')
            else:
                viiva.set_linestyle('none')
            suptitle(locale.format_string("%i–%i; %s ≥ %4.2f",
                                          (lukija.vuosi0,lukija.vuosi1,konsstr,konsraja)))
    tight_layout()
    if(sys.argv[-1] == '1'):
        savefig("%s/esiintyvyys%2i_%i_%i.png" %(kuvat,int(konsraja*100),vuosi0,vuosi1))
    else:
        show()
