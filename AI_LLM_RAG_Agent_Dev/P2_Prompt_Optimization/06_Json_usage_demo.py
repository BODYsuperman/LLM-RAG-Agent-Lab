"""

JavaScript Object Notation (JSON) 是一种轻量级的数据交换格式，易于人阅读和编写，同时也易于机器解析和生成。在AI工程中，JSON常用于数据存储、配置文件、API通信等场景。以下是一些JSON使用的示例：

1. 数据存储：将AI模型的训练数据、参数或结果以JSON格式保存，方便后续加载和分析。
2. 配置文件：使用JSON格式编写AI系统的配置文件，如模型参数、训练设置等，便于管理和修改。
3. API通信：在AI系统与外部服务（如数据库、其他API）进行通信时，使用JSON格式传递数据，确保数据结构清晰且易于解析。

"""
import json

# 示例数据
data = {
    "name": "小明",
    "age": 18,
    "pets": ["猫", "狗", "兔子"]
}

# 将数据转换为JSON字符串 用dumps()函数将Python对象转换为JSON字符串
json_string = json.dumps(data, ensure_ascii=False)
print("JSON字符串：", json_string, type(json_string))

# 将JSON字符串转换回Python对象 用loads()函数读取JSON字符串
python_obj = json.loads(json_string)
print("Python对象：", python_obj, type(python_obj))
