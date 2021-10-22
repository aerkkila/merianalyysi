#!/usr/bin/python3

import struct
from jaettu import ajonimet
from matplotlib.pyplot import *
import numpy as np

for jasen in ['10', '50', '90']:
    for kind,kirjain in enumerate('ABD'):
        with open("pituus%s_%s001.bin" %(jasen,kirjain), "rb") as f:
            sisalto = f.read()
        xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
        if(kirjain == 'A'):
            fig=figure(figsize=(xpit/100*2/0.88, ypit/100*2/0.9))
            fig.add_axes((0,   0.5, 0.44,0.45))
        elif(kirjain == 'B'):
            fig.add_axes((0.45,0.5, 0.44,0.45))
        elif(kirjain == 'D'):
            fig.add_axes((0,   0,   0.44,0.45))
        kuva = np.empty((ypit,xpit), dtype=int)
        muoto = 'h'*xpit
        for j in range(ypit):
            kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
        imshow(kuva)
        title(ajonimet[kind*2][:-len(' M.N')])
        clim(0,225)
        axis(False)
    alue = fig.add_axes((0.9,0.1,0.05,0.8))
    colorbar(cax=alue)
    show()
