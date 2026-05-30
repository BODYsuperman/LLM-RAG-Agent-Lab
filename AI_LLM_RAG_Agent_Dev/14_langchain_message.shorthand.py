"""
LangChain 消息简写形式示例

本示例演示 LangChain 中消息定义的两种方式：
1. 标准格式：使用 SystemMessage、HumanMessage、AIMessage 对象
2. 简写格式：使用 2 元组 (role, content) 的形式

核心概念：
- 标准格式：显式使用消息类，类型安全，代码清晰
- 简写格式：使用元组，代码更简洁，但需要手动指定角色字符串
- 两种格式在功能上完全等价，LangChain 会自动转换

优缺点对比：
标准格式优点：
- 类型安全，IDE 可以提供更好的代码补全和类型检查
- 代码可读性强，一眼就能看出消息类型
- 支持更多高级功能（如消息元数据、工具调用等）
- 因为是是动态转换所以简写支持{}内部填充变量，可运行时填充模版提示词
标准格式缺点：
- 代码相对冗长，需要导入多个类
- 对于简单场景可能显得过于正式

简写格式优点：
- 代码简洁，减少导入和类名
- 适合快速原型开发和简单场景
- 消息列表更紧凑，易于阅读

简写格式缺点：
- 类型安全性较差，字符串拼写错误不会在编译时发现
- IDE 支持较弱，缺少代码补全
- 不支持消息的高级属性（如 name、tool_calls 等）
"""

import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

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

    ("system", "你是一名来自边塞的诗人"),
    ("human", "给我写一首唐诗"),

    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),

    ("human", "按照上面的格式再写一首")
]


print("\n" + "=" * 50 + "\n")

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)

print("\n" + "=" * 50 + "\n")

for chunk in chat2.stream(messages):
    print(chunk.content, end="", flush=True)


