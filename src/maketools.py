import os

from langchain import agents
from langchain.base_language import BaseLanguageModel 
from src.tools.default import defaultTool
from src.tools.default import recoverPassword
from src.tools.default import semanticSearch
from src.tools.default import getAgenda 

#from lya2tools.recuperarDatosPersonales import recuperarDatosPersonalesTool
 


def make_tools(llm: BaseLanguageModel, api_keys: dict = {}, verbose=False):
     


    return [ 
        defaultTool(llm), 
        #semanticSearch(llm), 
        recoverPassword(llm), 
        getAgenda(llm),
    ]
