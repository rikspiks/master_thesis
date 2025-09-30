import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



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
save_titels = ['1','2','3','4','GIS','AMOC','WAIS','AMAZ']

networks = ["_0.0_0.0_0.0","_0.0_0.0_1.0","_0.0_0.0_-1.0",
            "_1.0_0.0_0.0","_1.0_0.0_1.0","_1.0_0.0_-1.0",
            "_-1.0_0.0_0.0","_-1.0_0.0_1.0","_-1.0_0.0_-1.0"]

path = "C:/Users/LENOVO/Desktop/FAIR-PyCas"
risk = np.load('risk_array_2-4.npy')

scenario_colors = ['gold', 'mediumaquamarine','green', 'tab:orange', 'red', 'mediumvioletred', "indigo"]  
labels = ['$\geq$ 1', '$\geq$ 2','$\geq$ 3','all 4', 'GIS', 'AMOC', 'WAIS', 'AMAZ']

myhre = 2.9 
# --------------------- Histogramm Data -----------------------------
all_x = tcrecs[:, 1]
counts, bins = np.histogram(all_x, bins=10)
max_count = counts.max()

# ---------- MAIN Plot ----------------------------------------


def logistic(x, l,x0, k):
    return l / (1 + np.exp(-k*(x - x0)))

for idx,r in enumerate(range(-8, 0)):
    
    # HISTOGRAM PART
    
    # Figure mit zwei Achsen
    fig, (ax_hist, ax) = plt.subplots(2, 1, sharex=True, figsize=(15, 13),
                                      gridspec_kw={'height_ratios': [1, 3], 'hspace': 0.05})

    # Histogramm mit echter y-Achse + normierter Alpha
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
    #ax_hist.legend(fontsize="xx-large", loc='upper right', bbox_to_anchor=(1.29, 0.97))
    ax_hist.set_title(labels[r])
    
    # MAIN Part
    
    #fig, ax = plt.subplots()

    
    for i, s in enumerate(scenarios):
        data = risk[risk[:, 1].astype(int) == s]
        
        
        x = data[:, 0].astype(float)
        y = data[:, r].astype(float)

        # Fit
        popt, _ = curve_fit(logistic, x, y, p0=[max(y), np.median(x), 1], maxfev=9000)        
        
        color = scenario_colors[i]

        # Plot scatter
        plt.scatter(x, y, color=color, s=65, edgecolor="black", label=f"{s} ppm Scenario")
        

        # Plot curve
        x_fit = np.linspace(min(x), max(x), 100)
        x_fit = np.unique(np.concatenate(([min(x)], x_fit, [max(x)])))  # Start/End explizit drin, Duplikate raus
        y_fit = logistic(x_fit, *popt)
        #plt.plot(x_fit, y_fit, color=scenario_colors[i], linewidth=2)
        
       
    plt.axhline(y=0.5, color = "black", linestyle = ":")
    plt.text(5.9, 0.54, "50% Tipping Risk", color = "black", ha = "right", fontsize = "xx-large")
    plt.xlabel("Equilibrium Climate Sensitivity (°C)")
    plt.ylabel("Tipping Risk (%)")
    
    
    ticks = np.arange(0, 1.1, 0.1)
    plt.yticks(ticks, [f"{int(t*100)}" for t in ticks])

    plt.axvspan(0.5, 2.9, color='lightgrey', alpha=0.8, zorder=0, label = "Unlikely ECS Range \n(Myhre et al. 2025)")
    plt.axvspan(0.5, 1.8, color='grey', alpha = 0.7, zorder=0, label = "CMIP6 Bounds")
    plt.axvspan(5.6, 6.0, color='grey', alpha=0.7, zorder=0)



    plt.ylim(-0.1,1.1)
    plt.xlim(0.5,6)
    #plt.legend(fontsize = "xx-large", loc='upper right', bbox_to_anchor=(1.32, 0.99), title = "Scenarios", title_fontsize="xx-large")
    plt.tight_layout()
    
    outpath = fr"C:\Users\LENOVO\Desktop\FAIR-PyCas\TR-ECS-plot\latin\plot-one_{save_titels[idx]}.png"
    plt.savefig(outpath)
    plt.show()
    plt.close()
    
'''

to get all plots in one pdf:
    
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages

# Beispiel-Funktion (deine hast du ja schon definiert)
def logistic(x, L, x0, k):
    return L / (1 + np.exp(-k * (x - x0)))

# Ausgabe-PDF
outpdf = r"C:\Users\LENOVO\Desktop\FAIR-PyCas\TR-ECS-plot\all_plots.pdf"

with PdfPages(outpdf) as pdf:
    for idx, r in enumerate(range(-8, 0)):
        
        # Figure mit zwei Achsen
        fig, (ax_hist, ax) = plt.subplots(2, 1, sharex=True, figsize=(15, 13),
                                          gridspec_kw={'height_ratios': [1, 3], 'hspace': 0.05})

        # Histogramm zeichnen
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
        ax_hist.axvline(x=np.median(tcrecs[:,1]), color="black", label="Median ECS")
        ax_hist.axvline(x=myhre, linestyle="--", color="black", label="Minimum Likely ECS \n(Myhre et al. 2025)")
        ax_hist.axvline(x=1.8, color="grey", linestyle="--", label="CMIP6 Bounds")
        ax_hist.axvline(x=5.6, linestyle="--", color="grey")
        #ax_hist.set_title(labels[r])

        # MAIN Part
        for i, s in enumerate(scenarios):
            data = risk[risk[:, 1].astype(int) == s]
            
            x = data[:, 0].astype(float)
            y = data[:, r].astype(float)

            # Fit
            popt, _ = curve_fit(logistic, x, y, p0=[max(y), np.median(x), 1], maxfev=9000)        

            color = scenario_colors[i]

            # Scatter
            ax.scatter(x, y, color=color, s=65, edgecolor="black", label=f"{s} ppm Scenario")

            # Curve
            x_fit = np.linspace(min(x), max(x), 100)
            x_fit = np.unique(np.concatenate(([min(x)], x_fit, [max(x)])))
            y_fit = logistic(x_fit, *popt)
            # ax.plot(x_fit, y_fit, color=color, linewidth=2)

        ax.axhline(y=0.5, color="black", linestyle=":")
        ax.text(5.9, 0.54, "50% Tipping Risk", color="black", ha="right", fontsize="xx-large")
        ax.set_xlabel("Equilibrium Climate Sensitivity (°C)")
        ax.set_ylabel("Tipping Risk (%)")

        ticks = np.arange(0, 1.1, 0.1)
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{int(t*100)}" for t in ticks])

        ax.axvspan(0.5, 2.9, color='lightgrey', alpha=0.8, zorder=0,
                   label="Unlikely ECS Range \n(Myhre et al. 2025)")
        ax.axvspan(0.5, 1.8, color='grey', alpha=0.7, zorder=0, label="CMIP6 Bounds")
        ax.axvspan(5.6, 6.0, color='grey', alpha=0.7, zorder=0)

        ax.set_ylim(-0.1, 1.1)
        ax.set_xlim(0.5, 6)

        plt.tight_layout()
        
        # in PDF speichern
        pdf.savefig(fig)
        plt.close(fig)

print(f"Alle Plots wurden in {outpdf} gespeichert.")

