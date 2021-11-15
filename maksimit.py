#!/usr/bin/python3

import sys, os
import numpy as np

if len(sys.argv) < 5:
    print("Käyttö: ./tämä kansio/ vanha_tunniste uusi_tunniste\n"
          "1. sarakkeen eli kys. arvon tulostusmuoto\n"
          "Esim. ./maksimit.py ../tiedokset/ pintaalat makspintaalat 6.0f")
    exit()

muoto = "%%%s\t%%3.0f\t%%4.0f\n" %(sys.argv[4])

for nimi in os.listdir(sys.argv[1]):
    if(nimi[0:len(sys.argv[2])] != sys.argv[2]): #tunniste ei täsmää
        continue
    tiedos = np.loadtxt(sys.argv[1]+nimi, dtype='float32')
    ulosnimi = sys.argv[3] + nimi[len(sys.argv[2]):] #vaihdetaan tunniste
    f = open(sys.argv[1]+ulosnimi, "w")
    i=0
    while i < len(tiedos[:,0]):
        vuosi = tiedos[i,2]
        pit = 0
        for v in tiedos[i:,2]:
            pit += 1
            if v != vuosi:
                break
        ind = np.nanargmax(tiedos[i:i+pit,0])
        f.write(muoto %(tiedos[ind+i,0],tiedos[ind+i,1],tiedos[ind+i,2]))
        i += pit
    f.close()
