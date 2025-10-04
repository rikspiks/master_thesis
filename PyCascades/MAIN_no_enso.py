
# Add modules directory to path
import os
import sys
import re

sys.path.append('')

# global imports
import numpy as np
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.)
import itertools
import time
import glob
from PyPDF2 import PdfMerger
from netCDF4 import Dataset


# private imports from sys.path
from core.evolve import evolve

#private imports for earth system
from earth_sys.timing_no_enso import timing
from earth_sys.functions_earth_system_no_enso import global_functions
from earth_sys.earth_no_enso import earth_system

#measure time
#start = time.time()
#############################GLOBAL SWITCHES#########################################
time_scale = True            # time scale of tipping is incorporated
plus_minus_include = True    # from Kriegler, 2009: Unclear links; if False all unclear links are set to off state and only network "0-0" is computed
######################################################################
duration = 50000 #actual real simulation years; OR EVEN 100000 years
ScenarioT = ["05",1,15,2,3,4,5]
ScenarioC = [309, 344, 382, 424, 523, 646, 798]


#Names to create the respective directories
#namefile = "no"
long_save_name = "results"

# if oscillation output
amoc_os = []

#######################GLOBAL VARIABLES##############################
#drive coupling strength
coupling_strength = np.linspace(0.0, 1.0, 11, endpoint=True)
#temperature input (forced with generated overshoot inputs)
GMT_files = np.sort(glob.glob("temp_input/*.txt"))

########################Declaration of variables from passed values#######################
#Must sort out first and second value since this is the actual file and the number of nodes used
sys_var = np.array(sys.argv[1:], dtype=str) #low sample -3, intermediate sample: -2, high sample: -1

#####################################################################

GMT_files = GMT_files[int(sys_var[-2]):int(sys_var[-2])+50]

latin_ID = sys_var[-1]
####################################################################

#Tipping ranges from distribution
limits_gis, limits_thc, limits_wais, limits_amaz, limits_nino = float(sys_var[0]), float(sys_var[1]), float(sys_var[2]), float(sys_var[3]), float(sys_var[4])

#Probability fractions = in wie vielen Fällen kommt Cascade, also dass das eine das andere zum kippen bringt
# TO GIS
pf_wais_to_gis, pf_thc_to_gis = float(sys_var[5]), float(sys_var[6])
# TO THC
pf_gis_to_thc, pf_nino_to_thc, pf_wais_to_thc = float(sys_var[7]), float(sys_var[8]), float(sys_var[9])
# TO WAIS
pf_nino_to_wais, pf_thc_to_wais, pf_gis_to_wais = float(sys_var[10]), float(sys_var[11]), float(sys_var[12])
# TO NINO
pf_thc_to_nino, pf_amaz_to_nino = float(sys_var[13]), float(sys_var[14])
# TO AMAZ
pf_nino_to_amaz, pf_thc_to_amaz = float(sys_var[15]), float(sys_var[16])

#tipping time scales
tau_gis, tau_thc, tau_wais, tau_nino, tau_amaz = float(sys_var[17]), float(sys_var[18]), float(sys_var[19]), float(sys_var[20]), float(sys_var[21])


#Time scale
"""
All tipping times are computed in comparison to the Amazon rainforest tipping time. As this is variable now, this affects the results to a (very) level
"""
if time_scale == True:
    print("compute calibration timescale")
    #function call for absolute timing and time conversion
    time_props = timing(tau_gis, tau_thc, tau_wais, tau_amaz, tau_nino)
    gis_time, thc_time, wais_time, nino_time, amaz_time = time_props.timescales()
    conv_fac_gis = time_props.conversion()
else:
    #no time scales included
    gis_time = thc_time = wais_time = nino_time = amaz_time = 1.0
    conv_fac_gis = 1.0

#include uncertain "+-" links:
if plus_minus_include == True:
    plus_minus_links = np.array(list(itertools.product([-1.0, 0.0, 1.0], repeat=3)))

    #in the NO_ENSO case (i.e., the second link must be 0.0)
    plus_minus_data = []
    for pm in plus_minus_links:
        if pm[1] == 0.0:
            plus_minus_data.append(pm)
    plus_minus_links = np.array(plus_minus_data)

else:
    plus_minus_links = [np.array([1., 1., 1.])]



################################# MAIN #################################
#Create Earth System
earth_system = earth_system(gis_time, thc_time, wais_time, nino_time, amaz_time,
                            limits_gis, limits_thc, limits_wais, limits_nino, limits_amaz,
                            pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc, pf_nino_to_thc,
                            pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_nino_to_wais,
                            pf_thc_to_nino, pf_amaz_to_nino, pf_nino_to_amaz, pf_thc_to_amaz)

################################# MAIN LOOP #################################
for kk in plus_minus_links:
    print("Wais to Thc:{}".format(kk[0]))
    print("Amaz to Nino:{}".format(kk[1]))
    print("Thc to Amaz:{}".format(kk[2]))
    try:
        os.stat("{}".format(long_save_name))
    except:
        os.makedirs("{}".format(long_save_name), exist_ok = True)

    try:
        os.stat("{}/network_{}_{}_{}".format(long_save_name,  kk[0], kk[1], kk[2]))
    except:
        os.makedirs("{}//network_{}_{}_{}".format(long_save_name, kk[0], kk[1], kk[2]), exist_ok = True)

    #save starting conditions
    np.savetxt("{}/network_{}_{}_{}/empirical_values.txt".format(long_save_name, kk[0], kk[1], kk[2]), sys_var, delimiter=" ", fmt="%s")

    

    for GMT_file in GMT_files:
        print(GMT_file)
        parts = re.split("ECS|.txt", GMT_file)
        ECS = float(parts[1])
        
        
        GMT_series = np.loadtxt(GMT_file) # Temperatur einlesen -> 1D array
        for col in range(GMT_series.shape[1]):
            GMT = GMT_series[:,col]
            out_gmt = []
            print("ECS: {}°C".format(ECS))
            print("Scenario:", ScenarioT[col], "°C")
            print("Final CO2 concentration:", ScenarioC[col], "ppm")

                
            for strength in coupling_strength:
                print("Coupling strength: {}".format(strength))
                output = []
                
                for t in range(0, int(duration)):
                    #if os.path.isfile("{}/network_{}_{}_{}/feedbacks_ECS{}_ID{}_Scenario{}_{:.2f}.txt".format(long_save_name, 
                     #   kk[0], kk[1], kk[2], ECS, latin_ID, ScenarioC[col],strength)) == True:
                      #  print("File already computed")
                       # break
                    #print(t)
                    #For feedback computations
                    effective_GMT = GMT[t]
    
                    #get back the network of the Earth system
                    net = earth_system.earth_network(effective_GMT, strength, kk[0], kk[1], kk[2])
    
                    # initialize state
                    if t == 0:
                        initial_state = [-1, -1, -1, -1] #initial state
                    else:
                        initial_state = [ev.get_timeseries()[1][-1, 0], ev.get_timeseries()[1][-1, 1], ev.get_timeseries()[1][-1, 2], ev.get_timeseries()[1][-1, 3]]
                    ev = evolve(net, initial_state)
                    # plotter.network(net)
                    
    
                    # Timestep to integration; it is also possible to run integration until equilibrium
                    timestep = 0.1
    
                    #t_end given in years; also possible to use equilibrate method
                    t_end = 1.0/conv_fac_gis #simulation length in "real" years
                    ev.integrate(timestep, t_end) #?
    
    
                    #saving structure
                    output.append([ECS, 
                                   ScenarioC[col],
                                   strength,
                                   latin_ID,
                                   t,
                                   ev.get_timeseries()[1][-1, 0],
                                   ev.get_timeseries()[1][-1, 1],
                                   ev.get_timeseries()[1][-1, 2],
                                   ev.get_timeseries()[1][-1, 3],
                                   net.get_number_tipped(ev.get_timeseries()[1][-1]),
                                   [net.get_tip_states(ev.get_timeseries()[1][-1])[0]].count(True),
                                   [net.get_tip_states(ev.get_timeseries()[1][-1])[1]].count(True),
                                   [net.get_tip_states(ev.get_timeseries()[1][-1])[2]].count(True),
                                   [net.get_tip_states(ev.get_timeseries()[1][-1])[3]].count(True)
                                   ])
                    
                
                if len(output) != 0:
                    #saving structure
                    data = np.array(output)
                    #print(data[-1])
                    

                    # get infos for oscillation cases
                    time = data.T[4]
                    #state_gis = data.T[1]
                    state_thc = data.T[6].astype(float)
                    #state_wais = data.T[3]
                    #state_amaz = data.T[4]
                    first_1 = next((i for i, v in enumerate(state_thc) if v >= 1), None)
                    last_minus1 = next((i for i, v in reversed(list(enumerate(state_thc))) if v <= -1), None)
                    if first_1 and last_minus1 != None:
                        if last_minus1 > first_1:
                            print("Found Oscillation")
                            amoc_os.append([kk[0], kk[1], kk[2], ECS, latin_ID, ScenarioC[col], strength])
                    
                    # now only extract the last time step and append it
                    out_gmt.append(data[-1])
                
    
    
    
            #necessary for break condition
            if len(out_gmt) != 0:
                #saving structure
                output_data = np.array(out_gmt)
                np.savetxt("{}/network_{}_{}_{}/ECS{}_ID{}_Scenario{}_strngth{}.txt".format(long_save_name, 
                     kk[0], kk[1], kk[2], ECS, latin_ID,ScenarioC[col], strength), output_data, fmt = '%s')

                    
                
amoc_os = np.array(amoc_os)
np.savetxt(f"{long_save_name}/oscillations/amoc_oscillations_ID{latin_ID}_{sys_var[-2]}.txt",amoc_os.astype(float))
print("Finish")
