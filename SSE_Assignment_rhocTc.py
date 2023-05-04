import numpy as np
import matplotlib.pylab as plt
#%matplotlib inline
from scipy import constants as con

# Plotting script for SSE assignment
from mymisc import *


import mesa_reader as mr
#diretions of the LOG-files
log1 = mr.MesaLogDir('./1M_prems_to_wd/LOGS')
log2 = mr.MesaLogDir('./2M_prems_to_wd/LOGS')


### log(rho_c) vs. log(T_c) plot
no = -1
#define T profile of last time step
def T_profile(log, i):
    p = log.profile_data()#profile_number=i)
    t = p.temperature
    return t
#define last entropy profile
Teff_1 = T_profile(log1, no)
Teff_2 = T_profile(log2, no)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.profile_data()#profile_number=i)
    r = p.logRho
    return r

#define last entropy profile
rho_1 = rho_profile(log1, no)
rho_2 = rho_profile(log2, no)


#Mass vs. Temperature plot
#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig, ax = plt.subplots(1, 1, figsize=(columnwidth, columnwidth*3/4))

ax.plot(Teff_1, rho_1, '-.',label = r'$1M_\odot$ star', color = 'orange')
ax.plot(Teff_2, rho_2, '--', label = r'$2M_\odot$ star', color = 'blue')

ax.plot(np.log10(15000000), np.log10(150), marker = '*', label = r'Sun', color = 'orange')

ax.set_ylabel(r'log($\rho_c$) $[kg/m^3]$')
ax.set_xlabel(r'log(T$_c$) $[K]$')
ax.set_title(r'$log(\rho)$ -log(T$_c$)-diagram')
plt.legend(loc = 'best', prop={'size': 7})
plt.grid()
plt.savefig('./figures/profile_log(Tc)_vs_log(rhoc).pdf') 
