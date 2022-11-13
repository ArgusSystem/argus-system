from utils.orm.src import Person


def _get_people():
    people = Person.select(Person.id, Person.name, Person.photos).execute()
    return list(map(lambda person: {
        'id': person.id,
        'text': person.name,
        'photos': person.photos
    }, people))


class PeopleController:

    @staticmethod
    def make_routes(app):
        app.route('/people')(_get_people)
