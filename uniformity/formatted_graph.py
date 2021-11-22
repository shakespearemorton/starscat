#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 08:33:16 2021

@author: WilliamMorton
"""
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 14})
plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

t  = np.linspace(1,30,10)
extR = [6.458449999999999, 5.949085999999999, 6.205022000000001, 5.98026, 5.958887999999999, 5.339492, 5.311136, 5.6025, 5.521859183673469, 5.191368]
fwhmR = [165.47938775510207, 168.5422, 168.5422, 172.74540000000002, 180.6096, 188.4742, 183.18580000000003, 187.11860000000001, 185.95489795918368, 189.42320000000004]
extH = [6.200578, 5.853936, 6.138515999999999, 5.369748, 5.225102000000001, 4.895650000000001, 4.892035999999999, 4.295520000000001, 4.320738, 4.189668]
fwhmH = [166.91500000000005, 178.57620000000003, 182.77899999999997, 198.91500000000005, 218.1692, 223.03612244897963, 228.7448, 230.08375, 241.66541666666663, 236.65581395348838]

plt.figure(dpi=1200)
fig, ax1 = plt.subplots()

color = 'tab:red'
color2 = 'tab:blue'
ax1.set_xlabel('% Variance of Gaussian')
ax1.set_ylabel('$Q_{ext}$ (a.u.)',color=color)
ax1.plot(t, extR,'--', color=color)
ax1.plot(t, extH, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


ax2.set_ylabel('FWHM (nm)',color=color2)  
ax2.plot(t, fwhmR, color=color2)
ax2.plot(t, fwhmH,'--', color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('uniformity.png',format='png',dpi = 1200)