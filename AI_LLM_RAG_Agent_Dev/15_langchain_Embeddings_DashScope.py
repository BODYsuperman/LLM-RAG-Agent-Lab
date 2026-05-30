"""
LangChain 嵌入模型（Embeddings）调用示例

本示例演示如何在 LangChain 中使用阿里云 DashScope 的嵌入模型：
- 使用 `DashScopeEmbeddings` 创建嵌入模型实例
- 调用 `embed_query()` 对单条文本生成向量
- 调用 `embed_documents()` 对多条文本批量生成向量

核心概念：
- Embedding（向量化）：将一段文本转换成一个浮点数列表（向量），
  使得「相似的文本」在向量空间中的距离更近，用于相似度搜索、向量数据库、RAG 检索等。

ollama pull qwen3-embedding
"""

import os
# from langchain_community.embeddings import DashScopeEmbeddings


# #default model is "text-embeddings-v1"
# model = DashScopeEmbeddings();

from langchain_ollama  import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="qwen3-embedding:latest")

print(embeddings.embed_query("人工智能是什么？"))
print(embeddings.embed_documents(["人工智能是什么？", "今天天气怎么样？"]))