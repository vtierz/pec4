"""
Aquestes funcions són per transformar les dades del diccionari.
"""

import re
from collections import Counter
import pandas as pd


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
