"""
Date utility module for datetime operations.

This module provides utility functions for common datetime operations,
including getting start/end times for different periods and date
formatting utilities.
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional
import pytz


def get_start_datetime(timezone: str = "UTC") -> Tuple[datetime, datetime]:
    """
    Get start datetime for today and week ago.

    Args:
        timezone: Timezone string (default: "UTC")

    Returns:
        Tuple of (today_start, week_start) datetime objects

    Example:
        >>> today, week_ago = get_start_datetime()
        >>> print(today)  # 2024-01-15 00:00:00
        >>> print(week_ago)  # 2024-01-08 00:00:00
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = (now - timedelta(days=7)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        return today_start, week_start
    except pytz.exceptions.UnknownTimeZoneError:
        # Fallback to UTC if timezone is invalid
        now = datetime.now(pytz.timezone("UTC"))
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = (now - timedelta(days=7)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return today_start, week_start


def get_month_start_datetime(timezone: str = "UTC") -> datetime:
    """
    Get start datetime for current month.

    Args:
        timezone: Timezone string (default: "UTC")

    Returns:
        Start datetime of current month

    Example:
        >>> month_start = get_month_start_datetime()
        >>> print(month_start)  # 2024-01-01 00:00:00
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    except pytz.exceptions.UnknownTimeZoneError:
        now = datetime.now(pytz.timezone("UTC"))
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_date_range(days: int, timezone: str = "UTC") -> Tuple[datetime, datetime]:
    """
    Get date range from today going back specified number of days.

    Args:
        days: Number of days to go back
        timezone: Timezone string (default: "UTC")

    Returns:
        Tuple of (start_date, end_date) datetime objects

    Example:
        >>> start, end = get_date_range(30)
        >>> print(start)  # 2023-12-16 00:00:00
        >>> print(end)    # 2024-01-15 23:59:59
    """

    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = (now - timedelta(days=days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        return start_date, end_date
    except pytz.exceptions.UnknownTimeZoneError:
        now = datetime.now(pytz.timezone("UTC"))
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        start_date = (now - timedelta(days=days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    return start_date, end_date


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.

    Args:
        dt: Datetime object to format
        format_str: Format string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        Formatted datetime string

    Example:
        >>> dt = datetime.now()
        >>> formatted = format_datetime(dt, "%Y-%m-%d")
        >>> print(formatted)  # "2024-01-15"
    """
    return dt.strftime(format_str)


def parse_datetime(
    date_string: str, format_str: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[datetime]:
    """
    Parse datetime string to datetime object.

    Args:
        date_string: String to parse
        format_str: Format string to use for parsing

    Returns:
        Parsed datetime object or None if parsing fails

    Example:
        >>> dt = parse_datetime("2024-01-15 10:30:00")
        >>> print(dt)  # 2024-01-15 10:30:00
    """
    try:
        return datetime.strptime(date_string, format_str)
    except ValueError:
        return None


def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """
    Check if two datetime objects represent the same day.

    Args:
        dt1: First datetime object
        dt2: Second datetime object

    Returns:
        True if both dates are on the same day

    Example:
        >>> dt1 = datetime(2024, 1, 15, 10, 30)
        >>> dt2 = datetime(2024, 1, 15, 15, 45)
        >>> is_same_day(dt1, dt2)  # True
    """
    return dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day


def get_weekday_name(dt: datetime) -> str:
    """
    Get weekday name for datetime object.

    Args:
        dt: Datetime object

    Returns:
        Weekday name (Monday, Tuesday, etc.)

    Example:
        >>> dt = datetime(2024, 1, 15)  # Monday
        >>> weekday = get_weekday_name(dt)
        >>> print(weekday)  # "Monday"
    """
    return dt.strftime("%A")
