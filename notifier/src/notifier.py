from utils.events.src.messages.broken_rule_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode
from utils.orm.src import Notification
from utils.tracing.src.tracer import get_context


class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer

    def on_broken_rule(self, message):
        broken_restriction_message: BrokenRestrictionMessage = decode(BrokenRestrictionMessage, message)

        with self.tracer.start_as_current_span('notifier', context=get_context(broken_restriction_message.trace_id)):

            Notification(broken_rule_id=broken_restriction_message.broken_restriction_id).save()
