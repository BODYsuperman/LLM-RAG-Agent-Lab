"""
LangChain PyPDFLoader 文档加载器示例

本示例对应课件中关于 PyPDFLoader 的内容，重点演示：

1. PyPDFLoader 简介：
   - LangChain 内支持许多 PDF 的加载器，我们选择其中的 PyPDFLoader 使用
   - PyPDFLoader 依赖 PyPDF 库，需要安装：pip install pypdf
   - PyPDFLoader 使用简单，可以快速加载 PDF 中的文字内容

2. PyPDFLoader 参数：
   - file_path: 文件路径（必填）
   - mode: 读取模式，可选 'page'（按页面划分不同 Document）和 'single'（单个 Document）
   - password: 文件密码（可选，用于加密的 PDF 文件）

3. mode 参数说明：
   - 'page': 按页面划分，每个页面生成一个独立的 Document 对象
   - 'single': 将整个 PDF 作为一个 Document 对象

核心概念：
- PyPDFLoader：用于加载 PDF 文件的文档加载器
- Document：LangChain 文档的统一载体类
- mode：文档加载模式，控制如何将 PDF 内容分割为 Document 对象
"""

from langchain_community.document_loaders import PyPDFLoader

loader =  PyPDFLoader(file_path="./data/sample.pdf", 
                      password=None,
                       # "single"
                      mode="page" )


i = 0

for doc in loader.load():
    i += 1
    print(f"【Document {i}】")
    print(f"Content: {doc.page_content[:200]}...")
    print(f"Metadata: {doc.metadata}")
    print("-" * 80)
