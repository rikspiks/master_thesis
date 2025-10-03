# Master Thesis: Climate Sensitivity as a Determinant of Climate Tipping Risk

This GitHub Repository contains all code I used for my Master Thesis. All code is written in Python. The complete Methodology is sketched out in the workflow below.
The Thesis answers the question: _How does Climate Sensitivity determine Climate Tipping Risk?_

All data can be found in the [Zenodo Project](https://zenodo.org/records/17256491?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjcwMjAxMmU5LTk1Y2EtNGFhYy1hMDRjLTQyYWM1ZDI4YTJmNSIsImRhdGEiOnt9LCJyYW5kb20iOiI2ZDQ3ZDc5YzI0NzBmM2MwMTgzODNiNmEzYTRmMjAxOSJ9.A6ZO8jsTwhK2j3jas2Oq-7lYOvRo79YgIRWGS0-yJt_jYNIIIRfZmcfrYF32QFhFvfFsAFW5H-W9Oe_aQbvHPA).

## Structure: 

**1. FaIR:**

`fair-get-temperatures.py` – Executes steps 1–4 of the workflow in FaIR.

`method_plots.py` – Generates methodology plots for FaIR section.

Outputs: temperature time series + ECS ensemble [Zenodo](https://zenodo.org/records/17256491?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjcwMjAxMmU5LTk1Y2EtNGFhYy1hMDRjLTQyYWM1ZDI4YTJmNSIsImRhdGEiOnt9LCJyYW5kb20iOiI2ZDQ3ZDc5YzI0NzBmM2MwMTgzODNiNmEzYTRmMjAxOSJ9.A6ZO8jsTwhK2j3jas2Oq-7lYOvRo79YgIRWGS0-yJt_jYNIIIRfZmcfrYF32QFhFvfFsAFW5H-W9Oe_aQbvHPA)

**2. Latin Hypercube Sampling:**

`latin_probability_distribution.py` - Generates sampled input parameters (tipping timescales, temperatures) for PyCascades.

`latin_sh_file.txt` - Contains command lines to run PyCascades.
   
**Preprocessing:** 

`ECS-T Files in right format.py` - Formats and zips ECS temperature data (`ecs-timeseries.zip` in Zenodo).
         
**3. PyCascades:**

`MAIN-No_enso.py` - is the main script to run the pycascades model

`core/`, `earth_sys/` – Contain model functions and modules.

Running Pycascades requires:

`ecs-timeseries.zip`

`results/oscillations/` folder

`latin_sh_file.txt`


**4. Analysis:**

`analysis.py`- Collects all PyCascades Outputs into one file (`pycas_output.npy`)

`convert-from-output-to-risk.py` - Calculates the tipping risk from the output `pycas_output.npy` and saves it in `risks_data.npy`

Results: `pycas_output.npy` and `risks_data.npy` are stored in [Zenodo](https://zenodo.org/records/17256491?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjcwMjAxMmU5LTk1Y2EtNGFhYy1hMDRjLTQyYWM1ZDI4YTJmNSIsImRhdGEiOnt9LCJyYW5kb20iOiI2ZDQ3ZDc5YzI0NzBmM2MwMTgzODNiNmEzYTRmMjAxOSJ9.A6ZO8jsTwhK2j3jas2Oq-7lYOvRo79YgIRWGS0-yJt_jYNIIIRfZmcfrYF32QFhFvfFsAFW5H-W9Oe_aQbvHPA)

`all-scenario-ECS-plots.py` 

`results-analyse.py`- Prints the risk values reported on in the thesis

`main-ECS-TR-plot_option-curve.py` -  Creates main ECS-Tipping Risk Plot

`all-scenario-ECS-plots.py` - Scenario-ECS Plot (Secon main figure) and Scenario-ECS Plot for 1-4 tipped element cases and each tipping element

`elements-ECS-TR.py` - ECS-Tipping Risk Plots for 1-4 tipped element cases and each tipping element



![MA_Workflow](https://github.com/user-attachments/assets/b184dfae-b5ae-4a88-bcff-a3a00b142034)

