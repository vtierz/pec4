"""
Aquest script executa totes les funcions per als exercicis.
"""

from dataset.load import decompress_data
from dataset.load import csv_to_list_dict
from preprocess.transform import transform_csv_text
from preprocess.transform import eliminate_stopwords
from preprocess.transform import get_bow_list
from preprocess.transform import get_vocabulary
from preprocess.transform import save_dict_bow
from analysis.analyze import pre_word_cloud
from analysis.analyze import create_word_clouds
from analysis.analyze import create_histogram

# 1.1 Descomprimim les dades
decompress_data()

# 1.2 Carreguem les dades i imprimim els 5 elements de la llista de diccionaris
path_to_file = './data/twitter_reduced.csv'
print(csv_to_list_dict(path_to_file)[:5])

# 2.1 Transformem el text de l'arxiu
df_transformed = transform_csv_text(path_to_file)


# 2.2 Eliminem les stop words del diccionari
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
              'you', 'your', 'yours', 'yourself', 'yourselves', 'he',
              'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
              'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
              'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
              'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
              'been', 'being', 'have', 'has', 'had', 'having', 'do',
              'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
              'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
              'with', 'about', 'against', 'between', 'into', 'through', 'during',
              'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
              'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
              'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
              'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
              'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
              'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

df_trans_filtered = eliminate_stopwords(df_transformed, stop_words)

# Exercici 3.
# Mostrem 5 primers elements de la llista de diccionaris obtinguda.
list_bow = get_bow_list(df_trans_filtered)
print(list_bow[:5])

# Mostrem les 10 primeres paraules del vocabulari ordenades alfabèticament.
vocabulary_list = get_vocabulary(df_trans_filtered)
print(vocabulary_list[:10])


# Exercicis (4.1 i 4.2).
# Afegim diccionari de freqüències al dataset original i mostrem l'element 20.
# Guardem l'arxiu twitter_processed.csv a la carpeta "data".

path_output_file = './data/twitter_processed.csv'
save_dict_bow(df_trans_filtered, list_bow, path_output_file)

# Exercici 5.
# Creem les word clouds per cada cluster.
df_word_cloud = pre_word_cloud(path_output_file)
create_word_clouds(df_word_cloud)


# Exercici 6.
# Creem l'histograma per cada cluster.
create_histogram(df_word_cloud, 0)
create_histogram(df_word_cloud, 4)

# Exercici 7.
# a. Quines són les paraules més utilitzades en les crítiques positives?
print("En les crítiques positives trobem paraules com: \n"
      "good, love, like, thanks, lol, u, new, great, etc.\n"
      "Se m'acudeixen frases com I love you, I feel good, this is great, etc...")

# b. Quines són les paraules més utilitzades en les crítiques negatives?
print("Entre les crítiques negatives trobem paraules com: \n"
      "work, cant, dont, back, still, really, want, sad, miss, etc.\n"
      "Se m'acudeixen frases com I don't really want, I am sad, I miss...")

# c. Hi ha paraules que apareguin tant en les crítiques positives com en les negatives?
print("Apareixen tant a crítiques positives com negatives paraules com: \n"
      "im, go, get, good, today, time, etc...\n"
      "Totes tenen la característica que es poden utilitzar per escriure un esta positiu o negatiu")

# d. A partir de la word cloud, què es pot deduir sobre el sentiment general de cada grup?
print("A partir d'un word cloud se'n poden deduir les temàtiques de les converses d'usuaris de twitter: \n"
      "Per exemple, com s'ha comentat es pot deduir que la gent escriu tuits dient que estima \n"
      "a una persona o li encanta alguna cosa, o que no vol anar a treballar, que avui se sent bé o malament, etc.")
