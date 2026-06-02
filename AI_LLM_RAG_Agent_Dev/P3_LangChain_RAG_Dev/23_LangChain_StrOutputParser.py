"""
LangChain StrOutputParser 字符串输出解析器示例

本示例对应课件中关于 StrOutputParser 的图片，重点演示：

1. 问题场景：当尝试构建 `chain = prompt | model | model` 时，会遇到类型不匹配错误
   - prompt 的输出是 PromptValue 类型
   - model 的输出是 AIMessage 类型
   - 第二个 model 的 invoke 方法期望的输入类型是 LanguageModelInput
     (即 PromptValue | str | Sequence[MessageLikeRepresentation])
   - 但实际接收到的是 AIMessage 类型，导致 ValueError

2. 解决方案：使用 StrOutputParser 进行类型转换
   - StrOutputParser 是 LangChain 内置的简单字符串解析器
   - 可以将 AIMessage 解析为简单的字符串
   - 是 Runnable 接口的子类，可以加入链
   - 正确的链式写法：`chain = prompt | model | parser | model`

3. 实际应用场景：当需要将第一个模型的输出作为第二个模型的输入时

核心概念：
- StrOutputParser：将 AIMessage 转换为字符串的解析器
- LanguageModelInput：模型输入的类型约束
- 类型转换：在链式调用中处理不同组件之间的类型不匹配问题
"""

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


parser = StrOutputParser()
model = ChatOpenAI(model="glm-5")

prompt = PromptTemplate.from_template(
        "我邻居姓:{lastname}, 刚生了{gender},请起名,仅告知名字无需其它内容"
    )



chain = prompt | model | parser | model

res: AIMessage = chain.invoke({
    "lastname": "张",
    "gender": "男"
})

print(res.content)
