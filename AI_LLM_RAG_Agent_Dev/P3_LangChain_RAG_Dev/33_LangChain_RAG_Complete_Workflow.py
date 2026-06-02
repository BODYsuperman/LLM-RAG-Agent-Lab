"""
LangChain RAG（检索增强生成）完整流程示例

本示例对应课件中关于 RAG 完整流程的内容，重点演示：

1. RAG 流程概述：
   - RAG（Retrieval-Augmented Generation）是结合向量检索和大语言模型的生成能力
   - 流程：用户提问 -> 向量库检索 -> 构建提示词（用户提问 + 检索到的参考资料）-> LLM 生成回答

2. 核心组件：
   - ChatTongyi：大语言模型，用于生成回答
   - InMemoryVectorStore：向量存储，用于存储和检索文档
   - OllamaEmbeddings：嵌入模型，用于将文本转换为向量
   - ChatPromptTemplate：提示词模板，用于构建包含上下文的提示词
   - StrOutputParser：输出解析器，用于将模型输出解析为字符串

3. 完整流程步骤：
   a. 初始化模型和向量存储
   b. 准备资料（向量库的数据）
   c. 用户提问
   d. 检索向量库（找到与用户提问最相似的文档）
   e. 构建提示词（用户提问 + 检索到的参考资料）
   f. 通过链式调用生成回答

核心概念：
- RAG：检索增强生成，结合向量检索和 LLM 生成
- Vector Store：向量存储，用于存储和检索文档向量
- Similarity Search：相似性搜索，根据查询找到最相似的文档
- Prompt Template：提示词模板，用于构建包含上下文的提示词
- Chain：链式调用，将多个组件串联起来执行
"""
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
    print("【步骤 5】检索与问题相关的知识")
    print("-" * 80)
    print(f"用户问题：{input_text}")
    result = vector_store.similarity_search(input_text, k=2)
    print(f"检索到 {len(result)} 条相关内容：")
    for i, doc in enumerate(result, 1):
        print(f"  {i}. {doc.page_content}")
    print()
    
    # 6. 构建参考文本
    print("【步骤 6】构建参考上下文")
    print("-" * 80)
    reference_text = " ".join([doc.page_content for doc in result])
    print(f"参考资料：{reference_text}\n")
    
    # 7. 构建链并调用
    print("【步骤 7】构建链并调用")
    print("-" * 80)
    print("链结构：prompt | print_prompt | model | StrOutputParser()")
    print()
    
    chain = prompt | print_prompt | model | StrOutputParser()
    res = chain.invoke({"input": input_text, "context": reference_text})
    
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