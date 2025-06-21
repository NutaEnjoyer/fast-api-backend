from datetime import datetime, timedelta


def get_start_datetime() -> tuple[datetime, datetime]:
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = (datetime.now() - timedelta(days=7)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    return today_start, week_start
