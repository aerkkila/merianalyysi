#!/usr/bin/python3

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
from jaettu import *
import locale

nimet = ("Max Planck", "EC-Earth", "Hadley Centre")

bp = [0]*6;

for aind in range(len(ajot)):
    data = np.genfromtxt('%s/makspintaalat_%s.txt' %(kansio,ajot[aind]))
    ala = data[:,0]
    vuosi = data[:,2]

    df = pd.DataFrame({'vuosi': vuosi, 'ala': ala})
    fit = smf.ols('ala ~ vuosi', data=df).fit()
    
    #tehdään testit ja tallennetaan muistiin
    bp[aind] = sms.het_breuschpagan(fit.resid, fit.model.exog)[1]
    
f = open("%s/pa_heteroskedastisuus.txt" %taulukot, "w");
f.write("& RCP 4.5 & RCP 8.5 \\\\\n\\hline\n");

locale.setlocale(locale.LC_ALL, paikallisuus)
    for aind in range(len(ajot)):
        if(aind % 2 == 0):
            f.write(locale.format_string("%s & %.4f & ", (nimet[aind//2], bp[aind])));
        else:
            f.write(locale.format_string("%.4f \\\\\n", bp[aind]));

f.close();
