import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma

from utils.config_handler import chroma_conf

from model.factory import embeded_model
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os

from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, text_loader, listed_with_allowed_types, get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection"]["name"],
            embedding_function=embeded_model,
            persist_directory=chroma_conf["persist_directory"]
        )
        self.splitter = RecursiveCharacterTextSplitter(
            
            chunk_size = chroma_conf["processing"]["chunk_size"],
            chunk_overlap = chroma_conf["processing"]["chunk_overlap"],
            separators= chroma_conf["processing"]["separators"],
            length_function = len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["retrieval"]["k"]})

    def load_document(self):

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["storage"]["md5_hex_store"])):
                open(get_abs_path(chroma_conf["storage"]["md5_hex_store"]), "w", encoding="utf-8").close()
                return False

            with  open(get_abs_path(chroma_conf["storage"]["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["storage"]["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")
        
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return text_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []
        
        allowed_file_path = listed_with_allowed_types(
            get_abs_path(chroma_conf["storage"]["data_path"]),
            tuple(chroma_conf["knowledge"]["allow_knowledge_file_type"]),
        )

        for path in allowed_file_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[load knowledge base]{path} is already in knowledge base, skip")
                continue
            
            try:
                documents:list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[load knowledge base]{path} no useful text content, skip")
                    continue
                
                split_document: list[Document] = self.splitter.split_documents(documents)

                if not split_document:
                     logger.warning(f"[load knowledge base]{path} no useful text content after splitting, skip")
                     continue
                    
                self.vector_store.add_documents(split_document)
                
                save_md5_hex(md5_hex)

                logger.info(f"[load knowledge base]{path} content successfully")

            except Exception as e:
                 logger.error(f"[load knowledge base]{path} content failed: {str(e)}", exec_info = True)

# if __name__ == "__main__":
#     # vs = VectorStoreService()

#     # vs.load_document()

#     # retriever = vs.get_retriever()

#     # res = retriever.invoke('lost')

#     # for f in res:
#     #     print(f.page_content)
#     #     print("."*20)