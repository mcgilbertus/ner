import asyncio
import csv
import datetime
import os

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

html_path = './html'
txt_path = './txt'


async def extraer_texto(id):
    archivo_html = f'{html_path}/{id}.html'
    async with aiofiles.open(archivo_html, 'r') as f:
        content = await f.read()
        soup = BeautifulSoup(content, 'html.parser')
        texto = soup.get_text()

    archivo_txt = f'{txt_path}/{id}.txt'
    async with aiofiles.open(archivo_txt, 'w', encoding='utf-8') as f:
        await f.write(texto)
    print(f'Texto extraido de {archivo_html} y guardado en {archivo_txt}')


async def descargar_texto_original(id, url, session):
    archivo = f'{html_path}/{id}.html'
    if os.path.exists(archivo):
        print(f'El archivo {archivo} ya existe')
        return

    print(f'Descargando texto original {id}')
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            async with aiofiles.open(archivo, 'wb') as f:
                await f.write(content)
            print(f'Texto original {id} descargado en {archivo}')
            await extraer_texto(id)


async def parse_csv(archivo):
    async with aiohttp.ClientSession() as session:
        with open(archivo, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"')
            linea = 0
            descargados = 0
            for row in csv_reader:
                if linea < 1:
                    # saltea los headers
                    linea += 1
                    continue

                if linea % 100 == 0:
                    print(f'Lineas procesadas: {linea}')

                if os.path.exists(f'{html_path}/{row[0]}.html'):
                    print(f'salteando archivo existente: {row[0]}')
                    linea += 1
                    continue

                # if procesadas == 10:
                #     break

                if row[4] != '':
                    # print(f'Id: {row[0]}, Tipo: {row[1]}, Numero: {row[2]}, TextoOriginal: {row[13]}, TextoActualizado: {row[14]}, ModificadoPor: {row[15]}, ModificaA: {row[16]}')
                    try:
                        await descargar_texto_original(row[0], row[4], session)
                        descargados += 1
                        if descargados % 100 == 0:
                            print(f'Descargados: {descargados}')
                    except Exception as e:
                        print(f'Error procesando linea {linea}: {e}')

                linea += 1


if __name__ == '__main__':
    os.makedirs(html_path, exist_ok=True)
    os.makedirs(txt_path, exist_ok=True)
    print(f'{datetime.datetime.now()} - Iniciando proceso')
    asyncio.run(parse_csv('../Normas-Filtradras-y-Balanceadas.csv'))
    print(f'{datetime.datetime.now()} - Fin!')

