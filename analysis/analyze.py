"""
Aquestes funcions són per analitzar les dades.
"""


import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast


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
    # Definim els clústers segons el valor del sentiment
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
    :return: Word clouds de tweets per cada cluster.
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
            # Filtrem les claus buides
            if word !='':
                # Afegim cada paraula al diccionari i sumem les freqüències
                total_word_freq[word] = total_word_freq.get(word, 0) + freq

    # Ordenem les paraules de forma descendent per freqüència total
    sorted_freq = sorted(total_word_freq.items(), key=lambda x: x[1], reverse=True)

    # Ens quedem amb el top 20
    selection = sorted_freq[:20]

    # Preparem les dades per l'histograma
    words = [item[0] for item in selection]
    freq = [item[1] for item in selection]

    # Configurem i mostrem l'histograma
    plt.bar(words, freq)
    plt.title('Top 20 paraules del cluster {}'.format(cluster))
    plt.xticks(rotation=45)
    plt.show()
