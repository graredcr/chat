import streamlit as st
import random
import time
import requests 
import os
import shutil
from datetime import date

 
from src.agents.lya2Agent import lya2Agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks import StreamlitCallbackHandler



from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import  CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS





os.environ['OPENAI_API_KEY']            = st.secrets["OPENAI_API_KEY"] 
os.environ['HUGGINGFACEHUB_API_TOKEN']  = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
token                                   = st.secrets["TOKEN"]

def createBdd():
    print('createBdd')
    if not os.path.isdir('./vectorBDD'):
        print('createBdd start')
        loader          = PyPDFLoader("./data/manual_usuario.pdf")
        documents       = loader.load()

        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=5500, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 

        #db = FAISS.from_documents(docs, embedding_function, persist_directory = persist_directory)
        faiss = FAISS.from_documents(docs, embedding_function)

        faiss.save_local("./vectorBDD", "manual_usuario")
    else:
        print('createBdd exist')



def getAuthInfo( token): 
    print('getAuthInfo')
    url = 'https://dev2.lya2.com/lya2git/index01.php?pag=93&rest=true'
    auth = requests.get(url, headers={'Authorization': str(token)  })  
     
    if(auth.status_code == 200):
        data    = auth.json() 
        today   = date.today()
        d1      = today.strftime("%d/%m/%Y")

        name = data['data']['0']['nombre']+" "+data['data']['0']['apellidos'];

        context=[]
        context.append("Nombre del usuario  es "+name) 
        context.append("Fecha, hoy es dia "+d1) 
        context.append("Email "+data['data']['0']['email'])
        context.append("Nivel de acceso "+data['data']['0']['acceso'] )
        context.append("Soy staff del "+data['data']['0']['name_subcenterprincipal'])
        context.append("Identificador de usuario "+data['data']['0']['id_personal'] )
        context.append("Identificador de sylbo "+data['data']['0']['id_sylbo'] )
        
        
       
        
        return [context, name] 
     
    return false
  
def initHistory(token):
    print('initHistory')
    #get info for context and name
    [context, name] = getAuthInfo(token) 

    return [context, name]

print('LOAD 1 - initHistory')
[context, name] = initHistory(token)

#CHAT history
chat_history = []  
chat_history.extend(
    [
        HumanMessage('Me llamo '+name),
        AIMessage('Hola como estas'),
    ]
) 
 

st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
agent = lya2Agent(  
    temp=0.0,
    context = context,
    token = token,
    #callbacks = [st_callback],
    stream=False
).agent_executor

print('LOAD 2 -- CREATE BDD')
createBdd()

st.title("Lya2 chat")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

 
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Say something")
if prompt:   
    with st.chat_message("user"): 
        st.markdown(prompt) 
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("waiting"): 
            response    = agent.invoke({"input": prompt, "chat_history": chat_history  } ) 

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        st.write(response["output"]) 
        chat_history.extend(
            [ 
                HumanMessage(content=prompt), 
                AIMessage(content=response["output"]),
            ]
        )
    
 

        
