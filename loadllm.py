import streamlit as st
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from llama_cpp import Llama

model_path = './models/llama-2-7b-chat.Q4_K_M.gguf'
model_url  = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_0.bin"

os.environ['OPENAI_API_KEY']            = st.secrets["OPENAI_API_KEY"] 
os.environ['HUGGINGFACEHUB_API_TOKEN']  = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
token                                   = st.secrets["TOKEN"]

class Loadllm:
    @staticmethod
    def load_llm():
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        # Prepare the LLM

        """llm = LlamaCpp(
            model_path=model_path,
            n_gpu_layers=40,
            n_batch=512,
            n_ctx=2048,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,
        )"""

        
        #llm = Llama(model_path=model_path)

        #response=llm("Share some cool facts about The Office TV Series.")
        #print(response['choices'][0]['text'])

        llm = ChatOpenAI(
            temperature= 0, 
            model_name= "gpt-3.5-turbo-0125",
            request_timeout=1000,
            #max_tokens=1000,
            streaming=False, #si true excribe mientras encuentra resultados
            #callbacks=[StreamingStdOutCallbackHandler()],
            #callbacks = callbacks,
            openai_api_key = os.environ['OPENAI_API_KEY'] ,
            verbose = False,
            )

        return llm
