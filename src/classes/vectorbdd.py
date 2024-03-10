from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import  CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

class vectorBddLya2:
    def __init__(self):
        print("ini")

    def createBdd(self, nivel):
        print('createBdd')
        namebdd = "manual_usuario"
        if int(nivel) < 1:
            namebdd = "manual_admin"

        if not os.path.isdir('./vectorBDD_'+nivel):
            print('createBdd start vector_'+nivel)
            if int(nivel) <= 1:
                #loader = PyPDFDirectoryLoader("./data/", extract_images=True)  
                #loader = PyPDFDirectoryLoader("./data/" )  

                #loader = PyPDFLoader("./data/puentes.pdf", extract_images=True)
                #loader = WebBaseLoader("https://dev2.lya2.com/lya2git/index01.php?pag=3000&tabs=2")
                #loader = CSVLoader('./data/imagenes.csv')
                
                loader = JSONLoader(
                    file_path='./data/Solutions.json',
                    jq_schema='.[5].category.folders[1].articles[]', 
                    text_content=False,
                    json_lines=True
                    )
                
                #loader = UnstructuredXMLLoader(    "./data/Solutions.xml")


            else: 
                #loader          = PyPDFLoader("./data/manual_usuario.pdf", extract_images=True)
                loader = JSONLoader(
                    file_path='./data/Solutions.json',
                    jq_schema='.[5].category.folders[0].articles[]', 
                    text_content=False,
                    json_lines=True
                    )

            
            documents       = loader.load()
            print(documents)
            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(documents)

            embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") 

            #db = FAISS.from_documents(docs, embedding_function, persist_directory = persist_directory)
            faiss = FAISS.from_documents(docs, embedding_function)

            faiss.save_local("./vectorBDD_"+nivel, namebdd)
        else:
            print('createBdd exist')
 