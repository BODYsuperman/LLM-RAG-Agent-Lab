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
              {"role": "system", "content": "你是AI助理"},
              {"role": "user", "content": "小明有三只宠物"},
              {"role": "assistant", "content": "好的"},
              {"role": "user", "content": "小祝有10只宠物"},
              {"role": "assistant", "content": "好的"},
               {"role": "user", "content": "小明和小祝一共有多少只宠物？"},
              ],
              stream=True
             
)   

print("🤖 AI: ", end="", flush=True)
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行