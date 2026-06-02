"""
LangChain 长期会话记忆示例

本示例对应课件中关于长期会话记忆的图片，重点演示：

1. 问题场景：如何实现持久化会话记录
   - InMemoryChatMessageHistory 是临时存储，程序重启后丢失
   - 生产环境需要持久化存储，可以使用文件存储或数据库存储
   - 本示例演示基于文件存储的长期会话记忆实现

2. 核心组件：
   - FileChatMessageHistory：自定义的基于文件存储的会话历史记录类
   - BaseChatMessageHistory：LangChain 提供的基类，需要继承并实现三个方法
   - messages_from_dict / message_to_dict：消息序列化和反序列化工具

3. 实现方法：
   - add_messages：同步模式，添加消息到文件
   - messages：同步模式，从文件读取消息
   - clear：同步模式，清除文件中的消息

核心概念：
- FileChatMessageHistory：基于文件存储的持久化历史记录存储
- BaseChatMessageHistory：会话历史记录的基类
- session_id：会话标识符，用作文件名
- 长期会话记忆：存储在文件中，程序重启后仍然保留
"""

import json
import os
from typing import Any, Dict, Sequence

from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import  ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, directory: str = "chat_history"):
        self.session_id = session_id
        self.directory = directory
        os.makedirs(directory, exist_ok=True)
        self.file_path = os.path.join(directory, f"{session_id}.json")

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        existing_messages = self.messages
        all_messages = existing_messages + list(messages)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([message_to_dict(msg) for msg in all_messages], f, ensure_ascii=False, indent=4)

    @property
    def messages(self) -> Sequence[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            messages_data = json.load(f)
            return messages_from_dict(messages_data)

    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)



model = ChatOpenAI(model="glm-5");

prompt = ChatPromptTemplate.from_messages([
  ("system",
 """
你需要记住用户在历史会话中提供的所有事实信息。

例如：
- 小明有两只猫
- 小刚有两只狗

当用户询问统计、汇总、推理问题时，
请结合全部历史记录进行回答。
 """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "请根据历史会话记录来回答我的问题：{question}")
])

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("历史会话记录：")
    print("="*20, full_prompt.to_string(), "="*20)  
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

store = {}


def get_history(session_id):

    return FileChatMessageHistory(session_id=session_id, directory="./chat_history")



conversation_chain =  RunnableWithMessageHistory(
base_chain,
get_history,
input_messages_key="question",
history_messages_key="chat_history"
)


if __name__ == "__main__":

    
    session_config = {
        "configurable":{
            "session_id": "user_001"
        }
    }

    res = conversation_chain.invoke(
       
        {"question": "小明有两个猫"},
         config= session_config,
    )
    print("第一次执行", res)

    res = conversation_chain.invoke(
        {"question": "小刚有两个狗"},
        config= session_config,
    
    )
    print("第二次执行", res)

    res = conversation_chain.invoke(
        {"question": "总共有几个宠物"},
        config= session_config,
    )
    print("第三次执行", res)
  
    