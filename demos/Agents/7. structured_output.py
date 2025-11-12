# -*- coding: utf-8 -*-
"""
@File    : 7. structured_output.py
@Time    : 2025/11/12 9:44
@Desc    : 
"""
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy


@tool
def search_tool(query: str) -> str:
    """搜索信息"""
    return f"结果是{query}"


class ContactInfo(BaseModel):
    """联系方式"""
    name: str
    email: str
    phone: str


agent = create_agent(
    model="deepseek-chat",
    tools=[search_tool],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "从以下内容中提取联系方式：曹雪芹，caoxueqin@163.com，010-5899977"}]
})

print(result)
# {'messages': [
#     HumanMessage(content='从以下内容中提取联系方式：曹雪芹，caoxueqin@163.com，010-5899977',
#                  additional_kwargs={},
#                  response_metadata={},
#                  id='66589904-86ff-40e7-99c0-92c4dde84b73'),
#     AIMessage(content='',
#               additional_kwargs={'refusal': None},
#               response_metadata={
#                   'token_usage': {'completion_tokens': 37, 'prompt_tokens': 230, 'total_tokens': 267,
#                                   'completion_tokens_details': None,
#                                   'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0},
#                                   'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 230},
#                   'model_provider': 'deepseek',
#                   'model_name': 'deepseek-chat',
#                   'system_fingerprint': 'fp_ffc7281d48_prod0820_fp8_kvcache',
#                   'id': 'ff83c55b-da27-48f3-9930-f6386bedabc0',
#                   'finish_reason': 'tool_calls',
#                   'logprobs': None},
#               id='lc_run--5154f781-b4a5-48bd-865e-74f0cd89196d-0', tool_calls=[
#             {'name': 'ContactInfo', 'args': {'name': '曹雪芹', 'email': 'caoxueqin@163.com', 'phone': '010-5899977'},
#              'id': 'call_00_9CttzSFYzqSyKyR5ZCTvbz9Z', 'type': 'tool_call'}],
#               usage_metadata={'input_tokens': 230, 'output_tokens': 37, 'total_tokens': 267,
#                               'input_token_details': {'cache_read': 0}, 'output_token_details': {}}),
#     ToolMessage(content="Returning structured response: name='曹雪芹' email='caoxueqin@163.com' phone='010-5899977'",
#                 name='ContactInfo', id='e5683c18-f725-4710-9c0f-f9103e7a5f8a',
#                 tool_call_id='call_00_9CttzSFYzqSyKyR5ZCTvbz9Z')],
#     'structured_response': ContactInfo(name='曹雪芹', email='caoxueqin@163.com', phone='010-5899977')}

agent = create_agent(
    model="deepseek-chat",
    tools=[search_tool],
    response_format=ProviderStrategy(ContactInfo)
)
