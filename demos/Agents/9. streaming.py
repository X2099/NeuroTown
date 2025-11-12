# -*- coding: utf-8 -*-
"""
@File    : 9. streaming.py
@Time    : 2025/11/12 10:47
@Desc    : 
"""
from langchain.agents import create_agent

agent = create_agent(
    model="deepseek-chat"
)

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "搜索人工智能新闻并总结。"}]
}, stream_mode="values"):
    # print(chunk)
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
