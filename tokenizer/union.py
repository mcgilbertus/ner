# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:25:35 2023

@author: Gonzalo
"""
import os.path

import pandas as pd
from time import time
import re
from html import unescape

def cleantext(text):

    # Decodificar entidades HTML (por ejemplo: &amp; -> &) usando la función unescape de la biblioteca html
    cleaned_text = unescape(text)

    # Eliminar etiquetas HTML usando expresiones regulares
    cleaned_text = re.sub(r'<[^>]*>', '', cleaned_text)

    # Reemplazar espacios múltiples por un solo espacio
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    # Eliminar espacios al principio y al final del texto
    cleaned_text = cleaned_text.strip()
    
    # Convertir todo el texto a minúsculas (opcional)
    cleaned_text = cleaned_text.lower()    

    # Eliminar caracteres especiales y dígitos
    cleaned_text = re.sub(r'[!@#]', '', cleaned_text)

    # Corregir algunos errores comunes de codificación en Python (puedes personalizar esto según tus necesidades)
    # Ejemplo: reemplazar caracteres especiales como "Ã©" por sus equivalentes correctos ("é")
    cleaned_text = cleaned_text.replace("Ã©", "é")
    cleaned_text = cleaned_text.replace("Ã±", "ñ")

    # Patrón de expresión regular para buscar caracteres duplicados, excepto 'R' y 'L'
    cleaned_text = re.sub(r'([^rlw])\1+', r'\1', cleaned_text)

    # Corregir palabras repetidas que se repiten más de 2 veces
    cleaned_text = re.sub(r'\b(\w+)\b(?:\s+\1)+', r'\1', cleaned_text)
    
    # Eliminar acentos:
    cleaned_text = cleaned_text.replace('á','a')
    cleaned_text = cleaned_text.replace('é','e')
    cleaned_text = cleaned_text.replace('í','i')
    cleaned_text = cleaned_text.replace('ó','o')
    cleaned_text = cleaned_text.replace('ú','u')

    return cleaned_text

start_time = time()
df = pd.read_csv('../base-infoleg-normativa-nacional.csv')
print ("Tiempo de importar csv: " + str(time() - start_time)) 

def agregar_txt(id_norma):
    return 'si' if os.path.exists('../pyjuriscrapper/txt/' + str(id_norma) + '.txt') else 'no'
        # norma_completa = 'existe'
    # try:
    #     with open('../pyjuriscrapper/txt/' + str(id_norma) + '.txt', 'r', encoding='utf-8') as archivo:
    #         norma_completa = cleantext(archivo.read()).split()
    # except:
    #     norma_completa = 'No disponible'
    # Imprimir el contenido del archivo
    #print(norma_completa)
    # return norma_completa

start_time = time()
df['norma_completa'] = df['id_norma'].apply(lambda id: agregar_txt(id))
print ("Tiempo de carga de txts a df: " + str(time() - start_time))

df_normas_completas = df[df['norma_completa']!='no']

df_listas = df_normas_completas[['id_norma','norma_completa']]

# Listas de entidades posibles
tipo_norma_list = df_normas_completas['tipo_norma'].apply(lambda r: cleantext(r)).unique().tolist()
organismo_list = df_normas_completas['organismo_origen'].apply(lambda r: cleantext(r)).unique().tolist()
with open('organismos.txt','w',encoding='utf-8') as orgs:
    for o in organismo_list:
        orgs.write(o + '\n')

exit(0)

repositorio_list = ['infoleg', 'saij']

def encontrar_entidad(texto):
    '''
    0:  NO ENTIDAD
    
    1:  B-NOR: Tipo de norma (INICIO)
    2:  I-NOR: Tipo de norma (CONTINUACION)
    
    3:  B-ORG: Organismos
    4:  I-ORG
    
    5:  B-REP: Repositorio (InfoLEG, SAIJ, etc)
    6:  I-REP
    
    7:  B-FEC: Fechas
    8:  I-FEC
    
    9:  B-MISC
    10: I-MISC
    '''
    entidades = []
    token = 0
    while token < len(texto):
        # REPOSITORIOS:
        print(token)
        flag_entidad = False
        for i in repositorio_list:
            compuesto = i.split()
            if len(compuesto) == 1:
                if texto[token] == i:
                    entidades.append(5)
                    flag_entidad = True
                    token = token + 1
                    break
                else:
                    continue
            elif len(texto) - token >= len(compuesto):
                aux = token
                flag_comp = True
                for el in compuesto:
                    if texto[aux] == el:
                        aux = aux + 1
                    else:
                        flag_comp = False
                        break
                if flag_comp:
                    entidades.append(5)
                    flag_entidad = True
                    for a in range(len(compuesto)-1):
                        entidades.append(6)
                        token = token + 1
                    break
                    
        # TIPOS DE NORMAS:
        for i in tipo_norma_list:
            compuesto = i.split()
            if len(compuesto) == 1:
                if texto[token] == i:
                    entidades.append(1)
                    flag_entidad = True
                    token = token + 1
                    break
                else:
                    continue
            elif len(texto) - token >= len(compuesto):
                aux = token
                flag_comp = True
                for el in compuesto:
                    if texto[aux] == el:
                        aux = aux + 1
                    else:
                        flag_comp = False
                        break
                if flag_comp:
                    flag_entidad = True
                    entidades.append(1)
                    for a in range(len(compuesto)-1):
                        entidades.append(2)
                        token = token + 1
                    break
                    
        # ORGANISMOS:
        for i in organismo_list:
            compuesto = i.split()
            if len(compuesto) == 1:
                if texto[token] == i:
                    entidades.append(3)
                    flag_entidad = True
                    token = token + 1
                    break
                else:
                    continue
            elif len(texto) - token >= len(compuesto):
                aux = token
                flag_comp = True
                for el in compuesto:
                    if texto[aux] == el:
                        aux = aux + 1
                    else:
                        flag_comp = False
                        break
                if flag_comp:
                    flag_entidad = True
                    entidades.append(3)
                    for a in range(len(compuesto)-1):
                        entidades.append(4)
                        token = token + 1
                    break

        if flag_entidad == False:
            entidades.append(0)
            token = token + 1
    return entidades


start_time = time()
df_listas['entidades'] = df_listas['norma_completa'].apply(lambda l: encontrar_entidad(l))
print ("Tiempo de carga de txts a df: " + str(time() - start_time))

 

