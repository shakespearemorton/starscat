import numpy as np
import os
import matplotlib.pyplot as plt

cur = os.getcwd()
h = np.arange(20,40)
r = np.arange(5,20)
siz = 20
ext = np.zeros((15,siz))
for i in range(siz):
    for j in range(siz):
        os.chdir(cur+'/'+repr(i)+'/'+repr(j+1))
        try:
            data = np.loadtxt('qtable',skiprows=14)
            ext[i,j] = data[2]
        except:
            pass
fig, ax = plt.subplots()
im = ax.imshow(ext)
ax.set_xticks(np.arange(len(h)))
ax.set_yticks(np.arange(len(r)))
# ... and label them with the respective list entries
ax.set_xticklabels(h)
ax.set_yticklabels(r)
fig.tight_layout()
plt.ylabel('radius (nm)')
plt.xlabel('height (nm)')
plt.title('probable tip dimensions of large seed small growth GNS')
plt.show()
os.chdir(cur)
plt.savefig('summary.png')
np.savetxt('raw_data.txt',ext)