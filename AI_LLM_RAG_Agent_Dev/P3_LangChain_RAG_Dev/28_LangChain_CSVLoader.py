
"""
LangChain CSVLoader 文档加载器示例

本示例对应课件中关于文档加载器的内容，重点演示：

1. Document 类：
   - Document 是 LangChain 内文档的统一载体
   - 所有文档加载器最终返回此类的实例
   - 核心属性：page_content（文档内容）和 metadata（文档元数据）

2. 文档加载器接口：
   - load()：一次性加载全部文档
   - lazy_load()：延迟流式传输文档，对大型数据集很有用，避免内存溢出

3. CSVLoader 使用：
   - 基本使用：加载带表头的 CSV 文件
   - 自定义解析：使用 csv_args 参数自定义分隔符、引号字符、字段名等

核心概念：
- Document：LangChain 文档的统一载体类
- CSVLoader：用于加载 CSV 文件的文档加载器
- BaseLoader：所有文档加载器需要实现的基类接口
- load()：同步加载所有文档
- lazy_load()：延迟流式加载文档，返回生成器
"""


import langchain_community.document_loaders as document_loaders


loader = document_loaders.CSVLoader(file_path="./data/stu.csv",
                                     csv_args={
                                         "delimiter": ",",
                                         "quotechar": '"',
                                         "fieldnames": ["name", "age", "gender"]
                                     },

                                     encoding="utf-8"
                                     )


#bacth load
# documents = loader.load()

# through iterator load can prevent memory overflow(OOM) when the data is too large, and can be used in streaming scenarios
doc = loader.lazy_load();

loader.lazy_load()
for doc in documents:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)

    # print(doc)
    print("-" * 50)