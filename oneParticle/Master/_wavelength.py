import numpy as np

wl = np.linspace(0.708,0.808,20) #Wavelength range of interest (in micron)


with open('ddscat1.par', 'r') as file :
    filedata = file.read()
if len(wl) == 1:
    filedata = filedata.replace('REPWAVES',"{:.4f}".format(wl))
else:
    filedata = filedata.replace('REPWAVES',"{:.4f}".format(wl[REPLACE -1]))
with open('ddscat.par', 'w') as file:
    file.write(filedata)
