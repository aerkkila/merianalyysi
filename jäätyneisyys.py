#!/usr/bin/python3

### kuvaajat jäätyneenä olemisen todennäköisyydestä vuoden kuluessa ###

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import locale
locale.setlocale(locale.LC_ALL, "fi_FI.utf8");

historia = 1;

if historia:
    ajot = ("A001", "B001", "D001");
    ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
else:
    ajot = ("A002", "A005", "B002", "B005", "D002", "D005");
    ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
sk = "/home/aerkkila/a/pakspaikat";
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue");
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
aika = 30;
sigmaGauss = 10/3;
gaussPit = 10;

#gaussin alipäästösuodatin:
gaussPaino = lambda t,sigma: 1/(np.sqrt(2*np.pi)*sigma) * np.exp(-0.5 * t**2/sigma**2);

def suodata(a, sigma, suodPit):
    tulos = np.zeros(len(a));
    for kohta in range(len(tulos)):
        if(kohta-suodPit < 0 or kohta+suodPit >= len(tulos)):
            tulos[kohta] = np.nan;
        else:
            s = 0;
            for T in range(-suodPit, suodPit+1):
                s += a[kohta-T]*gaussPaino(T,sigma);
            tulos[kohta] = s;
    return tulos;

#piirrettäköön kuvaaja 1.11. – 15.6.
miinuspaiva = 61+gaussPit;
pluspaiva = 166+gaussPit;

def piirraKuva(paikka_ajot, alkuv, loppuv, fig):
    kerr = 2 if historia else 1;
    for pind in range(len(paikat)):
        ax = plt.subplot(3,2,pind+1);
        sarakt = np.shape(paikka_ajot)[2] - 2; #lopussa päivä ja vuosi
        for aind in range(sarakt):
            paivia = len(np.where(paikka_ajot[pind][:,-1] == alkuv+1)[0]);
            F = [0]*(paivia);
            alkuind = np.where(paikka_ajot[pind][:,-1] == alkuv)[0][pluspaiva];
            w = np.where(paikka_ajot[pind][:,-1] == loppuv)[0];
            loppuind = w[pluspaiva] if(len(w)) else len(paikka_ajot);
            ind = alkuind
            xPaivat = np.arange(-miinuspaiva,pluspaiva);
            while(ind < loppuind):
                for d in range(paivia):
                    if(paikka_ajot[pind][ind][aind] == 0):
                        F[d] += 1;
                    ind+=1;
            F = np.array(F);
            F = F/(loppuv-alkuv); #nimittäjänä n eikä n+1
            F = suodata(F, sigmaGauss, gaussPit);
            plt.plot(xPaivat, F, color=varit[aind*kerr], label=ajonimet[aind]);
        plt.grid('on');
        plt.ylim([-0.05, 1.05]);
        #pykäliin päivämäärät
        tikit = np.arange(-50,151,12.5);
        ajat = pd.to_datetime(tikit,unit='D');
        plt.xticks(tikit, ajat.strftime("%e. %b"), rotation=45, fontsize=10);
        #50 päivän välein korostettu viiva
        gridx = ax.xaxis.get_gridlines();
        for i in range(len(gridx)):
            if i%4==0:
                gridx[i].set_linewidth(1.5)
                gridx[i].set_color("k");
        plt.title(paikat[pind], fontsize=15);
        plt.ylabel('jään todennäköisyys',fontsize=15);
        plt.legend(ncol=1, fontsize=9, frameon=0);
        plt.tight_layout();
    fig.suptitle("%i – %i" %(alkuv+1, loppuv), fontsize=18);
    if 0:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/jäätyneisyys%i_gs%i.png'
                    %(alkuv+1, round(sigmaGauss*3)));

paikka_ajot = [[]]*len(paikat);
for pind in range(len(paikat)):
    tied = "%s/%s_sulako%s.txt" %(sk, paikat[pind], "Hist" if historia else "");
    suluus = np.genfromtxt(tied, comments="#", dtype='int16');
    #1. vuosi jää pois, koska talvea ei ole kokonaan, samaten viim. puoli vuotta
    pit = len(suluus);
    mukaan = np.zeros(len(suluus), dtype='bool');
    for i in range(pit-miinuspaiva):
        vuosi = suluus[i,-1];
        paiva = suluus[i,-2];
        if(vuosi%4 and 365 >= paiva and paiva > 365-miinuspaiva):
            mukaan[i] = True;
        elif(vuosi%4==0 and 366 >= paiva and paiva > 366-miinuspaiva):
            mukaan[i] = True;
        elif(paiva <= pluspaiva):
            mukaan[i] = True;

    paikka_ajot[pind] = suluus[mukaan];

alkuv = paikka_ajot[0][0,-1]; #kirjoitettakoon suurempi vuosiluku, koska vuosi vaihtuu
loppuv = paikka_ajot[0][-1,-1];
valiv = 0;

if((loppuv-alkuv)/aika < 1.5):
    valiv = loppuv
    loppuv = 0;
else:
    valiv = alkuv+aika;
    valiv1 = loppuv-aika;

if 1:
    fig = plt.figure(figsize=(12,10));
    piirraKuva(paikka_ajot, alkuv, valiv, fig);
    plt.close();

    if(loppuv):
        fig = plt.figure(figsize=(12,10));
        piirraKuva(paikka_ajot, valiv1, loppuv, fig);
        plt.close();

#kuva vastefunktiosta
if 0:
    f = np.linspace(0, 1/3);
    y = np.exp(-2*(np.pi*f*sigmaGauss)**2);
    plt.plot(f,y);
    plt.ylabel('Taajuusvaste');
    plt.xlabel('taajuus ($d^{-1}$)');
    plt.title('Alipäästösuodattimen taajuusvaste, σ = %i/3' %round(sigmaGauss*3));
    if 0:
        plt.show();
    else:
        plt.savefig('/home/aerkkila/a/kuvat1/jäätyneisyys_gaussVaste%i.png'
                    %(round(sigmaGauss*3)));
