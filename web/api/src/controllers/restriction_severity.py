from utils.orm.src.models import RestrictionSeverity


def _get_severities():
    return [
        {
            'id': severity.id,
            'name': severity.name
        } for severity in RestrictionSeverity.select().order_by(RestrictionSeverity.value.asc())
    ]


class RestrictionSeveritiesController:

    @staticmethod
    def make_routes(app):
        app.route('/restriction_severities', methods=['GET'])(_get_severities)
