#!/usr/bin/python3

import numpy as np
import scipy.stats as st
from matplotlib.pyplot import *
import locale
locale.setlocale(locale.LC_ALL, "fi_FI.utf8");

jaaraja = "15_1";
sk = "/home/aerkkila/a/pintaalat_%s/" %jaaraja;
uk = "/home/aerkkila/a/kuvat1";

ajot = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
ajotied = ["A002", "A005", "B002", "B005", "D002", "D005"];

figure(figsize=(12,10));
for aind in range(len(ajot)):
    data = np.genfromtxt("%spa_%s_maks.txt" %(sk,  ajotied[aind]));
    pa = data[:,0];
    vuodet = data[:,2];

    a,b,r,p,kkv = st.linregress(vuodet, pa);

    subplot(3,2,aind+1);
    plot(vuodet,pa,'o', color='deepskyblue');
    plot(vuodet, a*vuodet+b, color='r');
    title(locale.format_string("%s, p = %.3f\n%.1fe3 $km^2/10a$, $\sigma_{res}$ = %.0f",
                               (ajot[aind], p, a/100, np.std(pa-(a*vuodet+b)))));
    xlabel("vuosi", fontsize=11);
    ylabel("pinta-ala ($km^2$)", fontsize=11);


suptitle("Pinta-alat vuosina %i – %i" %(vuodet[0], vuodet[-1]));
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig("%s/paRegressio_%s.png" %(uk, jaaraja));
