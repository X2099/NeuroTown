# -*- coding: utf-8 -*-
"""
@File    : state.py
@Time    : 2025/10/31 10:02
@Desc    : 
"""
from typing import List, Dict, Any


class WorldState:
    def __init__(self):
        self.time: int = 0
        self.events: List[Dict] = []
        self.recent_events_window: int = 10

    def add_event(self, event: Dict):
        self.events.append(event)
        if len(self.events) > 200:
            self.events = self.events[-200:]

    def recent_events(self, n: int = 5) -> str:
        items = self.events[-n:]
        return '\n'.join(f"{e.get('actor', '?')}: {e.get('text', '')}" for e in items)

    def advance_time(self):
        self.time += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "events": self.recent_events(10)
        }
