# -*- coding: utf-8 -*-
"""
@File    : use_time_travel.py
@Time    : 2025/11/19 16:15
@Desc    : 
"""
import os
import getpass

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, NotRequired
from langchain.chat_models import init_chat_model


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("DEEPSEEK_API_KEY")


class State(TypedDict):
    topic: NotRequired[str]
    joke: NotRequired[str]


model = init_chat_model("deepseek:deepseek-chat", temperature=0)


def generate_topic(state: State) -> dict:
    """通过LLM生成笑话主题"""
    msg = model.invoke("给我一个好笑的笑话主题（简短一句话）。")
    return {"topic": msg.content}


def write_joke(state: State) -> dict:
    """通过LLM编写笑话"""
    msg = model.invoke(f"写一则关于{state['topic']}的简短笑话（简短一句话）。")
    return {"joke": msg.content}


# 创建工作流
workflow = StateGraph(State)
workflow.add_node("generate_topic", generate_topic)
workflow.add_node("write_joke", write_joke)
workflow.add_edge(START, "generate_topic")
workflow.add_edge("generate_topic", "write_joke")
workflow.add_edge("write_joke", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer)
