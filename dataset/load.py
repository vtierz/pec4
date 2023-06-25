"""
Aquest mòdul serveix per descomprimir l'arxiu twitter_reduced.zip
"""

import os
import glob
import zipfile
import csv


def decompress_data():
    """
    Funció per descomprimir l'arxiu twitter_reduced.zip
    Return: twitter_reduced.csv
    """

    # Definim el directori al arxiu per descomprimir
    zip_files = glob.glob('./data/twitter_reduced.zip')
    if zip_files:
        zip_file = zip_files[0]
    directory = os.path.dirname(zip_file)

    # Descomprimim l'arxiu i el guardem a la carpeta data
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(directory)

    print("L'arxiu s'ha descomprimit i guardat a la carpeta data")


def csv_to_list_dict(path_to_file):
    """
    Funció per passar un csv a una llista de diccionaris.
    :param path_to_file: Arxiu csv com a input.
    :return: Llista de diccionaris.
    """
    # Creem una llista buida
    list_dict = []

    # Obrim l'arxiu i el llegim
    with open(path_to_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Iterem per cada línia, la passem a diccionari i l'afegim a la llista
        for row in reader:
            list_dict.append(dict(row))
    return list_dict
