from logging import getLogger

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.broken_rule_message import BrokenRuleMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.orm.src.database import connect
from utils.orm.src.models import BrokenRestriction
from utils.tracing.src.tracer import get_context, get_tracer

logger = getLogger(__name__)


class Warden:
    def __init__(self, tracer_configuration, db_configuration, publisher_configuration):
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-summarizer')
        self.db = connect(**db_configuration)
        self.publisher = Publisher.new(**publisher_configuration)

    def execute_with(self, message):
        matched_face_message: MatchedFaceMessage = decode(MatchedFaceMessage, message)

        with self.tracer.start_as_current_span('warden', context=get_context(matched_face_message.trace)):
            # Prepare sighting record
            broken_restrictions = self.db.execute_sql(
                'SELECT face.id AS face_id, restriction.id AS restriction_id '
                'FROM face '
                'LEFT JOIN videochunk ON video_chunk_id = videochunk.id '
                'LEFT JOIN camera ON camera_id = camera.id '
                'LEFT JOIN area ON area_id = area.id '
                'LEFT JOIN people ON person_id = people.id '
                'LEFT JOIN restriction ON restriction.role_id = people.role_id '
                'AND restriction.area_type_id = type_id '
                'AND to_char(timestamp \'epoch\' + face.timestamp * interval \'1 ms\', \'HH24:MI\') >= to_char(restriction.time_start, \'HH24:MI\') '
                'AND to_char(timestamp \'epoch\' + face.timestamp * interval \'1 ms\', \'HH24:MI\') < to_char(restriction.time_end, \'HH24:MI\') '
                'WHERE is_match = TRUE AND restriction.id IS NOT NULL AND face.id = ' + matched_face_message.face_id + ';'
            )

            for broken_restriction_result in broken_restrictions:
                face_id = broken_restriction_result[0]
                restriction_id = broken_restriction_result[1]

                BrokenRestriction(face_id=face_id, restriction_id=restriction_id).save()

                self.publisher.publish(encode(BrokenRuleMessage(face_id=face_id, restriction_id=restriction_id)))

        logger.info("Finished - %s", matched_face_message)
