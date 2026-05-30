from langchain_community.llms.tongyi import Tongyi
from langchain_ollama import ChatOllama

def call_tongyi(prompt: str, model_name: str = "qwen-max"):
    model = Tongyi(model=model_name)
    return model.invoke(prompt).content


def call_ollama(prompt: str, model_name: str = "llama3.2:1b"):
    model = ChatOllama(model=model_name)
    return model.invoke(prompt).content


if __name__ == "__main__":
    prompt = "请介绍一下人工智能的基本概念。"
    print("\n调用通义模型：")
    print(call_tongyi(prompt))
    print("\n调用Ollama模型：")
    print(call_ollama(prompt))

