import langchain
import requests 
from pydantic import ValidationError 
from langchain_core.prompts import ChatPromptTemplate


#from langchain import  chains
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#from rmrkl  import ChatZeroShotAgent, RetryAgentExecutor

from langchain.agents import Tool  
from langchain.agents import AgentExecutor, create_structured_chat_agent, ZeroShotAgent

from langchain_community.llms import HuggingFaceHub

from dotenv import load_dotenv
from typing import Optional
 
from src.maketools import make_tools

from openai import OpenAI  
from langchain_openai import ChatOpenAI  
from langchain.chains import LLMChain 

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.output_parsers import StrOutputParser

from langchain.prompts import MessagesPlaceholder 


def _make_llm(model, temp, api_key, callbacks, streaming: bool = False):
    llm = ChatOpenAI(
            temperature=temp, 
            model_name= model,
            request_timeout=1000,
            #max_tokens=1000,
            streaming=False, #si true excribe mientras encuentra resultados
            #callbacks=[StreamingStdOutCallbackHandler()],
            callbacks = callbacks,
            openai_api_key = api_key,
            verbose = False,
            )
     

    #llm = HuggingFaceHub(repo_id= 'google/flan-t5-xl', bind_tools={"temperature":0, "max_length":512})
 

    return llm

class lya2Agent:
    def __init__(
        self,
        token,
        nivel,
        callbacks=[StreamingStdOutCallbackHandler()], 
        tools=None,
        #model="llama-13b-chat"
        model="gpt-3.5-turbo-0125",
        #model="gpt-4", 
        tools_model="gpt-3.5-turbo-0125",
        #tools_model="gpt-4",
        temp=0.0,
        context='', 
        max_iterations=3,
        verbose=False,
        stream: bool = False,
        openai_api_key: Optional[str] = None,
        api_keys: dict = {},

    ):
        """Initialize ChemCrow agent."""

        load_dotenv()
        self.token = token
        """try: 
            self.llm = _make_llm(model, temp, openai_api_key, streaming)
        except ValidationError:
            raise ValueError('Invalid OpenAI API key')
        """ 
        

        
        api_keys['OPENAI_API_KEY'] = openai_api_key
        llm         = _make_llm(model, temp, openai_api_key, callbacks,  stream)
        tools_llm   = _make_llm(model, temp, openai_api_key, callbacks, stream)
        tools = make_tools(
            llm,
            api_keys = api_keys,
            token = self.token,
            nivel = nivel,
            verbose=False
        )
        tools_llm = tools_llm.bind_tools(tools)
  

        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful assistant.\
                    Use the tools provided, using the most specific tool available for each action.\
                    Your final answer should contain all information necessary to answer the question and subquestions.\
                    If not have a good answer, we can list de description tools.\
                    Your answer by default are in spanish language and a good explanation by steps for the actions.\
                    For personal questions no use tools, and only can show the name. If you detect date or you can deduce it from user query, you should write it in the answer with format DD/MM/YYYY.\
                     \
                    If the user question your function, you can describe the tools list. \
                    Only you can use one tool for query. \
                    If no tool works to answer the query, do not use any",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                MessagesPlaceholder(variable_name="context"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"], 
                "context": lambda x: context, 
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                   x["intermediate_steps"]
                ),
            }
            | prompt
            | tools_llm
            | OpenAIToolsAgentOutputParser() 
            #| StrOutputParser()
        )  
        self.agent_executor  = AgentExecutor(agent=agent, tools=tools,  verbose=False, max_iterations=max_iterations )  

    
        
 