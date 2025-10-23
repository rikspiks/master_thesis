import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


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

tcrecs = np.loadtxt("C:/Users/LENOVO/Desktop/FAIR-PyCas/Tdata/tcrecs.txt", delimiter= ",")
ecs = np.round(tcrecs[:,1],6) 
scenarios = np.array((309, 344, 382, 424, 523, 646, 798))

networks = ["_0.0_0.0_0.0","_0.0_0.0_1.0","_0.0_0.0_-1.0",
            "_1.0_0.0_0.0","_1.0_0.0_1.0","_1.0_0.0_-1.0",
            "_-1.0_0.0_0.0","_-1.0_0.0_1.0","_-1.0_0.0_-1.0"]

risk = np.load('C:/Users/LENOVO/Desktop/FAIR-PyCas/risks_data.npy')

titels = ['$\geq$ 1', '$\geq$ 2','$\geq$ 3','all 4', 'GIS', 'AMOC', 'WAIS', 'AMAZ']
save_titels = ['1','2','3','4','GIS','AMOC','WAIS','AMAZ']

## --------------------- DEFINE FUNCTIONS ----------------

def left_inverse_min_preimage(x, y, *, sort_x=True, fill_value=np.nan):
    """
    Build a callable g(yq) that returns the smallest x such that the
    piecewise-linear interpolation through (x, y) attains yq.
    
    Parameters
    ----------
    x, y : array-like, same length
        Sample points of the (possibly non-monotone) function.
    sort_x : bool
        If True, sort points by x before building segments.
    fill_value : float
        Value to return when yq lies outside the overall y-range (no preimage).
    
    Returns
    -------
    g : callable
        g(yq) -> array of minimal x's (same shape as yq) where f(x)=yq,
        or fill_value when no solution.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if sort_x:
        order = np.argsort(x)
        x, y = x[order], y[order]
    
    # Build segments
    x0 = x[:-1]; x1 = x[1:]
    y0 = y[:-1]; y1 = y[1:]
    
    # Drop zero-length-in-x segments (duplicate x's). If you want another policy,
    # e.g., average or max across duplicates, preprocess x,y before this step.
    keep = (x1 != x0)
    x0 = x0[keep]; x1 = x1[keep]
    y0 = y0[keep]; y1 = y1[keep]
    
    # Precompute for speed
    dx = x1 - x0
    dy = y1 - y0
    
    ymin_seg = np.minimum(y0, y1)
    ymax_seg = np.maximum(y0, y1)
    non_horizontal = (dy != 0.0)
    horizontal = ~non_horizontal

    def g(yq):
        yq_arr = np.asarray(yq, float)
        Y = yq_arr[..., None]  # shape (..., 1) to broadcast across segments

        # Crossings on non-horizontal segments: ymin <= yq <= ymax
        crosses = (Y >= ymin_seg) & (Y <= ymax_seg) & non_horizontal
        # x_at_y = x0 + t*dx, where t = (yq - y0) / dy
        t = (Y - y0) / dy
        x_cross = x0 + t * dx

        # Horizontal segments: include left endpoint when yq == y0 == y1
        horiz_hit = horizontal & (Y == y0)
        x_horiz = np.where(horiz_hit, np.minimum(x0, x1), np.inf)

        # Candidate x's: from crossings or horizontal hits
        candidates = np.where(crosses, x_cross, np.inf)
        candidates = np.minimum(candidates, x_horiz)

        # Minimal x across all segments; if none, set to fill_value
        xmin = np.min(candidates, axis=-1)
        xmin = np.where(np.isfinite(xmin), xmin, fill_value)

        return xmin.reshape(yq_arr.shape)

    return g
# ---- Burning Amber -----------------------------
risk = np.load("C:/Users/LENOVO/Desktop/FAIR-PyCas/risk_array_2-4.npy")

colors = ['gold', 'darkorange', 'black']
labels = ['10 % Tipping Risk', '50 % Tipping Risk', '90 % Tipping Risk']

# get percentage data
results = []

for i, s in enumerate(scenarios):
    data = risk[risk[:, 1].astype(int) == s]
    x = data[:,0]
    y = data[:,2]
    
    g = left_inverse_min_preimage(x, y)
    # Query a few y-levels:
    y_levels = np.array([0.01, 0.10, 0.5, 0.9])
    x_leftmost = g(y_levels)
    results.append((s,x_leftmost[1],x_leftmost[2], x_leftmost[3]))
        
        
perc = np.array(results)

myhre = 2.9 

# for Burning Amber Bars
x_vals = np.unique(risk[:, 0])
y_vals = np.unique(risk[:, 1])

# Gitter erstellen für bars
X, Y = np.meshgrid(y_vals, x_vals)  
# Leeres Z-Gitter für Werte
Z = np.full_like(X, np.nan, dtype=float)

# Werte einfügen - Indizes angepasst
for row in risk:
    x_idx = np.where(y_vals == row[1])[0][0]  
    y_idx = np.where(x_vals == row[0])[0][0]  
    Z[y_idx, x_idx] = row[2]

Z[(Z == 0) | (Z == 1)] = np.nan

# Plot
fig, ax = plt.subplots()
plt.axhspan(0.7, myhre, color='lightgrey', alpha=0.8, label='Unlikely Range \n(Myhre et al., 2025)')  # axvspan zu axhspan geändert
plt.axhspan(0.7, 1.8, color='grey', alpha = 0.7, label="CMIP6 Bounds")  
plt.axhspan(5.6, 6, color='grey', alpha = 0.7)  

# Pcolormesh ohne Alpha-Trennung
c = ax.pcolormesh(X, Y, Z, cmap="RdYlGn_r", shading='auto')

cb = plt.colorbar(c, ax=ax)
cb.set_label("Tipping Risk (%)")

for i in range(3):
    # plot results array sodass x = scenario und y = ECS
    plt.plot(perc[:, 0], perc[:, i+1], color=colors[i], label=labels[i], linewidth = 3)
    
ticks = np.linspace(0.1, 0.9, 9)
cb.set_ticks(ticks)
cb.set_ticklabels([f"{int(t*100)}" for t in ticks])

# Achsenbeschriftungen 
plt.xlabel("Atmospheric Carbon Concentration (ppm)")  
plt.ylabel("Equilibrium Climate Sensitivity (°C)")    
plt.ylim(0.7, 6)  
plt.xlim(300)

plt.axvline(x=430, linestyle="--", color="black")  # axhline zu axvline geändert
plt.text(433, 5.5, "Current Concentration ~430 ppm", color="black", va="top", fontsize="x-large")  # Koordinaten und Alignment angepasst

# Legende ohne Alpha-Legende
plt.legend(fontsize="xx-large", loc="best", bbox_to_anchor=(0.93, 0.93))
plt.tight_layout()

# ---Plots for 2-4 tipped + element specific --------------------------------


#labels = ['1 % Tipping Risk','10 % Tipping Risk', '50 % Tipping Risk', '90 % Tipping Risk']
labels = ['5 % Tipping Risk','10 % Tipping Risk', '25 % Tipping Risk','50 % Tipping Risk','75 % Tipping Risk', '90 % Tipping Risk', '95 % Tipping Risk']

# decide for one way to define the colors
colors = ['greenyellow','green','gold', 'orange', 'r', 'maroon', 'black' ]
# OR
cmap = plt.get_cmap("plasma_r")  # or "RdYlGn_r", "RdYlBu", "RdYlOrBr"
colors = [cmap(i) for i in np.linspace(0, 1, 7)]


'''
############################################################
For every of the 8 cases
get the percentages
'''

for idx, r in enumerate(range(-8, 0)): 
    
    # get percentage data
    results = []
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        x = data[:,0]
        y = data[:,idx+2]
        
        g = left_inverse_min_preimage(x, y)
        # Query a few y-levels:
        y_levels = np.array([0.05, 0.10,0.23, 0.5,0.75,0.9, 0.95])
        x_leftmost = g(y_levels)
        results.append((s,x_leftmost[0],x_leftmost[1],x_leftmost[2], x_leftmost[3], x_leftmost[4], x_leftmost[5], x_leftmost[6]))

    
    perci = np.array(results)
    
    plt.figure(figsize = (17, 9))    
    for i in range(7):
        # plot results array sodass x = scenario und y = ECS
        plt.plot(perci[:, 0], perci[:, i+1], color=colors[i], label=labels[i], linewidth = 3)
    plt.xlabel("Atmospheric Carbon Concentration (ppm)")  
    plt.ylabel("Equilibrium Climate Sensitivity (°C)")    
    plt.ylim(0.7, 6)  
    plt.xlim(300,850)
    plt.legend(fontsize="xx-large", loc="upper right", bbox_to_anchor=(1.23, 0.99))
    plt.title(titels[idx])
    outpath = fr"C:\Users\LENOVO\Desktop\FAIR-PyCas\TR-ECS-plot\latin\plot_{save_titels[idx]}_secondplotv2.png"
    #plt.savefig(outpath, bbox_inches="tight")
    plt.show()
    plt.close()
        

'''
OPTION:
    Save all of them in one pdf.
    
'''

'''
    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

outpdf2 = r"C:\Users\LENOVO\Desktop\FAIR-PyCas\TR-ECS-plot\second_plots.pdf"

with PdfPages(outpdf2) as pdf:
    for idx, r in enumerate(range(-8, 0)): 
        
        # get percentage data
        results = []
        for i, s in enumerate(scenarios):
            data = risk[risk[:, 1].astype(int) == s]
            x = data[:,0]
            y = data[:,idx+2]
            
            g = left_inverse_min_preimage(x, y)
            # Query a few y-levels:
            y_levels = np.array([0.05, 0.10, 0.23, 0.5, 0.75, 0.9, 0.95])
            x_leftmost = g(y_levels)
            results.append((s, *x_leftmost))
    
        perci = np.array(results)
    
        fig, ax = plt.subplots(figsize=(18, 9))    
        for i in range(7):
            ax.plot(perci[:, 0], perci[:, i+1], color=colors[i], label=labels[i], linewidth=3)
        
        ax.set_xlabel("Atmospheric Carbon Concentration (ppm)")  
        ax.set_ylabel("Equilibrium Climate Sensitivity (°C)")    
        ax.set_ylim(0.7, 6)  
        ax.set_xlim(300, 850)
        ax.set_title(titels[idx])
        
        # Legende außerhalb, nicht abgeschnitten
        ax.legend(fontsize="xx-large", loc="upper right", bbox_to_anchor=(1.21, 0.99))
        
        plt.tight_layout()
        
        # Speichern in PDF mit tight bounding box
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

print(f"Alle Plots in {outpdf2} gespeichert.")

'''
        
        
