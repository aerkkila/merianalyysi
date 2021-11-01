#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import sys, locale
import matplotlib.ticker as ticker
from jaettu import *

if(suomeksi):
    xnimi = 'Jään laajuus $(km^2)$'
    ynimi = 'Todennäköisyyskertymä'
else:
    xnimi = 'Ice extent $(\mathrm{km}^2)$'
    ynimi = 'Cumulative probability'

fonttikoko = 13

for aind,ajo in enumerate(ajot_hist):
    tiedos = np.loadtxt("%s/makspintaalat_%s.txt" %(kansio,ajo), usecols=[0],dtype=float)
    tiedos = np.sort(tiedos)
    yakseli = np.arange(1,len(tiedos)+1) / (len(tiedos)+1)
    plot(tiedos,yakseli, color=varit[aind*2+1],label=ajonimet[aind*2][:-len('4.5')])
    locale.setlocale(locale.LC_ALL, paikallisuus)
    paikallista_akselit()
    legend()
    xlabel(xnimi,fontsize=fonttikoko)
    ylabel(ynimi,fontsize=fonttikoko)
    yticks(fontsize=fonttikoko)
    xticks(fontsize=fonttikoko)
show()
