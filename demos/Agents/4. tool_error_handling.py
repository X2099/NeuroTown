# -*- coding: utf-8 -*-
"""
@File    : 4. tool_error_handling.py
@Time    : 2025/11/10 16:39
@Desc    : 
"""
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage


@wrap_tool_call
def handle_tool_errors(request, handler):
    """自定义工具执行异常处理消息"""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: 请检查你的输入然后重试。({e})",
            tool_call_id=request.tool_call['id']
        )


agent = create_agent(
    model=model,
    tools=[search, get_weather],
    middleware=[handle_tool_errors]
)
