"""
查看 Chroma 向量存储中的数据
"""

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def get_embeddings():
    return OllamaEmbeddings(model="qwen3-embedding")


# 连接到已存在的 Chroma 数据库
vector_store = Chroma(
    collection_name="knowledge_base",
    embedding_function=get_embeddings(),
    persist_directory="./chroma_db"
)

# 查看集合信息
print("=" * 50)
print("向量存储统计：")
print(f"集合名称: {vector_store._collection.name}")
print(f"文档数量: {vector_store._collection.count()}")

# 查看所有文档
print("\n" + "=" * 50)
print("所有存储的文档：")
results = vector_store.get()

for i, (doc_id, doc_content, metadata) in enumerate(zip(results['ids'], results['documents'], results['metadatas'])):
    print(f"\n--- 文档 {i+1} (ID: {doc_id}) ---")
    print(f"内容: {doc_content[:200]}..." if len(doc_content) > 200 else f"内容: {doc_content}")
    print(f"元数据: {metadata}")

# 执行相似性搜索
print("\n" + "=" * 50)
print("搜索测试：'MySQL'")
search_results = vector_store.similarity_search("MySQL", k=3)
for doc in search_results:
    print("\n-" * 30)
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
