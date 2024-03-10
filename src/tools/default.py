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
  
class defaultTool(BaseTool):
    name = "defaultTool"
    description = "default tool for those questions for which no tool has been found"
    args_schema: Type[BaseModel] = SearchInput

    def __init__(self, llm: BaseLanguageModel, nivel: str ):
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