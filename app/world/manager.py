# -*- coding: utf-8 -*-
"""
@File    : manager.py
@Time    : 2025/10/31 11:10
@Desc    : 
"""
import asyncio
import random
from typing import List
from time import monotonic

from .state import WorldState
from ..agents.npc_agent import NPCAgent


class TownManager:
    def __init__(self, agents: List[NPCAgent], world: WorldState):
        self.agents = agents
        self.world = world

    async def run(self, steps: int = 10, tick_delay: float = 1.0):
        """
        核心循环：每个 step 增加 world.time，并让所有 agent 依次思考和行动。
        tick_delay 控制每一轮之间的暂停（秒）
        """
        start = monotonic()
        self.world.advance_time()
        recent_str = self.world.recent_events()
        print(f"\n=== Tick {self.world.time} ===")
        # 并发或顺序取决你想要的行为风格；这里按顺序执行，便于可读性与调试
        for agent in self.agents:
            try:
                action = await agent.think_and_act(self.world)
                # 统一事件结构
                evt = {"tick": self.world.time, "actor": action.get("actor"), "text": action.get("text")}
                self.world.add_event(evt)
                print(f"🕒 t={self.world.time} | {evt['actor']}: {evt['text']}")
            except Exception as e:
                raise e

            elapsed = monotonic() - start
            wait = max(0.0, tick_delay - elapsed)
            if wait > 0:
                await asyncio.sleep(wait)
        print("\n=== Simulation complete ===")

    async def step(self):
        """
        世界时间推进一刻，更新所有NPC的状态与事件
        """
        self.world.advance_time()
        events = []
        for npc in self.agents:
            action = await npc.think_and_act(self.world)
            # 统一事件结构
            evt = {"tick": self.world.time, "actor": action.get("actor"), "text": action.get("text")}
            self.world.add_event(evt)
            events.append(f"{npc.name} {action}")
        return events


town_world = WorldState()
# 创建 NPC
npcs = [
    NPCAgent(name="李建国", role="教师", mood="开心", x=random.randint(1, 100), y=random.randint(1, 100), emoji="🧑‍🌾"),
    NPCAgent(name="王铁锤", role="铁匠", mood="好奇", x=random.randint(1, 100), y=random.randint(1, 100), emoji="👩‍🎨"),
    NPCAgent(name="张秀才", role="画家", mood="疲倦", x=random.randint(1, 100), y=random.randint(1, 100), emoji="👨‍🔧")
]
# 简单预设一些记忆
# lijianguo.memory.add("I love gardening and teaching children.")
# bob.memory.add("I own a small stall at the market selling spices.")
# eve.memory.add("I paint city scenes and sell paintings at the cafe.")
# 启动管理器
# -------------------------------------------------------------------------
# 全局单例（让 FastAPI 直接使用）
# -------------------------------------------------------------------------
town_manager = TownManager(agents=npcs, world=town_world)
