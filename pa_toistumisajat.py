#!/usr/bin/python3

import numpy as np
from numpy import log, exp
from matplotlib.pyplot import *
from scipy.stats import linregress
import sys
from jaettu import *

def kautto():
    print("Käyttö: ./tämä alkuvuosi loppuvuosi(otetaan mukaan) laji(g/w) (1, jos tallenna)")
    exit()

if suomeksi:
    xnimi = "toistumisaika (vuotta)"
    ynimi = "pinta-ala $(km^2)$"
else:
    xnimi = 'Time interval (years)'
    ynimi = 'Extent $(\mathrm{km}^2)$'
try:
    vuosi0 = int(sys.argv[1])
    vuosi1 = int(sys.argv[2])
    laji = sys.argv[3]
except:
    kautto()
    
if laji == 'g': #gumbel
    Fm = lambda F: -log(-log(F))
    xm = lambda x: x
    pa_T = lambda T: (Fm(1/T)-b) / a
elif laji == 'w': #weibull
    Fm = lambda F: log(-log(1-F))
    xm = lambda x: log(x)
    pa_T = lambda T: exp((Fm(1/T)-b) / a)
else:
    kautto()

T0 = 1.005
T1 = 100

#pinta-alat kaikista toistumisajoista
#a ja b ovat taulukoita, joten tässä ovat kaikki ajot
Ttaul = np.geomspace(T0, T1, num=200)

fig2 = figure(2,figsize=(6,4))
sp2 = fig2.add_subplot(111)
fig1 = figure(1,figsize=(10,8))
for aind,ajo in enumerate(ajot):
    
    #luetaan tulokset
    tiedos = np.loadtxt('%s/makspintaalat_%s.txt' %(kansio,ajo), usecols=(0,2))
    try:
        tiedos = rajaa(tiedos, vuosi0, vuosi1)
    except Exception as e:
        print(str(e))
        exit()
    pa = np.sort(tiedos[:,0])
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0)
    Tpiste = 1/F
    
    #rajataan suoran sovituksesta pois kokonaisjäätymiset
    raja = len(pa)
    for tmp in range(len(pa)-1):
        if(pa[tmp] > 103000):
            raja = tmp
            break
    F1 = Fm(F)
    x1 = xm(pa)
    a, b, r, p, kkv = linregress(x1[0:raja], F1[0:raja])
    
    pa_sovitus = pa_T(Ttaul)
    fig1.add_subplot(3,2,aind+1)
    plot(Tpiste, pa, 'o', markersize=3, color='deepskyblue')
    plot(Ttaul, pa_sovitus, color='r')
    ylim(top=105000)
    xscale('log',base=10)
    title(ajonimet[aind])
    xlabel(xnimi, fontsize=11)
    ylabel(ynimi, fontsize=11)
    sp2.plot(Ttaul, pa_sovitus, color=varit[aind], label=ajonimet[aind])

suptitle('%i–%i' %(vuosi0, vuosi1))
tight_layout(h_pad=1)

figure(2)
#title('%i–%i' %(vuosi0, vuosi1))
xlabel(xnimi, fontsize=14)
ylabel(ynimi, fontsize=14)
xticks(fontsize=14)
yticks(fontsize=14)
legend(fontsize=13)
tight_layout()
ylim(top=105000)
if sys.argv[-1] == '1':
    figure(2)
    savefig('%s/pa_%stoistumisajat%i_%i.png' %(kuvat, laji, vuosi0, vuosi1))
    figure(1)
    savefig('%s/pa_%stoistumisajat_erikseen%i_%i.png' %(kuvat, laji, vuosi0, vuosi1))
else:
    show()
