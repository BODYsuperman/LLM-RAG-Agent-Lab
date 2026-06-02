"""
LangChain Runnable 抽象基类与 __or__ 运算符重写示例

本示例对应课件中关于 Runnable 基类和 __or__ 方法的图片，重点演示：

1. LangChain 中的绝大多数核心组件都继承了 Runnable 抽象基类（位于 langchain_core.runnables.base）
2. 使用「|」运算符（如 chain = prompt | model）时，chain 变量是 RunnableSequence 类型
3. 这是因为 Runnable 基类内部对 __or__ 魔术方法进行了改写
4. 继续使用「|」添加新组件，依旧会得到 RunnableSequence，这就是链的基础架构

核心概念：
- Runnable：LangChain 中所有可运行组件的抽象基类
- RunnableSequence：通过 __or__ 方法创建的序列对象，用于链式调用
- __or__：Python 的位或运算符重写，在 LangChain 中用于组合组件
"""
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


prompt =  PromptTemplate.from_template("你是一个AI助手，回答用户的问题。")
model = ChatOpenAI(model="glm-5" )

chain = prompt | model

print(type(chain))  # 输出 <class 'langchain_core.runnables.base.RunnableSequence'>

