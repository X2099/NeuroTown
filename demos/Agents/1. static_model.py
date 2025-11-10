# -*- coding: utf-8 -*-
"""
@File    : static_model.py
@Time    : 2025/11/6 16:29
@Desc    : 
"""

from langchain.agents import create_agent

agent = create_agent(
    'gpt5',
    tools=tools
)

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model='gpt5',
    temperature=0.1,
    max_tokens=100,
    timeout=30,
    # ...
)
agent = create_agent(model, tools=tools)
