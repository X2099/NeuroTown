# -*- coding: utf-8 -*-
"""
@File    : memory_store.py
@Time    : 2025/11/20 16:06
@Desc    : 
"""
import uuid

from langgraph.store.memory import InMemoryStore

in_memory_store = InMemoryStore()

user_id = "1"
namespace_for_memory = (user_id, "memories")
memory_id = str(uuid.uuid4())
memory = {"food_preference": "我喜欢吃牛肉。"}

in_memory_store.put(namespace_for_memory, memory_id, memory)
