#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import scipy.stats as st
import locale
import matplotlib.ticker as ticker

locale.setlocale(locale.LC_ALL, "fi_FI.utf8");
paikallistaja = ticker.ScalarFormatter(useLocale=True);
def paikallista_akselit(x=1,y=1):
    if x:
        gca().xaxis.set_major_formatter(paikallistaja);
    if y:
        gca().yaxis.set_major_formatter(paikallistaja);

sk = '/home/aerkkila/a/pintaalat_15_1/';
uk = '/home/aerkkila/a/kuvat1/';

ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
ajonimet = ("Max Planck 4.5", "Max Planc 8.5", "EC-Earth 4.5", "EC-Earth 8.5", "Hadley Center 4.5", "Hadley Center 8.5");
aika = -1;
vuosi0 = 2006; #käytetään toistaiseksi vain nimeämiseen
kuvakoko = (10,10);

figure(figsize=kuvakoko);
for aind in range(len(ajot)):
    data = np.genfromtxt(sk + 'pa_' + ajot[aind] + '_maks.txt', usecols=[0]);
    if(aika < 0):
        aika = len(data); #mahdollistaisi lyhemmän pätkän valinnan
    i = 0;
    pa = data[i*aika:(i+1)*aika];
    pa = np.sort(pa);
    F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0);

    #rajataan ei huomioitaviksi suoran sovituksessa kokonaisjäätymiset
    raja = len(pa);
    for tmp in range(len(pa)-1):
        if(pa[tmp] > 103000):
            raja = tmp;
            break;

    Fg = -1*np.log(-1*np.log(F));
    a, b, r, p, kkv = st.linregress(pa[0:raja], Fg[0:raja]);

    print('%s\t%.4e\t%.4f' %(ajot[aind],a,b));
    
    subplot(4,3,aind+(1 if aind < 3 else 4));
    plot(pa[0:raja], Fg[0:raja], 'o', color='deepskyblue'); #huomioidut pisteet
    plot(pa[raja:], Fg[raja:], 'o', color='r'); #ei-huomioidut pisteet
    plot(pa, a*pa+b, color='olive');
    title(locale.format_string("%s; $r^2$ = %.4f", (ajonimet[aind], r**2)));
    xlabel("pinta-ala ($km^2$)");
    ylabel("-ln(-ln(F(A)))");

    subplot(4,3,aind+(4 if aind < 3 else 7));
    plot(pa[0:raja], F[0:raja], 'o', color='deepskyblue'); #huomioidut pisteet
    plot(pa[raja:], F[raja:], 'o', color='r'); #ei-huomioidut pisteet
    plot(pa, np.exp(-np.exp(-a*pa-b)), color='olive');
    title(locale.format_string("%s; $σ_{res}$ = %.3f", (ajonimet[aind], np.std(F-(np.exp(-np.exp(-a*pa-b)))))));
    xlabel(u'pinta-ala ($km^2$)');
    ylabel("F",rotation=0);
    paikallista_akselit();
    
suptitle("%i – %i" %(vuosi0, vuosi0+aika-1));
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk+'paGumbsovit15_1.png');
