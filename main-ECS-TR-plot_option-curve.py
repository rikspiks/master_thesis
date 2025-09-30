import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit # in case of curve fitting
from matplotlib.lines import Line2D


#plot style things
plt.style.use('seaborn-v0_8-white')
plt.rcParams['figure.figsize'] = (15, 9)
plt.rcParams.update({
    'xtick.labelsize': 19,
    'ytick.labelsize': 19,
    'axes.titlesize': 25,
    'axes.labelsize': 22,
    'axes.titlepad': 27,       
    'axes.labelpad': 17,       
    'xtick.major.pad': 9,      
    'ytick.major.pad': 9       
})

tcrecs = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/tcrecs.txt", delimiter= ",")
ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

networks = ["_0.0_0.0_0.0","_0.0_0.0_1.0","_0.0_0.0_-1.0",
            "_1.0_0.0_0.0","_1.0_0.0_1.0","_1.0_0.0_-1.0",
            "_-1.0_0.0_0.0","_-1.0_0.0_1.0","_-1.0_0.0_-1.0"]

path = "C:/Users/LENOVO/Desktop/FAIR-PyCas"

data_path = os.path.join(path, "risk_array_2-4.npy")
risk = np.load(data_path)


############## Plot With Histogram ###############################################################

scenario_colors = ['gold', 'mediumaquamarine','green', 'tab:orange', 'red', 'mediumvioletred', "indigo"]  
myhre = 2.9

# Histogramm-Data
all_x = tcrecs[:, 1]
counts, bins = np.histogram(all_x, bins=10)
max_count = counts.max()

# need to make figure with 2 axis
fig, (ax_hist, ax) = plt.subplots(2, 1, sharex=True, figsize=(15, 13),
                                  gridspec_kw={'height_ratios': [1, 3], 'hspace': 0.05})

# Histogramm 
for i in range(len(bins) - 1):
    alpha = (counts[i] / max_count) * 0.8
    ax_hist.bar(
        (bins[i] + bins[i + 1]) / 2,
        counts[i],
        width=(bins[i + 1] - bins[i]),
        color='darkorange',
        alpha=alpha,
        align='center'
    )

ax_hist.set_ylabel("")
ax_hist.spines['top'].set_color('white')
ax_hist.spines['left'].set_color('white')
ax_hist.spines['right'].set_color('white')
ax_hist.spines['bottom'].set_color('black')
ax_hist.yaxis.set_ticks([])
ax_hist.axvline(x = np.median(tcrecs[:,1]), color = "black", label = "Median ECS")
ax_hist.axvline(x=myhre, linestyle="--", color="black", label= 'Minimum Likely ECS \n(Myhre et al. 2025)')
ax_hist.axvline(x = 1.8, color = "grey", linestyle="--", label = "CMIP6 Bounds")
ax_hist.axvline(x= 5.6, linestyle="--", color="grey")
ax_hist.legend(fontsize="xx-large", loc='upper right', bbox_to_anchor=(1.29, 0.97))

# for fitting a logistic curve
def logistic(x, x0, k):
    return 1 / (1 + np.exp(-k * (x - x0)))

for i, s in enumerate(scenarios):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:, 0].astype(float)
    y = data[:, 2].astype(float)
    
    popt, _ = curve_fit(logistic, x, y, p0=[np.median(x), 1], maxfev=9000)
    
    ax.scatter(x, y, color=scenario_colors[i], s=65, edgecolor="black", label=f"{s} ppm Scenario   ")
    
    x_fit = np.linspace(min(x), max(x), 1000)
    x_fit = np.unique(np.concatenate(([min(x)], x_fit, [max(x)])))
    y_fit = logistic(x_fit, *popt)
    # unhash for fitting the curve
    #ax.plot(x_fit, y_fit, color=scenario_colors[i], linewidth=2, label=f"{s} ppm Scenario   ")
    cont = [x_fit,y_fit]
    np.savetxt(f"C:/Users/LENOVO/Desktop/FAIR-PyCas/linefit_{s}.txt",np.array(cont))


ax.axhline(y=0.5, color="black", linestyle=":")
ax.text(5.9, 0.54, "50% Tipping Risk", color="black", ha="right", fontsize="xx-large")
ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
ax.set_ylabel("Tipping Risk (%)")
ax.set_ylim(-0.1, 1.1)
ax.set_xlim(0.5, 6)
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_yticklabels([f"{int(tick * 100)}" for tick in np.arange(0, 1.1, 0.1)])
#ax.axvline(x=myhre, linestyle="--", color="black", label= 'Minimum Likely ECS \n(Myhre et al. 2025)')
ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.8, zorder=0, label = "Unlikely ECS Range \n(Myhre et al. 2025)")
ax.axvspan(0.5, 1.8, color='grey', alpha = 0.7, zorder=0, label = "CMIP6 Bounds")
ax.axvspan(5.6, 6.0, color='grey', alpha=0.7, zorder=0)
ax.legend(fontsize="xx-large", loc='upper right', bbox_to_anchor=(1.29, 0.99),
          title="Scenarios", title_fontsize="xx-large")

plt.tight_layout()
plt.show()


########## ONLY HIST ########################################################################

# counts, bins = np.histogram(all_x, bins=10)
# max_count = counts.max()  # Nur für Alpha-Normierung

# fig, ax_hist = plt.subplots()

# for i in range(len(bins) - 1):
#     alpha = (counts[i] / max_count) * 0.8  # Alpha normiert
#     ax_hist.bar(
#         (bins[i] + bins[i + 1]) / 2,
#         counts[i],  # echte Count-Höhe
#         width=(bins[i + 1] - bins[i]),
#         color='darkorange',
#         edgecolor='black',
#         alpha=alpha,
#         align='center'
#     )

# ax_hist.set_ylabel("Count")
# ax_hist.set_xlabel("ECS")
# plt.tight_layout()
# plt.show()






































