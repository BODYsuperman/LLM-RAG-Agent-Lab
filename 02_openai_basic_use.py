from openai import OpenAI
import httpx

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    http_client=httpx.Client(trust_env=False)
) 

completion = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[{"role": "system", "content": "你是一个Python专家， 简单回答问题，不啰嗦"},
              {"role": "assistant", "content": "好的，我是编程专家，并且话不多， 你要问什么"},
              {"role": "user", "content": "你能否介绍一下Python的基本数据类型吗？"}
              ]
)   

print(completion.choices[0].message.content)