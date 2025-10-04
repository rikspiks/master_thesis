from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.25)
from pyDOE import * #function name >>> lhs

# SET SEEDS FOR REPRODUCIBILITY
SEED = 1583
np.random.seed(SEED)

#plot style things
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


#Tipping limits, see Schellnhuber, et al., 2016:
limits_gis  = [0.8, 3.0]  #0.8-3.0 (central: 1.5)     old values: [0.8, 3.2] here in brackets: values from new review of D.A. McKay (publicly available yet since January 2022)
limits_thc  = [1.4, 8.0]  #1.4-8.0 (central: 4.0)     old values: [3.5, 6.0]
limits_wais = [1.0, 3.0]  #1.0-3.0 (central: 1.5)      old values: [0.8, 5.5]
limits_amaz = [2.0, 6.0]  #2.0-6.0 (central: 3.5)      old values: [3.5, 4.5]
limits_nino = [3.0, 6.0]  #3.0-6.0 (central: unclear) old values: [3.5, 7.0]

#Time scale of tipping for the tipping elements (taken from the literature review of DA. McKay)
tau_gis  = [1000, 15000]         #1000-15000(central: 10.000)      old values: [1000, 15000] 
tau_thc  = [15, 300]             #15-120 (central: 50)             old values: [15, 300]     
tau_wais = [500, 13000]          #500-13000 (central: 2000)        old values: [1000, 13000] 
tau_nino = [25, 200]             #unclear (around 100)             old values: [25, 200]     
tau_amaz = [50, 200]             #50-200 (central: 100)            old values: [50, 200]     


"""
Latin hypercube sampling with seed for reproducibility
Note: These points need a rescaling according to the uncertainty ranges
This can be done by: x_new = lower_lim + (upper_lim - lower_lim) * u[0;1), where u[0;1) = Latin-HC
"""
points = np.array(lhs(10, samples=10))  # This will now be reproducible due to np.random.seed()

#rescaling function from latin hypercube
def latin_function(limits, rand):
    resc_rand = limits[0] + (limits[1] - limits[0]) * rand
    return resc_rand


#MAIN
array_limits = []
sh_file = []
# for t in range(20):
#     ecs = t*50
#     print(t)
for i in range(0, len(points)):
    #print(i)
    
    unique_id = i + 1  # Simple ID from 1-25

    #TIPPING RANGES
    rand_gis = latin_function(limits_gis, points[i][0])
    rand_thc = latin_function(limits_thc, points[i][1])
    rand_wais = latin_function(limits_wais, points[i][2])
    rand_amaz = latin_function(limits_amaz, points[i][3])
    rand_nino = latin_function(limits_nino, points[i][4])
    
    rand_tau_gis = latin_function(tau_gis, points[i][5])
    rand_tau_thc = latin_function(tau_thc, points[i][6])
    rand_tau_wais = latin_function(tau_wais, points[i][7])
    rand_tau_amaz = latin_function(tau_amaz, points[i][8])
    rand_tau_nino = latin_function(tau_nino, points[i][9])

    array_limits.append([rand_gis, rand_thc, rand_wais, rand_amaz, rand_nino,
                         rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_nino, rand_tau_amaz])

    # sh_file.append(["python3 MAIN_no_enso.py {} {} {} {} {} 0.2 1.0 1.0 0.2 0.3 0.5 0.15 1.0 0.2 0.15 1.0 0.4 {} {} {} {} {} {} {}".format(
    #                          rand_gis, rand_thc, rand_wais, rand_amaz, rand_nino,
    #                          rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_nino, rand_tau_amaz,
    #                          ecs,
    #                          unique_id)]) 

# Save the seed used for this run
with open("run_parameters.txt", "w") as f:
    f.write(f"SEED used for this run: {SEED}\n")
    f.write(f"Number of parameter sets: {len(array_limits)}\n")
    f.write(f"LHS dimensions: 10\n")
    f.write(f"LHS samples: 25\n")

array_limits = np.array(array_limits)
np.savetxt("latin_prob.txt", array_limits, delimiter=" ")

#Create .sh file to run on the cluster
sh_file = np.array(sh_file)
np.savetxt("latin_sh_file.txt", sh_file, delimiter=" ", fmt="%s")

# Rest of your plotting code remains the same...
#tipping ranges and plots
gis = array_limits.T[0]
thc = array_limits.T[1]
wais = array_limits.T[2]
amaz = array_limits.T[3]
nino = array_limits.T[4]

plt.hist(gis, 24, facecolor='c', alpha=0.8, label="GIS")
plt.hist(thc, 25, facecolor='b', alpha=0.8, label="AMOC")
plt.hist(wais, 47, facecolor='k', alpha=0.8, label="WAIS")
plt.hist(amaz, 10, facecolor='g', alpha=0.8, label="AMAZ")
legend = plt.legend(loc='best', fontsize="xx-large", frameon=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('white')   # optional
legend.get_frame().set_alpha(1)
plt.xlabel("Tipping Temperature [°C]")
#plt.ylabel("N")
plt.tight_layout()
plt.savefig("latin_prob_TR.png")
plt.savefig("latin_prob_TR.pdf")
plt.show()
plt.clf()
plt.close()

#feedbacks
rand_tau_gis = array_limits.T[5]
rand_tau_thc = array_limits.T[6]
rand_tau_wais = array_limits.T[7]
rand_tau_nino = array_limits.T[8]
rand_tau_amaz = array_limits.T[9]

plt.hist(rand_tau_gis,  140, facecolor='c', alpha=0.8, label="GIS")
plt.hist(rand_tau_thc,  16, facecolor='b', ec='b', alpha=0.8, label="AMOC")
plt.hist(rand_tau_wais, 120, facecolor='k', alpha=0.8, label="WAIS")
plt.hist(rand_tau_amaz, 14, color='g',ec='g', alpha=0.8, label="AMAZ")
legend = plt.legend(loc='best', fontsize="xx-large", frameon=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_edgecolor('white')   # optional
legend.get_frame().set_alpha(.4)
plt.xlabel("Tipping time (Years)")
#plt.ylabel("N")
plt.tight_layout()
plt.savefig("latin_prob_tau.png")
plt.savefig("latin_prob_tau.pdf")
plt.show()
plt.clf()
plt.close()


print("Finish")