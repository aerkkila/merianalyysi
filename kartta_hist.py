#!/usr/bin/python3
from matplotlib.pyplot import *
import numpy as np
import struct, sys
from jaettu import kuvat

paikat = ("Tornio (Röyttä)", "Kemi (Ajos)", "Hailuoto (Marjaniemi)", "Raahe", "Bygdeå (Ratan)", "Nordmaling (Järnäs)", "Kalajoki (Rahja)", "Kokkola (Märaskär)", "Korsholm (Valsörarna)")

#ensin ajetaan Puhdissa ohjelma paikat_kartalla.c
#tämä käyttää sen ulostuloa "kartta_hist.bin"

with open('kartta_hist.bin', "rb") as f:
    sisalto = f.read()
xpit, = struct.unpack("i", sisalto[0:4])
ypit, = struct.unpack("i", sisalto[4:8])
taulpohja = np.zeros((ypit,xpit,3))+1 #rgb
taulpaikat = np.zeros((ypit,xpit,4)) #rbga
for j in range(ypit):
    for i in range(xpit):
        taulpohja[ypit-1-j,i,:] = 0.6 + 0.4*(sisalto[8+j*xpit+i] > 0)
        
for j in range(ypit):
    for i in range(xpit):
        if sisalto[8+j*xpit+i] > 1:
            jnyt = ypit-1-j
            taulpaikat[jnyt-5:jnyt+5,i-5:i+5,:] = (0, 1, 1, 0.5)

figure(figsize=(xpit/100*1.5,ypit/100*1.5))
imshow(taulpohja)
imshow(taulpaikat)
axis(False)
tight_layout()

for j in range(ypit):
    for i in range(xpit):
        sind = 8+j*xpit+i
        if sisalto[sind] > 1:
            pind = sisalto[sind]-2
            jnyt = ypit-1-j
            if pind == 0: #Tornio
                text(i-95,jnyt+4,paikat[pind],color=(0,0,0,1),fontsize=12)
            elif pind == 2: #Hailuoto
                text(i-133,jnyt+4,paikat[pind],color=(0,0,0,1),fontsize=12)
            elif pind == 3: #Raahe
                text(i-43,jnyt+4,paikat[pind],color=(0,0,0,1),fontsize=12)
            elif pind == 4: #Ratan
                text(i-100,jnyt+4,paikat[pind],color=(0,0,0,1),fontsize=12)
            elif pind == 5: #Nordmaling
                text(i-55,jnyt-8,paikat[pind],color=(0,0,0,1),fontsize=12)
            elif pind == 8: #Mustasaari
                text(i+5,jnyt+4,paikat[pind],color=(0,0,0,1),fontsize=12)
            else:
                text(i-33,jnyt+15,paikat[pind],color=(0,0,0,1),fontsize=12)

if sys.argv[-1] == '1':
    savefig("%s/kartta_hist.png"%kuvat)
else:
    show()
