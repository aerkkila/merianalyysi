#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
from numpy import log, exp
import scipy.stats as st
import sys, locale
import matplotlib.ticker as ticker
from jaettu import *

def kautto():
    print("Käyttö: ./tämä alkuvuosi loppuvuosi laji(g/f/w) (1, jos tallenna)")
    exit()

try:
    vuosi0 = int(sys.argv[1])
    vuosi1 = int(sys.argv[2])
    laji = sys.argv[3]
except Exception as e:
    print(str(e))
    kautto()

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
    kautto()

for pind,paikka in enumerate(paikat):
    fig=figure(num=pind,figsize=(10,10))
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

        F1 = Fm(F)
        x1 = xm(suure)
        a,b,r,p,kkv = st.linregress(x1[raja:], F1[raja:])

        sca(axs[aind*2])
        plot(x1[raja:], F1[raja:], '.', color='deepskyblue')
        plot(x1[:raja], F1[:raja], '.', color='r')
        xrajat = xlim()
        xviiva = np.linspace(xrajat[0], xrajat[1], 200)
        plot(xviiva, a*xviiva+b, color='olive')
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit()
        title(locale.format_string("%s; $r^2$ = %.4f", (ajonimet[aind], r**2)))
    
        sca(axs[aind*2+1])
        plot(suure[raja:], F[raja:], '.', color='deepskyblue')
        plot(suure[:raja], F[:raja], '.', color='r')
        xraja0 = xlim()[0]
        xraja1 = xlim()[1]
        if xraja0 <= 0:
            xraja0 = 0.01 
        xviiva = np.linspace(xraja0, xraja1, 200)
        plot(xviiva, Fpalaute(xviiva), color='olive')
        title(locale.format_string("%s; $σ_{res}$ = %.3f", (ajonimet[aind], np.std(F[raja:]-Fpalaute(suure[raja:])))))
       
    paikallista_akselit()
    suptitle(paikka)
    tight_layout()
if sys.argv[-1] == '1':
    savefig("testi_%s.png" %paikat_fi[pind])
else:
    show()

