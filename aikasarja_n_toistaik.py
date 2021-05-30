#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa
#gumbelsuoran termit luetaan tiedostoista,
#jotka tehdään ohjelmalla laske_gumbkertoimet.py

import numpy as n
from matplotlib.pyplot import *
import sys

jaaraja = "15_1";
uk = '/home/aerkkila/a/kuvat1/';

nimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Centre 4.5", "Hadley Centre 8.5");
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
    xlabel("vuosi", fontsize=15);
    ylabel("pinta-ala ($km^2$)", fontsize=15);
    yticks(fontsize=13);
    xticks(fontsize=13);
    title('%s' %(nimet[aind]));
    
tight_layout(h_pad=1);
if len(sys.argv)==2 and sys.argv[1]=='1':
    savefig(uk + "pa_viivat"+jaaraja+".png");
else:
    show();

close();
