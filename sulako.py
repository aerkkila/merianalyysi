#!/usr/bin/python3

### tiedostot siitä, onko jokin paikka sula ###
### jos jäässä, luku 0, luvut 1, 2 ja 3 kertovat,
  # rajoittaako paksuus, peittävyys, vai molemmat ###

import numpy as np
import sys

historia = int(sys.argv[1])
paksraja = 0.01 - 0.000001;
konsraja = 0.15 - 0.000001;
if historia:
    ajot = ("A001", "B001", "D001");
else:
    ajot = ("A002", "A005", "B002", "B005", "D002", "D005");
sk = "/home/aerkkila/a/pakspaikat";
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");

for pind in range(len(paikat)):
    ajoTulos = [[]]*len(ajot);
    for aind in range(len(ajot)):
        paks = np.genfromtxt("%s/%s_icevolume_%s_kaikki.txt"
                             %(sk, paikat[pind], ajot[aind]), usecols=[0]);
        kons = np.genfromtxt("%s/%s_soicecov_%s_kaikki.txt"
                             %(sk, paikat[pind], ajot[aind]), usecols=[0]);
        ddata = [0]*len(paks);
        for i in range(len(paks)):
            if(paks[i] < paksraja):
                ddata[i] += 1;
            if(kons[i] < konsraja):
                ddata[i] += 2;
        ajoTulos[aind] = ddata;

        
    da = np.genfromtxt("%s/%s_icevolume_%s_kaikki.txt"
                       %(sk, paikat[pind], ajot[aind]), usecols=[1,2]);
    tied = "%s/%s_sulako%s.txt" %(sk, paikat[pind], "Hist" if historia else "");
    f = open(tied, "w");
    f.write(("#" + "%s, "*(len(ajot)-1) + "%s, päivä, vuosi\n") %(ajot));
    for d in range(len(ajoTulos[0])):
        for a in range(len(ajot)):
            f.write("%i\t" %ajoTulos[a][d]);
        f.write("%i\t%i\n" %(da[d][0], da[d][1]));
