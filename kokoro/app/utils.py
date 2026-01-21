import time

def enforce_min_duration(text: str, min_seconds: float = 0.5):
    estimated_time = len(text) * 0.02
    if estimated_time < min_seconds:
        time.sleep(min_seconds - estimated_time)
