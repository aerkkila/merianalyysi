#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa
#jokaiselle ajolle valitaan joko gumbel- tai weibull-jakauma
#voi valita yhden kaikille (esim. g) tai kaikille erikseen (esim. gwggwg)

import numpy as np
from numpy import log, exp
from scipy.stats import linregress
from matplotlib.pyplot import *
import sys, locale
from jaettu import *

try:
    aikaikk  = int(sys.argv[1])
    lajit = sys.argv[2]
except:
    print("Käyttö: ./tämä aikaikkuna lajit(g/w) (1, jos tallenna)")
    exit()

Tn = (2, 5, 10, 30, 50) #halutut toistumisajat
#gumbel
Fg = lambda F: -log(-log(F)) #koordinaattimuunnos
xg = lambda x: x #koordinaattimuunnos
x_Fg = lambda F,a,b: (Fg(F)-b) / a #palauttaan uuden x:n kun suora on sovitettu
#weibull
Fw = lambda F: log(-log(1-F))
xw = lambda x: log(x)
x_Fw = lambda F,a,b: exp((Fw(F)-b) / a)

class Jakaumat:
    def __init__(self,lajit,ajat):
        self.todnak = 1/np.array(ajat)
        self.lajit=lajit
        while len(self.lajit) < len(ajot):
            self.lajit += self.lajit[-1]
    def __enter__(self):
        return self
    def sovita(self,x,F,aind):
        if self.lajit[aind] == 'g': #gumbel
            a, b, r, p, kkv = linregress(xg(x), Fg(F))
            return np.append(x_Fg(self.todnak,a,b), r**2)
        if self.lajit[aind] == 'w': #weibull
            a, b, r, p, kkv = linregress(xw(x), Fw(F))
            return np.append(x_Fw(self.todnak,a,b), r**2)
        else:
            print("laji oli %s" %(self.lajit[aind]))
            kautto()
    def __exit__(self,type,value,traceback):
        pass

if suomeksi:
    xnimi = 'vuosi'
    ynimi = 'pinta-ala $(km^2)$'
    ulaotsikko = 'aikaikkuna = %i vuotta' %aikaikk
else:
    xnimi = 'year'
    ynimi = 'area $(km^2)$'
    ulaotsikko = 'time window = %i years' %aikaikk

fig = figure(figsize=(12,10))
axs = fig.subplots(3,2).flatten()
ytikit = np.linspace(0,80000,9)
ynimet = ["%.i" %luku if not i%2 else '' for i,luku in enumerate(ytikit)]
F = np.array(np.arange(1,aikaikk+1) / (aikaikk+1))
jakaumat = Jakaumat(lajit,Tn)
for aind in range(len(ajot)):
    tiedos = np.loadtxt('%s/makspintaalat_%s.txt'\
                      %(kansio, ajot[aind]), usecols=[0,2])
    v0 = tiedos[0,1]
    pituus = len(tiedos)-aikaikk+1
    alat = np.zeros((pituus,len(jakaumat.todnak)+1))
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    for ind in range(pituus):
        pa = np.sort(tiedos[ind : ind+aikaikk, 0]) #valitaan aikaikkuna
        raja = len(pa) #rajataan kokonaisjäätymiset pois sovituksesta
        for tmp in range(len(pa)-1):
            if(pa[tmp] > 103000):
                raja = tmp
                break
        alat[ind,:] = jakaumat.sovita(pa[:raja],F[:raja],aind)

    sca(axs[aind])
    ylim(0,90000)
    vuodet = np.arange(v0,v0+pituus) + (aikaikk-1)//2
    plot(vuodet, alat[:,:-1], color='k')
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
    title('%s (%s)' %(ajonimet[aind], jakaumat.lajit[aind]))

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

suptitle(ulaotsikko)
tight_layout(h_pad=1)
if sys.argv[-1] == '1':
    savefig("%s/pa%s_aikasarja_toistaik.png" %(kuvat, aikaikk))
else:
    show()
