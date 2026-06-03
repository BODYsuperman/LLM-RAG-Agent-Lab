import os
from datetime import datetime
import config_data as config

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document

from file_history_store import get_history

def print_prompt(prompt_value):

    print("\n" + "=" * 50)
    print("【生成的提示词】")
    print(prompt_value.to_string() if hasattr(prompt_value, 'to_string') else str(prompt_value))
    print("=" * 50)
    return prompt_value  # 必须返回，否则链会断开


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(

            embedding= OllamaEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [

                 ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录,如下:"),
                 MessagesPlaceholder("history"),
                ("user", "请回答用户提问:{input}")
            ]
        )

        self.chat_model = ChatOpenAI(model= config.chat_model_name)

        self.storage_path = config.chat_history_path

        self.chain = self.__getchain()

    def get_conversation_chain(self):
        return self.chain



    def __getchain(self):
        retriever =    self.vector_service.get_retriever() 
        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            # 将检索到的多个文档片段拼接成一个字符串，作为 LLM 的「参考资料上下文」
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            return formatted_str
        
        def format_for_retriever(value: dict)-> str:
            return value["input"]
        
        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]

            return new_value
 
        rag_chain = (
        { 
              "input": RunnablePassthrough(),
              "context": RunnableLambda(format_for_retriever)| retriever | format_document
        }| RunnableLambda(format_for_prompt_template) |
            self.prompt_template
            # | debug_runnable("chain.after_prompt_template")  # ChatPrompt
              | print_prompt                                  # 已有的 prompt 打印
            # | debug_runnable("chain.after_print_prompt")    # 打印后的 prompt（同上）
            | self.chat_model
            # | debug_runnable("chain.after_chat_model")      # LLM 输出（通常是 Message/ChatResult）
            | StrOutputParser()
            # | debug_runnable("chain.after_output_parser")   # 最终字符串输出
        )

        conversation_chain=  RunnableWithMessageHistory(

            rag_chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain
    

if __name__ == '__main__':

    session_config = {
        "configurable":{
            "session_id": "user_001",
        }
    }
    res = RagService().chain.invoke({"input" : "我身高180cm， 尺码推荐"}, session_config)
    print(res)