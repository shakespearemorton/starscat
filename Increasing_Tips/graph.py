import numpy as np
import os
import matplotlib.pyplot as plt
#Figure 5

folder = ['8x20','10x24','10x25','8x16','12x24']
colors = ['orange','indigo','maroon','deepskyblue','hotpink']
plt.rcParams.update({'font.size': 14})
plt.rcParams["figure.figsize"] = (22,4)

cur = os.getcwd()
slope = []
plt.figure(dpi=1200)
k=0
plt.subplot(1,3,1)
for i in folder:
    os.chdir(cur+'/'+i)
    data = np.loadtxt('summary.txt')
    siz = data[0,:]
    siz += 1
    siz *= 24e-3
    vol = ((4/3)*np.pi*(siz*1e3)**3)
    v = (vol)**(2/3)
    m_ext = 6.022e23*(10**-17/np.log(10))*(9*np.pi/16)**(1/3)*v *data[3,:]+data[7,:]
    plt.plot(v,m_ext,'.',label = i)
    k+=1
plt.xlabel('$Volume^{2/3}$ ($nm^2$)')
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.ylabel('\u03B5 ($M^{-1}$ $cm^{-1}$)')
os.chdir(cur)

#plt.savefig('molar_extinction.png',format='png',dpi = 1200,bbox_inches='tight')

#Figure 4C

k=0
#plt.figure(dpi=1200)
plt.subplot(1,3,2)
for i in folder:
    os.chdir(cur+'/'+i)
    data = np.loadtxt('summary.txt')
    siz = data[0,:]
    siz += 1
    siz *= 24e-3
    vol = ((4/3)*np.pi*(siz*1e3)**3)
    scattering = data[7,:]/data[7,0]
    plt.plot((vol),scattering,'.',label = i)
    k+=1
#plt.legend()
plt.xlabel('Volume ($nm^3$)')
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.ylabel('Normalised $Q_{sca}$ @ LSPR (a.u.)')
os.chdir(cur)
#plt.savefig('scattering.png',format='png',dpi = 1200,bbox_inches='tight')

k=0
#plt.figure(dpi=1200)
plt.subplot(1,3,3)
for i in folder:
    os.chdir(cur+'/'+i)
    data = np.loadtxt('summary.txt')
    siz = data[0,:]
    siz += 1
    siz *= 24e-3
    vol = ((4/3)*np.pi*(siz*1e3)**3)
    scattering = data[3,:]/data[3,0]
    plt.plot((vol),scattering,'.',label = i)
    k+=1
#plt.legend(bbox_to_anchor=(1, 0.5))
plt.xlabel('Volume ($nm^3$)')
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.ylabel('Normalised $Q_{abs}$ @ LSPR (a.u.)')
os.chdir(cur)
plt.savefig('summary2.png',format='png',dpi = 1200,bbox_inches='tight')