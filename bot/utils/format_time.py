import functools


@functools.lru_cache
def format_time(milliseconds: int) -> str:
    secs = milliseconds / 1000
    secs = secs % (24 * 3600)
    hours = secs // 3600
    secs %= 3600
    mins = secs // 60
    secs %= 60
    return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
