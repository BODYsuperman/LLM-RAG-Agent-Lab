"""
    信息抽取任务 - Few-Shot 学习示例：
    1. 使用 Few-Shot 方式让模型理解信息抽取任务
    2. 从金融文本中提取：日期、股票名称、开盘价、收盘价、成交量
    3. 按照 JSON 格式输出，缺失信息用 '原文未提及' 表示
"""
from openai import OpenAI
import httpx
import json

client = OpenAI(
    base_url="https://api.lkeap.cloud.tencent.com/plan/v3",
    # api_key="ollama",
    # http_client=httpx.Client(trust_env=False)
) 

# 3. 定义需要抽取的信息字段（Schema）
schema = ['日期', '股票名称', '开盘价', '收盘价', '成交量']
    
# 4.定义示例数据（Few-Shot 示例）
examples_data = [
        {
            "content": "2023-01-10,股市震荡。股票强大科技A股今日开盘价100人民币,一度飙升至105人民币,随后回落至98人民币,最终以102人民币收盘,成交量达到520000。",
            "answers": {
                "日期": "2023-01-10",
                "股票名称": "强大科技A股",
                "开盘价": "100人民币",
                "收盘价": "102人民币",
                "成交量": "520000"
            }
        },
        {
            "content": "2024-05-16,股市波动。股票英伟达美股今日开盘价105美元,一度飙升至109美元,随后回落至100美元,最终以116美元收盘,成交量达到3560000。",
            "answers": {
                "日期": "2024-05-16",
                "股票名称": "英伟达美股",
                "开盘价": "105美元",
                "收盘价": "116美元",
                "成交量": "3560000"
            }
        },
           {
        "content": "2024-05-16,股票测试B股今日开盘价50人民币,收盘价55人民币。（注意：这句话里没有说成交量）",
        "answers": {
            "日期": "2024-05-16",
            "股票名称": "测试B股",
            "开盘价": "50人民币",
            "收盘价": "55人民币",
            "成交量": "原文未提及"
        }
    }
    ]
# 5. 定义需要抽取信息的问题列表
questions = [
        "2025-06-16,股市震荡。股票传智教育A股今日开盘价66人民币,一度飙升至70人民币,随后回落至65人民币,最终以68人民币收盘,成交量达到123000。",
        "2025-06-06,股市波动。股票黑马程序员A股今日开盘价200人民币,一度飙升至211人民币,随后回落至201人民币,最终以206人民币收盘。"
        ]
    
# 6. 构建消息列表
messages = []

messages.append({
        "role": "system",
        "content": f"你帮我完成信息抽取,我给你句子,你抽取{schema}信息,按JSON字符串输出,如果某些信息不存在,用'原文未提及'来表示,参考下面的示例。"
    })



for example in examples_data:
     # 添加用户输入（待抽取的句子）
    messages.append({
        "role": "user",
        "content": example["content"]
    })
     # 添加助手回复（期望的抽取结果）
    messages.append({
        "role": "assistant",
        "content": json.dumps(example["answers"], ensure_ascii=False)
    })

for question in questions:
    response = client.chat.completions.create(
        model="minimax-m2.5",
        messages=messages + [{"role": "user", "content": f"按照上述的例子，现在抽取这个句子的信息{question}"}]
    )
    print("🤖 AI: ", response.choices[0].message.content)
