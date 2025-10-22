# -*- coding: utf-8 -*-
"""
Very brief analysis of the Oscillation Cases
"""

import numpy as np
import os
import glob


amoc_oscillations = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Oscillations/all_amoc_oscillations.txt")     

# ---------- Let' Analyse ---------------------------------------------------
print("Total Number of Model Runs with Oscillations" ,len(amoc_oscillations))

for n in range(7):
    print(np.unique(amoc_oscillations[:,n]))

'''
At total of 13 959 cases, = 4.5 % of all model runs. 
They were constricted to (i) negative coupling between AMOC and WAIS, and
    (ii) high coupling strengths of 0.7 to 1. 
    Nonetheless, oscillations occurred in each scenario and with 
    nearly all ECS values (994 of 1000 cases).
'''
