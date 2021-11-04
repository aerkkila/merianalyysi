#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa

import numpy as np
from numpy import log, exp
from scipy.interpolate import interp1d
from matplotlib.pyplot import *
import sys, locale, argparse
from jaettu import *

pars = argparse.ArgumentParser()
pars.add_argument('-a', '--aikaikk', type=int, default=45,
                  help='Monestako vuodesta todennäköisyydet määritetään')
pars.add_argument('-s', '--tallenna', type=int, default=0, const=1, nargs='?',
                  help='Tallenna luotu kuva')
args = pars.parse_args()

Tn = (1.11111, 2, 5, 10, 30) #halutut toistumisajat
p_Tn = np.empty(len(Tn))
for i in range(len(p_Tn)):
    p_Tn[i] = 1/Tn[i]

if suomeksi:
    xnimi = 'vuosi'
    ynimi = 'jään laajuus ($\mathrm{km^2}$)'
    ulaotsikko = 'aikaikkuna = %i vuotta' %args.aikaikk
else:
    xnimi = 'year'
    ynimi = 'ice extent ($\mathrm{km^2}$)'
    ulaotsikko = 'time window = %i years' %args.aikaikk

fig = figure(figsize=(12,10))
axs = fig.subplots(3,2).flatten()
ytikit = np.linspace(0,100000,11)
ynimet = ["%.i" %luku if not i%2 else '' for i,luku in enumerate(ytikit)]
p_aikaikk = np.arange(1,args.aikaikk+1) / (args.aikaikk+1)
for aind in range(len(ajot)):
    tiedos = np.loadtxt('%s/makslaajuudet_%s.txt'\
                      %(kansio, ajot[aind]), usecols=[0,2])
    v0 = tiedos[0,1]
    pituus = len(tiedos)-args.aikaikk+1
    alat = np.zeros((pituus,len(Tn))) #aikasarja, todennäköisyys
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    for ind in range(pituus):
        pa = np.sort(tiedos[ind : ind+args.aikaikk, 0]) #valitaan aikaikkuna
        inter = interp1d(p_aikaikk, pa, kind='cubic')
        alat[ind,:] = inter(p_Tn)

    sca(axs[aind])
    ylim(0,100000)
    vuodet = np.arange(v0,v0+pituus) + (args.aikaikk-1)//2
    plot(vuodet, alat[:,0], color='r')
    plot(vuodet, alat[:,1:], color='k')
    grid('on')
    yticks(ticks=ytikit, labels=ynimet, fontsize=13)
    viivat=gca().yaxis.get_gridlines()
    for i,viiva in enumerate(viivat):
        if not i%2:
            viiva.set_color('k')
        else:
            viiva.set_linestyle(':')
    xlabel(xnimi, fontsize=15)
    ylabel(ynimi, fontsize=15)
    xticks(fontsize=13)
    title('%s' %(ajonimet[aind]))

#r^2 oikealle y-akselille
    if 0:
        ax2 = gca().twinx()
        vari = 'lightskyblue'
        ax2.plot(vuodet, alat[:,-1], color=vari)
        ylabel('$r^2$', rotation=0, fontsize=15, color=vari)
        yticks(fontsize=13, color=vari)
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit(0,1)
        ylim([0.85, 1])

#suptitle(ulaotsikko)
tight_layout(h_pad=1)
if sys.argv[-1] == '1':
    savefig("%s/pa%s_aikasarja_toistaik.png" %(kuvat, args.aikaikk))
else:
    show()
