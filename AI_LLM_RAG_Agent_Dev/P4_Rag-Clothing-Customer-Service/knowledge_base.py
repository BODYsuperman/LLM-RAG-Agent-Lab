

import hashlib
import os
from datetime import datetime
import config_data as config

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()

            if line == md5_str:
                return True
            
        return False
        
def save_md5(md5_str: str):

    with open(config.md5_path, 'a' , encoding= "utf-8") as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding = "utf-8"):

    str_bytes = input_str.encode(encoding= encoding)

    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()

    return md5_hex



class KnowledgeBaseService(object):

    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function= OllamaEmbeddings(model= config.embedding_model_name),
            persist_directory= config.persist_directory

        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,
            chunk_overlap = config.chunk_overlap,
            separators= config.separators,
            length_function = len

        )


    def upload_by_str(self, data:str, filename):
        md5_hex = get_string_md5(data)  
        if check_md5(md5_hex):
            return "skip content already exists in knowledge base"
        if(len(data) > config.max_spliter_char_number):
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

            # 构建元数据
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小曹",
        }
        
        # 内容就加载到向量库中了
        # iterable -> list \ tuple
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )
        
        # 保存MD5值
        save_md5(md5_hex)
        return "[成功]内容已经成功载入向量库"

if __name__ == '__main__':
    
    service = KnowledgeBaseService()
    r = service.upload_by_str("ikun", "testfile")
    print(r)
