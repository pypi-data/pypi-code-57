#
import csv


#
from government.models import Body
from government.models import Jurisdiction
import us


#
from election.models import Election
from election.models import Race


def load_office_descriptions(source_file, election_cycle, descriptor_field):
    """"""
    fed_govt_id = (
        Jurisdiction.objects.filter(name="U.S. Federal Government")
        .values_list("id", flat=True)
        .get()
    )

    us_house = Body.objects.get(jurisdiction_id=fed_govt_id, slug="house")

    with open(source_file) as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            row_state_obj = us.states.lookup(row["state"])

            Race.objects.filter(
                office__body_id=us_house.id,
                office__division__parent__name=row_state_obj.name,
                office__division__code=row["district"],
                cycle__slug=election_cycle,
            ).update(division_description=row[descriptor_field])
