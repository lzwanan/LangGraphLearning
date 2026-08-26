from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# 1. 定义状态 State
class HelloState(TypedDict):
    name: str
    greeting: str


# 2. 定义节点 Node
def greet(hello_state: HelloState) -> dict:
    name = hello_state['name']
    return {"greeting": f"Hello, {name}!"}


def add_emoji(hello_state: HelloState) -> dict:
    greeting = hello_state['greeting']
    return {"greeting": greeting + ".... 🙂"}


# 3. 构建图 Graph
graph = StateGraph(HelloState)

# 点
graph.add_node("greet", greet)
graph.add_node("add_emoji", add_emoji)

# 点构成线
graph.add_edge(START, "greet")
graph.add_edge("greet", "add_emoji")
graph.add_edge("add_emoji", END)

# 4. 编译图
app = graph.compile()

# 5. 运行
result = app.invoke({"name": "lz"})
print(result)
"""
{'name': 'lz', 'greeting': 'Hello, lz!.... 🙂'}
"""

print(result['greeting'])
"""
Hello, lz!.... 🙂
"""