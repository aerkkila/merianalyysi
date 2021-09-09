#!/usr/bin/python3

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import locale
locale.setlocale(locale.LC_ALL, 'fi_FI.utf8');

ajot = ("A002", "A005", "B002", "B005", "D002", "D005")
nimet = ("Max Planck", "EC-Earth", "Hadley Centre")

sk = '/home/aerkkila/b/tiedokset'

bp = [0]*6;

for aind in range(len(ajot)):
    data = np.genfromtxt('%s/pintaalat_%s_maks.txt' %(sk,ajot[aind]))
    ala = data[:,0]
    vuosi = data[:,2]

    df = pd.DataFrame({'vuosi': vuosi, 'ala': ala})
    fit = smf.ols('ala ~ vuosi', data=df).fit()
    
    #tehdään testit ja tallennetaan muistiin
    bp[aind] = sms.het_breuschpagan(fit.resid, fit.model.exog)[1]
    
f = open("/home/aerkkila/b/taulukot/pa_heteroskedastisuus.txt", "w");
f.write("& RCP 4.5 & RCP 8.5 \\\\\n\\hline\n");

for aind in range(len(ajot)):
    if(aind % 2 == 0):
        f.write(locale.format_string("%s & %.4f & ", (nimet[aind//2], bp[aind])));
    else:
        f.write(locale.format_string("%.4f \\\\\n", bp[aind]));

f.close();
