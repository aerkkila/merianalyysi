#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa
#gumbelsuoran termit luetaan tiedostoista,
#jotka tehdään ohjelmalla laske_gumbkertoimet.py

import numpy as n
from matplotlib.pyplot import *

jaaraja = "15_1";
uk = '/home/aerkkila/a/kuvat1/';

nimet = ["A: 4.5", "A: 8.5", "B: 4.5", "B: 8.5", "D: 4.5", "D: 8.5"];
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];

#halutut toistumisajat
Tn = [2, 5, 10, 30, 50];

#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista
pa_l = lambda T,a,b: (-n.log(-n.log(1/T))-b) / a;

figure(figsize=(12,10));
for aind in range(len(ajot)):
    
    #luetaan suoran parametrit
    tied = "gumbkertoimet_%s_%s.txt" %(jaaraja,ajot[aind]);
    data = n.genfromtxt(tied, usecols=[0,1,3]); #a, b, vuosi
    a = data[:,0];
    b = data[:,1];
    v = data[:,2];

    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä on kaikki vuodet
    A = [[]]*len(Tn);
    tmp = 0;
    for T in Tn:
        A[tmp] = pa_l(T,a,b);
        tmp+=1;
    A = n.array(A);
    A = A.transpose();

    subplot(3,2,aind+1);
    plot(v, A, color='k');
    grid('on')
    xlabel("vuosiluku");
    ylabel("pinta-ala ($km^2$)");
    #ylim([5000, 75000])
    title('%s' %(nimet[aind]));
    
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk + "pa_viivat"+jaaraja+".png");

close();
