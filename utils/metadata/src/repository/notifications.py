from utils.orm.src.models import Notification, Person, Restriction, RestrictionWarden, UserPerson


def create_notification(user_id, broken_restriction_id):
    Notification(user=user_id, broken_restriction_id=broken_restriction_id).save()


def get_offenders(offender_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .where(UserPerson.person == offender_id)
               .execute())


def get_wardens(restriction_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .join(Person, on=(Person.id == UserPerson.person_id))
               .join(RestrictionWarden, on=(RestrictionWarden.role_id == Person.role_id))
               .join(Restriction, on=(Restriction.id == RestrictionWarden.restriction_id))
               .where(Restriction.id == restriction_id)
               .distinct()
               .execute())
