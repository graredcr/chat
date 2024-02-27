from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, List, Union
from langchain_openai import OpenAI
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun, CallbackManagerForToolRun)
from langchain.chains import LLMMathChain, LLMChain

from langchain.base_language import BaseLanguageModel

from langchain_community.embeddings.sentence_transformer import  SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
 
from langchain.prompts import PromptTemplate

import requests
import json



from typing import Union
from math import pi

from typing import Any 


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query") 

class getAgenda(BaseTool):
    name = "getAgenda"
    description = "Información sobre mi agenda, mi calendario. Lista de eventos, programación o sessiones"
    args_schema: Type[BaseModel] = SearchInput
    llm: BaseLanguageModel

    def __init__(self, llm: BaseLanguageModel ): 
        super(getAgenda, self).__init__(llm=llm)
         


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        #print('getCalendarInfo getCalendarInfo getCalendarInfo getCalendarInfo') 
        url = 'https://dev2.lya2.com/lya2git/index01.php?pag=300&tabs=1&alias=0&rest=D&action=calendarlist&tipo=month&fecha=2024-02-19tipo=DAY'
        r = requests.get(url, headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZGV2Mi5seWEyLmNvbSIsImF1ZCI6Imh0dHBzOlwvXC9kZXYyLmx5YTIuY29tIiwiaWF0IjoxNzA4MzY3Nzk5LCJleHAiOjMyODUxNjc3OTksImRhdGEiOnsidWlkIjoiMTMiLCJiZCI6ImVtcHJlc2EiLCJpZF9jZW50cm8iOiIyIiwidXN1YXJpbyI6InNvbGVyIiwiaWRfYmRkIjoiMSIsImFjY2VzbyI6IjIiLCJ6b25hIjpudWxsLCJ1dWlkIjoiIn19.jRx6ubaiWK-YCX2m9XjfB-fwvgwt6mPWRyB4RLndY3g'})
        data = r.json() 
        json_schema =  data['data']['rows']
        #print(json_schema)
        #Format the JSON schema into a string representation 
        json_schema_str = json.dumps(json_schema)
        #data = f"Esquema JSON de los eventos. :"+json_schema_str+" type:3 son tareas, type:4 vacaciones o permisos. "
      
        #foormatear información
        template = """devolver el listado eventos con el siguiente formato:

        - Nombre evento
        - descripción
        - Fecha
        - Hora
        - Lugar
  \
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
        )
 
        #CHAINS ***********
        chain = LLMChain(
            llm = self.llm, 
            prompt = prompt, 
            verbose=False 
        )
 

        #output = chain.invoke({"json": json.dumps(json_schema)}) 

         

        output  = chain.invoke({"question": json_schema})

        return output 
        

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

    

class defaultTool(BaseTool):
    name = "defaultTool"
    description = "default tool for those questions for which no tool has been found"
    args_schema: Type[BaseModel] = SearchInput

    def __init__(self, llm: BaseLanguageModel ):
        super(defaultTool, self).__init__(llm=llm)


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return "No se ha encontrado una tool para responder a esta pregunta.\
         Buscamos en el historial o contexto si tenemos la respuestas \
         Si no la tenemos, debemos preguntar al usuario que reformule la pregunta porque no lo hemos entedido. \
         Seguidamente  listar las desripciones de nuestras funciones  ."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class semanticSearch(BaseTool):
    name = "semanticSearch"
    description = 'userful for search  respond questions of lya2 application or sylbo application.\
     Questions about: Area, horario, peonada, permisos, informes, instrucciones del calendario o agenda personal, sesiones.'
    args_schema: Type[BaseModel] = SearchInput

    def __init__(self, llm: BaseLanguageModel ):
        super(semanticSearch, self).__init__(llm=llm)


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print("\n Semantic search:"+query+" \n") 
        """Use the tool."""
        persist_directory   = "./chatgptbdd2" 
        embedding_function  = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 
        vectordb            = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
        answers             = vectordb.similarity_search(query);

        context             = []
        for answer in answers: 
            context.append(answer.page_content)  

        return context

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

    

class recoverPassword(BaseTool):
    name = "lost_my_passwrod"
    description = "useful for restore the password"
    args_schema: Type[BaseModel] = SearchInput 
    llm: BaseLanguageModel

    def __init__(self, llm: BaseLanguageModel ):  
        super(recoverPassword, self).__init__(llm=llm)
    

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        confirmation = input("Necesitas que te ayude a recuperar tu passwrod? Y/N")
        if confirmation == 'Y': 
            return self.llm.invoke('Responder al usuario que le hemo enviado un email con las intrucciones. \
                Que mire su correo y sigua las instrucciones.')
        else: 
            return self.llm.invoke('No hemos entendido lo que el usuario quiere. Responder amablemente.') 

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")