import streamlit as st
import random
import time
import requests 
import os
import shutil
from datetime import date
import calendar


from src.classes.vectorbdd import vectorBddLya2
from src.classes.lya2Rest import lya2Rest 

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks import StreamlitCallbackHandler 

from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader, WebBaseLoader, CSVLoader, UnstructuredXMLLoader, JSONLoader
#from langchain_community.document_loaders.image import UnstructuredImageLoader


from langchain.text_splitter import  CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS


os.environ['OPENAI_API_KEY']            = st.secrets["OPENAI_API_KEY"] 
os.environ['HUGGINGFACEHUB_API_TOKEN']  = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
#token                                   = st.secrets["TOKEN"]

chat_history = [] 
context = ''
agent = ''

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False 

def disabledTokenInput():
    st.session_state["disabled"] = True 

token_input = st.text_input(
    "TOKEN", 
    disabled = st.session_state["disabled"], 
    on_change = disabledTokenInput
)

if token_input:
    print('if input token_input change')
    if "token_input" not in st.session_state: 
        st.session_state["token_input"] = token_input 
        token = "Bearer "+token_input 
    else:
        st.session_state["token_input"] = token_input 
        token = "Bearer "+token_input
    
    lya2RestObj = lya2Rest()
    [context, name, nivel] = lya2RestObj.getAuthInfo(token) 

    vectorBddLya2Obj = vectorBddLya2()
    vectorBddLya2Obj.createBdd(nivel)
 
if st.session_state["disabled"] == True: 
    prompt = st.chat_input( "Say something"  )
    if prompt: 
        print('LOAD   - promptpromptprompt') 
        