import numpy as np

suomeksi = False
kuvat = '/home/aerkkila/b/kuvat'
tiedokset = '/home/aerkkila/b/tiedokset'

ajot = ("A002", "A005", "B002", "B005", "D002", "D005")
ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Centre 4.5", "Hadley Centre 8.5")
varit = ("red", "lightsalmon", "green", "lime", "blue", "deepskyblue")

def rajaa(tiedos, vuosi0, vuosi1):
    tiedos = tiedos[np.where(vuosi0 <= tiedos[:,1])]
    if not len(tiedos):
        raise Exception('Vuosi0 epäonnistui: %i, tyhjä tiedos' %vuosi0)
        return tiedos
    
    tiedos = tiedos[np.where(tiedos[:,1] <= vuosi1)]
    if not len(tiedos):
        raise Exception('Vuosi1 epäonnistui: %i, tyhjä tiedos' %vuosi1)
    
    return tiedos
