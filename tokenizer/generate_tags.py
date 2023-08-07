### Tokenizer
# Dado un archivo de texto, genera un archivo con una palabra por linea, seguida de su tag
# Los tags se dan en un archivo tags.txt, con el siguiente formato:
import glob
import re

tag_nulo = 0


def leer_tag_names() -> list[str]:
    """
    Lee los tags del archivo tags.txt
    :return: lista de tags
    """
    tag_names = []
    with open('tags.txt', 'r', encoding='utf-8') as f:
        for tag in f.readlines():
            tag_name = tag.strip('\n').split(' ')[1]
            if tag_name != '':
                tag_names.append(tag_name)
    return tag_names


def cleantext(text):
    """
    Limpia el texto de caracteres especiales, acentos, etc.
    :param text:
    :return:
    """
    # Eliminar etiquetas HTML usando expresiones regulares
    cleaned_text = re.sub(r'<[^>]*>', '', text)

    # Reemplazar espacios múltiples por un solo espacio
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    # Eliminar espacios al principio y al final del texto
    cleaned_text = cleaned_text.strip()

    # Convertir todo el texto a minúsculas (opcional)
    cleaned_text = cleaned_text.lower()

    # Eliminar caracteres especiales y dígitos
    cleaned_text = re.sub(r'[!@#]', '', cleaned_text)

    # Patrón de expresión regular para buscar caracteres duplicados, excepto 'C', 'R' y 'L'
    cleaned_text = re.sub(r'([^crlw])\1+', r'\1', cleaned_text)

    # Corregir palabras repetidas que se repiten más de 2 veces
    cleaned_text = re.sub(r'\b(\w+)\b(?:\s+\1)+', r'\1', cleaned_text)

    # Eliminar acentos:
    cleaned_text = cleaned_text.replace('á', 'a')
    cleaned_text = cleaned_text.replace('é', 'e')
    cleaned_text = cleaned_text.replace('í', 'i')
    cleaned_text = cleaned_text.replace('ó', 'o')
    cleaned_text = cleaned_text.replace('ú', 'u')

    return cleaned_text


def imprimir_linea_y_tags(linea: list[str], tags: list[int], tag_names: list[str]) -> None:
    """
    Imprime una linea de texto y sus tags
    :param linea:
    :param tags:
    :return:
    """
    line1 = ""
    line2 = ""
    for word, label in zip(linea, tags):
        full_label = tag_names[label]
        max_length = max(len(word), len(full_label))
        line1 += word + " " * (max_length - len(word) + 1)
        line2 += full_label + " " * (max_length - len(full_label) + 1)
    print(line1)
    print(line2)


def taggea_frase(frase: list[str], tag_inicio: int, tag_continuacion: int, palabras: list[str], tags: list[int]) -> None:
    """
    Dada una frase, la buscar en la lista de palabras y asigna los tags que correspondan.
    La frase puede aparecer mas de una vez
    :param frase:
    :param tag_inicio:
    :param tag_continuacion:
    :param palabras:
    :param tags:
    :return:
    """
    # for i in range(len(frase)):
    try:
        comienzo = palabras.index(frase[0], 0, len(palabras) - len(frase[0]))
    except ValueError:
        comienzo = -1

    while comienzo >= 0:
        if tags[comienzo] == tag_nulo:
            encontrada = True
            for j in range(1, len(frase)):
                if comienzo + j >= len(palabras) \
                        or palabras[comienzo + j] != frase[j] \
                        or tags[comienzo + j] != tag_nulo:
                    encontrada = False
                    break
            if encontrada:
                tags[comienzo] = tag_inicio
                for j in range(1, len(frase)):
                    tags[comienzo + j] = tag_continuacion
                comienzo = comienzo + len(frase) - 1
        try:
            comienzo = palabras.index(frase[0], comienzo + 1, len(palabras) - len(frase[0]))
        except ValueError:
            comienzo = -1


def completa_tags(frases: list[str], tag_inicio: int, tag_continuacion: int, palabras: list[str], tags: list[int]) -> None:
    """
    Dada una lista de frases, busca cada una en la lista de palabras y completa los tags
    :param frases:
    :param tag_inicio:
    :param tag_continuacion:
    :param palabras:
    :param tags:
    :return:
    """
    for frase in frases:
        taggea_frase(frase.split(' '), tag_inicio, tag_continuacion, palabras, tags)
        # si ya 'taggeo' la linea entera, no hace falta seguir buscando
        try:
            tags.index(tag_nulo)
        except ValueError:
            break


def procesar_archivo(archivo, dest_file):
    """ procesa un archivo linea por linea y muestra los resultados
    :param idx: id del archivo
    :return:
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f.readlines():
            linea = cleantext(linea)
            if linea == '':
                continue

            palabras = linea.split(' ')
            tags = [tag_nulo for i in range(len(palabras))]
            completa_tags(tipos_normas, tag_inicio=1, tag_continuacion=2, palabras=palabras, tags=tags)
            completa_tags(organismos, tag_inicio=3, tag_continuacion=4, palabras=palabras, tags=tags)
            for p, t in zip(palabras, tags):
                dest_file.write(f'{p} {t}\n')
            dest_file.write('\n')  # una linea en blanco entre cada linea de texto
            # imprimir_linea_y_tags(palabras, tags, tag_names)
            # print()


if __name__ == '__main__':
    # prepara las listas generales
    with open('tipos_normas.txt', 'r', encoding='utf-8') as f:
        tipos_normas = f.read().splitlines()

    with open('organismos.txt', 'r', encoding='utf-8') as f:
        organismos = f.read().splitlines()

    tag_names = leer_tag_names()

    with open('dataset.csv', 'w', encoding='utf-8') as dest_file:
        num_archivo = 0
        for f in glob.glob('../scrapper/txt/*.txt'):
            procesar_archivo(f, dest_file)
            num_archivo += 1
            if num_archivo % 100 == 0:
                print(f'Procesados {num_archivo} archivos')
