# Importing Dependecies
from fastapi import FastAPI
import time
import pickle
from utils import search
from sentence_transformers import SentenceTransformer


#PATHS
STATUTE_MODEL= SentenceTransformer(r'models\msmarco-distilbert-base-v4-e1')


app = FastAPI()


@app.get("/")
def start():
    try:
        return {'code':200}
    
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return {"error":message}


@app.get("/statute/")
async def get_statute(query: str):
    try:
        start_time = time.time()
        
        vectorizer=pickle.load(open(r'models\vectorizer.pkl','rb'))
        tfidf_vector=vectorizer.transform([query]).toarray().astype('float32')

        sbert_vector=STATUTE_MODEL.encode([query])
        
        articles=search.search_article(tfidf_vector,sbert_vector)

        return {'code':200,'statute':articles,'time':time.time()-start_time}

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return {"error":message}

