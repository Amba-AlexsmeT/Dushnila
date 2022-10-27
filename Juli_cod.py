
import numpy as np
import random
import pylab
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
#try:
#    import piplite
#    await piplite.install(['ipywidgets'])
#except ImportError:
#    pass
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from hapi import *
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import FloatSlider
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interactive
import matplotlib.pyplot as plt

db_begin("H2O_1")
fetch("H2O", 1,1,  7182.0, 7184.0)
nu_H2O, sw_H2O = getColumns('H2O', ["nu", "sw"])
nu, coef = absorptionCoefficient_Lorentz(((1,1), (1,2), (1,3), (1,4), ), 'H2O', Environment = {'p': 0.04, 'T':296}, OmegaStep=0.001, GammaL = 'gamma_self', HITRAN_units = True)

def get_data(name):
    data = pd.read_csv(name, delimiter='\t').replace(to_replace=',', value =  '.', regex = True).astype('float')
    return data

monitor_data = get_data("datadata/monitor.txt")
calibration_data = get_data("datadata/калибровка.txt")
Fabri_Pero_data = get_data("datadata/фабри-перо2 ток накачки и амплитуда сигнала.txt")
data = get_data("datadata/2")

#fig, ax = plt.subplots(2,3, figsize = (20, 10))
#________________________________________________________________________________
R = 8.31
N_AV = 6.022141e23
l = 32 #cm

#________________________________________________________________________________
#print("PPM: ", cons*1e6)

def coeff(abs_nu, T, P, volume_mix_ratio):
    #fig, axs = plt.subplots(2,3, figsize=(20,10))
    V_m = (R*T)/(P*101325)
    L = (N_AV/V_m)
    n = (L*volume_mix_ratio)*1e-6
    #plt.figure(figsize =(20,10))

    nu, coef_L = absorptionCoefficient_Lorentz(SourceTables ="H2O",
                                               Environment = {'T':T, 'p':P},
                                               Diluent = {'self':volume_mix_ratio, 'air':1.-volume_mix_ratio},
                                               HITRAN_units = True)
    coef_D = absorptionCoefficient_Doppler(SourceTables ="H2O",
                                               Environment = {'T':T, 'p':P},
                                               Diluent = {'self':volume_mix_ratio, 'air':1.-volume_mix_ratio},
                                               HITRAN_units = True)[1]
    nu, coef_V = absorptionCoefficient_Voigt(SourceTables ="H2O",
                                               Environment = {'T':T, 'p':P},
                                               OmegaStep = 1e-5,
                                               Diluent = {'self':volume_mix_ratio, 'air':1.-volume_mix_ratio},
                                               HITRAN_units = True)


    plt.figure(figsize =(20,10))
    plt.plot(nu, numpy.exp(-coef_V*n*l))
    plt.plot(np.array(x)+abs_nu, y_D)
    
    #plt.figure(figsize = (20,10))
    #return nu, 1-numpy.exp(coef_L*n*l),1-numpy.exp(coef_D*n*l), 1-numpy.exp(coef_V*n*l)
    #axs[0][0].plot(nu, numpy.exp(-coef_L*n*l))
    #axs[0][1].plot(nu, numpy.exp(-coef_D*n*l))
    #axs[0][2].plot(nu, numpy.exp(-coef_V*n*l))
    #axs[0][2].plot(np.array(x)+abs_nu, y_D)
    #axs[1][1].plot(x+abs_nu, abs(numpy.exp(-coef_D*n*l))
    #axs[1][2].plot(x+abs_nu, abs(numpy.exp(-coef_V*n*l))


    
interactive_plot = interactive(coeff,
                               abs_nu=FloatSlider(value=7181.812, min = 7170, max = 7190, step = 0.0001, continuous_update = True, readout_format='.5f',),
                               T=FloatSlider(value=296, min = 288, max = 350, step = 0.01, continuous_update = True,),
                               P=FloatSlider(value=0.04, min = 0.01, max = 0.5, step = 10e-7, continuous_update = True, readout_format='.7f',),
                               volume_mix_ratio=FloatSlider(value=0.7, min = 0, max = 1, step = 10e-7, continuous_update = True, readout_format='.7f',));
output = interactive_plot.children[-1]
output.layout.height = '700px'
interactive_plot
