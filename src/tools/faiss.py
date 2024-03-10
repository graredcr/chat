from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, List, Union
from langchain_openai import OpenAI
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun, CallbackManagerForToolRun)

#from langchain_community.document_loaders import PyPDFLoader
#from langchain.text_splitter import  CharacterTextSplitter
#from langchain_openai import OpenAIEmbeddings 

from langchain.base_language import BaseLanguageModel 
from langchain_community.embeddings import SentenceTransformerEmbeddings 
from langchain_community.vectorstores import FAISS

from src.classes.num_tokens_from_messages import num_tokens_from_messages

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query") 


class faissSeach(BaseTool):
    name = "faissSeach"
    description = "Userful when the user needs steps for make something in lya2 aplication or configuration  lya2 aplication. \
     - Description home \
     - Lya2 Intern messages \
     - Sylbo messages \
     - My claendar description \
     - Events \
     - Show/Hide Sections Button\
     - General Calendar \
     - Permission or vacation\
     - Cahnges \
     - simple change \
     - Double change \
     - Substitution \
     - Session \
     - daily program \
     - weekly program \
     - Rastrico \
     - User and password \
     - lya2 calendar synchronization \
    Only queries of lya2 product. No greetings, goodbyes and otrhe things \
    You can extract images and add ths images to anwer. \
    "
    args_schema: Type[BaseModel] = SearchInput
    nivel: str

    def __init__(self, llm: BaseLanguageModel , nivel: str):
        super(faissSeach, self).__init__(llm=llm , nivel=nivel)
     
 
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("\nfaissSeach") 
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("./vectorBDD_"+self.nivel,embedding_function, "manual_usuario") 
        output =  db.similarity_search(query+". Images and links included if you found some relationated with query", 3)

        docs_and_scores = db.similarity_search_with_score(query)
        responses = []
        for scores in docs_and_scores:
            print( scores[1] )
            print( scores[0] )
            print( "\n" )
            #añadimos solo los que superen el score 1.7
            if scores[1] > 1.65:
                responses.append(scores[0])

        #encoding = tiktoken.get_encoding("cl100k_base")
        # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0125")
        numtokens = num_tokens_from_messages(str(responses)) 
        print("numtokens:: "+str(numtokens))
        if numtokens < 15000:
            return responses
        return  'No hay respuesta posible'

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async") 