"""
Mòduls per resoldre els exercicis.
"""

import os
import glob
import zipfile
import csv
import re
from collections import Counter
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast



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


def transform_csv_text(path_to_file):
    """
    Aquesta funció elimina del 'text' URL, non-ASCII caràcters i caràcters especials.
    També passa a minúscula tot el text.
    :param path_to_file: path a l'arxiu.
    :return: Dataframe.
    """
    # Creem un dataframe a partir de l'arxiu passat com a paràmetre.
    df = pd.read_csv(path_to_file)

    # Passem el text a minúscula
    df['text'] = df['text'].str.lower()
    # Eliminem caràcters especials i símbols
    df['text'] = df['text'].apply(lambda t: re.sub(r'[^a-zA-Z0-9\s]|\t', '', t))
    # Eliminem caràcters non-ASCII
    df['text'] = df['text'].apply(lambda t: re.sub(r'[^\x00-\x7F]+', '', t))
    # Eliminem les url
    df['text'] = df['text'].apply(lambda t: re.sub(r'http\S+', '', t))
    print("S'ha transformat el text del l'arxiu.")
    return df


def eliminate_stopwords(dataframe, stop_words):
    """
    Aquesta funció elimina les stopwords (prèviament definides) del 'text' del diccionari.
    :param dataframe: Dataframe com a input.
    :param stop_words: Llista de paraules que es volen eliminar (stopwords).
    :return: Retorna el dataframe inicial sense les stopwords al 'text'.
    """
    dataframe['text'] = dataframe['text'].apply(
        lambda words: ' '.join(word for word in words.split(' ') if word not in stop_words))
    print("S'han eliminat les stop words del dataframe.")
    print(dataframe.tail(5))
    return dataframe


def get_bow_list(dataframe):
    """
    Funció per aconseguir una llista amb la bossa de paraules (bow) de cada 'text'.
    :param dataframe: dataframe com a input.
    :return: Llista de diccionaris amb el recompte de paraules del 'text'.
    """
    # Creem una llista buida per guardar els diccionaris amb les bow
    df = dataframe
    bow_list = [dict(Counter(text.split(' '))) if text is not None else {} for text in df['text']]
    print("S'ha creat la llista amb la bossa d'hores de cada tweet.")
    return bow_list


def get_vocabulary(dataframe):
    """
    Funció per crear un llista amb el vocabulari de tots els tweets.
    :param dataframe: Dataframe com a input.
    :return: Llista ordenada amb el vocabulari de paraules úniques de tweets
    """
    df = dataframe
    vocabulary = sorted(list(set(' '.join(df['text'].values).split(' '))))
    return vocabulary


def save_dict_bow(dataframe, bow_list_dict, path_output_file):
    """
    Funció per guardar la llista de diccionaris al dataset original.
    :param dataframe: Dataframe d'entrada.
    :param bow_list_dict: Llista de diccionaris amb bow.
    :param path_output_file: És el path a l'arxiu csv processat.
    :return: dataframe amb diccionari de bow com a nova columna.
    """
    # Definim el dataframe
    df = dataframe

    # Afegim el nou camp amb el diccionari de les bow per cada registre
    df['dict_freq'] = bow_list_dict
    df.to_csv(path_output_file, index=False)
    print("S'ha afegit el diccionari de freqüències a l'arxiu original")
    print("S'ha creat l'arxiu twitter_processed")
    print("Aquí sota es pot veure el registre número 20 de l'arxiu")
    print(df.iloc[20])
    return None


def pre_word_cloud(path_to_file):
    """
    Funció per crear word clouds per clústers
    :param path_to_file: Path a l'arxiu com a input
    :return: Retorna word clouds per clústers
    """
    # Carreguem l'arxiu d'entrada
    df = pd.read_csv(path_to_file)

    # Realitzem el càlcul del total d'observacions del df
    total_rows = len(df)

    # Calculem el total de nuls
    df['text'] = df['text'].replace(r'^\s*$', np.nan, regex=True)
    count_nulls = df['text'].isna().sum()

    # Calculem el percentatge de nulls i l'imprimim per pantalla
    print("El percentatge de nulls és: ", "{:.4f}%".format((count_nulls / total_rows) * 100))
    # Definim el clústers segons el valor del sentiment
    clusters = set(df['sentiment'])
    num_clusters = len(clusters)
    print("Hi ha {} clusters de sentiment a les dades is són els següents: {}".format(
        num_clusters, clusters))
    df.dropna(subset=['text'], inplace=True)
    return df


def create_word_clouds(dataframe):
    """
    Funció per crear word clouds para cada cluster d'un dataframe.
    :param dataframe: Dataframe com a input.
    :return: Wordclouds de tweets per cada cluster.
    """
    df = dataframe
    # Definim els clusters de sentiment
    cluster_sentiment = set(df['sentiment'])

    for cluster in cluster_sentiment:
        text_cluster = df[df['sentiment'] == cluster]['text']
        corpus = ' '.join(text_cluster)
        word_cloud = WordCloud(width=1000, height=500, background_color='black').generate(corpus)

        plt.figure(figsize=(10, 8))
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.title('Word Cloud del cluster número: {}'.format(cluster))
        plt.axis('off')
        plt.show()


def create_histogram(dataframe, cluster):
    """
    Funció per crear un histograma de 20 paraules més comunes d'un cluster.
    :param dataframe: Dataframe com a input.
    :param cluster: Cluster seleccionat.
    :return: Un histograma d'un cluster.
    """
    # Seleccionem les dades del cluster seleccionat.
    df = dataframe[dataframe['sentiment'] == cluster]

    # Seleccionem la columna on estan els diccionaris
    dict_freq = df['dict_freq']

    # Definim un diccionari buit on recollirem les freqüències totals
    total_word_freq = {}

    # Iterem cada registre on estan els diccionaris de freqüències
    for dict_str in dict_freq:
        # Avaluem si la cadena és un diccionari i la guardem com a diccionari
        dict_freq = ast.literal_eval(dict_str)

        # Iterem sobre cada diccionari de freqüències
        for word, freq in dict_freq.items():
            # Excluim les claus buides
            if word !='':
                # Afegim cada paraula al diccionari i sumem les frqüències
                total_word_freq[word] = total_word_freq.get(word, 0) + freq

    # Ordenem les paraules de forma descendent per freqüència total
    sorted_freq = sorted(total_word_freq.items(), key=lambda x: x[1], reverse=True)

    # Get the top 20 terms with highest frequencies
    selection = sorted_freq[:20]

    # Preparem les dades per l'histograma
    words = [item[0] for item in selection]
    freq = [item[1] for item in selection]

    # Configurem i mostrem l'histograma
    plt.bar(words, freq)
    plt.title('Top 20 paraules del cluster {}'.format(cluster))
    plt.xticks(rotation=45)
    plt.show()
