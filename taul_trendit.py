#!/usr/bin/python3

#tekee taulukon simuloiduista trendeistä ja merkitsevyydestä

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import pymannkendall as mk
import locale
locale.setlocale(locale.LC_ALL, 'fi_FI.utf8');

muuttuja = "ajankohdat" #icevolume tai ajankohdat
sarake = 1; #paksuus tai alku --> 0, jäätalven pituus --> 1
pns = 0; #pienin neliösumma vai theil-senn
historia = 0; #skenaariot vai historia-ajo

if historia:
    ajot = ("A001", "B001", "D001");
else:
    ajot = ("A002", "B002", "D002", "A005", "B005", "D005");
ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
sk = "/home/aerkkila/a/pakspaikat/";
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");

if muuttuja == "icevolume":
    ulostunniste = "h";
elif sarake == 0:
    ulostunniste = "alku";
else:
    ulostunniste = "pit";

ft = open("/home/aerkkila/a/taul_%sTrendit%s.txt"
          %(ulostunniste, "Hist" if historia else ""), "w");
if(historia):
    ft.write( (" & %s"*2 + " & %s \\\\\n\\hline\n") %(ajonimet) );
else:
    ft.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") );
    ft.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet*2) );

fr = open("/home/aerkkila/a/taul_%sStdResid%s.txt"
          %(ulostunniste, "Hist" if historia else ""), "w");
if(historia):
    fr.write( (" & %s"*2 + " & %s \\\\\n\\hline\n") %(ajonimet) );
else:
    fr.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") );
    fr.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet*2) );

for p in range(len(paikat)):
    ft.write("%s" %paikat[p]);
    fr.write("%s" %paikat[p]);
    for a in range(len(ajot)):
        if(muuttuja == "icevolume"):
            tiednimi = "%s%s_%s_%s_maks.txt" %(sk, paikat[p], muuttuja, ajot[a]);
        elif(muuttuja == "ajankohdat"):
            tiednimi = "%s%s_%s_%s.txt" %(sk, paikat[p], ajot[a], muuttuja);
        data = np.genfromtxt(tiednimi);
        suure = data[:,0];
        vuosi = data[:,2];

        #jäätymisajankohdasta poistetaan jäätymättömät talvet
        if ulostunniste == "alku":
            tmpind = np.where(suure > -1000);
            suure = suure[tmpind];
            vuosi = vuosi[tmpind];
   
        if pns: #pienin neliösumma
            df = pd.DataFrame({'vuosi': vuosi, 'suure': suure});
            fit = smf.ols('suure ~ vuosi', data=df).fit();
        else: #theil-senn
            df = pd.Series(suure, vuosi);
            ts = mk.original_test(df);

        #tehdään testit ja tulostetaan
        if(pns):
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
        else:
            if(ts.p < 0.01):
                ft.write(locale.format_string(" & \\textbf{%.1f}", ts.slope*10));
            elif(ts.p < 0.05):
                ft.write(locale.format_string(" & %.1f", ts.slope*10));
            else:
                ft.write(locale.format_string(" & (%.1f)", ts.slope*10));
            resid = suure - (vuosi*ts.slope - ts.intercept);
            fr.write(locale.format_string(" & %.2f", np.std(resid)));
    ft.write(" \\\\\n");
    fr.write(" \\\\\n");

ft.close();
fr.close();
