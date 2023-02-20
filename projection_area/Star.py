import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.spatial.transform import Rotation
import warnings
warnings.filterwarnings("ignore")
import time, sys
from numpy import random

def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2:.1}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

class nanostar:
    '''
    pvol = aeff / radius of core (obviously needs to be greater than 1)
    
    '''
    def __init__(self, radius, tipr, tiph, aeff, gammar = 0, gammah = 0, surface = 0, rounding = 0):
        self.radius = radius
        self.tipr = tipr
        self.tiph = tiph
        self.aeff = aeff
        self.gammar = gammar
        self.gammah = gammah
        
        
        print('\n--- Creating Star ---\n')
        if surface == 0:
            print('star for DDA calculations')
            print('will output shape.dat and an image')
        self.shape = sphere(radius)
        self.shape = unique_rows(self.shape)
        print('generating tip, this may take a moment...')
        self.tip = cone(tipr,tiph,radius)
        print('tip generated')
        countTips(self)
        tipDirections(self)
        print('applying tips')
        pos = self.shape
        for i in self.tipv:
            r = Rotation.from_matrix(rotation_matrix_from_vectors(i,self.tip[-1]))
            cone2 = r.apply(self.tip)
            pos = np.concatenate((pos,cone2))
        pos = pos.astype(int)
        self.shape = unique_rows(pos)
        print('\n---Writing Outputs---\n')
        writeVMD(self.shape)
        print('VMD file written')
        writeDDSCAT(self.shape)
        print('DDSCAT shape file written')
        print('\n--- Finished ---')
        
def writeVMD(pos,filename = 'VMD.txt'):
    with open( filename, 'w' ) as g:
        num = len(pos)
        g.write(repr(num)+'\n\n')
        for t in range(num):
            g.write( "C {0:.5f} {1:.5f} {2:.5f} \n".format( pos[t,0], pos[t,1], pos[t,2] ) )
            
def writeDDSCAT(pos):
    nParticles = len(pos)
    x = int(np.max(pos[0,:]))- int(np.min(pos[0,:]))
    y = int(np.max(pos[1,:]))- int(np.min(pos[1,:]))
    z = int(np.max(pos[2,:]))- int(np.min(pos[2,:]))
    with open( 'shape.dat', 'w' ) as g:
        g.write(' >TARREC   rectangular prism; AX,AY,AZ= ' +repr(x)+' '+repr(y)+' '+repr(z)+'\n     '+repr(nParticles)+' = NAT \n')
        g.write('  1.000000  0.000000  0.000000 = A_1 vector\n')
        g.write('  0.000000  1.000000  0.000000 = A_2 vector\n')
        g.write('  1.000000  1.000000  1.000000 = lattice spacings (d_x,d_y,d_z)/d\n')
        g.write('  0.000000  0.000000  0.000000 = lattice offset x0(1-3) = (x_TF,y_TF,z_TF)/d for dipole 0 0 0\n')
        g.write('       JA  IX  IY  IZ ICOMP(x,y,z)\n')
        for t in range(nParticles):
            xi = pos[t,0]
            yi = pos[t,1]
            zi = pos[t,2]
            g.write( "      {0:.0f}   {1:.0f}   {2:.0f}   {3:.0f} 1 1 1 \n".format( t+1, pos[ t, 0 ], pos[ t, 1 ], pos[ t, 2 ] ) )
    return

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def sphere(R):
    pos = []
    N = 2
    for xi in np.linspace(int(-R), int(R),int(R*N)):
        for yi in np.linspace(int(-R), int(R),int(R*N)):
            for zi in np.linspace(int(-R), int(R),int(R*N)):
                if xi**2+yi**2+zi**2 <= (R)**2:
                    pos.append([xi,yi,zi])
    return pos

def cone(coneR,coneH,R=0):
    global H
    global coneR1
    coneT = np.arctan(coneR/coneH)
    hyp = np.sqrt(coneR**2+coneH**2)
    coneR = np.sin(coneT)*hyp
    T = 0
    if R != 0:
        T = -np.sqrt(R**2-coneR**2)+R
    H = coneH+T
    cone = []
    k = 0
    for xi in np.linspace(int(-coneR), int(coneR),int(coneR*2*N)):
        for yi in np.linspace(int(-coneR), int(coneR),int(coneR*2*N)):
            for zi in np.linspace(int(0), int(H),int(H*N)):
                k+=1
                #update_progress(k/N**3)
                if ((abs(zi) < H) and (np.sqrt(xi**2+yi**2) < (H-zi)/(float(H))*(coneR))):
                    cone.append([xi,yi,zi+int(R-(T))])
    coneR1 = coneR
    return np.array(cone)
                    
    

              
    

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix
    
def countTips(star):
    avg_ae = []
    avg_tips = []
    avg_vol = []
    con_prime = cone(star.tipr,star.tiph,star.radius)
    for i in range(12):
        star.num = 0
        pos = star.shape
        d2 = np.array(unique_rows(pos[:,:2]))
        ae = np.sqrt(len(d2)/np.pi)
        sa_remain = (4*np.pi*star.radius**2)
        while ae <= star.aeff:
            r = Rotation.random(1)
            con = r.apply(con_prime)
            pos = np.array(pos)
            pos = np.concatenate((pos,con))
            pos = np.array(pos).astype(int)
            pos = list(pos)
            pos = unique_rows(pos)
            d2 = np.array(unique_rows(pos[:,:2]))
            ae = np.sqrt(len(d2)/np.pi)
            star.num+=1
            sa_remain -= (np.pi*(coneR1)**2)
            if sa_remain < 0:
                break
        avg_ae.append(ae)
        avg_tips.append(star.num)
        avg_vol.append(len(pos))
        plt.figure()
        plt.scatter(d2[:,0],d2[:,1],color='gold')
        plt.title(str(len(pos)))
        print(len(pos))
        plt.savefig('test'+str(len(avg_ae))+'.png')
        

    for i in range(6):
        star.num = 0
        pos = star.shape
        d2 = np.array(unique_rows(pos[:,:2]))
        ae = np.sqrt(len(d2)/np.pi)
        sa_remain = (4*np.pi*star.radius**2)
        while ae <= star.aeff:
            con_prime = cone(star.tipr*random.normal(loc=1,scale=star.gammar),star.tiph*random.normal(loc=1,scale=star.gammah),star.radius)
            r = Rotation.random(1)
            con = r.apply(con_prime)
            pos = np.array(pos)
            pos = np.concatenate((pos,con))
            pos = np.array(pos).astype(int)
            pos = list(pos)
            pos = unique_rows(pos)
            d2 = np.array(unique_rows(pos[:,:2]))
            ae = np.sqrt(len(d2)/np.pi)
            star.num+=1
            sa_remain -= (np.pi*(coneR1)**2)
            if sa_remain < 0:
                break
        avg_ae.append(ae)
        avg_tips.append(star.num)
        avg_vol.append(len(pos))
        plt.figure()
        plt.scatter(d2[:,0],d2[:,1],color='gold')
        plt.title(str(len(pos)))
        print(len(pos))
        plt.savefig('test'+str(len(avg_ae))+'.png')
        
    star.num = np.mean(np.array(avg_tips))
    star.aeff = np.mean(np.array(avg_ae))
    star.ran = np.max(avg_vol)-np.min(avg_vol)
    star.shape = np.mean(avg_vol)
    
def tipDirections(star):
    print('\n--- Placing tips ---\n')
    print('tips will be placed equidistant from one another')
    star.tipv = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(int(star.num)):
        y = 1 - (i / float(star.num - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        star.tipv.append(rescale(np.array([x,y,z]),star.radius))
        
def rescale(r1,r):
  mod = np.sqrt( ( r1**2 ).sum() )
  teta = np.arctan( r1[ 1 ]  / r1[ 0 ] )
  if r1[ 0 ] > 0:
    phi = np.arccos( r1[ 2 ] / mod )
  else:
    phi = 2.0 * np.pi - np.arccos( r1[ 2 ] / mod ) 
  rvec = surface( phi,teta,r)

  return rvec

def surface( p, t,r):
  x = r * np.sin( p ) * np.cos( t )
  y = r * np.sin( p ) * np.sin( t )
  z = r * np.cos( p ) 
  return (  [x, y, z]  ) 
