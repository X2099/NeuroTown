# -*- coding: utf-8 -*-
"""
@File    : npc_memory.py
@Time    : 2025/10/31 13:57
@Desc    : 
"""
import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pypinyin import lazy_pinyin

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh-v1.5")


class SimpleMemory:
    """
    轻量化记忆：保留原文历史 + 支持关键词检索
    """

    def __init__(self, owner_name: str, role: str, persist_dir="data/memory"):

        pinyin_name = ''.join(lazy_pinyin(owner_name))
        self.persist_dir = os.path.join(persist_dir, pinyin_name)
        os.makedirs(self.persist_dir, exist_ok=True)
        index_path = os.path.join(self.persist_dir, "index.faiss")
        if os.path.exists(index_path):
            print(f"🔁 正在加载【{owner_name}】的本地记忆...")
            self.vs = FAISS.load_local(self.persist_dir, embeddings, allow_dangerous_deserialization=True)
            self.history = [doc.page_content for doc in self.vs.docstore._dict.values()]
        else:
            print(f"🆕 初始化【{owner_name}】的记忆库...")
            self.history = [f"我是{role}{owner_name}。"]
            self.vs = FAISS.from_texts(self.history, embeddings)
            self.save_memory()

    def add(self, text: str):
        if not text.strip():
            return
        self.history.append(text)
        self.vs.add_texts([text])
        self.save_memory()

    def recent(self, n: int = 5) -> str:
        return "\n".join(self.history[-n:])

    def recall(self, query: str, k: int = 3) -> str:
        docs = self.vs.similarity_search(query, k)
        return '\n'.join(doc.page_content for doc in docs)

    def save_memory(self):
        """保存到本地"""
        self.vs.save_local(self.persist_dir)
