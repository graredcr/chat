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

  
#from langchain_community.vectorstores import FAISS


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query") 
  

class faissSeach(BaseTool):
    name = "faissSeach"
    description = "Userful when the user needs steps for make something related of lya2 product  or sylbo product.\
    When the query contains one of following words: Schedules, areas, permits, vacations, peonadas, releases, library, messages\
    you can extract images and add ths images to anwer."
    args_schema: Type[BaseModel] = SearchInput

    def __init__(self, llm: BaseLanguageModel ):
        super(faissSeach, self).__init__(llm=llm)


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("\nfaissSeach")
        """loader          = PyPDFLoader("./data/manual_usuario.pdf")
        documents       = loader.load()
        text_splitter   = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs            = text_splitter.split_documents(documents)
        embeddings      = OpenAIEmbeddings()
        db              = FAISS.from_documents(docs, embeddings)""" 
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = faiss.load_local("./vectorBDD",embedding_function, "manual_usuario")



        #db = createBdd() 
 
        return  db.similarity_search(query, 3) 

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async") 