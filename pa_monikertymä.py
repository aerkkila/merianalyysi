#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
from numpy import log, exp
import scipy.stats as st
import sys, locale
import matplotlib.ticker as ticker
from jaettu import *

if(suomeksi):
    xnimi = 'pinta-ala $(km^2)$'
else:
    xnimi = 'area $(km^2)$'
    
def kautto():
    print("Käyttö: ./tämä alkuvuosi loppuvuosi g/f/w (1, jos tallenna)")
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
    xm = lambda x: log(x)
    Fpalaute = lambda x: x # ei määritelty, koska tätä ei käytetä
elif laji == 'w': #weibull
    Fm = lambda F: log(-log(1-F))
    xm = lambda x: log(x)
    Fpalaute = lambda x: 1-exp(-(x**a*exp(b)))
else:
    kautto()

fig=figure(figsize=(10,10))
axs = fig.subplots(4,3).flatten(order='F')
for aind,ajo in enumerate(ajot):
    tiedos = np.genfromtxt("%s/makspintaalat_%s.txt" %(kansio,ajo), usecols=[0,2],dtype=float)
    try:
        tiedos = rajaa(tiedos, vuosi0, vuosi1)
    except Exception as e:
        print(str(e))
        kautto()
    i = 0
    pa = np.sort(tiedos[:,0])
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0)

    #rajataan ei huomioitaviksi suoran sovituksessa kokonaisjäätymiset
    raja = len(pa)
    for tmp in range(len(pa)-1):
        if(pa[tmp] > 103000):
            raja = tmp
            break

    F1 = Fm(F)
    x1 = xm(pa)
    a, b, r, p, kkv = st.linregress(x1[0:raja], F1[0:raja])

    sca(axs[aind*2])
    plot(x1[0:raja], F1[0:raja], 'o', color='deepskyblue') #huomioidut pisteet
    plot(x1[raja:], F1[raja:], 'o', color='r') #ei-huomioidut pisteet
    plot(x1, a*x1+b, color='olive')
    locale.setlocale(locale.LC_ALL, paikallisuus)
    paikallista_akselit()
    title(locale.format_string("%s; $r^2$ = %.4f", (ajonimet[aind], r**2)));
    xlabel("x'", fontsize=11)
    ylabel("y'", fontsize=12)

    sca(axs[aind*2+1])
    plot(pa[0:raja], F[0:raja], 'o', color='deepskyblue') #huomioidut pisteet
    plot(pa[raja:], F[raja:], 'o', color='r') #ei-huomioidut pisteet
    plot(pa, Fpalaute(pa), color='olive')
    title(locale.format_string("%s; $σ_{res}$ = %.3f", (ajonimet[aind], np.std(F[:raja]-Fpalaute(pa[:raja])))))
    xlabel(xnimi, fontsize=11)
    paikallista_akselit()
    ylabel("F",rotation=0, fontsize=12)

suptitle("%i–%i; %s" %(vuosi0, vuosi1, 'gumbel' if laji == 'g' else 'weibull'))
tight_layout(h_pad=1)
if sys.argv[-1] == '1':
    savefig('%s/pa_%s_kertymä%i_%i.png' %(laji, kuvat, vuosi0, vuosi1))
else:
    show()
