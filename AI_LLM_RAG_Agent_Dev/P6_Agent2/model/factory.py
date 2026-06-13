from abc import ABC, abstractmethod
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from utils.config_handler import rag_conf


class BaseModelFactory(ABC):

    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatOpenAI(model=rag_conf["chat_model_name"])

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return OllamaEmbeddings(model=rag_conf["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embeded_model = EmbeddingsFactory().generator()
