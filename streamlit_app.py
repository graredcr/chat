import streamlit as st
import random
import time
import requests 
import os
import shutil
from datetime import date
import calendar


 
from src.agents.lya2Agent import lya2Agent
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

def createBdd(nivel):
    print('createBdd')
    namebdd = "manual_usuario"
    if int(nivel) < 1:
        namebdd = "manual_admin"

    if not os.path.isdir('./vectorBDD_'+nivel):
        print('createBdd start vector_'+nivel)
        if int(nivel) <= 1:
            #loader = PyPDFDirectoryLoader("./data/", extract_images=True)  
            #loader = PyPDFDirectoryLoader("./data/" )  

            #loader = PyPDFLoader("./data/puentes.pdf", extract_images=True)
            #loader = WebBaseLoader("https://dev2.lya2.com/lya2git/index01.php?pag=3000&tabs=2")
            #loader = CSVLoader('./data/imagenes.csv')
             
            loader = JSONLoader(
                file_path='./data/Solutions.json',
                jq_schema='.[5].category.folders[1].articles[]', 
                text_content=False,
                json_lines=True
                )
            
            #loader = UnstructuredXMLLoader(    "./data/Solutions.xml")


        else: 
            #loader          = PyPDFLoader("./data/manual_usuario.pdf", extract_images=True)
            loader = JSONLoader(
                file_path='./data/Solutions.json',
                jq_schema='.[5].category.folders[0].articles[]', 
                text_content=False,
                json_lines=True
                )

        
        documents       = loader.load()
        print(documents)
        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 

        #db = FAISS.from_documents(docs, embedding_function, persist_directory = persist_directory)
        faiss = FAISS.from_documents(docs, embedding_function)

        faiss.save_local("./vectorBDD_"+nivel, namebdd)
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
        indexdia = today.weekday();
        print("indexdiaindexdia: "+str(indexdia))
        #if indexdia < 0: 
        #    indexdia = 6
        diastring = calendar.day_name[indexdia]
        print(str(diastring))

        name = data['data']['0']['nombre']+" "+data['data']['0']['apellidos'];
        nivel = data['data']['0']['acceso']

        context=[]
        context.append("Nombre del usuario  es "+name) 
        context.append("Fecha, hoy es dia "+d1+", "+str(diastring))
        context.append("Email "+data['data']['0']['email'])
        context.append("Nivel de acceso "+nivel )
        context.append("Soy staff del "+data['data']['0']['name_subcenterprincipal'])
        context.append("Identificador de usuario "+data['data']['0']['id_personal'] )
        context.append("Identificador de sylbo "+data['data']['0']['id_sylbo'] )

        return [context, name, nivel ] 
     
def initHistory(token):
    print('initHistory')
    #get info for context and name
    [context, name, nivel] = getAuthInfo(token) 

    return [context, name, nivel]

def init(token):
    print('LOAD 1 - initHistory')

    [context, name, nivel] = initHistory(token)

    #CHAT history
        
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
        nivel = nivel,
        #callbacks = [st_callback],
        stream=False
    ).agent_executor

    #st.session_state["agent"] = agent 

    print('LOAD 2 -- CREATE BDD')
    createBdd(nivel)

    st.title("Lya2 chat")

    return agent

chat_history = [] 
context = ''
agent = ''

token_input = st.text_input('TOKEN', '')  
if token_input:
    print('if input token_input change')
    if "token_input" not in st.session_state: 
        st.session_state["token_input"] = token_input 
        token = "Bearer "+token_input
        
        
    else:
        st.session_state["token_input"] = token_input 
        token = "Bearer "+token_input
    
    agent = init(token)

    prompt = st.chat_input("Say something")
    if prompt: 
        print('LOAD   - promptpromptprompt') 

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
       
        with st.chat_message("user"): 
            st.markdown(prompt) 
            st.session_state.messages.append({"role": "user", "content": prompt}) 

            with st.spinner("waiting"): 
                response    = agent.invoke({"input": prompt+', explicación con alguna imagen si es posible en formato HTML.' , "chat_history": chat_history  } ) 

        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            st.write(response["output"]) 
            #st.image(imagenradom)
            chat_history.extend(
                [ 
                    HumanMessage(content=prompt), 
                    AIMessage(content=response["output"]),
                ]
            )
        