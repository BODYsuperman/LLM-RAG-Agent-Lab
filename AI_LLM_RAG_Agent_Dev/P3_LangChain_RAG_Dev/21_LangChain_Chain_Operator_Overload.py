"""
运算符重写与 LangChain 中「|」链式调用的关系示例

本示例对应课件中关于「chain = chat_prompt_template | model」背后原理的图片，
分为两部分进行讲解：

1. 纯 Python 示例：通过重写 __or__ 方法，让 a | b | c 代码返回一个自定义的「序列对象」
   - a | b 会调用 a.__or__(b)
   - (a | b) | c 会继续调用 MySequence.__or__(c)
   - 自定义类只要实现 __or__，就可以控制「|」运算的行为
2. LangChain 示例：说明 ChatPromptTemplate 和 ChatTongyi 也是通过重写「|」来实现链式调用
   - chat_prompt_template | chat 本质是创建了一个 RunnableSequence（可运行的链）
   - chain.invoke(...) / chain.stream(...) 就是对这个「链对象」发起调用
"""


class Test(object):
    def __init__(self, name):
        self.name = name
    def __or__(self, other):
        print(f"调用了 {self.name}.__or__({other.name})")
        return MySequence([self, other])
    def __str__(self):
        return f"Test({self.name})"
        
class MySequence(object):   
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self, other):
        print(f"调用了 MySequence.__or__({other.name})")
        self.sequence.append(other)
        return self
   
    def run(self):
        print("运行序列：")
        for item in self.sequence:
            print(f" - {item}")
        print("序列运行完毕。")


if __name__ == "__main__":
    a = Test("A")
    b = Test("B")
    c = Test("C")
    
    # 通过重写 __or__，实现 a | b | c 的链式调用
    chain = a | b | c  # 实际上是 (a | b) | c
    print("链式调用完成，准备运行链：")
    chain.run()
    print(type(chain))