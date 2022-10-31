from utils.orm.src import Person


def _get_people():
    people = Person.select().execute()

    return list(map(lambda person: person.name, people))


class PeopleController:

    @staticmethod
    def make_routes(app):
        app.route('/people')(_get_people)
