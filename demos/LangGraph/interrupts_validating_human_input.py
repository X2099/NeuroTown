# -*- coding: utf-8 -*-
"""
@File    : interrupts_validating_human_input.py
@Time    : 2025/11/21 15:06
@Desc    : 
"""
import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt


class FormState(TypedDict):
    age: None | int


def get_age_node(state: FormState):
    prompt = "你的年龄是多少？"
    while True:
        answer = interrupt(prompt)
        if isinstance(answer, int) and answer > 0:
            return {"age": answer}
        prompt = f"“{answer}”不是有效年龄。请输入一个正数。"


builder = StateGraph(FormState)
builder.add_node("collect_age", get_age_node)
builder.add_edge(START, "collect_age")
builder.add_edge("collect_age", END)

checkpointer = SqliteSaver(sqlite3.connect("forms.db", check_same_thread=False))
graph = builder.compile(checkpointer)
