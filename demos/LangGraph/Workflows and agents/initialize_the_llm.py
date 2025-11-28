# -*- coding: utf-8 -*-
"""
@File    : initialize_the_llm.py
@Time    : 2025/11/28 10:24
@Desc    : 
"""
import os
import getpass
from langchain_deepseek import ChatDeepSeek


def _set_env(var: str):
    if not os.getenv(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("DEEPSEEK_API_KEY")

llm = ChatDeepSeek(model="deepseek-chat")
