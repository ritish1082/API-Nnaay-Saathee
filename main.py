import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Legal Information Retreival",
    page_icon= "⚖️", 
    layout="wide"
)

st.header("Nnaay Saathee UI")

txt = st.text_area(label="Find statute to your case",placeholder="write your use case")



if st.button('Find Statute'):
    start_time=time.time()
    res=requests.get(url="http://127.0.0.1:8000/statute/?query="+txt)
    articles=res.json()
    if articles['code']==200:
        statutes=articles['statute']
        # statute_id=articles['article_id']
        st.text("Fetched in "+ str(time.time()-start_time)[:4]+"seconds")
        # st.write(articles)
    else:
        st.text("SERVER ERROR FOUND !")

    st.table(statutes)

