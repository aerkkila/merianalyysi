#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
from numpy import log, exp
from scipy.stats import linregress
import locale, sys, argparse
import matplotlib.ticker as ticker
from jaettu import *

if suomeksi:
    xnimi = 'Paksuuden vuosimaksimi (cm)'
    ynimi = 'Todennäköisyyskertymä'
else:
    xnimi = 'Maximum thickness (cm)'
    ynimi = 'Cumulative propability'

pars = argparse.ArgumentParser()
pars.add_argument('-v0', '--vuosi0', type=int, default=2052,
                  help='Ensimmäinen mukaan otettava vuosi')
pars.add_argument('-v1', '--vuosi1', type=int, default=2097,
                  help='Viimeinen mukaan otettava vuosi')
pars.add_argument('-l', '--lajit', default='maksh_loppulajit.txt',
                  help='Mikä jakauma sovitetaan (w/g/f/ø): Weibull, Gumbel, Fréchet tai ei mikään. Voi antaa yhden lajin, jota käytetään kaikkiin tai jokaiselle eri lajin järjestyksessä paikka,ajo: gwwwgfwwø... tai .txt-päätteisen tiedoston nimen, jossa on lueteltu lajit tuossa järjestyksessä. Tiedostosta luetaan vain nuo kirjaimet (gwfø) ja seassa saa olla muutakin.')
pars.add_argument('-h0', '--paksraja', type=float, default=1.0,
                  help='Vain tätä suuremmat arvot huomioidaan jakauman sovituksessa.')
pars.add_argument('-t', '--tallenna', nargs='?', type=int, const=1, default=0,
                  help='Tallennetaanko kuvat (0/1), oletus on ei. Pelkkä --tallenna riittää myös ilman argumenttia')
ar = pars.parse_args()
nimialku = 'maksh'

def valitse_yhtalot(laji):
    global Fm, xm, Fpalaute
    if laji == 'g': #gumbel
        Fm = lambda F: -log(-log(F))
        xm = lambda x: x
        Fpalaute = lambda x: exp(-exp(-a*x-b))
    elif laji == 'γ': #gumbel**2
        Fm = lambda F: -log(-log(F))
        xm = lambda x: x**2
        Fpalaute = lambda x: exp(-exp(-a*x**2-b))
    elif laji == 'f': #fréchet
        Fm = lambda F: log(-log(F))
        xm = lambda x: log(x+1e-7)
        Fpalaute = lambda x: exp(-x**a*exp(b))
    elif laji == 'w': #weibull
        Fm = lambda F: log(-log(1-F))
        xm = lambda x: log(x+1e-7)
        Fpalaute = lambda x: 1-exp(-x**a*exp(b))
    elif laji == 'ø': #ei mitään
        Fm = lambda F: F
        xm = lambda x: x
        Fpalaute = lambda x: F
    else:
        print("Virheellinen laji: %s" %laji)

def hae_raja(xtiedos, hraja):
    for i,t in enumerate(xtiedos):
        if t > hraja:
            return i
    return len(xtiedos)

if len(ar.lajit) > 3 and ar.lajit[-4:] == '.txt':
    with open(ar.lajit) as f:
        tied = f.read()
    ar.lajit = ''
    for c in tied:
        if c == 'w' or c == 'g' or c == 'f' or c == 'ø' or c == 'γ':
            ar.lajit += c
    if(len(ar.lajit) != len(ajot)*len(paikat)):
        print("Varoitus, luettiin %i lajia %i:n sijaan" %(len(ar.lajit), len(ajot)*len(paikat)))

F = np.array(range(1,ar.vuosi1-ar.vuosi0+2)) / (ar.vuosi1-ar.vuosi0+2.0) #kertymäfunktio

fig = plt.figure(figsize=(12,10))
for pind,paikka in enumerate(paikat_fi):
    ax = plt.subplot(3,2,pind+1)
    plt.xlim(-0.7,100)
    for aind,ajo in enumerate(ajot):
        tiednimi = '%s/%s_%s_%s.txt' %(kansio, nimialku, paikka, ajo)
        tiedos = np.loadtxt(tiednimi, usecols=(0,2))
        tiedos = rajaa(tiedos, ar.vuosi0, ar.vuosi1)
        tiedos = np.sort(tiedos[:,0])
        laji = ar.lajit[(pind*len(ajot)+aind) if len(ar.lajit) > 1 else 0]
        valitse_yhtalot(laji)
        if(laji=='ø'):
            plt.plot(tiedos, F, color=varit[aind], label=ajonimet[aind])
            continue
        plt.plot(tiedos, F, '.', color=varit[aind], markersize=1.5)
        F1 = Fm(F); x1 = xm(tiedos)
        raja = hae_raja(tiedos, ar.paksraja)
        a,b,r,p,kkv = linregress(F1[raja:], x1[raja:]) #pienin neliösumma x-suunnassa
        b = -b/a
        a = 1/a
        xlinsp = np.linspace(0.1,xlim()[1],200)
        plt.plot(xlinsp, Fpalaute(xlinsp), color=varit[aind], label=ajonimet[aind] + ' (%s)' %laji)

    plt.grid('on')
    plt.title(paikat[pind], fontsize=15)
    locale.setlocale(locale.LC_ALL, paikallisuus)
    paikallista_akselit()
    plt.ylim(0,1)
    plt.ylabel(ynimi, fontsize=15)
    plt.xlabel(xnimi, fontsize=15)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)
    plt.legend(fontsize=9, frameon=0)
fig.suptitle("%i–%i"%(ar.vuosi0,ar.vuosi1), fontsize=16)
plt.tight_layout()

if ar.tallenna:
    plt.savefig('%s/%s_kert%i_%i.png' %(kuvat,nimialku,ar.vuosi0,ar.vuosi1))
else:
    plt.show()
