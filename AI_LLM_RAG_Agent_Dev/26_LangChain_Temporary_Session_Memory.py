
"""
LangChain 临时会话记忆示例

本示例对应课件中关于临时会话记忆的图片，重点演示：

1. 问题场景：如何封装历史记录
   - 除了自行维护历史消息外，也可以借助 LangChain 内置的历史记录附加功能
   - LangChain 提供了 History 功能，帮助模型在有历史记忆的情况下回答

2. 核心组件：
   - RunnableWithMessageHistory：在原有链的基础上创建带有历史记录功能的新链
   - InMemoryChatMessageHistory：为历史记录提供内存存储（临时用）
   - get_history 函数：获取指定会话ID的历史会话记录函数

3. 使用方式：
   - 基于 RunnableWithMessageHistory 在原有链的基础上创建带有历史记录功能的新链
   - 基于 InMemoryChatMessageHistory 为历史记录提供内存存储（临时用）
   - 通过 session_id 区分不同的会话，每个会话维护独立的历史记录

核心概念：
- RunnableWithMessageHistory：为链添加历史记录功能的包装器
- InMemoryChatMessageHistory：基于内存的临时历史记录存储
- session_id：会话标识符，用于区分不同的对话会话
- 临时会话记忆：存储在内存中，程序重启后丢失
"""


from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory


model = ChatOpenAI(model="glm-5");

prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据历史会话记录来回答用户的问题。"),
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
    if(session_id not in store):
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]



conversation_chain =  RunnableWithMessageHistory(
base_chain,
get_history,
input_messages_key="question",
history_messages_key="chat_history"
)


if __name__ == "__main__":

    
    session_config = {
        "configurable":{
            "session_id": "123456"
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
  
    