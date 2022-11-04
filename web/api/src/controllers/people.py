from utils.orm.src import Person


def _get_people():
    people = Person.select(Person.id, Person.name).execute()
    return list(map(lambda person: {'id': person.id, 'text': person.name}, people))


class PeopleController:

    @staticmethod
    def make_routes(app):
        app.route('/people')(_get_people)
