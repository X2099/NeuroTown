# -*- coding: utf-8 -*-
"""
@File    : 8. memory.py
@Time    : 2025/11/12 10:15
@Desc    : 
"""
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware


class CustomState(AgentState):
    user_preferences: dict


# 通过中间件定义状态
class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]

    def before_model(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        ...


agent = create_agent(
    model=model,
    tools=tools,
    middleware=[CustomMiddleware()]
)
# 通过参数 state_schema 定义智能体状态
agent = create_agent(
    model,
    tools=tools,
    state_schema=CustomState
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "我喜欢更技术性的解释。"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"}
})
