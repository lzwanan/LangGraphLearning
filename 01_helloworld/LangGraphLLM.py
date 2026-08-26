import json
import os
from typing import TypedDict, Annotated, List, Any

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph

"""
LangGraph 简单案例HelloWorld：
构建一个最小的有向图，流程是：START → 模型节点 → END

LangGraph的灵魂：State(状态) + Nodes(节点) + Edges(边) + Graph(图)
"""
load_dotenv()


# 1. 定义状态对象 State
class LLMState(TypedDict):
    # messages 是一个消息列表, Annotated + add_messages 表示, 支持自动追加消息
    messages: Annotated[List, add_messages]


# 2. 定义大模型
llm = init_chat_model(
    model_provider=os.getenv("MODEL_PROVIDER"),
    model=os.getenv("MODEL"),
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 3. 定义节点函数 Node
def model_node(state: LLMState) -> LLMState:
    """ 调用大模型, 并把回复加入到 state['messages'] 中 """
    reply = llm.invoke(state['messages'])  # 输入历史消息, 调用模型
    return {'messages': [reply]}  # 返回新消息, 并自动加入到 State 节点中


# 构建图结构 Graph
graph = StateGraph(LLMState)
graph.add_node('model', model_node)
graph.add_edge(START, 'model')
graph.add_edge('model', END)

# 编译图
app = graph.compile()
result = app.invoke({"messages": "请用一句话解释, 什么是LangGraph"})
print(result)
print("-" * 50)
print(f"模型回答: {result['messages'][-1].content}")  # -1表示从右往左遍历
"""
模型回答: LangGraph 是一个基于图结构的开源库，用于构建有状态、可编排的多步骤 AI 代理工作流。
"""
print("-" * 50)
# 打印可视化
app.get_graph().print_ascii()
"""
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +-------+    
  | model |    
  +-------+    
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
"""
