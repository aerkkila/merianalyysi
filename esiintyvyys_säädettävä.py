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
        self.ckirj = CDLL("./esiintyvyys_säädettävä.so")
        self.ckirj.esiintyvyys.restype = POINTER(c_float*365)
        self.ckirj.alusta(c_int(paiva0), c_int(vuosi0), c_int(vuosi1))
        self.tulos = np.zeros(paiva1-paiva0, dtype=float)
        self.paiva0=paiva0
        self.vuosi0=vuosi0
        self.vuosi1=vuosi1
        self.gausspit=gausspit
    def __enter__(self):
        return self
    def lue(self, konsraja, tiedosind):
        tulos = self.ckirj.esiintyvyys( c_float(konsraja),
                                        c_int(gausspit),
                                        c_int(tiedosind) )
        self.tulos = tulos.contents[0:paiva1-paiva0]
        return self.tulos
    def siirra_aikaikkunaa(self, nvuosia):
        self.ckirj.siirra_aikaikkunaa(c_int(nvuosia))
        self.vuosi0 += nvuosia
        self.vuosi1 += nvuosia
    def __exit__(self, type, value, traceback):
        self.ckirj.vapauta()

def painettaessa(tapaht):
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
    for ind in range(len(nimet)):
        lukija.lue(konsraja, ind)
        viivat[ind].set_ydata(lukija.tulos)
    locale.setlocale(locale.LC_ALL, paikallisuus)
    suptitle(locale.format_string("%i–%i; $3\sigma=$%i\n%s ≥ %4.2f",
                                  (lukija.vuosi0,lukija.vuosi1,gausspit,konsstr,konsraja)))
    draw()
    
def paivita(arvo):
    global konsraja
    for i,viiva in enumerate(viivat):
        viiva.set_ydata(lukija.lue(arvo,i))
    konsraja = arvo
    locale.setlocale(locale.LC_ALL, paikallisuus)
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
gausspit = 15

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
subplots_adjust(top=0.9)
gauss_liuku = Slider(
    ax = axes([0.1, 0.93, 0.78, 0.07]),
    label = "concentration",
    valmin=0,
    valmax=1,
    valinit=konsraja
)
gauss_liuku.on_changed(paivita)

with Lukija(paiva0, vuosi0, vuosi1, gausspit) as lukija:
    nimet = []
    viivat = []
    for pind,paikka in enumerate(paikat):
        sca(axs[pind])
        ylim((-0.05, 1.05))
        for aind,ajo in enumerate(ajot):
            nimi = "%s/peittävyydet_%s_%s.txt" %(kansio, paikat_fi[pind], ajo)
            nimet.append(nimi)
            lukija.lue(konsraja,pind*6+aind)
            viiva, = plot(xakseli, lukija.tulos, color=varit[aind], label=ajonimet[aind])
            viivat.append(viiva)
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
    suptitle(locale.format_string("%i–%i; $3\sigma=$%i\n%s ≥ %4.2f",
                                  (lukija.vuosi0,lukija.vuosi1,gausspit,konsstr,konsraja)))
    if(sys.argv[-1] == '1'):
        savefig("%s/esiintyvyys%2i_%i_%i.png" %(kuvat,int(konsraja*100),vuosi0,vuosi1))
    else:
        show()
