#!/usr/bin/python3

#ensin pitää ajaa pa_gumbkertymä.py, joka luo tiedoston pa_gumbkertoimet_%i_%i.txt

import numpy as np
from numpy import log
from matplotlib.pyplot import *
import sys
from jaettu import *

if suomeksi:
    xnimi = "toistumisaika (vuotta)"
    ynimi = "pinta-ala $(km^2)$"
else:
    xnimi = 'time interval (years)'
    ynimi = 'area $(km^2)$'
try:
    vuosi0 = int(sys.argv[2])
except:
    vuosi0 = 2055
try:
    vuosi1 = int(sys.argv[3])
except:
    vuosi1 = 2100
    
gumbtied = "pa_gumbkertoimet_%i_%i.txt" %(vuosi0, vuosi1);
tiedos = np.loadtxt(gumbtied, usecols=(1,2))
    
a = tiedos[:,0]
b = tiedos[:,1]
pa_l = lambda T: (-log(-log(1/T))-b) / a

T0 = 1.005
T1 = 100

#pinta-alat kaikista toistumisajoista
#a ja b ovat taulukoita, joten tässä on kaikki ajot
Tarr = np.geomspace(T0, T1, num=200)
A = [[]]*len(Tarr)
for i in range(len(Tarr)):
    A[i] = pa_l(Tarr[i])
A = np.array(A)

fig2 = figure(2,figsize=(6,4))
sp2 = fig2.add_subplot(111)
fig1 = figure(1,figsize=(10,8))
for aind in range(len(ajot)):
    
    #kertymäfunktio haetaan tuloksista
    tiedos = np.loadtxt('%s/makspintaalat_%s.txt' %(kansio,ajot[aind]), usecols=(0,2))
    try:
        tiedos = rajaa(tiedos, vuosi0, vuosi1)
    except Exception as e:
        print(str(e))
        exit()
    pa = np.sort(tiedos[:,0])
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0)
    Tpiste = 1/F
    
    A1 = A[:,aind]
    fig1.add_subplot(3,2,aind+1)
    plot(Tpiste, pa, 'o', markersize=3, color='deepskyblue')
    plot(Tarr, A1, color='r')
    ylim(top=105000)
    xscale('log',base=10)
    title(ajonimet[aind])
    xlabel(xnimi, fontsize=11)
    ylabel(ynimi, fontsize=11)
    sp2.plot(Tarr, A1, color=varit[aind], label=ajonimet[aind])

suptitle('%i–%i' %(vuosi0, vuosi1))
tight_layout(h_pad=1)

figure(2)
title('%i–%i' %(vuosi0, vuosi1))
xlabel(xnimi, fontsize=11)
ylabel(ynimi)
tight_layout()
legend()
ylim(top=105000)
if len(sys.argv) > 1 and sys.argv[1] == '1':
    figure(2)
    savefig('%s/pa_toistumisajat%i_%i.png' %(kuvat, vuosi0, vuosi1))
    figure(1)
    savefig('%s/pa_toistumisajat_erikseen%i_%i.png' %(kuvat, vuosi0, vuosi1))
else:
    show()
