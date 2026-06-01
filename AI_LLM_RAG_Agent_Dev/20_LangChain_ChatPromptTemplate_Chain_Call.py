"""
LangChain 链式调用（ChatPromptTemplate | ChatTongyi 模型）示例

本示例对应课件中关于「链式调用」的图片，重点演示：

1. 使用 ChatPromptTemplate 构建提示词模板，并通过 MessagesPlaceholder 注入历史会话
2. 使用「|」运算符把提示词模板和聊天模型链接成一个 chain
3. chain 的类型为 RunnableSerializable，可通过 invoke / stream 触发执行
4. 上一个组件（ChatPromptTemplate）的输出，会作为下一个组件（模型）的输入
"""

import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

chatPromptTemplate =  ChatPromptTemplate.from_messages([
    ("system", "你是一个边塞诗人。"),

    MessagesPlaceholder(variable_name="history"),
    ("human", "请再来一首唐诗"),
])

    # 准备历史会话数据（使用元组格式，与图片中的示例一致）
history_data = [
    ("human", "你来写首诗。"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗， 再来一首"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
]

prompt_template = chatPromptTemplate.invoke({"history": history_data}).to_string()



model = ChatOpenAI(
    model="glm-5",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.lkeap.cloud.tencent.com/plan/v3"
)

#create a chain by linking the prompt template and the model 
# must implement RunnableSerializable interface, so that it can be invoked or streamed
chain = chatPromptTemplate | model


#call by invoke, the output of the previous component (ChatPromptTemplate) will be passed as input to the next component (model)
res = chain.invoke({
    "history": history_data
})
print(res.content)

for chunk in chain.stream({
    "history": history_data
}):
    print(chunk.content, end="")
    
