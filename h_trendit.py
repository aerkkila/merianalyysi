#!/usr/bin/python3

#tekee taulukon skenaarioitten trendeistä ja merkitsevyydestä paksuuden osalta

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import locale
locale.setlocale(locale.LC_ALL, 'fi_FI.utf8');

muuttuja = "icevolume" #peittävyys_paksuus
ajot = ["A002", "B002", "D002", "A005", "B005", "D005"];
ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
alkuvuosi = 2006;
loppuvuosi = 2059; #ensimmäinen, jota ei ole
sk = "/home/aerkkila/a/pakspaikat/";
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");

ft = open("/home/aerkkila/a/taul_hTrendit.txt", "w");
ft.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") );
ft.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet*2) );

fr = open("/home/aerkkila/a/taul_hStdResid.txt", "w");
fr.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") );
fr.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet*2) );

for p in range(len(paikat)):
    ft.write("%s" %paikat[p]);
    fr.write("%s" %paikat[p]);
    for a in range(len(ajot)):
        tiednimi = "%s%s_%s_%s_maks.txt" %(sk, paikat[p], muuttuja, ajot[a]);
        data = np.genfromtxt(tiednimi);
        h = data[:,0];
        vuosi = data[:,2];

        df = pd.DataFrame({'vuosi': vuosi, 'paks': h});
        fit = smf.ols('paks ~ vuosi', data=df).fit();

        #tehdään testit ja tulostetaan
        if(fit.pvalues.vuosi < 0.01):
            ft.write(locale.format_string(" & \\textbf{%.1f}", fit.params.vuosi*10));
        elif(fit.pvalues.vuosi < 0.05):
            ft.write(locale.format_string(" & %.1f", fit.params.vuosi*10));
        else:
            ft.write(locale.format_string(" & (%.1f)", fit.params.vuosi*10));
        fr.write(locale.format_string(" & %.2f", np.std(fit.resid)));
        print(sms.het_breuschpagan(fit.resid, fit.model.exog)[1]);
        print(sms.het_white(fit.resid, fit.model.exog)[1]);
        print("");
    ft.write(" \\\\\n");
    fr.write(" \\\\\n");

ft.close();
fr.close();
