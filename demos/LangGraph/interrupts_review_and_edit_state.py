# -*- coding: utf-8 -*-
"""
@File    : interrupts_review_and_edit_state.py
@Time    : 2025/11/21 11:04
@Desc    : 
"""
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt


class ReviewState(TypedDict):
    generated_text: str


def review_node(state: ReviewState):
    updated = interrupt({
        "instruction": "请审核并编辑此内容。",
        "content": state["generated_text"]
    })
    return {"generated_text": updated}


builder = StateGraph(ReviewState)
builder.add_node("review", review_node)
builder.add_edge(START, "review")
builder.add_edge("review", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer)
