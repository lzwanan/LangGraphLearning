from langgraph.constants import START, END
from langgraph.graph import StateGraph

'''
我们先在不接入大模型的情况下构建一个加减法图工作流，
我们这里自定义两个简单函数：一个是加法函数接收当前State并将其中的x值加1，
另一个是减法函数接收当前State并将其中的x值减2，
然后添加名为addition和subtraction的节点，并关联到两个函数上，最后构建出节点之间的边。
'''


# 定义节点 Node
def addition(state):
    print(f'加法节点收到的初始值:{state}')
    return {"x": state['x'] + 1}


def subtraction(state):
    print(f'减法节点收到的初始值:{state}')
    return {"x": state['x'] - 2}


# 定义图
graph = StateGraph(dict)
graph.add_node('addition', addition)
graph.add_node('subtraction', subtraction)

graph.add_edge(START, 'addition')
graph.add_edge('addition', 'subtraction')
graph.add_edge('addition', END)

# 打印边和节点
print("边: ")
print(graph.edges)
print("节点: ")
print(graph.nodes)
"""
边: 
{('__start__', 'addition'), ('addition', '__end__'), ('addition', 'subtraction')}
节点: 
{'addition': StateNodeSpec(runnable=addition(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class 'dict'>, retry_policy=None, cache_policy=None, is_error_handler=False, error_handler_node=None, ends=(), defer=False, timeout=None, trace_policy=None), 'subtraction': StateNodeSpec(runnable=subtraction(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class 'dict'>, retry_policy=None, cache_policy=None, is_error_handler=False, error_handler_node=None, ends=(), defer=False, timeout=None, trace_policy=None)}
"""
print("=" * 50)

# 编译
app = graph.compile()
result = app.invoke({"x": 5})
print(f"result: {result}")
"""
加法节点收到的初始值:{'x': 5}
减法节点收到的初始值:{'x': 6}
result: {'x': 4}
"""
print("=" * 50)

# 打印图
app.get_graph().print_ascii()
"""
 +-----------+   
 | __start__ |   
 +-----------+   
        *        
        *        
        *        
  +----------+   
  | addition |   
  +----------+   
        *        
        *        
        *        
+-------------+  
| subtraction |  
+-------------+  
        *        
        *        
        *        
  +---------+    
  | __end__ |    
  +---------+    
None
"""
print("=" * 50)
