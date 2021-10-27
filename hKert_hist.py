#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import pandas as pd
from scipy.stats import *
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
ytiedos = np.arange(1,32) / 32
for pind,paikka in enumerate(nimet):
    sca(axs[pind])
    print(paikka)
    for aind,ajo in enumerate(ajot_hist):
        tied = "%s/maksh_hist_%s_%s.txt" %(kansio, tnimet[pind], ajo);
        tiedos = np.loadtxt(tied, usecols=(0));
        tiedos = np.sort(tiedos)
        plot(tiedos, ytiedos, color=varit[aind*2], label=ajonimet_hist[aind])
        print(tiedos[np.where(tiedos > 100)])
    print(v0[pind])
    print(v1[pind])
    hnto = hnnot[paikka][np.arange(v0[pind],v1[pind]+1)]
    hnto = np.sort(hnto)
    hnto = hnto[np.where(~np.isnan(hnto))]
    plot(hnto, ytiedos, color='y', label='observations')
    legend(fontsize=10,frameon=False)
    grid('on')
    title(paikka)
show()
exit()


for p in range(len(paikat)):
    ax = plt.subplot(3,2,p+1);
    
    if(p < len(paikkaind)): #havainnot
        htmp = np.sort(hnnot[p]);
        F = np.array(range(1,len(htmp)+1)) / (len(htmp)+1.0); #diskreetti kertymäfunktio
        plt.plot(htmp, F, color='k', label="havainnot");        
    for a in range(len(ajot)): #malli
        htmp = np.sort(paikka_ajo[p][a])
        F = np.array(range(1,len(htmp)+1)) / (len(htmp)+1.0); #diskreetti kertymäfunktio
        plt.plot(htmp, F, color=varit[a], label=ajonimet[a]);
    
    plt.grid('on')
    plt.title(paikat[p], fontsize=15);
    paikallista_akselit();
    plt.ylim(0,1)
    plt.xlim(0,110)
    plt.ylabel('Todennäköisyyskertymä',fontsize=15)
    plt.xlabel('Paksuuden vuosimaksimi (cm)',fontsize=15)
    plt.yticks(fontsize=13);
    plt.xticks(fontsize=13);
    plt.legend(ncol=1, fontsize=11, loc='upper left', frameon=0);
    plt.tight_layout();

if len(sys.argv)==2 and sys.argv[1]=='1':
    plt.savefig('/home/aerkkila/a/kuvat1/pakskert_hist.png');
else:
    plt.show();
