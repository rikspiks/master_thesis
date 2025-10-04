# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 10:33:53 2025

@author: LENOVO
"""

import os
import re
import numpy as np
import glob
#import matplotlib.pyplot as plt


#plot style things
#plt.style.use('seaborn-v0_8-white')
#plt.rcParams['figure.figsize'] = (12, 9)
#plt.rcParams.update({
 #   'xtick.labelsize': 19,
 #   'ytick.labelsize': 19,
 #   'axes.titlesize': 25,
 #   'axes.labelsize': 22,
 #   'axes.titlepad': 27,       # Abstand Titel
 #   'axes.labelpad': 17,       # Abstand Achsenbeschriftung
 #   'xtick.major.pad': 9,      # Abstand X-Ticks
 #  'ytick.major.pad': 9       # Abstand Y-Ticks
#})

#tcrecs = np.loadtxt("/p/projects/dominoes/rikemue/ecs-pycas-latin/tcrecs.txt", delimiter= ",")
#ecs = np.round(tcrecs[:,1],6) 
#scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

networks = ["0.0_0.0_0.0","0.0_0.0_1.0","0.0_0.0_-1.0",
            "1.0_0.0_0.0","1.0_0.0_1.0","1.0_0.0_-1.0",
            "-1.0_0.0_0.0","-1.0_0.0_1.0","-1.0_0.0_-1.0"]

path = "/p/projects/dominoes/rikemue/ecs-pycas-latin/results/"

print("Compiling Data")


for i_n, network in enumerate(networks):
    network_path = os.path.join(path, "network_" + network) 
    results = []
    files = glob.glob(os.path.join(network_path, "*.txt"))
     
    for file in files:
        if os.path.basename(file) == "empirical_values.txt":
            continue
        if os.path.basename(file) == "all_results.npy":
            continue
    
    
        parts = re.split(r"ECS|_ID|_Scenario|_|\.txt", os.path.basename(file)) #['', '5.767625', '8', '798', 'strngth1.0', '']
        data = np.loadtxt(file)
        
        net = np.full(len(data), str(network))
        ECS      = data[:,0]
        scenario = data[:,1].astype(int)
        strength = data[:,2].astype(float)
        ID       = data[:,3].astype(int)

        num_tipped = data[:,9].astype(int)
        GIS_f  = data[:,10].astype(int)
        AMOC_f = data[:,11].astype(int)
        WAIS_f = data[:,12].astype(int)
        AMAZ_f = data[:,13].astype(int)
        
        
        for i in range(len(data)):
            results.append([
                #net[i],
                ECS[i],
                scenario[i],
                #strength[i],
                #ID[i],
                num_tipped[i],
                GIS_f[i],
                AMOC_f[i],
                WAIS_f[i],
                AMAZ_f[i]
            ])
            
        
        
    # BIG RESULTS TABLE
    results = np.array(results, dtype=object)
    save_path = os.path.join(network_path, "all_results.npy")
    np.save(save_path, results)
