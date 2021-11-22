#----------------------------Imports------------------------------
import numpy as np
import pandas as pd
import os
from func import *

Evolution = pd.read_csv("Evolution.csv")
vari = list(Evolution.columns.values.tolist())
Progress = np.loadtxt('Progress.csv',skiprows=1,delimiter=',')
x = np.loadtxt('population.txt')
Evolution = scribe(Evolution,param,vari,data)
Evolution.to_csv('Evolution.csv',index=False)
P_space=loadstart()
pop = genes(Progress[:,-1],P_space,len(x),Progress[:,0:len(vari)-1])
np.savetxt("population.txt",pop)