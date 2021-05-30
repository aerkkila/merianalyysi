#!/usr/bin/python3

#tekee värikuvan, jonka akselit x, y, c ovat:
#vuosiluku, toistumisaika, pinta-ala
#käytetään liukuvaa aikasarjaa
#gumbelsuoran termit luetaan tiedostoista,
#jotka tehdään ohjelmalla laske_gumbkertoimet.py

import numpy as n
from matplotlib.pyplot import *
from matplotlib.colors import ListedColormap
import locale, sys
import matplotlib.ticker as ticker

locale.setlocale(locale.LC_ALL, "fi_FI.utf8");
paikallistaja = ticker.ScalarFormatter(useLocale=True);
def paikallista_akselit(x=1,y=1):
    if x:
        gca().xaxis.set_major_formatter(paikallistaja);
    if y:
        gca().yaxis.set_major_formatter(paikallistaja);

jaaraja = "15_1";
uk = '/home/aerkkila/a/kuvat1/';

nimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Centre 4.5", "Hadley Centre 8.5");
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];

tallenna = 1 if len(sys.argv)==2 and sys.argv[1]=='1' else 0

#pienin ja suurin mukaanotettava toistumisaika
T0 = 2;
T1 = 80;

#Pinta-alaväli, jolle värit skaalautuvat
A0 = 5000; A1 = 80000;

#kaavat värien laskemiselle värikartassa
#vihr1 = lambda c: n.tanh(n.abs((0 if(c < 1/2) else 1) - c) * 5);
vihr = lambda c: n.abs(n.sin(c**0.4*n.pi*20)**0.4)
pun = lambda c: c**0.5;
sin = lambda c: 1-pun(n.abs(c-0.33))

#tehdään rgba-värikartta halutusta pinta-alavälistä
varit = [[]]*256
c = n.linspace(0,1,256);
for tmp in range(256):
    varit[tmp] = [pun(c[tmp]), vihr(c[tmp]), sin(c[tmp]), 1];
    vkartta = ListedColormap(varit);

Tarr = n.array(range(T0, T1+1));
Tarr = Tarr[::-1]; #suunnanvaihdos koska kuva toimii näin päin

#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista
pa_l = lambda T,a,b: (-n.log(-n.log(1/T))-b) / a;

figure(figsize=(12,10));
for aind in range(len(ajot)):
    
    #luetaan suoran parametrit
    tied = "gumbkertoimet_%s_%s.txt" %(jaaraja,ajot[aind]);
    data = n.genfromtxt(tied); #a, b, r^2, vuosi
    a = data[:,0];
    b = data[:,1];
    r2 = data[:,2];
    v = data[:,3];
    rajat = [min(v), max(v), T0, T1];

    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä on kaikki vuodet
    A = [[]]*(T1+1-T0);
    tmp = 0;
    for T in Tarr:
        A[tmp] = pa_l(T,a,b);
        tmp+=1;
    A = n.array(A);

    subplot(3,2,aind+1);
    kuva = imshow(A, cmap=vkartta, aspect='auto', extent=rajat, vmin=A0, vmax=A1);
    xlabel("vuosi", fontsize=15);
    ylabel("toistumisaika (vuotta)", fontsize=15);
    yticks(fontsize=13);
    xticks(fontsize=13);
    title('%s' %(nimet[aind]), fontsize=15);
    ax2 = gca().twinx();
    ax2.plot(v,r2, color='w');
    ylabel("$r^2$", rotation=0, fontsize=15);
    yticks(fontsize=13);
    paikallista_akselit();
    ylim([0.92, 1])
    
tight_layout(h_pad=1);
if not tallenna:
    show();
else:
    savefig(uk + "pa_värit"+jaaraja+".png");

close();

#Tehdään varipalkki erilliseksi kuvaksi, koska muuten on vaikeaa
figure(figsize=(3,10));
palkki = [[]]*256;
for tmp in range(256):
    palkki[tmp] = [tmp*(A1-A0)/256+A0]*10
imshow(palkki, cmap=vkartta, vmin=A0, vmax=A1);

#halutut pinta-alat (yticks) väripalkille
ax = gca();
ax.set_xticks([]);
ytikit = n.array([A0, 15000, 20000, 25000, 35000, 50000, 60000, A1]);
yticks(fontsize=15)
ytiknorm = (ytikit - A0) / (A1 - A0) * 255;
ax.set_yticks(ytiknorm);
ax.set_yticklabels(ytikit);
ylabel("pinta-ala ($km^2$)", fontsize=15);
tight_layout();

if not tallenna:
    show();
else:
    savefig(uk + "pa_värit_väripalkki.png");
