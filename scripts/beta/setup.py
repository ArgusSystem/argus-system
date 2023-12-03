from scripts.alpha.setup import create_rule
from utils.orm.src.database import connect
from utils.orm.src.models import AreaType, PersonRole, RestrictionSeverity

# Must had run Alpha setup previously
if __name__ == "__main__":
    connect('argus', 'argus', 5432, 'argus', 'panoptes')

    trespasser_role_id = PersonRole.insert(name='trespasser').execute()

    public_area_type_id = AreaType.get(AreaType.name == 'public').id
    private_area_type_id = AreaType.get(AreaType.name == 'private').id

    critical_severity = RestrictionSeverity.get(RestrictionSeverity.name == 'critical').id

    warden = PersonRole.get(name='host').id

    create_rule('role',
                [trespasser_role_id],
                [public_area_type_id, private_area_type_id],
                '00:00', '23:59',
                critical_severity, warden)
