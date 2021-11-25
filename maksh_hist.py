#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from jaettu import *
import locale, sys
import matplotlib.ticker as ticker

#locale.setlocale(locale.LC_ALL, paikallisuus);

#paikkaind = (2, 8, 6, 11);
#nimet = ("Tornio (Röyttä)", "Kemi (Ajos)", "Hailuoto (Marjaniemi)", "Raahe", "Ratan", "Nordmaling (Järnäs)", "Kalajoki (Rahja)", "Kokkola (Märaskär)", "Mustasaari (Vallgrund)")
nimet = ("Tornio", "Kemi", "Hailuoto", "Raahe", "Kalajoki", "Kokkola", "Korsholm", "Bygdeå", "Nordmaling")
tnimet = ("Tornio", "Kemi", "Hailuoto", "Raahe", "Kalajoki", "Kokkola", "Mustasaari", "Bygdeå", "Nordmaling")

v0 = (1978,1975,1975,1978,1975,1978,1975,1974,1976)
v1 = (2008,2005,2005,2008,2005,2008,2005,2007,2006)

hnnot = pd.read_csv('../perämeri.csv', index_col=0)

fig = figure(figsize=(12,12))
axs = fig.subplots(3,3).flatten()
ytiedos = 1 - np.arange(1,32) / 32
kaikki_hnnot = np.empty(len(nimet)*31)
kaikki_tkset = [[]]*3
for i in range(3):
    kaikki_tkset[i] = np.empty_like(kaikki_hnnot)

fonttikoko = 15
for pind,paikka in enumerate(nimet):
    sca(axs[pind])
    xlim((0,120))
    for aind,ajo in enumerate(ajot_hist):
        tied = "%s/maksh_hist_%s_%s.txt" %(kansio, tnimet[pind], ajo);
        tiedos = np.loadtxt(tied, usecols=(0));
        tiedos = np.sort(tiedos)
        kaikki_tkset[aind][31*pind:31*(pind+1)] = tiedos
        plot(tiedos, ytiedos, color=varit[aind*2+1], label=ajonimet_hist[aind])
    hnto = hnnot[paikka][np.arange(v0[pind],v1[pind]+1)]
    hnto = np.sort(hnto)
    hnto = hnto[np.where(~np.isnan(hnto))]
    kaikki_hnnot[31*pind:31*(pind+1)] = hnto
    plot(hnto, ytiedos, color='k', label='observations')
    if not pind:
        legend(fontsize=fonttikoko,frameon=False)
    grid('on')
    tight_layout()
    title(paikka,fontsize=fonttikoko)
    xticks(fontsize=fonttikoko)
    yticks(fontsize=fonttikoko)
if(sys.argv[-1] == '1'):
    savefig('%s/maksh_kert_hist.png' %kuvat)
else:
    show()
close(fig)

kaikki_hnnot = np.sort(kaikki_hnnot)
ytiedos = 1 - np.arange(1,31*len(nimet)+1) / (len(nimet)*31+1)
plot(kaikki_hnnot, ytiedos, color='k', label='observations')
for i,t in enumerate(kaikki_tkset):
    t = np.sort(t)
    plot(t, ytiedos, color=varit[i*2+1], label=ajonimet_hist[i])
    print(ks_2samp(kaikki_hnnot, t).pvalue)
legend(fontsize=fonttikoko)
grid('on')
xlim((0,120))
xlabel('Maximum thickness (cm)',fontsize=fonttikoko)
ylabel('Probability',fontsize=fonttikoko)
yticks(fontsize=fonttikoko)
xticks(fontsize=fonttikoko)
tight_layout()
if(sys.argv[-1] == '1'):
    savefig('%s/maksh_kert_hist_kaikki.png' %kuvat)
else:
    show()
