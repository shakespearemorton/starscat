from Star import *

aeff = 77
radius = 51.5
max_r = 113.3
poss = np.loadtxt('poss.txt')
tipH,tipR,num,sh,ran = poss[1]
star = nanostar(radius,tipR,tipH,aeff)
d2 = np.array(unique_rows(star.shape[:,:2]))
ae = np.sqrt(len(d2)/np.pi)
print(ae)
plt.scatter(d2[:,0],d2[:,1])
plt.title(str(len(star.shape)))
plt.savefig('test1.png')