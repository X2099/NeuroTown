# -*- coding: utf-8 -*-
"""
@File    : handles_emails_agent.py
@Time    : 2025/11/13 16:47
@Desc    : 
"""
from typing import TypedDict, Literal

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.types import Command, RetryPolicy, interrupt
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage


class EmailClassification(TypedDict):
    """邮件分类结构化"""

    # 意图：“问题”、“缺陷”、“计费”、“功能”、“复杂”
    intent: Literal["question", "bug", "billing", "feature", "complex"]
    # 紧急程度：“低”、“中”、“高”、“严重”
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str  # 主题
    summary: str  # 摘要


class EmailAgentState(TypedDict):
    """define state"""
    # 邮件的原始数据
    email_content: str
    email_sender: str
    email_id: str
    # 邮件分类
    classification: EmailClassification | None
    search_results: list[str] | None
    customer_history: dict | None
    draft_response: str | None
    messages: list[str] | None


llm = ChatDeepSeek(model="deepseek-chat")


def read_email(state: EmailAgentState) -> dict:
    """提取并解析邮件内容"""
    return {"messages": [HumanMessage(content=f"处理邮件：{state['email_content']}")]}


def classify_intent(state: EmailAgentState) -> Command[
    Literal["search_documentation", "human_review", "draft_response", "bug_tracking"]
]:
    """使用 LLM 对电子邮件意图和紧急程度进行分类，然后进行相应的路由"""
    structured_llm = llm.with_structured_output(EmailClassification)
    classification_prompt = f"""
    分析此客户电子邮件并对其进行分类：

    邮件内容：{state['email_content']}
    发件人：{state['email_sender']}
    
    提供包含intent（意图）、urgency（紧急程度）的分类以及topic（主题）和summary（摘要）。
    """
    classification = structured_llm.invoke(classification_prompt)
    if classification['intent'] == 'billing' or classification['urgency'] == 'critical':  # 计费 严重
        goto = "human_review"
    elif classification['intent'] in ['question', 'feature']:
        goto = "search_documentation"
    elif classification['intent'] == 'bug':
        goto = "bug_tracking"
    else:
        goto = "draft_response"
    return Command(update={"classification": classification}, goto=goto)


def search_documentation(state: EmailAgentState) -> Command[Literal["draft_response"]]:
    """在知识库中搜索相关信息"""
    classification = state.get('classification', {})
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"
    try:
        search_results = [
            "通过【设置】 > 【安全】 > 【更改密码】重置密码",
            "密码长度必须至少为12个字符",
            "密码必须包含大写字母、小写字母、数字和符号"
        ]
    except Exception as e:
        search_results = [f"搜索功能发生异常，暂时不可用: {str(e)}"]
    return Command(update={"search_results": search_results}, goto="draft_response")


def bug_tracking(state: EmailAgentState) -> Command[Literal["draft_response"]]:
    """创建或更新bug跟踪工单"""
    ticket_id = "BUG-12345"
    return Command(
        update={
            "search_results": [f"创建了Bug跟踪工单：{ticket_id}。"],
            "current_step": "bug_tracked"
        },
        goto="draft_response"
    )


def draft_response(state: EmailAgentState) -> Command[Literal["human_review", "send_reply"]]:
    """根据上下文生成回复草稿，并根据质量进行路由"""
    classification = state.get('classification', {})
    # 按需从原始状态数据格式化上下文
    context_sections = []
    if state.get('search_results'):
        formatted_docs = '\n'.join([f"- {doc}" for doc in state['search_results']])
        context_sections.append(f"相关文档：\n{formatted_docs}")
    if state.get('customer_history'):
        context_sections.append(f"客户等级：{state['customer_history'].get('tier', 'standard')}")

    # 根据格式化的上下文构造提示词
    draft_prompt = f"""
    撰写给此客户邮件的回复：
    {state['email_content']}
    
    邮件意图：{classification.get('intent', 'unknown')}
    紧急程度：{classification.get('urgency', 'medium')}
    
    {chr(10).join(context_sections)}
    
    指导原则：
    - 保持专业和乐于助人的态度
    - 解决客户的具体问题
    - 必要时使用客户提供的文档
    """
    response = llm.invoke(draft_prompt)
    # 根据紧急程度和意图确定是否需要人工审核
    needs_review = (classification.get('intent') == 'complex' or
                    classification.get('urgency') in ('high', 'critical'))
    goto = "human_review" if needs_review else "send_reply"
    return Command(
        update={"draft_response": response.content},
        goto=goto
    )


def human_review(state: EmailAgentState) -> Command[Literal["send_reply", END]]:
    """暂停进行人工审核（使用中断），并根据决策进行路由"""
    classification = state.get('classification', {})
    human_decision = interrupt({
        "email_id": state.get('email_id', ''),
        "original_email": state.get('email_content', ''),
        "draft_response": state.get('draft_response', ''),
        "urgency": classification.get('urgency'),
        "intent": classification.get('intent'),
        "action": "请审核并批准或者编辑此回复。"
    })
    if human_decision.get("approved"):
        return Command(
            update={"draft_response": human_decision.get("edited_response", state.get("draft_response", ""))},
            goto="send_reply"
        )
    else:
        return Command(update={}, goto=END)


def send_reply(state: EmailAgentState) -> dict:
    """发送回复邮件"""
    print(f"发送回复邮件：{state['draft_response'][:100]}……")
    return {}


workflow = StateGraph(EmailAgentState)  # 状态
workflow.add_node("read_email", read_email)  # 阅读邮件
workflow.add_node("classify_intent", classify_intent)  # 意图识别分类
workflow.add_node("search_documentation", search_documentation,
                  retry_policy=RetryPolicy(max_attempts=3, initial_interval=1))  # 搜索信息
workflow.add_node("bug_tracking", bug_tracking)  # Bug跟踪
workflow.add_node("draft_response", draft_response)  # 生成回复草稿
workflow.add_node("human_review", human_review)  # 人工审核
workflow.add_node("send_reply", send_reply)  # 发送回复邮件

workflow.add_edge(START, "read_email")  # START -> 阅读邮件
workflow.add_edge("read_email", "classify_intent")  # 阅读邮件 -> 意图识别并分类
workflow.add_edge("send_reply", END)  # 发送回复邮件 -> END

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == '__main__':
    from pprint import pprint

    initial_state = {
        "email_content": "我的订阅费被重复扣款了！情况紧急！",
        "email_sender": "customer@example.com",
        "email_id": "email_123",
        "messages": []
    }
    config = {"configurable": {"thread_id": "customer_123"}}
    result = app.invoke(initial_state, config)
    pprint(result)
    # print(f"草稿已准备好供审核: {result['draft_response'][:100]}...")

    from langgraph.types import Command

    human_response = Command(
        resume={
            "approved": True,
            "edited_response": "对于重复收费，我们深表歉意。我已经启动了立即退款流程……"
        }
    )

    # 恢复执行
    final_result = app.invoke(human_response, config)
    print(final_result)
    print(f"发送回复邮件成功！")
