from datetime import datetime
from pytz import timezone


TZ_ARG = timezone('America/Argentina/Buenos_Aires');


def from_timestamp_ms(timestamp):
    return from_timestamp(timestamp // 1000)


def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=TZ_ARG)
