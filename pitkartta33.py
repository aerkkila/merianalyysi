#!/usr/bin/python3

import struct, matplotlib.colors as colors
from jaettu import kuvat
from matplotlib.pyplot import *
from matplotlib.cm import get_cmap
import numpy as np
import xarray as xr

#ensin tehdään kartat kaikista vuosista ohjelmilla pktied.c ja pitkart_kartoista.c
#näistä 10 50 90 prosenttiosuus ohjelmalla xkarttoja.c
#sitten käytetään tätä

with open('kartmask.bin', 'rb') as f:
    kartmask = f.read()
kartmask = np.frombuffer(kartmask,dtype=np.int8)
dat = xr.open_dataset('bathy_meter.nc')
nemomask = np.array(dat.bdy_msk)
dat.close()
nemomask = np.flip(nemomask, 0)

#värikartta saadaan epäjatkuvana
kartta = get_cmap('gnuplot2')
raja1=220
rajat = np.arange(0,raja1+1,20)
norm = colors.BoundaryNorm(rajat, kartta.N, clip=True)

otsikot = {'A':'Mean(MP,HC)', 'B':'EC-Earth', 'K':'Ice charts'}
kirjaimet = 'BAK'
fig = False
yrako = 0.035
Alue = (0, 0, 0.9, 1)
xgrid = 3; ygrid = 3
alue = lambda i,j: (Alue[0]+Alue[2]/xgrid*i, Alue[1]+Alue[3]/ygrid*(ygrid-1-j),
                    Alue[2]/xgrid, Alue[3]/ygrid-yrako)

#x-ero on pienempi kuin y-ero
#määrä on eri simulaatiossa ja kartassa
#tässä käytetään suhdetta 62:nnella leveyspiirillä
simsuhde = 0.78
karsuhde = 0.94

#rajataan reunoilta tyhjää pois
rvasen = 15
roikea = 15

for jkuva,arvo in enumerate(['10', '50', '90']):
    ikuva=0
    for kirjain in kirjaimet:
        y0 = 0 if kirjain == 'K' else 10
        with open("pituus%s_%s001.bin" %(arvo,kirjain), "rb") as f:
            sisalto = f.read()
        xpit,ypit,v0,v1 = struct.unpack('hhhh', sisalto[0:8])
        if not fig:
            fig = figure(figsize=((xpit-rvasen-roikea)/100*xgrid/Alue[2]*simsuhde, (ypit-y0)/100*ygrid/Alue[3]))
            fig.set_facecolor('#cccccc')
        fig.add_axes(alue(ikuva,jkuva))
        kuva = np.empty((ypit-y0,xpit), dtype=float)
        muoto = 'h'*xpit
        for j in range(y0,ypit):
            kuva[ypit-1-j,:] = struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
        if kirjain == 'A':
            with open("pituus%s_D001.bin" %(arvo), "rb") as f:
                sisalto = f.read()
            for j in range(y0,ypit):
                kuva[ypit-1-j,:] += struct.unpack(muoto, sisalto[8+j*xpit*2:8+(j+1)*xpit*2])
            kuva /= 2
        if kirjain == 'K':
            if arvo == '10':
                kartmask = np.flip(np.reshape(kartmask,(ypit,xpit)), 0)
            kuva[kartmask==1] = np.nan
        else:
            kuva[nemomask[:-y0,:]==0] = np.nan
            kuva = kuva[:,rvasen:-roikea]
        imshow(kuva, cmap=kartta, interpolation='nearest')#, norm=norm) #nan-arvot sotkevat ellei interpolointi ole 'nearest'
        if kirjain == 'K':
            gca().set_aspect(1/karsuhde)
        else:
            gca().set_aspect(1/simsuhde)
        title("%s %s %%" %(otsikot[kirjain],arvo), fontsize=15)
        clim(0,raja1)
        axis(False)
        ikuva += 1
        
alue = fig.add_axes((Alue[0]+Alue[2]-0.008, 0.1, 0.04, 0.8))
colorbar(cax=alue, ticks=rajat)
yticks(fontsize=15)
if(sys.argv[-1] == '1'):
    savefig("%s/pituuskartta_33.png" %kuvat)
else:
    show()
