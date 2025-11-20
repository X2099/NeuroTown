# -*- coding: utf-8 -*-
"""
@File    : checkpoints.py
@Time    : 2025/11/18 14:09
@Desc    : 
"""
from operator import add

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import StateSnapshot, PregelTask
from typing_extensions import TypedDict
from typing import Annotated


class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]


def node_a(state: State) -> dict:
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State) -> dict:
    return {"foo": "b", "bar": ["b"]}


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)
checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

result = graph.invoke({"foo": ""}, config)
print(result)

[
    StateSnapshot(values={'foo': 'b', 'bar': ['a', 'b']},
                  next=(),
                  config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                           'checkpoint_id': '1f0c5152-d76e-65b6-8002-b5d1b8ca540d'}},
                  metadata={'source': 'loop', 'step': 2, 'parents': {}},
                  created_at='2025-11-19T06:58:39.623723+00:00',
                  parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                                  'checkpoint_id': '1f0c5152-d769-6999-8001-d6343b3b2296'}},
                  tasks=(),
                  interrupts=()),

    StateSnapshot(values={'foo': 'a', 'bar': ['a']},
                  next=('node_b',),
                  config={
                      'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                       'checkpoint_id': '1f0c5152-d769-6999-8001-d6343b3b2296'}},
                  metadata={'source': 'loop', 'step': 1, 'parents': {}},
                  created_at='2025-11-19T06:58:39.621775+00:00',
                  parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                                  'checkpoint_id': '1f0c5152-d764-695a-8000-85bb4b696054'}},
                  tasks=(
                      PregelTask(id='520e8448-7c43-762b-6316-9bcad9a064db',
                                 name='node_b',
                                 path=('__pregel_pull', 'node_b'),
                                 error=None,
                                 interrupts=(), state=None, result={'foo': 'b', 'bar': ['b']}),),
                  interrupts=()),
    StateSnapshot(values={'foo': '', 'bar': []},
                  next=('node_a',),
                  config={
                      'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                       'checkpoint_id': '1f0c5152-d764-695a-8000-85bb4b696054'}},
                  metadata={'source': 'loop', 'step': 0, 'parents': {}},
                  created_at='2025-11-19T06:58:39.619721+00:00',
                  parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                                  'checkpoint_id': '1f0c5152-d75d-643a-bfff-0838c5030661'}},
                  tasks=(
                      PregelTask(id='1b5c2eb4-db6e-f161-a159-1145f4be9de2', name='node_a',
                                 path=('__pregel_pull', 'node_a'),
                                 error=None,
                                 interrupts=(), state=None, result={'foo': 'a', 'bar': ['a']}),),
                  interrupts=()),
    StateSnapshot(values={'bar': []},
                  next=('__start__',),
                  config={
                      'configurable': {'thread_id': '1', 'checkpoint_ns': '',
                                       'checkpoint_id': '1f0c5152-d75d-643a-bfff-0838c5030661'}},
                  metadata={'source': 'input', 'step': -1, 'parents': {}},
                  created_at='2025-11-19T06:58:39.616722+00:00',
                  parent_config=None,
                  tasks=(
                      PregelTask(id='1dfd459b-7930-9793-457b-cef2d76e8a4a', name='__start__',
                                 path=('__pregel_pull', '__start__'),
                                 error=None, interrupts=(), state=None, result={'foo': ''}),),
                  interrupts=())]
