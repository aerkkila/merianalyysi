#!/usr/bin/python3

#tallentaa kustakin ajosta ja paikasta aikasarjan, jossa on neljällä sarakkeella on:
#0. kertymäfunktion sovitussuoran kulmakerroin gumbelkoordinaatistossa
#1. suoran vakiotermi
#2. r^2 eli korrelaatiokertoimen neliö
#3. vuosiluku kyseisen aikaikkunan puolivälistä

import numpy as np
import scipy.stats as st

v0 = 2006; #ensimmäinen vuosi datassa
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
n = 30; #aikaikkunan pituus; jos negatiivinen, otetaan kaikki vuodet
muuttuja = "icevolume";

sk = '/home/aerkkila/a/pakspaikat/';

for aind in range(len(ajot)):
    for pind in range(len(paikat)):
        data = np.genfromtxt("%s%s_%s_%s_maks.txt"\
                             %(sk, paikat[pind], muuttuja, ajot[aind]),\
                             usecols=[0]);
        if(n < 0):
            n = len(data);

        #muodostetaan juokseva aikasarja, jossa on kerrallaan mukana n vuotta
        #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
        #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
        ind = 0;

        f = open("hGumbkertoimet_%s_%s.txt" %(paikat[pind], ajot[aind]), "w");
        while 1:
            h = data[ind : ind+n]; #valitaan aikaikkuna
            h = np.sort(h);
            h2 = h**2 #tämä on oikea satunnaismuuttuja
            F = np.array(range(1,len(h2)+1)) / (len(h2)+1.0); #kokeellinen kertymäfunktio

            #rajataan ei-huomioitaviksi suoran sovituksessa hyvin pienet arvot
            #jätejään alle 10 cm arvot pois
            raja = 0
            for tmp in range(len(h2)):
                if(h[tmp] < 10):
                    continue;
                raja = tmp;
                break;

            F = -1*np.log(-1*np.log(F)); #muunnos gumbelkoordinaatistoon

            #suoran sovitus sekä suoran parametrien ja vuoden tallentaminen
            a, b, r, p, kkv = st.linregress(h2[raja:], F[raja:]);
            f.write("%.5e\t%.5f\t%.4f\t%i\n" %(a,b,r**2, v0+ind+(n-1)//2));

            ind += 1;
            if (ind+n > len(data)):
                break;
        f.close();
