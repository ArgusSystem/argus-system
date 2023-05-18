from collections import defaultdict
from math import inf


def _get_key(sighting):
    return sighting.person_id, sighting.restriction_id


def intersect(a, b):
    return (a[0] <= b[0] <= a[1]) or (b[0] <= a[0] <= b[1])


class NotificationHistory:

    def __init__(self):
        # TODO: A deque may be more performant, with a circular array implementation
        self.history: defaultdict = defaultdict(list)

    def update(self, sighting):
        interval = sighting.interval()
        entries = self._get_entry(sighting)

        for entry in entries:
            if intersect(entry._interval, interval):
                entry._increase_interval(interval)
                return entry

        history_entry = NotificationHistory.Entry(interval)
        entries.append(history_entry)

        return history_entry

    def _get_entry(self, sighting):
        return self.history[_get_key(sighting)]

    class Entry:

        def __init__(self, interval):
            self._interval = interval
            self._users_notified = set()

        def _increase_interval(self, interval):
            self._interval = (
                min(self._interval[0], interval[0]),
                max(self._interval[1], interval[1])
            )

        def has_notified(self, user_id):
            return user_id in self._users_notified

        def notify_user(self, user_id):
            self._users_notified.add(user_id)
