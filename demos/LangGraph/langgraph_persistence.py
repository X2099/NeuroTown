# -*- coding: utf-8 -*-
"""
@File    : langgraph_persistence.py
@Time    : 2025/11/18 10:41
@Desc    : 
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from typing import Annotated
from operator import add


class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]


def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


# 定义图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 使用 InMemorySaver 作为检查点存储器
checkpointer = InMemorySaver()

# 编译图，传入 checkpointer
graph = workflow.compile(checkpointer=checkpointer)

# 执行图 (run)，指定 thread_id
config = {"configurable": {"thread_id": "thread-1"}}
graph.invoke({"foo": ""}, config)

# 获取最新状态
snapshot = graph.get_state(config)
print("Current state:", snapshot.values)

# 查看历史 checkpoint
history = list(graph.get_state_history(config))
for idx, snap in enumerate(history):
    print(f"Checkpoint {idx}: {snap.values}")
