"""
client.py
Single shared Anthropic client for the entire pipeline.
"""

import anthropic

_client = None

def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client
