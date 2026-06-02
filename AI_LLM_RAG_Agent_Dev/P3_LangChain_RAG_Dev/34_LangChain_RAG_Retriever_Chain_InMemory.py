"""
LangChain RAG：向量检索如何加入链（InMemoryVectorStore 版本）

本示例在 33_LangChain_RAG_Complete_Workflow 的基础上，重点演示：

1. retriever（检索器）概念：
   - 基于向量存储（Vector Store）封装出来的「检索组件」
   - 通过 vector_store.as_retriever() 得到
   - 输入：用户查询文本；输出：与查询最相似的文档列表（List[Document])

2. 向量检索加入链（Chain）的典型方式：
   - 使用 Runnable 组合：{"context": retriever | format_docs, "input": RunnablePassthrough()}
   - 将「检索」作为链中的一个步骤，而不是在链外手动调用 similarity_search
   - 整体链结构：输入问题 -> 检索器 -> 格式化文档 -> PromptTemplate -> ChatModel -> StrOutputParser

3. 本示例使用的组件：
   - OpenAI：大语言模型，用于生成回答
   - InMemoryVectorStore：内存向量存储，适合小规模 demo
   - OllamaEmbeddings：嵌入模型，将文本转换为向量
   - ChatPromptTemplate：提示词模板，将 context 和 input 组合成提示词
   - Runnable 系列（RunnablePassthrough 等）：用来把「检索」和「LLM 调用」串成一条链
   - StrOutputParser：输出解析器，将模型输出解析为字符串

对比 33 号脚本：
------------------------------------
- 33 号脚本：检索（similarity_search）在链外手动调用，然后把结果拼成 reference_text 传给链
- 本脚本：检索通过 retriever.as_retriever() 直接成为链中的一个步骤，链从「问题」自动走到「最终回答」
"""
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore  # 修正导入
from langchain_openai import ChatOpenAI


def init_chat_model() -> ChatOpenAI:
    return ChatOpenAI(model="glm-5")


def init_vector_store() -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore(
        embedding=OllamaEmbeddings(model="qwen3-embedding")
    )
    return vector_store


def print_prompt(prompt_value):
    """打印提示词内容（调试用）"""
    print("\n" + "=" * 50)
    print("【生成的提示词】")
    print(prompt_value.to_string() if hasattr(prompt_value, 'to_string') else str(prompt_value))
    print("=" * 50)
    return prompt_value  # 必须返回，否则链会断开


def format_func(docs: list[Document]):
    if not docs:
        return "No references"
    formated_str = "["
    for doc in docs:
        formated_str += doc.page_content
    formated_str += "]"
    return formated_str

def rag_complete_workflow_demo(input_text: str) -> str:
    """RAG 完整工作流演示"""
    
    # 1. 初始化模型和向量存储
    print("【步骤 1】初始化模型和向量存储")
    print("-" * 80)
    model = init_chat_model()
    vector_store = init_vector_store()
    print("✅ 初始化完成\n")
    
    # 2. 准备提示词模板
    print("【步骤 2】准备提示词模板")
    print("-" * 80)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是一个专业的健康顾问。请以我提供的已知参考资料为主，简洁和专业的回答用户问题。\n\n参考资料：{context}",
        ),
        ("user", "用户提问：{input}"),
    ])
    print("✅ 提示词模板创建完成\n")
    
    # 3. 准备知识库资料
    print("【步骤 3】准备知识库资料")
    print("-" * 80)
    knowledge_texts = [
        "减肥就是要少吃多练，控制总热量摄入。",
        "在减脂期间饮食很重要，建议清淡少油，控制卡路里摄入并坚持运动。",
        "跑步是很好的有氧运动，每周坚持3-5次，每次30分钟以上效果更佳。",
        "减肥期间保证充足睡眠也很重要，睡眠不足会影响新陈代谢。",
    ]
    print(f"知识库内容：{knowledge_texts}\n")
    
    # 4. 将文本添加到向量存储
    print("【步骤 4】添加文本到向量存储")
    print("-" * 80)
    vector_store.add_texts(knowledge_texts)
    print(f"✅ 已添加 {len(knowledge_texts)} 条知识到向量库\n")
    
    # 5. 检索相似内容
   
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # 6. 构建参考文本
    # print("【步骤 6】构建参考上下文")
    # print("-" * 80)
    # reference_text = " ".join([doc.page_content for doc in result])
    # print(f"参考资料：{reference_text}\n")
    
    # 7. 构建链并调用
    print("【步骤 7】构建链并调用")
    print("-" * 80)
    print("链结构：prompt | print_prompt | model | StrOutputParser()")
    print()
    
    chain = (
{ "input": RunnablePassthrough(), "context": retriever 
                | format_func} 
                | prompt 
                | print_prompt 
                |  model | StrOutputParser() )

    res = chain.invoke(input_text)
    
    return res


if __name__ == "__main__":
    input_text = "减肥期间应该注意什么？"
    print("\n" + "🚀" * 20)
    print("开始 RAG 完整工作流演示")
    print("🚀" * 20 + "\n")
    
    answer = rag_complete_workflow_demo(input_text)
    
    print("\n" + "=" * 80)
    print("【最终回答】")
    print("=" * 80)
    print(answer)