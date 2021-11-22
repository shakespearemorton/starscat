import numpy as np
import os
import matplotlib.pyplot as plt

#3 for absorption
#7 for scattering
#-2 for enhancement

folder = ['8x20','10x24','10x25','8x16','12x24']
names= ['8:20','10:24','10:25','8:16','12:24']
cur = os.getcwd()
for j in range(len(folder)):
    i = folder[j]
    k = names[j]
    os.chdir(cur+'/'+i)
    data = np.loadtxt('summary.txt')
    tips = np.arange(len(data[3,:]))
    plt.plot(tips,data[3,:],'.',label=k)
os.chdir(cur)
plt.xlabel('Number of tips')
plt.ylabel('Absorption Efficiency @ LSPR (a.u.)')
plt.title('')
#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
plt.legend()
plt.savefig('absorption.png', bbox_inches='tight',format='png', dpi=1200)
