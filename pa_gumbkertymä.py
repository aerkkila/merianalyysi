#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import scipy.stats as st
import sys
import locale
import matplotlib.ticker as ticker

suomeksi = False
sk = '/home/aerkkila/b/tiedokset'
uk = '/home/aerkkila/b/kuvat'

if(suomeksi):
    locale.setlocale(locale.LC_ALL, "fi_FI.utf8")
    paikallistaja = ticker.ScalarFormatter(useLocale=True)
    
def paikallista_akselit(x=1,y=1):
    if x:
        gca().xaxis.set_major_formatter(paikallistaja)
    if y:
        gca().yaxis.set_major_formatter(paikallistaja)
    
def kautto():
    print("Käyttö: python3 pa_gumbkertymä.py alkuvuosi loppuvuosi")
    exit()

ajot = ("A002", "A005", "B002", "B005", "D002", "D005")
ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Centre 4.5", "Hadley Centre 8.5")
kuvakoko = (10,10)
try:
    vuosi0 = int(sys.argv[1])
except Exception as e:
    print(str(e))
    kautto()
try:
    vuosi1 = int(sys.argv[2])
except Exception as e:
    print(str(e))
    kautto()
ulos = open("pa_gumbkertoimet_%i_%i.txt" %(vuosi0,vuosi1), "w")

figure(figsize=kuvakoko)
for aind in range(len(ajot)):
    tiedos = np.genfromtxt("%s/pintaalat_%s_maks.txt" %(sk,ajot[aind]), usecols=[0,2],dtype=int)
    try:
        tiedos = tiedos[np.where(vuosi0 <= tiedos[:,1])]
    except Exception as e:
        print("Ei vuotta %i (%s)" %(vuosi0,ajot[aind]))
        print(str(e))
        kautto()
    try:
        tiedos = tiedos[np.where(tiedos[:,1] <= vuosi1)]
    except Exception as e:
        print("Ei vuotta %i (%s)" %(vuosi1,ajot[aind]))
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

    Fg = -1*np.log(-1*np.log(F))
    a, b, r, p, kkv = st.linregress(pa[0:raja], Fg[0:raja])

    ulos.write('%s\t%.4e\t%.4f\n' %(ajot[aind],a,b))
    
    subplot(4,3,aind+(1 if aind < 3 else 4))
    plot(pa[0:raja], Fg[0:raja], 'o', color='deepskyblue') #huomioidut pisteet
    plot(pa[raja:], Fg[raja:], 'o', color='r') #ei-huomioidut pisteet
    plot(pa, a*pa+b, color='olive')
    title(locale.format_string("%s; $r^2$ = %.4f", (ajonimet[aind], r**2)));
    if(suomeksi):
        xlabel("pinta-ala ($km^2$)", fontsize=11)
    else:
        xlabel("area ($km^2$)")
    ylabel("-ln(-ln(F(A)))", fontsize=12)

    subplot(4,3,aind+(4 if aind < 3 else 7))
    plot(pa[0:raja], F[0:raja], 'o', color='deepskyblue') #huomioidut pisteet
    plot(pa[raja:], F[raja:], 'o', color='r') #ei-huomioidut pisteet
    plot(pa, np.exp(-np.exp(-a*pa-b)), color='olive')
    title(locale.format_string("%s; $σ_{res}$ = %.3f", (ajonimet[aind], np.std(F-(np.exp(-np.exp(-a*pa-b)))))))
    if(suomeksi):
        xlabel('pinta-ala ($km^2$)', fontsize=11)
    else:
        xlabel('area ($km^2$)', fontsize=11)
    ylabel("F",rotation=0, fontsize=12)
    if(suomeksi):
        paikallista_akselit()

ulos.close()
suptitle("%i – %i" %(vuosi0, vuosi1))
tight_layout(h_pad=1)
if len(sys.argv) > 3 and sys.argv[3] == '1':
    savefig('%s/pa_gumbkertymä_%i_%i.png' %(uk, vuosi0, vuosi1))
else:
    show()
