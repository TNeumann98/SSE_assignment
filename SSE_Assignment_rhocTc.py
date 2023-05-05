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
    t = np.log10(t)
    return t
#define last entropy profile
Teff_1 = T_profile(log1, no)
Teff_2 = T_profile(log2, no)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.profile_data()#profile_number=i)
    r = p.logRho
    r = np.log10(np.exp(r))
    return r

#define last entropy profile
rho_1 = rho_profile(log1, no)
rho_2 = rho_profile(log2, no)


#Mass vs. Temperature plot
#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig, ax = plt.subplots(1, 1, figsize=(columnwidth, columnwidth*3/4))

ax.plot(rho_1,Teff_1, '-.',label = r'$1M_\odot$ star', color = 'orange')
ax.plot(rho_2,Teff_2, '--', label = r'$2M_\odot$ star', color = 'blue')

# straight line with slope 1/3
ax.plot([-3,3,9], [8-1,8+1,8+3], ls='-', alpha = 0.5, c='lightgreen')
ax.text(1, 8+1, r'$T_\mathrm{c} \propto \rho_\mathrm{c}^{1/3}$')

# flattening of evolutionary track from ~5*10^8 K on
ax.hlines(np.log10(5e8), -3.0, 10, color='purple', linestyle='-', alpha = 0.5, linewidth=0.7)

# define regions referring the equation of state:
ax.text(2,10, 'Radiation')
ax.text(-3.5,6, 'Ideal gas')
ax.text(1,4, 'Non-relativistic \n degenerate gas')
ax.text(6,4, 'Relativistic \n degenerate gas')


# add solar core conditions
ax.plot(np.log10(150),np.log10(15000000), marker = '*', label = r'Sun', color = 'orange')

ax.set_xlabel(r'log10($\rho_c$) $[kg/m^3]$')
ax.set_ylabel(r'log10(T$_c$) $[K]$')
ax.set_title(r'$log(\rho_c)$ -log(T$_c$)-diagram')
plt.legend(loc = 'best', prop={'size': 7})
plt.grid()
plt.savefig('./figures/profile_log(Tc)_vs_log(rhoc).pdf') 
