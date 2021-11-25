#!/usr/bin/python3

from matplotlib.pyplot import *
from jaettu import kuvat
import numpy as np
import sys

nimet = {'A':'Max Planck', 'B':'EC-Earth', 'D':'Hadley Centre', 'K':'Ice charts'}
varit = {'A':'lightsalmon', 'D':'deepskyblue', 'B':'lime', 'K':'k'}

fonttikoko = 14
for kirjain in 'ABDK':
    tiedos = np.loadtxt('../tiedokset/makslaajuudet_%s001.txt' %kirjain, usecols=(0,2))
    xdata = tiedos[:,0]
    xdata = np.sort(xdata) / 1000
    ydata = 1 - np.arange(1,len(xdata)+1) / (len(xdata)+1)
    plot(xdata, ydata, color=varit[kirjain], label=nimet[kirjain])
legend(fontsize=fonttikoko)
xlabel('Ice extent ($\mathrm{km}^2/1000$)',fontsize=fonttikoko)
ylabel('Probability',fontsize=fonttikoko)
yticks(fontsize=fonttikoko)
xticks(fontsize=fonttikoko)
grid('on')
tight_layout()
if sys.argv[-1] == '1':
    savefig('%s/laajuudet_hist.png'  %kuvat)
else:
    show()
