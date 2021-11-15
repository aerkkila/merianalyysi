#!/usr/bin/python3

from matplotlib.pyplot import *
from jaettu import kuvat
import numpy as np
import sys

nimet = {'A':'Max Planck', 'B':'EC-Earth', 'D':'Hadley Centre', 'K':'Ice charts'}
varit = {'A':'lightsalmon', 'D':'deepskyblue', 'B':'lime', 'K':'k'}

for kirjain in 'ABDK':
    tiedos = np.loadtxt('../tiedokset/makslaajuudet_%s001.txt' %kirjain, usecols=(0,2))
    xdata = tiedos[:,0][np.where(tiedos[:,1] < 2007)]
    xdata = np.sort(xdata)
    ydata = np.arange(1,len(xdata)+1) / (len(xdata)+1)
    plot(xdata, ydata, color=varit[kirjain], label=nimet[kirjain])
legend(fontsize=11)
xlabel('Ice extent ($\mathrm{km}^2$)',fontsize=11)
ylabel('Cumulative probability',fontsize=11)
yticks(fontsize=11)
xticks(fontsize=11)
grid('on')
if sys.argv[-1] == '1':
    savefig('%s/laajuudet_hist.png'  %kuvat)
else:
    show()
