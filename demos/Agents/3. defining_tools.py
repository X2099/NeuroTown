# -*- coding: utf-8 -*-
"""
@File    : 3. defining_tools.py
@Time    : 2025/11/10 11:37
@Desc    : 
"""
from langchain.tools import tool
from langchain.agents import create_agent


@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"Results for:{query}"


@tool
def get_weather(location: str) -> str:
    """获取指定地点的天气信息"""
    return f"{location}阳光明媚，19.5℃。"


agent = create_agent(model=model, tools=[search, get_weather])
