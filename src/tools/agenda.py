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

#from langchain.chains import create_extraction_chain

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number


import requests
import json 
import time
from datetime import datetime
 

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query") 

class getAgenda(BaseTool):
    name = "getAgenda"
    description = "Information about my agenda and program. Only for knowledge of personal events or program. When you can deduce a date or range of dates in the query user then the tool is ok for use. Questions like, what should I do tomorrow or what's my turn the day after tomorrow, you can use this tool but is the last tool option ever."
    args_schema: Type[BaseModel] = SearchInput
    llm: BaseLanguageModel
    token: str

    def __init__(self, llm: BaseLanguageModel, token: str ): 
        super(getAgenda, self).__init__(llm=llm,token =  token)
         
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
         
        """Use the tool."""
        print('getAgenda')

        today   = datetime.today()
        d1      = today.strftime("%d/%m/%Y")

        schema = Object(
            id="dates",
            description=(
                "Extract dates of string.  "
            ),
            attributes=[
                Text(
                    id="date",
                    description="Date in format DD/MM/YYYY",
                    examples=[ 
                        ("Querria la lista de eventos para mañana si hoy es 2022-05-02", "2022-05-03"),
                        ("Que me toca hacer el dia 09/10/2023", "2023-10-09"),
                        ("Que hice ayer  si hoy es 2022-05-02", "2022-05-01"),
                        ("Sacame los eventos para de aquí a 5 dias, hoy es 2022-05-05", "2022-05-10"),
                        ("Me puedes extraer la lista entre hoy y mañana,  si hoy es 2022-05-02", "['2022-05-02', '2022-05-03']"),
                        ("Me puedes sacar la lista del 13/05/2005 al 18/05/2005", "['2005-05-13', '2005-05-18']")
                        ],
                    many=True,
                ), 
            ],
            many=False,
        )

        chain = create_extraction_chain(self.llm, schema, encoder_or_encoder_class='json')  
        output  = chain.invoke( query+" (hoy es "+d1+")" ) 
        
        #de momento cogemos solo la primera fecha
        fecha = output['text']['data']['dates']['date'][0]

        print(fecha)

        url = 'https://dev2.lya2.com/lya2git/index01.php?pag=300&tabs=1&alias=0&rest=D&action=calendarlist&fecha='+fecha
        r = requests.get(url, headers={'Authorization': self.token })
        data = r.json() 
        json_schema =  data['data']['rows']
        #print(json_schema) 

        return json_schema 
        

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

    
 