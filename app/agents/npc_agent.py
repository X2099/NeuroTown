# -*- coding: utf-8 -*-
"""
@File    : npc_agent.py
@Time    : 2025/10/31 11:35
@Desc    : 
"""
import os
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent
from ..memory.npc_memory import SimpleMemory
from ..world.state import WorldState


class NPCAgent(BaseAgent):
    def __init__(self, name: str, role: str, mood: str, x: int, y: int, emoji="🧑‍🌾"):
        super().__init__(name, role, mood, x, y, emoji)
        self.memory = SimpleMemory(name, role)
        self.llm: ChatOpenAI = ChatOpenAI(
            temperature=0.7,
            model="deepseek-chat",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com"
        )
        # 一个简短的人设提示
        self.persona = f"你是{self.name}, 作为神经小镇上的一位{self.role}，请保持个性一致，并用一句简短的话回复你的行动。"

    async def think_and_act(self, world_state: WorldState) -> Dict[str, Any]:
        """
        1) 构建 prompt - persona + recent memories + observation
        2) 调用 LLM 得到行动文本
        3) 将行动存入记忆并返回结构化 action
        """
        recent_mem = self.memory.recent(4)
        obs = f"World time: {world_state.time}. Recent events: {world_state.recent_events}"
        prompt = [
            SystemMessage(content=self.persona),
            HumanMessage(
                content=f"Observations:\n{obs}\n\nMemories:\n{recent_mem}\n\nQuestion: 接下来你要做什么？请用一句简短的话来概括你的行为。")
        ]
        response = await self.llm.ainvoke(prompt)
        action_text = response.content.split()
        action = {"actor": self.name, "text": action_text}
        self.memory.add(action_text[0])
        return action

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "mood": self.mood,
            "x": self.x,
            "y": self.y,
            "emoji": self.emoji,
            "memory": self.memory.recent()
        }
