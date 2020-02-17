# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 14:27:20 2020

@author: matheus
"""

# Script para calculo de inflação de combustiveis.


import pandas as pd
import numpy as np
import datetime as dt


# Calculo da variação mensal

def inflacao_combustivel(dados):
    """faz o calculo de inflação mensal por combustivel
    (é provável que seja necessário formata a data do output do forms
    de dd/mm/yyyy/ para mm/yyyy antes de usar o script)"""
    
     
    df = pd.read_csv(dados) #xlsx ou csv
    df = df.groupby(by=df['Data']).mean()  #"Data" de acordo com o forms, nas bases antigas substituir por "Mes"
    col = df.columns
    for i in col:
        df['preco_lag_{}'.format(i)] = df[i].shift(1)
   
    
    df['var_etanol'] = (df['Etanol']/df['preco_lag_Etanol']) - 1
    df['var_gasol'] = (df['Gasolina Comum']/df['preco_lag_Gasolina Comum']) -1
    df['var_gasol_adt'] = (df['Gasolina Aditivada']/df['preco_lag_Gasolina Aditivada']) -1
    df['var_ds10'] = (df['Diesel s-10']/df['preco_lag_Diesel s-10']) -1
    df['var_ds500'] = (df['Diesel s-500']/df['preco_lag_Diesel s-500']) -1
    
    df = df[['var_etanol', 'var_gasol', 'var_gasol_adt',
           'var_ds10', 'var_ds500']]

    return df


def inflacao_acumulada(dados):
    """Acumulado de 12 meses"""
    df = inflacao_combustivel(dados)
    acumulado = []
    for i in df.columns:
        var = np.prod(df[i]+1) - 1 
        acumulado.append(var.round(5))

    acm = pd.DataFrame(acumulado, index=['Etanol', 'Gasolina Comum', 'Gasolina Aditivada', 'Diesel s-500',
       'Diesel s-10'])
    return acm

