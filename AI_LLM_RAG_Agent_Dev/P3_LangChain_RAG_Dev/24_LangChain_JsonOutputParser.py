"""
LangChain JsonOutputParser JSON输出解析器示例

本示例对应课件中关于 JsonOutputParser 的图片，重点演示：

1. 问题场景：构建多模型链时的标准处理逻辑
   - 非标准做法：chain = prompt | model | parser | model | parser
     上一个模型的输出没有被处理就输入下一个模型
   - 标准做法：invoke | stream 初始输入 → 提示词模板 → 模型 → 数据处理 → 
     提示词模板 → 模型 → 解析器 → 结果
     上一个模型的输出结果应该作为提示词模板的输入，构建下一个提示词，用来二次调用模型

2. 类型转换需求：
   - 模型的输出为：AIMessage类对象
   - 提示词模板要求输入为：dict类型（如右侧代码所示）
   - 所以需要完成：将模型输出的AIMessage → 转为字典 → 注入第二个提示词模板中，
     形成新的提示词(PromptValue对象)

3. 解决方案：使用 JsonOutputParser
   - StrOutputParser不满足 (AIMessage → Str)
   - 更换JsonOutputParser (AIMessage → Dict(JSON))

核心概念：
- JsonOutputParser：将 AIMessage 转换为字典（JSON格式）的解析器
- 多模型链：第一个模型生成JSON格式输出，第二个模型基于JSON数据进行处理
- 数据处理：在链式调用中，需要将第一个模型的输出转换为第二个提示词模板所需的格式
"""


from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="glm-5")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()
first_prompt = PromptTemplate.from_template(
"我领居姓:{lastname}, 刚生了{gender},请起名,仅告知名字无需其它内容,返回格式是JSON key是name, value是名字    ")

second_prompt = PromptTemplate.from_template(
"对于姓名{name}, 给出名字的解释说明"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

# res = chain.invoke({
#     "lastname": "张",
#     "gender": "男"
# })


for chunk in chain.stream({
    "lastname": "张", 
    "gender" : "男"
}):
    print(chunk, end="", flush=True)

# print(res)
# print(type(res))  # 输出 <class 'str'>，最终结果是字符串类型

