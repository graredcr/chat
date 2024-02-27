import streamlit as st
import random
import time
import requests 
import os
from datetime import date


from dotenv import load_dotenv
from src.agents.lya2Agent import lya2Agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks import StreamlitCallbackHandler



os.environ['OPENAI_API_KEY'] = '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' 
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZGV2Mi5seWEyLmNvbSIsImF1ZCI6Imh0dHBzOlwvXC9kZXYyLmx5YTIuY29tIiwiaWF0IjoxNzA4OTYxMjcyLCJleHAiOjMyODU3NjEyNzIsImRhdGEiOnsidWlkIjoiMzc2IiwiYmQiOiJlbXByZXNhIiwiaWRfY2VudHJvIjoiMiIsInVzdWFyaW8iOiJhZGFsaWEiLCJpZF9iZGQiOiIxIiwiYWNjZXNvIjoiMSIsInpvbmEiOm51bGwsInV1aWQiOiIifX0.OIdg4pDIs88UtP5fl-bgmg2DxD2UwI5kEoxmjysvbbo'


def getAuthInfo( token): 
    url = 'https://dev2.lya2.com/lya2git/index01.php?pag=93&rest=true'
    auth = requests.get(url, headers={'Authorization': str(token)  })  
     
    if(auth.status_code == 200):
        data    = auth.json() 
        today   = date.today()
        d1      = today.strftime("%d/%m/%Y")

        context=[]
        context.append("Fecha, hoy es dia "+d1) 
        context.append("Email "+data['data']['0']['email'])
        context.append("Nivel de acceso "+data['data']['0']['acceso'] )
        context.append("Soy staff del "+data['data']['0']['name_subcenterprincipal'])
        context.append("Identificador de usuario "+data['data']['0']['id_personal'] )
        context.append("Identificador de sylbo "+data['data']['0']['id_sylbo'] )
        
        
        name = data['data']['0']['nombre']+" "+data['data']['0']['apellidos'];
        
        return [context, name] 
     
    return false

chat_history = []  
def initHistory(token):

    #get info for context and name
    [context, name] = getAuthInfo(token)

    #CHAT history
    chat_history = []  
    chat_history.extend(
                [
                    HumanMessage('Me llamo '+name),
                    AIMessage('Hola como estas'),
                ]
            ) 

    return [context, name, chat_history ]


[context, name, chat_history] = initHistory(token)

st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
agent = lya2Agent(  
    temp=0.0,
    context = context,
    token=token,
    #callbacks = [st_callback],
    stream=False
).agent_executor


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



# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.spinner('Wait for it...')
        st.markdown(prompt)
        chat_history.extend(
            [
                HumanMessage(content=prompt), 
                #AIMessage(content=response["output"]),
            ]
        )

    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        with st.spinner("waiting"): 
            response    = agent.invoke({"input": prompt, "chat_history": chat_history  } ) 
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        st.write(response["output"]) 
        chat_history.extend(
            [ 
                AIMessage(content=response["output"]),
            ]
        )

 
    #response = agent.invoke({"input": prompt, "chat_history": chat_history})
    #st.session_state.messages.append({"role": "assistant", "content": response["output"] })
    #st.markdown(response["output"])
    
    #stream          = st.write_stream(response["output"] )

    
 

        
