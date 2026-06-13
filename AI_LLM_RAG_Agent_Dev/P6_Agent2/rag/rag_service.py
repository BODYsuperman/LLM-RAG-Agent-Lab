
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document

from langchain_core.output_parsers import StrOutputParser

from vector_store import VectorStoreService

from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model




def print_prompt(prompt_value):

    print("\n" + "=" * 50)
    print("【生成的提示词】")
    print(prompt_value.to_string() if hasattr(prompt_value, 'to_string') else str(prompt_value))
    print("=" * 50)
    return prompt_value  # 必须返回，否则链会断开


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | print_prompt|  self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str)->list[Document]:
        return self.retriever.invoke(query)
    
    def rag_summarize(self, query: str)-> str:

        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[reference material {counter}]: {doc.page_content} | metadata: {doc.metadata}\n"

        return self.chain.invoke(
            {

                "input":query,
                "context": context
            }
        )

if __name__ == "__main__":
    rag = RagSummarizeService()

    rag.rag_summarize("小户型适合哪些扫地机器人？")