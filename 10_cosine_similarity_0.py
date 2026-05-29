



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
"""

def get_dot(vec_a, vec_b):
    if(len(vec_a) != len(vec_b)):
        raise ValueError("Vectors must be of the same length")
    return sum(a * b for a, b in zip(vec_a, vec_b))

def get_norm(vec):
    return sum(x ** 2 for x in vec) ** 0.5


def cosine_similarity(vec_a, vec_b):    
    dot_product = get_dot(vec_a, vec_b)
    norm_a = get_norm(vec_a)
    norm_b = get_norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0  # 避免除以零的情况
    
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    vec1 = [0.12, -0.54, 0.87, 0.03]
    vec2 = [0.10, -0.50, 0.90, 0.05]
    vec3 = [-0.80, 0.20, -0.30, 0.70]

    print(f"vec1 vs vec2 余弦相似度: {cosine_similarity(vec1, vec2):.4f}")  # 约 0.9997（非常相似）
    print(f"vec1 vs vec3 余弦相似度: {cosine_similarity(vec1, vec3):.4f}")  # 约 -0.3835（不相似）