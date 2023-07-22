import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import json
import ast

st.set_page_config(
    page_title="Legal Information Retreival",
    page_icon= "⚖️", 
    layout="wide"
)

st.header("Nnaay Saathee UI")

txt = st.text_area(label="Find statute to your case",placeholder="write your use case")



if st.button('Find Statute'):
    if len(txt)<5:
        st.text("⚠️ Query too small to be fetched !")
    else:
        start_time=time.time()
        res=requests.get(url="http://127.0.0.1:8000/statute/?query="+txt)
        articles=res.json()
        if articles['code']==200:
            statutes=articles['statute']
            st.text("Fetched in "+ str(time.time()-start_time)[:4]+"seconds")
        else:
            st.text("SERVER ERROR FOUND !")

        if len(statutes) > 0:
            st.table(statutes)
        else:
            st.text("⚠️ Query not clear ! Rephrase query ")



if st.button('Similar Case'):
    if len(txt)<5:
        st.text("⚠️ Query too small to be fetched !")
    else:
        start_time=time.time()
        res=requests.get(url="http://127.0.0.1:8000/case/?query="+txt)
        articles=res.json() 
        cases=articles['case']
        cases_f=ast.literal_eval(cases)
        st.table(cases_f)
        # cases=articles['case']
        # st.table(cases)
        # if articles['code']==200:
        #     cases=articles['case']
        #     st.text("Fetched in "+ str(time.time()-start_time)[:4]+"seconds")
        #     # st.write(articles)
        # else:
        #     st.text("SERVER ERROR FOUND !")

        # if len(cases) > 0:
        #     st.table(cases)
        # else:
        #     st.text("⚠️ Query not clear ! Rephrase query ")
