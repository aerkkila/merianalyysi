#!/usr/bin/python3

#tekee taulukon simuloiduista trendeistä ja merkitsevyydestä
kautto = 'Käyttö: ./tämä haluttu_tunniste nimialku (1, jos historia)'

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import pymannkendall as mk
import sys, locale
from jaettu import *

if len(sys.argv) < 3:
    print(kautto)
    exit()

try:
    historia = int(sys.argv[-1]) #skenaariot vai historia-ajo
except:
    historia = 0
pns = 0; #pienin neliösumma vai theil-senn

if historia:
    ajot = ("A001", "B001", "D001")
else:
    ajot = ("A002", "B002", "D002", "A005", "B005", "D005")
ajonimet = ("Max Planck", "EC-Earth", "Hadley Centre")
ajonimet2 = ("MP", "EC", "HC")

ft = open("%s/%s%s_trendit.txt"
          %(taulukot, sys.argv[1], "Hist" if historia else ""), "w")
fr = open("%s/%s%s_keskihajonta.txt"
          %(taulukot, sys.argv[1], "Hist" if historia else ""), "w")

for tied in (ft, fr):
    if(historia):
        tied.write( (" & %s" + " &"*2 + " \\\\\n") %("Historia"))
        tied.write( (" & %s"*2 + " & %s \\\\\n\\hline\n") %(ajonimet) )
    else:
        tied.write( ("%s & %s" + " &"*2 + " & %s" + " &"*2 + " \\\\\n") %("RCP", "4.5", "8.5") )
        tied.write( (" & %s"*5 + " & %s \\\\\n\\hline\n") %(ajonimet2*2) )

for pind in range(len(paikat)):
    ft.write("%s" %(paikat[pind]))
    fr.write("%s" %(paikat[pind]))
    for aind,ajo in enumerate(ajot):
        tiednimi = "%s_%s_%s.txt" %(sys.argv[2], paikat_fi[pind], ajo)
        tiedos = np.loadtxt(tiednimi, usecols=(0,2))
   
        if pns: #pienin neliösumma
            df = pd.DataFrame({'vuosi': tiedos[:,1], 'suure': tiedos[:,0]})
            fit = smf.ols('suure ~ vuosi', data=df).fit()
        else: #theil-senn
            df = pd.Series(tiedos[:,0], tiedos[:,1])
            ts = mk.original_test(df)

        #tehdään testit ja tulostetaan
        locale.setlocale(locale.LC_ALL, paikallisuus)
        if(pns):
            if(fit.pvalues.vuosi < 0.01):
                ft.write(locale.format_string(" & \\textbf{%.1f}", fit.params.vuosi*10))
            elif(fit.pvalues.vuosi < 0.05):
                ft.write(locale.format_string(" & %.1f", fit.params.vuosi*10))
            else:
                ft.write(locale.format_string(" & (%.1f)", fit.params.vuosi*10))
                fr.write(locale.format_string(" & %.2f", np.std(fit.resid)))
            print(sms.het_breuschpagan(fit.resid, fit.model.exog)[1])
            print(sms.het_white(fit.resid, fit.model.exog)[1])
            print("")
        else:
            if(ts.p < 0.01):
                ft.write(locale.format_string(" & \\textbf{%.1f}", ts.slope*10))
            elif(ts.p < 0.05):
                ft.write(locale.format_string(" & %.1f", ts.slope*10))
            else:
                ft.write(locale.format_string(" & (%.1f)", ts.slope*10))
            resid = tiedos[:,0] - (tiedos[:,1]*ts.slope - ts.intercept)
            fr.write(locale.format_string(" & %.2f", np.std(resid)))
    ft.write(" \\\\\n")
    fr.write(" \\\\\n")
ft.close()
fr.close()
