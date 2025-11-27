# -*- coding: utf-8 -*-
"""
@File    : interrupts_in_tools.py
@Time    : 2025/11/21 11:24
@Desc    : 
"""
import sqlite3
from typing import TypedDict

from langchain.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt


class AgentState(TypedDict):
    messages: list[dict]


@tool
def send_email(to: str, subject: str, body: str):
    """向收件人发送电子邮件"""
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "批准发送此电子邮件？"
    })
    if response.get("action") == "approve":
        final_to = response.get("to", to)
        final_subject = response.get("subject", subject)
        final_body = response.get("body", body)
        print(f"[send_email] to={final_to} subject={final_subject} body={final_body}")
        return f"邮件已发给{final_to}。"
    return "邮件被取消发送。"


model = ChatDeepSeek(model="deepseek-chat").bind_tools([send_email])


def agent_node(state: AgentState):
    result = model.invoke(state["messages"])
    return {"messages": state["messages"] + [result]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

checkpointer = SqliteSaver(sqlite3.connect("tool-approval.db", check_same_thread=False))
graph = builder.compile(checkpointer=checkpointer)
