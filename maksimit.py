#!/usr/bin/python3

import sys, os
import numpy as np

if len(sys.argv) < 2:
    print("Käyttö: ./tämä kansio/ vanha_tunniste uusi_tunniste\n"
          "Esim. ./maksimit.py ../tiedokset/ pintaalat makspintaalat")
    exit()

for nimi in os.listdir(sys.argv[1]):
    if(nimi[0:len(sys.argv[2])] != sys.argv[2]): #tunniste ei täsmää
        continue
    tiedos = np.loadtxt(sys.argv[1]+nimi, dtype='float32')
    ulosnimi = sys.argv[3] + nimi[len(sys.argv[2]):] #vaihdetaan tunniste
    f = open(sys.argv[1]+ulosnimi, "w")
    for i in range(0, len(tiedos[:,0]), 366):
        ind = np.nanargmax(tiedos[i:i+366,0])
        f.write("%6.0f\t%3.0f\t%4.0f\n"%(tiedos[ind+i,0],tiedos[ind+i,1],tiedos[ind+i,2]))
    f.close()
