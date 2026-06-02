from openai import OpenAI
import httpx

client = OpenAI(

    base_url="http://localhost:11434/v1",
    api_key="ollama",
    http_client=httpx.Client(trust_env=False)
)

completion = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[{"role": "user", "content": "你好,你是谁， 可以做什么"}],
    temperature=0.7
)

print(completion.choices[0].message.content)