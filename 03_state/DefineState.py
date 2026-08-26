from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class BasicState(TypedDict):
    """ 基本状态定义 """
    user_input: str
    response: str
    count: int
    process_data: dict


# 创建图
graph = StateGraph(BasicState)
graph.add_edge(START, END)

# 编译生成图
app = graph.compile()

initial_state = {
    "user_input": "test",
    "response": "test",
    "count": 1,
    "process_data": {"key": "value"}
}

# 调用
result = app.invoke(initial_state)
print(result)
"""
{'user_input': 'test', 'response': 'test', 'count': 1, 'process_data': {'key': 'value'}}

"""
