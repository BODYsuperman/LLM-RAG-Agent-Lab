
import config_data as config

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class VectorStoreService(object):

    def __init__(self, embedding):
        self.embedding = embedding
        self.vector_store = Chroma(

            collection_name= config.collection_name,
            embedding_function= self.embedding,
            persist_directory= config.persist_directory
        )
    
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {"k": config.similarity_threshold})
    

if __name__ == '__main__':
    retriever =  VectorStoreService(OllamaEmbeddings(model= config.embedding_model_name)).get_retriever()

    res =  retriever.invoke("体重是 180斤, 推荐下尺码 ")
    print(res)
