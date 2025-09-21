"""Utility helpers for working with mem0 memory client."""

from __future__ import annotations

from typing import Any, Dict, List

from mem0 import MemoryClient


class Mem0Memory:
    def __init__(self, client: MemoryClient, user_id: str):
        self.client = client
        self.user_id = user_id

    def add_message(self, content: str) -> Dict[str, Any]:
        payload = [{"role": "user", "content": content}]
        return self.client.add(messages=payload, user_id=self.user_id)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        return self.client.search(query=query, user_id=self.user_id, top_k=top_k)

    def get_summary(self) -> Dict[str, Any]:
        return self.client.get_summary(filters={"user_id": self.user_id})
