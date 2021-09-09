import numpy as np

suomeksi = False
kuvat = '/home/aerkkila/b/kuvat'
tiedokset = '/home/aerkkila/b/tiedokset'

def rajaa(tiedos, vuosi0, vuosi1):
    tiedos = tiedos[np.where(vuosi0 <= tiedos[:,1])]
    if not len(tiedos):
        raise Exception('Vuosi0 epäonnistui: %i, tyhjä tiedos' %vuosi0)
        return tiedos
    
    tiedos = tiedos[np.where(tiedos[:,1] <= vuosi1)]
    if not len(tiedos):
        raise Exception('Vuosi1 epäonnistui: %i, tyhjä tiedos' %vuosi1)
    
    return tiedos
