import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv
from agents.lya2Agent import lya2Agent
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage, HumanMessage


os.environ['OPENAI_API_KEY'] = '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' 
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'


load_dotenv()
ss = st.session_state
 





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

agent = lya2Agent(  
    temp=0.0,
    context = context,
    token=token
).agent_executor

while True:
    message = input("\nHuman: ")
    if message=='exit':
        print(f"End this conversation")
        break
    if message: 
        """with get_openai_callback() as cb:
            response = agent.invoke({"input": message})
            print('**** RESPONSE ^^^')
            print(response) 
            print(cb)
            """

        response = agent.invoke({"input": message, "chat_history": chat_history})
        #print("\not**** RESPONSE AGENT ^^^\n")
        print( response["output"] ) 

        chat_history.extend(
            [
                HumanMessage(content=message),
                AIMessage(content=response["output"]),
            ]
        )
        #response = chain(message)
        #print(f"AI: {response}")


