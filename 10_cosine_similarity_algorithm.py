"""

理解向量和嵌入是掌握向量数据库的第一步。

什么是向量（Vector）
在数学上，向量就是一组有序的数字。

[0.12, -0.54, 0.87, 0.03, ..., 0.61]   ← 这就是一个向量

相似度计算方法
找到"最相似的向量"的核心是计算两个向量的距离或相似度。以下是三种最常用的方法。

余弦相似度（Cosine Similarity）
余弦相似度衡量两个向量的方向角，忽略长度。这是最常用的方法，尤其适合文本场景。

公式：cosine_similarity(A, B) = (A · B) / (|A| · |B|)

结果范围：-1 到 1，值越大越相似
适用场景：文本语义搜索、文档相似度
欧氏距离（Euclidean Distance）
欧氏距离衡量两点之间的直线距离，距离越小越相似。

公式：d(A, B) = sqrt(Σ(A_i - B_i)^2)

结果范围：0 到 ∞，值越小越相似
适用场景：图像检索、地理位置相关应用
点积（Dot Product）
点积是向量相乘求和，结合了方向和长度信息。

公式：A · B = Σ A_i × B_i

适用场景：推荐系统（向量已归一化时等价于余弦相似度）


"""

import numpy as np

# 余弦相似度：衡量方向相似性
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 欧氏距离：衡量绝对位置差异
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

# 点积：结合方向与长度
def dot_product(a, b):
    return np.dot(a, b)

# 示例向量
v1 = np.array([0.12, -0.54, 0.87, 0.03])
v2 = np.array([0.10, -0.50, 0.90, 0.05])
v3 = np.array([-0.80, 0.20, -0.30, 0.70])

print(f"v1 vs v2 余弦相似度: {cosine_similarity(v1, v2):.4f}")  # 约 0.9997（非常相似）
print(f"v1 vs v3 余弦相似度: {cosine_similarity(v1, v3):.4f}")  # 约 -0.3835（不相似）