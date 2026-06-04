"""
LangChain Agent ReAct 行动框架示例（基于通义 ChatTongyi）

本示例对应课件中关于「ReAct 思考-行动-观察」框架的图片代码，重点演示：

1. 如何定义可供 Agent 调用的工具（获取体重 / 身高）
2. 如何在 `system_prompt` 中显式约束 Agent 必须按照「思考 → 行动 → 观察 → 再思考」的流程解决问题
3. 如何结合 `agent.stream(..., stream_mode="values")` 观察 ReAct 框架下的思考过程与工具调用

ReAct 核心概念回顾：
- Thought（思考）：模型用自然语言分析当前信息、规划下一步
- Action（行动）：模型决定调用哪个工具，以及调用参数
- Observation（观察）：接收工具返回结果，并基于结果进行下一轮思考
"""




from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

@tool(description="Get weight, return Integer, unit is kg")
def get_weight() -> int:
    return 90



@tool(description="Get height, return Integer, unit is cm")
def get_height() -> int:
    return 175

agent = create_agent(
    model= ChatOpenAI(model = "glm-5" ),
    tools=[get_weight, get_height],
    system_prompt= """
你是严格遵循 ReAct 框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题：

1. 思考（Thought）：用简短中文说明你当前要解决什么子问题、准备如何做
2. 行动（Action）：如果需要外部信息，只能调用一个合适的工具，并给出工具名称与参数
3. 观察（Observation）：接收工具返回结果，描述你从中得到的关键信息
4. 再思考（Thought）：基于新的信息继续推理，直至得到最终答案

约束要求：
- 每轮最多只能调用 1 个工具，禁止单次调用多个工具
- 在作出最终回答前，至少展示一次完整的「思考→行动→观察→再思考」过程
- 请用清晰的中文解释你在每一步的理由，让用户能看懂你的 ReAct 过程
""")


user_question = "计算我的BMI，并给出是否正常的结论。"
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

