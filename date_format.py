from datetime import date


def format_date(date_value):
    if not date_value:
        return ""

    if isinstance(date_value, str):
        date_value = date.fromisoformat(date_value)

    return date_value.strftime("%b %d, %Y")
