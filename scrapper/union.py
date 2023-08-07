# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:25:35 2023

@author: Gonzalo
"""

import pandas as pd
from time import time

start_time = time()
df = pd.read_csv('base-infoleg-normativa-nacional.csv')
print("Tiempo de importar csv: " + str(time() - start_time))

def agregar_txt(id_norma):
    try:
        with open('./txt/' + str(id_norma) + '.txt', 'r', encoding='utf-8') as archivo:
            norma_completa = archivo.read()
    except:
        norma_completa = 'No disponible'
    # Imprimir el contenido del archivo
    #print(norma_completa)
    return norma_completa

start_time = time()
df['norma_completa'] = df['id_norma'].apply(lambda id: agregar_txt(id))
print("Tiempo de carga de txts a df: " + str(time() - start_time))


start_time = time()
df.to_excel('df_normas.xlsx', index = False)
print("Tiempo de creación de excel: " + str(time() - start_time))
