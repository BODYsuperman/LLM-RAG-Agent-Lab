"""
FewShot 提示词模板（FewShotPromptTemplate）用法示例

本示例演示如何使用 LangChain 的 FewShotPromptTemplate 来构建少样本学习（Few-Shot Learning）提示词。

FewShotPromptTemplate 的核心参数：
- examples: 示例数据，list，内套字典（每个字典代表一个示例）
- example_prompt: 示例数据的提示词模板（PromptTemplate），用于格式化每个示例
- prefix: 组装提示词，示例数据前的内容
- suffix: 组装提示词，示例数据后的内容（通常包含用户输入变量）
- input_variables: 列表，注入的变量列表（在 suffix 中使用的变量）

工作流程：
1. 使用 example_prompt 格式化 examples 中的每个示例
2. 将 prefix + 格式化后的示例 + suffix 组合成最终提示词
3. 将 input_variables 中的变量注入到 suffix 中

本示例包含两个演示：
1. 反义词示例：根据给定的示例，让模型推断新词的反义词
2. 情感分析示例：根据给定的示例，让模型分析文本的情感倾向
"""

"""
演示 FewShotPromptTemplate 在反义词推断任务中的应用。

通过提供几个「词-反义词」的示例，让模型学习模式并推断新词的反义词。
"""

import os
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate


print("=" * 80)
print("【示例1】反义词推断：FewShot 提示词模板")
print("-" * 80)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="glm-5",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.lkeap.cloud.tencent.com/plan/v3"
)



# Step 1: 定义示例数据的模板
# 这个模板用于格式化每个示例，将示例数据中的 word 和 antonym 填入
example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")

# Step 2: 准备示例数据（list，内套字典）
# 每个字典包含一个示例的 word 和 antonym
example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
]

# Step 3: 创建 FewShotPromptTemplate
# - example_prompt: 用于格式化每个示例的模板
# - examples: 示例数据列表
# - prefix: 示例数据前的内容（说明任务和提供示例）
# - suffix: 示例数据后的内容（包含用户输入变量）
# - input_variables: 在 suffix 中使用的变量列表
few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="给出给定词的反义词,有如下示例:",
    suffix="基于示例告诉我:{input_word1}和{input_word2}的反义词是?",
    input_variables=["input_word1", "input_word2"],
)

# Step 4: 使用 FewShotPromptTemplate 生成最终提示词
# 方法1：使用 invoke 方法（推荐，返回 PromptValue 对象）
prompt_value = few_shot_prompt.invoke(input={"input_word1": "高大", "input_word2": "娴熟"})
prompt_text = prompt_value.to_string()

print("生成的 FewShot 提示词：\n")
print(prompt_text)
print("\n模型回复：\n")

# Step 5: 将生成的提示词发送给模型
res = llm.invoke(prompt_text)
print(res.content)
print()