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
    description = "For a common user query, greetings, questions other than lya2"
    args_schema: Type[BaseModel] = SearchInput

    def __init__(self, llm: BaseLanguageModel  ):
        super(defaultTool, self).__init__(llm=llm)


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        print("default tool")
        """Use the tool."""
        return query

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")