"""Utility helpers for mem0 CLI chat."""

from __future__ import annotations

from typing import Any, Dict, List

from mem0 import MemoryClient

DEFAULT_VERSION = "v1"


class Mem0Memory:
    def __init__(self, client: MemoryClient, user_id: str):
        self.client = client
        self.user_id = user_id

    def add(self, content: str) -> Dict[str, Any]:
        messages = [{"role": "user", "content": content}]
        return self.client.add(messages=messages, user_id=self.user_id)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        return self.client.search(
            query=query,
            version=DEFAULT_VERSION,
            user_id=self.user_id,
            top_k=top_k,
        )

    def recent(self, top_k: int = 3) -> List[Dict[str, Any]]:
        memories = self.client.get_all(version=DEFAULT_VERSION, user_id=self.user_id)
        return memories[:top_k]
