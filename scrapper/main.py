import csv
import os

import requests
from bs4 import BeautifulSoup

html_path = './html'
txt_path = './txt'


def extraer_texto(id):
    archivo_html = f'{html_path}/{id}.html'
    with open(archivo_html, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        texto = soup.get_text()

    archivo_txt = f'{txt_path}/{id}.txt'
    with open(archivo_txt, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f'Texto extraido de {archivo_html} y guardado en {archivo_txt}')


def descargar_texto_original(id, url):
    archivo = f'{html_path}/{id}.html'
    if os.path.exists(archivo):
        print(f'El archivo {archivo} ya existe')
        return

    print(f'Descargando texto original {id}')
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 200:
        with open(archivo, 'wb') as f:
            f.write(response.content)
        print(f'Texto original {id} descargado en {archivo}')
        extraer_texto(id)


def parse_csv(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        linea = 0
        procesadas = 0
        for row in csv_reader:
            if linea < 1:
                # saltea los headers
                linea += 1
                continue

            # if procesadas == 10:
            #     break

            if row[13] != '':
                # print(f'Id: {row[0]}, Tipo: {row[1]}, Numero: {row[2]}, TextoOriginal: {row[13]}, TextoActualizado: {row[14]}, ModificadoPor: {row[15]}, ModificaA: {row[16]}')
                descargar_texto_original(row[0], row[13])
                procesadas += 1
                print(f'Lineas procesadas: {procesadas}')

            linea += 1


if __name__ == '__main__':
    os.makedirs(html_path, exist_ok=True)
    os.makedirs(txt_path, exist_ok=True)

    parse_csv('../base-infoleg-normativa-nacional.csv')
