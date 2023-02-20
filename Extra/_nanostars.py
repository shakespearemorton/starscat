import numpy as np
import math
import random
from scipy.spatial.transform import Rotation

def writeVMD(pos,R=0):
    with open( 'VMD.txt', 'w' ) as g:
        num = len(pos)
        g.write(repr(num)+'\n\n')
        for t in range(len(pos)):
            xi = pos[t,0]
            yi = pos[t,1]
            zi = pos[t,2]
            g.write( "C {0:.5f} {1:.5f} {2:.5f} \n".format( pos[t,0], pos[t,1], pos[t,2] ) )
    return

def nanostar(R,coneR,coneH,num,gammaR=0,gammaH=0,N=0.1):
    pos = sphere(R,N)
    pos = unique_rows(pos)
    n=0
    if num ==0:
        pass
    else:
        while n <= num:
            con = cone(coneR+(random.uniform(-gammaR,gammaR)),coneH+(random.uniform(-gammaH,gammaH)),N,R)
            r = Rotation.random(1)
            con = r.apply(con)
            pos = np.array(pos)
            pos = np.concatenate((pos,con))
            pos = np.array(pos).astype(int)
            pos = list(pos)
            pos = unique_rows(pos)
            n+=1
    writeVMD(pos)
    writeDDSCAT(pos)
    return(pos)

def coreShellNanostar(thick,R,coneR,coneH,num,gammaR=0,gammaH=0,N=0.8):
    pos = sphere(R+thick,N)
    n=0
    while n <= num:
        con = cone(coneR+(random.uniform(-gammaR,gammaR)),coneH+(random.uniform(-gammaH,gammaH)),N,R+thick)
        r = Rotation.random(1)
        con = r.apply(con)
        pos = np.array(pos)
        pos = np.concatenate((pos,con))
        pos = np.array(pos).astype(int)
        pos = list(pos)
        pos = unique_rows(pos)
        n+=1
    writeVMD(pos,R)
    writeDDSCAT(pos,R)
    return(pos)


def cone(coneR,coneH,N,R=0):
    coneT = np.arctan(coneR/coneH)
    hyp = np.sqrt(coneR**2+coneH**2)
    coneR = np.sin(coneT)*hyp
    T = 0
    if R != 0:
        T = -np.sqrt(R**2-coneR**2)+R
    H = coneH+T
    cone = []
    for xi in np.linspace(int(-coneR), int(coneR),int(coneR*2/N)+1):
        for yi in np.linspace(int(-coneR), int(coneR),int(coneR*2/N)+1):
            for zi in np.linspace(int(0), int(H),int(H/N)+1):
                if ((abs(zi) < H) and (np.sqrt(xi**2+yi**2) < (H-zi)/(float(H))*(coneR))):
                    cone.append([xi,yi,zi+int(R-(T))])
    return np.array(cone)

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def writeDDSCAT(pos,R=0):
    tot = pos
    nParticles = len(tot)
    x = int(np.max(tot[0,:]))- int(np.min(tot[0,:]))
    y = int(np.max(tot[1,:]))- int(np.min(tot[1,:]))
    z = int(np.max(tot[2,:]))- int(np.min(tot[2,:]))
    with open( 'shape.dat', 'w' ) as g:
        g.write(' >TARREC   rectangular prism; AX,AY,AZ= ' +repr(x)+' '+repr(y)+' '+repr(z)+'\n     '+repr(nParticles)+' = NAT \n')
        g.write('  1.000000  0.000000  0.000000 = A_1 vector\n')
        g.write('  0.000000  1.000000  0.000000 = A_2 vector\n')
        g.write('  1.000000  1.000000  1.000000 = lattice spacings (d_x,d_y,d_z)/d\n')
        g.write('  0.000000  0.000000  0.000000 = lattice offset x0(1-3) = (x_TF,y_TF,z_TF)/d for dipole 0 0 0\n')
        g.write('       JA  IX  IY  IZ ICOMP(x,y,z)\n')
        for t in range(len(pos)):
            xi = pos[t,0]
            yi = pos[t,1]
            zi = pos[t,2]
            g.write( "      {0:.0f}   {1:.0f}   {2:.0f}   {3:.0f} 1 1 1 \n".format( t+1, pos[ t, 0 ], pos[ t, 1 ], pos[ t, 2 ] ) )
    return

def sphere(R,N):
    pos=[]
    for xi in np.linspace(int(-R), int(R),int(2*R/N)+1):
        for yi in np.linspace(int(-R), int(R),int(2*R/N)+1):
            for zi in np.linspace(int(-R), int(R),int(2*R/N)+1):
                if xi**2+yi**2+zi**2 <= (R)**2:
                    pos.append([xi,yi,zi])
    pos = np.array(pos).astype(int)
    pos = unique_rows(pos)
    return(pos)

h = np.arange(20,40)
r = np.arange(5,25)
R,tipR,tipH,gammaR,gammaH,num = 41/2,r[REPLACER],h[REPLACEH-1],0,0,20
pos= nanostar(R,tipR,tipH,num,gammaR,gammaH)
v = len(pos)
aeff = (v*(3/4)/np.pi)**(1/3)
with open('_ddscat.par', 'r') as file :
    filedata = file.read()
filedata = filedata.replace('REPRAD',"{:.4f}".format(aeff/1000))
with open('ddscat.par', 'w') as file:
    file.write(filedata)
