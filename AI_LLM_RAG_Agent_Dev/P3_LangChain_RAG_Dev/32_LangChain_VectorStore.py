"""
LangChain 向量存储（Vector Store）使用示例

本示例对应课件中关于向量存储的内容，重点演示：

1. 向量存储简介：
   - 向量存储是典型的 RAG（Retrieval Augmented Generation）流程的核心组件
   - 用于存储文档的嵌入向量，并执行相似性搜索
   - 典型的向量存储应用包括两个阶段：
     * 索引阶段（存储）：文档 -> 嵌入模型 -> 嵌入向量 -> 向量存储
     * 查询阶段（检索）：查询文本 -> 嵌入模型 -> 查询向量 -> 相似性搜索 -> Top-k 结果

2. LangChain 向量存储统一接口：
   - add_documents：存入向量（将文档转换为向量并存储）
   - delete：删除向量（通过指定的 id 删除）
   - similarity_search：向量检索（根据查询文本找到最相似的文档）

3. 向量存储类型：
   - 内置向量存储：InMemoryVectorStore（内存向量存储，适合小规模数据）
   - 外部向量存储：Chroma、FAISS、Milvus 等（持久化存储，适合大规模数据）

核心概念：
- Vector Store：向量存储，用于存储和检索文档向量
- Embedding：嵌入向量，将文本转换为数值向量
- Similarity Search：相似性搜索，根据查询向量找到最相似的文档
- RAG：检索增强生成，结合向量检索和大语言模型的生成能力
"""

import os

from langchain_community.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma


# use local Ollama Embedding
def get_embeddings():
    return OllamaEmbeddings(
        model="qwen3-embedding"
    )


# 加载文档
def load_documents(file_path: str):
    loader = CSVLoader(
        file_path=file_path,
        encoding="utf-8",
        source_column="source"
    )
    return loader.load()


# InMemory Vector Store
def create_inmemory_vectorstore(file_path: str):
    docs = load_documents(file_path)

    vector_store = InMemoryVectorStore(
        embedding=get_embeddings()
    )

    vector_store.add_documents(docs)

    return vector_store


# Chroma Vector Store
def create_chroma_vectorstore(
        file_path: str,
        persist_directory: str = "./chroma_db"
):
    docs = load_documents(file_path)

    vector_store = Chroma(
        collection_name="knowledge_base",
        embedding_function=get_embeddings(),
        persist_directory=persist_directory
    )

    vector_store.add_documents(docs)

    return vector_store


# 测试检索
def search(vector_store, query: str, k: int = 3):
    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    for doc in results:
        print("=" * 50)
        print(doc.page_content)
        print(doc.metadata)


if __name__ == "__main__":

    # 方案1：内存向量库
    # vector_store = create_inmemory_vectorstore(
    #     "./data/info.csv"
    # )

    # 方案2：Chroma持久化向量库
    vector_store = create_chroma_vectorstore(
        "./data/info.csv"
    )

    search(
        vector_store,
        "What is MySQL?"
    )