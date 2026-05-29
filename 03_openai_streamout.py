from openai import OpenAI
import httpx

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    http_client=httpx.Client(trust_env=False)
) 

response = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[
              {"role": "system", "content": "你是一个Python专家， 话很多"},
              {"role": "assistant", "content": "好的，我是编程专家，并且话多， 你要问什么"},
              {"role": "user", "content": "你能否介绍一下Python的基本数据类型吗？"}
              ],
              stream=True
             
)   

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content,
               end="", 
             flush=True)   