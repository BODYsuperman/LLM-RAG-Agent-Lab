"""
加载数据到 Chroma 向量库
"""

import os
import config_data as config
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_dir: str = "./data"):
    """加载 data 目录下的所有 txt 文件"""
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    return loader.load()


def split_documents(documents):
    """切分文档"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def load_to_vectorstore():
    """加载数据到向量库"""
    print("1. 加载文档...")
    documents = load_documents()
    print(f"   共加载 {len(documents)} 个文档")

    print("2. 切分文档...")
    chunks = split_documents(documents)
    print(f"   共切分 {len(chunks)} 个片段")

    print("3. 创建向量库...")
    embeddings = OllamaEmbeddings(model=config.embedding_model_name)

    # 如果已存在，先删除
    if os.path.exists(config.persist_directory):
        import shutil
        print(f"   删除旧的向量库: {config.persist_directory}")
        shutil.rmtree(config.persist_directory)

    vector_store = Chroma(
        collection_name=config.collection_name,
        embedding_function=embeddings,
        persist_directory=config.persist_directory
    )

    print("4. 添加文档到向量库...")
    vector_store.add_documents(chunks)
    print(f"   成功添加 {len(chunks)} 个文档片段")

    print("5. 完成！")
    return vector_store


if __name__ == '__main__':
    load_to_vectorstore()
