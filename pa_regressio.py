#!/usr/bin/python3

import numpy as np
import scipy.stats as st
from matplotlib.pyplot import *
import sys, locale
from jaettu import *

if(suomeksi):
    xnimi = 'vuosi'
    ynimi = 'pinta-ala ($km^2$)'
else:
    xnimi = 'year'
    ynimi = 'area ($km^2$)'

figure(figsize=(12,10));
for aind,ajo in enumerate(ajot):
    data = np.genfromtxt("%s/makspintaalat_%s.txt" %(kansio, ajo))
    pa = data[:,0]
    vuodet = data[:,2]

    a,b,r,p,kkv = st.linregress(vuodet, pa)

    subplot(3,2,aind+1)
    plot(vuodet,pa,'o', color='deepskyblue')
    plot(vuodet, a*vuodet+b, color='r')
    locale.setlocale(locale.LC_ALL, paikallisuus)
    title(locale.format_string("%s, p = %.3f\n%.1fe3 $km^2/10a$, $\sigma_{res}$ = %.0f",
                               (ajonimet[aind], p, a/100, np.std(pa-(a*vuodet+b)))), fontsize=12)
    xlabel(xnimi, fontsize=12)
    ylabel(ynimi, fontsize=12)
    xticks(fontsize=12)
    yticks(fontsize=12)

tight_layout(h_pad=1)
if len(sys.argv) == 2 and sys.argv[1] == "1":
    savefig("%s/pa_regressio.png" %(kuvat))
else:
    show()
