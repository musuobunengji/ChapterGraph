def normalize_progress(percent: int | float) -> float:
    """turn progrss in data.json to %"""
    return max(0.0, min(percent / 100.0, 1.0))
