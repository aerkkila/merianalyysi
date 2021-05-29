#!/usr/bin/python3

#tekee taulukon simuloiduista trendeistä ja merkitsevyydestä

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import pymannkendall as mk
import sys
import locale
locale.setlocale(locale.LC_ALL, 'fi_FI.utf8');

muuttuja = sys.argv[1] #icevolume tai ajankohdat
historia = int(sys.argv[2]); #skenaariot vai historia-ajo
pns = 0; #pienin neliösumma vai theil-senn
if(muuttuja == "icevolume"):
    sarake = 0;
elif(muuttuja == "ajankohdat"):
    sarake = 1;
else:
    print("1. argumentti olkoon \"icevolume\" tai \"ajankohdat\"");
    quit();

if historia:
    ajot = ("A001", "B001", "D001");
else:
    ajot = ("A002", "B002", "D002", "A005", "B005", "D005");
ajonimet = ("Max Planck", "EC-Earth", "Hadley Center");
ajonimet2 = ("MP", "EC", "HC");
sk = "/home/aerkkila/a/pakspaikat/";
paikat = ("Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn");

if muuttuja == "icevolume":
    ulostunniste = "h";
elif sarake == 0:
    ulostunniste = "alku";
else:
    ulostunniste = "pit";

ft = open("/home/aerkkila/a/taulukot/taul_%sTrendit%s.txt"
          %(ulostunniste, "Hist" if historia else ""), "w");
fr = open("/home/aerkkila/a/taulukot/taul_%sStdResid%s.txt"
          %(ulostunniste, "Hist" if historia else ""), "w");

for tied in (ft, fr):
    if(historia):
        tied.write( (" & %s" + " &"*2 + " \\\\\n") %("Historia"));
        tied.write( (" & %s"*2 + " & %s \\\\\n\\hline\n") %(ajonimet) );
    else:
        tied.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") );
        tied.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet2*2) );

for p in range(len(paikat)):
    ft.write("%s" %paikat[p]);
    fr.write("%s" %paikat[p]);
    for a in range(len(ajot)):
        if(muuttuja == "icevolume"):
            tiednimi = "%s%s_%s_%s_maks.txt" %(sk, paikat[p], muuttuja, ajot[a]);
        elif(muuttuja == "ajankohdat"):
            tiednimi = "%s%s_%s_%s.txt" %(sk, paikat[p], ajot[a], muuttuja);
        data = np.genfromtxt(tiednimi);
        suure = data[:,sarake];
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
