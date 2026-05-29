from openai import OpenAI
import httpx


"""
    金融文本分类任务示例：
    1. 使用 FewShot 方式向模型展示文本分类任务的示例
    2. 对4段金融文本进行分类
    3. 分类类别：['新闻报道','公司公告','财务公告','分析师报告']
"""

client = OpenAI(
    base_url="https://api.lkeap.cloud.tencent.com/plan/v3",
    # api_key="ollama",
    # http_client=httpx.Client(trust_env=False)
) 

# FewShot examples for financial text classification
fewshot_examples = [
        {
            "role": "user",
            "content": "\"今日,股市经历了一轮震荡,受到宏观经济数据和全球贸易紧张局势的影响。投资者密切关注美联储可能的政策调整,以适应市场的不确定性。\"是['新闻报道','公司公告','财务公告','分析师报告']里的什么类别?"
        },
        {
            "role": "assistant",
            "content": "新闻报道"
        },
        {
            "role": "user",
            "content": "\"本公司年度财务报告显示,去年公司实现了稳步增长的盈利,同时资产负债表呈现强劲的状况。经济环境的稳定和管理层的有效战略执行为公司的健康发展奠定了基础。\"是['新闻报道','公司公告','财务公告','分析师报告']里的什么类别?"
        },
        {
            "role": "assistant",
            "content": "财务公告"
        }
    ]


example_types = ['新闻报道','公司公告','财务公告','分析师报告']

# 4. 待分类的文本
texts_to_classify = [
        "今日,央行发布公告宣布降低利率,以刺激经济增长。这一降息举措将影响贷款利率,并在未来几个季度内对金融市场产生影响。",
        "ABC公司今日发布公告称,已成功完成对XYZ公司股权的收购交易。本次交易是ABC公司在扩大业务范围、加强市场竞争力方面的重要举措。据悉,此次收购将进一步巩固ABC公司在行业中的地位,并为未来业务发展提供更广阔的发展空间。详情请见公司官方网站公告栏",
        "公司资产负债表显示,公司偿债能力强劲,现金流充足,为未来投资和扩张提供了坚实的财务基础。",
        "最新的分析报告指出,可再生能源行业预计将在未来几年经历持续增长,投资者应该关注这一领域的投资机会",
        "小明喜欢小新哟"
]


for text in texts_to_classify:
    messages = fewshot_examples + [{"role": "user", "content": f"\"{text}\"是['新闻报道','公司公告','财务公告','分析师报告']，不清楚的分类为'不清楚类别'里的什么类别?"}]
    
    response = client.chat.completions.create(
        model="minimax-m2.5",
        messages=messages,
        temperature=0.0  # 设置温度为0以获得更确定的分类结果
    )   
    
    classification = response.choices[0].message.content.strip()
    print(f"文本: {text}\n分类结果: {classification}\n")