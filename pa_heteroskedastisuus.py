#!/usr/bin/python3

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import locale
locale.setlocale(locale.LC_ALL, 'fi_FI.utf8');

jaaraja = "15_1" #peittävyys_paksuus
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
nimet = ["A: 4.5", "A: 8.5", "B: 4.5", "B: 8.5", "D: 4.5", "D: 8.5"];

sk = '/home/aerkkila/a/pintaalat_'+jaaraja+'/';

bp = [0]*6;

for aind in range(len(ajot)):
    data = np.genfromtxt(sk + 'pa_' + ajot[aind] + '_maks.txt');
    ala = data[:,0];
    vuosi = data[:,2];

    df = pd.DataFrame({'vuosi': vuosi, 'ala': ala});
    fit = smf.ols('ala ~ vuosi', data=df).fit();
    
    #tehdään testit ja tallennetaan muistiin
    bp[aind] = sms.het_breuschpagan(fit.resid, fit.model.exog)[1];
    
f = open("/home/aerkkila/a/pa_heteroskedastisuus.txt", "w");

for aind in range(len(ajot)):
    f.write(" & %s" %nimet[aind]);
f.write(" \\\\\n\\hline\np-arvo");
for aind in range(len(ajot)):
    f.write(locale.format_string(" & %.4f", bp[aind]));
f.write("\\\\\n");

f.close();
