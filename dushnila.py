import numpy
import random
import pylab
import matplotlib.pyplot as plt
import hapi
from hapi import *
import pandas as pd
from matplotlib.gridspec import GridSpec

db_begin('data')
fetch_by_ids('CO2', [7, 8, 9, 10], 3589.1, 3590.199)

# Импортируем класс слайдера
from matplotlib.widgets import Slider


def first_y(T, P , x, cons):
    '''Отображаемая фукнция'''
    #концекнтрацию в давление чтобы п селф это была формула

    return absorptionCoefficient_Lorentz(((2,1), (2,2), (2,3), (2,4), ), 'CO2', Environment = {'p': P, 'T':T}, OmegaStep=0.001, GammaL = 'gamma_self', Diluent = {'self':cons, 'air': 1-cons}, HITRAN_units = True)[1]


def second_y(T, P , x, cons):
    '''Отображаемая фукнция'''
    #концекнтрацию в давление чтобы п селф это была формула

    return absorptionCoefficient_Doppler(((2,1), (2,2), (2,3), (2,4), ), 'CO2', Environment = {'p': P, 'T':T}, OmegaStep=0.001, GammaL = 'gamma_self', Diluent = {'self':cons, 'air': 1-cons}, HITRAN_units = True)[1]

def third_y(T, P , x, cons):
    '''Отображаемая фукнция'''
    #концекнтрацию в давление чтобы п селф это была формула

    return absorptionCoefficient_Voigt(((2,1), (2,2), (2,3), (2,4), ), 'CO2', Environment = {'p': P, 'T':T}, OmegaStep=0.001, GammaL = 'gamma_self', Diluent = {'self':cons, 'air': 1-cons}, HITRAN_units = True)[1]


if __name__ == '__main__':
    def get_param():
        return  pd.read_csv('CO2 absorption coefficient, cm-1.csv', delimiter=';').replace(to_replace=',', value =  '.', regex = True).astype('float')
    
    def updateGraph():
        '''!!! Функция для обновления графика'''
        # Будем использовать sigma и mu, установленные с помощью слайдеров
        global slider_T
        global slider_P
        global slider_cons
        global graph_1
        global graph_2
        global graph_3

        # Используем атрибут val, чтобы получить значение слайдеров
        T = slider_T.val
        P = slider_P.val
        cons = slider_cons.val
        x = absorptionCoefficient_Lorentz(((2,1), (2,2), (2,3), (2,4), ), 'CO2', Environment = {'p': P, 'T':T}, OmegaStep=0.001, GammaL = 'gamma_self', HITRAN_units = True)[0]
        #y = first_y(T, P, x , cons)

        graph_1.clear()
        graph_1.plot(x, first_y(T, P, x , cons))
        graph_2.clear()
        graph_2.plot(x, second_y(T, P, x , cons))
        graph_3.clear()
        graph_3.plot(x, third_y(T, P, x , cons))
        pylab.draw()

    def onChangeValue(value):
        '''!!! Обработчик события изменения значений слайдеров'''
        updateGraph()

#YFXFKJ KZNCRJQ GHJUHFVVS
    # Создадим окно с графиком


    fig, (graph_1, graph_2, graph_3) = pylab.subplots(3)
    graph_1.grid()
    graph_2.grid()
    graph_3.grid()


    # Оставим снизу от графика место для виджетов
    fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)



    # Создание слайдера для задания T
    axes_slider_T = pylab.axes([0.05, 0.25, 0.85, 0.04])
    slider_T = Slider(axes_slider_T,
                          label='T',
                          valmin=250,
                          valmax=500,
                          valinit=0.5,
                          valfmt='%1.2f')

    # !!! Подпишемся на событие при изменении значения слайдера.
    slider_T.on_changed(onChangeValue)

    # Создание слайдера для задания P
    axes_slider_P = pylab.axes([0.05, 0.17, 0.85, 0.04])
    slider_P = Slider(axes_slider_P,
                       label='P',
                       valmin=0.001,
                       valmax=2,
                       valinit=0.0,
                       valfmt='%1.2f')

    # !!! Подпишемся на событие при изменении значения слайдера.
    slider_P.on_changed(onChangeValue)

# Создание слайдера для задания cons
    axes_slider_cons = pylab.axes([0.05, 0.09, 0.85, 0.04])
    slider_cons = Slider(axes_slider_cons,
                       label='cs',
                       valmin=0,
                       valmax=1,
                       valinit=0.0,
                       valfmt='%1.2f')

# !!! Подпишемся на событие при изменении значения слайдера.
    slider_cons.on_changed(onChangeValue)

    updateGraph()

    pylab.show()