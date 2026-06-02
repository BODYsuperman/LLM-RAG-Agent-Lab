"""
使用 LangChain 调用聊天模型示例

本示例演示如何使用 LangChain 的进行多轮对话，包括：
- SystemMessage：设置系统角色
- HumanMessage：用户消息
- AIMessage：AI 回复消息
- 流式输出：实时显示模型生成的内容

核心概念：
- Chat：聊天模型，与 Tongyi LLM 不同，专门用于对话场景
- SystemMessage：设置 AI 的角色和行为
- HumanMessage：用户输入的消息
- AIMessage：AI 的回复消息
- stream 方法：流式输出，逐段返回结果

在此基础上，我们做了以下增强：
- 使用 .env / 环境变量中读取 API Key
- 演示多轮对话场景
- 演示流式输出的实时效果
"""
import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def get_model(provider="tencent"):
    if provider == "tencent":
        return ChatOpenAI(
            model="glm-5",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.lkeap.cloud.tencent.com/plan/v3"
        )

    if provider == "ollama":
        return ChatOllama(
            model="llama3.2:1b"
        )

    raise ValueError(f"Unknown provider: {provider}")

chat = get_model("tencent")
chat2 = get_model("ollama") 

messages = [
    SystemMessage(content="你是一名来自边塞的诗人"),

    HumanMessage(content="给我写一首唐诗"),

    AIMessage(
        content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"
    ),

    HumanMessage(
        content="按照上面的格式再写一首"
    )
]

print("\n" + "=" * 50 + "\n")

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)

print("\n" + "=" * 50 + "\n")

for chunk in chat2.stream(messages):
    print(chunk.content, end="", flush=True)

