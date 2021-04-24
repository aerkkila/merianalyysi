#!/usr/bin/python3

#tekee taulukon gumelsovituksen r²-termeistä pienimmässä neljänneksessä

import numpy as np
import scipy.stats as st
import locale
locale.setlocale(locale.LC_ALL, "fi_FI.utf8");

sk = '/home/aerkkila/a/pintaalat_15_1/';
uk = '/home/aerkkila/a/';

ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
nimet = ("Max Planck", "EC-Earth", "Hadley Center");

f = open(uk + "taul_pa25gumb151.txt", "w");
f.write("& RCP 4.5 & RCP 8.5 \\\\\n\\hline\n");
for aind in range(len(ajot)):
    data = np.genfromtxt(sk + 'pa_' + ajot[aind] + '_maks.txt');
    i = 0;
    pa = data[:,0];
    vuodet = data[:,2];
    pa = np.sort(pa);
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0);

    F = -1*np.log(-1*np.log(F));
    raja = len(pa)//4;
    a, b, r, p, kkv = st.linregress(pa[0:raja], F[0:raja]);

    if(aind % 2 == 0):
        f.write(locale.format_string("%s & %.3f & ", (nimet[aind//2], r**2)));
    else:
        f.write(locale.format_string("%.3f \\\\\n", r**2));

f.close();
