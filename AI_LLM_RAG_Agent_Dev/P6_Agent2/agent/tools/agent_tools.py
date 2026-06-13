import csv
import random
import threading
from typing import Any, Dict

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService


rag = RagSummarizeService()


# 模拟数据：实际场景可由会话/登录态提供
USER_IDS = [
    "1001", "1002", "1003", "1004", "1005",
    "1006", "1007", "1008", "1009", "1010",
]
MONTH_ARR = [
    "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
]

external_data = []

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return _get_rag_service().rag_summarize(query)


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(USER_IDS)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(MONTH_ARR)


def get