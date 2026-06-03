import streamlit as st
import time
from knowledge_base import KnowledgeBaseService

st.title("Knowledge Base Update Service")

# 初始化知识库服务
if 'kb_service' not in st.session_state:
    st.session_state.kb_service = KnowledgeBaseService()

# file_uploader
uploader_file = st.file_uploader(
    label="Please upload text file",
    type=['txt'],
    accept_multiple_files=False,
    # False表示仅接受一个文件的上传
)

if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # KB
    
    st.subheader(f"FileName: {file_name}")
    st.write(f"File Format: {file_type} | Size: {file_size:.2f} KB")
    
    # get_value -> bytes -> decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")
    
    # 显示文件内容预览
    with st.expander("File content preview"):
        st.text(text[:1000] + "..." if len(text) > 1000 else text)
    
    # 上传按钮
    if st.button("Upload to knowledge base"):
        # 在spinner内的代码执行过程中,会有一个转圈动画
        with st.spinner("Processing..."):
            time.sleep(1)  # 模拟等待效果
            result = st.session_state.kb_service.upload_by_str(text, file_name)
            st.success(result)