from hapi import *

def export():
    # подгружаем базу данных хитрана для СО2
    return db_begin('data'), fetch_by_ids('CO2', [7, 8, 9, 10], 3589.1, 3590.199)


def AC(name):
    """функция для абстракшнкоэфициента"""
    
    return  eval('absorptionCoefficient_'+name)
    



