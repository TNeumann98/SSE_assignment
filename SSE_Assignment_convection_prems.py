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


### convection plots for pre-ms and ms
no = -1
#define adiabatic convection profile of last time step
def adia_profile(log):
    p = log.profile_data()#profile_number=i)
    t = p.grada
    return t

adia1 = adia_profile(log1)
adia2 = adia_profile(log2)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.profile_data()#profile_number=i)
    r = p.gradr
    return r

#define last entropy profile
rad1 = rho_profile(log1, no)
rad2 = rho_profile(log2, no)


#Mass vs. Temperature plot
#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig, ax = plt.subplots(1, 1, figsize=(columnwidth, columnwidth*3/4))

ax.plot(adia1/rad1, '-.',label = r'$1M_\odot$ star', color = 'orange')
ax.plot(adia2/rad2, '--', label = r'$2M_\odot$ star', color = 'blue')

ax.set_ylabel(r'log($\rho_c$) $[kg/m^3]$')
ax.set_xlabel(r'log(T$_c$) $[K]$')
ax.set_title(r'$log(\rho_c)$ -log(T$_c$)-diagram')
plt.legend(loc = 'best', prop={'size': 7})
plt.grid()
plt.ylim(0,3)
#plt.show()
plt.savefig('./figures/convection_prems.pdf') 

#--------------------------------------------------------------------------------------------
###try via Kippenhahn plotter [code from website: https://github.com/orlox/mkipp]
import mkipp
import kipp_data
import mesa_data

fig = plt.figure()
spec = fig.add_gridspec(ncols=3, nrows=1, wspace=0.2, width_ratios = [5,5,1])
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[0, 1])
ax3 = fig.add_subplot(spec[0, 2])

# special define c-axis: convection criterion
def conv(identifier, log10_on_data, prof, return_data_columns = False):
    if return_data_columns:
        return ["grada", "gradr"]
    data = prof.get("grada")-prof.get("gradr")
    #print(prof.get("grada"),data)
    return data
    

kipp_args = mkipp.Kipp_Args(logs_dirs = ['./1M_prems_to_wd/LOGS'], show_conv=True, save_file = False, xaxis="star_age", time_units = "Myr", decorate_plot = False) #extractor = conv

mkipp.kipp_plot(kipp_args, axis=ax1)
kipp_plot = mkipp.kipp_plot(kipp_args, axis=ax2)
bar = fig.colorbar(kipp_plot.contour_plot, cax=ax3)

bar.set_label("$\\log_{10}|\\epsilon_{\\rm nuc}|$")
#bar.set_label("$\\Delta _{adia}/ \\Delta_{radi} $") # $\\log_{10}|\\epsilon_{\\rm nuc}|$")

history = mesa_data.mesa_data("./1M_prems_to_wd/LOGS/history.data", read_data_cols = ["star_age","log_R", "center_h1", "center_he4"])
for i, center_h1 in enumerate(history.get("center_h1")):
    if center_h1 < 1e-3:
        age_tams = history.get("star_age")[i]/1e6
        break
for i, center_he4 in enumerate(history.get("center_he4")):
    if center_he4 < 1e-3:
        age_hedep = history.get("star_age")[i]/1e6
        break
ax1.set_xlim([0,age_tams])
ax2.set_xlim([age_tams,age_hedep])
ax1.set_xlabel("Star age (Myr)")
ax2.set_xlabel("Star age (Myr)")
ax1.set_ylabel("Stellar radius (solar radii)")
ax2.yaxis.set_ticklabels([])
ax3.yaxis.set_ticklabels([])
ax1.set_title('Convecting regions: pre-ms')
ax2.set_title('and in ms')
plt.show()
plt.savefig("./figures/kippenhahn_convection_1M.pdf")
