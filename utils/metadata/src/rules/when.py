import pytz

from utils.time.src.timestamp import from_timestamp_ms
from .factory import create

START_TIME = 'start_time'
END_TIME = 'end_time'
TIME_ZONE = 'time_zone'
DAYS = 'days'

ALL_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def days_to_mask(days):
    num = 0

    for d in days:
        num |= 1 << ALL_DAYS.index(d)

    return num


class Single:

    def __init__(self, configuration):
        self.start_time = configuration[START_TIME]
        self.end_time = configuration[END_TIME]

    def match(self, timestamp):
        return self.start_time <= timestamp <= self.end_time


class Repeated:

    def __init__(self, configuration):
        self.start_time = configuration[START_TIME]
        self.end_time = configuration[END_TIME]
        self.days_mask = days_to_mask(configuration[DAYS])
        self.time_zone = pytz.timezone(configuration[TIME_ZONE])

    def match(self, timestamp):
        dt = from_timestamp_ms(timestamp, self.time_zone)
        tt = dt.timetuple()
        time = tt.tm_hour * 3600 + tt.tm_min * 60 + tt.tm_sec

        return ((1 << tt.tm_wday) & self.days_mask) > 0 and self.start_time <= time <= self.end_time


TYPES = {
    'single': Single,
    'repeated': Repeated
}


class WhenRule:

    def __init__(self, configuration):
        self.rules = [create(TYPES, node) for node in configuration]

    def match(self, when):
        return any(rule.match(when) for rule in self.rules)
