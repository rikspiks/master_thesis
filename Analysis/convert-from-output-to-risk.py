import os
import numpy as np


tcrecs = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/tcrecs.txt", delimiter= ",")
ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

networks = ["_0.0_0.0_0.0","_0.0_0.0_1.0","_0.0_0.0_-1.0",
            "_1.0_0.0_0.0","_1.0_0.0_1.0","_1.0_0.0_-1.0",
            "_-1.0_0.0_0.0","_-1.0_0.0_1.0","_-1.0_0.0_-1.0"]

path = "C:/Users/LENOVO/Desktop/FAIR-PyCas"
risk = np.load('C:/Users/LENOVO/Desktop/pycas_output.npy', allow_pickle=True)
# ################ 
all_rows = []
for file_data in risk:  # file_data.shape = (9, n_rows)
    ECS, scenario, strength, ID, num_tipped, GIS_f, AMOC_f, WAIS_f, AMAZ_f = file_data
    for i in range(len(ECS)):
        all_rows.append([ECS[i], scenario[i], strength[i], ID[i],
                          num_tipped[i], GIS_f[i], AMOC_f[i], WAIS_f[i], AMAZ_f[i]])
all_rows = np.array(all_rows)
results = all_rows
'''
NOW BEGINS THE FUN PART OF CALCULATING THE RISK 

get the risk for each scenario and ECS
die durchschnittlichen tr werte für jedes ecs
die dots die wir brauchen
'''

risk_list=[]
for s in scenarios:
    data = results[results[:, 1].astype(int) == s]
    print(s)
    for e in ecs:
        data_e = data[data[:, 0].astype(float)==e]
        one = 0
        two = 0
        three = 0
        four = 0
        no_tips = 0
        GIS = 0
        AMAZ = 0
        AMOC = 0
        WAIS = 0
        
        for i in range(len(data_e[:,4])):
            GIS = GIS + int(data_e[i,5])
            AMOC = AMOC + int(data_e[i,6])
            WAIS = WAIS + int(data_e[i,7])
            AMAZ = AMAZ + int(data_e[i,8])
            if int(data_e[i,4]) >= 1:
                one = one + 1
            if int(data_e[i,4]) >= 2:
                two = two + 1
            if int(data_e[i,4]) >= 3:
                three = three + 1
            if int(data_e[i,4]) >= 4:
                four = four + 1
            else:
                no_tips = no_tips + 1
                
        
        # calculate tipping risk
        one_risk = one/ len(data_e)
        three_risk = three/ len(data_e)
        two_risk = two/ len(data_e)
        four_risk = four/ len(data_e)
        GIS_risk = GIS/len(data_e)
        WAIS_risk = WAIS/len(data_e)
        AMOC_risk = AMOC/len(data_e)
        AMAZ_risk = AMAZ/len(data_e)
        risk_list.append([e,s,one_risk, two_risk, three_risk,four_risk,GIS_risk,AMOC_risk,WAIS_risk,AMAZ_risk])

print("Done") 
# SHORTER RISK ARRAY 
risk = np.array(risk_list)
save_path = os.path.join(path, "risks_data.npy")
np.save(save_path, risk)