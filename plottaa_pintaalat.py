#!/usr/bin/python3

import numpy as np
from numpy import log
from matplotlib.pyplot import *

jaaraja = "15_1";
sk = '/home/aerkkila/a/pakoodi/';
tied = "gumbelkertoimet_kokoaika_"+jaaraja+".txt";
uk = '/home/aerkkila/a/kuvat1/';

skdat = '/home/aerkkila/a/pintaalat_15_1/';

vuosi0 = 2006; #käytetään vain nimeämiseen

data = np.genfromtxt(sk + tied, usecols=[1,2], comments = '#');
a = data[:,0];
b = data[:,1];
pa_l = lambda T: (-log(-log(1/T))-b) / a;

#Tässä oletetaan ajojärjestys tiedostossa
ajot = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
ajotied = ["A002", "A005", "B002", "B005", "D002", "D005"];

T0 = 1;
T1 = 121;
vuosi0 = 2006;
aika = 54;

#pinta-alat kaikista toistumisajoista
#a ja b ovat taulkoita, joten tässä on kaikki ajot
Tarr = np.array(range(T0, T1));
A = [[]]*(T1-T0);
for T in Tarr:
    A[T-T0] = pa_l(T);
A = np.array(A);

figure(figsize=(12,10));
for aind in range(len(ajot)):
    
    #haetaan kertymäfunktio mallista
    pa = np.genfromtxt(skdat + 'pa_' + ajotied[aind] + '_maks.txt', usecols=[0]);
    pa = np.sort(pa);
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0);
    Tpiste = 1/F;
    
    A1 = A[:,aind];
    subplot(3,2,aind+1);
    plot(Tpiste, pa, 'o', markersize=3, color='deepskyblue');
    plot(Tarr, A1, color='r');
    xlim(left=0)
    xlabel("toistumisaika (vuotta)", fontsize=11);
    ylabel(u"pinta-ala $(km^2)$", fontsize=11);
    title('%s' %(ajot[aind]));

suptitle('Pinta-alat vuosina %i – %i' %(vuosi0, vuosi0+aika-1));
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk + "pa_x_"+jaaraja+".png");
