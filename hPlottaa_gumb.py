#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import sys

#plotataan halutulta aikaväliltä gumbelsovitus ja mallihavainnot gumbelkoordinaatistossa

pltInd = -1; #mikä indeksi otetaan gumbkertoimet-tiedostosta
skGumb = "./";
skMalli = "/home/aerkkila/a/pakspaikat/"
n = 30;
muuttuja = "icevolume";
uk = "/home/aerkkila/a/kuvat1/";

ajot = ["A002", "B002", "D002"];
skenaario = "RCP 4.5"
ajonimet = ("Max Planck", "EC-Earth", "Hadley Centre");
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
varit = ("r", "g", "b");

fig = figure(figsize=[12,10]);
for pind in range(len(paikat)):
    subplot(3,2,pind+1);
    for aind in range(len(ajot)):
        data = np.genfromtxt("%shGumbkertoimet_%s_%s.txt"\
                             %(skGumb, paikat[pind], ajot[aind]));
        a,b,r2,vuosi = data[pltInd, :];
        data = np.genfromtxt("%s%s_%s_%s_maks.txt"\
                             %(skMalli, paikat[pind], muuttuja, ajot[aind])\
                             , usecols=[0]);
        if(pltInd == -1):
            h = data[-n:]
        elif(pltInd < 0):
            h = data[pltInd-n+1:pltInd+1];
        else:
            h = data[pltInd:pltInd+n];
        h = np.sort(h);
        h2 = h**2;

        raja = n//len(h2);
        for tmp in range(len(h2)):
            if(h[tmp] < 10):
                continue;
            if(tmp > raja):
                raja = tmp;
            break;
        
        F = np.array(range(1,len(h2)+1)) / (len(h2)+1.0);
        F = -1*np.log(-1*np.log(F));

        plot(h2[raja:], F[raja:], 'o', color=varit[aind]\
             , label="%s, $r^2$ = %.3f" %(ajonimet[aind], r2));
        plot(h2[:raja], F[:raja], '.', color=varit[aind]);
        plot(h2, h2*a+b, color=varit[aind]);
        xlabel("$h^2$ ($cm^2$)", fontsize=13);
        ylabel("-ln(-ln(F))", fontsize=13);
        yticks(fontsize=13);
        xticks(fontsize=13);
        title("%s" %(paikat[pind]));
        legend(fontsize=10, frameon=0);

suptitle("%s %i – %i" %(skenaario, vuosi-(n-1)//2, vuosi+n//2));
tight_layout(h_pad=1);
if len(sys.argv)==2 and sys.argv[1]=='1':
    savefig(uk+"hGumbsovit.png");
else:
    show();
