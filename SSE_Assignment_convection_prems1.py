import numpy as np
import matplotlib.pylab as plt
#%matplotlib inline
from scipy import constants as con

# Plotting script for SSE assignment
from mymisc import *


# convection takes place when adia > rad1
# Use only one profile.
# profile 4 is pre-MS.


import mesa_reader as mr
#diretions of the LOG-files
log1 = mr.MesaLogDir('./1M_prems_to_wd/LOGS')
log2 = mr.MesaLogDir('./2M_prems_to_wd/LOGS')

prems_profile_number = 1
ms_profile_number = 7

### convection plots for pre-ms and ms
no = -1
#define adiabatic convection profile of last time step
def adia_profile(log,i): #,i added
    p = log.profile_data(profile_number=i)
    t = p.grada
    return t

adia1_prems = adia_profile(log1, prems_profile_number)
adia1_ms = adia_profile(log1, ms_profile_number)
adia2_prems = adia_profile(log2, prems_profile_number)
adia2_ms = adia_profile(log2, ms_profile_number)

#define rho profile of last time step
def rho_profile(log, i):
    p = log.profile_data(profile_number=i)
    r = p.gradr
    return r

#define last entropy profile
rad1_prems = rho_profile(log1, prems_profile_number)
rad1_ms = rho_profile(log1, ms_profile_number)
rad2_prems = rho_profile(log2, prems_profile_number)
rad2_ms = rho_profile(log2, ms_profile_number) # profile number 7 acts the same for 2M and 1M


def radius_profile(log,i): #,i added
    p = log.profile_data(profile_number=i)
    R = p.logR
    return 10**R

R1_prems = radius_profile(log1, prems_profile_number)
R1_ms = radius_profile(log1, ms_profile_number)
R2_prems = radius_profile(log2, prems_profile_number)
R2_ms = radius_profile(log2, ms_profile_number)

R1_prems_rel = adia1_prems/rad1_prems
R1_ms_rel = adia1_ms/rad1_ms
R2_prems_rel = adia2_prems/rad2_prems
R2_ms_rel = adia2_ms/rad2_ms

threshhold = 1
convection_mask1_prems = R1_prems_rel >= threshhold
convection_mask1_ms = R1_ms_rel >= threshhold
convection_mask2_prems = R2_prems_rel >= threshhold
convection_mask2_ms = R2_ms_rel >= threshhold

#Mass vs. Temperature plot
#adjust plotting properties
pagewidth, columnwidth = set_plot_defaults()
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(columnwidth, columnwidth*3/4))

ax1.plot(R1_prems, R1_prems_rel, '-.',label = r'$1M_\odot$ star', color = 'orange')
ax1.fill_between(R1_prems, np.min(R1_prems_rel), np.max(R1_prems_rel), where=convection_mask1_prems, color='gray', alpha=0.4, transform=ax1.get_xaxis_transform(), label='convection')
ax2.plot(R2_prems, R2_prems_rel, '--', label = r'$2M_\odot$ star', color = 'blue')
ax2.fill_between(R2_prems, np.min(R2_prems_rel), np.max(R2_prems_rel), where=convection_mask2_prems, color='gray', alpha=0.4, transform=ax2.get_xaxis_transform(), label='convection')

ax1.set_ylabel(r'$\nabla_{ad}/\nabla_{rad}$')
ax2.set_ylabel(r'$\nabla_{ad}/\nabla_{rad}$')
ax2.set_xlabel(r'Radius ($R_\odot$)')
fig1.suptitle(r'Convection in a pre-main sequence star')
ax1.legend(loc = 'best', prop={'size': 7})
ax2.legend(loc = 'best', prop={'size': 7})
ax1.grid()
ax2.grid()
# plt.show()
plt.savefig('./figures/convection1_prems.pdf') 

fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(columnwidth, columnwidth*3/4))

ax1.plot(R1_ms, R1_ms_rel, label = r'$1M_\odot$ star', color = 'orange')
ax1.fill_between(R1_ms, np.min(R1_ms_rel), np.max(R1_ms_rel), where=convection_mask1_ms, color='gray', alpha=0.4, transform=ax1.get_xaxis_transform(), label='convection')
ax2.plot(R2_ms, R2_ms_rel, label = r'$2M_\odot$ star', color = 'blue')
ax2.fill_between(R2_ms, np.min(R1_ms_rel)-2, np.max(R2_ms_rel)+2, where=convection_mask2_ms, color='gray', alpha=0.4, transform=ax2.get_xaxis_transform(), label='convection')
ax2.set_ylim([np.min(R1_ms_rel)-0.2, np.max(R2_ms_rel)+0.2])  # Added because of weird behaviour of ax2.fill_between

ax1.set_ylabel(r'$\nabla_{ad}/\nabla_{rad}$')
ax2.set_ylabel(r'$\nabla_{ad}/\nabla_{rad}$')
ax2.set_xlabel(r'Radius ($R_\odot$)')
fig2.suptitle(r'Convection in a main sequence star')
ax1.legend(loc = 'best', prop={'size': 7})
ax2.legend(loc = 'best', prop={'size': 7})
ax1.grid()
ax2.grid()

# plt.show()
plt.savefig('./figures/convection1_ms.pdf') 



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
    data = prof.get("grada")/prof.get("gradr")
    return data
    

kipp_args = mkipp.Kipp_Args(logs_dirs = ['./1M_prems_to_wd/LOGS'], save_file = False, xaxis="star_age", time_units = "Myr",extractor = conv, decorate_plot = False)

mkipp.kipp_plot(kipp_args, axis=ax1)
kipp_plot = mkipp.kipp_plot(kipp_args, axis=ax2)
bar = fig.colorbar(kipp_plot.contour_plot, cax=ax3)

bar.set_label("$\Delta _$adia$/ \Delta_$radi$ $") # $\\log_{10}|\\epsilon_{\\rm nuc}|$")

history = mesa_data.mesa_data("./1M_prems_to_wd/LOGS/history.data", read_data_cols = ["star_age","log_R", "center_h1", "center_he4"])
for i, center_h1 in enumerate(history.get("center_h1")):
    if center_h1 < 1e-3:
        age_tams = history.get("star_age")[i]/1e6
        break
for i, center_he4 in enumerate(history.get("center_he4")):
    if center_he4 < 1e-3:
        age_hedep = history.get("star_age")[i]/1e6
        break
# Not center_h1 > 1e-3: is main sequence???
# prems: all 12C gets converted into 14N (not usefull with profiles)
# Once the energy generated by hydrogen fusion compensates for the energy loss at the surface, the star stops contracting and setlles on the zero-age main sequence.
# Not yet any nuclear burning, energy source for its L is grav contraction.
# Profile 1 is surely a prems star. 
# h mass starts slowly decreasing from profile 3 forward (and increases in pace).
# Profile 7 is almost halfway its h supply and he is still increasing --> must be ms
ax1.set_xlim([0,age_tams])
ax2.set_xlim([age_tams,age_hedep])
ax2.set_xlabel("Star age (Myr)")
ax2.set_xlabel("Star age (Myr)")
ax1.set_ylabel("Stellar radius (solar radii)")
ax2.yaxis.set_ticklabels([])
ax3.yaxis.set_ticklabels([])
ax1.set_title('Convecting regions: pre-ms')
ax2.set_title('and in ms')
# plt.savefig("./figures/kippenhahn_convection_1M.pdf")
plt.show()
























"""
Backup:


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
    data = prof.get("grada")/prof.get("gradr")
    return data
    

kipp_args = mkipp.Kipp_Args(logs_dirs = ['./1M_prems_to_wd/LOGS'], save_file = False, xaxis="star_age", time_units = "Myr",extractor = conv, decorate_plot = False)

mkipp.kipp_plot(kipp_args, axis=ax1)
kipp_plot = mkipp.kipp_plot(kipp_args, axis=ax2)
bar = fig.colorbar(kipp_plot.contour_plot, cax=ax3)

bar.set_label("$\Delta _$adia$/ \Delta_$radi$ $") # $\\log_{10}|\\epsilon_{\\rm nuc}|$")

history = mesa_data.mesa_data("./1M_prems_to_wd/LOGS/history.data", read_data_cols = ["star_age","log_R", "center_h1", "center_he4"])
for i, center_h1 in enumerate(history.get("center_h1")):
    if center_h1 < 1e-3:
        age_tams = history.get("star_age")[i]/1e6
        break
for i, center_he4 in enumerate(history.get("center_he4")):
    if center_he4 < 1e-3:
        age_hedep = history.get("star_age")[i]/1e6
        break
# Not center_h1 > 1e-3: is main sequence???
# prems: all 12C gets converted into 14N (not usefull with profiles)
# Once the energy generated by hydrogen fusion compensates for the energy loss at the surface, the star stops contracting and setlles on the zero-age main sequence.
# Not yet any nuclear burning, energy source for its L is grav contraction.
# Profile 1 is surely a prems star. 
# h mass starts slowly decreasing from profile 3 forward (and increases in pace).
# Profile 7 is almost halfway its h supply and he is still increasing --> must be ms
ax1.set_xlim([0,age_tams])
ax2.set_xlim([age_tams,age_hedep])
ax2.set_xlabel("Star age (Myr)")
ax2.set_xlabel("Star age (Myr)")
ax1.set_ylabel("Stellar radius (solar radii)")
ax2.yaxis.set_ticklabels([])
ax3.yaxis.set_ticklabels([])
ax1.set_title('Convecting regions: pre-ms')
ax2.set_title('and in ms')
# plt.savefig("./figures/kippenhahn_convection_1M.pdf")
plt.show()

"""