from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph

"""
图的构建流程：
1、初始化一个StateGraph实例。
2、添加节点。
3、定义边，将所有的节点连接起来。
4、设置特殊节点，入口和出口（可选）。
5、编译图。
6、执行工作流。
"""


# 定义状态 State
class GraphState(TypedDict):
    process_data: dict


# 定义节点 Node
def input_node(state: GraphState) -> GraphState:
    print(f"input_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}


def process_node(state: GraphState) -> GraphState:
    print(f"process_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": {"process": "process_value9527"}}


def output_node(state: GraphState) -> GraphState:
    print(f"output_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": state.get('process_data')}


# 创建图 Graph, 并制定状态
graph = StateGraph(GraphState)

# 添加节点
graph.add_node('input', input_node)
graph.add_node('process', process_node)
graph.add_node('output', output_node)

# 添加边
graph.add_edge(START, 'input')
graph.add_edge('input', 'process')
graph.add_edge('process', 'output')
graph.add_edge('output', END)

app = graph.compile()
result = app.invoke({"process_data": {"name": "测试数据", "value": 123}})
print(f"result: {result}")
"""
input_node节点执行state.get('process_data')方法结果:  {'name': '测试数据', 'value': 123}
process_node节点执行state.get('process_data')方法结果:  {'input': 'input_value'}
output_node节点执行state.get('process_data')方法结果:  {'process': 'process_value9527'}
result: {'process_data': {'process': 'process_value9527'}}
"""
print("-" * 50)

app.get_graph().print_ascii()
"""
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +-------+    
  | input |    
  +-------+    
      *        
      *        
      *        
 +---------+   
 | process |   
 +---------+   
      *        
      *        
      *        
  +--------+   
  | output |   
  +--------+   
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
"""
print("-" * 50)