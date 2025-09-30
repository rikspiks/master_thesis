# -*- coding: utf-8 -*-
"""
Get the Numbers named in the Results:
    At \SI{344}{ppm}, an ECS above \SI{2.12}{\celsius} already implies a 
    tipping risk greater than \SI{0}{\%}, while only ECS values exceeding 
    \SI{3.73}{\celsius} push the risk beyond \SI{50}{\%}.  
    In comparison, the \SI{382}{ppm} scenario—just \SI{30}{ppm} 
    higher—already exhibits non-ne2.1gligible tipping risks for ECS above 
    \SI{1.94}{\celsius}, with probabilities surpassing \SI{50}{\%} at ECS 
    greater than \SI{2.5}{\celsius}. 
"""

import numpy as np

# Load Data
risk = np.load("C:/Users/LENOVO/Desktop/FAIR-PyCas/risk_array_2-4.npy")
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

# ---- Start Analysis ---------
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)

    # ECS for Risk > 0%
    idx = np.argmax(data[:, 2] > 0)  
    value = data[idx, 0]
    print("Tipping Risk starts to increase at ECS =",data[idx, 0])
    
    # ECS for Risk > 50%
    if np.any(data[:, 2] > 0.5):
        idx = np.argmax(data[:, 2] > 0.5)
        print("Tipping Risk exceeds 50% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk > 50%")

    
    # Maximum Risk
    print("Maximum Tipping Risk is", np.round(np.max(data[:,2]).astype(float)*100),"%.")

# ---- For the 2. Plot ----
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)

    # ECS for Risk > 0%
    idx = np.argmax(data[:, 2] >= 0.01)  
    value = data[idx, 0]
    print("Tipping Risk >= 1% start at ECS =",data[idx, 0])
    
    # ECS for Risk > 50%
    if np.any(data[:, 2] > 0.9):
        idx = np.argmax(data[:, 2] > 0.9)
        print("Tipping Risk exceeds 90% at ECS =", data[idx, 0])
    else:
        print("No ECS with tipping risk > 90%")
        
# --- Min, Mean, Max Risks
for i, s in enumerate(scenarios):
    print("\n**",s, "ppm Scenario**")
    data = risk[risk[:,1].astype(int)==s]
    data = np.sort(data,0)
    print(np.min(data[:,2]))
    print(np.mean(data[:,2]))
    print(np.max(data[:,2]))
    