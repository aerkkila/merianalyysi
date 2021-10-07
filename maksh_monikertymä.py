#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
from numpy import log, exp
import scipy.stats as st
import sys, locale, pylab
import matplotlib.ticker as ticker
from jaettu import *

sovitus = 'pns'

def kautto():
    print("Käyttö: ./tämä alkuvuosi loppuvuosi laji(g/f/w) (1, jos tallenna)")
    exit()

try:
    vuosi0 = int(sys.argv[1])
    vuosi1 = int(sys.argv[2])
    lajit = sys.argv[3]
except Exception as e:
    print(str(e))
    kautto()

if len(lajit) > 3 and lajit[-4:] == '.txt':
    with open(lajit) as f:
        tied = f.read()
    lajit = ''
    for c in tied:
        if c == 'w' or c == 'g' or c == 'f':
            lajit += c
    if(len(lajit) != len(ajot)*len(paikat)):
        printf("Varoitus, luettiin %i lajia %i:n sijaan" %(len(lajit), len(ajot)*len(paikat)))

def valitse_yhtalot(laji):
    global Fm, xm, Fpalaute
    if laji == 'g': #gumbel
        Fm = lambda F: -log(-log(F))
        xm = lambda x: x
        Fpalaute = lambda x: exp(-exp(-a*x-b))
    elif laji == 'f': #fréchet
        Fm = lambda F: log(-log(F))
        xm = lambda x: log(x+1e-7)
        Fpalaute = lambda x: exp(-x**a*exp(b))
    elif laji == 'w': #weibull
        Fm = lambda F: log(-log(1-F))
        xm = lambda x: log(x+1e-7)
        Fpalaute = lambda x: 1-exp(-x**a*exp(b))
    else:
        printf("Laji oli %s" %laji)
        kautto()

for pind,paikka in enumerate(paikat):
    fig=pylab.figure(num=pind,figsize=(10,10))
    axs = fig.subplots(4,3).flatten(order='F')
    for aind,ajo in enumerate(ajot):
        tiedos = np.genfromtxt("%s/maksh_%s_%s.txt" %(kansio,paikat_fi[pind],ajo), usecols=(0,2),dtype=np.float64)
        try:
            tiedos = rajaa(tiedos, vuosi0, vuosi1)
        except Exception as e:
            print(str(e))
            kautto()
        i = 0
        suure = np.sort(tiedos[:,0])
        F = np.array(range(1,len(suure)+1)) / (len(suure)+1.0)

        raja = len(suure)
        for i,s in enumerate(suure):
            if(suure[i] > 1): #aivan pieniä paksuuksia ei huomioida
                raja = i
                break

        laji_ind = pind*len(ajot) + aind if len(lajit) > 1 else 0
        valitse_yhtalot(lajit[laji_ind])
        F1 = Fm(F)
        x1 = xm(suure)
        if sovitus == 'pns':
            if 1:
                a,b,r,p,kkv = st.linregress(F1[raja:], x1[raja:]) #sovitetaan väärin päin, jotta neliösumma minimoidaan x-suunnassa
                b = -b/a
                a = 1/a
            else:
                a,b,r,p,kkv = st.linregress(x1[raja:], F1[raja:])
            print(a,b)
        elif sovitus == 'ts':
            ts = st.mstats.theilslopes(F1[raja:], x1[raja:])
            a = ts[0]
            b = ts[1]
            r = 0
        else:
            printf("Tuntematon sovitusmenetelmä: %s" %sovitus)
            exit()

        sca(axs[aind*2])
        plot(x1[raja:], F1[raja:], '.', color='deepskyblue')
        plot(x1[:raja], F1[:raja], '.', color='r')
        xraja0 = xlim()[0]
        xraja1 = xlim()[1]
        xviiva = np.linspace(xraja0, xraja1, 200)
        plot(xviiva, a*xviiva+b, color='olive')
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit()
        title(locale.format_string("%s (%s); $r^2$ = %.4f", (ajonimet[aind], lajit[laji_ind], r**2)))
    
        sca(axs[aind*2+1])
        plot(suure[raja:], F[raja:], '.', color='deepskyblue')
        plot(suure[:raja], F[:raja], '.', color='r')
        xraja0 = xlim()[0]
        xraja1 = xlim()[1]
        if xraja0 <= 0:
            xraja0 = 0.001 
        xviiva = np.linspace(xraja0, xraja1, 200)
        plot(xviiva, Fpalaute(xviiva), color='olive')
        title(locale.format_string("%s; $σ_{res}$ = %.3f", (ajonimet[aind], np.std(F[raja:]-Fpalaute(suure[raja:])))))
    
    paikallista_akselit()
    suptitle(paikka)
    tight_layout()
if sys.argv[-1] == '1':
    for i in range(len(paikat)):
        pylab.figure(i)
        savefig("testi_%s_%s.png" %(paikat_fi[i], lajit if len(lajit) == 1 else ''))
else:
    show()
