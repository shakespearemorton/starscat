from make_star import *

'''
Purpose:
    This study looks at the impact of non-uniform tips on the optical properties of gold nanostars
    
    In this particular example, the tip Radius is varied

'''

x = np.linspace(0.01,0.3,10) # Gaussian Variance from 1-30% of the average tip

R = 24
tipR = 12
tipH = 24
gammaR = x[REPLACE]
gammaH = 0
num = 13

pos= nanostar(R,tipR,tipH,num,gammaR,gammaH)