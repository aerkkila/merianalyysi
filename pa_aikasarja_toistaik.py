#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa
#gumbelsuoran termit luetaan tiedostoista,
#jotka tehdään ohjelmalla laske_gumbkertoimet.py

import numpy as np
import scipy.stats as st
from matplotlib.pyplot import *
import sys
from jaettu import *

aikaikk = 40
tallenna = 0
try:
    luku = int(sys.argv[1])
    if(luku < 2):
        tallenna = luku
    else:
        aikaikk = luku
except:
    pass
try:
    luku = int(sys.argv[2])
    if(luku < 2):
        tallenna = luku
    else:
        aikaikk = luku
except:
    pass

Tn = [2, 5, 10, 30, 50] #halutut toistumisajat
#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista
pa_l = lambda T,a,b: (-np.log(-np.log(1/T))-b) / a

if suomeksi:
    xnimi = 'vuosi'
    ynimi = 'pinta-ala $(km^2)$'
    ulaotsikko = 'aikaikkuna = %i vuotta' %aikaikk
else:
    xnimi = 'year'
    ynimi = 'area $(km^2)$'
    ulaotsikko = 'time window = %i years' %aikaikk

figure(figsize=(12,10))
for aind in range(len(ajot)):
    tiedos = np.loadtxt('%s/pintaalat_%s_maks.txt'\
                      %(tiedokset, ajot[aind]), usecols=[0,2])
    if(aikaikk < 0):
        aikaikk = len(tiedos)
    v0 = tiedos[0,1]
    param = np.zeros((len(tiedos)-aikaikk+1,3))
    
    #muodostetaan juokseva aikasarja, jossa on kerrallaan mukana n vuotta
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    ind = 0
    while 1:
        pa = np.sort(tiedos[ind : ind+aikaikk, 0]) #valitaan aikaikkuna
        F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0) #kokeellinen kertymäfunktio

        #rajataan ei-huomioitaviksi suoran sovituksessa kokonaisjäätymiset
        raja = len(pa)
        for tmp in range(len(pa)-1):
            if(pa[tmp] > 103000):
                raja = tmp
                break

        F = -1*np.log(-1*np.log(F)) #muunnos gumbelkoordinaatistoon

        #suoran sovitus sekä suoran parametrien ja vuoden tallentaminen
        a, b, r, p, kkv = st.linregress(pa[0:raja], F[0:raja])
        vuosi = v0+ind+(aikaikk-1)//2
        param[ind,:] = [a,b,vuosi]

        ind += 1
        if (ind+aikaikk > len(tiedos)):
            break
    
    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä ovat kaikki vuodet
    A = [[]]*len(Tn)
    tmp = 0
    for T in Tn:
        A[tmp] = pa_l(T,param[:,0],param[:,1])
        tmp+=1
    A = np.array(A)
    A = A.transpose()

    subplot(3,2,aind+1)
    plot(param[:,2], A, color='k')
    grid('on')
    xlabel(xnimi, fontsize=15)
    ylabel(ynimi, fontsize=15)
    yticks(fontsize=13)
    xticks(fontsize=13)
    title('%s' %(ajonimet[aind]))

suptitle(ulaotsikko)
tight_layout(h_pad=1)
if tallenna:
    savefig("%s/pa_viivat_%i.png" %(kuvat, aikaikk))
else:
    show()
