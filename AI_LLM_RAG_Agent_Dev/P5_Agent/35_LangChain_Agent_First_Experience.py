"""
LangChain Agent 智能体初体验示例（基于通义 ChatTongyi）

本示例对应课件中关于「Agent 智能体」的图片，重点演示：

1. 如何使用 LangChain 定义一个最简单的工具（查询天气）
2. 如何将聊天模型（ChatTongyi）和工具组合成一个 Agent 智能体
3. 如何向 Agent 发送用户消息，并打印出 Agent 返回的消息列表
4. 如何配合 StrOutputParser，将消息对象统一解析为字符串输出

核心概念：
- 工具（Tool）：Agent 可以调用的函数能力，例如：查天气、查数据库、调用 API 等
- Agent：拥有「规划 + 调用工具 + 记忆」能力的智能体，本质上是对大模型的封装
- system_prompt：系统提示词，用来规定 Agent 的角色和行为规范
- messages：对话消息列表（role + content），与前面消息示例保持一致

为了让你快速“上手有感觉”，本示例刻意保持简单：
- 只定义 1 个工具：`get_weather`，永远返回“晴天”
- 不引入复杂的记忆、规划逻辑，只展示最基本的调用链路
- 重点放在：看懂 Agent 的输入 / 输出结构
"""

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

@tool(description="lookup weather")
def get_weather() -> str:
    return "Sunny"

agent = create_agent(
    model= ChatOpenAI(model = "glm-5" ),
    tools=[get_weather],
    system_prompt= "You are a chat assistant that can answer users' questions and call up a weather lookup tool when needed.",
)


res = agent.invoke({
    "messages":[
        {"role":"user", "content": "How is weather like in NewYork tomorrow"}
    ]
})


print(res)

for msg in res["messages"]:
    print(type(msg).__name__, msg.content)
