#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa
#valitaan joka hetkelle Weibull- tai Gumbel-jakauma sen mukaan,
# kummassa on suurempi selittävyysaste

import numpy as np
from numpy import log, exp
from scipy.stats import linregress
from matplotlib.pyplot import *
import sys, locale
from jaettu import *

try:
    aikaikk  = int(sys.argv[1])
except:
    print("Käyttö: ./tämä aikaikkuna (1, jos tallenna)")
    exit()

Tn = (2, 5, 10, 30, 50) #halutut toistumisajat
#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista

#gumbel
Fg = lambda F: -log(-log(F))
xg = lambda x: x
pa_Tg = lambda T,a,b: (Fg(1/T)-b) / a
#weibull
Fw = lambda F: log(-log(1-F))
xw = lambda x: log(x)
pa_Tw = lambda T,a,b: exp((Fw(1/T)-b) / a)

if suomeksi:
    xnimi = 'vuosi'
    ynimi = 'pinta-ala $(km^2)$'
    ulaotsikko = 'aikaikkuna = %i vuotta' %(aikaikk)
else:
    xnimi = 'year'
    ynimi = 'area $(km^2)$'
    ulaotsikko = 'time window = %i years' %(aikaikk)
    
if(aikaikk < 0):
    aikaikk = len(tiedos)
fig = figure(figsize=(12,10))
axs = fig.subplots(3,2).flatten()
ytikit = np.linspace(0,80000,9)
ynimet = ["%.i" %luku if not i%2 else '' for i,luku in enumerate(ytikit)] #joka toiselle viivalle y-akselin arvo
for aind,ajo in enumerate(ajot):
    tiedos = np.loadtxt('%s/makspintaalat_%s.txt' %(kansio, ajo), usecols=(0,2))
    v0 = tiedos[0,1]
    paramg = np.zeros((len(tiedos)-aikaikk+1,4))
    paramw = np.zeros_like(paramg)
    
    #muodostetaan juokseva aikasarja, jossa on kerrallaan mukana n vuotta
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    ind = 0
    gumbelko = np.zeros(len(tiedos)-aikaikk+1, dtype=bool)
    for ind in range(len(tiedos)-aikaikk+1):
        pa = np.sort(tiedos[ind : ind+aikaikk, 0]) #valitaan aikaikkuna
        F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0) #kokeellinen kertymäfunktio

        #rajataan kokonaisjäätymiset pois sovituksesta
        raja = len(pa)
        for tmp in range(len(pa)-1):
            if(pa[tmp] > 103000):
                raja = tmp
                break

        #suorien sovitus sekä molempien suorien parametrien ja vuoden tallentaminen
        a, b, r, p, kkv = linregress(xg(pa[0:raja]), Fg(F[0:raja]))
        vuosi = v0+ind+(aikaikk-1)//2
        paramg[ind,:] = [a,b,r**2,vuosi]
        a, b, r, p, kkv = linregress(xw(pa[0:raja]), Fw(F[0:raja]))
        vuosi = v0+ind+(aikaikk-1)//2
        paramw[ind,:] = [a,b,r**2,vuosi]

        gumbelko[ind] = paramg[ind,2] >= paramw[ind,2]
    
    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä ovat kaikki vuodet
    alatw = np.zeros(len(tiedos)-aikaikk+1) + np.nan
    alatg = np.zeros_like(alatw) + np.nan
    sca(axs[aind])
    weibulko = np.invert(gumbelko)
    for T in Tn:
        alatg[gumbelko] = pa_Tg(T,paramg[gumbelko,0],paramg[gumbelko,1])
        alatw[weibulko] = pa_Tw(T,paramw[weibulko,0],paramw[weibulko,1])
        plot(paramw[:,3], alatg, color='r')
        plot(paramw[:,3], alatw, color='b')
    
    ylim(0,90000)
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
    if 1:
        ax2 = gca().twinx()
        vari = 'lightskyblue'
        ax2.plot(paramg[:,3], paramg[:,2], color='lightsalmon')
        ax2.plot(paramw[:,3], paramw[:,2], color=vari)
        ylabel('$r^2$', rotation=0, fontsize=15, color=vari)
        yticks(fontsize=13, color=vari)
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit(0,1)
        ylim([0.85, 1])

suptitle(ulaotsikko)
tight_layout(h_pad=1)
if sys.argv[-1] == '1':
    savefig("%s/pa_%s_aikasarja_toistaik_vaiht_%i.png" %(kuvat, laji, aikaikk))
else:
    show()
