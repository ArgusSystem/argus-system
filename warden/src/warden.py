from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.broken_restriction_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.orm.src.models import BrokenRestriction
from utils.tracing.src.tracer import get_context, get_trace_parent
from .rule_manager import RuleManager


class Warden:
    def __init__(self, tracer, publisher_configuration):
        self.tracer = tracer
        self.rule_manager = RuleManager()
        self.publisher = Publisher.new(**publisher_configuration)

    def execute_with(self, message):
        matched_face_message: MatchedFaceMessage = decode(MatchedFaceMessage, message)

        with self.tracer.start_as_current_span('warden', context=get_context(matched_face_message.trace)):
            face_id = matched_face_message.face_id

            warden_trace = get_trace_parent()

            for restriction_id in self.rule_manager.execute(face_id):
                broken_restriction = BrokenRestriction(face_id=face_id, restriction_id=restriction_id)
                broken_restriction.save()

                self.publisher.publish(encode(BrokenRestrictionMessage(broken_restriction_id=broken_restriction.id,
                                                                       face_id=face_id,
                                                                       restriction_id=restriction_id,
                                                                       trace_id=warden_trace)))
