# -*- coding: utf-8 -*-
"""
@File    : 5. system_prompt.py
@Time    : 2025/11/10 17:02
@Desc    : 
"""
from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest


class Context(TypedDict):
    user_role: str


@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """根据用户角色生成系统提示词"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "你是一位得力的智能助手。"
    if user_role == "expert":  # 专家
        return f"{base_prompt}请提供详细的技术解答。"
    elif user_role == "beginner":  # 新手
        return f"{base_prompt}用简洁易懂的方式解释概念，避免使用专业术语。"
    return base_prompt


agent = create_agent(
    model='gpt-4o',
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context

)

result = agent.invoke({
    "messages": [{"role": "user", "content": "解释一下机器学习！"}],
    "context": {"user_role": "expert"}
})
