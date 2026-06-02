"""
LangChain JSONLoader 文档加载器示例

本示例对应课件中关于 JSONLoader 的内容，重点演示：

1. JSONLoader 简介：
   - JSONLoader 用于将 JSON 数据加载为 Document 类型对象
   - 需要额外安装：pip install jq
   - jq 是跨平台的 JSON 解析工具，LangChain 底层使用 jq 进行 JSON 解析
   - 使用 jq_schema 语法来提取 JSON 中的信息

2. jq_schema 基本语法：
   - `.` 表示整个 JSON 对象（根）
   - `[]` 表示数组
   - `.name` 表示提取 name 字段
   - `.hobby` 表示提取 hobby 数组
   - `.hobby[1]` 或 `.hobby.[1]` 表示提取 hobby 数组的第二个元素
   - `.other.addr` 表示提取嵌套对象 other 中的 addr 字段
   - `.[]` 表示遍历数组中的每个元素
   - `.[].name` 表示提取数组中所有对象的 name 字段

3. JSONLoader 参数：
   - file_path: 文件路径
   - jq_schema: jq schema 语法，用于指定提取规则
   - text_content: 抽取的是否是字符串，默认 True（False 时提取为 Python 对象）
   - json_lines: 是否是 JsonLines 文件（每一行都是 JSON 的文件），默认 False

4. JsonLines 格式：
   - JsonLines 是一种格式，每行都是一个独立的 JSON 对象
   - 适合处理大型数据集，可以逐行读取而不需要一次性加载整个文件

核心概念：
- JSONLoader：用于加载 JSON 文件的文档加载器
- jq_schema：jq 语法，用于从 JSON 中提取特定数据
- JsonLines：每行一个 JSON 对象的文件格式
- Document：LangChain 文档的统一载体类
"""

from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".",
    text_content=False,
    json_lines=True

)
document = loader.load()

print(document)



