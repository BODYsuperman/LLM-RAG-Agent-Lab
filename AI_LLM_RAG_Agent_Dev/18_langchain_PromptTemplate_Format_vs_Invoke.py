"""
PromptTemplate / FewShotPromptTemplate 中 format 与 invoke 的对比示例

本示例对应课件图片中的内容，重点演示两件事：

1. PromptTemplate 的两种生成提示词方式：
   - format(...)：纯字符串替换，返回 str
   - invoke({...})：Runnable 标准接口，返回 PromptValue，再通过 .to_string() 得到 str

2. FewShotPromptTemplate 中常用的 invoke(...) 用法：
   - 传入 input 字典，返回 PromptValue，再 .to_string()

并通过一个小表格形式的打印，帮助你理解二者在：
   - 功能
   - 返回值类型
   - 传参方式
   - 支持的占位符
上的差异。
"""

