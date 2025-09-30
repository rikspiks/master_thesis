# -*- coding: utf-8 -*-
"""
-- Creating Methods Plots --

To visualize ECS ensemble and Scenarios

"""

# import libraries
import numpy as np
from matplotlib import pyplot as plt
# form some stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# for plor style
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (15, 9)
plt.rcParams.update({
    'xtick.labelsize': 19,
    'ytick.labelsize': 19,
    'axes.titlesize': 25,
    'axes.labelsize': 22,
    'axes.titlepad': 27,       # Abstand Titel
    'axes.labelpad': 17,       # Abstand Achsenbeschriftung
    'xtick.major.pad': 9,      # Abstand X-Ticks
    'ytick.major.pad': 9       # Abstand Y-Ticks
})

# import the data
tcrecs = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/tcrecs.txt",delimiter = ",")

T05 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_0.txt", delimiter = ",")
T1 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_1.txt", delimiter = ",")
T15 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_2.txt", delimiter = ",")
T2 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_3.txt", delimiter = ",")
T3 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_4.txt",delimiter = ",")
T4 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_5.txt", delimiter = ",")
T5 = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/T_6.txt", delimiter = ",")

Ts = [T05,T1, T15,T2,T3,T4,T5]
ppms = [309, 344, 382, 424, 523, 646, 798]
"""
1. TCR-ECS Pairs
"""
# ECS Histogram
plt.hist(tcrecs[:,1], edgecolor='white')
plt.axvline(x=np.median(tcrecs[:,1]), color='orange', linestyle='dashed')
plt.xlabel("Equilibrium Climate Sensitivity (°C)")
plt.tight_layout()
plt.show()

# Histogram with Consraints
data = tcrecs[:, 1]
bins = np.histogram_bin_edges(data, bins=10)
counts, _ = np.histogram(data, bins=bins)
lower, upper = 1.8, 5.6 # CMIP6 Constraints
# colors
bin_centers = (bins[:-1] + bins[1:]) / 2
colors = ['steelblue' if lower <= c <= upper else 'lightsteelblue' for c in bin_centers]
# Plot
plt.figure(figsize=(12, 8))
plt.bar(bins[:-1], counts, width=np.diff(bins), color=colors, align='edge', edgecolor='white')
# coloring out-of-cmip6 bins
for i in range(len(bins) - 1):
    if bins[i] < upper < bins[i+1]:
        plt.bar(upper, counts[i], width=bins[i+1]-upper, color='lightsteelblue', align='edge', edgecolor='white')
    if bins[i] < lower < bins[i+1]:
        plt.bar(bins[i], counts[i], width=lower-bins[i], color='lightsteelblue', align='edge', edgecolor='white')
# Constraints lines
plt.axvline(x=lower, color='black', linestyle='dashed')
plt.axvline(x=upper, color='black', linestyle='dashed')
plt.axvline(x = 2.9, color = "red", linestyle = ":", label = "Minimum Likely ECS \nafter Myhre et al. 2025")
plt.axvline(x=np.median(tcrecs[:,1]), color='orange', linestyle='dashed', label = "Median ECS")
plt.xlabel("Equilibrium Climate Sensitivity (°C)")
plt.tight_layout()
plt.legend()
plt.show()

# ECS-TCR relation
X = tcrecs[:, 0].reshape(-1, 1)  # TCR
y = tcrecs[:, 1]                # ECS

# Linear Model Fit
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

# Stat. values
slope = model.coef_[0]
intercept = model.intercept_
r2 = r2_score(y, y_pred)

plt.scatter(X, y)
plt.plot(X, y_pred, color='red')
#plt.title('TCR - ECS Correlation')
plt.ylabel('Equilibrium Climate Sensitivity (ECS)')
plt.xlabel('Transient Climate Response (TCR)')
plt.text(X.min(), y.max(), f'R² = {r2:.2f}', fontsize=19, color='red')
plt.show()

# ECS distribution, is uniform
plt.scatter(range(len(tcrecs)), tcrecs[:, 1])
plt.ylim(top=10)
plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.xticks([200, 400, 600, 800,1000])
plt.show()

print("Intercept:", intercept)

"""
2. Scenarios and Temperatures
"""
# construct scenarios
ppms = [309, 344, 382, 424, 523, 646, 798]
start_ppm = 278
nt = 10000 # number of time steps (in years) = 200 years ramp up and 2000 years stabilization
years = np.arange(1850, 1850+nt)

conc_list = []

for i_p, p in enumerate(ppms):
    conc = np.full_like(years, p, dtype=float)
    conc[0] = 278
    j = 0
    slope = (p - start_ppm) / 200
    for i in range(1850,2050):
        conc[years == i] = start_ppm+j*slope
        j = j+1
    conc_list.append(conc)
conc_list = np.array(conc_list)
# now we would run the model for each concentration scneario to get the temperatures. butwe already load the temp-data from my previos run. So we can skip the step because it takes long


# Ramp-Up Stabilization Scenarios - CO2 Concentrations in ppm
for ip, p in enumerate(ppms):
    plt.plot(range(2000), conc_list[ip,:2000], label = f"{p} ppm")
plt.ylabel('Atmospheric CO2 Concentration (ppm)')
plt.xlabel("Years")
plt.legend(fontsize = "xx-large", bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()

# Temperature ranges over time
for i, p in enumerate(ppms):
    plt.fill_between(range(len(T3)), np.max(Ts[i], axis = 1), np.min(Ts[i], axis = 1), alpha=.1, linewidth=0)
plt.ylabel('Global Temperature Change (°C)')
plt.xlabel("Years")
#plt.legend(fontsize = "xx-large", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout() 

# Final Temperatures Histograms
final_T = []
for i, T in enumerate(Ts):
    f = Ts[i][nt-1, :]
    final_T.append(f)
final_T = np.column_stack(final_T)

plt.figure(figsize=(14, 5)) 
for i, p in enumerate(ppms):
    plt.hist(final_T[:, i], bins=13, histtype="barstacked", edgecolor="white", 
             alpha=0.3, label=f"{p} ppm")
    median = np.median(final_T[:, i])
    plt.axvline(median, color="C"+str(i), linestyle="-", linewidth=2)

plt.xlabel("Final Temperature (°C)")
plt.legend(fontsize="xx-large")
plt.show()

"""
2. Time Until Equilibrium
"""
threshold = 0.0001
tt = Ts
all_steps =[]

for T in tt:
    steps = []

    for i in range(len(tcrecs)):
        temp = T[:, i]
        # Berechne die Differenzen zwischen aufeinanderfolgenden Zeitpunkten
        diffs = np.abs(np.diff(temp))

        # Finde den Zeitpunkt, an dem die Änderung unter dem Schwellenwert bleibt
        stable_point = np.where(diffs < threshold)[0]

        # Wenn der stabile Punkt gefunden wurde, speichere den ersten Zeitpunkt
        if stable_point.size > 0:
            steps.append(stable_point[0] + 1)  # +1 weil `np.diff` einen Index verschiebt
        else:
            steps.append(nt)  # Falls keine Stabilisierung gefunden wurde, gehe bis zum Ende
        
    all_steps.append(steps)

# Deistinguish them again
#steps_T05, steps_T1, steps_T15, steps_T2, steps_T3, steps_T4, steps_T5 = all_steps

all_step = np.array(all_steps)

# plot

plt.figure() 

for i, p in enumerate(ppms):
    plt.scatter(tcrecs[:,1], all_step[i,:], alpha=0.3, label=f"{p} ppm")
plt.xlabel('Equilibrium Climate Sensitivity (°C)')
plt.ylabel('Time until Equilibrium reached (Years)')
plt.legend(fontsize = "xx-large")
plt.show()

"""
Done :) 
"""


# Histogram How many Tipped Elements
#plt.hist(results[:,9], bins = 5, edgecolor = "white")
#plt.xlabel("Number of Tipped Elements")
#hist_path = os.path.join(path, "analysis/hist_num.png")
#plt.savefig(hist_path)
#plt.close()

# # TIPPING RISK of scenarios

# print("Risk - Scenario Plot")

# risk_list=[]
# # get the risk for each scenario and ECS
# # die durchschnittlichen tr werte für jedes ecs
# # die dots die wir brauchen
# for s in scenarios:
#     data = results[results[:, 2].astype(int) == s]
#     for e in ecs:
#         data = data[data[:, 1].astype(float)==e]
#         print(data)
#         tipped_sys = 0
#         no_tips = 0
#         GIS = 0
#         AMAZ = 0
#         AMOC = 0
#         WAIS = 0
        
#         for i in range(len(data[:,4])):
#             if data[i,4].astype(int) >= 1:
#                 tipped_sys = tipped_sys + 1
#                 GIS = GIS + data[:,5]
#                 AMOC = AMOC + data[:,6]
#                 WAIS = WAIS + data[:,7]
#                 AMAZ = AMAZ + data[:,8]
#             else:
#                 no_tips = no_tips + 1
                
#         print("Tipped:", tipped_sys)
#         print("Cases of no tipping: ", no_tips)
        
#         # calculate tipping risk
#         tipping_risk = tipped_sys/ len(data)
#         risk_list.append([e,s,tipping_risk,tipped_sys,GIS,AMOC,WAIS,AMAZ])
    
#     print("Risk - ECS plot")
    
#     plt.scatter(risk_list[:,0], risk_list[:,2], s = 70, edgecolor = "black")
#     plt.xlabel("Equilibrium Climate Sensitivity (°C)")
#     plt.ylabel("Tipping Risk (%)")

#     plot_path = os.path.join(path, f"analysis/tiprisk-ecs-{s}.pdf",)
#     os.makedirs(os.path.dirname(plot_path), exist_ok=True)
#     plt.savefig(plot_path)
#     plt.close()

# # SHORTER RISK ARRAY 
# risk = np.array(risk_list)
# save_path = os.path.join(path, "analysis/risk.txt")
# np.savetxt(save_path, risk)

# plt.scatter(risk[:,1], risk[:,2], s = 70, edgecolor = "black")
# plt.xlabel("ppm Scenario")
# plt.ylabel("Tipping Risk (%)")

# plot_path = os.path.join(path, "analysis/scenario-tiprisk.pdf",)
# os.makedirs(os.path.dirname(plot_path), exist_ok=True)
# plt.savefig(plot_path)
# plt.close()


# # Risk - Coupling Strength
# print("Risk - Coupling Strength")

# coupling_strength = np.linspace(0.0,1.0,11, endpoint=True)

# for s in scenarios:
#     data = results[np.isin(results[:, 2].astype(int), s)]
#     risk_list=[]
#     for e in ecs:
#         data = data[np.isin(data[:, 1].astype(float), e)]
        
#         for strength in coupling_strength:
#             data_i = data[np.isin(data[:, 3].astype(float), np.round(strength, 1))]
            
#             tipped_sys = 0
#             no_tips = 0
            
#             for i in range(len(data_i)):
#                 if data_i[i,4].astype(int) >= 1:
#                     tipped_sys = tipped_sys + 1
#                 else:
#                     no_tips = no_tips + 1
                
#             print("Cases of Tipping:", tipped_sys)
#             print("Cases of no tipping:", no_tips)

#             # calculate tipping risk
#             if tipped_sys != 0:
#                 tipping_risk = tipped_sys/ len(data_i)
#             else:
#                 tipping_risk = 0
                
#             risk_list.append([e,s,strength,tipping_risk,tipped_sys])

#             print("Strength:", strength, "\nRisk:", tipping_risk, "\n------------")
        
#     risk_s = np.array(risk_list)
    
    
#     plt.scatter(risk_s[:,2], risk_s[:,3], s = 70, edgecolor = "black")
#     plt.xlabel("Coupling Strength")
#     plt.ylabel("Tipping Risk (%)")
#     plt.xlim(0.0,1.0)
#     plt.ylim(-0.2,1.2)
#     plt.title(f"{s} ppm scenario")
    
#     plot_path = os.path.join(path, "analysis", f"strength-tiprisk-{s}.pdf",)
#     os.makedirs(os.path.dirname(plot_path), exist_ok=True)
#     plt.savefig(plot_path)
#     plt.close()
    

# print("Finish")



