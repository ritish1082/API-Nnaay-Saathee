# Import Dependencies
import numpy as np
import pandas as pd
import faiss
import streamlit as st

#PATHS
statute_df=pd.read_csv(r'datasets/statute.csv')
case_df=pd.read_csv(r'datasets/raw_case_judgements_paragraphs.csv')

STATUTE_SBERT_INDEX=faiss.read_index(r'datasets/statute_sbert.index')
STATUTE_TFIDF_INDEX=faiss.read_index(r'datasets/statute_tfidf.index')

CASE_SBERT_INDEX=faiss.read_index(r'datasets/case_sbert.index')
# CASE_TFIDF_INDEX=faiss.read_index('')

# what happens 5 are not present catch error
def get_common_top_k(tfidf_results, st_results,article=1):
    article_ids= list(set(tfidf_results[:]).intersection(st_results[:]))
    article_ids =  article_ids[:5] if len(article_ids)>4 else article_ids
    if article==1:
        articles =[ get_article(article) for article in article_ids]
    else:
        articles =[ get_case(article) for article in article_ids]
    return articles

def get_article(dataframe_idx):
    info = statute_df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['article_id'] = info['Article_ID']
    meta_dict['article'] = info['Articles']
    return meta_dict


def search_article(tfidf_vector,sbert_vector):
    #Sbrert
    sbert_k = STATUTE_SBERT_INDEX.search(sbert_vector, 25)
    sbert_k_ids = list(np.unique(sbert_k[1].tolist()[0]))
    
    #TFIDF
    tfidf_k = STATUTE_TFIDF_INDEX.search(tfidf_vector, 25)
    tfidf_k_ids = list(np.unique(tfidf_k[1].tolist()[0]))

    return get_common_top_k(tfidf_k_ids,sbert_k_ids)


def get_case(dataframe_idx):
    info = case_df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['case_id'] = info['case_id']
    meta_dict['paragraph'] = info['paragraph']
    return meta_dict


def search_case(sbert_vector):
    #Sbrert
    sbert_k = CASE_SBERT_INDEX.search(sbert_vector, 5)
    sbert_k_ids = list(np.unique(sbert_k[1].tolist()[0]))
    cases = [get_case(int(article)) for article in sbert_k_ids]

    return cases
    #TFIDF
    # tfidf_k_ids=adsfghjkl
    # # tfidf_k = CASE_TFIDF_INDEX.search(tfidf_vector, 25)
    # # tfidf_k_ids = list(np.unique(tfidf_k[1].tolist()[0]))

    # return get_common_top_k(tfidf_k_ids,sbert_k_ids)