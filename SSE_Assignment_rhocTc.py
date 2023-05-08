import numpy as np
import matplotlib.pylab as plt
from astropy import constants as const
from scipy import constants as con
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
    p = log.history#.profile_data()#profile_number=i)
    t = p.log_center_T
    return t
#define last entropy profile
Teff_1 = T_profile(log1, no)
Teff_2 = T_profile(log2, no)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.history#.profile_data()#profile_number=i)
    r = p.log_center_Rho
    return r

#define last entropy profile
rho_1 = rho_profile(log1, no)
rho_2 = rho_profile(log2, no)


#Collecting star ages
log1_age = log1.history.star_age
log2_age = log2.history.star_age

age1_min = np.min(log1_age)
age1_max = np.max(log1_age)
age2_min = np.min(log2_age)
age2_max = np.max(log2_age)
age_max = np.max([age1_max, age2_max])

# Star 1 gets ten times older than star 2. --> Using same colorbar for both results in a blue line.
age1_norm = (log1_age-age1_min)/(age_max-age1_min)
age2_norm = (log2_age-age2_min)/(age_max-age2_min)
age1_colors = plt.cm.coolwarm(age1_norm)
age2_colors = plt.cm.coolwarm(age2_norm)

#density vs. Temperature plot
#adjust plotting properties
plt.figure(figsize=(9, 6))
pagewidth, columnwidth = set_plot_defaults()
#fig, ax = plt.subplots(1, 1, figsize=(columnwidth, columnwidth*3/4))

plt.scatter(rho_1,Teff_1, edgecolors=age1_colors, color='white', linewidths=0.5,label = r'$1M_\odot$ star')
plt.scatter(rho_2,Teff_2, edgecolors=age2_colors, color='black', linewidths=0.5, label = r'$2M_\odot$ star')

# define regions referring the equation of state: 
plt.text(2,10, 'Radiation', size = 15)
plt.text(-3.5,4, 'Ideal gas', size = 15)
plt.text(1,4, 'Non-relativistic \n degenerate gas', size = 15)
plt.text(7.5,4, 'Relativistic \n degenerate gas', size = 15)
# add solar core conditions :rho_sun = 1.622e2 # g/cm^3, T_sun = 1.571e7 # K (source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html)
plt.plot(np.log10(1.622e2 ),np.log10(1.571e7), marker = '*',markersize = '15', label = r'Sun', color = 'orange')

# from old script
kB = const.k_B.cgs.value
m_u = const.u.cgs.value
pi = np.pi
h = const.h.cgs.value
c = const.c.cgs.value
me = const.m_e.cgs.value
mH = const.m_p.cgs.value

X, Y, Z = 0.7, 0.28, 0.02
mu = (2*X + 3/4*Y + 1/2*Z)**-1
mue = 2/(1+X)

a = 8*pi**5*kB**4 / (15*h**3*c**3)
Ke = h**2/(20*me) * (3/pi)**(2/3) * 1/mH**(5/3)
Ker = h*c/8 * (3/pi)**(1/3) * 1/mH**(4/3)

rho = np.logspace(-4, 10, 800)

T1 = (3*kB/(a*mu*m_u) * rho)**(1/3)               # hergeleitet auf schmierblock auf ipad
T2 = Ke*rho**(2/3)/mue**(5/3) * mu*m_u/kB
T3 = Ker*rho**(1/3)/mue**(4/3) * mu*m_u/kB
rho4 = (Ker/Ke)**3 * mue
T4 = (3*Ke/a * (rho/mue)**(5/3))**(1/4)
T5 = (3*Ker/a * (rho/mue)**(4/3))**(1/4)

plt.plot(np.log10(rho), np.log10(T1), color="saddlebrown", lw=3, label=r"$P_{id}=P_{rad}$")
plt.plot(np.log10(rho[rho<rho4]), np.log10(T2[rho<rho4]), color="darkgreen", lw=3, label=r"$P_{id}=P_{NR,e}^D$")
plt.plot(np.log10(rho[rho>rho4]), np.log10(T2[rho>rho4]), color="darkgreen", ls=":")
plt.plot(np.log10(rho[rho<rho4]), np.log10(T3[rho<rho4]), color="darkmagenta", ls=":")
plt.plot(np.log10(rho[rho>rho4]), np.log10(T3[rho>rho4]), color="darkmagenta", lw=3, label=r"$P_{id}=P_{ER,e}^D$")
plt.plot(np.log10(len(T2[T2<T3])*[rho4]), np.log10(T2[T2<T3]), color="black", lw=3, label=r"$P_{NR,e}^D=P_{ER,e}^D$")
plt.plot(np.log10(rho), np.log10(T4), ls="-.", color="lightgreen", label=r"$P_{rad}=P_{NR,e}^D$")
plt.plot(np.log10(rho), np.log10(T5), ls="--", color="peachpuff", label=r"$P_{rad}=P_{ER,e}^D$")

plt.fill_between(np.log10(rho), np.log10(T1), np.log10(1e11), color=col["orange"], alpha = 0.5, label="Radiation")
plt.fill_between(np.log10(rho[rho<rho4]), np.log10(T2[rho<=rho4]), np.log10(T1[rho<=rho4]), alpha = 0.5, color=col["sky blue"], label="Ideal Gas")
plt.fill_between(np.log10(rho[rho>rho4]), np.log10(T3[rho>=rho4]), np.log10(T1[rho>=rho4]), alpha = 0.5, color=col["sky blue"])
plt.fill_between(np.log10(rho[rho<rho4]), np.log10(1e3), np.log10(T2[rho<rho4]), alpha = 0.5, color=col["bluish green"], label="NR degen.")
plt.fill_between(np.log10(rho[rho>rho4]), np.log10(1e3), np.log10(T3[rho>rho4]), alpha = 0.5, color=col["reddish purple"], label="ER degen.")

plt.ylim(3,11)
plt.xlim(-4,10)
plt.xlabel(r'log10($\rho_c$) $[kg/m^3]$',size=15)
plt.ylabel(r'log10(T$_c$) $[K]$',size=15)
plt.title(r'$log(\rho_c)$ -log(T$_c$)-diagram with eos',size=18)
plt.legend(loc = 'best', prop={'size': 8})
plt.grid()

sm = plt.cm.ScalarMappable(cmap='coolwarm')
sm.set_array([])
# plt.colorbar(sm)
cbar = plt.colorbar(sm, ticks=np.linspace(0, 1, 6))
cbar.ax.set_yticklabels(np.linspace(0, age1_max/10**9, 6))

plt.show()

# plt.savefig('./figures/profile_log(Tc)_vs_log(rhoc).pdf') 
