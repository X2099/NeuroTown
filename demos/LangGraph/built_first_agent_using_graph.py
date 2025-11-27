# -*- coding: utf-8 -*-
"""
@File    : built_first_agent_using_graph.py
@Time    : 2025/11/27 10:54
@Desc    : 
"""
import operator
from typing import TypedDict, Annotated, Literal

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph

model = init_chat_model("deepseek:deepseek-chat", temperature=0)


@tool
def multiply(a: int, b: int) -> int:
    """计算整数a和整数b的乘积"""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """计算整数a和整数b的和"""
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """计算整数a除以整数b的商"""
    return a / b


tools = [multiply, add, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def llm_call(state: MessagesState) -> dict:
    """大语言模型决定是否使用工具"""
    return {
        "messages": [
            model_with_tools.invoke(
                [SystemMessage(content='你是一名乐于助人的助手，任务是对一组输入数据进行算术运算。')]
                + state['messages']
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


def tool_node(state: MessagesState) -> dict:
    """执行工具调用"""
    result = []
    for tool_call in state['messages'][-1].tool_calls:
        tool = tools_by_name[tool_call['name']]
        observation = tool.invoke(tool_call['args'])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call['id']))
    return {'messages': result}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """根据LLM是否发出工具调用，决定是否继续循环或停止。"""
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent = agent_builder.compile()
