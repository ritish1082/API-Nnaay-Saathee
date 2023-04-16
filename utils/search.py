# Import Dependencies
import numpy as np
import pandas as pd
import faiss

df=pd.read_csv(r'datasets/statute.csv')

#PATHS
SBERT_INDEX=faiss.read_index(r'datasets/statute_sbert.index')
TFIDF_INDEX=faiss.read_index(r'datasets/statute_tfidf.index')


# what happens 5 are not present catch error
def get_common_top_k(tfidf_results, st_results):
    article_ids= list(set(tfidf_results[:]).intersection(st_results[:]))
    article_ids =  article_ids[:5] if len(article_ids)>4 else article_ids
    articles =[ get_article(article) for article in article_ids]
    return articles

def get_article(dataframe_idx):
    info = df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['article_id'] = info['Article_ID']
    meta_dict['article'] = info['Articles']
    return meta_dict


def search_article(tfidf_vector,sbert_vector):
    #Sbrert
    sbert_k = SBERT_INDEX.search(sbert_vector, 25)
    sbert_k_ids = list(np.unique(sbert_k[1].tolist()[0]))
    
    #TFIDF
    tfidf_k = TFIDF_INDEX.search(tfidf_vector, 25)
    tfidf_k_ids = list(np.unique(tfidf_k[1].tolist()[0]))

    return get_common_top_k(tfidf_k_ids,sbert_k_ids)

