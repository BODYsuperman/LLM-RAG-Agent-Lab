"""
LangChain TextLoader 和文档分割器示例

本示例对应课件中关于 TextLoader 和 RecursiveCharacterTextSplitter 的内容，重点演示：

1. TextLoader 简介：
   - TextLoader 用于将文本文件加载为 Document 类型对象
   - 支持指定文件编码（默认使用系统编码）
   - 可以加载各种纯文本格式的文件

2. RecursiveCharacterTextSplitter 简介：
   - RecursiveCharacterTextSplitter（递归字符文本分割器）主要用于按自然段落分割大文档
   - 是 LangChain 官方推荐的默认字符分割器
   - 它在保持上下文完整性和控制片段大小之间实现了良好平衡，开箱即用效果佳

3. RecursiveCharacterTextSplitter 参数：
   - chunk_size: 分段的最大字符数
   - chunk_overlap: 分段之间允许重叠的字符数（用于保持上下文连续性）
   - separators: 文本分段依据，按优先级排序的分隔符列表
   - length_function: 字符统计依据（函数），默认使用 len

核心概念：
- TextLoader：用于加载文本文件的文档加载器
- RecursiveCharacterTextSplitter：递归字符文本分割器，用于将大文档分割成小块
- Document：LangChain 文档的统一载体类
- chunk_size：每个文档块的最大字符数
- chunk_overlap：文档块之间的重叠字符数
"""


from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(file_path="./data/Python_Basics.txt", encoding="utf-8")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                          # ensure that the semantic context is continuous between chunks, which is important for maintaining the integrity of the information when processing large documents. The overlap allows for better understanding and retention of the content across chunks.
                                          chunk_overlap=50,
                                          # 文本分段依据，按优先级排序
                                        # 优先使用双换行符分割，然后是单换行符，然后是句号等
                                        separators=["\n\n", "\n", ". ", "! ", "? ", ".", "!", "?", " ", ""],
                                        # 字符统计依据（函数）
                                        length_function=len, ) 
 # 分割文档
split_docs = splitter.split_documents(docs)

print(f"分割后得到 {len(split_docs)} 个文档块\n")
print("前 3 个文档块内容：")
print("-" * 80)
for i, doc in enumerate(split_docs[:3], start=1):
    print(f"\n【文档块 {i}】")
    print(f"长度：{len(doc.page_content)} 个字符")
    print(f"内容：{doc.page_content[:150]}...")
    print(f"元数据：{doc.metadata}")
print()