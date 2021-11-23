#!/usr/bin/python3

import struct, matplotlib.colors as colors
from jaettu import ajonimet,kuvat
from matplotlib.pyplot import *
from matplotlib.cm import get_cmap
import numpy as np

#ensin tehdään kartat kaikista vuosista ohjelmilla pktied.c ja pitkart_kartoista.c
#näistä 10 50 90 prosenttiosuus ohjelmalla xkarttoja.c
#sitten käytetään tätä

kartta = get_cmap('gnuplot2')
raja1=181
rajat = np.arange(0,raja1,15)
norm = colors.BoundaryNorm(rajat, kartta.N, clip=True)

Alue = (0, 0, 1, 1)

with open("ensijää10_A001.bin", "rb") as f:
    sisalto = f.read()
xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
fig=figure(figsize=(xpit/100/0.86*2, ypit/100*2))
fig.add_axes(Alue)
kuva = np.empty((ypit,xpit), dtype=int)
muoto = 'h'*xpit
for j in range(ypit):
    kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2 : 8+(j+1)*xpit*2])

imshow(kuva, cmap=kartta)
#clim(0,raja1)
axis(False)

alue = fig.add_axes((0.88,0.1,0.05,0.8))
cb = colorbar(cax=alue, ticks=rajat)
yticks(fontsize=16)
if(sys.argv[-1] == '1'):
    savefig("pituuskartta50_kartta.png")
else:
    show()
