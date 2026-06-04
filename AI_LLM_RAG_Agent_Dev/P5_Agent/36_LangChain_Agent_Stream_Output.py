"""
LangChain Agent 智能体流式输出示例（基于通义 ChatTongyi）

本示例对应课件中关于「Agent.stream 流式输出」的图片代码，重点演示：

1. 如何创建一个可以调用工具（查询股票信息）的 Agent 智能体
2. 如何使用 `agent.stream(..., stream_mode="values")` 持续接收增量消息
3. 如何从每个 `chunk` 中取出最新一条消息，并根据是「普通回复」还是「工具调用」做不同处理

核心概念回顾：
- invoke / 调用：一次性得到完整结果（上一节 `35_LangChain_Agent_First_Experience.py` 已演示）
- stream / 流式：连续收到多个结果块（chunk），可以一边生成、一边展示
- stream_mode="values"：每个 chunk 都是一个「完整状态快照」，其中 `messages` 字段包含当前为止的所有消息
"""


from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

@tool(description="Get stock price: Enter a stock name to return a string of information")
def get_price(name: str) -> str:
    return f"stock {name} price is 200$"



@tool(description="Get stock info: Enter a stock name to return a string of information")
def get_info(name: str) -> str:
    return f"stock {name} is a is a publicly traded company"


agent = create_agent(
    model= ChatOpenAI(model = "glm-5" ),
    tools=[get_price, get_info],
    system_prompt= """You are an AI assistant capable of answering questions related to stocks.
             When you need to look up stock prices or company profiles, please use the appropriate tools as needed.
             When formulating your response or using tools, please briefly explain your reasoning in simple Chinese."""
        )


user_question = "What's the stock price of Tesla, please introduce a little bit？"
for chunk in  agent.stream(
        input={
            "messages": [
                {"role": "user", "content": user_question},
            ]
        },
        stream_mode="values",
    ):
    latest_message = chunk['messages'][-1]

    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content) 

    try:
        if latest_message.tool_calls:
            print( f"tool calls: { [tc['name'] for tc in latest_message.tool_calls] }")  
    except AttributeError as e:
        pass

