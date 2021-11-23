#!/usr/bin/python3

import struct, matplotlib.colors as colors
from jaettu import ajonimet,kuvat
from matplotlib.pyplot import *
from matplotlib.cm import get_cmap
import numpy as np

#ensin tehdään kartat kaikista vuosista ohjelmilla pktied.c ja pitkart_kartoista.c
#näistä 10 50 90 prosenttiosuus ohjelmalla xkarttoja.c
#sitten käytetään tätä

#värikartta halutaan epäjatkuvana
kartta = get_cmap('gnuplot2')
raja1=235
rajat = np.arange(0,raja1,18)
norm = colors.BoundaryNorm(rajat, kartta.N, clip=True)

for jasen in ['10', '50', '90']:
    for kind,kirjain in enumerate('ABDK'):
        with open("pituus%s_%s001.bin" %(jasen,kirjain), "rb") as f:
            sisalto = f.read()
        xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
        if(kirjain == 'A'):
            fig=figure(figsize=(xpit/100*2/0.88, (ypit-10)/100*2/0.9))
            fig.add_axes((0,   0.5, 0.44,0.45))
        elif(kirjain == 'B'):
            fig.add_axes((0.45,0.5, 0.44,0.45))
        elif(kirjain == 'D'):
            fig.add_axes((0,   0,   0.44,0.45))
        elif(kirjain == 'K'):
            fig.add_axes((0.45, 0, 0.44, 0.45))
        y0 = 0 if kirjain == 'K' else 10
        kuva = np.empty((ypit-y0,xpit), dtype=int)
        muoto = 'h'*xpit
        for j in range(y0,ypit):
            kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2 : 8+(j+1)*xpit*2])
        imshow(kuva, cmap=kartta, norm=norm)
        if(kirjain == 'K'):
            title('Ice charts')
        else:
            title(ajonimet[kind*2][:-len(' M.N')])
        clim(0,raja1)
        axis(False)
        
    alue = fig.add_axes((0.9,0.1,0.05,0.8))
    cb = colorbar(cax=alue, ticks=rajat)
    if(sys.argv[-1] == '1'):
        savefig("%s/pituuskartta%s.png" %(kuvat,jasen))
    else:
        show()
