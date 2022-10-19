#импорты разных библиотек
import numpy
import random
import pylab
from hapi import *
import pandas as pd
from pylab import GridSpec
from matplotlib.widgets import Slider
from pathlib import Path
import os

# подгружаем базу данных хитрана для СО2

db_begin('data')
fetch_by_ids('CO2', [7, 8, 9, 10], 3589.1, 3590.199)

#<-------функции------->
def Y_ax(T, P, n, cons, name = "Lorentz"):
    '''функция высчитывания значения y'''

    # переменные для коэфициента
    isotopes = ((2,1), (2,2), (2,3), (2,4), )
    substance = 'CO2'
    cert_Environment = {'p': P, 'T':T}
    cert_OmegaStep = 0.001
    cert_GammaL = 'gamma_self'
    cert_Diluent = {'self':cons, 'air': 1-cons}

    k = -(eval('absorptionCoefficient_'+name)(isotopes, substance, Environment = cert_Environment, OmegaStep = cert_OmegaStep, GammaL = cert_GammaL, Diluent = cert_Diluent,HITRAN_units = True)[1])

    return 1-numpy.exp(k*n*47)


def slava_merlow():
    '''Функция для загрузки данных'''
    
    SRC = Path(os.getcwd() + '/CO2 absorption coefficient, cm-1.csv')
    return  pd.read_csv(SRC, delimiter=';').replace(to_replace=',', value =  '.', regex = True).astype('float')

def updateGraph():
    '''!!! Функция для обновления графика'''
    
    # зададим глобальные переменные
    global slider_T
    global slider_P
    global slider_cons
    global graph_1
    global graph_2
    global graph_3
    global graph_4
    global grid_visible
    global data
    
    # Подгружаем дату
    data = slava_merlow()

    # Используем атрибут val, чтобы получить значение слайдеров
    T = slider_T.val
    P = slider_P.val
    cons = slider_cons.val
    
    # производим вычисления n
    R = 8.31
    N_AV = 6.022141e23
    V_m = (R*T)/(P*101325)
    L = (N_AV/V_m)
    
    print("PPM: ", cons*1e6)
    
    n = (L*cons)*1e-6
    
    
    # задаем икс
    x = absorptionCoefficient_Lorentz(((2,1), (2,2), (2,3), (2,4), ), 'CO2', Environment = {'p': P, 'T':T}, OmegaStep=0.001, GammaL = 'gamma_self', HITRAN_units = True)[0]
   

    # обновляем разные графики
    graph_1.clear()
    graph_1.grid()
    graph_1.plot(x, Y_ax(T, P, n , cons , 'Lorentz'),data['Wavenumber, cm-1'],data['Lorentz']) #тут мы задаем икс который мы определили выше, и строим график славы, собирая данные из его данных
    graph_1.legend(['Lorentz', 'Slava'])

    graph_2.clear()
    graph_2.grid()
    graph_2.plot(x, Y_ax(T, P, n , cons, 'Doppler'),data['Wavenumber, cm-1'],data['Doppler'])
    graph_2.legend(['Doppler', 'Slava'])

    graph_3.clear()
    graph_3.grid()
    graph_3.plot(x, Y_ax(T, P, n , cons, 'Voigt'),data['Wavenumber, cm-1'],data['Voigt'])
    graph_3.legend(['Voigt', 'Slava'])

    graph_4.clear()
    graph_4.grid()
    graph_4.plot(x, Y_ax(T, P, n, cons, 'Voigt'),data['Wavenumber, cm-1'],data['Voigt'])
    graph_4.legend(['Voigt', 'Slava'])

    pylab.draw()

def onChangeValue(value):
    '''!!! Обработчик события изменения значений слайдеров'''
    updateGraph()

# <----Основное тело программы----->
# Создадим окно с графиком

# обозначаем, где собственно находяться графики
graph_1 = pylab.subplot2grid((3,2),(0,0))
graph_2 = pylab.subplot2grid((3,2),(0,1))
graph_3 = pylab.subplot2grid((3,2),(1,0))
graph_4 = pylab.subplot2grid((3,2),(1,1))

# для каждого графики ставим решетку-разметку
graph_1.grid()
graph_2.grid()
graph_3.grid()
graph_4.grid()


# Создание слайдера для задания температуры Т
axes_slider_T = pylab.axes([0.05, 0.25, 0.85, 0.04])
slider_T = Slider(axes_slider_T,
                      label='T',
                      valmin=250,
                      valmax=500,
                      valinit=296,
                      valfmt='%1.2f')

# Подпишемся на событие при изменении значения слайдера.
slider_T.on_changed(onChangeValue)

# Создание слайдера для задания давление Р
axes_slider_P = pylab.axes([0.05, 0.17, 0.85, 0.04])
slider_P = Slider(axes_slider_P,
                   label='P',
                   valmin=0.001,
                   valmax=2,
                   valinit=0.01,
                   valfmt='%1.4f')

# Подпишемся на событие при изменении значения слайдера.
slider_P.on_changed(onChangeValue)

# Создание слайдера для задания концентрации cons
axes_slider_cons = pylab.axes([0.05, 0.09, 0.85, 0.04])
slider_cons = Slider(axes_slider_cons,
                   label='cs',
                   valmin=0,
                   valmax=1,
                   valinit=0.02,
                   valfmt='%1.7f')

# Подпишемся на событие при изменении значения слайдера.
slider_cons.on_changed(onChangeValue)


# запускаем первый раз функцию, чтобы отрисовать
updateGraph()

# выводим собственно окно со всем вышеперечисленным
pylab.show()
