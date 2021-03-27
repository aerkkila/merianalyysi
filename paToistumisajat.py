#!/usr/bin/python3

import numpy as np
from numpy import log
from matplotlib.pyplot import *

jaaraja = "15_1";
sk = '/home/aerkkila/a/pakoodi/';
tied = "gumbelkertoimet_kokoaika_"+jaaraja+".txt";
uk = '/home/aerkkila/a/kuvat1/';

skdat = '/home/aerkkila/a/pintaalat_%s/' %jaaraja;

vuosi0 = 2006; #käytetään vain nimeämiseen

data = np.genfromtxt(sk + tied, usecols=[1,2], comments = '#');
a = data[:,0];
b = data[:,1];
pa_l = lambda T: (-log(-log(1/T))-b) / a;

#Tässä oletetaan ajojärjestys tiedostossa
ajot = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
ajotied = ["A002", "A005", "B002", "B005", "D002", "D005"];
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue");

T0 = 1.05;
T1 = 100;
vuosi0 = 2006;
aika = 54;

#pinta-alat kaikista toistumisajoista
#a ja b ovat taulkoita, joten tässä on kaikki ajot
Tarr = np.geomspace(T0, T1, num=200);
A = [[]]*len(Tarr);
for i in range(len(Tarr)):
    A[i] = pa_l(Tarr[i]);
A = np.array(A);

fig2 = figure(2,figsize=(6,4));
sp2 = fig2.add_subplot(111);
fig1 = figure(1,figsize=(10,8));
for aind in range(len(ajot)):
    
    #haetaan kertymäfunktio mallista
    pa = np.genfromtxt(skdat + 'pa_' + ajotied[aind] + '_maks.txt', usecols=[0]);
    pa = np.sort(pa);
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0);
    Tpiste = 1/F;
    
    A1 = A[:,aind];
    fig1.add_subplot(3,2,aind+1);
    plot(Tpiste, pa, 'o', markersize=3, color='deepskyblue');
    plot(Tarr, A1, color='r');
    ylim(top=105000);
    xscale('log',base=10)
    title(ajot[aind]);
    xlabel("toistumisaika (vuotta)", fontsize=11);
    ylabel("pinta-ala $(km^2)$", fontsize=11);
    sp2.plot(Tarr, A1, color=varit[aind], label=ajot[aind]);

figure(1);
suptitle('Tilastolliset jään pinta-alat Pohjanlahdella vuosina %i – %i' %(vuosi0, vuosi0+aika-1));
tight_layout(h_pad=1);
figure(2);
title('Tilastolliset pinta-alat vuosina %i – %i' %(vuosi0, vuosi0+aika-1));
xlabel("toistumisaika (vuotta)", fontsize=11);
ylabel("pinta-ala $(km^2)$");
tight_layout();
legend();
ylim(top=105000);
if 1:
    show();
else:
    figure(2);
    savefig(uk + "paToistumisajat%s.png" %jaaraja);
    figure(1);
    savefig(uk + "paToistumisajatErikseen%s.png" %jaaraja);
