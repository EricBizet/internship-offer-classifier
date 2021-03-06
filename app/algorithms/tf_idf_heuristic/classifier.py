import numpy as np
import pandas as pd
import collections
import re
from utils import abs_path

def predict(text) -> dict:
    words=re.findall("[\w']+", text)

    # count times of appearance of each word
    frequency = dict(collections.Counter(words))

    dataframe = pd.DataFrame(frequency.items(), columns=["word", "n_appear"])

    # Nettoyage

    stopwords = set()
    stopwords_path = abs_path("algorithms/tf_idf_heuristic/stopWordsFR.txt")
    with open(stopwords_path) as file:
        for word in file:
            stopwords.add(word[:-1])

    dataframe['word'] = dataframe['word'].astype(str)

    filtered_df = dataframe[~dataframe["word"].isin(stopwords)]

    # Attribution des catégories


    keywords = {
        "développement": 0,
        "web" : 0,
        "développeur" : 0,
        "front" : 0,
        "backend" : 0,
        "c++" : 0,
        "machine" : 1,
        "learning" : 1,
        "data" : 1,
        "image" : 2,
        "discretisation" : 2,
        "points" : 2,
        "objet" : 2,
        "grille" : 2,
        "3D" : 2
    }

    categories = [
        "Developpement",
        "MachineLearning",
        "TraitementImage"
    ]

    keyword_df = pd.DataFrame(keywords.items(), columns=["word", "category"])
    categories_df = pd.DataFrame(categories, columns=["label"])

    in_text_kw_df = keyword_df.merge(filtered_df, left_on='word', right_on='word')
    cat_count = in_text_kw_df.groupby(['category']).sum()



    categories_df['n_appear'] = cat_count['n_appear']
    categories_df['exponential'] = np.exp(categories_df['n_appear'])
    exp_sum = np.sum(categories_df['exponential'])
    if exp_sum != 0: 
        categories_df['probability'] = categories_df['exponential'] / exp_sum
    else:
        categories_df['probability'] = 1 / categories_df.shape[0]

    result_probability = categories_df[['label', 'probability']]
    result_probability = result_probability.fillna(0)
    labels_dict = result_probability.to_dict()
    
    return labels_dict