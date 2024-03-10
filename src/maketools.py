import os

from langchain import agents
from langchain.base_language import BaseLanguageModel 
#from src.tools.default import defaultTool
#from src.tools.default import recoverPassword
#from src.tools.default import semanticSearch
from src.tools.agenda import getAgenda 
from src.tools.faiss import faissSeach 
from src.tools.faissAdministrator import faissAdministratorSearch 

#from lya2tools.recuperarDatosPersonales import recuperarDatosPersonalesTool
 


def make_tools(llm: BaseLanguageModel, token: str ,nivel: str, api_keys: dict = {}, verbose=False):
     


    return [ 
        #defaultTool(llm = llm), 
        #semanticSearch(llm), 
        #recoverPassword(llm),
        faissSeach(llm = llm, nivel = nivel),
        faissAdministratorSearch(llm = llm, nivel = nivel),
        getAgenda(llm = llm,token = token),
    ]
