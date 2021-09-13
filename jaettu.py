import numpy as np
from matplotlib.pyplot import *
import matplotlib.ticker as ticker
import locale

suomeksi = False
if suomeksi:
    kuvat = '/home/aerkkila/b/kuvat'
    taulukot = '/home/aerkkila/b/taulukot'
    locale.setLocale(locale.LC_ALL, 'fi_FI.utf8')
else:
    kuvat = '/home/aerkkila/b/kuvat_en'
    taulukot = '/home/aerkkila/b/taulukot_en'
pa_kansio = '/home/aerkkila/b/pintaalat'
h_kansio = '/home/aerkkila/b/paksuudet'

ajot = ("A002", "A005", "B002", "B005", "D002", "D005")
ajot_hist = ('A001', 'B001', 'D001')
ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Centre 4.5", "Hadley Centre 8.5")
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue")
paikat = ('Kemi', 'Kalajoki', 'Mustasaari', 'Nordmaling', 'Rauma', 'Söderhamn')
paikat_en = ('Kemi', 'Kalajoki', 'Korsholm', 'Nordmaling', 'Rauma', 'Söderhamn')

def rajaa(tiedos, vuosi0, vuosi1):
    tiedos = tiedos[np.where(vuosi0 <= tiedos[:,1])]
    if not len(tiedos):
        raise Exception('Vuosi0 epäonnistui: %i, tyhjä tiedos' %vuosi0)
        return tiedos
    
    tiedos = tiedos[np.where(tiedos[:,1] <= vuosi1)]
    if not len(tiedos):
        raise Exception('Vuosi1 epäonnistui: %i, tyhjä tiedos' %vuosi1)
    
    return tiedos

paikallistaja = ticker.ScalarFormatter(useLocale=True)
def paikallista_akselit(x=1,y=1):
    if x:
        gca().xaxis.set_major_formatter(paikallistaja)
    if y:
        gca().yaxis.set_major_formatter(paikallistaja)
