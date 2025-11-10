# -*- coding: utf-8 -*-
"""
@File    : routes_town.py
@Time    : 2025/10/31 15:18
@Desc    : 
"""
from fastapi import APIRouter
from ..world.manager import town_manager

router = APIRouter()


@router.get("/state")
async def get_town_state():
    """获取小镇当前状态"""
    return town_manager.world.to_dict()


@router.get("/npcs")
async def get_all_npcs():
    """返回所有NPC的基本信息"""
    return [npc.to_dict() for npc in town_manager.agents]


@router.post("/tick")
async def tick_world():
    """时间推进一步"""
    result = await town_manager.step()
    return {"message": "时间流动了一刻", "event": result}
