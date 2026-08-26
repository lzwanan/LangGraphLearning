from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph

"""
LangGraph 图输入输出模式和私有状态传递演示

该演示展示了：
1. 如何定义图的输入和输出模式
"""


# 输入状态
class InputState(TypedDict):
    question: str


# 定义输出状态模式
class OutputState(TypedDict):
    answer: str


# 定义整体状态模式，结合输入和输出
class OverallState(InputState, OutputState):
    pass


# 定义处理节点
def answer_node(state: InputState) -> dict:
    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}

    print(f"  输出: {result}")
    return result


def demo_input_output_schema():
    builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
    builder.add_edge(START, 'answer_node')
    builder.add_node('answer_node', answer_node)
    builder.add_edge('answer_node', END)
    graph = builder.compile()

    result = graph.invoke({"question": "你好"})
    print(f"调用结果: {result}")
    graph.get_graph().print_ascii()

if __name__ == '__main__':
    demo_input_output_schema()
"""
执行 answer_node 节点:
  输入: {'question': '你好'}
  输出: {'answer': '你好', 'question': '你好'}
调用结果: {'answer': '你好'}
 +-----------+   
 | __start__ |   
 +-----------+   
        *        
        *        
        *        
+-------------+  
| answer_node |  
+-------------+  
        *        
        *        
        *        
  +---------+    
  | __end__ |    
  +---------+    

"""