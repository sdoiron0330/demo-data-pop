from nautobot.apps.jobs import Job, FileVar, register_jobs
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status
from csv import DictReader

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

class LoadLocationJob(Job):

    data_file = FileVar("Locations CSV file")

    def run(self, data_file):
        # too lazy to figure out how data files work
        data_lines = data_file.readlines()
        print(data_lines)
        for index, data in enumerate(data_lines):
            data = data.split(",")
            location = {
                "name": data[0],
                "city": data[1],
                "state": data[2]
            }
            if location["state"] in states:
                state_name = states[location["state"]]
            else:
                state_name = location["state"]
            state, _ = Location.objects.update_or_create(
                name=state_name,
                defaults={
                    "location_type": LocationType.objects.get(name="State")
                },
                create_defaults={
                    "status": Status.objects.get(name="Active")
                }
            )
            city, _ = Location.objects.update_or_create(
                name=location["city"],
                defaults={
                    "location_type": LocationType.objects.get(name="City")
                },
                create_defaults={
                    "status": Status.objects.get(name="Active")
                }
            )
            location_name = location["name"]
            if location_name.endswith("-DC"):
                location_type = LocationType.objects.get(name="Data Center")
            elif location_name.endswith("-BR"):
                location_type = LocationType.objects.get(name="Branch")
            else:
                self.logger.info(f"Unable to process location type in row {index + 1}")
                continue
            site, created = Location.objects.update_or_create(
                name=location_name,
                defaults={
                    "location_type": location_type
                },
                create_defaults={
                    "status": Status.objects.get(name="Active")
                }
            )
            self.logger.info(f"{'Created' if created else 'Updated'} site {location_name}")

register_jobs(LoadLocationJob)