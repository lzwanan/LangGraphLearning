import uuid
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

# 6. 打印图的边和节点信息
# 打印图的ascii可视化结构   pip install grandalf
print(app.get_graph().print_ascii())
print("=" * 10)
"""
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +-------+    
  | greet |    
  +-------+    
      *        
      *        
      *        
+-----------+  
| add_emoji |  
+-----------+  
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
None
"""

# 打印mermaid代码
print(app.get_graph().draw_mermaid())
print("=" * 10)
"""
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	greet(greet)
	add_emoji(add_emoji)
	__end__([<p>__end__</p>]):::last
	__start__ --> greet;
	greet --> add_emoji;
	add_emoji --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# 生成.png并写入文件
png_bytes = app.get_graph().draw_mermaid_png(max_retries=2, retry_delay=2.0)
output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
with open(output_path, "wb") as f:
    f.write(png_bytes)
print(f"图片已生成: {output_path}")