# -*- coding: utf-8 -*-
"""
@File    : base_agent.py
@Time    : 2025/10/31 9:35
@Desc    : 
"""
import abc


class BaseAgent(abc.ABC):
    """
    抽象的智能体基类，定义接口
    """

    def __init__(self, name: str, role: str, mood: str, x: int, y: int, emoji: str):
        """
        :param name: 名称
        :param role: 角色
        :param mood: 心情
        :param x: x坐标
        :param y: y坐标
        :param emoji: 头像
        """
        self.name = name
        self.role = role
        self.mood = mood
        self.x = x
        self.y = y
        self.emoji = emoji

    @abc.abstractmethod
    async def think_and_act(self, world_state: dict) -> dict:
        """
        基于当前 world_state 做出决策并返回 action 描述
        """
        raise NotImplementedError
