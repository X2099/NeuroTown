# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2025/11/4 14:17
@Desc    : 
"""
from app.memory.npc_memory import SimpleMemory

mem = SimpleMemory("李小白", "data/memory")

mem.add("小李今天在集市买了水果。")
mem.add("阿花喜欢画画。")
mem.add("老王准备去旅行。")

print("\n🔎 查询结果：")
result = mem.recall("谁喜欢艺术？")
print(result)
