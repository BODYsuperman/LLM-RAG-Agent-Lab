"""
通用提示词模板（PromptTemplate）用法示例

本示例对应课件中的两段代码：

1）标准写法（先生成提示词文本，再喂给模型）：

from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，帮忙起名字，请简略回答。"
)

prompt_text = prompt_template.format(lastname="张", gender="女儿")
model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)

2）基于 chain 的写法（把 PromptTemplate 和 模型 链起来）：

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，帮忙起名字，请简略回答。"
)

model = Tongyi(model="qwen-max")
chain = prompt_template | model
res = chain.invoke(input={"lastname": "曹", "gender": "女儿"})

在此基础上，我们封装成可直接运行的脚本，并增加了说明性输出，便于学习。
"""

import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    """
你是一位经验丰富的中文起名顾问。

我的邻居姓{lastname}，
刚生了{gender}。

请给出3个名字。
"""
)

llm = ChatOpenAI(
    model="glm-5",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.lkeap.cloud.tencent.com/plan/v3"
)

chain = prompt | llm

res = chain.invoke({
    "lastname": "王",
    "gender": "儿子"
})

print(res.content)
