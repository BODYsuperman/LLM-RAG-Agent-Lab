"""
LangChain RunnableLambda 自定义函数加入链示例

本示例对应课件中关于 RunnableLambda 的图片，重点演示：

1. RunnableLambda 类的作用：
   - RunnableLambda 是 LangChain 内置的类
   - 将普通函数或 lambda 匿名函数转换为 Runnable 接口实例
   - 方便自定义函数加入 chain，实现更灵活的数据转换

2. 使用 RunnableLambda 的方式：
   - 显式使用：my_func = RunnableLambda(lambda x: {...})
   - 隐式使用：直接在链中使用 lambda 函数，会自动转换为 RunnableLambda

3. 为什么可以直接使用函数：
   - Runnable 接口在实现 `__or__` 方法时，支持 Callable 接口的实例
   - 函数就是 Callable 接口的实例
   - 本质是将函数自动转换为 RunnableLambda

核心概念：
- RunnableLambda：将函数转换为 Runnable 的包装器
- Callable：Python 中的可调用对象接口
- 自定义数据转换：在链中插入自定义的数据处理逻辑
"""



from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

model = ChatOpenAI(model="glm-5")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()
first_prompt = PromptTemplate.from_template(
"我领居姓:{lastname}, 刚生了{gender},请起名,仅告知名字无需其它内容")

my_func = RunnableLambda(lambda ai_msg:{"name": ai_msg.content.strip()})

second_prompt = PromptTemplate.from_template(
"对于姓名{name}, 给出名字的解释说明"
)

chain = first_prompt | model | my_func | second_prompt | model | str_parser

# res = chain.invoke({
#     "lastname": "张",
#     "gender": "男"
# })


for chunk in chain.stream({
    "lastname": "姚", 
    "gender" : "女"
}):
    print(chunk, end="", flush=True)


