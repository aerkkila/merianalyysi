#!/usr/bin/python3

import numpy as np
import locale
locale.setlocale(locale.LC_ALL, "fi_FI.utf8");

sk = "/home/aerkkila/a/pakspaikat";
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");
dalku = 244; #päivä, jolloin vuosi vaihtuu
nimet = ("MP", "EC", "HC");

def tee_taulukko():
    ulos = open("/home/aerkkila/a/taulukot/taul_paksVaiKons.txt", "w");
    ulos.write("RCP & 4.5" + " &"*2 + " & 8.5" + " &"*2 + " \\\\\n");
    ulos.write((" & %s"*6 + " \\\\\n") %(nimet*2));
    for pind in range(len(paikat)):
        ulos.write("\\hline\n");
        tied = "%s/%s_sulako.txt" %(sk, paikat[pind]);
        data = np.genfromtxt(tied, comments="#", dtype='int32');
        alkuvuosi = data[0,-1]
        loppuvuosi = data[-1,-1];
        mukaan = np.ones(366, dtype=bool);
        mukaan[365-dalku] = False;
        ajoja = np.shape(data)[1]-2;
        ulos.write("%s" %(paikat[pind]));
        kons_ajot = [];
        for aind in range(ajoja):
            paks = [];
            kons = [];
            for vind in range(loppuvuosi-alkuvuosi):
                mukaan[365-dalku] = True if(alkuvuosi+vind % 4) else False
                alku = dalku + 366*vind;
                vdata = data[alku:alku+366][mukaan];
                nPaks = 0;
                nKons = 0;
                for i in range(len(vdata)):
                    if(vdata[i,aind]) == 1:
                        nPaks += 1;
                    elif(vdata[i,aind]) == 2:
                        nKons += 1;
                paks.append(nPaks);
                kons.append(nKons);
            kons_ajot.append(kons);
            ulos.write(locale.format_string(" & %2i %4.1f %2i",
                                            (np.min(paks), np.mean(paks), np.max(paks))));
        ulos.write(" \\\\\n");
        for aind in range(ajoja):
            kons = kons_ajot[aind];
            ulos.write(locale.format_string(" & %2i %4.1f %2i",
                                            (np.min(kons), np.mean(kons), np.max(kons))));
        ulos.write(" \\\\\n");
    ulos.close();

tee_taulukko();
