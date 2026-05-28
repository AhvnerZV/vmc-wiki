"""
client.py
Single shared Anthropic client with exponential backoff retry.
Handles 429 (rate limit) and 5xx (server error) automatically.
"""

import time
import anthropic

_client: anthropic.Anthropic | None = None

MAX_RETRIES    = 4
BASE_DELAY     = 2.0   # seconds before first retry
MAX_DELAY      = 60.0  # cap


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def create_message_with_retry(**kwargs) -> anthropic.types.Message:
    """
    Wraps client.messages.create with exponential backoff.
    Retries on RateLimitError and InternalServerError.
    All other errors bubble up immediately.
    """
    client  = get_client()
    delay   = BASE_DELAY
    attempt = 0

    while True:
        try:
            return client.messages.create(**kwargs)

        except anthropic.RateLimitError as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise RuntimeError(
                    f"Rate limit hit {MAX_RETRIES} times in a row. "
                    "Wait a few minutes and re-run."
                ) from e
            wait = min(delay * (2 ** (attempt - 1)), MAX_DELAY)
            print(f"    Rate limited. Retrying in {wait:.0f}s (attempt {attempt}/{MAX_RETRIES})...")
            time.sleep(wait)

        except anthropic.InternalServerError as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise RuntimeError(f"Anthropic server error after {MAX_RETRIES} retries.") from e
            wait = min(delay * (2 ** (attempt - 1)), MAX_DELAY)
            print(f"    Server error. Retrying in {wait:.0f}s (attempt {attempt}/{MAX_RETRIES})...")
            time.sleep(wait)

        except anthropic.APIConnectionError as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise RuntimeError("Network connection failed. Check your internet.") from e
            wait = min(delay * (2 ** (attempt - 1)), MAX_DELAY)
            print(f"    Connection error. Retrying in {wait:.0f}s (attempt {attempt}/{MAX_RETRIES})...")
            time.sleep(wait)
