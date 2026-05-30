import os

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


def get_minmax():
    return ChatOpenAI(
        model="glm-5",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.lkeap.cloud.tencent.com/plan/v3"
    )


def get_ollama():
    return ChatOllama(
        model="llama3.2:1b"
    )


def stream_chat(llm, prompt):
    for chunk in llm.stream(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)


stream_chat(get_minmax(), "介绍一下杭州")

print("\n" + "=" * 50 + "\n")

stream_chat(get_ollama(), "介绍一下杭州")