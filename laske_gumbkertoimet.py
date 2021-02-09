#!/usr/bin/python3

#tallentaa kustakin ajosta aikasarjan, jossa on neljällä sarakkeella on:
#0. kertymäfunktion sovitussuoran kulmakerroin gumbelkoordinaatistossa
#1. suoran vakiotermi
#2. r^2 eli korrelaatiokertoimen neliö
#3. vuosiluku kyseisen aikaikkunan puolivälistä

import numpy as np
import scipy.stats as st

jaaraja = "15_1" #peittävyys_paksuus
v0 = 2006; #ensimmäinen vuosi datassa
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
n = 30; #aikaikkunan pituus; jos negatiivinen, otetaan kaikki vuodet

sk = '/home/aerkkila/a/pintaalat_'+jaaraja+'/';

for aind in range(len(ajot)):
    data = np.genfromtxt(sk + 'pa_' + ajot[aind] + '_maks.txt', usecols=[0]);
    if(n < 0):
        n = len(data);
    
    #muodostetaan juokseva aikasarja, jossa on kerrallaan mukana n vuotta
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    ind = 0;

    f = open("gumbkertoimet_" + jaaraja + "_" + ajot[aind] + ".txt", "w");
    while 1:
        pa = data[ind : ind+n]; #valitaan aikaikkuna
        pa = np.sort(pa);
        F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0); #kokeellinen kertymäfunktio

        #rajataan ei-huomioitaviksi suoran sovituksessa kokonaisjäätymiset
        raja = len(pa);
        for tmp in range(len(pa)-1):
            if(pa[tmp] > 103000):
                raja = tmp;
                break;

        F = -1*np.log(-1*np.log(F)); #muunnos gumbelkoordinaatistoon

        #suoran sovitus sekä suoran parametrien ja vuoden tallentaminen
        a, b, r, p, kkv = st.linregress(pa[0:raja], F[0:raja]);
        f.write("%.5e\t%.5f\t%.4f\t%i\n" %(a,b,r**2, v0+ind+(n-1)//2));

        ind += 1;
        if (ind+n > len(data)):
            break;
    f.close();
