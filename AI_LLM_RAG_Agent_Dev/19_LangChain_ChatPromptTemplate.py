"""
LangChain 聊天提示词模板（ChatPromptTemplate）示例

本示例演示如何使用 ChatPromptTemplate 和 MessagesPlaceholder 来动态注入历史会话信息。

核心概念：
- 历史会话信息并不是静态的（固定的），而是随着对话的进行不停地积攒，即动态的
- 所以，历史会话信息需要支持动态注入
- MessagesPlaceholder 作为占位符，提供 history 作为占位的 key
- 基于 invoke 动态注入历史会话记录
- 必须是 invoke，format 无法注入

关键点：
1. ChatPromptTemplate：用于构建聊天提示词模板
2. MessagesPlaceholder：用于占位历史会话消息列表
3. invoke 方法：动态注入历史会话记录（format 方法不支持）
4. 历史会话数据：使用元组格式 (role, content) 或消息对象格式
"""



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



llm = ChatOpenAI(
    model="glm-5",
   
)

chain = chatPromptTemplate | llm

res = chain.invoke({
    "history": history_data
})

print(res.content)

# prompt_value = chatPromptTemplate.invoke(
#     {"history": history_data}
# )

# res = llm.invoke(prompt_value.messages)

# print(res.content)