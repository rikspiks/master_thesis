# Master Thesis: Climate Sensitivity as a Determinant of Climate Tipping Risk

This GitHub Repository contains all code I used for my Master Thesis. All code is written in Python. The complete Methodology is sketched out in the workflow below.
The Thesis answers the question: How does Climate Sensitivity determine Climate Tipping Risk?

## Structure: 
**1. FaIR:**
     fair-get-temperatures.py - Contains all steps done in FaIR, 1 to 4 in the workflow.
     Output Temperature Time Series file are ... somewhere..
     tcrecs.txt -  is the generated ensemble of TCR-ECS pairs
     method_plots.py cotains code for plots in the fair part of the methodology

**2. Latin Hypercube Sampling:**
     latin_probability_distribution.py - is the code that uses latin hypercube sampling method to generate different input parameters (tipping time scale and temperature)   for pycascades, to take uncertainties in these into account.
   latin_sh_file.txt - is the subsequent output contains the comand lines to run pycascades
   **Rearranging Temperature files:** 
   ECS-T Files in right format.py - rearranges the temperature files to make PyCascades run smoothly and more computational efficient. This code makes one data file per ECS     and puts all of them in one zip-file. The zip file is ecs-timeseries.zip (see Zenodo).
         
**3. PyCascades:**
    MAIN-No_enso.py - is the main script to run the pycascades model
    core and earth_sys folders contain scripts and functions as part of pycascades
    latin_sh_file.txt - contains the comand lines to run pycascades with subsequent input variables
    Additionally it needs:
       ecs-timeseries.zip
       Folder called results, containing a folder called oscillations

**4. Analysis:**
     risk_array_2-4.npy - this file contains the 

![MA_Workflow](https://github.com/user-attachments/assets/d361ff4d-93a6-4c32-9720-76facb31880f)

