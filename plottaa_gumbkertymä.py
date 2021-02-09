#!/usr/bin/python3

from matplotlib.pyplot import *
import numpy as np
import scipy.stats as st

sk = '/home/aerkkila/a/pintaalat_15_1/';
uk = '/home/aerkkila/a/kuvat/';

ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];
nimet = ["A_RCP4.5", "A_RCP8.5", "B_RCP4.5", "B_RCP8.5", "D_RCP4.5", "D_RCP8.5"];
aika = -1;
vuosi0 = 2006; #käytetään toistaiseksi vain nimeämiseen

figure(figsize=(12,10));
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
    
    subplot(3,2,aind+1);
    plot(pa[0:raja], F[0:raja], 'o', color='deepskyblue'); #huomioidut pisteet
    plot(pa[raja:], F[raja:], 'o', color='r'); #ei-huomioidut pisteet
    plot(pa, np.exp(-np.exp(-a*pa-b)), color='olive');
    title(u'%s %i – %i' %(nimet[aind], vuosi0, vuosi0+aika-1));
    xlabel(u'pinta-ala (km²)', fontsize=15);
    ylabel('kertymätodennäköisyys F', fontsize=15);
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk+'pa_gumbkertymä_kokoaika_15_1.png');
