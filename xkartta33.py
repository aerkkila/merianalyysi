#!/usr/bin/python3

import struct, matplotlib.colors as colors
from jaettu import kuvat
from matplotlib.pyplot import *
from matplotlib.cm import get_cmap
import numpy as np
import sys

#ensin tehdään kartat kaikista vuosista ohjelmilla pktied.c ja pitkart_kartoista.c
#näistä 10 50 90 prosenttiosuus ohjelmalla xkarttoja.c
#sitten käytetään tätä

kartta = get_cmap('gnuplot2')
raja1=235
rajat = np.arange(0,raja1,18)
norm = colors.BoundaryNorm(rajat, kartta.N, clip=True)

kirjaimet = sys.argv[1]
ulosnimi = sys.argv[2]
if not ('D' in kirjaimet):
    otsikot = {'A':'Mean(MP,HC)', 'B':'EC-Earth', 'K':'Ice charts'}
elif not ('K' in kirjaimet):
    otsikot = {'A':'Max Planck', 'B':'EC-Earth', 'D':'Hadley Centre'}
fig = False
rako = (0.01, 0.035)
Alue = (0, 0, 0.9, 1)
xgrid = 3; ygrid = 3
alue = lambda i,j: (Alue[0]+Alue[2]/xgrid*i, Alue[1]+Alue[3]/ygrid*(ygrid-1-j),
                    Alue[2]/xgrid-rako[0], Alue[3]/ygrid-rako[1])

for jkuva,arvo in enumerate(['10', '50', '90']):
    ikuva=0
    for kirjain in kirjaimet:
        y0 = 0 if kirjain == 'K' else 10
        with open("%s%s_%s001.bin" %(ulosnimi,arvo,kirjain), "rb") as f:
            sisalto = f.read()
        xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
        if not fig:
            fig = figure(figsize=(xpit/100*xgrid/0.88, (ypit-y0)/100*ygrid/0.9))
        fig.add_axes(alue(ikuva,jkuva))
        kuva = np.empty((ypit-y0,xpit), dtype=int)
        muoto = 'h'*xpit
        for j in range(y0,ypit):
            kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
        if otsikot[kirjain] == 'Mean(MP,HC)':
            with open("%s%s_D001.bin" %(ulosnimi,arvo), "rb") as f:
                sisalto = f.read()
            for j in range(y0,ypit):
                kuva[ypit-1-j,:] += struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
            kuva //= 2
        imshow(kuva, cmap=kartta, norm=norm)
        title("%s %s %%" %(otsikot[kirjain],arvo), fontsize=17)
        clim(0,raja1)
        axis(False)
        ikuva += 1
        
alue = fig.add_axes((Alue[0]+Alue[2]-0.02, 0.1, 0.05, 0.8))
colorbar(cax=alue, ticks=rajat)
yticks(fontsize=15)
if(sys.argv[-1] == '1'):
    savefig("%s/%skartta_33.png" %(kuvat,ulosnimi))
else:
    show()
