def filter_pluralize(number: int, singular: str = '', plural: str = 's') -> str:
    return singular if number == 1 else plural


def filter_seconds_to_mm_ss(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes:02d}:{seconds:02d}'
