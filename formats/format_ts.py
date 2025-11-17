def format_ts(microseconds: float) -> str:
    s = int(microseconds / 1000)  # отбрасываем дробную часть
    m = s // 60
    s = s % 60
    return f"{m:02d}:{s:02d}"
