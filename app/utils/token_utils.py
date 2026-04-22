def approximate_token_count(text: str) -> int:
    # quick heuristic: ~4 chars per token in English
    return max(1, len(text) // 4)
