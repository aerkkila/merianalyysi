#!/usr/bin/python3

import struct, matplotlib.colors as colors
from jaettu import kuvat
from matplotlib.pyplot import *
from matplotlib.cm import get_cmap
import xarray as xr
import numpy as np
import sys

#ensin tehdään kartat kaikista vuosista ohjelmilla pktied.c ja pitkart_kartoista.c
#näistä 10 50 90 prosenttiosuus ohjelmalla xkarttoja.c
#sitten käytetään tätä

dat = xr.open_dataset('bathy_meter.nc')
mask = np.array(dat.bdy_msk)
dat.close()
mask = np.flip(mask, 0)

if len(sys.argv) < 2 or sys.argv[1] not in ('10','50','90'):
    numero = '10'
else:
    numero = sys.argv[1]

#värikartan saisi tällä epäjatkuvana poistamalla kommentoinnin imshow:n perästä
kartta = get_cmap('gnuplot2')
raja1 = 190 if numero == '90' else 140
rajat = np.arange(0,raja1+1,20)
norm = colors.BoundaryNorm(rajat, kartta.N, clip=True)

otsikot = {'A':'Max Planck', 'B':'EC-Earth', 'D':'Hadley Centre', 'K':'Ice charts'}
rcpt = {'2':'RCP 4.5', '5':'RCP 8.5'}
kirjaimet = 'ABD'
fig = False
rako = (0.0, 0.035)
Alue = (0, 0, 0.9, 1)
xgrid = 3; ygrid = 2
alue = lambda i,j: (Alue[0]+Alue[2]/xgrid*i, Alue[1]+Alue[3]/ygrid*(ygrid-1-j),
                    Alue[2]/xgrid-rako[0], Alue[3]/ygrid-rako[1])

for jkuva,arvo in enumerate(['2','5']):
    ikuva=0
    for kirjain in kirjaimet:
        y0 = 0 if kirjain == 'K' else 10
        with open("pituus%s_%s00%s.bin" %(numero,kirjain,arvo), "rb") as f:
            sisalto = f.read()
        xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
        if not fig:
            fig = figure(figsize=(xpit/100*xgrid/0.88, (ypit-y0)/100*ygrid/0.9))
            fig.set_facecolor('#bfaaca')
        fig.add_axes(alue(ikuva,jkuva))
        kuva = np.empty((ypit-y0,xpit), dtype=float)
        muoto = 'h'*xpit
        for j in range(y0,ypit):
            kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
        kuva[mask[:-y0,:]==0] = np.nan
        imshow(kuva, cmap=kartta)#, norm=norm)
        title("%s %s" %(otsikot[kirjain],rcpt[arvo]), fontsize=17)
        clim(0,raja1)
        axis(False)
        ikuva += 1

alue = fig.add_axes((Alue[0]+Alue[2]-0.01, 0.1, 0.05, 0.8))
colorbar(cax=alue, ticks=rajat)
yticks(fontsize=16)
if(sys.argv[-1] == '1'):
    savefig("%s/pituuskartta%s_%i.png" %(kuvat,numero,v0))
else:
    show()
