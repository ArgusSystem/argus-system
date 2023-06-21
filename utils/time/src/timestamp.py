from datetime import datetime, timezone


def from_timestamp_ms(timestamp):
    return from_timestamp(timestamp // 1000)


def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
