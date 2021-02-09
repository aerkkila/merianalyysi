#!/usr/bin/python3

import numpy as np
from numpy import log
from matplotlib.pyplot import *

jaaraja = "15_1";
sk = '/home/aerkkila/a/pakoodi/';
tied = "gumbelkertoimet_kokoaika_"+jaaraja+".txt";
uk = '/home/aerkkila/a/kuvat/';

skdat = '/home/aerkkila/a/pintaalat_15_1/';

vuosi0 = 2006; #käytetään vain nimeämiseen
varit = ('r', 'g', 'b', 'm', 'c', 'k');

data = np.genfromtxt(sk + tied, usecols=[1,2], comments = '#');
a = data[:,0];
b = data[:,1];
pa_l = lambda T: (-log(-log(1/T))-b) / a;

#Tässä oletetaan ajojärjestys tiedostossa
ajot = ["A_RCP4.5", "A_RCP8.5", "B_RCP4.5", "B_RCP8.5", "D_RCP4.5", "D_RCP8.5"];
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
    plot(Tpiste, pa, 'o', markersize=2);
    plot(Tarr, A1);
    xlim(left=0)
    xlabel("toistumisaika (vuotta)");
    ylabel(u"pinta-ala $(km^2)$");
    title('%s %i – %i' %(ajot[aind], vuosi0, vuosi0+aika-1));
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk + "pa_x_"+jaaraja+".png");
