# -*- coding: utf-8 -*-
"""
@File    : 2.dynamic_model.py
@Time    : 2025/11/7 16:41
@Desc    : 
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-4o-mini")
advanced_model = ChatOpenAI(model="gpt-4o")


@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话的复杂程度选择模型"""
    message_count = len(request.state['messages'])
    if message_count > 10:
        # 对于更长的对话使用更强大的模型
        model = advanced_model
    else:
        model = basic_model
    request.model = model
    handler(request)


agent = create_agent(
    model=basic_model,
    tools=tools,
    middleware=[dynamic_model_selection]
)
