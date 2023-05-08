import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
#%matplotlib inline
from scipy import constants as con

# Plotting script for SSE assignment
from mymisc import *


import mesa_reader as mr
#diretions of the LOG-files
log1 = mr.MesaLogDir('./1M_prems_to_wd/LOGS')
log2 = mr.MesaLogDir('./2M_prems_to_wd/LOGS')


# Hertzsprung-Russeldiagram

log1_L = log1.history.log_L
log1_Teff = log1.history.log_Teff
log2_L = log2.history.log_L
log2_Teff = log2.history.log_Teff
log1_age = log1.history.star_age
log2_age = log2.history.star_age


#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), constrained_layout=False)

# plt.figure(figsize=(9, 6))

age1_min = np.min(log1_age)
age1_max = np.max(log1_age)
age2_min = np.min(log2_age)
age2_max = np.max(log2_age)
age_max = np.max([age1_max, age2_max])

# Star 1 gets ten times older than star 2. --> Using same colorbar for both results in a blue line.
age1_norm = (log1_age-age1_min)/(age1_max-age1_min)
age2_norm = (log2_age-age2_min)/(age2_max-age2_min)
age1_colors = plt.cm.viridis(age1_norm)
age2_colors = plt.cm.viridis(age2_norm)
print(age1_min, age1_max)
print(age2_min, age2_max)

ax1.scatter(log1_Teff, log1_L, color=age1_colors, linewidths=0.5, label = r'1 M$_\odot$ star', marker = '.', alpha = 0.5) #edgecolors=age1_colors,
ax2.scatter(log2_Teff, log2_L, color=age2_colors, linewidths=0.5, label = r'2 M$_\odot$ star', marker = '.', alpha = 0.5)

# ax1.plot([log1_Teff[0], log2_Teff[0]],[log1_L[0],log2_L[0]], linestyle = '', marker = 's', markeredgecolor = 'black', alpha = 0.5, label = 'Start evolution', color = 'limegreen')
# ax1.plot([log1_Teff[-1], log2_Teff[-1]], [log1_L[-1], log2_L[-1]], linestyle = '', marker = 'o', markeredgecolor = 'black', alpha = 0.5,label = 'End evolution as wd', color = 'red')
# ax2.plot([log1_Teff[0], log2_Teff[0]],[log1_L[0],log2_L[0]], linestyle = '', marker = 's', markeredgecolor = 'black', alpha = 0.5, label = 'Start evolution', color = 'mediumorchid')
# ax2.plot([log1_Teff[-1], log2_Teff[-1]], [log1_L[-1], log2_L[-1]], linestyle = '', marker = 'o', markeredgecolor = 'black', alpha = 0.5,label = 'End evolution as wd', color = 'red')

ax1.scatter(log1_Teff[0], log1_L[0], marker = 's', edgecolor = 'black' , alpha=0.5, label = 'Start evolution for 1 M$_\odot$ star', color = 'limegreen')
ax1.scatter(log2_Teff[0], log2_L[0], marker = 's', edgecolor = 'black' , alpha=0.5, label = 'Start evolution for 2 M$_\odot$ star', color = 'mediumorchid')
ax1.scatter(log1_Teff[-1], log1_L[-1], marker = 'o', edgecolor = 'black' , alpha=0.5, label = 'End evolution for 1 M$_\odot$ star', color = 'limegreen')
ax1.scatter(log2_Teff[-1], log2_L[-1], marker = 'o', edgecolor = 'black' , alpha=0.5, label = 'End evolution for 2 M$_\odot$ star', color = 'mediumorchid')

ax2.scatter(log1_Teff[0], log1_L[0], marker = 's', edgecolor = 'black' , alpha=0.5, label = 'Start evolution for 1 M$_\odot$ star', color = 'limegreen')
ax2.scatter(log2_Teff[0], log2_L[0], marker = 's', edgecolor = 'black' , alpha=0.5, label = 'Start evolution for 2 M$_\odot$ star', color = 'mediumorchid')
ax2.scatter(log1_Teff[-1], log1_L[-1], marker = 'o', edgecolor = 'black' , alpha=0.5, label = 'End evolution for 1 M$_\odot$ star', color = 'limegreen')
ax2.scatter(log2_Teff[-1], log2_L[-1], marker = 'o', edgecolor = 'black' , alpha=0.5, label = 'End evolution for 2 M$_\odot$ star', color = 'mediumorchid')


# ax1.set_xlabel(r'$\log\,T_\mathrm{eff}/\mathrm{K}$')
ax2.set_xlabel(r'$\log\,T_\mathrm{eff}/\mathrm{K}$')
ax1.set_ylabel(r'$\log\,L/\mathrm{L}_\odot$')
ax2.set_ylabel(r'$\log\,L/\mathrm{L}_\odot$')
fig.suptitle('HR-diagram: Evolutionary stages of 1/ 2 M$_\odot$ star')
ax1.set_title(r'1 M$_\odot$ star')
ax2.set_title(r'2 M$_\odot$ star')
ax1.legend(loc = 'best', prop={'size': 6})
ax2.legend(loc = 'best', prop={'size': 6})
ax1.grid(linewidth=0.1)
ax2.grid(linewidth=0.1)
ax1.set_xlim([5.25, 3.25])
ax2.set_xlim([5.25, 3.25])
ax1.set_ylim([-1.25, 4])
ax2.set_ylim([-1.25, 4])

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes('right', size='5%', pad=0.05)
sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array([])
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes('right', size='5%', pad=0.05)

# fig.subplots_adjust(right=0.2) # or whatever
cbar = plt.colorbar(sm, cax=cax1, ticks=np.linspace(0, 1, 6), orientation = 'vertical')
cbar.ax.set_yticklabels(np.round(np.linspace(0, age1_max/10**9, 6), decimals = 2))
cbar.set_label('Age ($\cdot 10^9$ yr)')
cbar2 = plt.colorbar(sm, cax=cax2, ticks=np.linspace(0, 1, 6))
cbar2.ax.set_yticklabels(np.round(np.linspace(0, age2_max/10**9, 6), decimals = 2))
cbar2.set_label('Age ($\cdot 10^9$ yr)')

# plt.show()
plt.savefig('./figures/hr_evolution.pdf')
"""

# Kippenhahn diagrams

import mkipp
#fig, (ax1, ax2) = plt.subplots(1, 2) #possible for mkipp?

# main Kippenhahn diagram
kipp_plot = mkipp.kipp_plot(mkipp.Kipp_Args(logs_dirs=['1M_sol_nonrot_template/LOGS'], 
                                                #xaxis ="star_age", 
                                                decorate_plot = False))

# we used 'decorate_plot = False', so add colorbar and label
cbar = plt.colorbar(kipp_plot.contour_plot, pad=0.05)
cbar.set_label(r'$\log\, \epsilon_\mathrm{nuc}\,/\,\mathrm{erg}\,\mathrm{s}^{-1}\,\mathrm{g}^{-1}$')

# xy labels
plt.xlabel("Model number")
plt.ylabel(r'$m_{*}\,/\,\mathrm{M}_\odot$')
plt.title(r'MESA: non-rotating 1 $\mathrm{M}_\odot$ star')
plt.savefig('./figures/kip_mesa_1M_9Myr.pdf') # , dpi='figure', format='pdf', res = 300)
###########################################################
#Kippenhahn diagrams of Arepo diagrams
# main Kippenhahn diagram my model
kipp_plot = mkipp.kipp_plot(mkipp.Kipp_Args(logs_dirs=['mesa_merger_progenitors_for_arepo_simulation/LOGS-m1-9myr'],
                                                xaxis ="star_age", 
                                                decorate_plot = False))

# we used 'decorate_plot = False', so add colorbar and label
cbar = plt.colorbar(kipp_plot.contour_plot, pad=0.05)
cbar.set_label(r'$\log\, \epsilon_\mathrm{nuc}\,/\,\mathrm{erg}\,\mathrm{s}^{-1}\,\mathrm{g}^{-1}$')

# xy labels
plt.xlabel("Time/Myr")
plt.ylabel(r'$m\,/\,\mathrm{M}_\odot$')
plt.title(r'Original 1$\mathrm{M}_\odot$ star till 9Myr')
plt.savefig('./figures/kip_arepo_1M_9Myr_age.pdf') # , dpi='figure', format='pdf', res = 300)


# Further plots: MESA

#choose profile to plot
no = -1
#mass of star over profile == length of profile array: 
# 0 --> 1 M(r)/M* #---> revert y-axis
#star mass
def m_profile(log, i):
    s = 0
    p = log.profile_data(profile_number=i)
    m = p.mass
    qm = p.q
    try:
        dm = p.dm
        return m, qm, dm
    except:
        return m,qm
m1, qm1, dm1 = m_profile(log1,no)
m2, qm2, dm2 = m_profile(log2,no)#/np.max(m_profile(log9,no))


# check if -1 takes the right profile
p = log1.profile_data(profile_number=-1)
age = p.star_age
print(age)

### log(rho_c) vs. log(T_c) plot

#define T profile of last time step
def T_profile(log, i):
    p = log.profile_data(profile_number=i)
    t = p.temperature
    return t
#define last entropy profile
Teff_1 = T_profile(log1, no)
Teff_2 = T_profile(log2, no)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.profile_data(profile_number=i)
    r = p.logRho
    return r

#define last entropy profile
rho_1 = rho_profile(log1, no)
rho_2 = rho_profile(log2, no)


#Mass vs. Temperature plot
#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig, ax = plt.subplots(1, 1, figsize=(columnwidth, columnwidth*3/4))

ax.plot(m1, (rho_1), '-.',label = r'$1M_\odot$ star', color = 'orange')
ax.plot(m2, (rho_2), '--', label = r'$2M_\odot$ star', color = 'orange')

ax.set_ylabel(r'log($\rho_c$) $[kg/m^3]$')
ax.set_xlabel(r'log(T$_c$) $[K]$')
ax.set_title(r'$log(\rho)$ -log(T$_c$-diagram')
plt.legend(loc = 'best', prop={'size': 7})
plt.grid()
plt.savefig('./figures/profile_log(Tc)_vs_log(rhoc).pdf') # , dpi='figure', format='pdf', res = 300)

"""
