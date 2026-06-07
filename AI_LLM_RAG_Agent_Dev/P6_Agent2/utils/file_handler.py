import os
import hashlib
from logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document





def get_file_md5_hex(filepath: str):

    if not os.path.exists(filepath):
        logger.error(f"[md5] file{filepath} doesn't exists")
        return
    
    if not os.path.isfile(filepath):
        logger.error(f"md5] path{filepath} is not a file")

    md5_obj = hashlib.md5()

    #4KB for chunk_size, avoid OOM
    chunk_size = 4096

    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            """
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """

            md5_hex = md5_obj.hexdigest()

            return md5_hex
        
    except Exception as e:
        logger.error(f"Failed to calculate the MD5 hash of the file{filepath} {str(e)}")

        return None

def listed_with_allowed_types(path: str, allowed_tyeps: tuple[str]):

    files = []

    if not os.path.isdir(path):
        logger.error(f"[listed_with_allowed_types] {path} is not a directory")
        return allowed_tyeps
    
    for f in os.listdir(path):
        if f.endswith(allowed_tyeps):
            files.append(os.path.join(path, f))

    return tuple(files)

def pdf_loader(file_path: str, passwd = None)-> list[Document]:
    return PyPDFLoader(file_path, passwd).load()


def text_loader(file_path: str, passwd = None)-> list[Document]:
    return TextLoader(file_path, passwd).load()

            
        
    