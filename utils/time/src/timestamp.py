from datetime import datetime, timezone

import pytz

ARGENTINA_TZ = pytz.timezone('America/Buenos_Aires')


def from_timestamp_ms(timestamp, tz):
    return from_timestamp(timestamp // 1000, tz)


def from_timestamp(timestamp, tz=timezone.utc):
    return datetime.fromtimestamp(timestamp, tz)
